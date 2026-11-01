/* ============================================================
 *  合成大奶娃 · 重力感应 / 摇一摇
 *
 *  - 倾斜手机：水果往低的那一边滚（左右方向）
 *  - 晃动手机：水果跟着惯性甩来甩去、往上蹦——就像真的在摇一个装满水果的盒子，
 *    摇一摇能把卡住的缝隙抖开、让同级的撞到一起合成
 *  - 原本「向下」的重力保持不变，所以手机竖着拿、平放、斜着拿都能照常玩
 *
 *  只往 game.js 暴露的 __DNW__.ext 里写加速度（px/s²），不碰其他任何逻辑。
 *  关掉重力感应 = ext 归零 = 和原版一模一样。
 * ============================================================ */
(function () {
  'use strict';

  const DNW = window.__DNW__;
  if (!DNW || !DNW.ext) return;
  const ext = DNW.ext;

  const G  = 9.81;
  const PX = (DNW.GRAVITY || 2600) / G;   // 真实 1 m/s² ≈ 游戏里 265 px/s²

  /* —— 手感参数（单位都是真实世界的 m/s²） —— */
  const TILT_DEAD  = 0.7;    // 约 4° 以内的倾斜不算（手拿着本来就有点歪）
  const TILT_MAX   = 7.5;    // 侧向最多算到 ~50° 倾斜
  const TILT_GAIN  = 1.15;   // 倾斜力度（1 = 真实比例）
  const SHAKE_DEAD = 1.3;    // 手抖不算
  const SHAKE_GAIN = 2.0;    // 摇晃放大倍数：放大一点才爽
  const SHAKE_MAX  = 45;     // 单次甩动上限（≈12000 px/s²），防止水果互相穿模
  const SHAKE_FX   = 9;      // 超过这个算「猛摇」，按钮图标跟着抖一下
  const STALE_MS   = 300;    // 这么久没收到传感器数据就当作停了，加速度清零
  const NEED_MS    = 700;    // 这么久没数据、浏览器又要授权 → 提示「点我开启」
  const NONE_MS    = 2500;   // 开启后这么久一个有效数据都没有 = 设备没有传感器

  const PREF_KEY = 'danaiwa.tilt.v1';   // 记住玩家是否手动关掉过

  const stage = document.getElementById('stage');
  if (!stage) return;

  const DME = window.DeviceMotionEvent;
  const DOE = window.DeviceOrientationEvent;
  const isTouch = ('ontouchstart' in window) || (navigator.maxTouchPoints || 0) > 0;
  const needsPermission = !!(DME && typeof DME.requestPermission === 'function');
  const isIOS = /iPad|iPhone|iPod/.test(navigator.userAgent) ||
                (navigator.platform === 'MacIntel' && (navigator.maxTouchPoints || 0) > 1);

  /* 没有触屏（桌面电脑）或浏览器压根不支持：什么都不加，保持原样 */
  if (!DME || !isTouch) return;

  /* ---------------------------------------------------------
   *  开关按钮（浮在棋盘左上角，点它不会触发投放）
   * ------------------------------------------------------- */

  const btn = document.createElement('button');
  btn.type = 'button';
  btn.className = 'tilt-chip';
  btn.id = 'tiltBtn';
  btn.innerHTML = '<span class="tilt-ico" aria-hidden="true">📳</span><span class="tilt-lbl"></span>';
  const lbl = btn.querySelector('.tilt-lbl');
  const ico = btn.querySelector('.tilt-ico');
  /* 放在结束遮罩前面：遮罩弹出来时会盖住它 */
  const overlay = document.getElementById('overlay');
  stage.insertBefore(btn, overlay || null);
  stage.classList.add('has-tilt');

  /* 棋盘上按下就是瞄准/投放，这里拦住，别让点按钮变成扔水果 */
  ['pointerdown', 'pointerup', 'mousedown', 'touchstart', 'touchend'].forEach((t) => {
    btn.addEventListener(t, (e) => e.stopPropagation());
  });

  /* off / need（等授权）/ wait（等数据）/ on / denied / none（没传感器） */
  let mode = 'off';

  const TEXT = {
    off:    '重力感应·关',
    need:   '点我开启重力感应',
    wait:   '重力感应…',
    on:     '重力感应·开',
    denied: '未授权·重开网页再允许',
    none:   '没有重力传感器'
  };

  function setMode(m) {
    mode = m;
    lbl.textContent = TEXT[m] || '';
    btn.dataset.mode = m;
    btn.setAttribute('aria-pressed', String(m === 'on' || m === 'wait'));
    if (m !== 'on') { ext.ax = 0; ext.ay = 0; }
  }

  let noneTimer = 0;
  function hideLater() {
    clearTimeout(noneTimer);
    noneTimer = setTimeout(() => { if (mode === 'none') btn.hidden = true; }, 3000);
  }

  /* ---------------------------------------------------------
   *  坐标换算
   *
   *  W3C 约定：设备坐标 x 向右、y 朝屏幕顶部、z 朝屏幕外；
   *  静止时 accelerationIncludingGravity 指向「上」（平放 = (0, 0, +9.81)）。
   *  iOS Safari 历史上整组符号是反的，下面用 deviceorientation 的角度自动校准，
   *  拿不到角度时才按系统猜。
   * ------------------------------------------------------- */

  let sgn = isIOS ? -1 : 1;    // 原始数据 × sgn = 规范方向
  let vote = 0;                // 校准投票（饱和计数，越正越确定是规范方向）
  let ori = null;              // 最近一次 { beta, gamma, t }

  function screenAngle() {
    const so = window.screen && window.screen.orientation;
    if (so && typeof so.angle === 'number') return so.angle;
    if (typeof window.orientation === 'number') return window.orientation;
    return 0;
  }

  /* 用设备姿态角推出「规范方向下，静止时 accIG 应该指向哪」，跟实测比一比 */
  function calibrate(gx, gy, gz, now) {
    if (!ori || now - ori.t > 500) return;
    const mag = Math.sqrt(gx * gx + gy * gy + gz * gz);
    if (mag < 7.5 || mag > 12) return;          // 正在甩，数据不干净，不投票
    const b = ori.beta * Math.PI / 180;
    const g = ori.gamma * Math.PI / 180;
    const cb = Math.cos(b);
    /* 「上」在设备坐标里 = (-cosβ·sinγ, sinβ, cosβ·cosγ) */
    const ex = -cb * Math.sin(g), ey = Math.sin(b), ez = cb * Math.cos(g);
    const dot = (gx * ex + gy * ey + gz * ez) / mag;
    if (dot > 0.75) vote = Math.min(12, vote + 1);
    else if (dot < -0.75) vote = Math.max(-12, vote - 1);
    if (vote >= 4) sgn = 1;
    else if (vote <= -4) sgn = -1;
  }

  /* ---------------------------------------------------------
   *  传感器 → 加速度
   * ------------------------------------------------------- */

  const lp = { x: 0, y: 0, z: 0, init: false };   // 平滑后的重力（原始坐标）
  let lastAt = 0;
  let startedAt = 0;
  let fxUntil = 0;

  function onOrient(e) {
    if (e.beta == null || e.gamma == null) return;
    ori = { beta: e.beta, gamma: e.gamma, t: performance.now() };
  }

  function onMotion(e) {
    if (!listening) return;
    const ig = e.accelerationIncludingGravity;
    if (!ig || ig.x == null || ig.y == null) return;
    const la = e.acceleration;
    const now = performance.now();
    const iz = ig.z || 0;

    /* 1) 拆成「重力」和「手机自身的加速度」 */
    let gx, gy, gz, lx, ly;
    if (la && la.x != null && la.y != null) {
      /* 系统已经帮忙拆好了：重力 = 含重力 − 线性加速度 */
      gx = ig.x - la.x; gy = ig.y - la.y; gz = iz - (la.z || 0);
      lx = la.x; ly = la.y;
      if (!lp.init) { lp.x = gx; lp.y = gy; lp.z = gz; lp.init = true; }
      lp.x += (gx - lp.x) * 0.35;
      lp.y += (gy - lp.y) * 0.35;
      lp.z += (gz - lp.z) * 0.35;
    } else {
      /* 只有含重力的数据：低通滤波估重力，剩下的就是甩动 */
      if (!lp.init) { lp.x = ig.x; lp.y = ig.y; lp.z = iz; lp.init = true; }
      lp.x += (ig.x - lp.x) * 0.1;
      lp.y += (ig.y - lp.y) * 0.1;
      lp.z += (iz - lp.z) * 0.1;
      lx = ig.x - lp.x; ly = ig.y - lp.y;
    }
    gx = lp.x; gy = lp.y; gz = lp.z;

    calibrate(gx, gy, gz, now);
    lastAt = now;
    if (mode !== 'on') setMode('on');

    /* 2) 转到屏幕坐标：设备坐标(y 朝上) 按屏幕旋转角转 +θ，再翻成画布的 y 朝下 */
    const th = screenAngle() * Math.PI / 180;
    const c = Math.cos(th), s = Math.sin(th);

    /* 「下」= -规范重力读数；只取左右分量做倾斜 */
    const dx = -sgn * gx, dy = -sgn * gy;
    const downX = dx * c - dy * s;

    /* 盒子里的惯性力 = -手机加速度 */
    const ax = -sgn * lx, ay = -sgn * ly;
    const fX = ax * c - ay * s;
    const fY = -(ax * s + ay * c);

    /* 3) 倾斜：死区 + 上限 */
    let tilt = 0;
    const at = Math.abs(downX);
    if (at > TILT_DEAD) tilt = Math.sign(downX) * Math.min(TILT_MAX, at - TILT_DEAD);

    /* 4) 摇晃：死区 + 放大 + 上限 */
    let sx = 0, sy = 0;
    const m = Math.sqrt(fX * fX + fY * fY);
    if (m > SHAKE_DEAD) {
      let k = (m - SHAKE_DEAD) / m * SHAKE_GAIN;
      const mm = m * k;
      if (mm > SHAKE_MAX) k *= SHAKE_MAX / mm;
      sx = fX * k;
      sy = fY * k;
    }

    ext.ax = (tilt * TILT_GAIN + sx) * PX;
    ext.ay = sy * PX;

    if (m > SHAKE_FX && now > fxUntil) {
      fxUntil = now + 350;
      ico.classList.remove('wiggle');
      void ico.offsetWidth;
      ico.classList.add('wiggle');
    }
  }

  /* 传感器停了 / 切后台：别让最后一次的加速度一直顶着 */
  setInterval(() => {
    const now = performance.now();
    if (mode === 'on' && now - lastAt > STALE_MS) { ext.ax = 0; ext.ay = 0; }
    if (mode === 'wait') {
      const waited = now - startedAt;
      if (needsPermission && !asked && waited > NEED_MS) {
        setMode('need');                          // 继续监听；等玩家点一下再申请
      } else if (waited > NONE_MS) {
        setMode('none'); stopListening(); hideLater();
      }
    }
  }, 150);

  document.addEventListener('visibilitychange', () => {
    if (document.hidden) { ext.ax = 0; ext.ay = 0; }
  });

  /* ---------------------------------------------------------
   *  开 / 关 / 授权
   *
   *  不靠「有没有 requestPermission」来猜平台（新版 Chrome 也有这个函数）：
   *  一律先监听，有数据就直接开；等一会儿还没数据、且浏览器要授权（iOS），
   *  才显示「点我开启」，在玩家下一次点击里申请。
   * ------------------------------------------------------- */

  let listening = false;
  let asked = false;          // 本次页面已经在用户点击里申请过授权了

  function startListening() {
    if (!listening) {
      window.addEventListener('devicemotion', onMotion);
      if (DOE) window.addEventListener('deviceorientation', onOrient);
      listening = true;
    }
    lp.init = false;
    startedAt = performance.now();
    setMode('wait');
  }

  function stopListening() {
    if (listening) {
      window.removeEventListener('devicemotion', onMotion);
      if (DOE) window.removeEventListener('deviceorientation', onOrient);
      listening = false;
    }
    ext.ax = 0; ext.ay = 0;
  }

  /* 必须在用户点击里调用（iOS 13+）。动作和方向是同一个授权，一起要 */
  function requestInGesture() {
    asked = true;
    let p;
    try { p = DME.requestPermission(); } catch (err) { p = Promise.reject(err); }
    if (DOE && typeof DOE.requestPermission === 'function') {
      try { DOE.requestPermission().catch(() => {}); } catch (err) { /* 拿不到方向也能玩，只是少了自动校准 */ }
    }
    p.then((r) => {
      if (r === 'denied') { if (mode !== 'on') setMode('denied'); return; }
      if (mode !== 'on') startListening();       // granted / prompt：等数据来
    }, () => { if (mode !== 'on') setMode('denied'); });
  }

  function turnOn() {
    try { localStorage.setItem(PREF_KEY, 'on'); } catch (e) { /* 忽略 */ }
    btn.hidden = false;
    startListening();
    if (needsPermission) requestInGesture();   // 这里一定在点击里，顺手申请
  }

  function turnOff() {
    try { localStorage.setItem(PREF_KEY, 'off'); } catch (e) { /* 忽略 */ }
    stopListening();
    setMode('off');
  }

  btn.addEventListener('click', (e) => {
    e.stopPropagation();
    if (mode === 'on' || mode === 'wait') turnOff();
    else turnOn();
  });

  /* 玩家在棋盘上松手（这是一次用户手势）：如果还在等授权，顺便申请 */
  stage.addEventListener('touchend', () => {
    if (mode === 'need' && !asked) requestInGesture();
  });

  /* ---------------------------------------------------------
   *  启动：默认开启
   * ------------------------------------------------------- */

  let pref = null;
  try { pref = localStorage.getItem(PREF_KEY); } catch (e) { /* 忽略 */ }

  if (pref === 'off') {
    setMode('off');
  } else {
    startListening();
    /* iOS：本次会话已经授权过的话，不用点击也会直接给 granted */
    if (needsPermission) {
      try { DME.requestPermission().then(() => {}, () => {}); } catch (e) { /* 忽略 */ }
    }
  }

  /* 调试句柄 */
  window.__DNW_TILT__ = {
    get mode() { return mode; },
    get sign() { return sgn; },
    get vote() { return vote; },
    on: turnOn, off: turnOff
  };
})();

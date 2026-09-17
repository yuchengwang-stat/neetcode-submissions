class Solution:
    def countSubstrings(self, s: str) -> int:
        ans = 0
        n = len(s)
        for i in range(n):
            l = i
            r = i
            while l >= 0 and r <= n-1:
                if s[l] == s[r]:
                    ans += 1
                else:
                    break
                l -= 1
                r += 1
            l = i
            r = i + 1
            while l>=0 and r<=n-1:
                if s[l] == s[r]:
                    ans +=1
                else:
                    break
                l-=1
                r += 1
        return ans

        
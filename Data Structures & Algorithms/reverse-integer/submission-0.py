class Solution:
    def reverse(self, x: int) -> int:
        sign = -1 if x < 0 else 1
        upper = 2 ** 31 - 1
        lower = -2 ** 31 
        x = abs(x)
        r = 0
        while x != 0:
            if (lower - x%10)/10 <= r <= (upper - x%10)/10:
                r = r*10 + x % 10
            else:
                return 0
            x = x // 10
        r *= sign
        return r



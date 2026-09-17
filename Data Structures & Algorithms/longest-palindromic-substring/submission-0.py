class Solution:
    def longestPalindrome(self, s: str) -> str:
        n = len(s)
        ans = ""
        for i in range(n):
            for l, r in ((i,i),(i,i+1)):
                while l >=0 and r <= n-1:
                    if s[l] == s[r]:
                        l -= 1
                        r += 1
                    else:
                        break
                ans = s[l+1:r] if len(ans) < len(s[l+1:r]) else ans
        return ans
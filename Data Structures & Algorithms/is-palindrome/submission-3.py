class Solution:
    def isPalindrome(self, s: str) -> bool:
        n = len(s)
        l = 0
        r = n-1
        while l<=r:
            while l <= n-1 and not s[l].isalnum():
                l += 1
            while r >= 0 and not s[r].isalnum():
                r -= 1
            if l <= n-1 and r >= 0 and s[l].lower() != s[r].lower():
                return False
            else:
                l+=1
                r-=1
        return True
class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        cnt_s = Counter(s)
        cnt_t = Counter(t)
        return cnt_s == cnt_t
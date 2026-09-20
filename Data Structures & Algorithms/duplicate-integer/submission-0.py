class Solution:
    def hasDuplicate(self, nums: List[int]) -> bool:
        cnt = Counter()
        for c in nums:
            cnt[c] += 1
            if cnt[c] > 1:
                return True
        return False
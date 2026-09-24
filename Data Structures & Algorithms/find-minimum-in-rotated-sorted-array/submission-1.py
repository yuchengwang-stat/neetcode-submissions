class Solution:
    def findMin(self, nums: List[int]) -> int:
        l = 0 
        r = len(nums) - 2
        if len(nums) == 1:
            return nums[0]
        target = nums[-1]
        while l <= r:
            m = (l + r) // 2
            if nums[m] < target:
                r = m - 1
            else:
                l = m + 1
        return nums[l]
                

            
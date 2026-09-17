class Solution:
    def subsetsWithDup(self, nums: List[int]) -> List[List[int]]:
        path = []
        ans = []
        n = len(nums)
        ans.append([])
        nums.sort()
        def dfs(i):
            if i == n:
                return
            for j in range(i,n):
                if j > i and nums[j] == nums[j-1]:
                    continue
                path.append(nums[j])
                ans.append(path[:])
                dfs(j + 1)
                path.pop()
        dfs(0)
        return ans
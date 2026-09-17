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
            used = []
            for j in range(i,n):
                if nums[j] in used:
                    continue
                path.append(nums[j])
                used.append(nums[j])
                ans.append(path[:])
                dfs(j + 1)
                path.pop()
        dfs(0)
        return ans
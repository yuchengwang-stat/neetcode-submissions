class Solution:
    def combinationSum2(self, candidates: List[int], target: int) -> List[List[int]]:
        path = []
        ans = []
        candidates.sort()
        n = len(candidates)
        def dfs(i,s):
            if sum(path) == target:
                ans.append(path[:])
                return
            for j in range(i,n):
                if j > i and candidates[j - 1] == candidates[j]:
                    continue
                if s> target:
                    return
                path.append(candidates[j])
                dfs(j+1,s + candidates[j])
                path.pop()
        dfs(0,0)
        return ans
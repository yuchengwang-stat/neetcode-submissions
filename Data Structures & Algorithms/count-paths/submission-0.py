from functools import cache
class Solution:
    def uniquePaths(self, m: int, n: int) -> int:
        @cache
        def dfs(i,j):
            if i == 0 and j == 0:
                return 1
            if i != 0 and j != 0:
                return dfs(i-1,j) + dfs(i,j-1)
            if i != 0:
                return dfs(i-1,j)
            if j != 0:
                return dfs(i,j-1)
        
        return dfs(m-1,n-1)



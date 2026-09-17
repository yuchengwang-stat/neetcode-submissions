
class Solution:
    def pacificAtlantic(self, heights: List[List[int]]) -> List[List[int]]:
        n = len(heights)
        m = len(heights[0])
        def dfs(i,j,visit,prev):
            if not (0<=i<=n-1 and 0<=j<=m-1) or (i,j) in visit or heights[i][j] < prev :
                return
            visit.add((i,j))
            dfs(i + 1,j,visit,heights[i][j])
            dfs(i - 1,j,visit,heights[i][j])
            dfs(i ,j+1,visit,heights[i][j])
            dfs(i ,j-1,visit,heights[i][j])
        atl = set()
        pac = set()
        for i in range(n):
            dfs(i,0,pac,0)
            dfs(i,m-1,atl,0)
        for i in range(m):
            dfs(0,i,pac,0)
            dfs(n-1,i,atl,0)
        return [[i,j] for i,j in pac & atl]
            


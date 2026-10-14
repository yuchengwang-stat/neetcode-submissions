class Solution:
    def generateParenthesis(self, n: int) -> List[str]:
        ans = []
        path = []
        def dfs(l,r):
            if l+r == 2 * n:
                ans.append("".join(path[:]))
                return
            if r<n and l-r>0:
                path.append(")")
                dfs(l,r+1)
                path.pop()
            if l<n:
                path.append("(")
                dfs(l+1,r)
                path.pop()
            
        dfs(0,0)
        return ans

                


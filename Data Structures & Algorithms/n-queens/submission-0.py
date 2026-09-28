class Solution:
    def solveNQueens(self, n: int) -> List[List[str]]:
        ans = []
        path = []
        visited_col = Counter()
        visited_left = Counter()
        visited_right = Counter()
        def dfs(i):
            if i == n:
                ans.append(path[:])
                return 
            for j in range(n):
                if visited_col[j] == 1 or visited_left[i + j] == 1 or visited_right[j - i] == 1:
                    continue
                path.append("".join(j * ["."] + ["Q"] + (n-j-1)*["."]))
                visited_col[j] = 1
                visited_left[i + j] = 1
                visited_right[j - i] = 1
                dfs(i + 1)
                visited_col[j] -= 1
                visited_left[i + j] -= 1
                visited_right[j - i] -= 1
                path.pop()
        dfs(0)
        return ans
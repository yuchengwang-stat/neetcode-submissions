class Solution:
    def exist(self, board: List[List[str]], word: str) -> bool:
        n = len(word)
        y = len(board)
        x = len(board[0])
        visited = [[0 for _ in range(x)] for _ in range(y)]
        dirs = [(1,0),(0,1),(-1,0),(0,-1)]
        def dfs(i,j,k):
            visited[i][j] = 1
            if k == n - 1 and board[i][j] == word[n-1]:
                return True
            res = []
            if board[i][j] == word[k]:
                for mx, my in dirs:
                    if y-1 >= i + mx >= 0 and x-1 >= j + my >= 0 and visited[i + mx][j + my] == 0:
                        res.append(dfs(i + mx,j + my,k+1))
                        visited[i + mx][j + my] = 0
                return any(res)
            return False
        starting = []
        for i in range(y):
            for j in range(x):
                if board[i][j] == word[0]:
                    starting.append([i,j])
        ans = []
        for i,j in starting:
            ans.append(dfs(i,j,0))
            visited[i][j] = 0
        return any(ans)

class Solution:
    def spiralOrder(self, matrix: List[List[int]]) -> List[int]:
        ans = []
        m = len(matrix)
        n = len(matrix[0])
        visit = [[0 for i in range(n)] for _ in range(m)]
        current = [0,0]
        dir = [(0,1),(1,0),(0,-1),(-1,0)]
        d = 0
        ty = [0,0]
        while True:
            ty[0] = current[0] + dir[d][0]
            ty[1] = current[1] + dir[d][1]
            if ty[0] > m-1 or ty[1] > n-1 or ty[0] < 0 or ty[1] < 0 or visit[ty[0]][ty[1]] == 1:
                d = (d+1) % 4
                ty[0] = current[0] + dir[d][0]
                ty[1] = current[1] + dir[d][1]
                if ty[0] > m-1 or ty[1] > n-1 or ty[0] < 0 or ty[1] < 0 or visit[ty[0]][ty[1]] == 1:
                    ans.append(matrix[current[0]][current[1]])
                    break
                continue
            else:
                visit[current[0]][current[1]] = 1
                ans.append(matrix[current[0]][current[1]])
                current[0] += dir[d][0]
                current[1] += dir[d][1]
        return ans
            
            
            

        
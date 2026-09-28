class Solution:
    def setZeroes(self, matrix: List[List[int]]) -> None:
        m, n = len(matrix), len(matrix[0])
        row_zeros = any(x == 0 for x in matrix[0])
        col_zeros = any(row[0] == 0 for row in matrix)
        for i in range(1,m):
            for j in range(1,n):
                if matrix[i][j] == 0:
                    matrix[0][j] = 0
                    matrix[i][0] = 0
        for i in range(1,m):
            for j in range(1,n):
                if matrix[0][j] == 0 or matrix[i][0] == 0:
                    matrix[i][j] = 0
        if row_zeros is True:
            for j in range(n):
                matrix[0][j] = 0
        if col_zeros is True:
            for i in range(m):
                matrix[i][0] = 0
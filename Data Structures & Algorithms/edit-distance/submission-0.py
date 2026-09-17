from functools import cache
class Solution:
    def minDistance(self, word1: str, word2: str) -> int:
        n = len(word1)
        m = len(word2)
        i = n-1
        j = m-1

        @cache
        def dfs(i, j):
            if i < 0 or j < 0:
                return abs(i - j)
            if word1[i] != word2[j]:
                return min(dfs(i-1,j),dfs(i,j-1), dfs(i-1, j-1) ) + 1
            if word1[i] == word2[j]:
                return dfs(i-1, j-1)
        
        return dfs(n-1,m-1)
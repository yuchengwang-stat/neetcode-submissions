from functools import cache
class Solution:
    def wordBreak(self, s: str, wordDict: List[str]) -> bool:
        n = len(s)
        @cache
        def dfs(i,j):
            if j == n:
                if s[i:j] in wordDict:
                    return True
                else:
                    return False
            else:
                if s[i:j] in wordDict:
                    return dfs(j,j+1) or dfs(i,j+1)
                else:
                    return dfs(i,j+1)
        return dfs(0,1)
            
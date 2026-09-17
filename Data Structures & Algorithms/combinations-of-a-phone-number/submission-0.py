MAP = ["","","abc","def","ghi","jkl","mno","pqrs","tuv","wxyz"]
class Solution:
    def letterCombinations(self, digits: str) -> List[str]:
        n = len(digits)
        if n == 0:
            return []
        path = []
        ans = []
        def dfs(i):
            if i == n:
                ans.append("".join(path[:]))
                return
            current = MAP[int(digits[i])]
            m = len(current)
            for j in range(m):
                path.append(current[j])
                dfs(i + 1)
                path.pop()
        dfs(0)
        return ans

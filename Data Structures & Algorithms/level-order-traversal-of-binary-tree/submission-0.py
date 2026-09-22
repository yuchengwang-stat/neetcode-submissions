# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
from collections import deque
class Solution:
    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        q = deque()
        q.append(root)
        ans = []
        l = len(q)
        while q:
            res = []
            for _ in range(l):
                cur = q.popleft()
                if cur:
                    q.append(cur.left)
                    q.append(cur.right)
                    res.append(cur.val)
            l = len(q)
            if res:
                ans.append(res)
        return ans


        
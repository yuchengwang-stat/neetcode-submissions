# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

class Solution:
    def rightSideView(self, root: Optional[TreeNode]) -> List[int]:
        right = []
        cnt = 0
        def dfs(node,depth):
            nonlocal cnt
            if not node:
                return
            if depth >= cnt:
                right.append(node.val)
                cnt += 1
            dfs(node.right,depth+1)
            dfs(node.left,depth+1)
        dfs(root,0)
        return right
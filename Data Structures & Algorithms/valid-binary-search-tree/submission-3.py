# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

class Solution:
    def isValidBST(self, root: Optional[TreeNode]) -> bool:
        BST_list = []
        prev = None
        def BST(node):
            nonlocal prev
            if not node:
                return True
            if not BST(node.left):
                return False
            if prev and node.val <= prev.val:
                return False
            prev = node
            if not BST(node.right):
                return False
            return True
        return BST(root)
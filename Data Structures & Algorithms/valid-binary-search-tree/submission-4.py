# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
from math import inf
class Solution:
    def isValidBST(self, root: Optional[TreeNode]) -> bool:
        def BST(node,lo,hi):
            if not node:
                return True
            if node.val <= lo or node.val >= hi:
                return False
            if not BST(node.left, lo, node.val):
                return False
            if not BST(node.right, node.val, hi):
                return False

            return True
        return BST(root,-inf, inf)
        
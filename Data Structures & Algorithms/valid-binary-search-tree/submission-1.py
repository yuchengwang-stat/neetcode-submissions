# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

class Solution:
    def isValidBST(self, root: Optional[TreeNode]) -> bool:
        BST_list = []
        def BST(node):
            if not node:
                return
            BST(node.left)
            BST_list.append(node.val)
            BST(node.right)
        BST(root)
        n = len(BST_list)
        print(BST_list)
        for i in range(n):
            if i==0:
                continue
            if BST_list[i]<=BST_list[i-1]:
                return False
        return True
            

            
            
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
def reverse(node):
    cur = node
    pre = None
    while cur:
        nxt = cur.next
        cur.next = pre
        pre = cur
        cur = nxt
    return pre
class Solution:
    def reorderList(self, head: Optional[ListNode]) -> None:
        slow = head
        fast = head
        
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
        
        tail = reverse(slow)
        n1 = head
        n2 = tail
        while n1 and n2 and n1 is not n2:
            nxt1 = n1.next
            nxt2 = n2.next
            n1.next = n2
            if nxt1 is not n2:
                n2.next = nxt1
            else:
                n2.next = None
            n1 = nxt1
            n2 = nxt2


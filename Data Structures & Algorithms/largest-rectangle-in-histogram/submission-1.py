class Solution:
    def largestRectangleArea(self, heights: List[int]) -> int:
        stack = []
        mx = 0
        h = [0] + heights + [0]
        n = len(h)
        for i in range(n):
            while stack and h[stack[-1]] > h[i]:
                top = stack.pop()
                l = stack[-1]
                size = (i - l - 1) * h[top]
                mx = max(mx,size)
            stack.append(i)
        return mx
                
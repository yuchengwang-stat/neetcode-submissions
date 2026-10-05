class Solution:
    def evalRPN(self, tokens: List[str]) -> int:
        stack = []
        for i,x in enumerate(tokens):
            if x not in "*+-/":
                stack.append(int(x))
                continue
            a = int(stack.pop())
            b = int(stack.pop())
            if x == "+":
                stack.append(a + b)
            if x == "-":
                stack.append(b - a)
            if x == "*":
                stack.append(a * b)
            if x == "/":
                stack.append(int(b / a))
        return stack[-1]    
                
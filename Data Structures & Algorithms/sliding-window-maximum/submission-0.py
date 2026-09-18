import heapq
class Solution:
    def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:
        l = 0
        r = k
        h = [(-nums[i],i) for i in range(l,r)]
        heapq.heapify(h)
        ans = []
        n = len(nums)
        while r <= n:
            if l!=0:
                heapq.heappush(h,(-nums[r-1],r-1))
            while h[0][1]<l:
                heapq.heappop(h)
            ans.append(-h[0][0])
            r+=1
            l+=1
        return ans
        
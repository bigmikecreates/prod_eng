from collections import deque

class FIFOCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}
        self.order = deque()

    def get(self, key):
        return self.cache.get(key, -1)
    
    def put(self, key, value):
        if key in self.cache:
            self.cache[key] = value
            return
        
        if len(self.cache) >= self.capacity:
            oldest_key = self.order.popleft()
            del self.cache[oldest_key]

        self.cache[key] = value
        self.order.append(key)
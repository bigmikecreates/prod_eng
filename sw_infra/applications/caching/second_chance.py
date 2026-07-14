from collections import deque

class SecondChanceCache:
    """
    FIFO cache with a reference bit.

    Recently accessed entries receive a second chance before eviction.
    """

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}
        self.queue = deque()

    def get(self, key):
        if key not in self.cache:
            return -1
        
        self.cache[key]["ref"] = 1
        return self.cache[key]["value"]

    def put(self, key, value):
        if self.capacity <= 0:
            return

        if key in self.cache:
            self.cache[key]["value"] = value
            self.cache[key]["ref"] = 1
            return

        while len(self.cache) >= self.capacity:
            oldest_key = self.queue.popleft()

            if self.cache[oldest_key]["ref"] == 1:
                self.cache[oldest_key]["ref"] = 0
                self.queue.append(oldest_key)
            else:
                del self.cache[oldest_key]
                break

        self.cache[key] = {"value": value, "ref": 1}
        self.queue.append(key)


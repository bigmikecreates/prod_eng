"""
First-In, First-Out (FIFO) cache eviction policy.

Overview
--------
FIFO evicts the item that has been in the cache the longest, regardless of
how frequently or how recently it has been accessed.

The cache maintains insertion order. When the cache reaches its capacity,
the oldest inserted entry is removed to make room for the new one.

Example
-------
Capacity = 3

put(A)
put(B)
put(C)

Cache:
[A, B, C]

put(D)

Evict A

Cache:
[B, C, D]

Characteristics
---------------
- Does not consider access frequency.
- Does not consider access recency.
- Extremely simple implementation.
- Low memory overhead.

Advantages
----------
- Easy to understand and implement.
- Predictable eviction behaviour.
- Constant-time insertion and eviction.

Disadvantages
-------------
- Frequently accessed items may still be evicted.
- Generally lower cache hit rates than LRU or LFU.

Time Complexity
---------------
get():   O(1)
put():   O(1)
evict(): O(1)

Space Complexity
----------------
O(capacity)

Common Use Cases
----------------
- Simple bounded queues
- Streaming systems
- Lightweight embedded caches
- Systems where simplicity is preferred over cache efficiency
"""

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
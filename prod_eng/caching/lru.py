"""
Least Recently Used (LRU) cache eviction policy.

Overview
--------
LRU evicts the item that has not been accessed for the longest period of time.

The assumption behind LRU is temporal locality:
items accessed recently are more likely to be accessed again soon.

Each access promotes an entry to the most recently used position. When
capacity is exceeded, the least recently used entry is evicted.

Example
-------
Capacity = 3

put(A)
put(B)
put(C)

Cache:
[A, B, C]

get(A)

Cache:
[B, C, A]

put(D)

Evict B

Cache:
[C, A, D]

Characteristics
---------------
- Tracks recency of access.
- Does not track frequency of access.
- Commonly implemented using a hash map and doubly linked list.

Advantages
----------
- Excellent general-purpose cache policy.
- High cache hit rate for workloads exhibiting temporal locality.
- Widely used in databases, browsers, and distributed systems.

Disadvantages
-------------
- Sequential scans can evict useful data.
- Frequently used but temporarily inactive entries may be removed.

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
- Web browsers
- API response caches
- Database page caches
- Redis-like systems
- General-purpose in-memory caches
"""

from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = OrderedDict()

    def get(self, key):
        if key not in self.cache:
            return -1
        
        self.cache.move_to_end(key)
        return self.cache[key]
    
    def put(self, key, value):
        if key in self.cache:
            self.cache.move_to_end(key)

        self.cache[key] = value

        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)
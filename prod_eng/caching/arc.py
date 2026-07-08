"""
Adaptive Replacement Cache (ARC) eviction policy.

Overview
--------
ARC dynamically balances recency and frequency to improve cache
performance across changing workloads.

Instead of relying solely on LRU or LFU, ARC maintains multiple lists:

- Recent entries
- Frequently used entries
- Recent history
- Frequent history

The algorithm continuously adapts how much space each list receives based
on observed access patterns.

Characteristics
---------------
- Adaptive algorithm.
- Combines recency and frequency.
- Automatically tunes itself.

Advantages
----------
- Resistant to sequential scans.
- Consistently high cache hit rates.
- Adapts without manual tuning.

Disadvantages
-------------
- Significantly more complex than LRU.
- More bookkeeping required.
- Historically affected by software patents.

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
- Enterprise storage systems
- Filesystems
- Database engines
- High-performance storage appliances
"""

from collections import deque

class ARCCache:
    """
    Adaptive Replacement Cache

    Balances recency and frequency using two real caches and two ghost caches.
    """

    def __init__(self, capacity: int):
        self.capacity = capacity

        self.t1 = OrderedDict() # recent cache
        self.t2 = OrderedDict() # frequent cache
        self.b1 = OrderedDict() # recent ghost
        self.b2 = OrderedDict() # frequent ghost

        self.p = 0  # adaptive target size for T1

    def get(self, key):
        if key in self.t1:
            value = self.t1.pop(key)
            self.t2[key] = value
            return value

        if key in self.t2:
            value = self.t2.pop(key)
            self.t2[key] = value
            return value

        return -1

    def put(self, key, value):
        if self.capacity <= 0:
        return


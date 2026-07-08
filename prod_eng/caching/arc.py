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
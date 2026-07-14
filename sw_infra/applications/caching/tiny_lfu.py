"""
Window TinyLFU (W-TinyLFU) cache eviction policy.

Overview
--------
W-TinyLFU is a modern cache replacement algorithm that combines
admission control with frequency-based eviction.

Unlike traditional cache policies, new entries are not automatically
admitted into the cache. Instead, a compact frequency sketch estimates
whether a candidate entry is likely to improve the overall cache hit
rate.

The algorithm typically consists of:

- A small LRU admission window
- A frequency estimator (TinyLFU sketch)
- A segmented main cache

Only entries that are predicted to be valuable are retained.

Characteristics
---------------
- Combines recency and frequency.
- Uses probabilistic frequency estimation.
- Includes admission control before insertion.

Advantages
----------
- State-of-the-art cache hit rates.
- Resistant to cache pollution.
- Excellent performance across diverse workloads.

Disadvantages
-------------
- Most complex algorithm in this collection.
- Requires probabilistic data structures.
- Higher implementation complexity.

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
- Caffeine (Java)
- Modern application caches
- High-performance distributed systems
- Large-scale backend services
"""
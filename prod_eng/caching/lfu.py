"""
Least Frequently Used (LFU) cache eviction policy.

Overview
--------
LFU evicts the item that has been accessed the fewest number of times.

Rather than tracking recency, LFU maintains an access count for every
cached entry. When eviction is required, the entry with the lowest
access frequency is removed.

Many implementations use LRU as a tie-breaker for entries with the same
frequency.

Example
-------
Capacity = 3

A -> 15 accesses
B -> 2 accesses
C -> 8 accesses

put(D)

Evict B

Characteristics
---------------
- Tracks access frequency.
- Often groups entries by frequency buckets.
- Frequently implemented using multiple linked lists.

Advantages
----------
- Excellent for stable workloads with repeatedly accessed data.
- Frequently used items remain in the cache longer.

Disadvantages
-------------
- More complex implementation than LRU.
- Historical popularity can keep stale entries alive.
- Higher bookkeeping overhead.

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
- Database buffer managers
- Recommendation systems
- Long-running backend services
- Machine learning inference caches
"""
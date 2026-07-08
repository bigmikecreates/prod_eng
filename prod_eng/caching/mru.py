"""
Most Recently Used (MRU) cache eviction policy.

Overview
--------
MRU evicts the item that was accessed most recently.

Unlike LRU, MRU assumes that recently accessed entries are less likely
to be accessed again immediately.

Although uncommon, MRU performs well for certain sequential access
patterns where previously accessed data is unlikely to be reused.

Example
-------
Capacity = 3

put(A)
put(B)
put(C)

Cache:
[A, B, C]

get(C)

Cache:
[A, B, C]

put(D)

Evict C

Cache:
[A, B, D]

Characteristics
---------------
- Tracks recency.
- Removes the newest entry.
- Opposite behaviour to LRU.

Advantages
----------
- Performs well for sequential scans.
- Avoids keeping recently processed data.

Disadvantages
-------------
- Poor performance for most general-purpose workloads.
- Rarely used compared to LRU.

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
- Sequential file processing
- Database scan workloads
- Certain scientific computing applications
"""
"""
CLOCK cache eviction policy.

Overview
--------
CLOCK is an efficient approximation of Least Recently Used (LRU).

Instead of maintaining a fully ordered linked list, CLOCK arranges cache
entries in a circular buffer. Each entry maintains a reference bit that
indicates whether it has been accessed recently.

When eviction is required, a rotating pointer examines entries:

- If the reference bit is 1, it is cleared and the pointer advances.
- If the reference bit is 0, the entry is evicted.

This approach approximates LRU while significantly reducing maintenance
overhead.

Characteristics
---------------
- Approximate LRU.
- Low bookkeeping cost.
- Circular traversal using a clock hand.

Advantages
----------
- Lower memory overhead than exact LRU.
- Excellent scalability.
- Widely used in operating systems.

Disadvantages
-------------
- Only approximates true LRU.
- Can occasionally evict a recently useful page.

Time Complexity
---------------
Average get():   O(1)
Average put():   O(1)
Average evict(): O(1)

Space Complexity
----------------
O(capacity)

Common Use Cases
----------------
- Operating system page replacement
- Virtual memory management
- Large memory caches
"""
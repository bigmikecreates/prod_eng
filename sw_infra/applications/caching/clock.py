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

class ClockEntry:
    """
    Stores one cache entry and its reference bit.
    """

    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.ref = 1

class ClockCache:
    """
    CLOCK cache.

    Approximates LRU using a circular buffer and rotating clock hand.
    """

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.entries = [None] * capacity
        self.cache = {}
        self.hand = 0
        self.size = 0

    def get(self, key):
        if key not in self.cache:
            return -1

        index = self.cache[key]
        entry = self.entries[index]
        entry.ref = 1

        return entry.value

    def put (self, key, value):
        if self.capacity <= 0:
            return

        if key in self.cache:
            index = self.cache[key]
            entry = self.entries[index]
            entry.value = value
            entry.ref = 1
            return

        if self.size < self.capacity:
            entry = ClockEntry(key, value)
            self.entries[self.size] = entry
            self.cache[key] = self.size
            self.size += 1
            return

        while True:
            entry = self.entries[self.hand]

            if entry.ref == 1:
                entry.ref = 0
                self.hand = (self.hand + 1) % self.capacity
            else:
                del self.cache[entry.key]

                new_entry = ClockEntry(key, value)
                self.entries[self.hand] = new_entry
                self.cache[key] = self.hand

                self.hand = (self.hand + 1) % self.capacity
                return
    

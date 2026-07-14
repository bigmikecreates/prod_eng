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

class Node:
    class Node:
        """
        Represents a single cache entry.

        Stores the key, value, access frequency, and linked list pointers.
        """

    def __init__(self, key=None, value=None):
        self.key = key
        self.value = value
        self.freq = 1
        self.prev = None
        self.next = None

class DoublyLinkedList:
    """
    Stores nodes that share the same access frequency.

    Nodes are ordered by recency to provide LRU tie-breaking.
    """

    def __init__(self):
        self.head = Node()
        self.tail = Node()

        self.head.next = self.tail
        self.tail.prev = self.head

        self.size = 0

    def append(self, node: Node) -> None:
        previous = self.tail.prev

        previous.next = node
        node.prev = previous

        node.next = self.tail
        self.tail.prev = node

        self.size += 1

    def remove(self, node: Node) -> None:

        previous = node.prev
        nxt = node.next

        previous.next = nxt
        nxt.prev = previous
        
        self.size -= 1

    def pop_left(self) -> Node:
        
        if self.size == 0:
            raise IndexError("Frequency bucket is empty.")

        node = self.head.next
        self.remove(node)

        return node

class LFUCache:
    """
    Least Frequently Used (LFU) cache.

    Evicts the least frequently accessed entry. When multiple entries share
    the same frequency, the least recently used entry is evicted.
    """

    def __init__(self, capacity: int):
        self.capacity = capacity

        self.cache = {}

        self.frequency_lists = {}

        self.minimum_frequency = 0

    def _update_frequency(self, node: Node) -> None:
        """
        Moves a node to the next frequency bucket after it is accessed.
        """
        frequency = node.freq

        frequency_list = self.frequency_lists[frequency]
        frequency_list.remove(node)

        if (
            frequency == self.minimum_frequency
            and frequency_list.size == 0
        ):
            self.minimum_frequency += 1

        node.freq += 1

        new_frequency = node.freq

        if new_frequency not in self.frequency_lists:
            self.frequency_lists[new_frequency] = DoublyLinkedList()

        self.frequency_lists[new_frequency].append(node)

    def get(self, key):
        """
        Returns the cached value for the given key, or -1 if it does not exist.

        Accessing an entry increments its frequency.
        """
        if key not in self.cache:
            return -1

        node = self.cache[key]

        self._update_frequency(node)

        return node.value

    def put(self, key, value):
        """
        Inserts or updates a cache entry, evicting the least frequently used
        entry if the cache is at capacity.
        """
        if self.capacity == 0:
            return

        if key in self.cache:
            node = self.cache[key]
            node.value = value

            self._update_frequency(node)
            return

        if len(self.cache) >= self.capacity:
            eviction_list = self.frequency_lists[self.minimum_frequency]

            victim = eviction_list.pop_left()

            del self.cache[victim.key]

        node = Node(key, value)

        self.cache[key] = node

        self.minimum_frequency = 1

        if 1 not in self.frequency_lists:
            self.frequency_lists[1] = DoublyLinkedList()

        self.frequency_lists[1].append(node)

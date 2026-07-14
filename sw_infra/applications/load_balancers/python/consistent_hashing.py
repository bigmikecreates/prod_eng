import bisect
import hashlib

class Server:
    def __init__(self, name: str):
        self.name = name

class ConsistentHashLoadBalancer:
    def __init__(self, servers: list[Server]):
        self.ring = {}
        self.sorted_keys = []

        for server in servers:
            key = self._hash(server.name)
            self.ring[key] = server
            self.sorted_keys.append(key)
        
        self.sorted_keys.sort()

    def _hash(self, value: str) -> int:
        return int(hashlib.md5(value.encode()).hexdigest(), 16)
    
    def route_request(self, client_id: str) -> Server:
        key = self._hash(client_id)

        index = bisect.bisect(self.sorted_keys, key)

        if index == len(self.sorted_keys):
            index = 0

        server_key = self.sorted_keys[index]

        return self.ring[server_key]
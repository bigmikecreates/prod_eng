import random

class WeightedRandomLoadBalancer:
    def __init__(self, servers):
        """
        servers = [
            ("server-a", 5),
            ("server-b", 2),
            ("server-c", 1),
        ]
        """
        self.servers = servers

    def select_server(self):
        names = [server for server, weight in self.servers]
        weights = [weight for server, weight in self.servers]

        return random.choices(
            names,
            weights=weights,
            k=1
        )[0]

lb = WeightedRandomLoadBalancer([
    ("server-a", 5),
    ("server-b", 2),
    ("server-c", 1),
])

for request_id in range(1, 21):
    selected = lb.select_server()
    print(f"Request {request_id} -> {selected}")
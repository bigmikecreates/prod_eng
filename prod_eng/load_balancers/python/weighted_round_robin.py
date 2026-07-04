class WeightedRoundRobinBalancer:
    def __init__(self, servers):
        """
        servers = [
            ("A",5),
            ("B",1),
            ("C",1),
        ]
        """

        self.expanded_servers = []

        for server, weight in servers:
            self.expanded_servers.extend([server] * weight)

        self.index = 0

    def select_server(self):
        server = self.expanded_servers[self.index]
        self.index = (self.index + 1) % len(self.expanded_servers)
        return server

lb = WeightedRoundRobinBalancer([

    ("A", 5),
    ("B", 1),
    ("C", 1),
])

for i in range(14):
    print(f"Request {i+1} -> Server {lb.select_server()}")

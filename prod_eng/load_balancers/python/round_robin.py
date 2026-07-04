class RoundRobinBalancer:
    def __init__(self, servers):
        self.servers = servers
        self.index=0

    def select_server(self):
        server=self.servers[self.index]
        self.index=(self.index+1) % len(self.servers)
        return server

lb = RoundRobinBalancer(["A", "B", "C"])

for i in range(10):
    print(f"Request {i+1} -> Server {lb.select_server()}")

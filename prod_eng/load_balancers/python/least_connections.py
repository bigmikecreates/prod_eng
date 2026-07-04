from dataclasses import dataclass

@dataclass
class Server:
    name: str
    active_connections: int = 0

    def handle_request(self):
        self.active_connections += 1
        print(f"{self.name} handling request. Active: {self.active_connections}")

    def finish_request(self):
        if self.active_connections > 0:
            self.active_connections -= 1

class LeastConnectionsLoadBalancer:
    def __init__(self, servers: list[Server]):
        self.servers = servers

    def route_request(self) -> Server:
        server = min(self.servers, key = lambda s: s.active_connections)
        server.handle_request()
        return server
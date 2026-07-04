from dataclasses import dataclass
from server import Server as BaseServer

@dataclass
class Server(BaseServer):
    weight: int
    active_connections: int = 0

    def load(self) -> float:
        return self.active_connections/self.weight
    
    def handle_request(self):
        self.active_connections += 1
        super().handle_request()
        print(
            f"(connections={self.active_connections})"
            f"weight={self.weight}"
        )

    def finish_request(self):
        if self.active_connections > 0:
            self.active_connections -= 1

class WeightedLeastConnectionsLoadBalancer:
    def __init__(self, servers: list[Server]):
        self.servers = servers

    def route_request(self) -> Server:
        server = min(self.servers, key=lambda s: s.load())#
        server.handle_request()
        return server
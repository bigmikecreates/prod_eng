import hashlib
from prod_eng.applications.load_balancers.python.server import Server

class IPHashLoadBalancer:
    def __init__(self, servers: list[Server]):
        self.servers = servers

    def route_request(self, client_ip: str) -> Server:
        hash_value = int(
            hashlib.md5(client_ip.encode()).hexdigest(),
            16,
        )

        index = hash_value % len(self.servers)

        server = self.servers[index]
        server.handle_request()

        return server
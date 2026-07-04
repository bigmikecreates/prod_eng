from server import Server

class LeastResponseTimeLoadBalancer:
    def __init__(self, servers: list[Server]):
        self.servers = servers

    def route_request(self) -> Server:
        server = min(self.servers, key = lambda s: s.response_time_ms)
        server.handle_request()
        return server
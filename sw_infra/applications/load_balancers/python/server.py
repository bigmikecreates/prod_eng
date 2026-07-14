from dataclasses import dataclass

@dataclass
class Server:
    name: str
    response_time_ms: float

    def handle_request(self):
        print(f"{self.name} handling request."\
              f"Response time: {self.response_time_ms}ms.")
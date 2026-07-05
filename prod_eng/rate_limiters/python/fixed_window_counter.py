import time
from collections import defaultdict

class FixedWindowCounterRateLimiter:
    def __init__(self, max_requests: int, window_seconds: int):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = defaultdict(list)

    def allow_requests(self, client_id: str) -> bool:
        now = time.time()
        window_start = now - self.window_seconds

        # Remove expired reqeusts
        self.requests[client_id] = [
            timestamp
            for timestamp in self.requests[client_id]
            if timestamp > window_start
        ]

        # Check if client is still within limit
        if len(self.requests[client_id]) < self.max_requests:
            self.requests[client_id].append(now)
            return True
        
        return False
from collections import defaultdict, deque
import time

class SlidingWindowLogRateLimiter:
    def __init__(self, max_requests: int, window_seconds: int):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = defaultdict(deque)

    def allow_requests(self, client_id: str) -> bool:

        now = time.time()
        window_start = now - self.window_seconds
        request_log = self.requests[client_id]

        # Remove expired requests
        while request_log and request_log[0] <= window_start:
            request_log.popleft()

        # Check if request can be accepted
        if len(request_log) < self.max_requests:
            request_log.append(now)
            return True

        return False
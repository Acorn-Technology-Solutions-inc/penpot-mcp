"""
Rate limiting utilities.
"""

import time
from collections import deque
from typing import Deque

from penpot_mcp.exceptions import RateLimitError


class RateLimiter:
    """
    Token bucket rate limiter.

    Tracks requests within a time window and raises an error if limit is exceeded.
    """

    def __init__(self, max_requests: int = 100, window_seconds: int = 60):
        """
        Initialize rate limiter.

        Args:
            max_requests: Maximum number of requests allowed in the time window.
            window_seconds: Time window in seconds.
        """
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests: Deque[float] = deque()

    def _clean_old_requests(self) -> None:
        """Remove requests outside the current time window."""
        now = time.time()
        cutoff = now - self.window_seconds

        while self.requests and self.requests[0] < cutoff:
            self.requests.popleft()

    async def acquire(self) -> None:
        """
        Acquire permission to make a request.

        Raises:
            RateLimitError: If rate limit is exceeded.
        """
        self._clean_old_requests()

        if len(self.requests) >= self.max_requests:
            raise RateLimitError(
                f"Rate limit exceeded: {self.max_requests} requests per {self.window_seconds} seconds"
            )

        self.requests.append(time.time())

    def get_current_usage(self) -> int:
        """
        Get current number of requests in the window.

        Returns:
            Number of requests in the current window.
        """
        self._clean_old_requests()
        return len(self.requests)

    def reset(self) -> None:
        """Reset the rate limiter."""
        self.requests.clear()

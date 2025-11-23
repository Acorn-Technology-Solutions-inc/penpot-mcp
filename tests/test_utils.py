"""
Tests for utility modules.
"""

import pytest

from penpot_mcp.exceptions import RateLimitError
from penpot_mcp.utils.cache import Cache
from penpot_mcp.utils.rate_limit import RateLimiter


class TestRateLimiter:
    """Test rate limiter functionality."""

    @pytest.mark.asyncio
    async def test_rate_limiter_allows_requests(self):
        """Test rate limiter allows requests within limit."""
        limiter = RateLimiter(max_requests=5, window_seconds=60)

        for _ in range(5):
            await limiter.acquire()  # Should not raise

        assert limiter.get_current_usage() == 5

    @pytest.mark.asyncio
    async def test_rate_limiter_blocks_excess(self):
        """Test rate limiter blocks requests exceeding limit."""
        limiter = RateLimiter(max_requests=3, window_seconds=60)

        for _ in range(3):
            await limiter.acquire()

        with pytest.raises(RateLimitError):
            await limiter.acquire()

    def test_rate_limiter_reset(self):
        """Test rate limiter can be reset."""
        limiter = RateLimiter(max_requests=5, window_seconds=60)
        limiter.requests.append(1.0)
        limiter.reset()
        assert len(limiter.requests) == 0


class TestCache:
    """Test cache functionality."""

    def test_cache_set_and_get(self):
        """Test cache can store and retrieve values."""
        cache = Cache()
        cache.set("key1", "value1")
        assert cache.get("key1") == "value1"

    def test_cache_get_missing(self):
        """Test cache returns None for missing keys."""
        cache = Cache()
        assert cache.get("nonexistent") is None

    def test_cache_delete(self):
        """Test cache can delete values."""
        cache = Cache()
        cache.set("key1", "value1")
        cache.delete("key1")
        assert cache.get("key1") is None

    def test_cache_clear(self):
        """Test cache can be cleared."""
        cache = Cache()
        cache.set("key1", "value1")
        cache.set("key2", "value2")
        cache.clear()
        assert cache.get("key1") is None
        assert cache.get("key2") is None

    def test_cache_disabled(self):
        """Test cache respects enabled flag."""
        cache = Cache(enabled=False)
        cache.set("key1", "value1")
        assert cache.get("key1") is None

    def test_cache_invalidate_pattern(self):
        """Test cache pattern invalidation."""
        cache = Cache()
        cache.set("user:1:profile", "data1")
        cache.set("user:1:settings", "data2")
        cache.set("user:2:profile", "data3")

        cache.invalidate_pattern("user:1")

        assert cache.get("user:1:profile") is None
        assert cache.get("user:1:settings") is None
        assert cache.get("user:2:profile") == "data3"

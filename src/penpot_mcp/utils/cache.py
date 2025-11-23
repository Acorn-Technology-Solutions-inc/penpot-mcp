"""
Simple in-memory cache with TTL support.
"""

import time
from typing import Any, Dict, Optional


class CacheEntry:
    """A cache entry with expiration time."""

    def __init__(self, value: Any, ttl: int):
        """
        Initialize cache entry.

        Args:
            value: The cached value.
            ttl: Time-to-live in seconds.
        """
        self.value = value
        self.expires_at = time.time() + ttl

    def is_expired(self) -> bool:
        """Check if entry has expired."""
        return time.time() > self.expires_at


class Cache:
    """
    Simple in-memory cache with TTL support.

    Used for caching API responses to reduce load on Penpot API.
    """

    def __init__(self, default_ttl: int = 300, enabled: bool = True):
        """
        Initialize cache.

        Args:
            default_ttl: Default time-to-live in seconds (5 minutes).
            enabled: Whether caching is enabled.
        """
        self.default_ttl = default_ttl
        self.enabled = enabled
        self._cache: Dict[str, CacheEntry] = {}

    def get(self, key: str) -> Optional[Any]:
        """
        Get value from cache.

        Args:
            key: Cache key.

        Returns:
            Cached value if found and not expired, None otherwise.
        """
        if not self.enabled:
            return None

        entry = self._cache.get(key)
        if entry is None:
            return None

        if entry.is_expired():
            del self._cache[key]
            return None

        return entry.value

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """
        Set value in cache.

        Args:
            key: Cache key.
            value: Value to cache.
            ttl: Optional TTL override. Uses default_ttl if not specified.
        """
        if not self.enabled:
            return

        ttl = ttl if ttl is not None else self.default_ttl
        self._cache[key] = CacheEntry(value, ttl)

    def delete(self, key: str) -> None:
        """
        Delete value from cache.

        Args:
            key: Cache key to delete.
        """
        if key in self._cache:
            del self._cache[key]

    def clear(self) -> None:
        """Clear all cached values."""
        self._cache.clear()

    def invalidate_pattern(self, pattern: str) -> None:
        """
        Invalidate all keys matching a pattern.

        Args:
            pattern: String pattern to match (simple substring match).
        """
        keys_to_delete = [key for key in self._cache.keys() if pattern in key]
        for key in keys_to_delete:
            del self._cache[key]

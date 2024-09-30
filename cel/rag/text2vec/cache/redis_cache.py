from redis import Redis
from .base_cache import BaseCache

class RedisCache(BaseCache):
    def __init__(self, redis: str | Redis = None):
        self.client = redis if isinstance(redis, Redis) else Redis.from_url(redis or 'redis://localhost:6379/0')

    def memoize(self, typed: bool, tag: str, expire: int = None):
        def decorator(func):
            def wrapper(*args, **kwargs):
                key = f"{tag}:{args}:{kwargs}" if typed else f"{tag}:{args}"
                cached_result = self.client.get(key)
                if cached_result:
                    return eval(cached_result)
                result = func(*args, **kwargs)
                if result is not None and expire:
                    self.client.setex(key, expire, str(result))
                return result
            return wrapper
        return decorator
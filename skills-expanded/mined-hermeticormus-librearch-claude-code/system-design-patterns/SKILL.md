---
name: "system-design-patterns"
description: "Worked system design patterns: back-of-envelope capacity estimation, URL shortener, sliding window rate limiter in Redis, news feed fan-out, and typeahead search, plus the design anti-patterns to avoid. Use when working a system design problem."
---

# System Design Patterns

> Named patterns with code and calculations for URL shortener, rate limiter, consistent hashing, news feed fan-out, and back-of-envelope capacity estimation.

## Patterns

### Pattern: Back-of-Envelope Capacity Estimation

```
Problem: Design a URL shortener for Twitter-scale (300M DAU, 1B URLs shortened/day)

ESTIMATION:

Writes (shortening):
  1B URLs/day ÷ 86,400 s/day = ~11,500 writes/s
  Peak (3x average):          = ~35,000 writes/s

Reads (redirects):
  Read:write ratio = 100:1
  11,500 writes/s × 100     = ~1.15M reads/s
  Peak:                       = ~3.5M reads/s

Storage:
  URL record: 500 bytes (short code + long URL + metadata)
  1B URLs/day × 365 days × 5 years = 1.825T URLs
  1.825T × 500 bytes              = ~912 TB ≈ 1 PB

Bandwidth:
  Write: 35,000 writes/s × 500 bytes = 17.5 MB/s
  Read:  3.5M reads/s × 500 bytes    = 1.75 GB/s (cache most of this)

Cache:
  80/20 rule: 20% of URLs = 80% of traffic
  Daily active URLs: 1B/day × 20% = 200M URLs
  Cache size: 200M × 500 bytes = 100 GB  (fits in Redis on a single large node)
```

### Pattern: URL Shortener Core Design (Python)

```python
import hashlib
import base64

class UrlShortener:
    """
    Base62 encoding of a sequential ID → 7-character short code.
    Sequential IDs avoid collision; no retry logic needed.
    """
    BASE62_CHARS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

    def __init__(self, id_generator, cache, db):
        self.id_gen = id_generator  # Distributed ID generator (Snowflake, DB auto-increment)
        self.cache = cache          # Redis
        self.db = db                # PostgreSQL

    def shorten(self, long_url: str) -> str:
        # Check if URL already shortened (deduplication)
        existing = self.db.find_by_long_url(long_url)
        if existing:
            return existing.short_code

        unique_id = self.id_gen.next_id()
        short_code = self._to_base62(unique_id)

        self.db.save(ShortUrl(short_code=short_code, long_url=long_url))
        return short_code

    def resolve(self, short_code: str) -> str:
        # Cache-aside: check Redis first
        cached = self.cache.get(f"url:{short_code}")
        if cached:
            return cached

        record = self.db.find_by_short_code(short_code)
        if not record:
            raise NotFoundException(short_code)

        # Cache with 24h TTL
        self.cache.setex(f"url:{short_code}", 86400, record.long_url)
        return record.long_url

    def _to_base62(self, num: int) -> str:
        result = []
        while num > 0:
            result.append(self.BASE62_CHARS[num % 62])
            num //= 62
        return ''.join(reversed(result)).zfill(7)
```

### Pattern: Rate Limiter with Sliding Window (Redis Lua)

```lua
-- Sliding window rate limiter (atomic Lua script executed on Redis)
-- Key: rate_limit:{user_id}:{window_start_minute}
-- Allows N requests per minute with sliding precision

local key = KEYS[1]           -- e.g., "rate_limit:user_123"
local limit = tonumber(ARGV[1]) -- e.g., 100 (requests per window)
local window = tonumber(ARGV[2]) -- e.g., 60 (window size in seconds)
local now = tonumber(ARGV[3])   -- Current timestamp (milliseconds)

-- Remove expired entries outside the window
redis.call("ZREMRANGEBYSCORE", key, "-inf", now - (window * 1000))

-- Count current requests in window
local count = redis.call("ZCARD", key)

if count >= limit then
    -- Rate limited — return remaining time until oldest entry expires
    local oldest = redis.call("ZRANGE", key, 0, 0, "WITHSCORES")
    if oldest and #oldest > 0 then
        local reset_at = tonumber(oldest[2]) + (window * 1000)
        return {0, math.ceil((reset_at - now) / 1000)}  -- {allowed=0, retry_after_s}
    end
    return {0, window}
end

-- Allow request — add timestamp to sorted set
redis.call("ZADD", key, now, now)
redis.call("EXPIRE", key, window)
return {1, 0}  -- {allowed=1, retry_after_s=0}
```

### Pattern: News Feed Fan-Out Strategy

```python
# Hybrid fan-out: push for normal users, pull for celebrities (> 1M followers)
CELEBRITY_FOLLOWER_THRESHOLD = 1_000_000

class NewsFeedService:

    def publish_post(self, author_id: str, post: Post) -> None:
        post_id = self.post_repo.save(post)
        follower_count = self.social_graph.get_follower_count(author_id)

        if follower_count < CELEBRITY_FOLLOWER_THRESHOLD:
            # Fan-out on write: push to each follower's feed cache
            # Background job processes up to ~500K fans asynchronously
            self.fanout_queue.enqueue(FanoutTask(post_id, author_id))
        else:
            # Celebrity: do NOT fan-out (would enqueue 100M write tasks)
            # Post is pulled at read time and merged into feed
            pass

    def get_feed(self, user_id: str, limit: int = 20) -> list[Post]:
        # Pull: get posts from user's pre-computed feed cache (fan-out on write users)
        cached_feed = self.feed_cache.get(user_id, limit * 2)

        # Merge: also pull from celebrities the user follows (fan-out on read)
        celebrity_followings = self.social_graph.get_celebrity_followings(user_id)
        celebrity_posts = []
        for celebrity_id in celebrity_followings:
            posts = self.post_repo.get_recent_posts(celebrity_id, limit=5)
            celebrity_posts.extend(posts)

        # Merge and sort by timestamp
        all_posts = cached_feed + celebrity_posts
        all_posts.sort(key=lambda p: p.created_at, reverse=True)
        return all_posts[:limit]
```

### Pattern: Typeahead / Autocomplete (Trie + Redis)

```python
import redis

class AutocompleteService:
    """
    Prefix-based autocomplete using Redis Sorted Sets.
    Score = search frequency (higher = more popular).
    """

    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client

    def index_term(self, term: str, frequency: int) -> None:
        """Index all prefixes of a term with its frequency as score."""
        term = term.lower().strip()
        for i in range(1, len(term) + 1):
            prefix = term[:i]
            # Sorted set key = prefix, member = full term, score = frequency
            self.redis.zadd(f"autocomplete:{prefix}", {term: frequency})

    def suggest(self, prefix: str, limit: int = 10) -> list[str]:
        """Return top-N suggestions for prefix, sorted by frequency."""
        prefix = prefix.lower().strip()
        # ZREVRANGEBYSCORE: highest score first (most popular terms)
        suggestions = self.redis.zrevrange(f"autocomplete:{prefix}", 0, limit - 1)
        return [s.decode() for s in suggestions]

# Usage:
# autocomplete.index_term("apple", 1000000)
# autocomplete.index_term("application", 500000)
# autocomplete.suggest("app") → ["apple", "application"]
```

## Anti-Patterns

### Anti-Pattern: Single Database for Everything at Scale

One PostgreSQL instance for all reads and writes at 1M RPS. The database is the bottleneck. Application pods scale horizontally but all their traffic funnels to one DB.

Fix: add read replicas for read-heavy workloads, Redis caching for hot data (the 20% of data serving 80% of reads), and consider sharding for write scaling beyond a single primary.

### Anti-Pattern: Synchronous Fan-Out in the Request Path

When a user posts a tweet, the request synchronously writes to 50M followers' feed tables before returning. The user waits 10+ seconds for their post to complete.

Fix: return 200 immediately after writing the post. Enqueue a background fan-out task. Followers may see the post with a 1-30 second delay (acceptable eventual consistency).

### Anti-Pattern: Ignoring the Read/Write Ratio

Designing a system optimized for writes when it is 100:1 read-heavy. Using a write-optimized data store (Cassandra append-only) when the access pattern is mostly by secondary indexes (which Cassandra handles poorly).

Always establish the read/write ratio in requirements before choosing a data store.

### Anti-Pattern: Missing Failure Modes in Design

A design that assumes all dependencies are always available. No discussion of: what happens when the database is down? What happens when a cache fails? What is the failover procedure?

Every system design must include: fallback strategy for each critical dependency, data durability guarantees, and recovery time objective (RTO).

## References

- Kleppmann, Martin. _Designing Data-Intensive Applications_. O'Reilly, 2017.
- Xu, Alex. _System Design Interview — An Insider's Guide_, vols 1-2. ByteByteGo, 2020, 2022.
- Dean, Jeff, and Sanjay Ghemawat. "MapReduce." OSDI 2004. (Influential system design example)
- AWS Architecture Center: aws.amazon.com/architecture/reference-architecture-diagrams

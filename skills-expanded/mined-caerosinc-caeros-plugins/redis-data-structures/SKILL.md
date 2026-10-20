---
name: redis-data-structures
description: Choose and use Redis data structures, strings, hashes, lists, sets, sorted sets, streams, plus TTL and keyspace hygiene. Use when the user is storing or modeling data in Redis.
---

# Redis Data Structures

Pick the structure from the access pattern, then name keys with a
`app:entity:id` convention (`shop:user:42`, `shop:cart:42`).

## Strings

```
SET session:abc123 "{...}" EX 3600 NX     # value + TTL + only-if-absent, atomically
GET session:abc123
INCR counter:pageviews                     # atomic, creates at 0
INCRBY api:quota:u42 -1
```

`SET ... NX EX` is the building block for locks and dedupe. `INCR` on a
string is the cheapest counter you can buy.

## Hashes: one object, many fields

```
HSET user:42 name "Aya" plan "pro" logins 7
HGET user:42 plan
HGETALL user:42
HINCRBY user:42 logins 1
HEXPIRE user:42 3600 FIELDS 1 otp          # per-field TTL (Redis 7.4+)
```

Prefer a hash over N separate string keys for one entity: fewer keys, one
TTL, atomic multi-field updates via a single HSET.

## Lists: queues and recent-N

```
LPUSH queue:emails "job1"
BRPOP queue:emails 5                       # blocking pop, 5s timeout: worker loop
LPUSH feed:u42 item ; LTRIM feed:u42 0 99  # capped recent-100 feed
```

Lists are fine for simple queues, but they have no acknowledgment: a worker
that crashes after BRPOP loses the job. Use streams when that matters.

## Sets and sorted sets

```
SADD tags:post:7 "redis" "cache"
SINTER online:now friends:u42              # set algebra: online friends
SISMEMBER seen:u42 item9

ZADD leaderboard 1520 "u42"
ZINCRBY leaderboard 10 "u42"
ZREVRANGE leaderboard 0 9 WITHSCORES       # top 10
ZRANGEBYSCORE actions:u42 <now-60s> +inf   # sliding-window rate limit: count then ZADD
ZREMRANGEBYSCORE actions:u42 -inf <now-60s>
```

Sorted sets are the workhorse: leaderboards, rate limiters, delayed-job
schedules (score = run-at timestamp, poll with `ZRANGEBYSCORE ... LIMIT 0 1`).

## Streams: durable, consumer-grouped events

```
XADD events:orders '*' type created orderId 7
XGROUP CREATE events:orders workers $ MKSTREAM
XREADGROUP GROUP workers w1 COUNT 10 BLOCK 5000 STREAMS events:orders >
XACK events:orders workers <id>            # ack after processing
XAUTOCLAIM events:orders workers w2 60000 0-0   # steal entries stuck with dead workers
XADD ... MAXLEN ~ 100000 ...               # cap stream length approximately
```

Streams give you at-least-once delivery, replay, and fan-out to multiple
groups. Monitor `XPENDING` for stuck messages.

## TTL patterns

```
EXPIRE key 3600        TTL key        PERSIST key
```

- Set TTLs at write time (`SET ... EX`), not as a second command, to avoid
  immortal keys when the second command fails.
- Add jitter (`3600 + rand(0..300)`) so a cohort of keys does not expire in
  the same second.
- A plain `SET key value` on an existing key CLEARS its TTL (use `KEEPTTL` to
  preserve it). This silently turns caches into permanent data.

## Keyspace hygiene

- Never `KEYS *` in production; iterate with `SCAN 0 MATCH shop:user:* COUNT 500`.
- `TYPE key`, `OBJECT ENCODING key`, `MEMORY USAGE key` when investigating.
- Big collections (a million-member set) block the event loop on deletion:
  use `UNLINK` instead of `DEL`.
- Everything is bytes: pick one serialization (JSON or msgpack) per app and
  stick to it, or use the JSON data type (see `redis-query-search`).

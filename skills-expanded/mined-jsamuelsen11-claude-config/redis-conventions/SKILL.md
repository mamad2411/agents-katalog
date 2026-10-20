---
name: redis-conventions
description:
  This skill should be used when working with Redis, designing key schemas, selecting data
  structures, configuring Redis clients, or managing Redis memory.
version: 0.1.0
---

# Redis Conventions

These are comprehensive conventions for Redis development, covering data structure selection, key
naming rules, TTL strategy, memory management, persistence configuration, and Redis 7+ features.
Following these conventions ensures efficient memory usage, low latency, operational visibility, and
maintainability across Redis 7+ environments.

## Existing Repository Compatibility

When working with existing Redis implementations and projects, always respect established
conventions and patterns before applying these preferences.

- **Audit before changing**: Review existing key patterns, data structures, and TTL policies to
  understand the project's current state and historical decisions.
- **Client library compatibility**: If the project uses a specific Redis client library, understand
  its conventions and defaults before suggesting changes. Different clients have different
  connection pool defaults, serialization formats, and error handling behaviors.
- **Key namespace migration**: If the project uses inconsistent key naming, flag the inconsistency
  but do not rename keys in production without a coordinated migration plan. Key renaming requires
  careful handling of active connections, TTL preservation, and data integrity.
- **Persistence changes**: Changing persistence configuration (RDB to AOF, or vice versa) can impact
  disk usage, write performance, and restart time. Document trade-offs before changing.
- **Backward compatibility**: When suggesting improvements, provide migration paths and rollback
  procedures for production systems. Never change key structures without considering existing
  consumers.

**These conventions apply primarily to new key schemas, new features, and scaffold output. For
existing systems, propose changes through proper change management processes.**

## Data Structure Selection Guide

Choosing the right data structure is the most critical Redis design decision. Each structure has
specific memory characteristics, operation complexity, and use case fit.

### String

The most versatile Redis type. Stores text, integers, floats, or binary data up to 512 MB.

**Best for**: Simple key-value caching, counters, flags, serialized objects, distributed locks.

**Key operations**: GET, SET, MGET, MSET, INCR, DECR, SETNX, SETEX.

**Encoding**: `int` for integers (8 bytes), `embstr` for strings <= 44 bytes, `raw` for larger
strings.

```redis
-- CORRECT: String for simple caching with TTL
SET myapp:cache:product:5001 '{"name":"Widget","price":29.99}' EX 3600

-- CORRECT: String for atomic counter with TTL
INCR myapp:rate:api:192.168.1.1:1706745600
EXPIRE myapp:rate:api:192.168.1.1:1706745600 60

-- CORRECT: String for distributed lock with owner and TTL
SET myapp:lock:order:5001 "owner-uuid-abc123" NX EX 30

-- WRONG: String for structured data needing partial updates
SET myapp:user:1001 '{"name":"Alice","email":"alice@example.com","age":30}'
-- Problem: Must deserialize, modify, re-serialize for any field update
-- Use Hash instead for partial field access
```

### Hash

A map of field-value pairs, ideal for representing objects with named fields.

**Best for**: Object storage with partial field access, user profiles, session data, per-entity
counters.

**Key operations**: HSET, HGET, HMGET, HGETALL, HDEL, HINCRBY, HSCAN.

**Encoding**: `listpack` for small hashes (< hash-max-listpack-entries), otherwise `hashtable`.

```redis
-- CORRECT: Hash for user profile with partial field access
HSET myapp:user:1001 name "Alice" email "alice@example.com" age 30
HGET myapp:user:1001 email
HINCRBY myapp:user:1001 age 1

-- CORRECT: Hash for session storage with sliding expiry
HSET myapp:session:abc123 user_id 1001 role "admin" last_active 1706745600
EXPIRE myapp:session:abc123 1800

-- WRONG: Separate string keys for each field of an object
SET myapp:user:1001:name "Alice"
SET myapp:user:1001:email "alice@example.com"
SET myapp:user:1001:age "30"
-- Problem: Wastes memory (per-key overhead), no atomic multi-field operations
```

### List

An ordered collection of strings, implemented as a quicklist (linked list of listpacks).

**Best for**: Message queues, activity feeds, recent items, bounded collections.

**Key operations**: LPUSH, RPUSH, LPOP, RPOP, LRANGE, LTRIM, BLPOP, BRPOP.

```redis
-- CORRECT: List for bounded recent activity feed
LPUSH myapp:feed:user:1001 '{"action":"login","ts":1706745600}'
LTRIM myapp:feed:user:1001 0 99

-- CORRECT: List for simple job queue with blocking pop
RPUSH myapp:queue:emails '{"to":"alice@example.com","subject":"Welcome"}'
BLPOP myapp:queue:emails 30

-- WRONG: List for random access by value
LPUSH myapp:items "apple" "banana" "cherry"
-- Then searching for "banana" requires O(N) scan
-- Use Set for membership testing
```

### Set

An unordered collection of unique strings.

**Best for**: Tags, unique visitors, membership testing, intersection/union/difference operations.

**Key operations**: SADD, SREM, SISMEMBER, SMEMBERS, SINTER, SUNION, SDIFF, SCARD.

```redis
-- CORRECT: Set for unique tags
SADD myapp:product:5001:tags "electronics" "sale" "featured"
SISMEMBER myapp:product:5001:tags "sale"

-- CORRECT: Set for unique visitors tracking
SADD myapp:visitors:2024-01-31 "user:1001" "user:1002"
SCARD myapp:visitors:2024-01-31

-- CORRECT: Set for finding common interests
SINTER myapp:interests:user:1001 myapp:interests:user:1002

-- WRONG: Set for ordered data
SADD myapp:leaderboard "alice:1500" "bob:1200"
-- Problem: No ordering, cannot range query by score; use Sorted Set
```

### Sorted Set

An ordered collection of unique strings, each with a floating-point score.

**Best for**: Leaderboards, priority queues, time-series indexes, rate limiting windows, ranking.

**Key operations**: ZADD, ZREM, ZSCORE, ZRANK, ZRANGE, ZREVRANGE, ZINCRBY, ZPOPMIN, ZPOPMAX.

```redis
-- CORRECT: Sorted Set for leaderboard
ZADD myapp:leaderboard 1500 "alice" 1200 "bob" 1800 "charlie"
ZREVRANGE myapp:leaderboard 0 9 WITHSCORES
ZINCRBY myapp:leaderboard 100 "alice"

-- CORRECT: Sorted Set for sliding window rate limiting
ZADD myapp:rate:user:1001 1706745600.123 "req-uuid-1"
ZREMRANGEBYSCORE myapp:rate:user:1001 0 1706745540
ZCARD myapp:rate:user:1001

-- WRONG: Sorted Set for simple membership testing
ZADD myapp:tags 0 "electronics" 0 "sale"
-- Problem: Scores unused, wasting memory; use Set instead
```

### Stream

An append-only log data structure with consumer groups for reliable messaging.

**Best for**: Event streaming, reliable message queues, audit logs, inter-service communication.

**Key operations**: XADD, XREAD, XREADGROUP, XACK, XLEN, XRANGE, XTRIM, XPENDING, XAUTOCLAIM.

```redis
-- CORRECT: Stream with consumer groups for reliable processing
XADD myapp:stream:events:orders * action "created" order_id 5001
XGROUP CREATE myapp:stream:events:orders processors 0 MKSTREAM
XREADGROUP GROUP processors worker-1 COUNT 10 BLOCK 5000 STREAMS myapp:stream:events:orders >
XACK myapp:stream:events:orders processors 1706745600123-0

-- CORRECT: Bounded stream with approximate trimming
XADD myapp:stream:logs MAXLEN ~ 100000 * level "info" message "Request processed"

-- WRONG: Stream without consumer groups for multi-consumer scenarios
XREAD COUNT 10 STREAMS myapp:stream:events:orders 0
-- Problem: No delivery guarantees, no acknowledgment, replays all messages
```

### HyperLogLog

A probabilistic data structure for cardinality estimation with 0.81% standard error.

**Best for**: Counting unique visitors, unique events, unique IPs where ~1% error is acceptable and
memory must be constant (12 KB max per key).

```redis
-- CORRECT: HyperLogLog for unique visitor counting
PFADD myapp:visitors:2024-01-31 "user:1001" "user:1002" "user:1003"
PFCOUNT myapp:visitors:2024-01-31
PFMERGE myapp:visitors:2024-w05 myapp:visitors:2024-01-29 myapp:visitors:2024-01-30

-- WRONG: Set for counting millions of unique items
SADD myapp:all_visitors "user:1" ... "user:10000000"
-- Problem: 10M members use 400MB+; HyperLogLog uses 12KB regardless of cardinality
```

## Key Naming Rules

Consistent key naming is critical for operational visibility, debugging, and preventing key
collisions in shared Redis instances.

### Rule 1: Colon Separator

Use colons (`:`) as the standard hierarchy separator. This is the universally accepted Redis
convention and enables tools like RedisInsight to display key hierarchies.

```redis
-- CORRECT: Colon-separated hierarchical keys
SET myapp:user:1001:profile '...'
SET myapp:cache:api:v2:products:list '...'

-- WRONG: Dot separator
SET myapp.user.1001.profile '...'

-- WRONG: Slash separator
SET myapp/user/1001/profile '...'

-- WRONG: Underscore separator (confuses hierarchy with word separation)
SET myapp_user_1001_profile '...'
```

### Rule 2: Lowercase Only

All key components must be lowercase. This prevents case-sensitivity bugs and ensures consistency.

```redis
-- CORRECT: All lowercase
SET myapp:user:1001:last_login "2024-01-31T12:00:00Z"

-- WRONG: Mixed case
SET myapp:User:1001:LastLogin "2024-01-31T12:00:00Z"

-- WRONG: SCREAMING_CASE
SET MYAPP:USER:1001:LAST_LOGIN "2024-01-31T12:00:00Z"
```

### Rule 3: Hierarchical Structure

Keys follow a logical hierarchy from general to specific: namespace, entity type, identifier,
attribute.

```text
Pattern: {namespace}:{entity}:{id}:{attribute}

Examples:
  myapp:user:1001:profile
  myapp:order:5001:status
  myapp:cache:api:products:page:1
  myapp:rate:api:192.168.1.1
  myapp:lock:order:5001
  myapp:queue:emails
  myapp:stream:events:orders
```

### Rule 4: Namespace Prefix

All keys must begin with a namespace prefix identifying the application or service.

```redis
-- CORRECT: Consistent namespace prefix
SET myapp:user:1001:profile '...'
SET myapp:session:abc123 '...'
SET myapp:cache:product:5001 '...'

-- WRONG: No namespace prefix
SET user:1001:profile '...'
-- Problem: Collides with other services sharing the same Redis instance

-- WRONG: Inconsistent namespace prefixes
SET myapp:user:1001:profile '...'
SET webapp:session:abc123 '...'
-- Problem: Two different prefixes for the same application
```

### Rule 5: No Single-Character Keys

Application keys must be descriptive and self-documenting.

```redis
-- CORRECT: Descriptive key name
SET myapp:user:1001:profile '...'

-- WRONG: Single-character key in application code
SET a '...'
-- Problem: Impossible to debug, no operational visibility
-- Exception: Single-char keys in Lua script local variables are acceptable
```

## TTL Strategy

### Mandatory TTL for Cache Keys

Every cache key must have a TTL. Keys without TTL that are not intentional persistent data will
accumulate and eventually cause out-of-memory conditions.

```redis
-- CORRECT: Cache with explicit TTL
SET myapp:cache:product:5001 '{"name":"Widget","price":29.99}' EX 3600

-- CORRECT: Session with TTL and sliding expiry
HSET myapp:session:abc123 user_id 1001 role "admin"
EXPIRE myapp:session:abc123 1800

-- WRONG: Cache without TTL
SET myapp:cache:product:5001 '{"name":"Widget","price":29.99}'
-- Problem: Key lives forever, stale data accumulates, memory grows unbounded
```

### Tiered TTL

Use different TTL values based on data volatility and cost of regeneration.

```text
Tier 1 - Hot cache (1-5 minutes):     API responses, rate counters, feature flags
Tier 2 - Warm cache (5-60 minutes):   Product details, user preferences, search results
Tier 3 - Cold cache (1-24 hours):     Report data, aggregated statistics, external API data
Tier 4 - Session/state (30m-24h):     User sessions, shopping carts, form state
Tier 5 - Persistent (no TTL):         Leaderboards, configuration (must be documented)
```

### TTL Renewal Rules

```redis
-- CORRECT: Sliding expiry for sessions (renew on activity)
HSET myapp:session:abc123 last_active 1706745600
EXPIRE myapp:session:abc123 1800

-- CORRECT: Fixed expiry for cache (do NOT renew on read)
SET myapp:cache:product:5001 '...' EX 3600
-- On read: GET myapp:cache:product:5001 (no EXPIRE renewal)

-- WRONG: Renewing cache TTL on every read
GET myapp:cache:product:5001
EXPIRE myapp:cache:product:5001 3600
-- Problem: Stale data lives forever if frequently accessed
```

## Memory Management

### Key Metrics to Monitor

```redis
-- Overall memory usage
INFO memory
-- Key: used_memory, used_memory_rss, mem_fragmentation_ratio

-- Per-key memory analysis
MEMORY USAGE myapp:cache:product:5001

-- Key encoding (verify efficient encoding)
OBJECT ENCODING myapp:user:1001
```

### UNLINK Over DEL

Always prefer UNLINK over DEL. UNLINK is non-blocking and reclaims memory in a background thread.

```redis
-- CORRECT: Non-blocking deletion
UNLINK myapp:cache:large_dataset

-- WRONG: Blocking deletion of large keys
DEL myapp:cache:large_dataset
-- Problem: DEL blocks the main thread; large keys cause latency spikes
```

### Encoding Optimization

Redis uses memory-efficient encodings for small data structures. Keep data within encoding
thresholds for optimal memory usage.

```text
Data Structure | Efficient Encoding | Threshold (Redis 7 defaults)
---------------|--------------------|-------------------------------------
Hash           | listpack           | < 128 entries, each < 64 bytes
List           | listpack/quicklist | Automatic quicklist of listpacks
Set            | listpack           | < 128 entries, each < 64 bytes
Sorted Set     | listpack           | < 128 entries, each < 64 bytes
String         | int                | Integer values
String         | embstr             | Strings <= 44 bytes
```

### Eviction Policy Selection

```text
Workload          | Recommended Policy  | Reason
------------------|---------------------|---------------------------------------
Pure cache        | allkeys-lfu         | Evict least frequently used, best hit rate
Mixed cache+data  | volatile-lru        | Only evict keys with TTL
Persistent store  | noeviction          | Never lose data, fail on OOM instead
TTL-based cache   | volatile-ttl        | Evict keys closest to expiry
```

## Persistence Rules

### Cache-Only Workload

Disable persistence entirely for pure cache instances where all data can be regenerated.

```text
# redis.conf for cache-only
save ""
appendonly no
```

### Data Store Workload

Use hybrid persistence (RDB + AOF) for data that cannot be regenerated.

```text
# redis.conf for data store
save 3600 1
save 300 100
save 60 10000
appendonly yes
appendfsync everysec
aof-use-rdb-preamble yes
```

### Hybrid Workload

For mixed cache and persistent data, use AOF with RDB preamble for fast recovery.

```text
# redis.conf for hybrid workload
save 3600 1
save 300 100
appendonly yes
appendfsync everysec
aof-use-rdb-preamble yes
```

## Redis 7 Functions Over Lua Scripts

Redis 7 introduced server-side functions as the replacement for standalone Lua scripts. Functions
are organized in libraries, stored on the server, and replicate correctly.

```lua
-- CORRECT: Redis 7 function library
#!lua name=myapp

local function rate_limit(keys, args)
    local key = keys[1]
    local limit = tonumber(args[1])
    local window = tonumber(args[2])
    local current = redis.call('INCR', key)
    if current == 1 then
        redis.call('EXPIRE', key, window)
    end
    if current > limit then
        return 0
    end
    return 1
end

redis.register_function('rate_limit', rate_limit)
```

```redis
-- Load and call function
FUNCTION LOAD "#!lua name=myapp\n..."
FCALL rate_limit 1 myapp:rate:api:192.168.1.1 100 60
```

```redis
-- WRONG: Raw EVAL for repeated operations
EVAL "local c = redis.call('INCR', KEYS[1]) ..." 1 key 100 60
-- Problem: Script text sent every call, no library organization
```

### Lua Script Rules (When Necessary)

```lua
-- CORRECT: Use KEYS and ARGV arrays (cluster compatible)
local val = redis.call('GET', KEYS[1])
if val == ARGV[1] then
    return redis.call('DEL', KEYS[1])
end

-- WRONG: Hardcoded key names (breaks cluster mode)
local val = redis.call('GET', 'myapp:user:1001')

-- WRONG: Long-running scripts
for i = 1, 1000000 do
    redis.call('SET', KEYS[i], ARGV[i])
end
-- Problem: Blocks entire server for script duration
```

## Command Safety Rules

### Dangerous Commands

```text
NEVER execute without explicit user confirmation:
  FLUSHALL / FLUSHDB   - Destroys all data
  DEBUG *              - Can crash the server
  CONFIG SET           - Changes runtime configuration
  CLUSTER RESET        - Destroys cluster state
  SHUTDOWN             - Stops the server

ALWAYS prefer:
  UNLINK over DEL      - Non-blocking deletion
  SCAN over KEYS       - Non-blocking iteration
```

### SCAN Over KEYS

```redis
-- CORRECT: SCAN with cursor-based iteration
SCAN 0 MATCH myapp:cache:* COUNT 100

-- WRONG: KEYS with glob pattern in application code
KEYS myapp:cache:*
-- Problem: O(N) scan blocks server for entire keyspace
```

### Blocking Commands Must Have Timeout

```redis
-- CORRECT: Blocking pop with timeout
BLPOP myapp:queue:jobs 30

-- WRONG: Blocking pop with infinite timeout
BLPOP myapp:queue:jobs 0
-- Problem: Connection blocked forever, prevents graceful shutdown
```

### No SELECT for Database Switching

```redis
-- WRONG: Using SELECT to switch databases
SELECT 1
SET user:1001:session '...'

-- CORRECT: Use key namespaces instead
SET myapp:session:user:1001 '...'
-- Key namespaces work in cluster mode, are visible in monitoring, and
-- do not depend on connection state
```

## Anti-Pattern Reference

```text
Anti-Pattern                    | Fix
--------------------------------|-----------------------------------------------
KEYS * in app code              | Use SCAN with cursor and COUNT
SET cache without TTL           | Always use SET ... EX or follow with EXPIRE
DEL on large keys               | Use UNLINK (non-blocking)
LPUSH without LTRIM             | Pair with LTRIM or use Stream MAXLEN
Values > 1MB                    | Compress or chunk into smaller keys
Hot key (global counter)        | Shard: counter:{shard_N}, sum for total
FLUSHALL/FLUSHDB in prod        | SCAN + UNLINK for targeted cleanup
Blocking cmd without timeout    | Always set timeout (e.g., BLPOP key 30)
SELECT for db switching         | Use key namespaces instead
Lock without TTL                | Always use SET NX EX
Lock release without owner check| Lua: compare owner then DEL
String for partial-update object| Use Hash for field-level access
Set for ordered data            | Use Sorted Set with scores
Pub/Sub for reliable delivery   | Use Streams with consumer groups
```

## Bitmap Conventions

Bitmaps are strings treated as bit arrays. Use for space-efficient boolean state tracking.

```redis
-- CORRECT: Bitmap for daily active users
SETBIT myapp:dau:2024-01-31 1001 1
SETBIT myapp:dau:2024-01-31 1002 1
BITCOUNT myapp:dau:2024-01-31

-- CORRECT: Bitmap for feature flags per user
SETBIT myapp:features:dark_mode 1001 1
GETBIT myapp:features:dark_mode 1001

-- CORRECT: Bitmap intersection for multi-day analysis
BITOP AND myapp:active_both myapp:dau:2024-01-30 myapp:dau:2024-01-31
BITCOUNT myapp:active_both

-- WRONG: Bitmap with sparse, high-value offsets
SETBIT myapp:logins 999999999 1
-- Problem: Allocates ~125MB for a single bit at offset ~1 billion
-- Use Set or HyperLogLog for sparse ID spaces
```

## Geospatial Conventions

Geospatial data is stored in Sorted Sets with geohash encoding.

```redis
-- CORRECT: Geospatial for store locator
GEOADD myapp:stores:coffee -73.985428 40.748817 "store:nyc-midtown"
GEOADD myapp:stores:coffee -73.968285 40.785091 "store:nyc-upperwest"
GEOSEARCH myapp:stores:coffee FROMLONLAT -73.980000 40.750000 BYRADIUS 5 km ASC COUNT 10
GEODIST myapp:stores:coffee "store:nyc-midtown" "store:nyc-upperwest" km

-- WRONG: Storing coordinates in separate string keys
SET myapp:store:nyc-midtown:lat "40.748817"
SET myapp:store:nyc-midtown:lon "-73.985428"
-- Problem: Cannot do radius queries, requires application-level distance calculation
```

## Cluster Mode Conventions

### Hash Tags for Multi-Key Operations

In Redis Cluster, multi-key operations require all keys to be on the same node. Use hash tags to
ensure related keys share the same hash slot.

```redis
-- CORRECT: Hash tags for related keys
SET myapp:{user:1001}:profile '...'
SET myapp:{user:1001}:settings '...'
-- Both keys hash to the same slot via {user:1001}

-- CORRECT: Transaction on same-slot keys
MULTI
HSET myapp:{order:5001}:data status "paid"
LPUSH myapp:{order:5001}:history "status_changed:paid"
EXEC

-- WRONG: Multi-key operation across different slots
MGET myapp:user:1001:profile myapp:user:1002:profile
-- Problem: Keys may be on different nodes, CROSSSLOT error

-- WRONG: Hash tag that groups too many keys on one node
SET myapp:{global}:counter1 0
SET myapp:{global}:counter2 0
-- Problem: All keys on same node, creates hot spot
```

### Cluster-Safe Key Design

```text
Rules for cluster-compatible key design:
1. Never hardcode key names in Lua scripts (pass through KEYS array)
2. Use hash tags only when multi-key atomicity is required
3. Distribute hash tags across many values to avoid hot nodes
4. Avoid MGET/MSET across different hash tags (use pipeline instead)
5. Test key distribution: CLUSTER KEYSLOT <key> to verify slot assignments
```

## Security Conventions

### ACL Configuration

```text
# Least-privilege ACL rules
user appuser on >password ~myapp:* &myapp:* +@all -@admin -@dangerous
user monitor on >monpass ~myapp:* +@read +info +ping
user cacheuser on >cachepass ~myapp:cache:* +get +set +del +unlink +expire +ttl
user default off
```

### Connection Security

```text
Production requirements:
1. AUTH/ACL: Always require authentication
2. TLS: Enable for non-local connections
3. bind: Bind to specific interfaces only
4. protected-mode: Enable (rejects unauthenticated external connections)
5. Disable default user in production
6. Never store credentials in code or configuration files
7. Use environment variables or secret management for passwords
```

## Pub/Sub vs Streams Decision Guide

```text
Feature              | Pub/Sub                    | Streams
---------------------|----------------------------|-----------------------------
Delivery guarantee   | At-most-once (fire-forget) | At-least-once (with ACK)
Message persistence  | No                         | Yes (append-only log)
Consumer groups      | No                         | Yes
Message replay       | No                         | Yes (from any ID)
Backpressure         | No (slow consumers drop)   | Yes (pending entries list)
Fan-out              | Yes (all subscribers)       | Yes (multiple groups)
Pattern matching     | Yes (PSUBSCRIBE)           | No (per-stream)

Use Pub/Sub for:     Cache invalidation, real-time notifications, config updates
Use Streams for:     Event sourcing, job queues, reliable messaging, audit logs
```

## Pipeline and Transaction Conventions

### Pipeline Sizing

```text
Recommended batch sizes: 100-1000 commands per pipeline
- Too small (< 10): Underutilizes network efficiency
- Too large (> 5000): Delays first response, uses excessive client memory
- Optimal: 100-500 for most workloads
```

### Transaction Rules

```redis
-- CORRECT: MULTI/EXEC for atomic multi-key operations
MULTI
DECRBY myapp:account:1001:balance 100
INCRBY myapp:account:1002:balance 100
EXEC

-- CORRECT: Optimistic locking with WATCH
WATCH myapp:account:1001:balance
GET myapp:account:1001:balance
MULTI
DECRBY myapp:account:1001:balance 100
EXEC

-- WRONG: Non-atomic read-modify-write without WATCH
GET myapp:account:1001:balance
SET myapp:account:1001:balance (old_value - 100)
-- Problem: Race condition between GET and SET
```

## Connection Pool Conventions

```text
Pool sizing guidelines:

Web applications:
  pool_size = max_concurrent_requests / 10
  min_idle = pool_size / 4

Background workers:
  pool_size = number_of_workers + 2
  min_idle = number_of_workers

General rule:
  pool_size = cpu_cores * 2
  min_idle = pool_size / 2

Maximum: 50 connections per application instance

Timeout settings:
  connect_timeout: 5 seconds
  command_timeout: 2 seconds
  retry_count: 3
  retry_delay: 100ms (with exponential backoff)
  max_retry_delay: 2000ms
```

## Monitoring Conventions

### Critical Metrics

```text
Memory:
  used_memory vs maxmemory         (alert at 80%)
  mem_fragmentation_ratio          (alert if > 1.5)
  evicted_keys                     (alert if > 0 for non-cache)

Performance:
  instantaneous_ops_per_sec
  latency percentiles (p50, p99)
  slowlog entries per minute

Connections:
  connected_clients vs maxclients  (alert at 80%)
  rejected_connections             (alert if > 0)

Replication:
  master_link_status               (alert if down)
  master_last_io_seconds_ago       (alert if > 10)

Persistence:
  rdb_last_bgsave_status           (alert if not ok)
  aof_last_bgrewrite_status        (alert if not ok)
```

### Health Check Pattern

```redis
-- Application health check
PING
-- Expected: PONG

-- Detailed health check
INFO server
-- Verify: redis_version, uptime_in_seconds

-- Write/read verification
SET myapp:health:check "ok" EX 10
GET myapp:health:check
```

## Key Documentation Template

All key patterns must be documented in `docs/db/redis-conventions.md`:

```markdown
| Pattern                      | Type       | TTL  | Purpose            |
| ---------------------------- | ---------- | ---- | ------------------ |
| myapp:user:{id}:profile      | Hash       | None | User profile data  |
| myapp:session:{token}        | Hash       | 30m  | Session data       |
| myapp:cache:product:{id}     | String     | 1h   | Product cache      |
| myapp:rate:api:{ip}:{window} | String     | 60s  | Rate limit counter |
| myapp:lock:{resource}:{id}   | String     | 30s  | Distributed lock   |
| myapp:queue:{name}           | List       | None | Job queue          |
| myapp:stream:events:{domain} | Stream     | None | Event stream       |
| myapp:leaderboard:{name}     | Sorted Set | None | Score ranking      |
```

## Sentinel Conventions

Redis Sentinel provides high availability through automatic failover for non-cluster setups.

```text
Sentinel architecture requirements:
- Minimum 3 Sentinel instances for quorum
- Sentinels monitor master and replica health
- Automatic failover when master is down
- Client discovers master via Sentinel

Configuration:
  sentinel monitor mymaster 10.0.0.1 6379 2
  sentinel down-after-milliseconds mymaster 5000
  sentinel failover-timeout mymaster 60000
  sentinel parallel-syncs mymaster 1
```

### Client Connection via Sentinel

```text
Client connection flow:
1. Connect to any Sentinel node
2. Ask for current master: SENTINEL get-master-addr-by-name mymaster
3. Connect to master for read/write operations
4. Subscribe to failover notifications for automatic reconnection
5. Reconnect to new master after failover event
```

## Redis Module Conventions

### RedisJSON

Use for native JSON document storage when partial updates and nested queries are needed.

```redis
-- CORRECT: Store and partially update JSON documents
JSON.SET myapp:user:1001 $ '{"name":"Alice","email":"alice@example.com","orders":[5001]}'
JSON.SET myapp:user:1001 $.email '"newalice@example.com"'
JSON.ARRAPPEND myapp:user:1001 $.orders 5002
JSON.NUMINCRBY myapp:user:1001 $.login_count 1
```

### RediSearch

Use for full-text search and secondary indexing on Hash or JSON data.

```redis
-- CORRECT: Create index and search
FT.CREATE myapp:idx:products ON HASH PREFIX 1 myapp:product:
  SCHEMA name TEXT WEIGHT 5.0 price NUMERIC SORTABLE category TAG

HSET myapp:product:5001 name "Wireless Keyboard" price 79.99 category "electronics"
FT.SEARCH myapp:idx:products "@category:{electronics} @price:[50 100]" SORTBY price ASC
```

### RedisTimeSeries

Use for time-series data with automatic downsampling and aggregation.

```redis
-- CORRECT: Create time series with retention and labels
TS.CREATE myapp:ts:cpu:server1 RETENTION 86400000 LABELS host server1 metric cpu
TS.ADD myapp:ts:cpu:server1 * 72.5
TS.RANGE myapp:ts:cpu:server1 - + AGGREGATION avg 60000
```

## Backup and Recovery Conventions

```text
Backup recommendations:
- RDB: Schedule regular BGSAVE, copy RDB to remote storage
- AOF: Copy during low-traffic windows, verify with redis-check-aof
- Cluster: Backup each node independently, record slot assignments
- Verify: redis-check-rdb dump.rdb (verify RDB integrity)

Retention:
- 7 daily snapshots
- 4 weekly snapshots
- 3 monthly snapshots

Recovery testing:
- Test restore procedure monthly
- Verify data integrity after restore
- Document recovery time and steps
```

## Version-Specific Conventions

```text
Redis 7.0+ features to prefer:
- Functions (FUNCTION LOAD) over EVAL/EVALSHA
- Listpack encoding over ziplist (automatic in 7.0+)
- Multi-part AOF (aof-use-rdb-preamble yes)
- XAUTOCLAIM for stream message recovery
- ACL improvements (selector-based permissions)
- Client-side caching with tracking

Redis 6.x compatibility:
- Use EVAL/EVALSHA instead of FUNCTION
- Use ziplist encoding thresholds
- ACLs available but fewer features than 7.x
- No XAUTOCLAIM (use XCLAIM with manual pending check)
```

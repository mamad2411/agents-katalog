---
name: caching-scan
description: "Find cache defects: entries that never expire, stampedes with no single-flight, keys missing the tenant or user, writes that never invalidate, errors and nulls cached as data, HTTP cache headers, cache writes before commit, the cache as an untimed dependency. Proved by a two-tenant, write-then-read or concurrent-miss test."
kind: skill
pack: performance
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: caching-scan

## Premise

A cache is a second copy of the truth with its own lifetime, its own keyspace and its own failure modes, and most cache defects are correctness defects that only look like performance. A key without the tenant serves one customer's catalog to another. A write path that forgets to invalidate serves yesterday's price until the TTL, or forever if there is none. A hot key that expires sends a hundred concurrent misses to the database at once. A cache on a shared connection that waits forever while the cache is down turns a cache outage into an API outage. Each of these is visible in the code: the key template, the write paths of the cached data, the miss path, the client options. This skill finds them and proves each with a deterministic test. `@caching-architect` (this pack) designs the replacement; this skill is the detector it consumes.

**Every finding cites the cache read or write at `<file:line>` + the key family and what data it holds + the entry point that reaches it + the missing control (TTL, single-flight, identity dimension, invalidation on a named write path, failure handling, `Cache-Control`, commit ordering, timeout) + the proof or the probe that would settle it + the fix in the project's cache library.** A grep hit is never a finding by itself, and "no cache issues" is never printed without the class-coverage block (§ Output).

**Classify every key family first.** Redis and its peers hold two kinds of data. A **cache entry** is derived from a source of truth and is safe to drop. **State** (a lock, lease, cursor, rate-limit window, OTP or single-use token, idempotency record, job status, queue) is the source of truth itself. The classes here apply to cache entries. State keys close as `N/A (state, not a cache)` for §1–§5 and §7 with one read; their correctness belongs to the skill that owns the mechanism (`logic-race-scan` for single-use and locks in the security pack, `@resilience-reviewer` for idempotency in the distributed-systems pack, when installed). §8 applies to both, because a request blocked on the store is blocked whatever the key holds.

## Boundaries

- **The cross-tenant or cross-user read** that a key without its identity dimension causes (§3) is a security finding: it goes to `@tenant-isolation-reviewer` § "Caches" (security pack, when installed) through [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 9, and the two runs dedupe by `<file:line>`. Without the security pack it is verified and reported here, tagged `security-class (owner pack not installed)`.
- **A private response stored by a shared cache or the browser** (`Cache-Control: public` or `s-maxage` on an authenticated route, a missing `no-store`, `cache_page` without `Vary: Cookie`) → `data-exposure-scan` § "9. Private responses cacheable" (security pack, when installed). §6 here owns the performance side: cacheable public responses and static assets sent with no or short caching, and a missing `Vary` that fragments or poisons a shared cache. Without the security pack, §6 reports the private leg too, tagged `security-class (owner pack not installed)`.
- **An in-process cache with no size bound** → `memory-growth-scan` § 1 (this pack). It is reported once, there; §1 here owns entries that never **expire** and remote stores with no memory policy.
- **Cache design** (which layer, which keys, which invalidation strategy for a new cache) → `@caching-architect` (this pack). The backend pack's `caching-strategy.md` pattern is the method when the backend pack is installed.
- **Process-local caches across replicas** (an in-process store such as locmem, `:memory_store`, Caffeine or Nest's default store behind more than one process; an `@CacheEvict` that clears one pod's copy; per-pod cold starts) → `request-path-scan` §17 (this pack), and sessions, limiters, dedupe sets, locks and once-per-fleet work → its §16, §18 and §20. This skill still judges such a cache's TTL (§1), stampede (§2), keys (§3) and invalidation (§4) within one process.
- **ORM result caches** (MikroORM `cache`, TypeORM `cache`, Hibernate second-level cache) are in scope here. Query shape and N+1 behind a cache are the database pack's (`query-shape-scan`, `n-plus-one-scan`, when installed): caching a per-row query does not fix an N+1, and that skill reports it.
- **Outbound timeouts in general** → `request-path-scan` §12 (this pack); retry and breaker policy → `@resilience-reviewer` § "2. Retries" and § "3. Circuit breaker" (distributed-systems pack, when installed). Synchronised load in general (cron at `:00`, reconnect storms) → `request-path-scan` §14. §8 here owns only the cache client and the request path's behaviour while the cache is slow or down; §2 owns synchronised expiry of cache keys.

## Adapt to the codebase

Read the cache libraries, their versions and the store's configuration (grep 0, the lockfile, `redis.conf` or the managed-cache parameter group) before judging a row, and print the lanes you ran. Defaults differ by library and are the usual source of a defect:

| Lane | Write / expiry spelling | Single-flight or early refresh | Invalidation primitive | The trap |
|---|---|---|---|---|
| **NestJS** (`@nestjs/cache-manager` on Keyv; Express or Fastify adapter) | `cache.set(k, v, ttl)`, TTL in **milliseconds** (NestJS docs, *Caching*); `CacheModule.register({ ttl, stores })` | none built in: an in-flight `Map<key, Promise>` deleted on settle, or `lru-cache` `fetch()` | `cache.del(k)` | `CacheInterceptor` caches `GET` responses keyed by "the request URL (in HTTP apps) or the cache key set through the `@CacheKey()` decorator" (NestJS docs): on an authenticated route every user shares an entry unless `trackBy` adds the principal. The default store is in-process |
| **Node** (ioredis, node-redis, `lru-cache`; Express, Fastify) | ioredis `set(k, v, 'EX', s)`; node-redis `set(k, v, { EX: s })`; a two-argument `set` never expires | `lru-cache` `fetch()` with `fetchMethod`: "multiple fetches for the same key … coalesced into a single call to fetchMethod" (lru-cache 11 source); `SET k v NX PX` as a cross-process lock | `del` / `unlink` | ioredis queues commands while disconnected (`enableOfflineQueue` default `true`), and `maxRetriesPerRequest: null`, which BullMQ requires for its worker connections, makes them "wait forever until the connection is alive again" (ioredis 6 `RedisOptions`). A request-path `get` on that connection hangs through a cache outage (§8) |
| **MikroORM** result cache | `em.find(E, where, { cache: true \| ms \| [key, ms] })`; default expiration 1 s; the default adapter is in memory, "shared for the whole `MikroORM` instance" (MikroORM 7.2 docs, *Result cache*) | none | `em.clearCache(key)` | with `[key, ms]` the key you pass is the entry's identity: two calls with different filters and one key share an entry. Writes do not clear it |
| **TypeORM** query cache | `cache: true` (1,000 ms), `cache: ms`, `cache: { id, milliseconds }`, QueryBuilder `.cache(id, ms)` (TypeORM docs, *Caching queries*) | none | invalidate by cache id | an explicit `id` ignores the parameters, as above; "users inserted during the … cache window won't be returned" by design |
| **Prisma · Drizzle · Sequelize · Knex** | no ORM-level result cache to configure: the application's own cache lane applies (Prisma Accelerate's `cacheStrategy`, where used, is a managed cache with its own `ttl`) | — | — | a cache wrapped around an ORM call inherits every row of this table |
| **Django / DRF** | `cache.set(k, v, timeout)`, default `TIMEOUT` 300 s, `None` = never expire; `cache_page`; locmem "is the default cache if another is not specified", and "each process will have its own private cache instance" (Django 5.2 docs, *Cache framework*) | `cache.get_or_set` takes no lock; `dogpile.cache` regions for one regeneration at a time | `cache.delete`, `transaction.on_commit(lambda: cache.delete(k))` | `cache_page` keys by URL and the `Vary` headers; with token auth, DRF's own examples add `vary_on_headers("Authorization")` per user (DRF docs, *Caching*) |
| **SQLAlchemy** (dogpile.cache) | region `expiration_time` | `region.get_or_create` regenerates under a lock | `region.delete(k)` / `invalidate()` | a region decorated on a function whose result depends on the current user but not its arguments |
| **Spring** (Spring Cache, Caffeine, Spring Data Redis) | Caffeine `expireAfterWrite`; Redis `RedisCacheConfiguration.entryTtl(…)` | `@Cacheable(sync = true)`: "only one thread is busy computing the value"; optional per provider, supported by every core `CacheManager` (Spring Framework docs, *Cache annotations*); Caffeine `refreshAfterWrite` | `@CacheEvict`, `@CachePut` | the default key is the method's parameters (`SimpleKeyGenerator`): a method that reads the user from `SecurityContextHolder` caches one answer for all users. Hibernate's second-level cache never sees writes made outside Hibernate |
| **Rails** | `Rails.cache.fetch(k, expires_in:)`, `write`; a `fetch` with no `expires_in` and no store default never expires | `race_condition_ttl`: other processes keep the expired value while one regenerates, "also known as the dog pile effect" (ActiveSupport 8.0 `cache.rb`) | versioned keys (`cache_key_with_version`), `Rails.cache.delete` | `:memory_store` per process: "process instances won't be able to share cache data" (Rails guide, *Caching with Rails*) |
| **Laravel** | `Cache::put($k, $v, $ttl)`, `Cache::remember($k, $ttl, fn)`; `forever` / `rememberForever` never expire | `Cache::flexible($k, [fresh, stale], fn)` (stale-while-revalidate), `Cache::lock($k, $s)` atomic locks (Laravel 12 docs, *Cache*) | `Cache::forget`, tags | `CACHE_STORE=array` or `file` on several hosts |
| **Go** (go-redis, ristretto, go-cache) | go-redis `Set(ctx, k, v, ttl)`, `0` = no expiration; go-cache `cache.NoExpiration` | `golang.org/x/sync/singleflight` | `Del` | a `singleflight` key that omits the tenant coalesces two tenants into one answer |
| **.NET** | `DistributedCacheEntryOptions`, `MemoryCacheEntryOptions` | `IMemoryCache.GetOrCreateAsync` does not coalesce; `HybridCache` coalesces per instance (performance research catalog, 2026-10-02) | `Remove`, `HybridCache` tags | `AddMemoryCache` on several instances |

The per-process stores in the trap column (locmem, `:memory_store`, `AddMemoryCache`, `CACHE_STORE=array` / `file`, Nest's default store) are judged here for TTL, keys, stampede and invalidation; their coherence across replicas is `request-path-scan` §17's.

## Context before hunting

On a whole-repo run, build one map first:

1. **Key families** (grep 0, 3a, 4a): the prefix, what each holds, whether it is a **cache entry** or **state** (§ Premise), the source of truth behind each cache entry, and the identity the data is scoped by (global, tenant, user, role, locale, currency).
2. **Write paths of every cached source of truth.** For each cache family, list every code path that changes the underlying data: the API's commands, admin screens, imports and bulk updates, jobs and consumers, migrations and backfills, raw SQL, other services that share the database. §4 is judged against this list.
3. **The store's own configuration**: `maxmemory` (0 means no limit on 64-bit Redis) and `maxmemory-policy` (`CONFIG GET maxmemory-policy`; the `volatile-*` policies "behave like `noeviction` if no keys have an associated expiration", Redis docs, *Key eviction*), the client options (timeouts, offline queue), and whether the cache store is shared with queues and locks.
4. **Deployment shape** (grep 0b): replicas and processes per replica, which multiply a stampede's origin load (§2) and decide whether a process-local cache is `request-path-scan` §17's concern.
5. **Hit and miss evidence**, where it exists: `keyspace_hits` / `keyspace_misses` from Redis `INFO stats`, the library's hit metrics, the origin's call rate. A cache with no measured hit ratio is a candidate cost, not a proven benefit.

## Pre-flight greps

Run as **one** script from the repo root (shell state does not survive between tool calls). Grep **N** feeds detector **§N**; grep 0 is context. Set `ROOTS` to the server code roots; greps 0b and 6c read deploy and proxy config from `.` on purpose. Every `rg` names its path: `rg` given no path reads stdin whenever stdin is a pipe, which under an agent's shell is a silent zero-hit run. A lane count of 0 is an `N/A` reason; any `rg` error on stderr (exit 2) is a failed grep, never zero hits. Multi-line greps print one line per match (`-o -r`) at the line where the match starts.

```bash
ROOTS=(.)        # the SERVER code roots; the browser app's HTTP cache belongs to the frontend pack
X=(-g '!**/node_modules/**' -g '!**/vendor/**' -g '!**/dist/**' -g '!**/build/**' -g '!**/.next/**' -g '!**/target/**' -g '!**/.venv/**'
   -g '!**/*.min.*' -g '!**/*.{md,mdx,lock,map,svg,json,snap,sql}' -g '!ai/**' -g '!docs/**' -g '!.claude/**'
   -g '!**/{test,tests,__tests__,spec,e2e,__mocks__,mocks,fixtures,__fixtures__,testdata,seeds,seeders,migrations,migrate,locales,i18n,generated,__generated__,.prisma,temp}/**'
   -g '!**/*.{spec,test,e2e-spec,mock,stories}.*' -g '!**/{*_test,*_spec,test_*,conftest}.*')
C='^(?![ \t]*+(?://|/?\*|#(?!\{)|--))[^\n]*?'     # skip comment-only lines
K='\b(?:cache|caches|cacheManager|cacheService|redis|redisClient|client|store|kv|memcached?|mc|this\.\w*(?:[Cc]ache|[Rr]edis|[Ss]tore)\w*|\w*[Cc]ache)\s*\.\s*'
ID='(?i:tenant|org|account|workspace|merchant|seller|shop|store|company|user|owner|member|principal|session|locale|lang|currency|role|scope|perm)'
for t in js ts py go java kotlin ruby php cs; do printf '%-7s %s\n' "$t" "$(rg --files -t "$t" "${X[@]}" "${ROOTS[@]}" | wc -l)"; done   # 0 = lane absent

# 0. Context: 0a the cache stores and libraries in use, with how many files import each.
rg -o --no-filename --pcre2 "$C"'\K(?:(?<=from\s["\x27])|(?<=require\(["\x27]))(?:ioredis|redis|@redis/client|@upstash/redis|@nestjs/cache-manager|cache-manager|keyv|@keyv/\w+|lru-cache|node-cache|memjs|@fastify/caching|apicache)(?=["\x27])|^\s*(?:import|from)\s+\K(?:redis|django_redis|cachetools|aiocache|dogpile|flask_caching|diskcache)\b|github\.com/\K(?:redis/go-redis|go-redis/redis|patrickmn/go-cache|dgraph-io/ristretto|allegro/bigcache|coocood/freecache)|\bimport\s+\K(?:org\.springframework\.cache|com\.github\.benmanes\.caffeine|javax\.cache)|\b(?:IDistributedCache|HybridCache|Rails\.cache|CacheModule\.register\w*|resultCache|django\.core\.cache)\b|\bCache::(?=\w)' "${X[@]}" "${ROOTS[@]}" | sort | uniq -c | sort -rn

# 0b. Deployment shape: replicas, autoscaling and processes per replica (deploy files; confirm the workload that runs the cache).
rg -n --pcre2 '^\s*(?:replicas|minReplicas|maxReplicas)\s*:\s*\d+|\bkind:\s*HorizontalPodAutoscaler\b|\bWEB_CONCURRENCY\b|^\s*workers\s*=\s*\d|\binstances\s*:\s*["\x27]?(?:\d+|max)\b|\bexec_mode\s*:\s*["\x27]?cluster|\bdesiredCount\b|\binstance_count\s*[=:]' -g '*.{yml,yaml,toml,tf,hcl,conf}' -g '{gunicorn,puma}*' -g 'Procfile*' -g '!**/node_modules/**' -g '!**/{test,tests,e2e,fixtures}/**' -g '!ai/**' -g '!docs/**' .

# 1. Entries that never expire: two-argument SETs and expiry-less writes per lane, tagged when the same file sets an
#    expiry somewhere (1a); configuration that turns expiry off (1b).
rg -n --pcre2 "$C$K"'(?:set|setAsync|hset|hmset|sadd|lpush|rpush|zadd)\(\s*[^,()\n]+(?:\([^()\n]*\))?\s*,\s*[^,\n]+\)\s*;?\s*$|'"$C"'\bcache\.set\(\s*[^,\n]+,\s*[^,\n]+,\s*(?:timeout\s*=\s*)?None\b|'"$C"'\bCache::(?:forever|rememberForever)\(|'"$C"'\bCache::put\(\s*[^,\n]+,\s*[^,\n]+\)\s*;|'"$C"'\bRails\.cache\.(?:write|fetch)\((?![^\n]*expires_(?:in|at))|'"$C"'\.Set\(\s*ctx\s*,\s*[^,\n]+,\s*[^,\n]+,\s*0\s*\)|'"$C"'\bcache\.NoExpiration\b|'"$C"'\.SetString(?:Async)?\(\s*[^,\n]+,\s*[^,\n]+\)\s*;' "${X[@]}" "${ROOTS[@]}" |
  while IFS= read -r hit; do rg -q --pcre2 '\b(?:p?expire\w*|setex|SetEx)\(|["\x27](?:EX|PX|EXAT|KEEPTTL)["\x27]|\b(?:ex|px|timeout|ttl|expires_in|EX|PX)\s*[:=]\s*[1-9]' "${hit%%:*}" && echo "$hit  [expiry set elsewhere in the file]" || echo "$hit"; done
rg -n --pcre2 "$C"'(?:\bttl\s*:\s*0\b|["\x27]TIMEOUT["\x27]\s*:\s*None\b|\bdefaultCacheConfig\(\)(?![^;\n]*entryTtl)|\bexpires_in\s*:\s*nil\b)' "${X[@]}" "${ROOTS[@]}"

# 2. Stampede: a read, then a compute, then a write of the same key, tagged by whether the file holds any single-flight,
#    lock or early-refresh primitive (2a); framework helpers that do not coalesce unless asked (2b).
rg -n -U -o --pcre2 "$C$K"'(?:get|getAsync|hget|Get|fetch)\(\s*(\w+)\s*[,)][^\n]*\n(?:[^\n]*\n){0,15}?[^\n]*'"$K"'(?:set|setex|setAsync|hset|Set|put|write)\(\s*\1\b' -r 'get → compute → set of $1' "${X[@]}" "${ROOTS[@]}" |
  while IFS= read -r hit; do rg -q --pcre2 '\bsingleflight\b|\b(?:inflight|inFlight|pending|loading)\w*\.(?:get|set|has)\(|\bcoalesc|\bdedupe|\.lock\(|\bLock\(|\bMutex\b|\bredlock\b|["\x27]NX["\x27]|\bnx\s*[:=]\s*(?:true|True)|race_condition_ttl|\bflexible\(|\bfetchMethod\b|refreshAfterWrite|stale-while-revalidate' "${hit%%:*}" && echo "$hit  [primitive present in file]" || echo "$hit  [no single-flight in file — check its callers: a single-flight factory or in-flight map may front this function]"; done
rg -n --pcre2 "$C"'(?:@Cacheable\((?![^)\n]*\bsync\s*=\s*true)|\bGetOrCreateAsync\(|\bcache\.get_or_set\(|\bCache::remember\(|\bRails\.cache\.fetch\((?![^\n]*race_condition_ttl)|\bcacheManager\.wrap\()' "${X[@]}" "${ROOTS[@]}"

# 3. Keys: 3a key templates (`prefix:${…}`) with no identity dimension, in files that use a cache; 3b response caches
#    keyed by URL or method arguments, and ORM result caches with a fixed id; 3c volatile parts that make every key unique.
rg -l --null --pcre2 "$K"'(?:get|set|setex|del|wrap|fetch|remember|Get|Set)\(' "${X[@]}" "${ROOTS[@]}" | xargs -0 -r rg -n --pcre2 "$C"'(?:\x60[a-z][\w.-]*:(?![^\x60\n]*'"$ID"')[^\x60\n]*\$\{[^\x60\n]*\x60|f["\x27][a-z][\w.-]*:(?![^"\x27\n]*'"$ID"')[^"\x27\n]*\{[^"\x27\n]*["\x27]|["\x27][a-z][\w.-]*:["\x27]\s*\+\s*(?![^,)\n]*'"$ID"')\w+)'
rg -n --pcre2 "$C"'(?:\bCacheInterceptor\b|@CacheKey\(|\bcache_page\(|\bCacheMiddleware\b|\bUpdateCacheMiddleware\b|\bapicache\b|@fastify/caching|\bcaches_(?:action|page)\b|\bunstable_cache\(|["\x27]use cache["\x27]|@Cacheable\(|\bcache\s*:\s*\[\s*["\x27\x60]|\bcache\s*:\s*\{\s*id\s*:|\.cache\(\s*["\x27\x60])' "${X[@]}" "${ROOTS[@]}"
rg -n --pcre2 "$C$K"'(?:get|set|setex|fetch|remember|Get|Set)\(\s*(?:\x60[^\x60\n]*\$\{[^}\n]*(?:Date\.now|new Date|randomUUID|uuid|requestId|JSON\.stringify\((?:req|request)\.(?:query|body))|f["\x27][^"\x27\n]*\{(?:time\.time|datetime\.now|uuid))' "${X[@]}" "${ROOTS[@]}"

# 4. Invalidation: per file that writes a cache, its writes against its invalidations (4a); every invalidation call
#    site, to map against the write paths of the data each cache holds (4b); delete-before-write (4c).
rg -c --pcre2 "$C$K"'(?:set|setex|hset|getOrSet|wrap|remember|put|Set|write)\(' "${X[@]}" "${ROOTS[@]}" | while IFS=: read -r f n; do d=$(rg -c --pcre2 "$K"'(?:del|unlink|delete|evict\w*|invalidate\w*|forget|clearCache|expire)\(|@CacheEvict\b' "$f"); echo "$f  writes=$n invalidations=${d:-0}"; done
rg -n --pcre2 "$C"'(?:'"$K"'(?:del|unlink|evict\w*|invalidate\w*|forget|clearCache)\(|@CacheEvict\b|@CachePut\b|\bon_commit\(|\bafter_commit\b|\bafterCommit\b)' "${X[@]}" "${ROOTS[@]}"
rg -n -U -o --pcre2 "$C$K"'(?:del|unlink|delete|evict|invalidate\w*|forget|clearCache)\([^\n]*\n(?:[^\n]*\n){0,8}?[^\n]*\b(persistAndFlush|flush|save|update|insert|commit|execute|\$transaction|transactional|create)\w*\(' -r 'invalidate, then $1' "${X[@]}" "${ROOTS[@]}"

# 5. Failures cached as data: a write of null / an error / an empty value (5a); a write inside an error handler (5b);
#    a falsy cached value read as a miss (5c).
rg -n --pcre2 "$C$K"'(?:set|setex|put|Set|write)\([^,\n]+,\s*(?:null|undefined|None|nil|\[\]|\{\}|err\w*|error\w*|e)\s*[,)]' "${X[@]}" "${ROOTS[@]}"
rg -n -U -o --pcre2 '\bcatch\s*(?:\([^)\n]*\))?\s*\{(?:[^\n]*\n){0,6}?[^\n]*'"$K"'(?:set|setex|put|Set)\(|\bexcept\b[^\n]*:[ \t]*\n(?:[^\n]*\n){0,6}?[^\n]*'"$K"'(?:set|set_many)\(' -r 'cache write inside an error handler' "${X[@]}" "${ROOTS[@]}"
rg -n --pcre2 "$C"'(?:\bif\s*\(\s*!\s*(?:await\s+)?\w*(?:[Cc]ached|FromCache|fromCache)\w*\s*\)|\bif\s+not\s+\w*cached\w*\s*:|'"$K"'get\([^)\n]*\)\s*(?:\|\||\bor\b)\s)' "${X[@]}" "${ROOTS[@]}"

# 6. HTTP caching headers: Cache-Control / Vary / ETag set in code (6a); static serving in code (6b) and proxy cache
#    rules (6c).
rg -n --pcre2 "$C"'(?:(?i:["\x27]cache-control["\x27])\s*[,:]\s*["\x27\x60][^"\x27\x60\n]*|@Header\(\s*["\x27](?i:cache-control|vary)["\x27]|\bcache_control\(|\bpatch_cache_control\(|\bvary_on_(?:cookie|headers)\b|\bfresh_when\(|\bstale\?\(|(?i:["\x27]vary["\x27])\s*[,:]|\bsetHeader\(\s*["\x27](?i:vary|cache-control|expires|etag)["\x27])' "${X[@]}" "${ROOTS[@]}"
rg -n --pcre2 "$C"'(?:\bexpress\.static\(|\bserveStatic\(|\bServeStaticModule\b|@fastify/static["\x27]|\bregister\(\s*fastifyStatic\b|\bStaticFiles\(|\bWhiteNoise|\bpublic_file_server\.headers|\bUseStaticFiles\()' "${X[@]}" "${ROOTS[@]}"
rg -n --pcre2 '(?i:^\s*(?:expires\s+\S+|add_header\s+cache-control\b|header\s+[^\n]*cache-control|proxy_cache(?:_valid)?\b|file_server\b))' -g '{Caddyfile*,*.conf,nginx*,*.caddy}' -g '!**/node_modules/**' .

# 7. Writes that put data in the cache: a set from request input (what was sent, not what was stored) (7a); a set inside
#    a transaction block, before the commit (7b).
rg -n --pcre2 "$C$K"'(?:set|setex|hset|put|Set|write)\([^\n]*\b(?:dto|body|input|payload|req\.body|request\.data|params)\b' "${X[@]}" "${ROOTS[@]}"
rg -n -U -o --pcre2 '(?:\btransactional\(|\$transaction\(|\btransaction\.atomic\b|@Transactional\b|\.transaction\(\s*(?:async\s*)?\(|\bDB::transaction\(|\bActiveRecord::Base\.transaction\b|\.BeginTransaction\()(?:[^\n]*\n){0,20}?[^\n]*'"$K"'(?:set|setex|hset|put|Set|write)\(' -r 'cache write inside a transaction block' "${X[@]}" "${ROOTS[@]}"

# 8. The cache as a dependency on the request path: files that build a cache client and set no command or socket timeout,
#    and clients told to wait forever while disconnected (8a); blocking or unbounded store commands (8b).
rg -l --pcre2 "$C"'\bnew\s+(?:Redis|IORedis|Cluster)\s*\(|\bcreateClient\(|\bredis\.(?:Strict)?Redis(?:\.from_url)?\(|\bredis\.from_url\(|\bredis\.NewClient\(|\bConnectionMultiplexer\.Connect' "${X[@]}" "${ROOTS[@]}" | while IFS= read -r f; do rg -q --pcre2 'commandTimeout|socketTimeout|socket_timeout|ReadTimeout|SyncTimeout|AsyncTimeout' "$f" && continue
  fns=$(rg -o -N --pcre2 '\bexport\s+(?:async\s+)?function\s+\K\w+|\bexport\s+const\s+\K\w+(?=\s*=\s*(?:async\s*)?\()' "$f" | paste -sd'|' -)   # a factory: read its call sites
  calls=$([ -n "$fns" ] && rg -n -A8 --pcre2 "\b(?:$fns)\(" "${X[@]}" "${ROOTS[@]}" | awk -v f="$f" 'index($0, f) != 1')   # drop the factory's own file
  t=$(printf '%s\n' "$calls" | rg -c --pcre2 'commandTimeout|socketTimeout'); n=$(printf '%s\n' "$calls" | rg -c --pcre2 "^[^:]+:\d+:.*\b(?:$fns)\(")
  echo "$f  cache client with no command/socket timeout in the file${fns:+ — factory ($fns): ${t:-0} timeout option(s) across ${n:-0} call site(s), read each}"; done
rg -n --pcre2 "$C"'\bmaxRetriesPerRequest\s*:\s*null\b' "${X[@]}" "${ROOTS[@]}"
rg -n --pcre2 "$C"'(?:\.keys\(\s*[\x60"\x27][^\x60"\x27\n]*\*|\bKEYS\s+\S*\*|\bflush(?:all|db)(?:Async)?\(|\bFLUSH(?:ALL|DB)\b|\.(?:hgetall|smembers)\(|\.lrange\([^)\n]*,\s*0\s*,\s*-1\s*\))' "${X[@]}" "${ROOTS[@]}"
```

A finding is a grep hit **plus** a read of the cache wrapper (what it stores, with which key and TTL) **plus** the write paths of the cached data **plus** the entry point. Three blind spots are structural:

- **Keys are built in helpers.** `this.cache.set(normalized, tenantId)` shows no prefix: the wrapper's `key()` method holds it. Read every wrapper once (grep 4a lists the files that write), then judge its callers as a group. Grep 3a reads only templates written as `prefix:${…}`.
- **A two-argument `set` on a port is not a Redis call.** The wrapper may add the TTL inside (`set(host, tenantId)` → `redis.set(key, v, 'EX', 300)`). Grep 1a's tag says whether the file sets an expiry anywhere; the decision comes from reading the wrapper.
- **Invalidation lives far from the cache.** The cache's own file rarely calls its `invalidate`; the commands that change the data do, and grep 4b lists them. A write path that is **absent** from 4b is what §4 is looking for, so the write-path map from § Context is the input, not the grep.

**Measured** (2026-10-02). On a real NestJS-on-Fastify + MikroORM monorepo of about 13,000 tracked files, with `ROOTS` set to the API app and the shared packages, the script runs in about 4 s. Grep 0a reports one library, ioredis, imported by 71 files; 0b, 19 deploy lines (an HPA of 2–10 for the API). Of the 41 files grep 4a lists as Redis writers, most hold **state** (locks, leases, cursors, OTP windows, rate-limit windows, job records); the cache families are a handful (permissions, entitlements, domain and subdomain resolution, list counts). Grep 1, 9 hits: five consumer cursors (state) and two calls through a resolution-cache port whose wrapper sets `'EX', 300`. Grep 2a, 11: three resolvers and a list-count cache read, compute and write with no single-flight in the file, and the permission cache is fronted by a separate single-flight factory. Grep 3a, 8 key templates without an identity token, all state (OTP, lease and leader-lock keys). Grep 4b, 26 invalidation sites: the permission cache is invalidated from eight role and member commands and the domain caches from three domain commands, the map §4 reads. Grep 5, 0. Grep 6, 10 (`public, max-age=300` on a public branding route; `no-store` on token and wallet responses; `immutable` for hashed web assets in the web image's nginx). Grep 7, 1. Grep 8, 5: the shared ioredis connection factory sets `maxRetriesPerRequest: null` and no `commandTimeout`, the shape §8 reads. **Re-measured 2026-10-15** on the same monorepo: that note is stale — the factory still defaults `maxRetriesPerRequest: null`, but the module that builds the request-path client passes `commandTimeout` and a retry cap, and only the BullMQ duplicate keeps `null` (BullMQ requires it on worker connections). 8a now reads a factory's call sites and prints `1 timeout option(s) across 4 call site(s)` instead of a bare "no timeout"; 2a's 6 rows each say to check the callers, where the permission cache's single-flight factory lives. The benchmark fixtures carry almost no cache code: `node-api` and `half-built-crm` return 0 on every grep; `vuln-fullstack` returns its deployment's `replicas: 3` (0b), one `private, no-store` header (6a) and two nginx `expires` rules (6c).

## The 3,000-hit path

1. **Classify and dismiss.** Run grep 4a, read each writing file once, and tag it `cache` or `state`. State families close for §1–§5 and §7 in one line each.
2. **Group by key family.** One decision covers every read and write of one family through one wrapper.
3. **Rank by blast radius × call rate.** Families holding tenant- or user-scoped data first (§3 is a security class), then hot keys in front of the database (§2), then authorization data (§4), then the rest.
4. **Read the top 30 families fully**: wrapper, key builder, TTL, miss path, write paths.
5. **Prefer runtime evidence at scale.** Run the e2e suite with a cache spy that records `(key, tenant of the request)` and fail on any key read by two tenants; count origin calls per key under concurrent misses; replay with `MONITOR` on a local Redis to list the keyspace actually written. Anchor what this finds back to `<file:line>`.
6. **Ledger the rest** as `Live, unreviewed (k families / n hits)` with the command that continues them. Never `checked`.

## Scans for

Severity assumes a cache entry (not state) on a production path. Raise one step for a public or unauthenticated entry point, or a key that is hot by measurement; lower one step when a cache is latency-only and the origin is verified to take 100% of misses.

| § | Class | CWE | Default |
|---|---|---|---|
| 1 | Entry that never expires (no TTL on mutable data; a store with no memory limit or eviction for it) | CWE-400 | medium; high for authorization or pricing data |
| 2 | Stampede: a hot-key miss with no single-flight, lock or early refresh; synchronised expiry | CWE-400 | critical for a hot key in front of the database; medium otherwise |
| 3 | Key defects: identity dimension missing (tenant, user, role, locale, currency), response cache keyed by URL or arguments only, a fixed ORM cache id, a key too fine to hit | CWE-524 | critical when another tenant or user can read the entry; medium for hit-rate keys |
| 4 | Invalidation gaps after writes: a write path that never invalidates, delete-before-commit or inside the transaction, a write that bypasses the cache's owner | — | high; critical for authorization data |
| 5 | Failures cached as data (errors, nulls, empty results for the full TTL); falsy values read as misses; hot not-found lookups never cached | — | medium; high when an outage is cached |
| 6 | HTTP caching headers: cacheable public responses and static assets sent with no or short caching; a missing `Vary`; private responses publicly cacheable (security's, routed) | CWE-525 | medium; high when a shared cache serves one user's response to another |
| 7 | Cache-aside vs write-through mismatch: the cache written from request input, before the commit, inside the transaction, or from a lagging replica | — | high |
| 8 | The cache as a dependency: no command timeout, commands queued forever while disconnected, no fallback, origin sized for the hit rate; blocking or unbounded store commands | CWE-400 | high; critical for `KEYS *` or `FLUSHALL` on a production path |

### 1. Entry that never expires

```
BAD:   await redis.set(`price:${tenantId}:${sku}`, JSON.stringify(p));          // no EX: stale until someone deletes it
       cache.set(f"dash:{tenant}:{month}", data, None) · Cache::rememberForever('plans', fn () => Plan::all())
       rdb.Set(ctx, key, v, 0) · CacheModule.register({ ttl: 0 })
GOOD:  await redis.set(key, JSON.stringify(p), 'EX', 600) · cache.set(key, data, 3600)
       an immutable or versioned key (v3:…) with no TTL, by design
```
**Read the code:** Is the value derived from mutable data? Is every write path guaranteed to invalidate it (§4), or is the TTL the only backstop? What does the store do at its memory limit (`maxmemory`, `maxmemory-policy`)? A key with no expiry under a `volatile-*` policy is never evicted. Is the TTL's unit right for the library (milliseconds in NestJS's cache manager, seconds in ioredis `EX`, Django and Laravel)? **Finding when** a cache entry derived from mutable data has no expiry and its invalidation does not provably cover every write path, or the store can fill with such entries. **Proof:** write the entry, change the source through a path that does not invalidate, advance time past the intended staleness bound, and assert the read returns the new value; `TTL <key>` in a local Redis returns `-1` before the fix.

### 2. Stampede

```
BAD:   let v = await cache.get(k); if (!v) { v = await db.heavyAggregate(); await cache.set(k, v, 'EX', 60); }   // 100 misses → 100 aggregates
       @Cacheable("catalog") on the homepage query (no sync = true) · Cache::remember('home', 60, fn () => …)
       every key in a warm-up loop written with the same EX 3600 (they all expire in the same second)
GOOD:  an in-flight Map<key, Promise> per process, deleted when the load settles · lru-cache fetch() · singleflight.Group
       @Cacheable(cacheNames = "catalog", sync = true) · Rails race_condition_ttl · Laravel Cache::flexible · a jittered TTL
       a cross-process lock (SET k v NX PX) when the origin cannot take one miss per replica
```
**Read the code:** How hot is the key (call rate, number of replicas)? What does the miss cost (an aggregate, a third-party call, a full scan)? Is there a single-flight per process, a lock across processes, early refresh or stale-while-revalidate? Does single-flight per process suffice, or does the origin need one call per cluster (miss cost × replicas)? Are keys written together with one TTL constant? This § grades whether a coalescing lock exists; the cross-process lock's own mechanics (owner-checked release, atomic TTL, acquire result, renewal) are distributed-systems `coordination-scan` §1–§4 when installed. A cold or low-rate key, a cheap origin, or a background refresher is not a finding (`precedents/performance.md` § 36). **Finding when** a hot key's miss path recomputes without coalescing and the origin cost is material. **Proof:** clear the key, fire C = 100 concurrent requests, and count origin calls with a spy on the loader: 1 per process after the fix (1 per cluster with a distributed lock), C before. The count is a run-invariant check ([`proof-oracles.md`](../../../../snippets/proof-oracles.md) § "Query-count scaling", counting loader calls instead of queries).

### 3. Key defects

```
BAD:   cache.get(`products:${slug}`) for a catalog scoped per tenant          // tenant A's product served to tenant B
       @UseInterceptors(CacheInterceptor) on GET /me/orders                   // keyed by URL: every user shares one entry
       @Cacheable("prefs") UserPrefs prefs() { var u = SecurityContextHolder…; }   // default key = method arguments (none)
       em.find(Order, { seller }, { cache: ['orders', 60_000] })               // fixed key: the first seller's rows for everyone
       `report:${month}` shared by every seller · key = `q:${JSON.stringify(req.query)}:${Date.now()}`   // never hits
GOOD:  one key builder: `t:${tenantId}:products:${slug}:v2` · CacheInterceptor.trackBy() including the principal
       @Cacheable(key = "#userId") with the user as an argument · cache: [`orders:${tenantId}:${seller.id}`, 60_000]
       normalised, ordered query parameters in the key; no timestamps or request ids
```
**Read the code:** Is any field of the cached value scoped by tenant, user, role, permission, locale or currency? Does the key carry each of those dimensions, or is the cache instance or namespace per tenant? For response caches (`CacheInterceptor`, `cache_page`, `apicache`, Next `unstable_cache`), what does the default key include, and is the route authenticated? Does the key include something unique per request (a timestamp, a request id, an unordered serialisation), so it never hits? Does a single-flight key omit the tenant, coalescing two tenants into one answer? **Finding when** a scoped value is cached under a key that omits its scope, or a key cannot repeat. **Proof:** [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § "Cross-tenant denial": prime the entry as tenant A, read as tenant B, and assert a miss or B's own data (it fails before the fix); repeat for user, role, locale and currency. For a too-fine key: two identical requests, and the second is a hit.

### 4. Invalidation gaps after writes

```
BAD:   updatePrice() writes the row and calls cache.invalidate(sku); bulkImportPrices() and the admin CSV path do not
       await redis.del(`order:${id}`); await em.flush();           // a reader repopulates the old row between the two
       a nightly import writes prices with raw SQL, bypassing the repository that owns the invalidation
GOOD:  every write path from the § Context map invalidates (or the cache key carries a version the write bumps)
       commit, then delete: Django transaction.on_commit(lambda: cache.delete(k)), Rails after_commit, Spring
       @TransactionalEventListener(phase = AFTER_COMMIT), a MikroORM afterFlush hook, an outbox event
       a short TTL as the backstop; versioned keys (cache_key_with_version) where writes are many
```
**Read the code:** For each cache family, which write paths change its source of truth (commands, admin, imports, bulk updates, jobs, raw SQL, migrations, other services)? Does each invalidate, or bump a version the key carries? Is the invalidation after the commit, or before it or inside the transaction (a concurrent reader repopulates the old value, and a rollback leaves the cache cleared for data that never changed)? Does the invalidation reach every replica's copy (a process-local copy is `request-path-scan` §17's)? A cache filled from **another service's** API and invalidated by that service's events: does the delete compare a version or position carried by the event, or can an older event (or a fill that started before it) leave the stale value — the fill needs the event's version or a lease token? How long is the TTL backstop, and is the staleness acceptable for this data (an authorization decision is not)? **Finding when** a write path changes cached data with no invalidation, or the invalidation can race the commit. **Proof:** write-then-read through each write path: change the data, then read through the cached path and assert the new value (it fails for the uncovered path). For delete-before-commit, interleave a reader between the delete and the commit with a barrier and assert the cache holds the new value once both finish.

### 5. Failures cached as data

```
BAD:   try { v = await partner.fetchRates(); } catch { v = null; } await cache.set(k, v, 'EX', 3600);   // one blip, an hour of nulls
       const cached = await cache.get(k); if (!cached) …            // a cached 0, '' or false is treated as a miss, recomputed every time
       a not-found lookup on a hot path never cached: every request for a missing slug reaches the database
GOOD:  cache only successes; cache a failure for seconds, not the success TTL, and distinctly (a tagged negative entry)
       if (cached !== null && cached !== undefined) · a wrapper that stores { v } so absence and falsy differ
       negative caching with a short TTL for hot not-found keys, invalidated when the row is created
```
**Read the code:** What does the miss path do when the origin fails or times out: return an error, a default, `null`, an empty list? Is that result written to the cache, and for how long? Does the read treat every falsy value as a miss? Are hot not-found lookups (domains, slugs, API keys) cached negatively, and is the negative entry cleared when the row appears? Negative caching deliberately off for keys whose existence flips often is not a finding. **Finding when** a transient failure is cached for the normal TTL, a legitimate falsy value is never served from the cache, or a hot not-found path reaches the origin on every request. **Proof:** make the origin fail once (fault injection in [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § "Fault injection"), then restore it and assert the next read returns fresh data within the failure TTL; for falsy values, count origin calls across two reads of a cached `0`.

### 6. HTTP caching headers

```
BAD:   express.static('public') / @fastify/static / WhiteNoise / UseStaticFiles serving hashed bundles with no max-age
       a public, rarely changing JSON catalog sent with no Cache-Control and no ETag
       content varied by Accept-Language or Accept-Encoding with no Vary: the CDN serves one language to all
GOOD:  hashed assets: Cache-Control: public, max-age=31536000, immutable · unhashed HTML: no-cache plus an ETag
       public API reads: public, max-age=<seconds>, s-maxage for the CDN, stale-while-revalidate where tolerated
       Vary on every request header the body depends on · authenticated responses: private, no-store (security's)
```
**Read the code:** Is the response the same for every caller (no session, no `Authorization`, no tenant from the host)? Are asset names content-hashed (so a long `max-age` with `immutable` is safe)? What does the proxy or CDN config add or override (grep 6c)? Which request headers change the body, and does `Vary` list them? Is the route authenticated, in which case the private leg is `data-exposure-scan`'s (§ Boundaries)? **Finding when** a cacheable public response or hashed asset is sent without usable caching, or a missing `Vary` lets a shared cache serve the wrong variant. **Proof:** an HTTP test asserts the headers on the real route (`app.inject` / supertest / the Django test client); for `Vary`, two requests with different `Accept-Language` through a caching proxy return different bodies. Response bytes and request counts per page view before and after are the impact, labelled measured.

### 7. Cache-aside vs write-through mismatch

```
BAD:   await cache.set(`profile:${id}`, dto);  await repo.update(id, dto);    // the request body, not the stored row
       await em.transactional(async (tx) => { tx.persist(o); await redis.set(`order:${o.id}`, …); });   // cached before commit
       read-after-write served from a replica, then cached for the full TTL
GOOD:  write the database, commit, then invalidate (cache-aside) or set from the committed row (write-through)
       one strategy per family: every write path either invalidates or writes through, never a mix
       populate the cache only from the primary, or from a read whose lag is bounded below the TTL
```
**Read the code:** Is the cache written with what the client sent, or with what the database stored (defaults, triggers, normalisation, server-set fields)? Is it written before the commit, or inside a transaction that can still roll back? Do different write paths use different strategies for the same family (one writes through, another invalidates, a third does neither)? Does a populate on miss read from a replica that can lag? **Finding when** the cache can hold data the database never committed, or a value that differs from the stored row. **Proof:** fault injection after the cache write and before the commit: assert the cache does not hold the rolled-back value; a write whose stored row differs from the request (a server default) reads back the stored row.

### 8. The cache as a dependency

```
BAD:   new Redis(url, { maxRetriesPerRequest: null }) shared by the request path      // a GET waits for the reconnect, however long
       a cache read with no timeout on every request, and no fallback when the cache errors
       the database sized for a 95% hit rate, with no cap on the miss rate after a flush or a key-version bump
       await redis.keys('session:*') on a request path · HGETALL on a hash that grows per user
GOOD:  a separate connection for the request path: commandTimeout set, offline queue off or bounded, errors caught
       and treated as a miss, with the miss path rate-limited · SCAN instead of KEYS · bounded collections
       a load test with the cache flushed: the origin holds, or a documented degraded mode engages
```
**Read the code:** Which client does the request path use, and with what options (`commandTimeout`, `connectTimeout`, `enableOfflineQueue`, `maxRetriesPerRequest`; redis-py `socket_timeout`; go-redis `ReadTimeout`)? Is it the same connection a queue or worker needs to wait on? What happens to a request when the cache errors or hangs: an error, a hang, a miss? Can the origin take the full miss rate after a flush, a deploy that bumps a key version, or a cold start? Are `KEYS`, `FLUSHALL` or whole-collection reads on a production path? **Finding when** a cache outage or slowdown can block or fail requests that the origin could have served, or a blocking command runs on a production path. **Proof:** [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § "Timeout firing": a cache endpoint that accepts and never answers (Toxiproxy `timeout`, or a local socket that never writes); the request completes from the origin within its budget after the fix and hangs before it.

## Output

```
caching-scan — lanes: nestjs 11 on fastify, ioredis 6, mikro-orm 6.6; django, spring, rails, laravel absent
Context: 14 Redis families (5 cache, 9 state) · API HPA 2–10 · maxmemory-policy: not in the repo (managed default unknown)

Findings: 2 · Unconfirmed: 1

1. src/catalog/catalog.cache.ts:22                             [report-with-fix]   critical
   §3 key without tenant — `catalog:${slug}` caches a per-tenant catalog; the wrapper is read by GET /storefront/:slug.
   Proof: test/catalog/catalog.tenant-cache.e2e-spec.ts — primed as tenant A, read as tenant B → A's 12 products (fails).
   Fix: build every key in CatalogCache.key(tenantId, slug). CWE-524 · owner: security (deduped with
   @tenant-isolation-reviewer by file:line)

2. src/infrastructure/redis/redis-connection.ts:66             [report-with-fix]   high
   §8 request path on a wait-forever client — the shared ioredis factory sets maxRetriesPerRequest: null (needed by the
   queue workers) and no commandTimeout; the list-count cache reads through it on every list request.
   Proof: Toxiproxy timeout on the Redis port → GET /orders held 30 s+ (fails; budget 2 s). Fix: a dedicated request-path
   connection with commandTimeout 200 ms and enableOfflineQueue false; a cache error counts as a miss.

3. src/shared/persistence/count-strategy.ts:181                [report-flagged]    medium
   §2 count cache with no single-flight — get → COUNT(*) → set on the list-count key; no in-flight map in the file.
   Unproven link: the key's call rate. Settling probe: 100 concurrent GET /orders after DEL of the key, counting COUNT
   statements (expect 1 per pod). Fix: an in-flight Map<key, Promise> deleted on settle.

Verification: 19 candidates → 2 findings · 1 unconfirmed · 9 hardening · 0 pre-existing · 7 refuted

Class coverage:
  §1  no expiry                     checked (9 hits → 0 findings: 5 cursors are state, 2 calls go through a port with EX 300)
  §2  stampede                      checked (11 hits → 1 unconfirmed; permission cache fronted by a single-flight factory)
  §3  key defects                   checked (8 templates → 0 among them: all state keys; 1 finding from the wrapper read)
  §4  invalidation                  checked (5 cache families, 26 invalidation sites mapped to 14 write paths → 0 findings)
  §5  failures cached               checked (0 hits; misses and errors are not written)
  §6  HTTP headers                  checked (10 hits → 0 findings; private routes routed to data-exposure-scan: none open)
  §7  write-through mismatch        checked (1 hit → 0 findings: payload built from the stored row)
  §8  cache as a dependency         checked (5 hits → 1 finding)
```

`[report-with-fix]`: the key family, what it holds, the entry point and the missing control are cited, the oracle fired, and the fix is local. `[report-flagged]`: one link is unproven (a call rate, a write path outside the repo, a store setting not in the repo), and the row names it and the settling probe. Numbers carry their label, **measured** or **ESTIMATED**; a number no tool produced is deleted. The coverage block lists **all eight** classes on every run: `checked (k hits → m findings)` only when the grep ran on a present lane; `N/A (<reason>)` only when the repo has no such surface (no cache library, no static serving); `blocked (<reason>)` when a grep failed or code could not be read; `Live, unreviewed (k families / n hits)` for families left after triage.

## False positives / precedents

The verifier reads [`precedents/performance.md`](../../../../snippets/precedents/performance.md) § "Caching" (precedents 34–36) and § "Memory" (32: a bounded cache is bounded), plus [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 4. The ones this skill meets most:

- **Immutable and versioned keys need no TTL** (§ 34): content-hashed assets, `v3:`-prefixed keys a write bumps, memoised pure functions of their key.
- **A key without a tenant is fine for global data** (§ 35): a public catalog shared by design, feature-flag definitions, a host-to-tenant resolution map keyed by the host. It flips back when any field of the value is tenant-, user-, locale- or permission-scoped.
- **"A cache in front" clears nothing on its own** (§ 36): it is a control only when its key covers the path, its hit ratio is measured and its miss path is bounded.
- **State is not a cache.** Locks, leases, cursors, OTP and single-use records, rate-limit windows and job records are kept without a TTL, or deleted by their owner, by design.
- **An L1 with a short TTL plus pub/sub invalidation in front of a shared L2** is coherent enough for most data; staleness inside a documented TTL is the design, not a bug.
- **A cold or low-rate key** with a cheap origin does not need single-flight; a background refresher (`refreshAfterWrite`, a warmer) replaces it.
- **Negative caching deliberately off** for keys whose existence flips often is a decision, not a gap.

## When to run

- On any diff that adds or changes a cache read or write, a key builder, a TTL, a cache library or its client options, a response-cache decorator or middleware, `Cache-Control` / `Vary` headers, static serving, or a write path of data some cache holds: the `/perf-audit` dispatch signal.
- On every whole-repo `/perf-audit`, reporting all eight classes.
- When an incident involved stale data, one user seeing another's data, a cache outage that became an API outage, or a database spike after a deploy or cache flush.

## Halt conditions

- Do not report a critical or high row as confirmed until a verifier other than the run that found it has passed it through [`refute-before-report.md`](../../../../snippets/refute-before-report.md). Under `/perf-audit` that happens in its verification phase; run standalone, apply the protocol as a separate second pass, tag those rows `self-verified`, and list the rest as Unconfirmed, Hardening, Pre-existing or Refuted. Never drop them.
- Halt on any finding without the cache read or write `<file:line>`, the key family and what it holds, the entry point, and the fix.
- Do not judge a key family before classifying it as cache or state.
- Do not mark a §3 row `[report-with-fix]` without the two-tenant (or two-user) test failing first; route it to the security owner when that pack is installed.
- Do not propose a longer TTL, a bigger cache instance, or "add a cache" as the fix for a correctness class; the fix is the key builder, the invalidation, the commit ordering or the failure handling. A new cache layer goes to `@caching-architect`.
- Do not print "no cache issues" without the class-coverage block. A class whose grep did not run is `blocked`, never `checked`.
- Do not re-derive a class another skill owns (§ Boundaries); cross-link it.

## Related

- `/perf-audit` dispatches this skill and folds its coverage block into the class ledger; `/perf-fix` closes the findings with a failing-first oracle, the root fix, a re-run of this detector on the patched line, and the sibling search.
- `@caching-architect` (this pack) designs caches and invalidation; `memory-growth-scan` (this pack) owns in-process caches with no size bound; `memory-leak-hunt` (this pack) confirms memory growth over a soak.
- `@tenant-isolation-reviewer` § "Caches" and `data-exposure-scan` § "9. Private responses cacheable" (security pack, when installed) own the cross-tenant and private-response consequences.
- `request-path-scan` (this pack) owns outbound timeouts in general (§12) and process-local state across replicas, a cache's coherence included (§17); `@resilience-reviewer` (distributed-systems pack, when installed) owns retry and breaker policy. The backend pack's `caching-strategy.md` (when installed) is the method behind the fixes.
- [`proof-oracles.md`](../../../../snippets/proof-oracles.md) (§ "Cross-tenant denial", § "Fault injection", § "Timeout firing", V33) and [`precedents/performance.md`](../../../../snippets/precedents/performance.md) are the shared proof and precedent files.

Sources (fetched 2026-10-02): NestJS docs, *Caching*; MikroORM 7.2 docs, *Result cache*; TypeORM docs, *Caching queries*; Django 5.2 docs, *Django's cache framework*; Django REST framework docs, *Caching*; Spring Framework docs, *Cache annotations*; Rails 8.0 guide, *Caching with Rails*, and `activesupport/lib/active_support/cache.rb` (8-0-stable); Laravel 12.x docs, *Cache*; ioredis 6.0 `RedisOptions.ts`; BullMQ docs, *Going to production*; lru-cache 11 `src/index.ts`; Redis docs, *Key eviction*. The class list, shapes and oracles come from the performance research catalog for this pack (2026-10-02: CM-01 to CM-05, SC-02 and RS-06; its source notes F, SC23 cache-as-capacity). Paraphrased; no text reproduced beyond short quoted phrases.

---
name: url-shortener
description: Design a URL shortener at scale (TinyURL / bit.ly style): short-code generation, redirect path, cache, partitioning, analytics, abuse. Topic playbook from the System Design series EP22. Use when the system is a link shortener, redirect service, or any read-heavy key-to-value lookup at scale. Sensors and evals gate.
user_invocable: true
---

Design a URL shortener. Topic playbook. The agent loads this reference and adapts it to the user's
real scale and product rules, then emits the SDD via the generic template.

Use when the problem is: a link shortener, a redirect service, vanity/branded short links, or any
read-dominated lookup of an opaque key to a stored value. Looks tiny, hides almost every core system
design theme: read>>write load, unique key generation, cache, partitioning, consistency, abuse,
analytics, multi-region.

Ask once if missing: target read QPS, custom-alias support, single vs multi-region, dedup policy
(same long URL = same code or not), edit/disable-after-create.

Read:
- guides/design-method.md
- guides/writing-style.md
- guides/templates/system-design.md
- guides/pipeline.md

Generate the SDD using the template, filled with the reference below, adapted to user scale.

Save to .claude/runtime/outputs/architect/design/{feature_id}.md.
Sensors: sensors/design-structure.md, sensors/design-rigor.md. Evals: evals/design-quality.md.

---

## Reference architecture (adapt, do not copy blindly)

One line: two very different flows share one product. **Create** is moderate write. **Resolve** is
huge read and latency-critical. Design the architecture around redirect; everything else bends to it.
Product and priority first, technology second. Anyone drawing Kafka in the first three minutes is
answering the wrong question.

### Requirements

Functional: long URL -> unique short URL; resolve short -> redirect to original; optional expiry;
custom alias; basic analytics (click, ts, user agent, referer, approx country); disable/ban malicious
links. Staff-level extras: TTL links, logical delete/tombstone, optional dedup, preview page for
suspicious links, rate limit per account/IP/tenant, multi-tenant custom domains, different SLA for
redirect vs analytics.

Non-functional priority order: **redirect availability** (if create fails for seconds it is bad; if
redirect fails the product dies) > low redirect latency (tens of ms on cache hit) > durability (an
issued code's mapping must never vanish) > horizontal read scale > security/anti-abuse >
observability.

### Scale sizing (worked example, redo with user's numbers)

`ASSUMPTION: 100M new links/month, 3B redirects/month, read:write ~30:1, peak 5x avg, 5y retention.`
- Writes: 100M / 2.6M s ~ 38 wps avg, ~200 wps peak. Trivial.
- Reads: 3B / 2.6M s ~ 1157 rps avg, ~6k rps peak. Comfortable for a well-built service, but
  enterprise/viral/QR/global can push to tens or hundreds of k rps. Design to grow.
- Storage: ~1 KB/record (code 8-10 B, long URL ~500 B, metadata 100-200 B). 6B records over 5y =
  ~6 TB raw, 15-25 TB with indexes/replication/backup. **Hot data is small, total data is large**,
  that distinction drives cache + storage choices.
- Analytics: 3B events/month. Never a synchronous counter on the transactional DB. Decouple it.

### API

`POST /v1/links` {long_url, custom_alias?, expires_at?, domain?, idempotency_key?} ->
{short_url, code, created_at, expires_at}. `GET /{code}` -> 301 if mapping is immutable (lower
perceived latency on repeat), 302/307 if you want flexibility (avoids aggressive client caching when
target may change). The 301-vs-302 choice is control vs efficiency. Product questions that change the
architecture: can a link be edited after create? can an alias be reused after expiry? same long URL =
same code or not? These drive idempotency, cache, and invalidation.

### Data model (two domains)

- **Transactional links table**: `code PK, long_url, url_hash?, owner_id?, domain, created_at,
  expires_at?, status(active|disabled|expired|banned), is_custom, redirect_type, metadata_json`.
  Indexes: PK on code, (owner_id, created_at), expires_at if TTL cleanup is frequent, url_hash if dedup.
- **Analytics events** (async, columnar / data lake / stream): `code, timestamp, ip_prefix or hashed
  IP, user_agent_hash, referer_domain, country, device_type`. Never on the synchronous redirect path.

### Short-code generation (the classic question)

- **A. Hash of long URL** -> base62. Deterministic, easy dedup, but truncation collides, same input
  forces same output, predictable/enumerable.
- **B. Sequential ID -> base62.** Simple, short, no collision with a good generator; but pure
  sequential is predictable, leaks volume, scrapeable.
- **C. Unique ID + reversible obfuscation -> base62.** Best practical answer: generate 64-bit unique
  ID, pass through a keyed bijection (Feistel network / bijective permutation), base62 encode, optional
  fixed-length pad. Preserves uniqueness, resists guessing.
- Code length (base62): 62^7 ~ 3.5T, 62^8 ~ 218T. 7 chars fits most; 8 gives operational slack.
  Custom alias bypasses this logic.
- **Staff design**: centrally-coordinated unique ID by ranges (or decentralized with uniqueness
  guarantee), reversible bijection to cut predictability, base62 encode, validate uniqueness in storage
  as last line of defense.

### Unique ID generation

- DB auto-increment: fine for MVP, central hotspot, blocks active multi-region.
- Snowflake-style (timestamp + worker id + local sequence): horizontal, time-ordered, DB-independent;
  watch clock skew, worker-id coordination, bit layout.
- Range allocation (service hands out blocks of 1M IDs per instance): very simple, near-zero
  per-request coordination; wastes IDs on restart (usually fine), needs reliable refill.
- For this case, range allocation or snowflake both work well.

### Create flow

Validate URL (http/https only; block SSRF targets: 127.0.0.1, 169.254.169.254, RFC1918, internal
hostnames; canonicalize; size limit; punycode/suspicious chars) -> check custom alias availability and
policy -> generate code -> persist to transactional DB -> write-through cache -> return short_url.
Idempotency: store the response per idempotency_key for a short window so client retries do not mint
duplicate links. **Dedup default: do not globally dedup** in the main product (breaks per-campaign /
per-tenant analytics, privacy, and distinct links for the same landing page). If wanted, dedup only as
an internal storage optimization, separating the logical link entity from the physical URL target.

### Redirect flow (the heart)

`GET /{code}` -> edge/app reads distributed cache -> hit returns target in a few ms -> emit analytics
event async/in parallel -> respond 301/302 with Location. On miss: read transactional DB or read
replica, validate status + expiry, populate cache with appropriate TTL, redirect. **Cache negative
results** (nonexistent code) for a short TTL (30-60s) to survive random-code miss storms. TTL choice:
if mapping is immutable, TTL can be hours and invalidation nearly disappears; if links can be
disabled/edited, choose short TTL, event-based invalidation, or split layers, keep the destination
near-immutable and use a fast blacklist for urgent blocks.

### Cache (read-heavy core)

L1 local per-instance for extreme hot keys, L2 distributed (Redis), transactional DB as source of
truth. Hot-key care: ensure the hot value fits L1; **single-flight** on miss so 1000 simultaneous
misses cause one DB fetch; limit concurrent refresh. Stampede control via request coalescing and
refresh-ahead.

### Storage choice

Workload is PK lookup by code, few relations, moderate write, very high read, strong durability. SQL
or a persistent KV both fit; what matters is efficient key lookup, mature replication, reliable
backup/restore, team familiarity. **Pragmatic pick: mature relational (Postgres)** with partitioning
when needed, read replicas, heavy cache in front. Evolve to Dynamo/Cassandra-style only when scale
truly forces it. Staff answer = the smallest system that holds the load with margin and evolves safely,
not the most exotic tech.

### Partitioning

Partition by code (or its internal ID). Hash partition: even distribution, good for random lookup,
harder rebalancing, no time locality. Range partition by time/ID: good archive/lifecycle and locality,
but monotonic ID creates a hot newest shard. For redirect lookup prefer hash or pseudo-random over the
obfuscated ID; analytics partitions differently.

### Consistency

Strong: custom-alias uniqueness (unique index on (domain, code)), link persisted before success
response, critical admin status changes. Eventual: analytics, cross-region DR replication, aggregated
dashboards. Redirect may read a replica if you accept a small post-create window, handle
read-after-write via region-sticky reads for a few seconds, write-through cache (resolves it well), or
fallback to primary when the replica lags.

### Multi-region

Separate create and resolve. **Resolve** is read-dominant and cacheable -> push to edge + multiple
regions, stateless regional service with strong regional cache. **Create** can start single-writer per
primary region (simplifies alias uniqueness + ID generation). Evolution: (1) one create region, many
redirect regions with replica + cache; (2) multi-region create with per-region ID ranges/namespaces;
(3) sophisticated active-active only if the business demands. Avoid premature active-active.

### Analytics without hurting redirect

Redirect is path A, analytics path B, never tightly coupled. Redirect responds fast; click event goes
to a queue/log; consumers aggregate counters per minute/hour/day/country/device/referer; dashboards
query a separate analytical store. If the queue dies: best-effort (drop analytics, keep redirect),
short local buffer with retry, or sampling under degradation, always preserve redirect first.
Retention tiers: raw 30 days, hourly aggregate 1 year, daily aggregate 5 years.

### Security and anti-abuse

Risks: phishing, malware, spam, link enumeration, open-redirect abuse, SSRF during validation.
Controls: rate limit per IP/token/tenant/suspicious ASN, domain reputation at create time, safe-
browsing checks (sync/async by risk), fast link disable, preview interstitial for suspicious links,
progressive friction/CAPTCHA, stronger auth for high-volume accounts. Anti-enumeration: obfuscation +
adequate code length + rate limit on the resolve endpoint + scan-pattern monitoring. Privacy: minimize/
truncate/short-window-hash IPs.

### Lifecycle and custom alias

Expiry: persist expires_at, validate at read time (do not rely only on offline cleanup, or an expired
link survives in cache), evict from cache on expiry, async cleanup job for archive/logical delete.
Tombstone banned/removed links to prevent reuse and aid audit. Custom alias needs strong consistency
(unique index on (domain, code)), reserved words (admin, login, api), per-tenant policy, no collision
with internal routes, minority of traffic, high value, so allow a stricter create flow.

### Observability

Metrics: create/resolve QPS, resolve p50/p95/p99, cache hit ratio per layer, errors by class,
not-found rate, banned/expired access rate, create->first-resolve propagation time, analytics pipeline
throughput/lag. Logs: sampled access logs, audit logs for admin ops, structured with correlation id.
Tracing: full on create path; sample on the hot resolve path. Alerts: cache-hit-ratio drop, p99 rise,
redirect error over threshold, abnormal 404 growth (scan), analytics backlog growth.

### Failure modes

- Cache down -> DB avalanche. Mitigate: rate limit + circuit breaker, L1 local for hot keys, degrade
  analytics, shed suspicious traffic.
- DB degraded -> misses and creates suffer. Mitigate: serve hot keys from cache, queue/retry creates,
  failover to promoted replica, protect alias operations.
- Region down. Mitigate: DNS/anycast to another region, pre-warmed regional replicas/caches; create may
  be briefly unavailable, redirect must survive.
- Reputation system down. Mitigate: degraded mode with local rules, more friction for new users, later
  review of links created in the window.

### Roadmap

1. MVP robust: one region, stateless API, Postgres primary + replica, Redis cache, range ID generator,
   analytics events on a queue, basic offline aggregate dashboard.
2. Medium scale: L1 local cache, hot-key control, DB partitioning or more distributed storage,
   multi-region redirect, maturer analytics pipeline, layered reputation/anti-abuse.
3. Global scale: multi-region create with per-region ranges/namespaces, tested automatic failover,
   per-tenant custom domains, premium branded links + per-client SLA, edge compute for some redirects.

### Common mistakes to avoid

Start from tech not requirements; let analytics block the critical redirect path; truncated hash
without discussing collision/predictability; ignore security/abuse; shard too early when relational +
cache still holds; skip cache invalidation / expiry / read-after-write; skip operations (metrics,
failover, degradation).

<!-- canon: Kleppmann (read>>write load params, consistency models), Vogels (design for failure, eventual consistency), Nygard (circuit breaker, single-flight, bulkhead), Helland (immutable mapping, events for analytics), Jeff Dean (cache-hit latency sizing) -->

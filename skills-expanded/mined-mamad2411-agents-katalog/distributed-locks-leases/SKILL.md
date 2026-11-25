---
name: distributed-locks-leases
description: Implements distributed mutual exclusion and leader election correctly across processes/nodes — Redis `SET key token NX PX <ttl>` with a unique random token + Lua compare-and-delete unlock (never bare DEL), etcd/ZooKeeper/Consul leases (lease grant + TTL + keepAlive renewal, ephemeral znode + watch on predecessor for leader election), and Postgres advisory locks (`pg_advisory_lock`/`pg_try_advisory_xact_lock`) for single-DB serialization — while treating every lock as a LEASE that can expire mid-work, so safety rides on monotonic fencing tokens that the protected resource checks-and-rejects-stale (per Kleppmann's Redlock critique), never on the lock alone. Covers TTL sizing vs work duration, renewal/keepalive, the GC-pause/clock-skew expiry hazard, split-brain, and choosing idempotency or partitioning INSTEAD of a lock.
when_to_use: You need only-one-runner-at-a-time across machines — a leader/singleton (cron that must not double-fire, one active scheduler/consumer), a critical section over a shared external resource (a row, a file, an API quota) spanning multiple nodes, leader election, or you're reaching for Redlock/`SETNX`/etcd leases/ZooKeeper. Distinct from async-concurrency-correctness (in-process mutexes/atomics/channels within ONE process — no network, no lease expiry) and idempotency-keys (the real safety net when the lock fails or expires — make the protected operation safe to repeat instead of/in addition to locking).
---

## When to Use

Reach for this skill when you need **at most one actor running at a time across separate processes or machines**, coordinated through a shared store — and a second concurrent runner would corrupt state:

- "Only one instance should run this cron / scheduler / migration / cleanup at a time"
- "Elect a leader / single active consumer across N replicas" (active-passive failover)
- "Two pods both processed the same job / both wrote the same file"
- "Serialize edits to one row/aggregate/external resource across the cluster"
- "I'm using Redis `SETNX` / Redlock / etcd lease / ZooKeeper ephemeral node for a lock"
- "Hold a lock while I do work, renew it, and release it safely"
- "The lock expired while my job was still running and another node started"

NOT this skill:
- A mutex/semaphore/atomic/channel **inside a single process** (Go `sync.Mutex`, Java `synchronized`/`ReentrantLock`, Python `Lock`, `asyncio` races) — no network, no TTL, no lease expiry → async-concurrency-correctness
- Making the protected operation **safe to run twice** so a lock failure/expiry is harmless (dedup table, upsert, set-don't-increment) → idempotency-keys (this is the safety net BELOW the lock; prefer it over a lock when you can)
- Throttling request *rate* (token bucket / sliding window), not exclusivity → rate-limiting
- Worker pool, job dispatch, DLQ, poison-message handling, exactly-once consumer semantics → message-queue-jobs
- Optimistic concurrency on a single DB row (`WHERE version = N` / `If-Match`/ETag, no separate lock service) → idempotency-keys (by-design) / db-migration-safety for schema
- Timeouts, retries, backoff, circuit breakers around the locked call → resilience-timeouts-retries
- Saga/state-machine coordination of a long multi-step workflow → design-state-machine / orchestrate-agent-workflow

## Steps

1. **First ask: do you actually need a distributed lock? Usually you don't.** A lock is a liveness/correctness liability (a held-but-dead lock stalls everyone; an expired one breaks mutual exclusion). Prefer, in order:

   | Instead of a lock | Technique | Why it's better |
   |---|---|---|
   | **Idempotency** | make the op safe to repeat (upsert, set-don't-increment, dedup key) → idempotency-keys | concurrent runs are *harmless*, not *prevented* — no expiry hazard at all |
   | **Partitioning** | shard work by key (Kafka partition, consistent-hash, `id % N`) so each key has exactly one owner | structural single-ownership, no shared lock at all |
   | **Single-DB serialization** | `SELECT ... FOR UPDATE` / unique constraint / `INSERT ... ON CONFLICT` / advisory lock (step 6) | the DB transaction *is* the lock, with real ACID guarantees |
   | **A queue / leader-elected scheduler** | one consumer per partition; framework-provided leader election (k8s `Lease`, Raft) | offloads the hard part to a tested system |

   Use a distributed lock only for **efficiency** (avoid duplicate work, where a rare double-run is *tolerable*) — NOT as your sole correctness guarantee. For correctness you also need step 4 (fencing) or idempotency.

2. **Treat every lock as a LEASE: it auto-expires after a TTL, and it can expire WHILE you still think you hold it.** This is the central hazard. A lock without a TTL deadlocks the whole system if the holder crashes; a lock with a TTL can expire mid-work (GC pause, CPU starvation, slow I/O, network partition, VM freeze) — then the store hands the lock to node B while node A, paused, *believes* it still holds it and resumes writing. Two writers, one lock. Conclusions that follow:
   - Always set a TTL (no infinite locks).
   - TTL alone is never sufficient for correctness — you must also fence (step 4) or be idempotent (step 1).
   - Pick TTL ≥ p99 work duration + safety margin; renew (step 5) for long work rather than setting a huge TTL.

3. **Redis single-node lock — acquire with a unique token, release with compare-and-delete (Lua), never bare `DEL`.** Use one atomic command and a per-acquisition random token so only the owner can unlock:
   ```
   # acquire — NX = only if absent, PX = TTL in ms, token = unique per acquisition (uuid/16 random bytes)
   SET resource_lock <token> NX PX 30000
   ```
   ```lua
   -- release — DELETE ONLY IF the value is still OUR token (compare-and-delete, atomic)
   if redis.call("GET", KEYS[1]) == ARGV[1] then
     return redis.call("DEL", KEYS[1])
   else return 0 end
   ```
   - **Never** `SETNX` + separate `EXPIRE` (non-atomic: crash between them = a lock that never expires). Use `SET ... NX PX` in one call.
   - **Never** a bare `DEL resource_lock` to release: if your lease already expired and B re-acquired, your `DEL` deletes *B's* lock. The token check prevents that.
   - **Redlock (multi-node) is contested — default to single-node + fencing.** Kleppmann's critique ("How to do distributed locking", 2016): Redlock relies on bounded clocks and pauses it can't guarantee, so it provides neither efficiency nor correctness better than a single node *for correctness*. Antirez disputes the framing, but the practical takeaway holds: **do not rely on any timing-based lock (Redlock included) for correctness — fence the resource (step 4).** Use single-node Redis for the cheap mutual-exclusion-for-efficiency case; reach for a consensus store (step 7) when you need real leader election.

4. **Fencing tokens — the only thing that makes a lease-based lock SAFE. The protected resource must reject stale writers.** On every acquisition, get a **monotonically increasing** token (the "fence"). Pass it with every write to the protected resource. The resource stores the highest token it has seen and **rejects any write carrying a token ≤ the last accepted one.** Now a paused node A (token 33) that wakes after B acquired (token 34) gets its write rejected — mutual exclusion is enforced *at the resource*, independent of who "thinks" they hold the lock.
   ```
   client A acquires → fence=33 → write(x, fence=33)   accepted, resource now at 33
   A pauses; lease expires; B acquires → fence=34 → write(y, fence=34)   accepted, resource at 34
   A resumes, still "holds" lock → write(z, fence=33)   REJECTED (33 ≤ 34)
   ```
   - Source of monotonic tokens: ZooKeeper `zxid`/znode version, etcd key `mod_revision` / a `CreateRevision`-based counter, Redis `INCR fence_counter` (single-node only — multi-node Redis can't guarantee monotonicity), or a DB sequence.
   - The resource MUST participate — if your storage/API can't check-and-reject a token (e.g. a dumb blob store), fencing is impossible and you fall back to idempotency (step 1). Many real systems can't fence; that's exactly why idempotency is the more robust default.

5. **Long work: renew (keepalive) instead of guessing a huge TTL — and abort if renewal fails.** For work that may exceed the TTL, run a watchdog that re-extends the lease at ~TTL/3:
   - Redis: a Lua `PEXPIRE` guarded by the same token check (extend only if still ours).
   - etcd: `LeaseKeepAlive` stream; ZooKeeper: session heartbeats keep the ephemeral node alive; Consul: session renew before TTL.
   - **Critical:** if a renewal FAILS or is late, you may have already lost the lease — **stop doing work immediately** (cancel the in-flight operation), don't blindly continue. The renewer and the worker must share a cancellation signal (context/CancellationToken). A renew thread that keeps extending after the worker is wedged is also a bug (it masks a stuck holder).

6. **Postgres advisory locks — the right tool when one Postgres is your coordination point.** No extra infra; the lock lives in the DB you already trust:
   | Function | Scope | Released by | Use for |
   |---|---|---|---|
   | `pg_advisory_lock(key)` | **session** | explicit `pg_advisory_unlock` or session end | held across transactions; must release manually (leaks if connection pooled + forgotten) |
   | `pg_advisory_xact_lock(key)` | **transaction** | automatically at COMMIT/ROLLBACK | **preferred** — no manual release, no leak; held only for the txn |
   | `pg_try_advisory_lock(key)` | session, **non-blocking** | as above | returns `true/false` instantly — "skip if someone else has it" (e.g. cron singleton) |
   - Key is a `bigint` (or two `int4`s) — hash your logical name: `pg_try_advisory_xact_lock(hashtext('nightly-report'))`. Beware `hashtext` collisions; use a deliberate keyspace for unrelated locks.
   - **Advisory locks are NOT enforced by the data** — they're cooperative; only code that *also* takes the lock is excluded. They don't lock rows. For row-level exclusion use `SELECT ... FOR UPDATE` instead.
   - **Pooling gotcha:** with a transaction pooler (PgBouncer `transaction` mode), session-level advisory locks break (different backend per statement). Use `*_xact_lock` or a `session` pool.

7. **etcd / ZooKeeper / Consul — when you need real leader election and consensus.** These are CP (consistent under partition) consensus stores; use them when a *rare* double-leader is unacceptable:
   - **etcd:** `Lease` (grant TTL) + a key written with that lease; election via the `concurrency.Election` API (campaign → leader holds key until lease lapses or it resigns). `mod_revision` gives you a fencing token for free.
   - **ZooKeeper:** create an **ephemeral sequential** znode; the lowest sequence number is leader; each node **watches only its immediate predecessor** (not all nodes — avoids the herd effect). On predecessor delete, re-check if you're now lowest. Ephemeral = auto-removed on session loss → automatic failover. The Curator `LeaderLatch`/`InterProcessMutex` recipes implement this correctly; prefer them over hand-rolling.
   - **Consul:** session + KV `acquire` flag; session TTL + health check ties lock liveness to the holder's health.
   - **Even here, fence.** Consensus guarantees agreement on *who holds the lease*, but a GC-paused leader still doesn't know its lease lapsed — the resource must still reject its stale-token writes (step 4). Consensus narrows the window; it doesn't remove the mid-work-expiry hazard.

8. **Defend against split-brain and clock skew.** Two nodes both believing they're leader = split-brain. Mitigations: a single consensus source of truth (don't run two independent lock services); fencing tokens so even a split-brain second writer is rejected at the resource; **never trust wall-clock time for lease math across nodes** — use the lock service's own expiry, and within a node use a *monotonic* clock (`CLOCK_MONOTONIC`, `time.monotonic()`, `Instant`/`System.nanoTime`) for "have I exceeded my budget?" since NTP steps and VM time-warps corrupt wall-clock deltas. Assume your process can pause arbitrarily long between any two lines (GC, OS scheduler, live-migration).

## Common Errors

- **No TTL → permanent deadlock on crash.** A holder dies, the lock is held forever, the system stalls. Fix: always set a TTL; renew for long work (step 5).
- **TTL but no fencing → silent double-write on mid-work expiry.** The lock expires during a GC pause, B acquires, A resumes and writes. Fix: monotonic fencing token rejected at the resource (step 4), or make the op idempotent (step 1).
- **`SETNX` then separate `EXPIRE`.** Crash between the two leaves a lock with no expiry = deadlock. Fix: single atomic `SET key token NX PX <ttl>`.
- **Releasing with bare `DEL` / no owner check.** If your lease already expired and someone re-acquired, you delete *their* lock. Fix: Lua compare-and-delete on your unique token.
- **Reusing a constant lock value.** Without a per-acquisition random token you can't tell your lock from a successor's — unlock and renew both become unsafe. Fix: fresh uuid/random token each acquire.
- **Trusting Redlock (or any timing lock) for correctness.** Bounded-clock/bounded-pause assumptions don't hold. Fix: single-node for efficiency-only; fencing/consensus for correctness (steps 3, 4, 7).
- **Renewal failure ignored.** The watchdog can't renew but the worker keeps writing without the lease. Fix: failed/late renew → cancel the work immediately via a shared cancellation signal.
- **Session-level `pg_advisory_lock` behind a transaction pooler.** Different backend per statement → lock acquired on one connection, never released / not visible. Fix: `pg_advisory_xact_lock`, or a session-mode pool.
- **Forgetting to release a session advisory lock.** Leaks until the connection dies; with pooling that connection is reused holding the lock. Fix: prefer `*_xact_lock` (auto-release at txn end).
- **Using a distributed lock where idempotency/partitioning was the right tool.** You inherit the whole expiry/split-brain failure surface for no reason. Fix: revisit step 1 — can the op be idempotent or key-partitioned instead?
- **Wall-clock lease math across nodes.** NTP steps / VM time-warps make "is my lease still valid?" wrong. Fix: trust the lock service's expiry; use a monotonic clock for local budget checks.
- **Watching all nodes in ZooKeeper leader election (herd effect).** Every change wakes every node. Fix: ephemeral-sequential + watch only your immediate predecessor (or use Curator recipes).

## Verify

1. **Mutual exclusion under contention:** spawn N nodes/goroutines racing for the same lock against the *real* shared store; assert exactly one holds it at any instant (e.g. each increments a shared counter inside the section and the section must never overlap — verified with a sentinel that fails if two enter).
2. **Crash releases the lock:** kill the holder mid-section; another node acquires within ~TTL (the lease expires), not never (no permanent deadlock) and not instantly (no missing TTL).
3. **Fencing rejects the stale writer:** simulate the Kleppmann scenario — A acquires (fence 33), pause A, let the lease expire, B acquires (fence 34) and writes, then resume A's write with fence 33 → the resource **rejects** it. Without fencing, this is the test that exposes the double-write.
4. **Atomic acquire:** the acquire path is a single `SET NX PX` (or equivalent) — grep shows no `SETNX`+`EXPIRE` two-step and no infinite/missing TTL.
5. **Safe release:** the unlock only deletes when the stored token matches (Lua/compare-and-delete); a test where the lease expired and was re-acquired confirms the old holder's release does NOT remove the new holder's lock.
6. **Renewal + abort:** for long work, the lease is extended at ~TTL/3 while the token still matches; inject a renewal failure and assert the worker *cancels* rather than continuing without the lease.
7. **Advisory-lock leak/pooling check:** advisory locks are `*_xact_lock` (or explicitly unlocked) and behave correctly under the actual connection-pool mode; `pg_locks` shows no orphaned advisory locks after the txn ends.
8. **Leader election failover:** kill the leader; a new leader is elected within the session/lease TTL; assert there is never *zero* leader for long nor *two* leaders simultaneously (split-brain) — and that a deposed leader's writes are fenced out.
9. **Default-choice justification:** confirm a distributed lock is genuinely needed — document why idempotency (idempotency-keys) or partitioning couldn't replace it; if the lock is correctness-critical, fencing or idempotency is present, not the lock alone.

Done = at most one actor runs at a time under real contention, every lock has a TTL and crash-frees within it, mid-work expiry cannot cause a double effect because the resource rejects stale fencing tokens (or the op is idempotent), acquire/release/renew are atomic and owner-checked, advisory locks are pool-safe and leak-free, leader election survives failover without split-brain, and the choice of a lock over idempotency/partitioning is deliberate — all proven by the contention, crash, and fencing tests in checks 1–8.

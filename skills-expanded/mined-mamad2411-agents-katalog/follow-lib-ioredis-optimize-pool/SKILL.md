---
name: follow-lib-ioredis-optimize pool
description: optimize ioredis — pipelining, connection reuse, retry/offline queue tuning
argument-hint: "[command-or-scope]"
related:
  - follow-lib-ioredis
  - run-bench
  - scan-codebase
  - report-before-after
---

## Goal

Reduce ioredis latency and connection churn — pipelining, connection reuse, retry/offline queue options — measuring before and after, without changing output

## Scope

- Use when Redis commands are slow from round-trips, reconnect storms, or connections being recreated
- Covers: `pipeline()`/`multi()`, connection reuse patterns, `retryStrategy`, `enableOfflineQueue`, `maxRetriesPerRequest`
- If there is no client yet → do `workflows/setup-ioredis/SKILL.md` first

## Execute

### 1. Baseline

> Goal: identify the real bottleneck with numbers

1. Do `/run-bench` or time the slow command paths — commands/sec, latency, RTT count
2. Do `/scan-codebase` looking for: sequential `await` commands in a loop, `new Redis()` created repeatedly per request/function
3. Check `MONITOR` or `SLOWLOG` on the Redis side if accessible — separate slow-from-RTT vs slow-from-the-command-itself
4. Do `/deep-optimize` if wider analysis is needed

### 2. Pipelining

> Goal: combine commands to cut round-trips

1. Batch independent reads/writes → `redis.pipeline()` then `exec()` — cuts RTT from N to 1
2. Need atomicity → `redis.multi()` (transaction) instead of a pipeline
3. On Cluster: pipeline commands must be slot-compatible — group by key slot or use hash tags
4. Check the result array from `exec()` — each entry is `[err, result]`, errors must be checked per command

### 3. Connection Reuse

> Goal: reduce connection churn and pick the right topology

1. One client instance per process per role — never `new Redis()` per request; cache the instance at module level
2. Separate connections: command client / subscriber / publisher — a (RESP2) subscriber blocks other commands
3. `lazyConnect` for clients used on some paths only — avoid a pointless connect at startup
4. If a hot path needs minimal latency → consider a dedicated connection instead of sharing with bulk work

### 4. Tune Retry And Queue

> Goal: reconnect behavior must not amplify failures

1. `retryStrategy(times)` — bounded backoff (e.g. `Math.min(times * 50, 2000)`); `null` = stop retrying
2. `maxRetriesPerRequest` — the default limits retries per command; `null` for BullMQ blocking commands
3. `enableOfflineQueue: false` when failing fast beats a stuck queue (v6: send commands from the `ready` listener)
4. `commandTimeout` to prevent hung commands — a value matching that path's SLO

### 5. Measure Again

> Goal: compare against the baseline

1. Re-measure the same workload — RTT count, latency, commands/sec
2. If there's no improvement or a regression → revert that point and report
3. Passed → `/report-before-after` with the numbers, then `/suggest-next-action`

## Rules

- Baseline always first — never optimize without numbers
- Fix one point at a time ordered by impact — pipelining (RTT) is usually bigger than micro options
- Never share a subscriber connection with the command client
- Preserve behavior — pipelines must check per-command errors, multi must be truly atomic
- If an option is unclear → check official docs
- Use `/follow-lib-ioredis` for the overview and setup

## Expected Outcome

- Round-trips reduced via pipelining — numbers better than the baseline
- Connection reuse correct — no per-request connections
- Retry/queue behavior fits the use case — doesn't amplify outages

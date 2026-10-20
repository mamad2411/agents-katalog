---
name: postgresql-high-availability-and-failover
description: >
  Designs PostgreSQL high-availability topologies with Patroni-managed
  automatic failover or manual streaming-replication failover, covers
  split-brain prevention (fencing, watchdog, consensus store quorum), and
  how to safely test failover without turning a drill into an outage. Use
  when the user asks to "set up PostgreSQL HA," "configure Patroni,"
  "design PostgreSQL automatic failover," "prevent split-brain in
  Postgres," or "test a Postgres failover safely."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: database-operations
  maturity: stable
---

# PostgreSQL High Availability and Failover

## Purpose

PostgreSQL has no built-in automatic failover — a standalone streaming
replica will happily keep serving stale reads forever if the primary
dies, with nothing promoting it unless something external decides to and
does so safely. This skill covers designing that "something external":
most commonly **Patroni** (a consensus-store-backed HA agent that
manages `pg_ctl`, `recovery.conf`/`standby.signal`, and a fencing
mechanism), the split-brain risks any automatic-failover design must
close off, and how to test failover realistically without it becoming an
actual incident. It builds on the replication mechanics covered in
[postgresql-operations-and-performance-tuning](../postgresql-operations-and-performance-tuning/SKILL.md);
this skill is specifically about the failover decision-making and
safety layer on top of that replication.

## When to use

- Designing a new PostgreSQL HA topology that needs automatic failover
  (not just a manually-promoted standby) for RTO reasons.
- Standing up or troubleshooting Patroni (or an equivalent, e.g.
  `pg_auto_failover`, `repmgr` with fencing) — cluster bootstrap,
  consensus store (etcd/Consul/ZooKeeper) integration, or a failed
  failover that left the cluster split-brained.
- Reviewing whether an existing HA design actually prevents split-brain
  (two nodes both believing they're primary and accepting writes
  simultaneously), not just "has a replica."
- Planning or executing a failover test/game-day against a topology
  that's never actually been failed over, or auditing one that's overdue
  for a test.
- Diagnosing a failover that took longer than expected, or one that
  promoted a replica that turned out to be behind the actual most-caught-up
  candidate.

## Prerequisites & environment

- A working streaming replication topology already in place (see
  [postgresql-operations-and-performance-tuning](../postgresql-operations-and-performance-tuning/SKILL.md)
  for setup) — this skill assumes replication mechanics are understood
  and focuses on the failover/fencing layer on top.
- For Patroni: a distributed consensus store — etcd, Consul, or
  ZooKeeper — with an odd number of nodes (3 or 5) across separate
  failure domains, since Patroni's leader election correctness depends
  on that store's own quorum guarantees, not on Patroni itself.
- Patroni installed on each PostgreSQL node, configured with a REST API
  endpoint and (strongly recommended) a fencing/watchdog mechanism —
  either a hardware/software watchdog device (`/dev/watchdog`) or a
  network fencing script that can guarantee a demoted-but-unresponsive
  old primary is actually stopped.
- A load balancer or connection-routing layer (HAProxy checking
  Patroni's REST API `/primary` and `/replica` endpoints, or a virtual
  IP) that applications connect through, so failover changes which node
  serves writes without every application needing to know the topology.
- A designated, calendared maintenance window and stakeholder
  notification process before any failover test against a production
  topology — see the destructive-action warning below.

## Step-by-step guidance

### 1. Understand why automatic failover needs a consensus store, not just Patroni's own judgment

A single node (even the current primary) cannot reliably tell the
difference between "the other node is dead" and "the network between us
is partitioned but the other node is fine" — this is the core
distributed-systems problem HA design must solve. Patroni delegates the
"who is allowed to be primary right now" decision to an external
consensus store (etcd/Consul/ZooKeeper) that itself has quorum-based
leader election, so a Patroni node only acts as primary while it holds a
valid, time-bounded lease (the "leader key") in that store — not based on
its own local view of the other node's liveness. This is why the
consensus store needs its own odd-numbered quorum across independent
failure domains: a 2-node etcd cluster (or 3 nodes all in one rack)
recreates the same split-brain risk one level down.

### 2. Configure Patroni with an explicit fencing strategy, not just leader election

Leader election alone is not sufficient to prevent split-brain — it
prevents two nodes from *believing* they should be primary at the same
moment, but does not guarantee a demoted node has actually *stopped*
accepting writes (e.g. if it's hung, or its Patroni agent has crashed
while PostgreSQL itself is still running and accepting connections).
Configure a `watchdog` device so a node that loses its leader lease and
cannot confirm its own demotion self-fences (reboots) rather than
continuing to run as an unmanaged primary:
```yaml
# patroni.yml (excerpt)
watchdog:
  mode: required
  device: /dev/watchdog
  safety_margin: 5

postgresql:
  parameters:
    synchronous_commit: "on"
  use_pg_rewind: true

bootstrap:
  dcs:
    ttl: 30
    loop_wait: 10
    retry_timeout: 10
    maximum_lag_on_failover: 1048576   # bytes; skip a candidate this far behind
    synchronous_mode: false
```
`mode: required` means Patroni refuses to start PostgreSQL at all if it
cannot arm the watchdog — a stricter but safer default than `mode:
automatic`, which degrades to running without fencing if the watchdog
device is unavailable.

### 3. Decide synchronous vs. asynchronous replication for the failover-safety trade-off

`synchronous_mode: true` in Patroni (paired with
`synchronous_commit: on` and Postgres's own
`synchronous_standby_names`) guarantees a promoted replica never loses a
committed transaction, at the cost of every commit on the primary
waiting for at least one synchronous replica's ACK — a slow or
partitioned replica directly increases primary write latency, and in the
worst case (`synchronous_mode_strict`) can block all writes if no
synchronous replica is available. Asynchronous replication (Patroni's
default) never blocks primary writes but can lose the last few
transactions' worth of data on failover if the promoted replica hadn't
yet received them. Choose deliberately per workload — synchronous for
data where any loss is unacceptable (financial ledgers), asynchronous
with `maximum_lag_on_failover` guarding against promoting a badly-behind
replica for everything else.

### 4. Route application traffic through a layer that follows Patroni's leader designation, not a static hostname

```
# haproxy.cfg (excerpt) — routes writes only to the current Patroni leader
backend postgres_primary
  option httpchk GET /primary
  http-check expect status 200
  server pg1 <PG1_HOST>:5432 check port 8008
  server pg2 <PG2_HOST>:5432 check port 8008
  server pg3 <PG3_HOST>:5432 check port 8008
```
Patroni's REST API returns 200 on `/primary` only from the node currently
holding the leader lease, so HAProxy's health check naturally routes to
whichever node that is after a failover — the application never needs
its own failover logic or a hardcoded primary hostname.

### 5. Verify the cluster's actual state before and after any failover, don't assume

```bash
patronictl -c /etc/patroni.yml list
```
This shows each member's role (Leader/Replica), state, and replication
lag in one view — the authoritative source for "which node is primary
right now," not a connection string cached somewhere in application
config.

### 6. Test failover deliberately, in a maintenance window, with a rollback plan

> **Warning — destructive/high-risk action.** A failover test against a
> production topology takes the current primary offline (even briefly)
> and forces a write-path cutover; if the consensus store or fencing is
> misconfigured, it can produce split-brain or data loss instead of a
> clean test. Never run a failover test against production outside a
> calendared maintenance window with stakeholders notified, and never
> run one without first confirming the replica you expect to be promoted
> is actually caught up (`patronictl list` showing near-zero lag) and
> that a manual rollback path (documented steps to demote back, or to
> restore from backup) is ready before you start.

```bash
# Planned, controlled failover to a specific, verified-caught-up replica
patronictl -c /etc/patroni.yml switchover --master pg1 --candidate pg2
```
Prefer `switchover` (graceful, coordinated demotion of the current
leader before promoting the candidate — no data loss if replication was
caught up) for planned tests and maintenance, and reserve `failover`
(forced promotion, used when the leader is actually unreachable) for
genuine leader-down scenarios or deliberately simulating one:
```bash
# Simulating a hard failure for a realistic test — only in a maintenance window
patronictl -c /etc/patroni.yml failover --candidate pg2
```
After either, verify with `patronictl list` that exactly one node shows
`Leader`, confirm application connectivity through the HAProxy/VIP layer
picked up the new primary, and confirm the old primary rejoined as a
healthy replica (Patroni uses `pg_rewind` to resynchronize it without a
full re-clone, when `use_pg_rewind: true` and the divergence is small
enough).

## Best practices

- Run the consensus store (etcd/Consul/ZooKeeper) with an odd number of
  nodes across genuinely independent failure domains (separate racks/AZs),
  never colocated 1:1 with the PostgreSQL nodes it's making decisions
  about — if the consensus store loses quorum at the same time as a
  PostgreSQL node failure, Patroni cannot safely fail over at all (a
  correct, conservative failure mode, but one worth designing to avoid).
- Always configure a real fencing mechanism (watchdog or STONITH-style
  network fencing), not leader election alone — leader election prevents
  two nodes from deciding to be primary, fencing guarantees a demoted
  node actually stops.
- Set `maximum_lag_on_failover` deliberately rather than leaving it at a
  default that might be too permissive for your durability requirements
  — a replica promoted from far behind the old primary is a silent data
  loss event, not a clean failover.
- Test failover on a real, calendared cadence (quarterly is a common
  baseline for critical systems) rather than only at initial setup — HA
  configuration drifts (a fencing script that stops working after an OS
  upgrade, a consensus store certificate that expired) are only caught by
  actually exercising the failover path.
- Route all application traffic through a Patroni-aware layer (HAProxy
  health checks against the REST API, or a DNS/VIP mechanism Patroni
  itself manages) — never rely on applications being individually
  updated with a new primary hostname after failover.

## Common pitfalls

- **Symptom:** After a network partition, both nodes briefly show as
  primary in application logs, and writes land on both before one is
  fenced.
  **Fix:** This is the signature of missing or broken fencing — leader
  election alone (a consensus-store lease) tells a node it *should* stop
  being primary, but a node that can't reach the consensus store to
  confirm can also fail to notice its lease expired if there's no
  watchdog/fencing forcing a hard stop. Configure `watchdog: mode:
  required` (not `automatic`) so Patroni refuses to run at all without
  working fencing, and verify the watchdog device is actually present
  and armed on every node, not just configured in `patroni.yml`.

- **Symptom:** A failover promotes a replica that turns out to be
  further behind than a different available replica, causing more data
  loss than necessary.
  **Fix:** `maximum_lag_on_failover` wasn't set (or was set too high), so
  Patroni considered a badly-lagging replica eligible. Set it to a
  realistic threshold for your workload's write volume, and check
  `patronictl list` lag figures before any planned failover to pick the
  best candidate explicitly via `--candidate` rather than letting an
  unconstrained automatic choice pick.

- **Symptom:** A `switchover` or `failover` test is run against
  production with no prior notice, during business hours, and it
  produces a real customer-facing outage when the fencing script hangs.
  **Fix:** This is exactly the destructive-action risk flagged above —
  failover tests against production must run in an announced maintenance
  window with a rollback plan ready, never as an ad hoc "let's see if it
  works" during peak traffic.

- **Symptom:** The old primary, after being demoted, fails to rejoin the
  cluster as a healthy replica and instead needs a full re-clone from
  `pg_basebackup`.
  **Fix:** `use_pg_rewind: true` wasn't set, or the divergence between
  the old primary's un-replicated writes and the new primary's timeline
  was too large for `pg_rewind` to resolve (it requires a common
  ancestor point and `wal_log_hints`/checksums enabled). Enable
  `pg_rewind` support proactively (`wal_log_hints = on` or data
  checksums at `initdb` time), and budget for a full re-clone as the
  fallback for large-divergence cases rather than treating it as
  unexpected.

- **Symptom:** Application connections keep hitting the old primary
  (now a replica, read-only) for several minutes after a successful
  Patroni failover, causing write errors.
  **Fix:** Applications are connecting via a cached/static hostname
  instead of through the HAProxy/VIP layer that tracks Patroni's
  `/primary` health check. Route all write traffic through that
  layer — a failover that's correct at the database layer but invisible
  to the connection-routing layer is not actually a complete failover.

## Worked example

**Scenario:** A 3-node PostgreSQL cluster (pg1 primary, pg2/pg3
replicas) managed by Patroni with a 3-node etcd cluster, behind HAProxy.
A quarterly failover game-day is scheduled to validate the setup ahead
of a compliance audit.

1. Pre-checks in the maintenance window: confirm all three nodes are
   healthy and near-zero lag (`patronictl list` shows Leader=pg1,
   Replica=pg2/pg3, lag <100KB each), confirm etcd cluster health
   (`etcdctl endpoint health` against all 3 members), confirm watchdog
   is armed on all nodes (`patronictl list` includes watchdog status in
   newer Patroni versions, or check `/dev/watchdog` directly).
2. Run a planned switchover to the most-caught-up replica, pg2:
   ```bash
   patronictl -c /etc/patroni.yml switchover --master pg1 --candidate pg2
   ```
3. Verify: `patronictl list` shows pg2 as Leader within seconds; HAProxy
   `/primary` health check flips to pg2 and application write traffic
   (confirmed via app-level query logs) shifts accordingly with a brief
   (sub-few-second) connection blip, not an extended outage.
4. Verify pg1 rejoined cleanly as a replica via `pg_rewind` (Patroni logs
   show a rewind operation, not a full basebackup) and is catching up
   normally.
5. Simulate an actual failure for a more realistic test: hard-kill the
   PostgreSQL process on pg2 (now primary) without going through
   Patroni, and confirm etcd's lease expiry plus Patroni's health checks
   on pg3 (or pg1) trigger an automatic `failover` (not `switchover`,
   since this wasn't graceful) to the next best candidate within the
   configured `ttl`/`loop_wait` window.
6. Document actual observed failover time (e.g. "leader lease expiry +
   promotion completed in 18 seconds, HAProxy traffic shift confirmed
   within 22 seconds total") against the team's RTO target, and file any
   gaps (e.g. watchdog not armed on pg3) as follow-up work before the
   next scheduled test.

## Cross-references

- [postgresql-operations-and-performance-tuning](../postgresql-operations-and-performance-tuning/SKILL.md) — the streaming replication mechanics (WAL shipping, replication slots, lag monitoring) this HA design is built on top of.
- [postgresql-configuration-validation](../postgresql-configuration-validation/SKILL.md) — validates `synchronous_standby_names` and replication-slot settings referenced here before they're applied to a live topology.
- [database-schema-migration-with-liquibase-and-flyway](../database-schema-migration-with-liquibase-and-flyway/SKILL.md) — schema migrations need their own coordination with a Patroni-managed cluster (e.g. always targeting the current leader via the same HAProxy/VIP layer, never a specific node hostname).

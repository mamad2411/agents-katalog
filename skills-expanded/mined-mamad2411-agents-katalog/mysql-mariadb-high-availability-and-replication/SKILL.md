---
name: mysql-mariadb-high-availability-and-replication
description: >
  Covers multi-master synchronous clustering for MySQL/MariaDB: Galera
  Cluster (MariaDB Galera / Percona XtraDB Cluster), MySQL Group
  Replication and InnoDB Cluster, quorum and split-brain prevention, and
  choosing between multi-master clustering and simple primary-replica
  topologies. Use when the user asks to "set up Galera Cluster," "why
  did my Galera node go non-primary," "configure MySQL Group
  Replication/InnoDB Cluster," "prevent MySQL split-brain," or "should we
  use Galera or plain replication."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: database-operations
  maturity: stable
---

# MySQL/MariaDB High Availability and Replication

## Purpose

Standard MySQL/MariaDB replication (covered in
[mysql-mariadb-operations-and-performance-tuning](../mysql-mariadb-operations-and-performance-tuning/SKILL.md))
gives you a single writable primary and read replicas — failover
requires promoting a replica and repointing traffic, which is either a
manual process or requires external tooling. **Galera Cluster**
(available as MariaDB Galera Cluster or Percona XtraDB Cluster) and
**MySQL Group Replication** (packaged as **InnoDB Cluster** with
MySQL Router) instead provide certification-based, virtually synchronous
multi-master replication where every node can accept writes and the
cluster itself enforces quorum to prevent a split-brain where two
partitions both believe they're authoritative. This skill covers setting
up and operating both clustering technologies, and — just as
importantly — when *not* to reach for multi-master clustering because a
simpler primary-replica topology with automated failover is the better
operational trade-off.

## When to use

- Standing up a Galera Cluster (MariaDB Galera / Percona XtraDB Cluster)
  or MySQL InnoDB Cluster (Group Replication + MySQL Router) for
  multi-region or multi-AZ write availability.
- A Galera node goes into `Non-Primary` state, or the cluster reports
  it can't reach quorum, and writes across the cluster stop.
- Diagnosing Galera flow control throttling writes cluster-wide, or a
  large transaction causing certification failures.
- Deciding between Galera/Group Replication multi-master clustering and
  a simpler asynchronous/semi-sync primary-replica topology with an
  external failover manager for a specific workload.
- Planning a rolling upgrade or a planned node restart (`SST`/`IST`
  state transfer) without taking the whole cluster offline.

## Prerequisites & environment

- Galera 4 (bundled with MariaDB 10.5+/Percona XtraDB Cluster 8.0+) or
  MySQL 8.0 Group Replication assumed for the syntax below. Note that
  Galera and Group Replication are **not interchangeable or
  interoperable** — Galera is a MariaDB/Percona ecosystem technology
  (via the `wsrep` API), Group Replication is MySQL's own plugin; choose
  one based on which base engine you're already committed to, not by
  mixing them.
- An **odd number of nodes** (3 minimum, 5 for more fault tolerance) in
  any Galera or Group Replication cluster — quorum in both technologies
  requires a strict majority of configured nodes to be reachable, and an
  even node count adds a node without improving fault tolerance while
  increasing the chance of an unresolvable 50/50 partition.
- Low-latency, reliable network links between nodes — both technologies
  use certification-based replication that requires every node to agree
  on transaction ordering before commit, so cross-region deployments
  with high inter-node latency will see materially higher commit latency
  and are more prone to flow-control throttling than a same-datacenter
  deployment.
- For InnoDB Cluster specifically: MySQL Shell (`mysqlsh`) for cluster
  provisioning (`dba.createCluster()`) and MySQL Router for
  application-transparent read/write routing to the current primary.
- A load balancer or proxy layer (ProxySQL, MySQL Router, or an external
  L4 load balancer with health checks) in front of the cluster — see
  [database-connection-pooling-strategies](../database-connection-pooling-strategies/SKILL.md)
  for routing patterns, since applications should never hardcode a
  specific node as "the" primary in a multi-master topology.

## Step-by-step guidance

### 1. Understand certification-based replication before operating either technology

Both Galera and Group Replication use **certification-based replication**:
a transaction commits locally first, then is broadcast to all nodes,
which independently "certify" it (check for write-set conflicts against
concurrently-committing transactions on other nodes) before applying it.
If certification fails on a node — because a concurrent transaction on
another node modified the same rows first — the *local* transaction
commit is rolled back and returned to the client as a deadlock-style
error, even though from the client's perspective it just issued a
normal `COMMIT`:
```
ERROR 1213 (40001): Deadlock found when trying to get lock; try restarting transaction
```
Applications writing to a multi-master cluster **must** implement
retry-on-deadlock logic for this specific error class — this is not
optional error handling, it's a structural consequence of
certification-based multi-master replication, and its absence is the
single most common application-level bug when migrating onto Galera or
Group Replication from single-primary MySQL.

### 2. Bootstrap a Galera Cluster and verify quorum

```ini
# galera.cnf on every node
[galera]
wsrep_on = ON
wsrep_provider = /usr/lib/galera/libgalera_smm.so
wsrep_cluster_address = "gcomm://node1,node2,node3"
wsrep_cluster_name = "orders_cluster"
wsrep_node_address = "<THIS_NODE_IP>"
wsrep_sst_method = mariabackup
binlog_format = ROW
```
On the very first node only, bootstrap a new cluster
(`gcomm://` with no peer addresses tells that node it is the cluster's
origin):
```bash
galera_new_cluster   # or: mysqld --wsrep-new-cluster on the first node only
```
Every subsequent node joins using the full `wsrep_cluster_address`
peer list and performs a **State Snapshot Transfer (SST)** — a full data
copy from a donor node — or an **Incremental State Transfer (IST)** if
its existing state is only briefly behind (within the donor's retained
write-set cache). Verify cluster size and state:
```sql
SHOW STATUS LIKE 'wsrep_cluster_size';
SHOW STATUS LIKE 'wsrep_cluster_status';   -- must read "Primary"
SHOW STATUS LIKE 'wsrep_local_state_comment';  -- "Synced" once caught up
```
`wsrep_cluster_status = Non-Primary` means this node's partition cannot
reach quorum and it will reject all reads and writes (with
`wsrep_provider_options` in the recommended default, non-`pc.ignore_quorum`
configuration) — this is Galera's split-brain prevention working as
intended, not a bug to bypass.

### 3. Configure Group Replication and InnoDB Cluster

```sql
-- On each member, via MySQL Shell
dba.configureInstance('root@node1:3306');
```
```javascript
// Create the cluster from the first (seed) instance
var cluster = dba.createCluster('ordersCluster');
cluster.addInstance('root@node2:3306');
cluster.addInstance('root@node3:3306');
cluster.status();
```
Group Replication supports **single-primary mode** (one writable
primary, others read-only, with automatic primary election on failure —
the recommended default for most workloads) or **multi-primary mode**
(every member writable, same certification-conflict/retry requirements
as Galera above). InnoDB Cluster's MySQL Router automatically discovers
the current primary and routes writes to it in single-primary mode, so
applications connect to Router, never to a specific node's hostname
directly:
```bash
mysqlrouter --bootstrap root@node1:3306 --user=mysqlrouter
```

### 4. Monitor and tune flow control (Galera-specific)

Flow control is Galera's mechanism for throttling the whole cluster's
write throughput down to the speed of its slowest-applying node, to
prevent any node falling so far behind it can never catch up:
```sql
SHOW STATUS LIKE 'wsrep_flow_control_paused';
SHOW STATUS LIKE 'wsrep_flow_control_sent';
```
A `wsrep_flow_control_paused` value significantly above 0 means the
cluster is spending real time throttled — usually caused by one node
with slower disks/CPU, a large single transaction that takes a long
time to apply on a slower node, or an SST/IST catch-up in progress on a
recently rejoined node. Investigate the specific lagging node
(`wsrep_local_recv_queue` size per node) rather than tuning flow-control
thresholds blindly, since the throttling is a symptom, not the root
cause.

### 5. Perform a rolling restart or upgrade without cluster downtime

Restart one node at a time, confirming `wsrep_local_state_comment =
Synced` and `wsrep_cluster_size` back to the full expected count before
moving to the next node:
```sql
-- before restarting a node, ensure application traffic is drained from it at the LB/proxy layer
SHOW STATUS LIKE 'wsrep_local_state_comment';
```
Restarting more than one node concurrently in a 3-node cluster drops
the surviving quorum to a single node, which most default configurations
will correctly refuse to treat as `Primary` (since a single node is not
a majority of three) — plan restarts strictly sequentially, never in
parallel, for any cluster size.

### 6. Decide deliberately between multi-master clustering and simple replication

Multi-master clustering (Galera/Group Replication) is the right choice
when write availability across multiple nodes/AZs with no manual
failover step is a hard requirement, and the team can commit to the
retry-on-deadlock application discipline in step 1. It is *not*
automatically the safer or simpler choice: certification conflicts,
flow control throttling, and SST/IST operational complexity are real,
ongoing costs. A simple primary-replica topology (async/semi-sync, per
[mysql-mariadb-operations-and-performance-tuning](../mysql-mariadb-operations-and-performance-tuning/SKILL.md))
paired with an external failover manager (e.g. Orchestrator, or a cloud
provider's managed failover) is often the better trade-off for a
workload that doesn't genuinely need multi-region concurrent writes,
since it avoids certification-conflict application complexity entirely.

## Best practices

- Build retry-on-deadlock (specifically for error 1213/40001) into every
  application writing to a Galera or multi-primary Group Replication
  cluster as a first-class requirement, not an afterthought discovered
  after a production incident.
- Always run an odd number of nodes (3 or 5), and never bypass
  quorum-loss protection (`pc.ignore_quorum`, `pc.ignore_sb`) as a
  routine operational workaround — those settings exist for narrow,
  deliberate recovery scenarios, not as a way to keep writing during a
  partition.
- Prefer single-primary Group Replication mode for most workloads —
  multi-primary mode's certification-conflict overhead is worth paying
  only for workloads that genuinely need concurrent multi-node writes.
- Restart cluster nodes strictly one at a time, verifying full quorum
  and `Synced` state before moving to the next, for both planned
  maintenance and rolling upgrades.
- Route application traffic through a proxy/router layer (MySQL Router,
  ProxySQL) that tracks real cluster/primary state, never a hardcoded
  node hostname, so a failover or planned node restart doesn't require
  an application-side connection string change.
- Monitor `wsrep_flow_control_paused` and per-node receive-queue size as
  standing health metrics — a cluster silently throttled by one slow
  node degrades write throughput for every node, not just the slow one.

## Common pitfalls

- **Symptom:** After a network blip, all three Galera nodes report
  `Non-Primary` and reject every read and write, even though all three
  processes are still running.
  **Fix:** This is quorum-loss protection working correctly, not a bug —
  if the nodes couldn't confirm a majority partition during the blip
  (e.g. a `gcomm` reconnection race), Galera deliberately refuses to
  serve traffic from any partition that can't prove it's the majority.
  Investigate and fix the underlying network instability; do not set
  `pc.ignore_quorum = true` as a routine fix, since that reintroduces the
  exact split-brain risk quorum checking exists to prevent.

- **Symptom:** Application writes intermittently fail with `ERROR 1213:
  Deadlock found` under normal concurrent load, with no obvious lock
  contention visible in `SHOW ENGINE INNODB STATUS`.
  **Fix:** This is a certification conflict between concurrently
  committing transactions on different nodes — expected behavior in a
  multi-master cluster, not evidence of a bug. Confirm the application
  has retry-on-1213 logic; if these are frequent, consider routing
  writes for a specific hot table/key range to a single node
  (application-level or via ProxySQL query routing) to reduce
  cross-node write conflicts on that specific hotspot.

- **Symptom:** Cluster-wide write throughput drops sharply and stays low
  for an extended period after one node rejoins following a restart.
  **Fix:** The rejoining node is performing an SST (full data copy) or
  catching up via IST, and flow control is throttling the whole cluster
  to avoid it falling further behind. This is expected during rejoin —
  size SST/IST windows for low-traffic periods where possible, and
  confirm the rejoining node reaches `Synced` state before assuming a
  persistent throughput regression.

- **Symptom:** A single very large transaction (a bulk `UPDATE` or
  `DELETE` touching millions of rows) causes flow control to pause the
  entire cluster for an extended window, or fails certification outright.
  **Fix:** Galera's write-set replication has practical limits on
  transaction size (`wsrep_max_ws_size`/`wsrep_max_ws_rows`) — very
  large single transactions should be batched into smaller chunks (e.g.
  a bulk delete run in bounded-size batches with a brief pause between
  batches) rather than issued as one massive transaction, both to avoid
  hitting certification limits and to avoid monopolizing flow control.

- **Symptom:** Someone restarts two nodes of a 3-node cluster
  simultaneously for a "quick" OS patch, and the cluster becomes fully
  unavailable.
  **Fix:** Restarting a majority of nodes at once drops the surviving
  node below quorum, and a single-node partition correctly refuses to
  serve as `Primary`.
  > **Warning — availability-destructive if done in parallel.** Always
  > restart cluster nodes strictly sequentially, confirming each
  > returns to `wsrep_cluster_size` = full expected count and
  > `Synced` state before touching the next node — never patch/restart
  > more than one node at a time regardless of how routine the
  > maintenance seems.

## Worked example

**Scenario:** A payments service needs multi-AZ write availability with
automatic failover and no manual promotion step. The team evaluates
Galera Cluster (MariaDB) against a simpler async-replication-plus-
Orchestrator setup, and ultimately deploys a 3-node Galera Cluster
across three AZs.

1. Provision 3 nodes, one per AZ, with `galera.cnf` pointing at each
   other via `wsrep_cluster_address`, and bootstrap the first node:
   ```bash
   galera_new_cluster
   ```
2. Join the remaining two nodes; each performs SST from the bootstrap
   node. Verify:
   ```sql
   SHOW STATUS LIKE 'wsrep_cluster_size';   -- 3
   SHOW STATUS LIKE 'wsrep_cluster_status'; -- Primary
   ```
3. Deploy ProxySQL in front of the cluster, configured to route writes
   to whichever node currently reports healthy `wsrep_local_state = 4`
   (Synced), with automatic failover between nodes on health-check
   failure — application connection strings point only at ProxySQL.
4. Audit application code for retry-on-1213 handling; find the payment
   settlement service lacks it, add exponential-backoff retry around
   the commit path specifically for deadlock-class errors before
   go-live.
5. Load-test with concurrent writes to the same customer-account rows
   from different nodes to confirm certification conflicts are
   correctly retried and don't surface as user-facing errors.
6. Document and rehearse the sequential-restart procedure for OS
   patching, explicitly calling out that patching must proceed one node
   at a time with quorum verification between each — validated against
   a staging replica of the same 3-node topology first via
   [mysql-mariadb-configuration-validation](../mysql-mariadb-configuration-validation/SKILL.md)-style
   pre-checks before the first production patch cycle.

## Cross-references

- [mysql-mariadb-operations-and-performance-tuning](../mysql-mariadb-operations-and-performance-tuning/SKILL.md) — single-primary async/semi-sync replication and general InnoDB tuning that underpins the nodes in a Galera/Group Replication cluster.
- [mysql-mariadb-configuration-validation](../mysql-mariadb-configuration-validation/SKILL.md) — validates `wsrep_*`/Group Replication settings and topology changes before they're applied to a live cluster.
- [database-connection-pooling-strategies](../database-connection-pooling-strategies/SKILL.md) — ProxySQL/MySQL Router routing patterns for directing application traffic to the current primary or a healthy node in a multi-master cluster.
- [postgresql-high-availability-and-failover](../postgresql-high-availability-and-failover/SKILL.md) — comparable HA/failover concerns (quorum, automatic promotion) for PostgreSQL, useful as a contrast since PostgreSQL's ecosystem favors single-primary failover tooling over multi-master clustering.

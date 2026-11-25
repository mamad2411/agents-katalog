---
name: couchbase-sizing
description: "Size Couchbase clusters, plan capacity, and pick the right Capella tier. Use whenever the user asks about sizing, capacity planning, RAM quota, working set, replicas, node count, scale up vs scale out, how much memory / disk / network is needed, Capella tier selection, GSI / FTS / vector index memory, eventing memory budget, or 'will this fit.' Triggers on numerical planning questions distinct from the couchbase-mcp skill (which operates an existing cluster) and the couchbase-data-modeling skill (which designs document shape). Use proactively for: planning a new deployment, deciding whether to scale up or out, right-sizing a Capella tier, estimating storage growth, planning for burst load, sizing for vector search, calculating XDCR bandwidth, deciding replica count, planning multi-service node mix, estimating eventing memory footprint, and any question that starts with 'how much' or 'how many nodes.'"
license: MIT
---

# Couchbase sizing & capacity planning

A skill for *numerical* planning of Couchbase deployments. Companion to `couchbase-mcp` (which operates clusters) and `couchbase-data-modeling` (which designs the data shape) — this skill answers "how much" and "how many."

## When this skill applies

Use this skill whenever the conversation involves estimating resources or capacity:

- "How much RAM do I need?"
- "How many nodes for X documents?"
- "Which Capella tier should I use?"
- "Will this fit in 32 GB?"
- "Should I scale up or scale out?"
- "How big will the index be?"
- "What replica count?"
- "Sizing for vector search"
- "How much XDCR bandwidth"
- "Capacity for next year's growth"

If the conversation is about *what* to store (modeling), use `couchbase-data-modeling`. If it's about *how to* operate (calling tools), use `couchbase-mcp`. This skill is purely about resource math.

## Pick the right reference

| Question | Read |
|---|---|
| "How much RAM / what's the working set?" | `references/memory.md` |
| "How many nodes? What replica count?" | `references/nodes.md` |
| "How much disk / storage?" | `references/disk.md` |
| "Network bandwidth, XDCR throughput?" | `references/network.md` |
| "How big will the GSI / FTS / vector index be?" | `references/indexes.md` |
| "Which Capella tier?" | `references/capella.md` |
| "Read-heavy vs write-heavy vs vector vs time-series sizing?" | `references/workload-shapes.md` |

## What you need from the user before sizing anything

Sizing math depends on workload data. Without these inputs, the best you can do is order-of-magnitude estimates with explicit assumptions. **Ask the user for any of these that aren't already in context:**

1. **Document count** at present, and expected growth rate (per month or year)
2. **Average document size** (and if it varies a lot, the 95th percentile too)
3. **Reads per second** (peak, not average — sizing is for peak)
4. **Writes per second** (peak)
5. **Working set assumption**: what fraction of documents are "hot" (accessed regularly)? Common: 20%, 50%, 100%
6. **Replica count target** (usually 1 or 2)
7. **Services needed** (Data, Query, Index, FTS, Eventing, Analytics, Backup, Search)
8. **TTL / retention** (does data age out?)

If the user doesn't have these numbers, give them a way to estimate. Most users underestimate document count and document size.

## The core sizing equation

A first-cut RAM estimate for the Data service:

```
RAM_per_node = (working_set_size + metadata_overhead) × (1 + replica_count)
             ÷ node_count
             + overhead_for_other_services
             + 20% headroom
```

Where:
- `working_set_size` = `document_count × avg_doc_size × working_set_fraction`
- `metadata_overhead` ≈ `document_count × 56 bytes` (Couchbase per-doc metadata)
- `overhead_for_other_services` depends on which services are on the same node

`memory.md` walks through this with worked examples.

## Three rules of thumb

**Rule 1 — Working set is what matters, not total data size.**
Couchbase keeps the working set in RAM; cold data lives on disk and pages in on demand. For most workloads, working set is 20-50% of total data size. If you size for 100% of data to fit in RAM, you're typically over-provisioning by 2-5x.

**Rule 2 — Always plan for one node failure.**
With replica count = 1, losing one node means the cluster has to absorb that node's load on the remaining nodes. Size so the post-failure cluster still has 20%+ headroom.

**Rule 3 — Add 20% headroom on every estimate.**
Compaction, rebalance, traffic spikes, monitoring overhead. The textbook number you calculate is the cluster running comfortably; reality involves slack.

## Scale up vs scale out

Couchbase scales horizontally well, so the default answer is usually "scale out" (add more smaller nodes). But scale-up has its place:

| Scale UP (bigger nodes) | Scale OUT (more nodes) |
|---|---|
| Higher per-node throughput for read-heavy KV | Better fault tolerance |
| Simpler ops (fewer machines to manage) | Better for write-heavy workloads (more parallel writes) |
| Cheaper per-GB at higher tiers | Better headroom (lose one of N=10 vs one of N=3) |
| Limited by max node spec | Limited only by cluster-wide overhead at >100 nodes |

**Default:** start with the smallest number of nodes that meets your fault-tolerance bar (3-node minimum for replica=1, 4+ for replica=2), then scale out as load grows.

## Service mix on nodes

Couchbase nodes can run any combination of services: Data, Query, Index, FTS, Eventing, Analytics, Backup, Search. Three common deployment patterns:

**Pattern: all-services on every node.** Simplest. Each node runs everything. Good for small clusters (< 5 nodes) where dedicated service nodes would be wasteful.

**Pattern: Data nodes + Query/Index nodes.** Most common at moderate scale. Separate the data plane (KV-heavy, latency-sensitive) from the query plane (CPU-heavy, can absorb bursts). 3 data nodes + 2 query/index nodes is a common starting shape.

**Pattern: dedicated nodes per service.** Production at scale. Data nodes do nothing but data. Index nodes are RAM-heavy. Analytics nodes have their own boxes entirely (they're storage-heavy). Eventing has its own pool sized to function memory + concurrency.

`nodes.md` covers the math for picking the mix.

## Capella vs self-managed sizing differences

For Capella, sizing translates to tier selection:

- The smallest free-tier cluster is enough for development and small staging
- Production tiers come in pre-sized configurations (e.g., 4 vCPU / 16 GB RAM, 16 vCPU / 64 GB RAM, etc.)
- You pick the tier per node and the node count separately
- Storage, network, and replication are managed by Capella — you don't size them directly

`capella.md` has the current tier breakpoints and which one to pick for what workload size.

For self-managed, you control everything: CPU, RAM, disk, network. All references apply.

## Common mistakes to flag

When the user proposes a size, check for these:

- **Sizing for total data, not working set** — typically 2-5x over-provisioned
- **Forgetting replicas** — `replica=1` doubles the storage and RAM requirement for the data
- **No headroom for node failure** — if N=3 and one fails, the remaining 2 absorb 150% of normal load
- **Ignoring index memory** — GSI indexes use RAM; vector and FTS indexes are RAM-heavy. Plan for them as a separate budget
- **Mixing service types without budget** — Data, Query, and Index on the same node compete for RAM; explicit budgets are needed
- **Sizing for steady-state without considering burst** — a Black Friday e-commerce site needs 3-5x the steady-state capacity
- **Forgetting growth** — sizing for today means re-sizing in 6 months; size for 12-18 months projected
- **Ignoring rebalance overhead** — a rebalance moves data while the cluster is under normal load. Need to leave I/O and CPU slack for it

## Related skills

- `couchbase-data-modeling` — document shape decisions (embedding vs reference, array width) directly affect document size estimates, which are inputs to sizing math
- `couchbase-mcp` — operating the cluster once sized and provisioned
- `couchbase-migration-execution` — sizing the target cluster before beginning a migration

---
name: distributed-consistency
description: Choose a consistency model for a cross-node operation — strong/eventual/causal, CAP/PACELC trade-off, idempotency + dedup, and when consensus (Raft/quorum) is warranted vs simpler.
---

# distributed-consistency

> "Consistent" is not one thing. Name the model you need per operation — most need less than strong, a few need more than eventual — and pay only for that.

## When to use

- A piece of data lives on / is read from more than one node, region, or service, and correctness depends on what readers see.
- Someone proposed a consensus system (Raft/Paxos/quorum) and you need to confirm it's warranted, not cargo-culted.
- A workflow invokes `polymath-architecture:distributed-consistency`.

Not this when: the consistency boundary is inside one service's object model — that is `aggregate-design`. For the messaging mechanics that deliver updates, see `event-driven-design`.

## Inputs

- The operation, its read/write pattern, and the cost of a stale or conflicting read (money? safety? mild annoyance?).
- Latency and availability requirements; single- vs multi-region.

## Procedure

1. **Classify the operation's need**: *strong/linearizable* (a read sees the latest write — uniqueness, balances, locks), *causal* (reads respect cause→effect order — comments, sessions), or *eventual* (converges, brief staleness fine — counters, feeds). Most operations are not strong.
2. **Apply CAP under partition, PACELC otherwise**: during a partition, choose consistency *or* availability; even with no partition, there is a latency↔consistency trade. State which you pick and the business reason.
3. **For eventual consistency, define convergence**: the staleness budget, conflict resolution (last-writer-wins with caution, version vectors, or CRDTs for commutative merges), and read-your-writes if users expect it.
4. **Make writes idempotent**: idempotency keys + dedup so retried/duplicated writes (inevitable in distributed systems) don't double-apply.
5. **Justify consensus only when needed**: leader election, a replicated log, or strict linearizability across nodes warrant Raft/quorum (e.g. `R+W>N`). It costs latency and operational complexity — if a single writer or a managed transactional store suffices, prefer that and say so.
6. **Check time assumptions**: don't rely on wall-clock ordering across nodes; use logical clocks / versions where ordering matters.
7. **Name the failure semantics**: what a client sees during a partition, a failover, and a conflict.

## Output

- A one-page decision: per-operation consistency model, the CAP/PACELC choice with its business justification, idempotency/dedup mechanism, conflict-resolution strategy, and a consensus-vs-simpler recommendation.

## Quality bar

- Each operation names exactly one consistency model and why weaker won't do.
- The partition/failover behavior the client sees is stated.
- Consensus is recommended only with a concrete need; otherwise the simpler option is named.
- Writes have an idempotency story — "we'll retry" without dedup is flagged.

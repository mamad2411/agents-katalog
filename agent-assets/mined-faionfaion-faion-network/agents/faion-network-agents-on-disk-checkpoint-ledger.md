# On-Disk Checkpoint Ledger

## Summary

**One-sentence:** Produces a Checkpoint Ledger Spec that gives a bash-and-cron agent orchestrator durable resume, per-unit history and real rollback — using a state directory, marker files and `flock`, with no framework, no database and no runtime Python.

**One-paragraph:** Durable checkpointing is the one capability the orchestration frameworks genuinely added: a run that survives a crash, a history you can replay to any earlier point, and a human gate that can stay open indefinitely without holding a process. None of that requires their runtime. The mechanism is four things on disk — an identity that is verified before any write, a marker written *before* dispatch rather than after, an append-only per-unit history, and a rollback that truncates that history and requeues instead of retrying on top of a bad state. This methodology specifies those four for an orchestrator you already have. The sharp edges are all in the ordering: a marker written after dispatch turns a crash into silence, a state directory created implicitly turns a typo into a phantom unit, and a missing marker read as "not started" quietly redoes finished work. Each is a real defect that has been observed, and each is closed by one rule.

**Ефективно для:**

- A queue, pool or cron orchestrator that dispatches agents and today records only `QUEUE / ACTIVE / DONE` — status, no history.
- Long multi-phase runs where a crash currently means "restart the unit" because nobody can tell how far it got.
- Anyone being told they need a durable-execution framework to get resume and time-travel replay.
- Runs with human approval gates that must survive hours or days without a process waiting on them.

## Applies If (ALL must hold)

- An orchestrator dispatches units of work to agents or subprocesses and can crash, be killed, or be rate-limited mid-run.
- A unit of work has more than one phase, and redoing a completed phase costs real money or real time.
- The orchestrator and its workers share one filesystem, or one they can both lock.

## Skip If (ANY kills it)

- Every unit is a single idempotent step — re-running it costs nothing, so a checkpoint buys nothing.
- Workers are distributed across hosts with no shared filesystem and no lock service; this specifies file-based state and `flock`, and neither survives that.
- A durable-execution engine already owns run state end to end. Two checkpoint authorities is worse than one, whichever one it is.

## Content

| File | What's inside |
|------|---------------|
| `content/01-core-rules.xml` | Six testable rules. R1 and R2 are the ordering rules that cause the observed defects; R5 separates rollback from retry. |
| `content/02-output-contract.xml` | The Checkpoint Ledger Spec: the state-directory layout, the four record fields, write boundaries, and the consistency rules the validator enforces. |
| `content/03-failure-modes.xml` | Six failure modes, four of them observed in production runs, each with the rule that prevents it. |
| `content/06-decision-tree.xml` | Routing from an observed state on disk to resume / dead-letter / roll back / do nothing. |
| `scripts/validate-on-disk-checkpoint-ledger.py` | Validates a spec: lineage ordering, marker vocabulary, boundaries, dead-letter policy. `--self-test` included. |

## Templates

| File | Purpose |
|------|---------|
| `templates/checkpoint-ledger-spec.yaml` | Fill-in spec; ships valid against the contract. |
| `templates/mark.sh` | The single creation path. Identity-checked, `flock`-guarded, appends to history. Exits non-zero on an unknown unit. |
| `templates/rollback.sh` | Truncate-and-requeue: removes markers at or after a phase in lineage order, records `rolled-back`, requeues. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- `agent-rollback-button-design` — reverts an agent *release*. This reverts one *run* to one *phase*; the two operate on different objects and both can be needed.
- `agent-replay-harness-cookbook` — replays a captured failure deterministically for debugging. The ledger resumes a live run; the harness reproduces a dead one.
- `subagent-as-context-firewall` — what a dispatched unit is allowed to see. The ledger records that a dispatch happened; that methodology bounds what it costs.
- `idempotent-write-tools` — the property that makes a resumed phase safe to re-run. Where it cannot be achieved, R4's non-idempotent boundary is the fallback.
- `context-graph-engineering` — unrelated object, adjacent vocabulary: that is the knowledge graph, this is run state.

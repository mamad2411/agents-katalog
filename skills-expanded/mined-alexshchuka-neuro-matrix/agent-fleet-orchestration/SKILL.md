---
name: agent-fleet-orchestration
description: Run a lead + subagent fleet to build a non-trivial system without collisions, drift, or false completion. Use when a task is large enough to parallelize across agents — decomposing it, freezing contracts, driving execution, and closing each stage with real evidence, not agent reports.
---

# Agent-fleet-orchestration: leading a fleet without drift or false completion

BLUF: the dominant failure modes are contract drift (agents fill unknowns differently, integration breaks), false completion (agent says done, code disagrees), and collisions (two agents touch the same file). This skill eliminates all three structurally.

## Stage 0 — decompose into disjoint-scope nodes

- Map the deliverable into nodes where each node owns a non-overlapping set of files or directories. Ownership is a hard partition: no file belongs to two nodes.
- Nodes that share data across a boundary are linked by a contract (interface, schema, wire format), not shared ownership.
- A node that is too large to hold in one agent's context is split further, not given to a stronger model. Size beats capability.

Rule of thumb: if you cannot state a node's output contract in one sentence, split it.

## Stage 1 — freeze contracts before any implementation

This is the single most leverage-yielding step. Agents filling nodes against a frozen edge cannot drift relative to each other — the contract is a mechanical stop.

- Author every cross-node interface, function signature, data schema, and wire format as committed files or explicit typed stubs before any implementation agent runs.
- Ambiguous contracts get a `QUESTION` block (same discipline as [paper-to-code](../paper-to-code/SKILL.md) Stage 1) — do not resolve ambiguity by picking a default and hoping.
- Once frozen, treat the contracts as immutable during the implementation phase; if a contract must change, stop all dependent nodes, revise, and re-fan.

Mirabilis example: the engine (ports & adapters), the Bubble Tea v2 TUI, and the auth-proxy chain each owned a disjoint directory; the port interfaces and the proxy wire protocol were committed as typed Go stubs before any agent wrote implementation code. A contract change mid-flight would have invalidated work in progress — it did not happen.

## Stage 2 — parallelize independent nodes, sequence dependent ones

- Nodes with no shared edges run in parallel — fan out.
- Nodes that consume another node's contract output run after that contract is green — sequence only what must sequence.
- Before fanning out, emit per-agent instructions that include: the node's owned paths, the frozen contracts it must satisfy, the adjacent contracts it must not touch, and the verification command that will close the node.

## Stage 3 — verify every claim with real tool output; code is truth

Never close a node on an agent's self-report. The agent says «done» — that is a hypothesis. Evidence that closes it:

| Claim | Acceptable evidence |
|---|---|
| «It builds» | paste of `go build ./...` (or stack equivalent) with exit 0 |
| «Tests pass» | paste of `go test ./...` with counts and exit 0 |
| «Lint clean» | paste of linter run with exit 0 |
| «Contract satisfied» | compile-time evidence (type-checks) or a targeted test of the boundary |

Not green = not done. Re-open the node with the tool output as context, not a restatement of the requirement.

Spot-check invariants in the code directly: read the file, grep the function, verify the type signature. Agent reports compress away exactly the details that hide bugs.

## Stage 4 — pick model tiers deliberately

- Implementation against a frozen contract is a scoped mechanical task: cheaper/faster models are appropriate. The contract removes the judgment call.
- Adversarial review of the integrated whole requires the strongest available model and an independent role (see [adversarial-review](../adversarial-review/SKILL.md)).
- The lead itself — decomposition, contract authoring, inter-node orchestration — is not a scoped mechanical task; do not downgrade it.

## Stage 5 — stall recovery

A stalled agent (loops, halts, produces output that does not satisfy the contract) is a signal, not a failure:
- Verify with tool output what actually happened vs what was expected.
- If the node is too large: split it and re-fan with smaller scopes.
- If the contract was under-specified: revise the contract, re-freeze, re-run.
- If the model is genuinely inadequate for the scope: upgrade only that node.

Do not patch a stalled agent's output without understanding why it stalled — that is gap-filling, the failure mode this skill exists to prevent.

## Stage 6 — fold corrections into downstream instructions

When a node produces output that the lead corrects, the correction must propagate: restate the corrected interface/behavior in every downstream agent's instruction set. Do not rely on downstream agents to infer corrections from implicit context.

## Output contract

1. Node map (owner → paths, contract). 2. Frozen contracts (committed artifacts). 3. Fan-out instructions (per agent, per node). 4. Verification evidence per closed node (tool output). 5. Stall log if any (what failed, what changed, re-run result). BLUF at every stage.

Counter: for a task a single agent can hold completely — no cross-node contracts, no parallelism, one owned scope — this overhead is waste; run the agent directly.

---
Provenance: distilled from the 2026-06-12 mirabilis rewrite session — a greenfield Go TUI + auth-proxy system built by a lead orchestrating a fleet across disjoint phases, with frozen port/adapter contracts preceding implementation and every completion gate closed by real build/test output, not agent reports.

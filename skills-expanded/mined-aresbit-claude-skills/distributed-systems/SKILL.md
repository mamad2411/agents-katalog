---
name: distributed-systems
description: >-
  AI-assisted distributed systems verification with TLA+ formal specification.
  Use when verifying distributed system correctness, discovering race conditions,
  writing TLA+ specifications from codebases, performing model checking on
  consensus/replication protocols, or setting up Lamport Agent workflows.
  Triggers on: "verify distributed system", "formal verification", "TLA+ spec",
  "model checking", "find race condition", "prove correctness", "CRAQ",
  "Paxos verification", "Raft verification", "chain replication verification",
  "distributed consensus verification".
---

# Distributed Systems — AI-Assisted Formal Verification

Production methodology for TLA+ verification of distributed systems, driven by AI agents. Battle-tested on Azure Storage (found subtle Paxos race condition) and DeepSeek 3FS (verified CRAQ consistency). Based on the [Lamport Agent](https://github.com/zfhuang99/lamport-agent) framework.

## Workflow Decision Tree

```
New verification task
├─ New codebase → Full 6-Phase Lamport Workflow (§1)
├─ Design doc only → Start at Phase 3 (properties), then 4→5
├─ Found a bug, confirm fix → Phase 4→5 only (encode fix, re-check)
└─ Just understand code → Phase 1→2 only (happy path + errors)
```

## 1. Full 6-Phase Lamport Workflow

All artifacts go in `./spec/<feature>/`. Each phase has a **user checkpoint** before proceeding.

### Phase 0 — plan.json

Create a structured plan with all phases, subtasks, and status tracking.

> Template and full phase details: [references/lamport-agent-workflow.md](references/lamport-agent-workflow.md)

### Phase 1 — Happy Path & Architecture

AI studies the codebase and produces:
- **`happy_path.md`** — Entities → Workflows → Success Conditions
- **`architecture.md`** — Components → Data Structures → Interfaces → Configuration

**How:** Give AI the feature name + component directory. It autonomously identifies relevant files, extracts essential information, and documents findings.

### Phase 2 — Error Handling & Concurrency

AI analyzes failures and concurrent interactions:
- **`behavior.md`** — State transitions, error handling strategies, concurrency control, known invariants
- **`diagrams.md`** — Sequence diagrams, error flows, state machines

### Phase 3 — Verification Properties

Define safety/liveness properties in natural language and semi-formal TLA+ notation. Prioritize: critical safety → data consistency → protocol correctness → liveness.

> Property patterns from CRAQ: [references/tla-spec-patterns.md](references/tla-spec-patterns.md)

### Phase 4 — Create TLA+ Model

AI encodes the system in TLA+:
- **`<feature>.tla`** — State variables, Init/Next predicates, fault injection, invariants
- **`<feature>.cfg`** — Model checking bounds, constants, property selection

**Key pattern:** AI refines the spec iteratively, updating one atomic action at a time. This incremental approach maintains precision.

### Phase 5 — Model Check & Debug

Run the pipeline: `tlaplus_parse` → `tlaplus_smoke` → `tlaplus_check`

| Result | Action |
|--------|--------|
| Syntax error | AI fixes the spec |
| Invariant violation | AI analyzes counterexample trace, explains the *design/implementation* bug. Do NOT modify the spec to make violations pass. |
| All pass | Document in `verification_summary.md` |

> Script to run the pipeline: `scripts/verify_tla.py`

## 2. Prompt Patterns

### Starting Verification
```
Let's formally verify the <feature> implementation and whether it provides
consistency between reads and writes, including during <failure scenarios>.
```

### Discovering Missing Safety Mechanisms
```
Investigate how <mechanism> (e.g., etags, locks) are used to prevent race
conditions in this code. Update the spec and documentation accordingly.
```

### Git History Deep-Dive
```
Analyze the git commit history for this feature using git MCP. Look for any
safety mechanisms, invariants, or edge-case fixes we might have missed.
```
Real impact: Git analysis on Azure Storage revealed a previously-overlooked pessimistic locking mechanism that was critical to safety.

### Counterexample Analysis
```
Here is the TLC counterexample trace. Identify the problematic sequence,
explain what invariant is violated, and why it happens at the design level.
```

## 3. Key Principles

- **AI writes specs; humans review.** AI-generated TLA+ specs rival human work after iterative refinement.
- **One atomic action at a time.** Incremental refinement keeps AI precise.
- **Only fix syntax errors in the spec.** Invariant violations mean bugs in the *system*, not the spec.
- **Git history is safety documentation.** Commits and PRs encode design rationale AI can extract.
- **AI self-corrects.** AI identifies and fixes its own syntax and logic errors (GPT 5.1 even argues back like a human team member).
- **Sequential Thinking MCP.** Use for complex reasoning chains in Phases 1-3.

## 4. Quick Reference

| Phase | Key Output | Checkpoint |
|-------|-----------|------------|
| 0 | `plan.json` | — |
| 1 | `happy_path.md`, `architecture.md` | User validates understanding |
| 2 | `behavior.md`, `diagrams.md` | User reviews analysis |
| 3 | `properties.md` (7-10 properties) | User approves properties |
| 4 | `<feature>.tla`, `<feature>.cfg` | — |
| 5 | `verification_summary.md` | — |

## Resources

### references/
- [lamport-agent-workflow.md](references/lamport-agent-workflow.md) — Complete 6-phase plan template with checkpoint details
- [tla-spec-patterns.md](references/tla-spec-patterns.md) — CRAQ property patterns, modeling patterns, common pitfalls
- [ai-verification-methodology.md](references/ai-verification-methodology.md) — 8-step methodology from Azure Storage case study
- [agent-setup.md](references/agent-setup.md) — VS Code + TLA+ MCP + Sequential Thinking MCP installation
- [lamport-agent-prompt.md](references/lamport-agent-prompt.md) — Full Lamport agent system prompt (reference for custom agent creation)

### scripts/
- `verify_tla.py` — Run parse → smoke → check pipeline and collect results

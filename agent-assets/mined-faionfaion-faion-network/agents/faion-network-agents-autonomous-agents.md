# Autonomous Agents

## Summary

**One-sentence:** Operating guide for autonomous LLM agents (ReAct, Plan-and-Execute, Reflexion) — iteration caps, idempotent tools, terminal conditions, named subagent roles, sandbox isolation, human checkpoints.

**One-paragraph:** Autonomous agents combine reasoning, memory, and tool use to pursue goals with minimal supervision. This methodology produces one operating spec per agent feature that pins the pattern (ReAct / Plan-and-Execute / Reflexion), the named subagent roles (planner / executor / verifier / critic) with their model choices, the iteration caps + terminal conditions, the idempotency contract for tools, sandbox isolation requirements, and the human-checkpoint policy for irreversible actions.

**Ефективно для:** Команд, які хочуть «зробити autonomous-агента» без хаосу infinite loops, lost messages і destructive tool calls; спека за пів дня дає чітку архітектуру, яку код може реалізувати лінійно.

## Applies If (ALL must hold)

- Agent will run autonomously (no human-in-loop for every step).
- Task involves ≥3 LLM round-trips or ≥3 tool calls.
- Sandbox isolation is available (e2b, docker, or equivalent) for any code execution.
- Idempotency can be enforced at tool layer (dedup keys, transactional writes).
- Named engineering owner for the spec.

## Skip If (ANY kills it)

- Single-call task — no autonomous loop needed.
- Pure read-only research with no writes — overkill.
- No sandbox available for code execution — fix that first.
- Team has no track record with agents — start with simpler sibling patterns.

## Prerequisites

| Artifact | Format | Source |
|---|---|---|
| Goal description | natural language ≤1000 chars | Operator |
| Tool inventory | name + schema + idempotency-class | Tool catalogue |
| Success criterion | test command / schema / human checkpoint | Owner |
| Sandbox URL or local docker | endpoint | Ops |
| Iteration budget | int (default 15) | Tech lead |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `geek/ai/ai-agents/agent-patterns/AGENTS.md` | Pattern picking. |
| `geek/ai/ai-agents/agent-shape-decision-frame/AGENTS.md` | Shape decision precedes this spec. |
| `geek/ai/ai-agents/idempotent-write-tools/AGENTS.md` | Idempotency anchor. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 4 rules: iteration caps + logs, named subagent roles, Reflexion critic, idempotent tools | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema for the agent spec | ~700 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns | ~900 |
| `content/04-procedure.xml` | deep | 6-step procedure: shape → pattern → roles → tools → guards → ship | ~1100 |
| `content/05-examples.xml` | medium | Worked example: autonomous code-fixer | ~1000 |
| `content/06-decision-tree.xml` | essential | Tree: irreversible? → sandboxed? → success-signal? → ship/escalate | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `classify_task` | haiku | Mechanical. |
| `design_subagent_roles` | sonnet | Per-instance judgment. |
| `compose_spec` | sonnet | Final composition. |
| `irreversible_review` | opus | High-stakes review. |

## Templates

| File | Purpose |
|------|---------|
| `templates/output-schema.json` | JSON Schema for the agent spec. |
| `templates/output.example.json` | Filled example. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-output.py` | Validate the agent spec. | Before implementation kickoff. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- parent skill: `geek/ai/ai-agents/`
- peer: [[agent-patterns]], [[agent-shape-decision-frame]], [[idempotent-write-tools]].

## Decision tree

See `content/06-decision-tree.xml`. Asks: (1) does the agent take irreversible actions? (2) is execution sandboxed where required? (3) is there a deterministic success signal? Leaves point to "ship autonomous", "ship with human gate", or "escalate".

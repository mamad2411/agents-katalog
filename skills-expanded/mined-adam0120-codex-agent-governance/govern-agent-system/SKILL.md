---
name: govern-agent-system
description: Manually govern native Codex custom-agent delegation with coordinator-first, cost-aware role selection. Use only when the user explicitly invokes `$govern-agent-system` or asks to use this Skill.
---

# Govern Agent System

Use this Skill only when the user explicitly invokes it. Invocation changes orchestration, not authority: every delegated operation must already be allowed by the task. If native delegation or reuse is unavailable, continue directly; missing optional tooling is not a blocker.

## Ownership and scheduling

The main agent owns scope, contracts, sequencing, architecture and product decisions, risk acceptance, integration, user decisions, and final acceptance. Delegate bounded implementation, search-heavy, repetitive, long-running, or independently verifiable work to the smallest suitable role. Work directly when the slice is trivial, tightly coupled, smaller than its handoff, or delegation is unavailable.

Treat one coherent behavior as one ownership unit. Do not split ordinary location, implementation, focused verification, fixes, and documentation into separate agents. Reuse one child through a linear stage. When multiple independent nodes are ready, start the smallest useful parallel batch; writers must own non-overlapping files or worktrees, and dependent or conflicting work stays serial. Keep one active writer per owned surface.

While children run, continue non-conflicting coordination and integration work. Wait only at a real dependency boundary.

## Role selection

| Role | Select for |
|---|---|
| `default` | Small bounded read-only advice with no specialist fit |
| `worker` | One settled implementation behavior and focused verification |
| `explorer` | One bounded discovery question or reproduction loop |
| `code_locator` | Exact revision-aware locations for factual questions |
| `cross_module_architect` | One frozen cross-module contract question and candidate options |
| `systems_safety` | One parent-approved safety invariant or narrow patch |
| `semantic_reviewer` | One frozen accumulated diff or narrow high-risk review |
| `release_operator` | One approved revision-bound release runbook and mutation batch |

Do not delegate unresolved product, architecture, authority, ownership, or risk decisions. The main agent resolves those first.

## Dispatch contract

Delegate only one observable state transition or one evidence question. Before dispatch, freeze:

1. Objective, repository/worktree, and exact baseline revision or immutable state.
2. Exact files, symbols, or narrow search area, with exclusions.
3. Allowed operation and the behavior, invariant, authority, and data-safety boundary.
4. Acceptance checks and evidence required by the parent.

Send only those facts in a compact, self-contained assignment. Do not send a project narrative, task transcript, or unrelated parent context.

## Native binding

Inspect the actual spawn schema before the first dispatch.

- If `agent_type` is available, pass the selected role through it. Omit direct model and reasoning overrides so the registered TOML supplies them.
- If `agent_type` is absent, enter **profile compatibility mode**: read the selected role's installed TOML, pass its exact `model` and `model_reasoning_effort`, and include a compact version of that role's operation, exclusions, and output contract in the assignment. This does not load the TOML developer prompt or sandbox; do not describe the child as role-bound or sandboxed.
- Start every role with `fork_turns="none"`; the assignment is its complete context. Use a positive history window only when an essential, immediately preceding decision cannot be restated safely. Never omit `fork_turns` or use `all`.
- Direct model or reasoning overrides are otherwise allowed only for the bounded escalation below.

A task name never binds a role. If spawn reports `unknown agent_type`, do not retry that role in the current task; continue directly or use an already registered suitable role. Newly installed roles require a fresh top-level task after Codex reloads its registry.

## Reuse

Reuse a child by id while its repository/worktree, operation class, owned surface, and frozen contract remain stable. The child's accepted edits do not invalidate reuse. Reuse the same writer for review fixes, affected verification, and related documentation. Create a new child only for a different owner, operation class, contract, independent review boundary, or materially changed surface.

Treat each `code_locator` as a reusable session keyed by repository/worktree roots, exact revisions, search boundary and exclusions, and evidence format. Start it without parent history. Before a follow-up, recheck the keyed revisions and boundary; if unchanged, send only `reuse baseline <revision>; boundary unchanged` plus the new factual items. Do not resend the assignment, source excerpts, or prior evidence. Related factual item lists may change within the same key. Retire the session when its key changes, the request becomes semantic, or the child is unavailable. Prefer one sequential locator per key; parallelize locators only when latency materially justifies the extra context.

## Results and escalation

Non-locator children return a compact **COMPLETE**, **PARTIAL**, or **STOP** envelope with scope, resulting state, verification, blockers, and next parent action. `code_locator` uses the factual Item and Lookup statuses defined in its TOML.

A refusal, failed safety gate, missing authority, or unresolved ownership remains `STOP`; never widen scope, switch roles, or elevate authority to bypass it. For two consecutive scope or ambiguity failures on the same task, shrink the node and clarify its invariant or acceptance signal. Only if a re-bounded node still fails because of reasoning quality—not tools, environment, authority, or scope—may the parent create one new node at the next supported model or reasoning level. Do not increase both capability and scope. Reserve the highest-cost reviewer for frozen high-risk diffs.

## Verification and review

The current owner runs focused verification and ordinary fixes for its coherent stage. Use a separate verifier only for an independently long-running check or required independent evidence.

Use `semantic_reviewer` once for an explicit review, a frozen high-risk accumulated diff, or a meaningful release boundary. Ordinary changes need owner verification and a final diff check. Reuse the writer for review fixes and rerun affected checks; repeat full review only when the fix changes a security, persistence, concurrency, migration, deployment, irreversible, or public-contract boundary.

Do not ask a child to load a Skill or discover external tools unless its assignment requires them. Bundled roles disable persistent memories, web search, Apps, and inherited MCP servers. Only `code_locator`, `explorer`, `cross_module_architect`, `systems_safety`, and `semantic_reviewer` explicitly enable CodeGraph for indexed call paths; add a dedicated role configuration for any other external tool. The role TOMLs define child behavior and session defaults; this Skill defines parent orchestration.

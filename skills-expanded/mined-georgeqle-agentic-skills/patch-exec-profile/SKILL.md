---
name: patch-exec-profile
description: Audit and fill missing lane metadata (Mode, Depends on, Owns, Branch) in agent-team and implementation-safe execution profiles in tasks/todo.md
type: execution
version: v0.0
invocation: sub-skill
parent: exec
---

# Patch Exec Profile

Audit and fill missing lane metadata in the `### Execution Profile` blocks of `tasks/todo.md`. Invoked just-in-time — typically auto-invoked by `/exec` when an `agent-team` phase has incomplete lane specs. Without complete `Mode`, `Depends on`, and (for write lanes) `Owns` / `Must not edit` / `Branch` values, `/exec` cannot build the lane DAG, push branch-backed lane work, open PRs, or enforce write-boundary integration.

## Prerequisites

- `tasks/todo.md` must exist and contain at least one `### Execution Profile` block.

## Process

1. **Read `tasks/todo.md`.** Find every phase with `Parallel mode: agent-team` or `Parallel mode: implementation-safe`.
2. **For each lane in each such profile**, check presence and concreteness of:
   - `Mode:` — one of `read-only | write | review`.
   - `Depends on:` — comma-separated lane names within the same phase, or `none`.
   - `Owns:` — required when `Mode: write`.
   - `Must not edit:` — required when `Mode: write`.
   - `Branch:` — required for `agent-team` write lanes and must not be `main` or `master`.
   - Placeholder values (e.g., `read-only | write | review`, `[lane, step, or none]`, `path/or/glob`) count as missing.
3. **Apply inference rules for obvious cases:**
   - Lane name contains `review` (e.g., `correctness-review`, `security-reviewer`) → `Mode: review`, `Depends on: <all write lanes in the phase>`.
   - Lane name contains `research`, `explorer`, `docs-research`, or ends in `-research-only` → `Mode: read-only`, `Depends on: none`.
   - Otherwise → `Mode: write`. `Depends on:` defaults to `none` unless step text references an explicit ordering (e.g., "after lane X completes").
4. **For ambiguous cases** (write lanes with no clear dependency signal but plausible orderings, multiple review lanes with unclear scope), enter plan mode and ask the user via `AskUserQuestion` before writing. Do not guess.
5. **Validate after inference:**
   - All write lanes in a phase have disjoint `Owns` paths (no path prefix overlap). If overlap is detected, surface it and stop — this is a profile design error, not a fill-in.
   - Every `Depends on:` reference names an existing lane in the same phase.
   - The lane DAG has no cycles.
   - Every `agent-team` write lane has a unique non-primary `Branch:` value.
   - The phase includes a consolidation/PR review step after write lanes and before final validation or shipping. If it is missing, surface it and stop; do not invent new implementation steps.
6. **Write the patched profile back to `tasks/todo.md`.** Do not commit. Do not push. `/ship` owns shipping.

## Constraints

- Do not modify anything outside `### Execution Profile` blocks.
- Do not change `Parallel mode` itself — that is a `/plan-phase` decision.
- Do not invent new lanes or new implementation steps. Only fill missing metadata on lanes that already exist.
- Do not fill `Owns` or `Must not edit` by inference — those are load-bearing write-boundary declarations. If a write lane is missing either field, stop and ask the user via `AskUserQuestion`.
- Do not fill `Branch` by inference when the phase naming or lane identity is ambiguous. If obvious, use `agent-team/phase-N-<lane-name>` and ensure it is unique.
- Do not touch `tasks/roadmap.md`, `tasks/history.md`, `tasks/manual-todo.md`, or any non-task file.

## Output

Report concisely:
- Phase(s) audited
- Lanes patched (lane name → fields filled with inferred values)
- Lanes flagged for user input (with the ambiguity)
- Validation errors surfaced (overlapping `Owns`, unresolved `Depends on`, cycles)

## Next-Step Routing

- **Next work:** resume the original executor (typically `/exec`) against the patched profile.
- **Recommended next command:** `/exec` (or whatever invoked this skill).

## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.


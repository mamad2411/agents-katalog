---
name: hades
description: |
  Canonical HADES system project skill: doctrine reminders (max-scope, no
  defer, no tech debt, no AI-attribution in commits), workflow patterns
  (brainstorm → spec → write-plan → execute-plan → release), hard rules,
  and pointers to project memory.
keywords:
  - hades
  - hades-system
  - autonomous-development
  - workforce-orchestration
  - max-scope
  - doctrine-driven
  - knowledge-graph
  - audit-chain
version: 0.12.0
license: Apache-2.0
agentskills_version: 1.0
metadata:
  conditional_activation:
    # repo path stays per design contract(project filesystem path);
    # operators may relocate the repo. The hint uses a generic placeholder
    # to avoid leaking operator identity into the release tree;
    # individual operators override via ~/.hermes config if needed.
    - cwd_starts_with: /path/to/projects/hades-system
    - cwd_contains: hades-system
---

# HADES — Canonical project skill

This skill is registered by the HADES Hermes plugin and is resolvable as
`hades:hades` (per Hermes plugin skill namespacing — see
`hermes_cli/plugins.py:551-595`). Load it via `/skill hades:hades`
in a Hermes session, or rely on conditional activation when working in a
HADES project directory.

## Project identity

HADES (formerly hades-system) is a multi-project agentic development
orchestrator. Go-based daemon + CLI + Hermes plugin (this package).
Privacy-by-default, max-scope doctrine, single-egress-point for LLM
traffic. Released as repository at `github.com/cbip-solutions/hades-system`
(repo URL preserved per design contract).

## Doctrine (load-bearing)

Operator directive (verbatim): _max scope always; build the final product,
not the stages; nunca limitarse por budget o tiempo; no defer; no
technical debt; no stubs, código completo._

These are the lens through which every implementation, review, and
trade-off decision is made — they OVERRIDE speed, convenience, or
methodology shortcuts. Reviewer "Minor" is severity tag, NOT permission
to defer.

- **Max-scope always** — final-shape architecture day 1; never incremental MVP
- **Build the final product, not the stages** — refactor toward shape from start
- **No stubs, código completo** — production code complete day 1
- **Never limit by budget or time** — scope decisions are doctrine-driven
- **No defer** — fix coverage gaps and untested behaviour before next task
- **No technical debt** — every gap surfaced today compounds tomorrow
- **Hard parts are where value lives** — when stage looks hard, that's the
  signal the work is load-bearing
- **Tests are the floor, not the ceiling** — coverage targets ≥85% / ≥90% are
  minimums; goal is 100% on documented behaviour + edge + adversarial paths

## Workflow patterns

Pipeline per plan: **brainstorm → design sections → spec → write-plan →
self-review (stage reality-check + stage grep + stage code-reviewer)
→ execute-plan → release**.

Canonical methodology: `docs/METHODOLOGY.md` in the repo. Quick reference
in user-level memory at `local agent memory`.

## Hard rules

1. **NO AI-attribution markers in commits** (invariant). Never
   `Co-Authored-By: prohibited assistant`, `Generated with prohibited assistant`, or any
   AI-attribution marker. Violations gated automatically by the plugin's
   `pre_tool_call` hook callback — returns `{"action": "block",
   "message": "..."}` to Hermes; Hermes blocks the tool call. Defense-
   in-depth: `bin/hades-event-poster` Go binary has the same regex.
2. **Conventional commits**: `type(scope): subject` (imperative, lowercase,
   no trailing period). Types: feat / fix / docs / test / refactor / chore /
   style / perf / build / ci.
3. **TDD always**: failing test first, never impl before test.
4. **All gates before commit**: `make build && make lint && make test &&
   make verify-invariants && go test -race ./... -count=2 &&
   GOOS=linux go build ./...`
5. **Coverage ≥85%** (≥90% security/correctness-critical files: network,
   validator, audit, redact, dispatcher, circuit_breaker, payg_safety,
   cost_ledger, pre_tool_call commit-gate path).
6. **Tag safety gate**: NEVER push tags without operator approval.

## Recovery flow

For session start (post `/clear` or new Hermes session): read `.hades/session.md`
at repo root. The `on_session_start` hook callback (in
`plugin/hades/hooks/session_handlers.py`) auto-loads its TL;DR
section. For canonical Hermes context injection, HADES design wires
`pre_llm_call` augmentation.

Operator may also invoke `/hades:start` (skill + slash command) for
explicit session resume synthesis.

For session end: invoke `/hades:handoff` (snapshots state to
.hades/session.md + commits + optionally pushes).

## Substrate

Hermes Agent (peer dependency, MIT, `brew install hermes-agent`). Per
ADR-0080 (substrate pivot from legacy plugin format to Hermes Agent, 2026-05-10).

HADES is the specialized SE backend (HRA + workforce + cost +
doctrine + audit + apply + merge); Hermes is the UX substrate (chat REPL +
multi-platform gateway + skills + memory + Curator + voice + Ink TUI).

## See also

- `local agent memory` —
  per-project memory index
- `architecture records` — substrate ADR
- `design records` —
  HADES design design (augmentation pipeline + Hermes UX; HADES design replaced gitnexus with caronte)
- `design records` —
  empirical Hermes v0.13.0 plugin contract
- `docs/METHODOLOGY.md` — canonical methodology (4 nested levels +
  3 transversals)

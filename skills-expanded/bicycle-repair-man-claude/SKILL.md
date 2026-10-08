# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project: Bicycle Repair Man (BRM)

A **workflow definition repository**. The goal is to combine:

- **Superpowers** (`claude-plugins-official`, v5.1.0) — the skills-driven methodology (brainstorming → writing-plans → subagent-driven-development → TDD → verification).
- **Pennyfarthing's action-oriented orchestration plumbing** — workflows, gates, handoffs, sidecars, prime context, tandem, output styles.

What is explicitly **out of scope** for BRM (decoupled, left to Pennyfarthing):

- The 1898/sprint workflow machinery — sprint YAML, story tracking, `current-sprint.yaml`, sprint archives.
- Scrum Master / story-selection flows (`sm-setup`, `sm-finish`, `/pf-sm`, `/pf-sprint`).
- Jira integration and bidirectional sync.
- Persona/theme research, OCEAN benchmarking, JobFair, Peloton — these are PF research concerns.

BRM keeps the *engine*, not the *fleet management*.

## Current state

v0.1.0 implementation in progress per `docs/superpowers/plans/2026-05-12-brm-v0.1.0-implementation.md`. The design spec at `docs/superpowers/specs/2026-05-12-brm-design.md` is the contract. Tests run via `python3 -m pytest -v` from the repo root; no other build pipeline.

## Source repos to reference

When designing or porting behavior, read the originals — do not re-derive from memory:

| Source | Path on this machine | What to look at |
|--------|----------------------|-----------------|
| Pennyfarthing (framework source) | `/Users/slabgorb/Projects/orc-penny/pennyfarthing/` | `pennyfarthing-dist/{workflows,gates,patterns,schemas,guides,protocols}` |
| Pennyfarthing orchestrator | `/Users/slabgorb/Projects/orc-penny/` | How sprint/session layer wraps the framework — useful as a *negative* reference (what BRM omits) |
| Superpowers plugin (installed) | `/Users/slabgorb/.claude/plugins/cache/claude-plugins-official/superpowers/5.1.0/` | `skills/`, `hooks/`, `AGENTS.md`, `README.md` |

Pennyfarthing's own `CLAUDE.md` (in `orc-penny/pennyfarthing/CLAUDE.md`) marks Superpowers as a *required companion plugin* — BRM is the natural place to formalize that relationship.

## In-scope concepts from Pennyfarthing

When porting/adapting, these are the parts BRM wants. All paths below are inside `orc-penny/pennyfarthing/pennyfarthing-dist/`:

| Concept | Location | Notes |
|---------|----------|-------|
| BikeLane workflow engine | `workflows/*.yaml` | Two flavors: **phased** (agent-driven handoffs, e.g. `tdd.yaml`, `bdd.yaml`, `sdd.yaml`, `trivial.yaml`, `patch.yaml`) and **stepped** (user-gated progression, e.g. `architecture.yaml`, `release.yaml`, `git-cleanup.yaml`). The `sdd.yaml` (Superpower Driven Development) workflow is the existing bridge between the two systems — start there. |
| Gates | `gates/` + `schemas/gate-schema.md` | Phase-transition checks. `GATE_RESULT` contract is the wire format. |
| Handoff protocol | `guides/handoff-cli.md` + `schemas/handoff-document-schema.md` | `pf handoff resolve-gate` / `complete-phase` / `marker`. |
| Prime context | `guides/prime.md` | Tiered context injection (Full/Refresh/Handoff/Minimal). |
| Agent sidecars | `sidecars/` (runtime) + agent definitions | Per-agent persistent learning files (`{agent}-patterns.md`, `-gotchas.md`, `-decisions.md`). |
| Tandem protocol | `guides/tandem-protocol.md` | Background observer pairing + Consultation Protocol. |
| Hooks | `guides/hooks.md` | Session/pre/post tool-use hook system. |
| Output styles | `guides/output-styles.md` | Terse/verbose/teaching response modes. |
| Patterns library | `patterns/` | Fan-out/fan-in, approval-gates, helper-delegation, tdd-flow. |
| Schemas | `schemas/` | Gate, session, workflow, workflow-step, skill, context, handoff-document. |
| Agent templates | `agents/templates/` | Strategic (Opus-class) and tactical (Haiku-class). |

## In-scope from Superpowers

The full skill library in `superpowers/5.1.0/skills/`:

`brainstorming`, `writing-plans`, `executing-plans`, `subagent-driven-development`, `dispatching-parallel-agents`, `test-driven-development`, `systematic-debugging`, `verification-before-completion`, `requesting-code-review`, `receiving-code-review`, `using-git-worktrees`, `finishing-a-development-branch`, `writing-skills`, `using-superpowers`.

The `using-superpowers` auto-invocation pattern (skill discovery and announcement) is the model BRM should preserve — superpowers skills *trigger automatically*, and that property is load-bearing.

## Design tension to resolve

PF wraps its workflows around **stories** (one session = one story id, sprint-scoped). Superpowers wraps its workflow around a **spec/plan** (one branch = one feature, plan-scoped). BRM must pick a primary noun — likely **plan** — and redefine workflow phases against it. This is the central design decision; don't assume it's been made.

## Conventions (provisional, until the user says otherwise)

- Match Pennyfarthing's file layout where practical (`workflows/`, `gates/`, `patterns/`, `schemas/`, `skills/`) so prior art transfers without translation.
- Workflow definitions are YAML. Gates are markdown with a `GATE_RESULT` contract block.
- Reference linked memories with PF's existing schema vocabulary before inventing new tags.

## What not to do

- Don't port `pf sprint`, `pf jira`, `current-sprint.yaml`, `/sm`, `/pf-sm`, `/pf-sprint`, story-id session files, or the `sprint/` directory shape.
- Don't pull in PF's persona/theme/OCEAN system — that's research scaffolding, not workflow plumbing.
- Don't symlink into `orc-penny/pennyfarthing/pennyfarthing-dist/` — BRM should own its definitions outright (copy + adapt, not link).

---
agent-notes: { ctx: "filled-in CLAUDE.md for greeter CLI sample", deps: [docs/methodology/phases.md], state: active, last: "sato@2026-03-21" }
---

# CLAUDE.md -- Project Instructions for Claude Code

## Project Overview

**Project Name:** greeter
**Description:** A simple CLI greeting tool
**Tech Stack:** Python + Click

**Codebase map:** `docs/code-map.md` -- read this first to understand the package structure, public APIs, and data flow.

## Agent-Notes Protocol (MANDATORY)

Every non-excluded file must have agent-notes metadata. See `docs/methodology/agent-notes.md` for spec.

1. Every new file gets agent-notes (excluded: pure JSON, lock files, binaries).
2. Every edit updates `last` to `<agent>@<date>`.
3. `ctx` under 10 words, `deps` = direct deps only, `state` must be accurate.

## Team & Process

**Methodology:** Phase-dependent hybrid teams. See `docs/methodology/phases.md` for the 7-phase model.

| Phase | Lead | Key Pattern |
|-------|------|------------|
| Discovery | Cam | Elicit before implementing |
| Architecture | Archie | ADR before code |
| Implementation | Tara then Sato | TDD red-green-refactor |
| Parallel Work | Grace | Market / self-claim |
| Code Review | Vik + Tara + Pierrot | Three parallel lenses |
| Debugging | Sato | Blackboard with Tara, Vik, Pierrot |
| Sprint Boundary | Grace | `/sprint-boundary` (mandatory) |

## Development Workflow

### Per Work Item
1. **Start** -- Move issue to "In Progress" on the board.
2. **TDD** -- Red then Green then Refactor. Tara writes failing tests first.
3. **Commit** -- One commit per issue, conventional message, `Closes #N`.
4. **Review** -- Move issue to "In Review." Invoke code-reviewer. Fix Critical/Important findings.
5. **Done Gate** -- Full checklist at `docs/process/done-gate.md`.
6. **Close** -- Move issue to "Done." Push.

### Commit Discipline
Commit and push after every reasonable chunk of work. One commit per issue. Conventional commits format.

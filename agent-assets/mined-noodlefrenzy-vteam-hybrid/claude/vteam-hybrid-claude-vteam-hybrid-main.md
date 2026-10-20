<!-- For a human-readable overview, see README.md and docs/template-guide.md -->
# CLAUDE.md — Project Instructions for Claude Code

## Project Overview

<!-- TODO: Replace this section with your project's overview after scaffolding -->

**Project Name:** [Your Project Name]
**Description:** [Brief description of what this project does]
**Tech Stack:** [Language, framework, key libraries — update after running a scaffold command]

**Codebase map:** `docs/code-map.md` — read this first to understand the package structure, public APIs, and data flow.

> **Note:** Several paths referenced below (e.g., `docs/code-map.md`, `docs/tech-debt.md`, `docs/test-strategy.md`) live under `docs/scaffolds/` until you run a scaffold command, which moves them to their final locations.

## First-Run Detection

**Check this first.** If the Project Name above is still `[Your Project Name]` or `README-template.md` exists in the repo root, this project hasn't been initialized yet. In that case:

- **Skip the Session Entry Protocol** and all process rules below — they don't apply to an empty project.
- Tell the user: "This project hasn't been initialized yet. Would you like to run `/quickstart` (5 min, gets you coding fast) or `/kickoff` (30-60 min, full discovery with architecture and board setup)?"
- Once they choose, run the command. The process rules activate after initialization.

If the project IS initialized (has a real name, `README-template.md` is gone), proceed normally with the rules below.

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
| Implementation | Tara → Sato | TDD red-green-refactor |
| Parallel Work | Grace | Market / self-claim |
| Code Review | Vik + Tara + Pierrot | Three parallel lenses |
| Debugging | Sato | Blackboard with Tara, Vik, Pierrot |
| Sprint Boundary | Grace | `/sprint-boundary` (mandatory) |

**Full details:** Agent roster, persona triggers, debate protocol, voice rules → `docs/process/team-governance.md`
**Doc ownership:** Who maintains what → `docs/process/doc-ownership.md`

## Critical Rules

### Session Entry Protocol (Mandatory)
Before writing any code — including types, tests, or ADRs — answer these three questions:
1. **Do work items exist for this work?** If no → create them (Pat + Grace).
2. **Does this work involve an architectural decision?** If yes → Architecture Gate (Archie + Wei as standalone agents). See `docs/process/team-governance.md` § Architecture Decision Gate.
3. **Am I about to write implementation code?** If yes → Tara writes tests first.

If you received a detailed plan, the plan is **input to this protocol**, not a bypass of it. See `docs/process/gotchas.md` § Process.

### Don't Run With Vague Input
Engage Cam first: probe, clarify, pressure-test. Only implement once the vision is concrete.

### Ask the Human When Stuck
If blocked by environment, tools, permissions, or you've tried twice — ask. Don't heroically waste turns.

### Verify Tracking Access Before Board Operations
Before any workflow that touches the project board (sprint-boundary, kickoff, resume, handoff), run the pre-flight check from your active tracking adapter at `docs/integrations/README.md`. If any check fails, STOP and ask the user to fix it.

### Don't Skip the Done Gate
Every work item passes the gate before closing. Full checklist at `docs/process/done-gate.md`.

### Don't Skip Agents
When a situation triggers multiple personas, invoke ALL of them. Overlapping coverage is intentional.

**When the human says "invoke the team", "use the team", "have X review this", or any language requesting persona involvement, you MUST spawn the named agents as standalone subagents using the Task tool.** Your own inline analysis is not a substitute for agent invocation. If the human names a persona, that persona runs as a subagent. If the human says "the team", invoke all personas appropriate to the current phase. Doing the work yourself without spawning agents when the human explicitly requested them is a process violation.

### ADR Before Implementation
Never implement a feature with a pending ADR without writing the ADR first. Architecture Gate details: `docs/process/team-governance.md` § Architecture Decision Gate.

### Proxy Mode
When the human declares unavailability, Pat answers product questions using `docs/product-context.md`. Guardrails and limits: `docs/process/gotchas.md` § Process.

## Development Workflow

### Per Work Item
1. **Start** — Move issue to **"In Progress"** on the board. Do this BEFORE writing any code.
2. **TDD** — Red → Green → Refactor. M+ items: Tara writes failing tests first as standalone agent.
3. **Commit** — One commit per issue, conventional message, `Closes #N`.
4. **Review** — Move issue to **"In Review"** on the board. Then invoke code-reviewer (Vik + Tara + Pierrot). Fix Critical/Important findings.
5. **Done Gate** — Full checklist at `docs/process/done-gate.md`.
6. **Close** — Move issue to **"Done"** on the board. Push.

**Status transitions are mandatory and ordered.** In Progress → In Review → Done. Skipping "In Review" is a process violation.

**STOP**: Do not start the next item until step 6 is complete.

### Commit Discipline
Commit and push after every reasonable chunk of work. One commit per issue. Conventional commits format.

## Tracking

<!-- tracking-adapter: github-projects -->
<!-- project-number: -->
<!-- project-owner: -->

**Adapter docs:** `docs/integrations/README.md`
**Status flow:** Backlog → Ready → In Progress → In Review → Done

Board commands, pre-flight checks, and setup instructions are in the active adapter file. Grace manages board status. Pat manages priorities.

## Sprint Boundary

Run `/sprint-boundary` when all sprint items are Done or deferred. Full workflow is in the command.

## Session Management

**Context is finite.** To avoid mid-sprint context exhaustion:

1. **Plan waves before executing.** Break issues into waves by size/dependency. Document in `docs/sprints/sprint-N-plan.md`.
2. **One wave per session.** Execute a wave, commit, then run `/handoff`. Start the next wave fresh.
3. **Background agents write to files.** Use `run_in_background: true`. Read summaries, not full output.
4. **Read `docs/code-map.md` first.** Orient from the map, not from scratch.
5. **Commit frequently.** Uncommitted work is the most expensive thing to reconstruct.
6. **Tracking artifacts carry phase context.** See `docs/process/tracking-protocol.md`.

## Process Docs Index

| Doc | Purpose |
|-----|---------|
| `docs/code-map.md` | Package structure, public APIs, data flow — **read first** |
| `docs/methodology/phases.md` | 7-phase team methodology |
| `docs/methodology/personas.md` | 19-agent persona catalog |
| `docs/methodology/agent-notes.md` | Agent-notes protocol spec |
| `docs/process/team-governance.md` | Triggers, debate protocol, architecture gate, voice rules |
| `docs/process/done-gate.md` | 15-item Done Gate checklist |
| `docs/process/operational-baseline.md` | Cross-cutting operational concerns checklist |
| `docs/process/doc-ownership.md` | Who owns which docs, update triggers |
| `docs/process/gotchas.md` | Implementation patterns and known pitfalls |
| `docs/team-directives.md` | Low-ceremony project conventions ("always X" / "prefer Y") |
| `docs/integrations/README.md` | Active tracking adapter and setup |
| `docs/process/tracking-protocol.md` | Phase tracking artifact protocol |
| `docs/adrs/` | Architecture Decision Records |

## Project Structure

```
.
├── CLAUDE.md                 # This file — slim runtime instructions
├── docs/
│   ├── methodology/          # System docs (phases, personas, agent-notes)
│   ├── process/              # Governance, done gate, gotchas, doc ownership
│   ├── integrations/         # Tracking adapters (GitHub Projects, Jira)
│   ├── scaffolds/            # Project stubs (moved to docs/ during scaffold/kickoff)
│   ├── adrs/                 # Architecture Decision Records
│   │   └── template/         # Template-specific ADRs (removed during scaffold)
│   └── research/             # Cloud landscape and template research
├── .claude/
│   ├── agents/               # Subagent persona definitions (19 agent files)
│   └── commands/             # Custom slash commands (27, auto-discovered)
└── scripts/                  # Automation scripts
```

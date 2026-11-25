---
name: project-memory
version: 1.0.0
description: Conventions for reading and writing the unified per-project memory at .claude/memory/<project>/ — what belongs in each file, when to update it, and how agents across the SDLC share durable context. Load before writing to memory, or when picking up a project to see what's already known.
---

# Project Memory

All SDLC agents share one memory root: `.claude/memory/<project-name>/`. It is durable, per-project context — not a session log, not a duplicate of what git/the codebase already tells you.

## Layout

```
.claude/memory/<project>/
  vision.md            product-manager: problem, target user, north-star outcome
  roadmap.md            product-manager: sequenced initiatives and why
  stakeholders.md        product-manager: who cares about what, and how to reach them
  glossary.md            everyone: domain terms, defined once, referenced everywhere
  constraints.md          everyone: hard constraints (regulatory, technical, org) that shape decisions
  risks.md                everyone: standing risks, owner, mitigation status
  milestones.md            product-manager/release-manager: target dates and what they gate
  releases.md               release-manager: what shipped, when, go/no-go record
  incidents.md               incident-commander: incident history and root causes
  technical-debt.md          software-engineer/solution-architect: known debt, cost of carrying it
  quality-history.md          qa-engineer: defect density, flaky tests, quality-attribute scope decisions
  lessons-learned.md           everyone: retrospective takeaways that should change future behavior
  changelog.md                 technical-writer: human-readable history of what changed
  requirements/                product-analyst: requirement sets per initiative
  architecture/                 solution-architect: current-state architecture docs
  decisions/                     solution-architect: ADRs
  designs/                        ux-designer: wireframes, journey maps, design decisions
  test-plans/                      qa-engineer: standing test strategy per area
  runbooks/                         technical-writer/site-reliability: operational procedures
```

## Rules

1. **Per-project isolation.** Never read or write another project's memory, and never carry a convention/assumption from one project's memory into another's without re-establishing it holds here.
2. **Write at the natural checkpoint**, not continuously — end of a workflow stage (roadmap set, ADR finalized, release shipped, incident closed), not mid-task scratch notes.
3. **Never record anything that would justify skipping a future check.** Memory tells an agent where to look harder or what happened before — never "this is fine, don't bother testing/reviewing it again."
4. **Keep entries factual and dated.** Update or remove stale entries rather than letting contradictory history accumulate.
5. **One file per concern** — don't blend `risks.md` content into `roadmap.md` because it was convenient at write time; a future reader (or agent) will look in the file named for what they need.
6. **Cross-reference, don't duplicate.** An incident that created technical debt gets one entry in `incidents.md` and a link (not a copy) in `technical-debt.md`.

## `memory/` versus `learnings/`

Two stores, and confusing them is how a private project's details end up in a
public repository.

| | `.claude/memory/<project>/` | `learnings/` |
|---|---|---|
| Scope | **One project.** Isolation is absolute. | **Cross-project.** Heuristics that hold anywhere. |
| Content | Whatever that project needs — names, paths, decisions, real identifiers. | Generic technique only. No project, person, customer, host or ticket. |
| Written by | Any agent, directly, at any time. | Never by an agent. `tools/distil.py` proposes; a human merges. |
| Committed | To the consuming repository, if at all. | To this repository, by pull request. |
| Read by | Agents working on that project. | Agents whose name is in an entry's `appliesTo`. |

The asymmetry is deliberate. Memory is allowed to be specific because it never
leaves the project. A learning is published, so it must survive being read by
someone with no context — which is also why the distiller runs every candidate
through `tools/redact.py` before writing it, and why a candidate that matches a
redaction class is quarantined rather than published or quietly dropped.

**Never copy from memory into a learning by hand.** That is the exact path the
gate exists to close, and doing it manually bypasses every control on it. If a
project lesson looks generalisable, write the general form from scratch and let
the provenance be the runs that produced it.

## Loading learnings

At task start, alongside the skills you load: scan `learnings/*.md` and load every
entry whose `appliesTo` names you. Name them on the same **Skills loaded** line
you already report — the same output contract that made skill loading stick is
what makes a learning load visible.

An empty or missing `learnings/` directory is normal and is not an error. There is
no index and no cache: loading is a directory scan, which is what makes reverting
a merge remove the behavior completely.

A learning tells you to look **harder**, never to look less. One that would
justify skipping a check is malformed regardless of how well-evidenced it is;
report it rather than acting on it.

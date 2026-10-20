---
name: wave-planning
description: >
  Turn ONE settled feature goal into a parallel build plan — N agent tasks that don't collide,
  emitted as a dependency-tagged wave manifest (id / deps / files / task). The crux it enforces:
  batch on FILE-DISJOINTNESS, not logic — two logically-independent tasks touching the same file
  cannot share a wave. Recipe: map seams → contracts into a foundation task → collision-free
  frontier → consolidate shared hotspots → serial integration last → manifest. Stops at the manifest
  (dispatch/worktrees are the harness's job; branching/landing is `memory`'s). Load AFTER the design
  is settled and BEFORE putting more than one agent on the work. Triggers: parallelize, decompose,
  wave plan, split this work, fan out, what can run in parallel, break this into tasks, run N at
  once, do these concurrently, file-disjoint, frontier, task manifest.
---

# Wave Planning — decompose one goal into a collision-free parallel build

> **On-demand decomposition playbook.** Load it once a design is settled and you're about to build
> with more than one agent. It answers exactly one question — *"how do I carve THIS goal so N agents
> run it without colliding?"* — and produces one artifact: a dependency-tagged **wave manifest**.
> **It stops there.** Fanning the manifest out, isolating workers, and collecting results are the
> harness's job, not this skill's.

## The boundary (decomposition only — hand the rest off)
This skill owns decomposition and nothing else. Keep these concerns apart — welding decomposition to
dispatch is the classic mistake, because the harness already owns dispatch:

| Concern | Owner | This skill? |
|---|---|---|
| **Decomposition** — carve the goal, tag deps + files, compute the frontier | **you, via this skill** | ✅ the whole job |
| Dispatch / worktree isolation / collection | the **harness** (`Workflow` `parallel`/`pipeline`, or concurrent `Agent` calls) | ❌ hand off |
| Branch per unit of work / land / record | the **`memory`** skill | ❌ hand off |
| The architecture + design forks the plan assumes | the **`software-architect`** agent (upstream) | ❌ consumes its output |

**Input:** a settled goal + the code it plugs into. **Output:** a wave manifest ready to fan out.
If you catch yourself writing a coordinator loop or a worker contract, you've left this skill.

## When this applies
Any time work will be split across more than one agent: "break this feature into tasks", "what can
run in parallel", "fan out the roadmap". Also whenever you **add a backlog task** — tag it (`deps` +
`files`) so the frontier stays a *query*, not a fresh judgment call each time.

## The method (goal → manifest)
1. **Map the seams first.** Read the requirements AND the exact code seams the goal plugs into
   (existing APIs, tables, modules, clients). Cheap and parallelizable — map requirements and
   code-seams (e.g. with concurrent read-only agents) before planning.
2. **Extract the contracts → ONE foundation task.** The inter-task data types / interfaces every
   downstream task shares. Fix these *first*; this is "contract-before-code" lifted to the
   orchestration level. The foundation is what unblocks the whole frontier — stub the stages against
   typed seams so the fan-out has something stable to build against.
3. **Carve the frontier on file-disjointness.** The frontier = tasks that are *ready* (deps met) AND
   *pairwise file-disjoint*. This is the crux: overlap is decided by **files, not logic** (see below).
4. **Consolidate hotspots OUT of the frontier.** Any file two+ tasks would edit is pulled into either
   the foundation (if it's a shared contract) or the integration (if it's wiring). The rule that makes
   this concrete: **parallel tasks create NEW files only**; every edit to a shared hotspot is owned by
   exactly one task. This is the active discipline that *makes* the frontier collision-free — not a
   hope that it is.
5. **Serial integration LAST.** One task wires the consolidated hotspots together and runs the
   end-to-end check. It depends on everything; it never parallelizes.
6. **Emit the manifest + group into waves.** Tag every task (below); a wave = a maximal file-disjoint
   ready set. Foundation is wave .0, the frontier is wave .1, integration is the final serial wave.

## The manifest (tag once per task)
Every actionable task carries the same four fields the roadmap and session plans use:

| Field | Meaning |
|---|---|
| **id** | stable kebab slug — how other tasks name it in `deps` |
| **deps** | ids that must land first; empty ⇒ ready at the start |
| **files** | paths/dirs it will touch — **the collision axis** (two tasks sharing a path can't share a wave, deps or not) |
| **task** | one line: the goal + its acceptance check |

Row shape:
`| stage-parse | core-contracts | src/parse.py | raw input → typed records, downstream refs stubbed |`

Then state the waves explicitly, e.g.: *2.0* foundation (+ any other dep-free task) → *2.1* the N-wide
frontier → *2.2* serial integration.

## The collision axis is FILES, not logic
The one rule that most often gets this wrong. Two tasks can be completely independent in *meaning* and
still be un-parallelizable because they both edit the same module. Batch on file-disjointness first,
deps second. When you're unsure whether a dependency edge exists between two tasks — **add it.** A
false serialize costs minutes; a missed edge corrupts two workers' worktrees.

## Guardrails (where naive splitting bites)
| Trap | Rule |
|---|---|
| Two independent tasks edit the same file | not parallelizable in one wave — consolidate the shared file into the foundation/integration, or serialize into different waves |
| A task quietly consumes another's output | if unsure the edge exists, **add the dep** |
| Over-splitting | a task must be worth a whole agent — fold trivial edits into a neighbor |
| Splitting the serial spine | never parallelize a dependency chain; fan out only its independent branches |
| A hotspot with no clear owner | assign it to exactly one task (foundation if contract, integration if wiring) — never two |

## Hand-off (what happens after the manifest)
- **To build it:** fan the frontier out — `Workflow` (`parallel`/`pipeline`, `isolation: worktree`)
  or concurrent `Agent` calls in one message. The harness dispatches, isolates, and collects.
- **To land it:** the **`memory`** skill's branch-per-unit-of-work + land + record sequence.
- **Design questions surfaced mid-plan** (a data-model shape, a fork): route to `software-architect`
  / the `governance` skill — don't decide architecture inside the decomposition.

## Gotcha
This skill's job is finished when the manifest exists. Its value is entirely in step 4 — **hotspot
consolidation** — and the file-disjointness axis; the dependency graph itself is table stakes. If a
plan's parallel tasks share an edited file, the plan is wrong no matter how clean the dependency graph
looks.

---
name: family-relay
description: "Run the six FAMILY stage agents as a relay in which the verdict word decides the next hop: FRAMED goes to architect, PROPOSED to maker, PLAN READY to the build, DIVERGED back to architect, PASS to launcher, STOP to a person. Covers the routing table, passing each hop the artifact plus only the previous Handoff section, treating a report with no verdict as a question, and the two-strike rule that steps back a stage when the same verdict returns. Use when framer, architect, maker, inspector, launcher or yielder reports are coming back and someone asks what happens next, what to do with a FIX, DIVERGED or NOT READY, or how to chain the stage agents. Not for choosing the workflow (family-workflow), dependency-graph orchestration (agent-orchestration), or briefing one agent (agent-delegation)."
allowed-tools: Agent(framer), Agent(architect), Agent(maker), Agent(inspector), Agent(launcher), Agent(yielder), Read, Write, Edit, Grep, Glob, Bash(git:*)
---

# The FAMILY relay

A relay is finished when every hop was chosen by a verdict word and not by habit, each hop received only what it needed, and the slice and the approach were decided in the main conversation.

Chaining agents fails in three quiet ways. The result of a stage is forwarded to whichever stage is next in the diagram rather than to the one the verdict names, so a `DIVERGED` goes back to the stage that wrote the plan it diverged from and the plan is rewritten to match the code. Every hop gets a paraphrase of the whole thread, so the next stage inherits the previous stage's framing instead of judging the artifact. And a stage returns the same verdict three times while the loop keeps feeding it, because nobody asked whether the stage before it was the problem.

## Scope

Use for: moving one slice through `framer`, `architect`, `maker`, the build, `inspector`, `launcher` and `yielder`, and for deciding what a returned verdict means.

Do not use for: choosing the workflow or profile (`family-workflow`), scheduling many agents over a dependency graph (`agent-orchestration`), or briefing a single agent on a single task (`agent-delegation`).

## The routing table

| Report | Verdict | Next hop |
| --- | --- | --- |
| framer | `FRAMED` | architect |
| framer | `NEEDS INPUT` | main conversation, then framer again |
| framer | `NOT FRAMED` | main conversation |
| architect | `PROPOSED` | maker |
| architect | `NEEDS FRAME` | framer |
| maker, plan | `PLAN READY` | build |
| maker, check | `ON PLAN` | inspector |
| maker, check | `DIVERGED` | architect, never maker again |
| inspector | `PASS` | launcher |
| inspector | `FIX` | build for each `FAILS` line; the Inspect owner for each `NOT ASSESSED` one |
| inspector | `STOP` | a person |
| launcher | `READY` | the release owner, who ships and measures the signal, then yielder |
| launcher | `N-A` | the main conversation, to write the Launch waiver, then yielder |
| launcher | `NOT READY` | the stage that owns the missing piece |
| yielder | `YIELDED` | framer, with the next slice |

`BLOCKED` from architect or maker, and `INSUFFICIENT EVIDENCE` from yielder, go to the main conversation: each names something only a person can supply. Read `references/routing.md` for the cases the table compresses, including who owns a `NOT READY`.

## Workflow

### 1. Decide the slice and the approach yourself

`framer` proposes a slice and `architect` proposes an approach; the main conversation accepts or changes each before the next hop. Delegating that choice hands the direction of the whole run to the stage with the least context on what you want.

### 2. Route on the first line

Read the verdict word and follow the table. A report with no verdict line is a question, not a result, and returns to the conversation.

### 3. Send each hop the artifact and the Handoff only

Give the next stage the previous artifact and only the previous report's `Handoff` section. If the report has none, pass its open-questions or not-assessed block verbatim. Never a paraphrase of the whole: a summary carries the previous stage's conclusions in as premises. Read `references/hop-brief.md` for what each hop receives.

### 4. Build between PLAN READY and the check

The build is not a stage agent. The main agent does it, or one writing agent on a mid tier, working step by step from the plan. Read `plan-drift-gate` for the brief and for the maker check that must come back `ON PLAN` before inspection.

### 5. Ask for go or no-go at the Inspect to Launch handoff

`PASS` from `inspector` is a statement about the change. Whether it ships is the go/no-go that handoff opens with, answered by the owner of Inspect. `launcher` returns `NOT READY` only by naming a missing go/no-go, release path, signal or rollback; a `NOT READY` naming none of them is a question.

### 6. Apply the two-strike rule

The same verdict from the same stage twice means the stage before it is wrong. Step back one further than the table says: a second `FIX` on the same finding goes to architect rather than the build, because a repeat means the approach is wrong and not the plan (`fresh-inspector-rounds` reopens Architect with the finding as a constraint); a second `DIVERGED` goes to framer rather than architect. `references/routing.md` lists each.

### 7. Waive in writing, and only two stages

Architect and Launch may be waived with the reason and the risk written down; the relay then skips that hop. Frame, Make, Inspect and Yield are not waivable.

## Anti-patterns

**Re-running maker on DIVERGED.** It rewrites the plan to fit the diff and the drift is ratified. The return goes to architect, which rules on the approach.

**The paraphrased handoff.** The next stage argues with your summary instead of reading the artifact.

**A third identical verdict.** Two strikes mean the input is wrong, not the stage.

**Delegating the slice.** A stage that picks its own slice is grading its own work.

## References

- `references/routing.md`: read at step 2 for every verdict, each stage's second-strike hop and who owns a `NOT READY`.
- `references/hop-brief.md`: read at step 3 for what each hop receives and the shape of the handoff when a report carries none.

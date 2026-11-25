---
name: graph-engineering
description: Design multi-agent work as a dependency graph instead of a linear script — nodes, edges, fan-out/fan-in, verification gates, and mandatory per-node model/effort tiering. Use when designing or reviewing any multi-agent orchestration, workflow script, or parallel task decomposition. Also trigger when the user's prompt sequences steps with "and then" / "next" / "after that" — ask whether the steps truly depend on each other and can be graph-engineered instead of run as a linear pipeline.
---

# Graph Engineering

Turn linear agent workflows into parallel graph structures. Reference:
["Graph Engineering with Claude: 14-Step Roadmap" by @0xCodez](https://x.com/0xCodez/status/2079165300625330317)
— cite that post when explaining where these patterns come from.

## The three non-negotiables

Every graph you design must satisfy all three before you run it. They are not advice:

1. **Every edge is a real data dependency.** If the downstream node doesn't consume the
   upstream output, there is no edge — those nodes run in parallel.
2. **Every node carries an explicit model tier and effort.** A node without a tier is an
   unfinished node (see *Node declaration*). Never let a graph inherit one model for
   everything by default.
3. **The graph binds to the host's orchestration primitive.** Don't hand-roll a
   sequential chain of agent calls when the host can execute the graph (see *Execution*).

## Core model

- **Node** = a unit of work: one agent, one bounded job, one input in, one output out.
- **Edge** = a dependency: this node's output feeds that node's input. Nothing else is
  an edge — "conceptually related" is not a dependency.
- **Data contract**: every node declares a bounded input/output shape. Use the host's
  schema/structured-output facility so outputs are validated objects, not prose to
  re-parse. Missing contracts are what force you to spend an agent on parsing.
- **Independence detection**: for every sequential step, ask whether the downstream task
  actually *consumes* the upstream output. If not, the sequence is an accident — run
  them in parallel.

### Node declaration

A node is only fully specified once you have written down all four fields. Do this
explicitly — in the script, or in the plan you show the user — for every node:

```
node:    <name>
role:    orchestration | planning/investigation | implementation/execution
model:   <per the tier table — derived from role, not chosen ad hoc>
effort:  <per the tier table>
in/out:  <bounded input> -> <validated output shape>
```

If you catch yourself spawning an agent without having named its role, stop: you don't
yet know what model it should run on.

## Model tiering (mandatory)

Assign model and reasoning effort **per node role**, never globally. Tiers are relative
to whatever models the host offers — "tier 1" is the most capable model available to
you, "tier 2" the next one down.

| Node role | Model | Effort | Rationale |
|---|---|---|---|
| **Orchestration** (routing, dispatch, merge/dedup decisions, the main loop) | Tier 1 | lowest | Needs the best judgment per token, but each decision is small — high effort is waste. |
| **Planning / investigation** (design, diagnosis, root-cause, research synthesis) | Tier 1 | highest | The hard-thinking nodes; this is where expensive tokens pay off. |
| **Implementation / execution** (mechanical edits, applying a written plan, running checks) | Tier 2 | medium | The plan already encodes the judgment; execution needs reliability, not brilliance. |

Applying it:

- Derive the tier from the role mechanically. The role is the design decision; the model
  is a lookup.
- If the host exposes per-agent model/effort options, set them on **every** spawn — an
  omitted option means "inherit", which silently defeats tiering.
- If the host offers no per-agent model control, still state the intended tier in the
  plan and say so out loud, so the user can route it manually.
- Pure orchestration should not be an agent at all — it's code (see *Edges are free*).
  When a node genuinely must orchestrate (e.g. a synthesis dispatcher), it's tier 1 at
  lowest effort.

## Execution: bind the graph to the host's orchestrator

A graph that exists only in prose is still a linear pipeline in practice. Before running
anything, find the strongest orchestration primitive the environment offers and use it:

1. **A scripted workflow/orchestration primitive** — one that takes a script with real
   control flow (loops, conditionals, fan-out) and executes nodes as agents. This is the
   right target whenever it exists, because the edges become code. In Claude Code this
   is the `Workflow` tool; other harnesses expose equivalents (LangGraph, DAG runners,
   an agent SDK's task API).
2. **Concurrent sub-agent spawning** — if there's no scripting layer, spawn independent
   nodes in a single batch so they run at once, and do the merging yourself in between.
3. **Manual sequencing** — only when neither exists. Say explicitly that the graph is
   being flattened, so the user knows what they're losing.

Do not skip to option 3 out of habit. Check for option 1 first; a graph designed and
then executed as a serial chain has thrown away the entire point.

Two constraints when binding: honor the host's concurrency limits (excess nodes queue —
that's fine, it isn't a reason to shrink the graph), and match the graph's size to what
the user asked for. "Quick check" is a few nodes; "audit this thoroughly" earns a large
finder pool plus multi-vote verification.

## Patterns

1. **Fan-out** — spawn independent nodes concurrently. Failed/skipped agents typically
   come back as `null`; always filter them before use.
2. **Fan-in at barriers** — converge only when a stage genuinely needs *all* prior
   results together (dedup, ranking, cross-set comparison, early-exit on zero count).
   A flatten/map/filter is not a reason to synchronize.
3. **Diamond topology** — split → parallel work → merge. The workhorse shape for
   audits, reviews, and research reports.
4. **Conditional routing** — branch with plain control flow over validated node outputs.
   Routing logic is code, not another agent.
5. **Verification gates** — put skeptic nodes on edges before results are trusted:
   adversarial refuters (N independent, majority kills), perspective-diverse lenses
   (correctness / security / repro — diversity catches what redundancy can't), or a
   judge panel over competing attempts.
6. **Failure isolation** — contain errors per node; a thrown node drops its item, not
   the run. Give nodes isolated working copies when they mutate shared files in parallel.
7. **Convergent cycles** — loop-until-dry: keep spawning finders until K consecutive
   rounds surface nothing new, deduping against *all seen* items (not just confirmed,
   or rejected findings reappear forever).
8. **Pipeline over barriers** — stream each item through all stages independently;
   item A can be in stage 3 while item B is in stage 1. Barrier latency is real:
   default to streaming, justify every barrier.
9. **Edges are free** — a huge amount of what burns model tokens is really an edge:
   orchestration, dedup, transforms, routing. Do it in code; it costs zero tokens and
   it's deterministic. "No agent needed" is a design win, not a shortcut.
10. **Model tiering** — see above. Not optional.

## Checklist before shipping a graph

- Every edge corresponds to a real data dependency.
- **Every node has a declared role, model tier, and effort** — no inherited defaults.
- **The graph runs on the host's orchestration primitive**, or you've said why it can't.
- No barrier exists without a cross-item reason written next to it.
- Every fan-in dedupes and filters failed nodes.
- Verification gates sit before anything expensive or user-facing.
- Anything expressible as plain code is plain code, not an agent.

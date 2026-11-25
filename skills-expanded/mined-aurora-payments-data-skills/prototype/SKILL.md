---
name: prototype
description: Build a throwaway prototype to answer a pipeline design question. Use when the user wants to sanity-check whether a transformation, dedup, grain, or incremental strategy holds on real data, or explore what shape a mart, metric table, or dashboard feed should be.
---

# Prototype

A prototype is **throwaway code that answers a question**. The question decides the shape. In a pipeline the question is almost always about the data, so a prototype runs against real sampled data. A design that has only ever met invented rows has answered nothing.

## Pick a branch

Identify which question is being answered, whether from the user's prompt, the surrounding code, or by asking if the user is around:

- **"Does this transformation / grain / incremental strategy hold?"** → [LOGIC.md](LOGIC.md). Build a scratch-schema prototype that pushes the candidate logic through a real data sample plus hand-built pathological rows, the cases that are hard to reason about on paper.
- **"What shape should this surface be?"** → [SHAPE.md](SHAPE.md). Materialize several radically different shapes for a mart or metric table side by side in a scratch schema, judged against one shared panel of consumer queries.

The two branches produce very different artifacts: getting this wrong wastes the whole prototype. If the question is genuinely ambiguous and the user isn't reachable, default to whichever branch better matches the surrounding code (a staging or intermediate transformation → logic; a consumer-facing mart or dashboard feed → shape) and state the assumption at the top of the prototype.

## Rules that apply to both

1. **Throwaway from day one, and clearly marked as such.** Locate the prototype code close to where it will actually be used (next to the layer it's prototyping for) so context is obvious, but name it so a casual reader can see it's a prototype, not production: a `proto_` prefix on every model and table. Prototype relations materialize only in a scratch schema (the project's dev-schema convention, or an ephemeral clone where the platform supports one) and never in a schema anything downstream reads.
2. **One command to run.** Whatever the project's existing runner supports: `dbt build --select +proto_<name>` (the leading `+` selects the model plus everything upstream, so the pathological fixture seed rebuilds on every run), `make <name>`, `papermill <notebook> <output>`, etc. The user must be able to rebuild the prototype end to end without thinking, because a prototype that takes three manual steps stops being re-run, and a prototype that isn't re-run stops answering.
3. **Read sampled, write dead-end.** Inputs are a small real slice, one partition or a bounded sample of the source, so every re-run is cheap. The partition is the natural unit to sample: it's the atomic unit of pipeline state. Outputs land only in the scratch schema and nothing may depend on them: no dashboard, no downstream model, no export. The scratch schema is the "PROTOTYPE, wipe me" name.
4. **Skip the polish.** No data tests, no schema contracts, no documentation, no orchestration wiring, nothing beyond what makes the prototype _runnable_. The point is to learn something fast. Tests come at capture time, when the pathological rows graduate into the promoted model's unit tests.
5. **Surface the data.** After every run, render what the logic did to the rows: inputs and outputs side by side (logic), or the same consumer query against every variant (shape), plus the row count in and out and the duplicate count on the claimed grain. Numbers the user can't see are decisions the user can't check.
6. **Capture it when done.** Fold any validated decision into the real DAG, where the winning model becomes a real model and the pathological fixture becomes its unit tests, then capture the prototype itself as a **primary source**: commit it to a throwaway branch, out of main, and leave a context pointer to that branch on the implementation issue. Capture the answer too, the verdict and the question it settled, in the issue or a commit. Drop the scratch schema. The main branch keeps only the validated decision.

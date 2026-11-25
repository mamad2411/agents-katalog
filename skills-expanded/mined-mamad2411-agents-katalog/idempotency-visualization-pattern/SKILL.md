---

name: idempotency-visualization-pattern
description: Visual patterns for demonstrating idempotency guarantees through request replay, key-based deduplication, and state convergence animations.
category: design
triggers:
  - idempotency visualization pattern
tags: [design, idempotency, visualization]
version: 1.0.0
---

# idempotency-visualization-pattern

Build idempotency visualizers around a **request timeline with duplicate-detection overlay**. The primary canvas shows a sequence of incoming requests (each with an idempotency key badge, timestamp, and payload hash), while a parallel "server state" panel shows only the operations that actually mutated state. When a duplicate arrives, draw a dashed redirect arrow from the duplicate to the originally-cached response, and keep the state panel visually unchanged — the absence of motion is the proof of idempotency. Color-code keys: green for first-seen (write-through), amber for replay-hit (cache-return), red for key-collision-with-different-payload (conflict).

For HTTP method quizzes, use a **method-matrix grid** where columns are HTTP verbs (GET, PUT, POST, PATCH, DELETE) and rows are scenarios ("called twice", "called N times", "called after failure"). Each cell shows a mini state diagram: identical end-states across repetitions mean idempotent (checkmark + green), diverging states mean non-idempotent (X + red). PATCH deserves a split cell since idempotency depends on patch semantics (JSON Merge Patch vs. JSON Patch with array-append ops).

For function playgrounds, pair an **input-output table** with a **"run N times" slider**. As the slider moves from 1→N invocations, the output column must remain visually frozen for idempotent functions and animate/diverge for non-idempotent ones. Always include a "side-effect ledger" showing external writes (DB rows, emails sent, charges made) — idempotency is defined by this ledger staying stable, not by the return value alone.

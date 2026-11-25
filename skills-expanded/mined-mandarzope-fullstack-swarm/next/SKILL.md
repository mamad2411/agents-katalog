---
name: next
description: >
  Run the pipeline autonomously: repeatedly apply CLAUDE.md dispatch rules
  (track-aware, including UX design and visual QA stages), dispatch eligible
  stories in parallel (cap 7), update _queue.json after each batch, and keep
  going until BLOCKED, full completion, or no dispatchable work. Use when the
  user types /next, or says "advance the pipeline", "run the swarm",
  "autonomous pipeline", or wants all ready stages drained without repeated
  /next.
---

Read `CLAUDE.md` and `stories/_queue.json`.

## Autonomous loop

Repeat **one iteration** until a **stop condition** fires:

### 1. Reload state

Re-read `stories/_queue.json` (and `CLAUDE.md` if needed) so each iteration uses fresh statuses.

### 2. Hard stop: BLOCKED

If any story is `BLOCKED` -> tell the human, summarize queue, **exit the loop** (do not dispatch).

### 3. Choose the next batch (priority order)

Apply dispatch rules 3–10 from `CLAUDE.md`, in order:
`FAILING_VISUAL_QA -> FAILING_QA -> READY_FOR_VISUAL_QA -> READY_FOR_QA -> READY_FOR_BUILD
-> READY_FOR_UX_DESIGN -> READY_FOR_LLD -> READY_FOR_ARCH`.

Only consider stories whose `deps` are all `DONE`. **Never** dispatch a story with unmet deps.
Use the **first** rule that matches at least one eligible story; collect **all** stories
matching that rule (with met deps) as one batch. Route by `track` per `CLAUDE.md`'s track
routing table (e.g. `READY_FOR_BUILD` dispatches `developer` for `track=backend` and
`frontend-developer` for `track=ui`/`fullstack`).

If **no** story matches rules 3–10:

- If **every** story is `DONE` -> short success summary, **exit**.
- If `prd/current.md` exists and the queue has **no** stories (empty array) -> dispatch
  `project-manager` once (same prompt as `/ship-prd`), parse `<status>`, update `_queue.json`,
  then **continue** the loop.
- Otherwise -> report queue state (e.g. `DRAFT`, waiting on deps, or stuck), **exit** — do not spin.

### 4. Parallel dispatch

If the batch has **multiple** slugs mapping to the **same** subagent role (after track
routing), dispatch them **in parallel** with concurrent Task tool calls (**cap 7** per
iteration). If the batch is a single story, one Task is enough.

**Maker ≠ checker:** `qa-engineer` and `visual-qa` must always be fresh Task dispatches —
never grade in the implementer's context.

Include in every subagent prompt:

- slug, `track`, absolute paths to inputs, expected outputs, target `next_status` on success
- prior QA/visual-QA report path when re-dispatching on `FAILING_QA`/`FAILING_VISUAL_QA`
- **Identity reinjection**: one line with the role's `role_id`, `identity_marker`, and
  `non_negotiables` from that agent's Identity block
- **Effort / model**: set Task `model` from CLAUDE.md effort routing (`xhigh` for
  project-manager / solution-architect / tech-lead / qa-engineer / visual-qa; `high` for
  ux-designer / developer / frontend-developer)

### 5. Apply results

When the batch finishes, parse **every** returned `<status>` block; for each story append a
`history` entry and set `status` to `next_status`.

### 6. Continue

**Immediately** start the next iteration at step 1. Do **not** stop after one batch to wait
for another `/next` unless a stop condition fired.

### Stop conditions (summary)

- Any `BLOCKED`
- All stories `DONE`
- No eligible batch and **not** the "empty queue + PRD present" special case
- **No-progress guard:** if an iteration performed **no** successful dispatch and the queue is
  unchanged, exit and explain — avoids infinite loops

Keep a short running log of batches dispatched so the final user summary lists what ran and
ends with the queue snapshot.

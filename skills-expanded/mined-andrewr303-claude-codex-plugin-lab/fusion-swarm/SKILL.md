---
name: fusion-swarm
description: >-
  Decompose a large or parallelizable task into subtasks, route each to the best-suited CLI,
  execute in dependency waves in parallel, then synthesize and verify one coherent
  deliverable. Use for multi-file migrations, broad audits, "do all of these", build work
  too big for one pass. Triggers: "swarm", "divide and conquer", "parallelize this",
  "split this across the models", "migrate everything".
---

# Fusion — Swarm

This is the **`swarm`** entrypoint. Load and run **`fusion-orchestrate`** forcing
`mode = swarm`. Unlike panel/council (everyone answers the *whole* task), a swarm splits the
task and gives each panelist a *piece* it's best at — cheaper and faster at scale.

## Mechanic (`references/collaboration-modes.md` §6)
1. **Decompose** (you): break the task into independent subtasks with explicit
   dependencies. If decomposition is itself uncertain, run a quick **scoping huddle** first.
2. **Route** each subtask to its best fit — break ties with `lessons.md` win-rates:
   - 🔴 codex → implementation, refactors, precise code
   - 🔷 copilot → breadth, long-context reading, synthesis-of-many
   - 🟢 opencode → high-volume cheap drafts, boilerplate
   - ⬛ grok → realtime / web-current facts
   - 🔵 you → glue, anything needing repo context, final assembly
3. **Execute in waves:** independent subtasks run in parallel (`fusion.sh dispatch` per
   subtask, backgrounded in one batch); dependent subtasks wait for their inputs. A subtask
   that fails retries on its next-best panelist (its alternate route).
4. **Synthesize + VERIFY** (you): assemble the pieces into one coherent deliverable and
   **run/test it end to end.** A swarm that produced parts you never assembled and ran is
   not done.

## Guardrails
- **Cost gate:** swarms can fan out widely — estimate subtask count × cost and **confirm
  with the user** before a large run.
- **Decompose-failure is silent:** if you can't cleanly split the task, say so and fall back
  to `panel` rather than faking parallelism.
- Record the run (`mode=swarm`) with per-subtask routing so the ledger learns the routing.

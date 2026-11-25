---
name: cyc-reflect
description: "Turn what went wrong or right in finished work into specific proposed edits to CYC skills, checks, or project rules, each tied to evidence. Use when the user says \"reflect\", \"what did we learn\", or \"improve the workflow\", after a task needed corrections, or when a missed dependency or repeated mistake appeared."
---

# Learn from outcomes

The output is proposed edits, not a list of lessons. A lesson that doesn't change a file changes nothing. Follow the [handoff contract](../../docs/skill-contract.md) and the [skill craft guide](../../docs/skill-craft.md).

## The core loop

1. **Collect the moments that mattered.** User corrections, failed checks, missed dependencies, rework, and things that went unusually well. Read the relevant run's `review.md`, handoffs and verification receipts, the selected error ledger, and available transcript or decision log. Use an improvements log only if the project already maintains one; the controller does not generate `.cyc/runs/improvements.tsv`. An AI-written summary is secondary evidence.
2. **Read each moment through three lenses.**
   - **Judgment:** what decision was wrong or right, and what would have led to the right one?
   - **Tooling:** what check, script, or search would have caught it mechanically?
   - **Beneath the obvious:** what is the learning under the first explanation? ("Missed the reminder job" may really be "we only searched imports.")
3. **Pick the strongest mechanism that would prevent it.** In order:
   1. make it impossible (a type or schema)
   2. a test, lint, or CI check
   3. a script or helper the skill tells the agent to run
   4. a sharper step or anti-pattern in an existing skill
   5. a new sentence of prose, as the last resort
4. **Apply the no-op test to every proposed skill edit.** Would a strong model behave differently with this sentence? If not, drop it.
5. **Prefer editing an existing skill over creating one.** A new skill needs recurring evidence across tasks.
6. **Write each proposal as an edit.** Target file, the exact change, the evidence (quoted correction or failed check), where it should *not* apply, and how you would tell if it made things worse.

## Acceptance for a proposal

Keep a proposal only if it is: tied to a real moment, specific enough to apply, decision-changing, not already covered, and durable (it will still be true next month). Drop one-off facts like commit hashes and versions; keep the pattern behind them.

A finding that the skill didn't trigger when it should have is a proposal to tune the skill's **description**, not its body.

## Done when

Each surviving proposal names a file, the change, its evidence, and its counter-case. "No supported lesson this time" is a valid result.

## Anti-patterns

| Name | The tell | Fix |
| --- | --- | --- |
| Lesson list | "We learned to be more careful" | Write the file edit or drop it |
| Prose for a machine job | Adding "remember to check X" when a script could | Build the check |
| One-off promotion | A single correction becomes a global rule | Wait for recurrence or ask the user |
| Authorship drift | The agent's idea recorded as the user's insight | Keep who said what |

## Handoff

Return proposals to the user. Apply them only when the current request authorizes editing skills or rules.

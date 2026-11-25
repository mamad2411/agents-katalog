---
name: lean-jev-usage
description: Explain what the `lean-jev` plugin does and how to use it. Use when someone invokes `/lean-jev-usage`, asks what this plugin covers, or wants to know how to hand a judgment call to Jev and how to add a recipe for a recurring one.
---

# lean-jev

One skill, one job: when a task turns on a judgment rather than on writing
something, hand that judgment to a model built for judgments — and frame it the
way that model needs it framed.

## What it gives you

`/lean-jev:ask-jev`, or simply asking to have Jev score something, routes a
decision to Jev, TypeSafe's System One model, through `scripts/jev.py`.
What comes back is typed: a probability for a yes/no, a position on a rubric you
wrote, a pick from a fixed set with the distribution behind it. Numbers only,
70–500 ms, a fraction of a cent.

The framing is the work. Jev reads a question literally, answers each one in
isolation, and explains nothing, so a question that bundles two factors returns a
confident number about neither. The skill holds the rules that keep a question
answerable — one factor per question, the right type for the job, state cut down
to what the question needs, every number reported next to the question that
produced it.

## Ad-hoc questions and recipes

**Ad-hoc** covers the one-off: score these candidates, rate each of these tests,
does this clear the bar. The general guidelines are enough — the skill picks the
type, splits what needs splitting, and batches the lot into a single call.

**Recipes** are for questions that keep coming back. A recipe is a written
decomposition of one high-level question into Jev-shaped sub-questions, with the
criteria spelled out and an honest note on what it leaves unanswered. The plugin
ships one, `references/evaluating-a-test.md`, for judging whether a test is worth
its lines. `references/writing-a-recipe.md` covers adding your own, including the
honesty rules that keep a recipe from promising more than it measures.

Recipes are where our own vocabulary accumulates: what "severe" means here, what
counts as worth raising, which house pattern a file is being held to.

## Why hand the judgment over at all

Three properties the agent's own read lacks:

- **No drift down a list.** Every question in a call is evaluated independently
  and in parallel, so item 40 gets the same attention as item 1.
- **No stake in the work.** An agent judging code it wrote an hour ago is a
  compromised reviewer.
- **Consistency.** The same rubric means the same thing next week, which is what
  makes a threshold worth tuning.

## When to keep it

Choosing between architectures or tools, anything needing several hops of
reasoning or simulated consequences, arithmetic, counting, dates. That is System
Two work — keep it in the agent, or in code. A single judgment with nothing at
stake is also cheaper to just answer.

## Requirements

The `evaluate` binary installed and a `TYPESAFE_API_KEY` exported; the plugin
ships the launcher only. Whatever goes in `state` leaves the machine. Both are
covered in the plugin `README.md`, and in `skills/ask-jev/references/setup.md`
for when the tool turns out to be missing mid-session.


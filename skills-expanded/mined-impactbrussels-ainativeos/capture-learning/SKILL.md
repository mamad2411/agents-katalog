---
name: capture-learning
description: Use when a real outcome just landed and the lesson should be banked so the OS stops repeating mistakes - an eval result, a customer reply, a metric move, a failed or won launch, a Share-of-Model move - when the founder says "we just learned", "that worked", "that failed", "log this", "note this for next time", "remember this", or after any real result. Appends a dated, sourced lesson to the right one of four KB files (PRINCIPLES, DOS-AND-DONTS, PLAYBOOK-LESSONS, MOATS-LEDGER); append, never overwrite. Skill before: a result that taught nothing and gets repeated. After: a dated sourced lesson the next founder inherits.
stage: cross-cutting
function: system
license: CC-BY-4.0
attribution: AI-Native OS by Adam M. Adamek (Impact Brussels ASBL)
---

# Capture Learning

The OS gets smarter only when real outcomes are banked. A skill that ran once and taught you nothing was a waste of the run; the same mistake made twice is the OS failing at its one job. This skill takes a thing that actually happened, an eval score, a customer reply, a number that moved, a launch that died, and writes it down as a dated, sourced lesson the next founder inherits. Append, never overwrite. Memory you can edit away is not memory.

## The method

Full append protocol, what is worth capturing, the file-routing table, a worked KB entry,
anti-patterns, and a copyable template: [`references/learning-loop-method.md`](references/learning-loop-method.md).

### Step 1 - Capture the real outcome
Write what happened, not what you hoped. The eval scored 0.71, not "the agent works well". The customer asked for a refund, not "mixed signal". A guess dressed as a result poisons the file for everyone downstream, so if you cannot point to the run, the reply, or the metric, you are not done capturing.

### Step 2 - Write the dated lesson
Use the `PLAYBOOK-LESSONS` format: a one-line lesson as the heading, then Context, What happened, Lesson, Source. State the lesson so the next founder avoids the mistake, not so you feel resolved about it.

### Step 3 - Append to the right file
Pick the home by shape of the learning:

| The learning is... | Append to |
|--------------------|-----------|
| A durable rule that should govern every design | `PRINCIPLES.md` |
| A concrete tactic, one move and its reason | `DOS-AND-DONTS.md` |
| A dated outcome from one real run or case | `PLAYBOOK-LESSONS.md` |
| Evidence about what compounds or what trust you earned | `MOATS-LEDGER.md` |

### Step 4 - Append, never overwrite
Add below the existing entries. Past lessons stay even when later ones sharpen them; the record of being wrong is itself the lesson.

## Output

- One logged lesson, dated and sourced, appended to the correct knowledge-base file.

## Constraints

- Append, never overwrite. The history is the asset.
- A real outcome, not a guess. No run, reply, or metric means nothing to bank yet.
- Stay theme-agnostic; the lesson must read true for a founder in any sector.

## Dictionary

[the learning loop](../../dictionary/07-ai-native-business.md#data-flywheel) ·
[a demo is not evidence](../../dictionary/05-failure-modes.md#sycophancy)

## Copy-paste version

> For non-coders: paste into any chatbot (Claude.ai, ChatGPT, Gemini).

```
Act as my AI-native learning archivist. Here is a real outcome I just had: [WHAT HAPPENED - the
actual eval score, customer reply, metric move, or failure]. Stage it came from: [DOMAIN / stage].
1. Restate the outcome in plain fact, stripped of hope. If I gave you a hope, not a result, say so.
2. Write it as a dated lesson in this exact shape:
   ### [today's date] - [one-line lesson]
   Context: what I was attempting.
   What happened: the real outcome.
   Lesson: the durable takeaway, written so the next founder avoids my mistake.
   Source: where this came from.
3. Tell me which file to append it to: a durable rule (PRINCIPLES), a tactic (DOS-AND-DONTS), a dated
   outcome (PLAYBOOK-LESSONS), or moat evidence (MOATS-LEDGER).
Append it below what's already there. Never overwrite an older lesson.
```

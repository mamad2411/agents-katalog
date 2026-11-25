---
name: distill-need
description: >-
  Use whenever someone is trying to understand something (a PR, feedback, a
  design, a long thread) or asks for something that may be a proposed solution:
  distill the real need before answering or building.
---
> Adapted from [AdirD/agent-shell-hamelech: melech-distill-need](https://github.com/AdirD/agent-shell-hamelech/tree/main/skills/melech-distill-need).
> Copyright (c) 2026 AdirD.
> Licensed under the MIT License: https://github.com/AdirD/agent-shell-hamelech/blob/main/LICENSE

# Distill need

The request or the thing they are trying to understand is not scripture. It is often a **proposed solution**, a dense explanation, or a big PR. Naive AI bullseyes the words. Your job is to **distill the need**, then offer paths that hit the outcome, which may look nothing like the named ask.

Classic pattern:

- Ask: "I need a faster horse."
- Distill: get to B faster.
- Better means: a car, or walk, if work is ten feet away.

## What you are trying to achieve

Separate:

1. **Literal ask / surface**: the named feature, tool, PR gap, or explanation they are stuck on
2. **Actual need / goal**: what must be true for them to be happy or to *get* it
3. **Context**: constraints that can collapse or change the problem
4. **Better means**: including reuse, process change, or don't-build

Then let the **user decide**. Surface the distillation; do not silently swap in your preferred solution.

## When to run

- The user says they are trying to understand something (feedback, a PR, a design, a chat thread)
- Someone asks for a feature, tool, or architecture that may be a proposed solution
- A long explanation failed and the blocker is still "what is the real point"
- Before building or reviewing a large change when the outcome is unclear

If the stuck point is a failed mental model after a correct explanation, prefer `make-it-click` after (or instead of) this. `distill-need` finds the *outcome*; `make-it-click` replaces the failed model.

## Workflow

### 1. Catch the proposed solution / surface

Restate the literal ask or the thing under discussion in one line. Mark it as a proposed solution or surface reading, not the mission.

### 2. Distill the outcome

Ask the smallest set of questions that reveal:

- what must be true when this is done
- why they want it now / why this feedback matters
- what pain happens if nothing changes

Prefer 1-3 high-leverage questions. Batch when forks are clear. Do not run a long intake.

### 3. Check collapsing context

Look for facts that change the category of solution:

- constraints, proximity, frequency, urgency, scale
- who feels the pain
- what "done" means in their world

If context is missing and would change the answer, ask for it. If you can infer safely from the repo or product, say the assumption.

### 4. Check existing solutions

Before inventing:

- is there already a wheel in the codebase, product, or process
- are they reinventing it
- if a known library, tool, or service may already do it, flag it

Prefer integrate / reuse / configure over greenfield when it hits the need.

### 5. Offer solution categories

Give 1-3 meaningfully different means to the same outcome. At least consider:

- **don't build** / manual / process / existing tool
- **smallest change** to something that already exists
- **the named ask** (or a cleaned version), if it still earns its place

For each path: outcome fit, cost, what you sacrifice, and when you'd choose it. Recommend one. User picks.

### 6. Hand off

- If the need dies or "walk" wins, stop. No plan, no code.
- If still build-shaped, align the concept and pick the smallest useful path.
- If they only needed holes poked, pressure-test that direction instead.
- If they needed to *understand*, lead with the distilled outcome in plain words, then the 1-3 paths.

## Question filter

Ask only what would change: the outcome definition, the solution category, whether building is justified, or whether something existing already solves it.

Do not ask implementation trivia. Do not invent requirements theater. This intercept can end with **don't build**.

## Do / Don't

**Do:** "You asked for a faster horse. Outcome seems to be: get to work faster. You live 10 feet away, so walking beats breeding."

**Don't:** Start designing a horse-optimization service.

**Do:** "Literal ask: custom RBAC engine. Distilled need: hide admin screens from non-admins. Role check on two routes may be enough. Confirm before we invent a policy framework."

**Don't:** Treat the named architecture as sacred. Recommend, then wait for the user to choose. Never silently replace their ask and start coding.

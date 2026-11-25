---
name: plan
description: Iterative deep planning with critiques and alternatives. Use when facing complex design decisions, architecture choices, or implementation strategies that require thorough analysis. Trigger for any request involving "how should I design", "what's the best approach", "help me plan", "architecture decision", "trade-offs between", or when a user is choosing between multiple technical approaches. Also trigger when a proposed plan needs critique or when the stakes of a wrong decision are high. Prefer this skill over a one-shot answer whenever the problem has meaningful complexity, multiple valid approaches, or non-obvious failure modes.
allowed-tools: Read, Glob, Grep, WebSearch
---

# Replan

Iterative design planning: plan → critique → refine. Repeat until robust.

---

## Step 0: Calibrate scope

Before starting, assess complexity:

| Signal                                          | Iterations |
| ----------------------------------------------- | ---------- |
| Small change, low reversibility risk            | 1–2        |
| New component, moderate coupling                | 2–3        |
| System-wide change, high coupling, irreversible | 3+         |

State your calibration explicitly: _"This looks like a 2-iteration problem because..."_

If unclear, ask one scoping question before proceeding.

---

## Step 1: Understand & Frame

- Read relevant code, docs, constraints
- State assumptions explicitly
- Frame the **core tension** — what is this design fundamentally trading off? (e.g., "consistency vs availability", "flexibility vs simplicity", "speed now vs maintainability later")

---

## Step 2: Initial Plan

Design your first approach. Include:

- Key decisions made and why
- What this plan optimises for
- What it deliberately sacrifices

---

## Step 3: Critique (run every iteration)

For each iteration, work through **all four lenses**:

### 🔴 Failure modes

- What breaks first under load or scale?
- What's the hardest scenario to test?
- What assumption, if wrong, invalidates the whole plan?
- What would you regret in 6 months?

### 🟡 Complexity audit

- What's the most "hand-wavy" part — where did you assume without verifying?
- Where does accidental complexity sneak in (over-engineering, premature abstraction)?
- What requires the most context to understand?

### 🟠 Coupling & cohesion

- What breaks if requirements change 20%?
- Is this testable in isolation? If not, why not?
- Where are the hidden dependencies?

### 🔵 Reversibility

- What decisions are hard to undo?
- Is there a cheaper way to validate the risky assumptions first?

---

## Step 4: Alternatives

Generate 2–3 alternatives. Each must directly address the critique from Step 3 — not just be stylistically different.

For each option:

### Option [X]: [Name]

[1–2 sentence description]

**Optimises for:** [specific axis — simplicity, reversibility, performance, etc.]
**Sacrifices:** [what it gives up]
**Kills which risk:** [which critique item from Step 3 this resolves]
**Pros:** ...
**Cons:** ...
**Risks:** ...

---

## Step 5: Select & develop best alternative

Pick the option that best balances:

1. Resolves the highest-severity critique item
2. Most reversible if wrong
3. Simplest to test

State selection reasoning explicitly. Then develop it fully.

---

## Step 6: Iterate

Repeat Steps 3–5 for the planned number of iterations (from Step 0).

After each iteration, pause and ask the user:

- Does this feel right, or is there a constraint I'm missing?
- Is there a decision here you want to make together?

---

## Step 7: Final Plan

Synthesise the best features across all iterations. Structure:

1. **Decision summary** — key choices made and why
2. **What this plan assumes** — explicit assumptions
3. **What would invalidate this plan** — top 2–3 failure conditions to watch for
4. **Implementation order** — what to build/validate first
5. **Open questions** — things still worth investigating

---

## Guidelines

- Kent Beck's Simple Design rules are a useful north star: passes tests → reveals intent → no duplication → fewest elements
- Honesty over confidence: say "I don't know how X works here, I'd need to check" rather than assuming
- For novel libraries or APIs: flag uncertainty and recommend a spike/prototype before committing
- Prefer reversible decisions over optimal-but-irreversible ones under uncertainty

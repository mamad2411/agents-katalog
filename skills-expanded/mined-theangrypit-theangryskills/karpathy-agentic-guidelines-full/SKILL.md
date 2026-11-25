---
name: karpathy-agentic-guidelines-full
description: Full Karpathy-inspired agentic coding guidance. Use when writing, reviewing, or delegating code and you need stricter control over assumptions, autonomy, verification, and context.
---

# Karpathy Agentic Guidelines - Full

## Overview

This is a stricter, workflow-aware version of the common Karpathy coding guidance.

It assumes the current reality Andrej Karpathy described in January 2026: we increasingly program in English, ask agents to perform large code actions, and get huge leverage from their stamina and loopiness. The win is real, but so are the failure modes: bad assumptions, overcomplication, sycophancy, unrelated edits, dead code, and subtle conceptual mistakes.

Core principle: use agents for generation and iteration, but keep human authority over intent, truth, review, and release decisions.

## When to Use

Use when:
- the task is big enough that agent loops are useful
- the model could silently make wrong assumptions
- success can be defined more clearly than the implementation path
- you care about keeping the codebase understandable after the change
- you are delegating or running multiple sessions and need stable control surfaces

Do not use when:
- the task is trivial and faster to do directly
- the work is pure exploration with no meaningful verification surface yet
- the main problem is missing product direction rather than execution quality

## Operating Model

### 1. Program in Outcomes, Not Keystrokes

Do not over-specify the path unless the path itself matters.

Prefer:
- success criteria
- invariants
- boundaries
- explicit non-goals

Good:
- "Reproduce the bug with a test, fix it, and keep adjacent lifecycle behavior unchanged."
- "Start with the naive correct version, then optimize only if correctness remains proved."

Bad:
- "Create three helper classes, then a config layer, then a wrapper, then..."

If the agent can loop, give it something crisp to loop toward.

### 2. Make Assumptions Expensive

The most common failure mode is not syntax. It is confident drift.

Require the agent to:
- surface assumptions that matter
- name unclear inputs
- call out conflicting evidence
- push back when the requested shape looks riskier than a simpler one

If multiple interpretations exist, do not silently choose one unless the tradeoff is clearly reversible and low-risk.

### 3. Keep a Human Review Surface Open

Agents generate. Humans discriminate.

For any code you care about:
- keep an IDE, diff, or file review surface open
- inspect the changed files directly
- verify that every changed line traces back to the request
- review for conceptual mistakes, not just compiler/test success

Do not treat "it ran" as proof. The dangerous failures are often coherent-looking but wrong.

### 4. Prefer Lightweight Planning Over Blind Momentum

The model should not disappear into a thousand-line construction without checkpoints.

Use:
- a short plan for multi-step work
- explicit verification after each meaningful step
- bounded task slices
- fresh context windows or separate sessions when tasks split naturally

The plan should be lightweight inline scaffolding, not ceremony.

### Decision Mode

Choose the lightest execution mode that preserves clarity and verification:

- direct execution
  - use for small, local, low-risk changes with an obvious verification path
- declarative plan
  - use when success criteria are clear but the exact path is better left to agent iteration
- task-sliced plan
  - use when the work spans multiple files or verification surfaces and needs stable checkpoints
- supervised delegation
  - use when tasks can be isolated, handed off cleanly, and reviewed by a controller without losing truth or scope control

Do not default to maximum ceremony or maximum autonomy. Pick the smallest mode that keeps the work legible.

### Defaults Beat Menus

When multiple approaches could work:
- pick a default
- explain why it is the default
- mention alternatives only as escape hatches
- if the task provides an exact output contract, required headings, or a fixed schema, reproduce it literally

Prefer:
- "Use `direct execution` here because the path is obvious."
- "Use `task-sliced plan` here because checkpoints and verification surfaces matter."

Avoid open-ended menus that make the agent sound flexible but less decisive.
Do not silently "improve" a required output format.

### 5. Default to the Simplest Construction That Works

Agents tend to bloat:
- abstractions
- APIs
- indirection
- fallback paths
- helper layers

Bias hard toward:
- direct code
- local reasoning
- fewer moving parts
- the naive correct version first

If 100 lines can be 20, reduce it.
If a helper is single-use, inline it.
If a config surface was not requested, do not invent it.

### 6. Treat Unrelated Edits as Regressions

Agents often "tidy" code they dislike or do not fully understand.

Do not allow:
- unrelated refactors
- comment churn
- style churn
- removal of orthogonal code
- deletion of pre-existing dead code unless requested

Clean up only what your change made unnecessary.

### 7. Use Tests and Tools as Loop Anchors

Karpathy's key leverage point is that agents are good at looping until they meet specific goals.

Exploit that by giving them anchors:
- failing tests
- reproducible bug cases
- browser or runtime checks
- explicit output contracts
- diff constraints

Prefer:
- "write the failing test first, then make it pass"
- "run the browser flow until this visible condition holds"
- "preserve correctness while optimizing"

### 7.5. Freeze the Harness, Narrow the Editable Surface

For exploratory or optimization-heavy work, make the search space smaller before giving the agent stamina.

Prefer:
- one primary editable surface when possible
- a frozen harness or fixed evaluation harness
- a fixed measuring stick
- a stable metric
- explicit "do not modify" boundaries

Examples:
- one target file instead of five loosely coupled files
- fixed benchmark, test, or reviewer script
- fixed acceptance metric while ideas vary

If the agent can change both the implementation and the measuring stick, you lose trustworthy progress.
When describing the loop, say explicitly that the evaluator is the frozen harness and the fixed measuring stick.

### 7.6. Establish a Baseline Before Iterating

The first useful run is often the untouched baseline.

Before trying improvements:
- run the current version
- measure and record the baseline current version
- capture the metric and important constraints
- make sure later changes are compared against something real

Do not start optimization from vibes. Start from a measured baseline.

### 7.7. Use a Keep-or-Discard Loop

When the work is experimental, every iteration should end with a decision:
- keep
- discard
- escalate because the signal is ambiguous

That decision should be based on:
- the metric
- correctness
- complexity cost
- collateral risk

If the result is worse, or equal but meaningfully more complex, bias toward discard.
If the result is slightly better but much simpler, bias toward keep.

### 8. Control Autonomy, Do Not Worship It

More autonomy is not automatically better.

Use bounded autonomy:
- scoped tasks
- explicit authority boundaries
- visible verification
- clear escalation points

Do not let any session become:
- a hidden planning authority
- a hidden truth source
- a hidden fallback lane
- a hidden release decision-maker

Agents can work hard. They should not become sovereign.

### Authority Map

Keep this division explicit:

- the agent may:
  - generate code
  - run bounded checks
  - iterate toward declared success criteria
  - surface tradeoffs, blockers, and possible simplifications
- the supervising human or controller keeps authority over:
  - intent

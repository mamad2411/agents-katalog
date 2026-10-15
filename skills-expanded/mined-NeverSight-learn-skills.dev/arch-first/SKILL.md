---
name: arch-first
version: 1.0.0
description: >-
  Full system design, trade-off analysis, and risk review before any
  implementation plan. No MVP shortcuts. Use for architecture, system design,
  module decomposition, multi-solution comparison, or scalability planning.
  /arch-first
---

# Arch-First — Design Before You Build

Default assumption: the user wants a **well-reasoned holistic design**, not
"here's a quick minimal version, we'll iterate later." Your role is
**architect** — see the full picture before discussing implementation.

## Before / After

**Without this skill:**
> User: "Add a notification system to our app."
> Agent: "Here's a quick implementation: add a `notify()` function that sends
> emails..." (No module breakdown, no alternatives considered, no failure modes.)

**With this skill:**
> Agent: Restates the problem in system terms → maps the full architecture
> (delivery channels, user preferences, queue, retry, templates) → identifies
> risks (delivery failure, rate limiting, spam) → compares two approaches
> (push-based vs pull-based) with trade-off table → recommends one with
> justification → phases the implementation aligned to the architecture.

---

## Core Rules

1. **No "minimal viable" first.** Unless the user explicitly asks for MVP-only, the first priority is understanding where the problem sits in the system: boundaries, modules, and dependencies.
2. **Design before execution.** A "phased plan" may only appear **after** architecture, risks, and alternatives have been laid out.
3. **Layered thinking.** Organize by architectural layers (context & constraints, core domain, interfaces, data, cross-cutting concerns, operational evolution) — not just a list of functions.
4. **At least two alternatives.** Never recommend only one approach without explaining why the others were rejected.
5. **Gaps must be explicit.** Before making a recommendation, list **known gaps and open questions**. Never pretend the analysis is complete when it isn't.

---

## When to Compress

- User explicitly says "just MVP / fastest way to get it working": give the minimal implementation, but still append one paragraph on "how to layer this properly if it grows."
- Narrow, self-contained question: answer directly, optionally add "if this goes into a larger system, watch out for…"

---

## Workflow (7 Steps)

### 1. Reframe the Problem
- Restate using **system-level** language: who it serves, success criteria, what is explicitly out of scope.
- Distinguish "what the user literally asked" from "what the system actually needs to solve."

### 2. Full Architecture
- **Blueprint:** modules, responsibility boundaries, data flow and control flow, internal and external dependencies.
- Mark **hard constraints** (performance, cost, security, etc.) and **soft preferences**.
- **Scale-up** (optional): requirements → high-level data flow → deep-dive on critical components → trade-offs and evolution path; include **order-of-magnitude estimates** on key metrics. Skip this if scale is not a concern.

### 3. Risks and Gaps
- **Hidden risks:** scale, consistency, security, single points of failure, operational burden.
- **Edge cases:** sudden spikes, partial failures, data corruption, rollback scenarios.
- Where information is insufficient, **list it separately** rather than filling the gap with vague statements.

### 4. Multi-Alternative Comparison
- ≥ 2 substantively different approaches.
- **Trade-off table:** pros / cons / when each fits / cost and complexity.

### 5. Recommendation with Justification
- Pick one primary recommendation (or an evolution path).
- Argue: **why this is the best fit** given current constraints; what is sacrificed; how to compensate later.

### 6. Phased Execution Plan (Only After the Above)
- Each phase has a **verifiable deliverable**, aligned with the architectural modules.
- Not "build a demo instead of designing" — rather, **ordered slices of a decided architecture**.
- If resources are limited, state what can be cut and the **architectural consequences** of cutting it.

### 7. Self-Check

| Check | If No → Action |
|-------|----------------|
| Did I skip straight to MVP? | Return to step 2 |
| Does the architecture cover data, interfaces, failure modes, and evolution? | Add missing sections |
| At least two alternatives compared with a justified pick? | Add comparison |
| Does the execution plan depend on the architecture above, not a separate ad-hoc plan? | Realign |

**Architecture health score** (optional): self-rate 0–10 + one sentence on the weakest point. Below 7 → add detail or flag explicitly as a risk.

---

## Anti-Patterns

- Jumping to "three lines of code solve this" with no module or data flow thinking.
- "Start with MVP, iterate later" as a substitute for architectural reasoning.
- Ignoring cross-cutting concerns (scalability, observability, permissions, data consistency).
- Self-check says "nothing missing" but lists no open questions — complex systems almost always have unresolved points.
- Alternative comparison that concludes "both are fine" with no decision criteria.

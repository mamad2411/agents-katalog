---
name: dsn-design-critique
version: 1.0.0
description: Give structured, actionable design feedback on a screen or flow - usability, visual hierarchy, and consistency - anchored to user goals and heuristics rather than taste.
author: matrixx0070
tags: [design, critique, usability, heuristics, review, hierarchy]
capabilities: []
---

# Design Critique

## When to use
Use this when a designer wants feedback before handoff, when a flow "feels off" but no one can name why, or when you need a review that separates real problems from personal preference. Works on a single screen, a full flow, or a component.

**Not for:** WCAG conformance (use dsn-accessibility-review), writing the interface words (use dsn-ux-copy), or greenlighting a direction — critique surfaces issues, it does not approve.

## Method
1. **Anchor to intent.** State the user's goal and the primary action for this screen. Every finding is judged against that goal, not your taste. *Decision:* if the goal is unstated and unguessable, ask before critiquing — a critique without intent is just opinion.
2. **Hierarchy.** Name what the eye hits first, second, third. Does that order match importance? Flag competing focal points, weak primary CTAs, content buried below the fold.
3. **Usability heuristics.** Walk Nielsen's ten (status, real-world match, user control, consistency, error prevention, recognition over recall, flexibility, minimalism, error recovery, help). Name the heuristic each issue violates.
4. **Consistency.** Check spacing, type scale, color roles, component variants, and terminology against the rest of the product. Note one-offs that should reuse an existing pattern.
5. **Separate signal from taste.** Mark each item Blocker / Improvement / Nit. *Decision:* if you cannot tie it to a goal or heuristic, it is a Nit — label it as opinion or drop it.
6. **Lead with what works** so strengths survive the next iteration.

## Example
Checkout screen, goal "complete payment". **What works:** clear order summary. **Blocker** — the gray "Continue" and gray "Cancel" have equal weight (heuristic: user control / visibility) — make Continue the single filled primary, Cancel a text link. **Nit** — I'd prefer more whitespace above the total (taste).

## Pitfalls
- Critiquing without stating the user goal — feedback drifts into preference.
- Listing problems with no suggested fix, leaving the designer stuck.
- Dumping 30 flat findings; unranked feedback is unactionable — always tier them.
- Dressing up taste ("I don't like this blue") as a usability problem.

## Output format
```
# Critique: <screen> — goal: <user goal>
**What works:** ...
**Blockers (breaks the task):** issue — heuristic — suggested fix
**Improvements:** issue — heuristic — suggested fix
**Nits (taste, optional):** ...
```
Every finding gets a concrete suggestion, not just a complaint.

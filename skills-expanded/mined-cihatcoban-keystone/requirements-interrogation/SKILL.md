---
name: requirements-interrogation
description: Extracts what someone actually needs before anything is built, one question at a time. Triggers - build me an admin dashboard (or any X), interview me about what I need, stress-test my thinking, vague request, are we sure about this, grill me.
---

# Requirements Interrogation

People ask for the solution they can imagine, not the one they need. "Build a
dashboard" is a guess about how to answer a question they haven't stated. The
cheapest moment to find that gap is before a line exists; afterwards, sunk cost
rationalizes the wrong thing into "good enough".

## When to use

- The request names an artifact but not an outcome ("a report", "an admin panel")
- Success has no definition, or the definition is an adjective
- The work is expensive or hard to reverse
- You catch yourself silently filling in a blank
- Someone says "just make it like X"

**When not to use:** the request is small, clear and cheap to redo; or an
explicit decision has already been recorded in a spec or ADR. Do not
re-interrogate a settled question.

## Method

One question at a time. A list of eight questions gets eight shallow answers;
one question gets a real one, and the answer redirects the next question.
Stop when you can state the problem, the user, the constraint and the success
signal back in one paragraph and the person agrees.

## Question ladder

Work down. Do not skip to the bottom.

| Level | Question | What it exposes |
|---|---|---|
| Outcome | "What becomes possible when this exists that isn't possible now?" | Whether the artifact is the point |
| Actor | "Who does this, how often, and what do they do today instead?" | The real workflow, and whether a workaround already works |
| Trigger | "Why now? What changed?" | Urgency, and the deadline nobody mentioned |
| Signal | "Six weeks after launch, what number tells us it worked?" | Whether success is measurable at all |
| Boundary | "What's explicitly *not* part of this?" | Scope, before it creeps |
| Failure | "What happens if this is wrong or down for a day?" | Reliability requirements — usually far lower or far higher than assumed |
| Volume | "How much data, how many users, how fast does it grow?" | Whether the simple design survives |
| Constraint | "What can't change? Budget, deadline, systems we must keep" | The real design space |
| Prior art | "Has anyone tried this? What happened?" | Buried history that saves weeks |

## Sharp probes

- **The five-whys on the artifact**: "Why a dashboard?" → "To see order status."
  → "Why?" → "Because support gets asked." Often ends at a notification, not a
  dashboard.
- **The inverse**: "What would make you cancel this project?"
- **The cheapest version**: "If you could only have 10% of this, which 10%?"
  Their answer is the actual requirement; the rest is ambition.
- **The manual test**: "Could one person do this by hand for a week?" If yes,
  do that first — it produces the ground truth an automated system needs.
- **The disagreement probe**: "Who would object to this, and what would they say?"

## Handling the "just build it" response

Some people experience questions as obstruction. Do not abandon the method;
compress it. Ask the two that change the design most — *outcome* and
*boundary* — then state your assumptions explicitly and start:

> "Building X with these assumptions: A, B, C. If any is wrong, tell me now —
> changing them later costs a rewrite of the Y part."

Written assumptions turn a silent guess into a visible one. That is the goal.

## Output

A short brief, not a transcript:

```markdown
## Problem
Who cannot do what, and what it costs them today.

## Success signal
The observable number or event that says it worked.

## Scope
In: ... / Out (deliberately): ...

## Constraints
Hard limits: deadline, systems, budget, compliance.

## Assumptions
Unverified things I am proceeding on; each one's blast radius if wrong.

## Open questions
Unanswered, with who can answer and by when.
```

This brief feeds `spec-driven-development`. Do not write the spec here.

## Exit checklist

- [ ] The outcome is stated as a capability, not an artifact
- [ ] Success has a number or an observable event
- [ ] The "out of scope" list is non-empty
- [ ] Every assumption is written down with its consequence if wrong
- [ ] The person has confirmed your one-paragraph restatement
- [ ] If questions were cut short, the assumptions section says so

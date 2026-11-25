---
name: first-principles-mode
description: first-principles-mode skill for assumption deconstruction and problem reframing. Use when a developer's proposed solution appears to be cargo-culted, overengineered, or built on unexamined assumptions. Activates on "everyone does it this way", "the standard approach is", "I assumed we needed X", or when a solution's complexity is disproportionate to the stated problem.
---

# first-principles-mode

## Purpose

Deconstruct every assumption beneath a proposed approach before allowing any forward progress — guide the human to reason from the actual constraints of the problem rather than inherited conventions, never propose an alternative approach or solution.

## Hard Refusals

- **Never propose an alternative approach** — the goal is to clear the ground, not to build on it. Building is the human's job.
- **Never confirm that an assumption is valid** — even if you believe it is. Confirmation short-circuits the reasoning.
- **Never let "everyone does it this way" stand as a justification.** Convention is not a first principle.
- **Never accept complexity as a given** — always ask what the complexity is solving.
- **Never move to solution exploration until all assumptions have been named and tested.**

## Triggers

- "The standard way to do this is..."
- "I assumed we'd need [pattern/technology/layer]"
- "Everyone uses [X] for this kind of problem"
- "We need [complex solution] because [vague reason]"
- Any proposed solution whose complexity seems disproportionate to the problem description

## Workflow

### 1. State the actual problem

Before examining the proposed solution, get the raw problem.

| AI Asks | Purpose |
|---------|---------|
| "Forget the solution for a moment — what is the actual problem you are trying to solve?" | Strips away the solution frame |
| "Who has this problem? How often? What happens if it's not solved?" | Establishes problem severity and frequency |
| "How do you know this is the problem? What evidence do you have?" | Tests whether the problem itself is well-defined |

**Gate 1:** Human has stated the problem independently of the solution, with evidence that it is real.

Memory note: Record the stripped problem statement in `SKILL_MEMORY.md`.

### 2. List every assumption in the proposed approach

Ask the human to enumerate — not defend — every assumption their approach rests on.

| AI Asks | Purpose |
|---------|---------|
| "List the things that have to be true for your approach to be the right one." | Surfaces implicit assumptions |
| "What would have to change about the world for your approach to be obviously wrong?" | Forces falsifiability |
| "Which parts of this approach could you remove if you had to, without breaking the core?" | Identifies necessary vs. assumed components |

**Gate 2:** Human has listed at least four assumptions. Do not proceed with fewer — shallow assumption lists mean the deconstruction isn't done.

### 3. Test each assumption against the actual problem

For each assumption the human lists, ask the one question that most directly challenges it:

```text
Assumption: "We need a queue because the load will be high"
→ "What is the actual expected load? What evidence supports that number?"

Assumption: "This needs to be a microservice"
→ "What specific property of a microservice does this problem require? Could a module boundary provide the same property?"

Assumption: "We need a cache here"
→ "What is the cost of recomputing the thing you'd cache? Have you measured it?"

Assumption: "We should use [industry standard pattern]"
→ "What problem was that pattern designed to solve? Is that the problem you have?"
```

**Gate 3:** Every assumption has been questioned. The human has either provided evidence for it or acknowledged it as unverified.

### 4. Identify what remains after deconstruction

| AI Asks | Purpose |
|---------|---------|
| "Of your assumptions, which ones have evidence? Which are guesses?" | Separates verified from speculative |
| "If you strip out every assumption that is unverified, what does the minimum viable solution look like?" | Finds the irreducible core |
| "What is the simplest thing that could possibly work for the actual problem you stated?" | First-principles anchor question |

**Gate 4:** Human has identified the minimum viable approach given only verified assumptions.

### 5. Decision point

```text
Did deconstruction reveal the original approach was well-founded?
├── Yes → "You've justified [N] assumptions with evidence. You can proceed with confidence.
│           What's your first step?"
└── No  → "You've identified [N] unverified assumptions. What do you want to do with that?"
```

Do not suggest what to do with the unverified assumptions. That is the human's judgment call.

## Deviation Protocol

If the human says "I don't have time for this, just tell me if my approach is right":

1. **Acknowledge**: "I hear that time is a constraint."
2. **Assess**: Ask "Which assumption in your approach are you most uncertain about?" — the shortcut is to focus first-principles questioning on the one assumption most likely to invalidate the approach.
3. **Guide forward**: Run the single most important assumption through steps 3-4 only. Gate the session to the highest-risk assumption if time is genuinely constrained.

## Related skills

- `skills/core-inversions/architect-interrogator` — when first-principles deconstruction leads to an architecture decision
- `skills/cognitive-forcing/complexity-cop` — when the deconstruction reveals over-engineering specifically
- `skills/cognitive-forcing/devils-advocate-mode` — when the human needs sustained pressure rather than one-time deconstruction

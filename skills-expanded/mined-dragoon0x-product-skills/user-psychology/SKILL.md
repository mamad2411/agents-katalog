---
name: user-psychology
description: "Apply motivation, friction, and trust patterns to product decisions. Maps cognitive biases and behavioral triggers to specific UI and copy choices. Use when reviewing flows for drop-off points or when something feels right but doesn't convert."
---

# User Psychology

Apply motivation, friction, and trust patterns to product decisions.

## How to use

- `/user-psychology` Apply behavioral constraints to this conversation.

## Constraints

### Motivation Patterns
- People act when the perceived benefit exceeds the perceived effort
- Reduce effort before increasing benefit (it's more effective)
- Loss aversion: people fear losing what they have more than gaining something new
- Social proof works because uncertainty triggers conformity
- Progress indicators motivate completion (the closer to done, the more motivated)

### Friction Mapping
- Map every step in a flow. Each step is a potential exit point.
- For each step: what effort is required, and what value does the user receive?
- MUST reduce steps between intent and completion
- SHOULD front-load value and back-load commitment
- NEVER add friction for "engagement" purposes (dark pattern)

### Trust Patterns
- Trust is built incrementally: small commitments before large ones
- Transparency about pricing, data usage, and limitations builds trust
- Admitting weaknesses builds more trust than claiming perfection
- MUST match expectations set in marketing with the actual product experience
- Broken trust is 10x harder to rebuild than to maintain

### Cognitive Load
- MUST limit choices per screen (5-7 options max without grouping)
- SHOULD use progressive disclosure instead of showing everything at once
- Familiar patterns reduce cognitive load (don't reinvent standard UI conventions)
- NEVER rely on user memory between screens (show context, don't assume it)

### Anti-Patterns
- Using psychological principles to manipulate rather than assist
- Dark patterns: hidden costs, trick questions, forced continuity, misdirection
- Artificial scarcity without real scarcity
- Guilt-based retention ("Are you sure? You'll lose everything!")
- Exploiting anxiety or FOMO for engagement

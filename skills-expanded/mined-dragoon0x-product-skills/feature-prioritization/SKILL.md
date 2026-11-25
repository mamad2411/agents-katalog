---
name: feature-prioritization
description: "Decide what to build next based on impact, not excitement. Applies scoring frameworks to feature backlogs. Use when scope is unclear, when the agent is about to build everything at once, or when deciding what ships in v1 vs v2."
---

# Feature Prioritization

Decide what to build next based on impact, not excitement.

## How to use

- `/feature-prioritization` Apply prioritization constraints to feature decisions in this conversation.
- `/feature-prioritization <features>` Score and rank a set of features.

## Constraints

### Scoring Framework
- MUST evaluate each feature against: reach (how many users), impact (how much it changes behavior), confidence (how sure are we), effort (how long to build)
- MUST produce a ranked list, not a tier system. Force hard choices.
- NEVER give two features the same priority. If they feel equal, dig deeper.
- SHOULD separate "must-have for launch" from "nice to have" from "later"

### Decision Rules
- If a feature serves <10% of users, it probably doesn't belong in v1
- If you can't explain why a feature matters in one sentence, cut it
- If a feature requires another feature to make sense, they ship together or not at all
- Technical debt reduction is a feature. Prioritize it honestly.
- NEVER build for hypothetical scale. Build for current users first.

### Scope Protection
- MUST define a scope ceiling before starting
- Every addition requires a subtraction
- "We'll add it later" is a valid and honest answer
- SHOULD track deferred features with clear criteria for when they become relevant

### Anti-Patterns
- Building the feature the loudest user requested
- Prioritizing based on ease of implementation rather than user impact
- Adding features to match a competitor's checklist
- Building infrastructure for scale you haven't reached
- Saying yes to everything and shipping nothing

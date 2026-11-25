---
name: feedback-synthesis
description: "Turn raw user feedback into actionable product decisions. Categorization frameworks, signal vs noise filtering, and severity scoring. Use when processing interviews, support tickets, or reviews into product direction."
---

# Feedback Synthesis

Turn raw user feedback into actionable product decisions.

## How to use

- `/feedback-synthesis` Apply feedback processing constraints to this conversation.

## Constraints

### Categorization
- Feature requests: what they want but don't have
- Pain points: what they have but doesn't work well
- Praise: what works and should be protected
- Confusion: what exists but isn't understood
- MUST separate the problem from the user's proposed solution

### Signal vs. Noise
- Volume of requests matters less than intensity of need
- 10 people mentioning something casually < 2 people who can't use the product without it
- MUST weight feedback by user segment (power users, new users, churned users)
- Churned user feedback is often the most valuable and least collected
- NEVER treat all feedback as equally important

### Processing Rules
- MUST identify the underlying need behind every request
- "I want a dark mode" might mean "the screen hurts my eyes" or "I want customization"
- MUST track feedback frequency AND severity separately
- SHOULD map feedback to existing product goals before treating it as new scope
- NEVER promise a feature to a user based on unprocessed feedback

### Anti-Patterns
- Building what the loudest user asked for
- Treating every support ticket as a feature request
- Surveying without a hypothesis
- Collecting feedback with no system for processing it
- Ignoring feedback that contradicts your roadmap

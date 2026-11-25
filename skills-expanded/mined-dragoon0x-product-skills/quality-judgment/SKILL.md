---
name: quality-judgment
description: "Know when something is good enough to ship and when it needs more work. Covers quality bars, the difference between polish and perfection, and making the ship-or-hold decision. Use when debating whether to ship, setting quality standards for the team, or when quality is inconsistent across releases."
---

# Quality Judgment

Know when to ship and when to hold — the line between done and good enough.

## How to use

- `/quality-judgment` Apply quality judgment constraints to this conversation.
- `/quality-judgment <feature>` Evaluate whether the described feature is ready to ship.

## Constraints

### Quality Bar Definition
- MUST define the quality bar before building, not during the ship decision
- Quality bars SHOULD vary by context: a v1 prototype has a different bar than a billing flow
- Core flows (signup, payment, core action) MUST have a higher quality bar than secondary features
- MUST distinguish between "works correctly" and "works well" — both matter differently
- NEVER let the quality bar be implicit. Write it down.

### Ship Decision Framework
Ask these questions:
- Does it solve the core user problem? If not, don't ship.
- Are there bugs that would cause data loss, security issues, or broken workflows? If yes, don't ship.
- Will the user understand how to use it without explanation? If not, fix onboarding.
- Would you be comfortable if a journalist wrote about this experience? If not, polish more.
- Is the remaining work polish or substance? Polish can come later. Substance can't.

### Good Enough vs. Perfect
- MUST ship when the core value works, even if edges are rough
- SHOULD use progressive quality: ship the core, then polish in fast follow-ups
- MUST know the difference between "we'll fix it later" that actually happens and the kind that doesn't
- NEVER hold a ship for cosmetic issues when users are waiting for the core functionality
- NEVER ship known broken experiences in core flows just to hit a date

### Quality Consistency
- MUST maintain consistent quality across the product. One polished feature next to a broken one erodes trust.
- SHOULD establish quality rituals: bug bashes, dogfooding sessions, regular QA passes
- MUST track quality debt alongside tech debt — both compound over time
- NEVER ignore quality regression because the new feature is exciting

### Anti-Patterns
- Perfectionism: holding indefinitely for polish while competitors ship
- The Shippable Minimum: shipping something so bare it damages the product's reputation
- Quality by Accident: no standards, so quality depends on who built it
- The Big Reveal: months of building with no user feedback until launch day
- Regression Blindness: shipping new features while existing ones quietly degrade

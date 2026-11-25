---
name: ux-intuition
description: "Develop the instinct for what makes a product feel right, beyond what data can tell you. Covers quality evaluation, interaction judgment, and knowing when something is off even if you can't articulate why. Use when evaluating designs, reviewing prototypes, or when metrics say it's fine but something feels wrong."
---

# UX Intuition

Know what feels right in a product before the data tells you.

## How to use

- `/ux-intuition` Apply UX intuition constraints to this conversation.
- `/ux-intuition <product or flow>` Evaluate the user experience of the described product or flow.

## Constraints

### The Feel Test
- MUST use the product as a real user would before evaluating it — not as someone who built it
- SHOULD ask: does this feel fast? Does it feel predictable? Does it feel respectful of my time?
- MUST notice moments of confusion, hesitation, or friction — these are signals even when small
- NEVER dismiss "it feels off" without investigating. Intuition often catches what metrics miss.
- SHOULD test on real devices and real network conditions, not just dev machines

### Interaction Judgment
- Every interaction MUST have clear feedback — the user should always know what happened
- MUST evaluate: can a user figure out what to do without instructions?
- SHOULD check state transitions: loading, empty, error, success. Each one is a user experience.
- NEVER accept "it works" as sufficient. Working and feeling good are different things.
- MUST consider edge cases the happy path ignores: first-time users, power users, error recovery

### Simplicity Standard
- MUST ask: can anything be removed without losing value?
- SHOULD count the number of decisions the user has to make. Fewer is almost always better.
- MUST ensure the primary action on every screen is obvious
- NEVER add a feature without asking how it affects the experience of existing features
- Complexity should be progressive — simple by default, powerful when needed

### Taste vs. Data
- MUST distinguish between personal taste and product judgment
- When intuition and data conflict, investigate — don't automatically defer to either
- SHOULD build conviction through exposure: use lots of products, notice what works
- MUST be able to articulate WHY something feels off, not just that it does
- NEVER override design decisions based on personal preference alone

### Anti-Patterns
- Metric-Only Evaluation: if the numbers are fine, the experience must be fine (wrong)
- Feature Blindness: so familiar with the product that you can't see confusion points
- Taste Tyranny: overriding design because you personally don't like the font
- Happy Path Only: evaluating the best case and ignoring error states and edge cases
- Pixel Perfectionism: obsessing over visual polish while core interactions are confusing

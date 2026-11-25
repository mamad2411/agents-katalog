---
name: market-validation
description: "Test assumptions before committing resources. Generates lean validation plans, fake door tests, and interview scripts. Use before building anything expensive or when there's no evidence anyone wants what's being built."
---

# Market Validation

Test assumptions before committing resources.

## How to use

- `/market-validation` Apply validation-first constraints to this conversation.
- `/market-validation <idea>` Generate a validation plan for the described idea.

## Constraints

### Assumption Mapping
- MUST list the top 3 assumptions that would kill the product if wrong
- MUST rank assumptions by risk: which one, if false, makes everything else irrelevant
- MUST design a test for the highest-risk assumption first
- NEVER build until the highest-risk assumption has some evidence behind it

### Validation Methods (ordered by speed and cost)
1. Talk to 5 people who have the problem. Just listen.
2. Search for existing solutions and read their reviews. What's missing?
3. Build a landing page that describes the product. Measure interest.
4. Create a fake door: a button that says "coming soon" to measure demand
5. Build the smallest possible thing that tests the core assumption

### Interview Framework
- Ask about past behavior, not future intent ("Tell me about the last time..." not "Would you use...")
- NEVER ask "Would you pay for this?" Ask "How do you solve this today and what does it cost you?"
- MUST listen for emotion. Mild interest is not validation. Frustration is.
- SHOULD identify the moment they switched from an old solution to their current one. What triggered it?

### Signal vs. Noise
- "That's cool" is not validation. "When can I use this?" is closer.
- Email signups are weak signals. Credit card on waitlist is strong.
- 100 lukewarm responses < 10 people who desperately need this
- MUST define what "validated" looks like before running the test

### Anti-Patterns
- Survey-based validation (people lie in surveys, even to themselves)
- Asking friends and family (they'll say what you want to hear)
- Treating a pitch deck as validation
- Building first, validating later
- Validating the easy assumption instead of the risky one

---
name: zero-to-one
description: "First principles decisions for products that don't exist yet. Helps reason about market gaps, user needs, MVP scope, and what to build first. Use when starting from scratch, scoping an MVP, or when the agent needs to think before it builds."
---

# Zero to One

First principles decisions for products that don't exist yet.

## How to use

- `/zero-to-one` Apply 0-to-1 thinking constraints to this conversation.
- `/zero-to-one <idea>` Evaluate an idea through first principles.

## Constraints

### Before Building Anything
- MUST articulate the problem before proposing a solution
- MUST identify who has this problem and how they solve it today
- MUST answer: why now? What changed that makes this possible or necessary?
- NEVER start with a solution and work backward to find a problem
- NEVER scope features before validating the core assumption

### MVP Definition
- MVP means the minimum thing that tests the core assumption, not a smaller version of the full product
- MUST identify the one thing the product needs to do well to survive
- SHOULD cut scope aggressively: if removing a feature doesn't kill the core value, remove it
- NEVER include admin panels, settings pages, or preference systems in v1 unless they ARE the product
- MUST define what "working" looks like before writing code

### Decision Framework
- For every feature: does this test our core assumption or is it nice-to-have?
- For every design choice: what's the fastest way to learn if this matters?
- For every technical choice: what's the simplest thing that could possibly work?
- Premature optimization of anything (code, design, copy, infrastructure) is the enemy of learning

### Risk Assessment
- Identify the biggest assumption that could kill this product
- Design the fastest way to test that assumption
- If the assumption is wrong, know this before building, not after

### Anti-Patterns
- Building for 6 months in stealth before talking to a single user
- Choosing tech stack based on scale requirements you don't have yet
- Designing for edge cases before handling the main case
- Treating the MVP like a demo instead of a real product people use
- Adding "just one more feature" before launching

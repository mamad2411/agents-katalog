---
name: service-boundaries
description: Define correct service boundaries. Use when deciding what belongs
  in each service or module.
metadata:
  tags: service, boundaries
---

# Service Boundaries

## Use this skill when
- Deciding what goes into each service or module
- Finding misaligned boundaries causing coupling
- Evaluating ownership conflicts between teams

## Do not use this skill when
- The boundaries are already good
- You need boundary enforcement in code (use clean-architecture)

## Instructions
1. Start from business capabilities, not technical layers.
2. Let each boundary own its data exclusively.
3. Co-locate things that change together; split things that scale or deploy independently.
4. Use bounded contexts to reconcile differing models.
5. Protect boundaries with contracts and tests.
6. Document ownership and the rationale for each boundary.

## Output Format
- Boundary | Owner | Owned data | Contracts | Change drivers

## Common Mistakes
- Boundaries around technical layers (all databases together)
- Ignoring Conway’s Law and team structure
- Sharing data across boundaries without a contract

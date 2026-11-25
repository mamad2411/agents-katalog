---
name: architecture-review
description: Architecture review skill for evaluating codebase design, module boundaries, coupling, test seams, domain language, and simplification opportunities. Use when the user asks to improve architecture, zoom out, reduce complexity, untangle code, or review a design.
---

# Architecture Review

Use this skill to reason about structure before proposing broad changes.

## Workflow

1. Map the system
   - Identify the relevant modules, entry points, data flow, and ownership boundaries.
   - Read local docs, domain glossary, ADRs, and tests if present.

2. Locate design pressure
   - Look for repeated conditionals, hidden coupling, unclear ownership, duplicated concepts, awkward test seams, and high-change files.
   - Distinguish annoying code from code that blocks future work.

3. Name the domain concepts
   - Use existing project language when available.
   - Flag mismatches where code names do not match business or product concepts.

4. Propose changes
   - Prefer small boundary improvements over sweeping rewrites.
   - Give options when tradeoffs are meaningful.
   - Identify the first reversible step.

5. Validate
   - Explain what tests or probes would prove the architecture change preserved behavior.
   - Avoid recommending refactors without a verification path.

## Output Format

```text
Current Shape
What the code is doing now.

Pressure Points
Specific issues with file references.

Recommended Move
The smallest valuable design improvement.

Validation
How to prove the change is safe.
```

## Rules

- Do not propose a rewrite unless incremental steps are impossible.
- Do not introduce abstractions just because two blocks look similar.
- Prefer deeper modules with simple interfaces over shallow layers that move complexity around.

---
applyTo: "**/*"
---

When working in this repository, optimize for reproducible report fidelity rather than generic document generation.

Always:

- identify the approved report artifact before proposing fixes
- extract explicit structural facts from the approved artifact before proposing implementation changes
- distinguish between data issues and formatting issues
- recommend the minimum effective fix layer
- preserve one canonical report model across outputs when possible
- verify merges, headers, notes, totals, section order, typography, and page behavior explicitly

Do not:

- assume preview output proves export fidelity
- ask AI to imitate a reference report without first writing down the format specification
- publish protected reference forms or real datasets
- describe the workflow in vague terms without acceptance criteria

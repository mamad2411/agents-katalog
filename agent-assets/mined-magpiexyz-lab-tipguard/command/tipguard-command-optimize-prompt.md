---
description: "Optimize a prompt using Claude best practices. Standalone utility — not part of the experiment lifecycle."
type: utility
reads: []
stack_categories: []
requires_approval: false
references: []
branch_prefix: chore
modifies_specs: false
---
Improve the following prompt to a world-champion level. Apply Claude prompt best practices, ensuring clarity, precision, strong role definition, explicit constraints, and minimal ambiguity, while preserving the original intent.

Guidelines:
- Use a clear system/role framing if applicable
- Add explicit output format constraints
- Include edge case handling where relevant
- Use structured sections (context, task, constraints, output format) when beneficial
- Prefer concrete examples over abstract descriptions
- Remove vague or redundant language
- Preserve the user's core goal and tone

Return the optimized prompt in a fenced code block so it can be copied directly.

Prompt to optimize:

$ARGUMENTS

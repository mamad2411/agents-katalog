---
name: ddd-verify
description: >
  Compare finished code against requirements and applicable official docs,
  research unexplained discrepancies, correct authorized changes, and run
  affected checks. Use for verification or review of an implementation.
license: MIT
compatibility: Install together with sibling skills ddd, ddd-scope, ddd-ground, and ddd-verify; the main procedure is referenced at ../ddd/SKILL.md.
metadata:
  author: ddd-methodology
  version: "0.8.0"
---

# Compare code with documentation

Load the `ddd` skill completely, through your native skill tool when you have one, otherwise by reading
[DDD](../ddd/SKILL.md), and apply **Compare the actual result**, using its
inspection/research steps to find the existing task note and refresh missing or
stale context. That skill owns the procedure and persistent-note rules.

For review-only work, report findings without editing application code or application documentation. For an
authorized fix, research unexplained discrepancies, correct them, and rerun
checks. Save the comparison and actual results in the same note, naming its path.
Relevant mismatches or unsupported consequential assumptions prevent a clean
completion claim. No assurance case or CLI verdict is required.

Consult [citation comparison](references/citation-entailment.md) or
[execution checks](references/test-traceability.md) when needed.

Compare affected application explanations with final code and checks; continue
independent comparisons around blocked parts while reporting a partial result.

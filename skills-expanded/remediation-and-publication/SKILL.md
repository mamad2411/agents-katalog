---
name: remediation-and-publication
description: Turn blocking and material findings into owned remediation actions, bind a human decision to the exact draft, and verify the published package.
tools: [build_remediation_plan, verify_report_package]
---

# Remediation and publication

## When to use

Use this procedure when a review has blocking or material findings and may ultimately create a durable report artifact.

## Steps

1. Build one action for every blocking or material finding with `build_remediation_plan`.
2. Require an owner role, a due date, and the evidence needed to close each action.
3. Draft without claiming approval or publication.
4. Bind the exact draft digest, action name, thread ID, and blocking findings into the human interrupt.
5. If rejected, record the terminal rejection and do not publish or promote the path.
6. If approved, publish once through the operation ledger.
7. Run `verify_report_package`; capture the workflow as successful only if all host checks pass.

## Promotion rule

After the same verified path recurs and has more successes than failures, distil its parameterised steps into a new SHA-versioned `SKILL.md`. Mark the raw recipe promoted so it no longer competes for retrieval attention.

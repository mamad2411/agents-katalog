---
name: n8n-validation-expert
description: Interpret validation errors and guide fixing them. Use when encountering validation errors, validation warnings, false positives, operator structure issues, or need help understanding validation results. Also use when asking about validation profiles, error types, or the validation loop process.
---

# n8n Validation Expert

Use this skill to interpret n8n validation output, choose the right validation profile, fix errors safely, handle false positives, and guide the validation loop to a deployable workflow.

## Invocation Triggers

- Validation errors, warnings, suggestions, or confusing validation output.
- Questions about `validate_node`, `validate_workflow`, `n8n_validate_workflow`, or `n8n_autofix_workflow`.
- Operator structure issues, false positives, profile choice, broken connections, or workflow-level validation failures.

## Core Philosophy

- Validate early and often.
- Treat validation as an iterative loop, not a one-shot check.
- Fix errors before warnings; review warnings case-by-case; suggestions are optional.
- Read the `fix` field when present; it often contains the remediation.
- Never assume success without checking `result.valid`.

## Severity Routing

| Severity | Blocks activation? | Action |
|---|---|---|
| Errors | Yes | Always fix before deploying |
| Warnings | No | Review; fix for production unless intentionally accepted |
| Suggestions | No | Optional improvements |

Common error types: `missing_required`, `invalid_value`, `type_mismatch`, `invalid_expression`, and `invalid_reference`.

See [error-catalog.md](references/error-catalog.md) and [ERROR_CATALOG.md](ERROR_CATALOG.md) for detailed examples.

## Validation Loop

1. Configure or modify one node/workflow section.
2. Validate with the appropriate profile.
3. Read errors completely.
4. Fix one class of issue at a time.
5. Validate again.
6. Repeat until `valid: true`.
7. Review warnings and document accepted false positives.

Multiple cycles are normal. See [validation-workflow.md](references/validation-workflow.md) for the full walkthrough.

## Profile Routing

| Profile | Use When |
|---|---|
| `minimal` | Quick checks during editing |
| `runtime` | Default pre-deployment validation |
| `ai-friendly` | AI-generated configs with noisy false positives |
| `strict` | Production, critical workflows, security-sensitive automation |

## Auto-Sanitization and Auto-Fix Gates

- Auto-sanitization runs automatically on every workflow save; do not fight it manually.
- It fixes known operator-structure and IF/Switch metadata issues.
- Broken connections, branch-count mismatches, and corrupt states still need manual recovery.
- `n8n_autofix_workflow` is opt-in: preview first with `applyFixes: false`.
- Apply only high-confidence fixes automatically; review medium/low confidence changes.
- Inspect `postUpdateGuidance` after auto-fix.

See [auto-fix-patterns.md](references/auto-fix-patterns.md) for full safety boundaries.

## False Positives

- Do not blanket-suppress warnings.
- Use `profile: "ai-friendly"` for LLM-generated configs when warnings are noisy.
- Document accepted false positives in workflow notes so reviewers do not keep re-fixing them.
- Hardcoded credential warnings are never acceptable.

See [troubleshooting.md](references/troubleshooting.md) and [FALSE_POSITIVES.md](FALSE_POSITIVES.md) for detailed acceptance criteria.

## Workflow-Level Validation

Use workflow validation when checking:

- Node configurations.
- Connections and broken references.
- Expression syntax and references.
- Logical flow, circular dependencies, multiple start nodes, or disconnected nodes.

Use recovery strategies such as minimal rebuild, binary search, `cleanStaleConnections`, or previewed auto-fix depending on failure type.

## Output Expectations

Return:

- Diagnosed errors with severity, type, property, and fix.
- Recommended next action and fix order.
- Profile recommendation.
- Auto-fix preview/apply guidance when relevant.
- False-positive acceptance reasoning when warnings are intentionally accepted.
- Validation status and remaining risks before deployment.

## Reference Map

| Need | Read |
|---|---|
| Full validation loop, profile detail, result shape | [validation-workflow.md](references/validation-workflow.md) |
| Error types and before/after examples | [error-catalog.md](references/error-catalog.md), [ERROR_CATALOG.md](ERROR_CATALOG.md) |
| Auto-sanitization and auto-fix safety matrix | [auto-fix-patterns.md](references/auto-fix-patterns.md) |
| False positives, recovery, best practices, debugging | [troubleshooting.md](references/troubleshooting.md), [FALSE_POSITIVES.md](FALSE_POSITIVES.md) |
| End-to-end validation scenarios | [examples.md](references/examples.md) |

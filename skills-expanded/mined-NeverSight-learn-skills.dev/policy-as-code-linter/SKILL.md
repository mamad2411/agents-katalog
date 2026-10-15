---
name: policy-as-code-linter
description: Vendor-neutral skill for linting simple policy-as-code rules (YAML) for style, safety, and completeness.
---

## When to invoke
- Your org stores lightweight access/control policies as code (e.g., allow/deny rules).
- You want a quick lint pass to catch missing fields, invalid enums, overly-broad principals, or risky wildcards.
- You need vendor-neutral checks before deploying to any policy engine.

## Inputs needed
- Path to a YAML policy file containing a list of rules.
- (Optional) Output path for a JSON report.

## Workflow
1. Load YAML and validate top-level shape (list of rules).
2. For each rule, validate required fields:
   - `id`, `effect` (allow|deny), `actions` (list), `resources` (list)
3. Run safety checks:
   - flag wildcard principals (`*`, `all`, `everyone`)
   - flag wildcard actions/resources (`*`) especially in allow rules
   - detect duplicate rule IDs
4. Run style checks:
   - enforce kebab-case IDs
   - recommend `description` field
5. Emit findings with severity levels.

## Output format
- JSON report:
  - `errors`: blocking issues
  - `warnings`: risky patterns
  - `info`: non-blocking recommendations
  - `summary`: counts
- Human-readable table to stdout.

## Guardrails
- Do not claim policy correctness for any specific cloud/IAM provider.
- Treat output as guidance; human review required for security-sensitive decisions.

## Reference code
- `policy_as_code_linter.py`

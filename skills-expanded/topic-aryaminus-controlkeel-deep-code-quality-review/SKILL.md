---
name: deep-code-quality-review
description: "Strict maintainability review: abstraction quality, file size, spaghetti growth, code-judo simplification. Trigger: 'deep quality review', 'thermo-nuclear review', 'harsh maintainability audit'."
when_to_use: "Activate ONLY when explicitly asked for a harsh code quality review. Do NOT auto-trigger during normal coding or security reviews."
argument-hint: "[file, PR, branch, or area]"
disable-model-invocation: true
license: Apache-2.0
compatibility:
  - opencode-native
  - claude-standalone
  - cursor-native
  - codex
metadata:
  author: controlkeel
  version: "1.1"
  category: quality
  ck_mcp_tools: [ck_validate, ck_finding, ck_git_diff, ck_review_submit]
  related_skills: [security-review, parallel-review]
---

# Deep Code Quality Review

Extremely strict maintainability review. Be **ambitious** about structure — search for "code judo" moves that make the implementation dramatically simpler.

## Do NOT use when
- Security review needed (use `security-review`)
- Normal code review or PR feedback
- Making behavior changes

## Standards (non-negotiable)

1. **File size**: Flag files crossing 1000 lines → `ck_finding` rule `code_quality.file_size` (severity `high`).
2. **No spaghetti**: Flag ad-hoc conditionals in unrelated flows → rule `code_quality.spaghetti_condition`.
3. **Design over "it works"**: If structure can be cleaner with same behavior, push for cleaner.
4. **Direct over magical**: Flag thin wrappers, identity functions, pass-through helpers → rule `code_quality.unnecessary_abstraction`.
5. **Type boundaries**: Flag unnecessary casts, optionality, ad-hoc shapes → rule `code_quality.type_boundary`.
6. **Canonical layer**: Flag feature logic in shared paths → rule `code_quality.wrong_layer`.
7. **Orchestration**: Flag sequential when parallel is simpler → rule `code_quality.orchestration`.

Additional rules: `code_quality.missing_abstraction`, `code_quality.magic_handling`, `code_quality.duplicate_logic`.

## Workflow

1. Run `ck_git_diff` to get changes. Run `ck_validate` for automated patterns.
2. Walk [quality checklist](references/quality-checklist.md) against every meaningful change.
3. Record each issue with `ck_finding` using the rule IDs above.
4. Submit findings via `ck_review_submit` (review_type: `plan`). Wait for approval.

## Approval bar

No approval unless: no structural regression, no missed simplification, no file explosion, no spaghetti growth, no unnecessary abstraction, no layer leak, no missed decomposition.

## Relationship to security-review

- **security-review**: OWASP, injection, auth, secrets, dependencies
- **this skill**: abstraction quality, file size, spaghetti, layering, simplification
- Use `parallel-review` to run both concurrently.

## Output

- `ck_finding` records with specific rule IDs
- `ck_review_submit` plan with prioritized findings
- No code changes — review only

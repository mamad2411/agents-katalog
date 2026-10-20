---
description: Internal review checklist to run before considering substantial work complete
globs:
alwaysApply: true
---

# Internal Code Review

Before calling substantial work done (new feature, page, screen, API route, refactor), review your own diff against this list. Fix what you find before finishing. Skip for trivial edits.

## Architecture
- Is it maintainable and placed where the codebase expects it?
- Any unnecessary complexity, abstraction, or new dependency?
- Any duplicated logic that already exists elsewhere?
- Did I touch anything unrelated to the task?

## Security (`03-security.mdc`)
- Can a malicious user bypass a control, change a price, or access another user's data?
- Are secrets exposed (client bundle, logs, responses, commits)?
- Is all input validated server-side?
- Is authorization enforced server-side?
- Could errors leak stack traces, internals, or PII?

## Performance (`04-performance.mdc`)
- Unnecessary or duplicate API requests?
- Efficient queries (no N+1, indexed, paginated)?
- Large resources loaded where not needed?
- Avoidable re-renders or rebuilds?

## UX (`02-frontend-quality.mdc`)
- Does the flow make sense end to end?
- Are loading, empty, error, success states present and useful?
- Responsive on small and large screens?

## Design (`01-design-system.mdc`, `10-design-rules.mdc`, `20-copy-rules.mdc`)
- Does it look generic or AI-generated?
- Is typography intentional?
- Are colors from tokens and coherent in every theme?
- Consistent spacing and hierarchy?
- Are cards, shadows, gradients, or rounded corners overused?
- Any fake metrics, testimonials, or banned copy words?

## Accessibility (`05-accessibility.mdc`)
- Fully keyboard operable with visible focus?
- Every control labelled?
- Contrast sufficient?
- Reduced motion respected?

## Verification (`06-testing.mdc`)
- Lint, type-check, build and tests pass?
- Negative tests added for security-sensitive logic?
- Report honestly what was verified and what was not.

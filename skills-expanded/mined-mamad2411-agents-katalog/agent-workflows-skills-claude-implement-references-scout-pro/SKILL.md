# Scout Prompt Template

Use this when dispatching a read-only scout subagent near the start of `/implement`.

## Recommended Agent Type

- `Explore` for read-only codebase mapping

## Required Inputs

- `{SPEC_SUMMARY}` — concise summary of the approved spec
- `{AC_OR_QA_FOCUS}` — the acceptance criteria or QA concerns that most shape the implementation
- `{WORKDIR}` — repo path

## Template

```text
You are scouting the codebase for an approved feature implementation.
Do not modify files.

Work from: `{WORKDIR}`

## Spec Summary

{SPEC_SUMMARY}

## Important Acceptance Criteria / QA Focus

{AC_OR_QA_FOCUS}

## Your Job

Read only the minimum code and project context needed to help the controller plan the first implementation slices.

Return:
1. likely files or modules to change,
2. existing patterns or analogous features to follow,
3. likely verification commands or test files,
4. major integration risks or ambiguities,
5. a suggested decomposition into the next 1-3 implementation slices.

Keep the output concise and implementation-oriented.
Do not propose speculative architecture changes unless the spec clearly requires them.
```

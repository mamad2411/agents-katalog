---
name: code-review
description: Review the implementation for style, security, and best practices.
compatibility: Requires bash, Claude Code
metadata:
  team: software-development
  role: reviewer
  version: "1.0"
---

## Procedure

1. **Discover project rules** — follow the Project Rules Discovery procedure from the team PROTOCOL. Read lint config and coding guidelines before reviewing.
2. **Run the linter** — execute the project's lint command. Every lint error is a Critical finding.
3. **Review against project rules** — check for style, security, and adherence to the project's actual standards (not generic best practices).
4. **Report findings** back to the developer with file:line references.
5. **Iterate** until all Critical issues are resolved and lint is clean.

## Gotchas

- Refer to `references/checklist.md` for the security and style checklist.
- Review against the project's own rules first, generic best practices second.
- Lint errors are always Critical — do not approve code with lint errors.

## Validation loop

The reviewer ensures that all flagged issues have been resolved, lint is clean, and no regressions have been introduced during the review cycle.

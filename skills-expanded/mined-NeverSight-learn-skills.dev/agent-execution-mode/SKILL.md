---
name: agent-execution-mode
description: Enforces disciplined execution, implementation tracking, design validation, code review rigor, and final reporting for production work, architecture, and review tasks. Use when work must be complete, verified, and documented instead of approximate or partial.
license: Apache-2.0
metadata:
  author: Mike Willbanks
  repository: https://github.com/mwillbanks/agent-skills
  homepage: https://github.com/mwillbanks/agent-skills
  bugs: https://github.com/mwillbanks/agent-skills/issues
---

# Agent Execution Mode

Use this skill whenever the user expects real completion: implementation, hardening, architecture, design alignment, review, documentation repair, or production-grade delivery.

This skill exists to stop the failure modes that make agent work untrustworthy: partial completion, fake confidence, visual-only validation, stale docs, missing tests, missing review artifacts, and missing execution state.

## When to use

Activate this skill when the request involves any of the following:

- implementing or fixing behavior that should be complete when returned
- hardening an existing implementation after regressions, repeated failures, or correctness gaps
- architecture or system design work that needs explicit decisions and durable documentation
- code review, PR review, or self-review that must produce a reliable artifact
- design-driven work where implementation must be checked against a specification or screenshot
- final reporting for substantial work

Default to `production` unless the user clearly requests another mode.

## Modes

Supported modes:

- `production`
- `hardening`
- `agentic-self-review`
- `general-review`
- `pr-review`
- `prototype`
- `design`
- `architecture`

Mode intent:

- `production`: complete implementation, repo-native patterns, tests and docs updated where needed. After completion is stated, run `agentic-self-review` before concluding.
- `hardening`: everything in `production`, plus stronger regression scrutiny, edge-case repair, and validation. After completion is stated, run `agentic-self-review` before concluding.
- `agentic-self-review`: apply the review standard in [references/REVIEW_INSTRUCTIONS.md](references/REVIEW_INSTRUCTIONS.md), fix obvious safe issues directly, and do not create a review artifact unless explicitly requested.
- `general-review`: produce a review artifact using [assets/TEMPLATE_REVIEW.md](assets/TEMPLATE_REVIEW.md) and the standard in [references/REVIEW_INSTRUCTIONS.md](references/REVIEW_INSTRUCTIONS.md).
- `pr-review`: requires a PR link, uses GitHub MCP to inspect intent and diff, records the review in [assets/TEMPLATE_PR_REVIEW.md](assets/TEMPLATE_PR_REVIEW.md), and submits inline feedback plus a summary review state through GitHub MCP.
- `prototype`: reduced polish is allowed only when explicitly requested; fake production claims are forbidden. After completion is stated, run `agentic-self-review` before concluding.
- `design`: design-focused work only. Use Figma MCP when a design specification exists; otherwise use screenshots or equivalent visual references. Do not claim runtime completeness unless it was actually implemented. After completion is stated, run `agentic-self-review` before concluding.
- `architecture`: produce durable system decisions, reusable structure, and implementation when feasible. After completion is stated, run `agentic-self-review` before concluding.

`recommendation-review` is removed. Use `general-review` or `pr-review` instead.

## Non-negotiable behavior

- Do not return a partial implementation as complete work.
- Do not stop at visual parity when behavior, state handling, contracts, documentation, or architecture are part of correctness.
- Do not leave TODOs, placeholders, mock production paths, or knowingly incomplete required work in production paths.
- Do not ignore repository-native abstractions when reusable boundaries already exist.
- Do not skip tests, validation, or docs when the change materially requires them.
- Do not claim completion if obvious QA failures, accessibility failures, or contract gaps remain in scope.
- Do not use review language that hides severity or uncertainty.

## Execution workflow

Follow this sequence unless the request explicitly narrows scope:

1. Identify the mode and create or update the task state when the work is implementation-oriented or substantial.
2. Gather the minimum context needed to stop guessing.
3. Implement or review with repository-native patterns.
4. Validate behavior, design, and affected workflows.
5. Update review and report artifacts when the mode requires them.
6. Update documentation when behavior, contracts, architecture, or operational usage changed.
7. State completion only when the implementation or design work is actually complete.
8. For `production`, `hardening`, `prototype`, `design`, and `architecture`, immediately run `agentic-self-review` after that completion statement and fix safe issues before concluding.
9. Finish only after the post-completion self-review is complete.

Detailed workflow rules live in [references/WORKFLOWS.md](references/WORKFLOWS.md).

## Tracking requirements

For implementation-oriented work, keep task tracking under `.agents/tasks/`.

Required files:

- `.agents/tasks/TASK_INDEX.md`
- `.agents/tasks/TASK_ID.md`

Rules:

- `TASK_INDEX.md` is a prepended markdown table. Newest rows go directly under the header.
- Required columns: `ID`, `Name`, `Description`, `Mode`, `Status`, `Thread IDs`, `Created At`, `Updated At`.
- `ID` is auto-generated, semantic, unique, lowercase, and hyphen-separated.
- Both `ID` and `Name` must link to `.agents/tasks/TASK_ID.md`.
- Each task file uses [assets/TEMPLATE_TASK_STATE.md](assets/TEMPLATE_TASK_STATE.md).
- Task frontmatter must include `id`, `name`, `short-description`, `thread-ids`, `created-at`, `updated-at`, and `state`.
- The markdown body title must be `# TASK_ID - TASK_NAME`.
- All timestamps must be UTC.

Use [assets/TEMPLATE_TASK_INDEX.md](assets/TEMPLATE_TASK_INDEX.md) for the index shape.

## Review requirements

For review work, keep review artifacts under `.agents/reviews/`.

Required files:

- `.agents/reviews/REVIEW_INDEX.md`
- `.agents/reviews/REVIEW_ID.md`

Rules:

- `REVIEW_INDEX.md` is a prepended markdown table. Newest rows go directly under the header.
- Required columns: `ID`, `Name`, `PR #`, `Description`, `Mode`, `Status`, `Count`, `Created At`, `Updated At`.
- `ID` is auto-generated, semantic, unique, lowercase, and hyphen-separated.
- Both `ID` and `Name` must link to `.agents/reviews/REVIEW_ID.md`.
- `PR #` links to the GitHub PR when the review is PR-backed; otherwise use `N/A`.
- Each review file uses [assets/TEMPLATE_REVIEW.md](assets/TEMPLATE_REVIEW.md) or [assets/TEMPLATE_PR_REVIEW.md](assets/TEMPLATE_PR_REVIEW.md).
- Review frontmatter must include `id`, `name`, `short-description`, `review-count`, `github-pr-number`, `github-pr-link`, `created-at`, `updated-at`, and `state`.
- The markdown body title must be `# REVIEW_ID - REVIEW_NAME`.
- When a second or later review occurs for the same item, mark which existing findings were resolved and place new findings at the top of the new iteration.
- `general-review`, `pr-review`, and `agentic-self-review` use the standard in [references/REVIEW_INSTRUCTIONS.md](references/REVIEW_INSTRUCTIONS.md).
- Reviews should also fold in the discipline from the `code-discipline` and `repo-standards-enforcement` skills when they are relevant to the code under review.

`pr-review` requirements:

- requires a PR link
- pull the PR diff and stated intent through GitHub MCP
- review the code against the PR intent, not just the diff mechanics
- record inline comment candidates, suggestions, and summary outcome in the markdown artifact
- use GitHub MCP to submit inline comments and the overall review state: `approved`, `changes-requested`, `comment`, or `rejected`
- on later review iterations, resolve or mark previously addressed findings before adding new ones

## Design and validation requirements

- `design` mode replaces the old `design-only` mode.
- When a Figma specification is available, use Figma MCP first.
- When Figma is not available, use screenshots or equivalent reference artifacts.
- For code changes with UI impact, validate both design and implementation using Playwright through the Docker MCP.
- Do not treat visual inspection alone as sufficient when interaction, state, or responsive behavior matters.

## Final report requirements

For substantial implementation, architecture, or multi-step review work, keep reports under `.agents/reports/`.

Required files:

- `.agents/reports/REPORT_INDEX.md`
- `.agents/reports/REPORT_ID.md`

Rules:

- `REPORT_INDEX.md` is a prepended markdown table. Newest rows go directly under the header.
- Recommended columns: `ID`, `Name`, `Description`, `Mode`, `Status`, `Created At`, `Updated At`.
- `ID` is auto-generated, semantic, unique, lowercase, and hyphen-separated.
- Both `ID` and `Name` link to `.agents/reports/REPORT_ID.md`.
- Each report file uses [assets/TEMPLATE_REPORT.md](assets/TEMPLATE_REPORT.md).
- Report frontmatter must include `id`, `name`, `short-description`, `mode`, `created-at`, `updated-at`, and `state`.
- Keep the latest run at the top of the report file.
- Do not delete prior run entries.

Use [assets/TEMPLATE_REPORT_INDEX.md](assets/TEMPLATE_REPORT_INDEX.md) for the index shape.

## Documentation policy

Documentation is mandatory when:

- existing documentation no longer matches behavior
- architecture or module boundaries changed
- a new component, workflow, or public contract was introduced
- operational usage or testing strategy materially changed

Update the smallest correct documentation surface. Do not leave stale docs behind.

## Mandatory self-review gate

Before concluding any task, verify all applicable items:

- completion claims match reality
- required states and edge cases were handled
- tests and validation were not skipped without cause
- docs were updated when needed
- review and report artifacts were updated when required by mode
- design and implementation were both validated when UI work was involved

For `production`, `hardening`, `prototype`, `design`, and `architecture`, this self-review gate is mandatory after completion has been stated. Do not skip it, compress it into a superficial pass, or treat earlier informal checking as a substitute.

If any answer is no, continue working or report the exact blocker.

## Templates and references

Templates:

- [assets/TEMPLATE_TASK_INDEX.md](assets/TEMPLATE_TASK_INDEX.md)
- [assets/TEMPLATE_TASK_STATE.md](assets/TEMPLATE_TASK_STATE.md)
- [assets/TEMPLATE_REVIEW_INDEX.md](assets/TEMPLATE_REVIEW_INDEX.md)
- [assets/TEMPLATE_REVIEW.md](assets/TEMPLATE_REVIEW.md)
- [assets/TEMPLATE_PR_REVIEW.md](assets/TEMPLATE_PR_REVIEW.md)
- [assets/TEMPLATE_REPORT_INDEX.md](assets/TEMPLATE_REPORT_INDEX.md)
- [assets/TEMPLATE_REPORT.md](assets/TEMPLATE_REPORT.md)

References:

- [references/WORKFLOWS.md](references/WORKFLOWS.md)
- [references/REVIEW_INSTRUCTIONS.md](references/REVIEW_INSTRUCTIONS.md)

Keep `SKILL.md` as the activation layer. Put deeper process rules in `references/` and reusable document shapes in `assets/`.

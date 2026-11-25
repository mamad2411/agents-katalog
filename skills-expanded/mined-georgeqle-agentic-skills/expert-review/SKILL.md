---
name: expert-review
description: Conduct a thorough project-wide code review as an expert panel, cross-referencing specs, changelogs, and design documents
type: review
version: v0.1
required_conventions: [alignment-page]
---

# Expert Review

Invoke as `$expert-review`.

Use this skill when the user wants a code review of the whole project or a specific path, with findings validated against project documentation.

## Process

1. Gather project context:
   - Read CLAUDE.md, README, and project config to understand conventions.
   - Search for and read specs (`specs/`, `spec.md`, `docs/`), changelogs (`CHANGELOG.md`, `tasks/history.md`), ADRs, interview logs (`*-__interview.md__`), and design docs.
   - Read `tasks/roadmap.md` if it exists to understand the full plan. Read `tasks/todo.md` for current phase and in-progress work. Read `tasks/manual-todo.md` (if it exists) for pending manual tasks. Read `tasks/record-todo.md` and `tasks/recurring-todo.md` (if they exist) for advisory context only.
   - Build a mental model of intentional decisions and documented trade-offs.
2. If the user provides a file or directory, scope the review there. Otherwise review the repository broadly.
3. Read enough of the codebase to understand the architecture before critiquing it.
4. Review against these dimensions:
   - Correctness
   - Security
   - Performance
   - Architecture
   - Error handling
   - Code quality
   - Testing
   - Dependency risks
   - Spec conformance — code that diverges from documented specs or design decisions
5. Cross-reference each finding against documentation before reporting:
   - If a pattern is an intentional documented decision, do not report it as an issue — list it under "Documented decisions" instead.
   - If code diverges from a spec, flag it as a spec conformance issue.
6. Verify findings (false-positive filter):
   - Re-read the actual source code for every finding. Confirm: the code behaves as claimed, the issue isn't handled elsewhere (guard clause, middleware, caller), flagged dependencies actually exist/are missing, and "missing" test coverage isn't in a different test file.
   - Drop any finding you cannot re-confirm on second read. If uncertain, downgrade to Low with a note that it needs manual verification.

## Output

Report findings grouped by severity:

- Critical: bugs, security issues, data-loss risks
- High: major performance, architecture, or error-handling problems
- Medium: maintainability or testing gaps with real impact
- Low: worthwhile improvements with limited risk
- Spec conformance: where code diverges from documented specs, with document reference
- Documented decisions (no action needed): patterns that look like issues but are intentional
- Positive observations: strong patterns worth preserving

## Follow-Through

After presenting findings, write Critical and High implementation fixes to `tasks/todo.md` under a `## Code Review Fixes` heading (append or replace existing section). One checkbox per finding with file:line and recommended fix. Do not add Medium/Low items. If a Critical/High observation is a non-blocking future validation or condition-gated measurement rather than a fix, write it to `tasks/record-todo.md` with source, condition, non-blocking reason, evidence, and promotion rule. Suggest `$exec` or `$investigate` to start fixing concrete work.

## Constraints

- Include concrete file and line references for each finding when possible.
- Every finding should include a specific recommended fix.
- Do not fill the review with style nitpicks.
- Never flag an intentional design decision as an issue. Respect documented trade-offs.
- If no project documentation exists, note the absence and recommend establishing specs or ADRs.


## Alignment Page

Follow the shared alignment-page convention via the packaged convention resolver; output path is `alignment/expert-review-{topic}.html`.

## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.

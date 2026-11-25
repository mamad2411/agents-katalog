---
name: tech-code-review-team
description: End-to-end code review workflow. Use when the user wants a complete code review package covering GitHub PR or git diff intake, strict bug/security/performance review, project coding standards, security auditing, clean-code maintainability checks, and structured Chinese review reports. Coordinates pr-reviewer, critical-code-reviewer, project-code-standard, security-audit, clean-code-review, and code-review-assistant.
metadata:
  short-description: Complete code review workflow
---

# Tech Code Review

Use this skill as the workflow entry point for a complete code review package. It coordinates the companion skills in this bundle instead of replacing them.

## Workflow

1. Use `pr-reviewer` to collect PR or git diff context, changed files, lint signals, test coverage hints, and initial risk level.
2. Use `critical-code-reviewer` to examine the changed code for bugs, edge cases, security holes, performance risks, type-safety gaps, and maintainability failures.
3. Use `project-code-standard` to check lint, formatting, naming, import order, file structure, and team conventions.
4. Use `security-audit` when changes touch authentication, authorization, credentials, dependencies, configuration, deployment, or input handling.
5. Use `clean-code-review` to evaluate code smells, anti-patterns, responsibility boundaries, readability, KISS/DRY/YAGNI, and refactoring opportunities.
6. Use `code-review-assistant` to assemble a structured Chinese review report with severity, evidence, file/line references where available, and actionable fixes.

## Routing

- If the user gives a GitHub PR URL or PR number, start with `pr-reviewer` when `gh` is available.
- If the user asks for a strict or adversarial review, use `critical-code-reviewer` early.
- If the request emphasizes lint, style, formatting, or team standards, use `project-code-standard`.
- If the request mentions credentials, auth, permissions, CVEs, deployment, or hardening, use `security-audit`.
- If the request asks whether the code is maintainable, readable, or clean, use `clean-code-review`.
- If the user wants a final review report in Chinese, use `code-review-assistant` for report assembly.

## Project-First Rules

When working in a local codebase:

1. Inspect the current git status and protect user changes before reading diffs or running tools.
2. Prefer the repository's real lint/test commands and established review conventions over generic advice.
3. Ground findings in code evidence: file path, line, behavior, risk, and a concrete fix.
4. Separate blocking bugs/security issues from style or maintainability suggestions.
5. Do not claim a PR is safe unless the relevant diff, tests, and risk areas were actually checked.

## Output Package

For a full code review package, produce:

1. PR or diff intake summary: changed files, scope, risk areas, and available test/lint evidence.
2. Findings list: grouped by severity with file/line references where possible.
3. Security audit notes: credentials, auth, dependency, input validation, and config risks.
4. Standards report: lint, formatting, naming, import order, and team convention gaps.
5. Clean-code assessment: maintainability risks, code smells, and refactoring suggestions.
6. Final Chinese review report: concise verdict, required fixes, suggestions, and verification notes.

## Operating Notes

- Keep review comments specific and actionable.
- Avoid style-only noise when a stronger correctness or security issue exists.
- Do not post comments to GitHub unless the user explicitly asks.
- If tooling is unavailable, state the verification limit and continue with source-based review.

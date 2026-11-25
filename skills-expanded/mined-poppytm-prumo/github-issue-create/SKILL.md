---
name: github-issue-create
description: Actionable bug reports, reproducible examples, structured feature requests, acceptance criteria, and gh issue create automation
---
# GitHub Issue Authoring & Specification

## 1. Clear & Searchable Issue Titling
Write concise, descriptive issue titles stating the core problem or capability clearly. Avoid vague titles like 'Bug in service' or 'Update code'.

## 2. Structured Bug Reports
Include environment details (OS, version, commit SHA), minimal reproduction steps, expected behavior, actual behavior, and relevant sanitized error logs.

## 3. Minimal Reproducible Example (MRE)
Provide the smallest possible code snippet, test case, or cURL command that reproduces the issue reliably without external proprietary dependencies.

## 4. Feature Requests with Measurable Value
Define feature issues with user stories, technical context, proposed architectural approach, and expected user or business impact.

## 5. Explicit Acceptance Criteria
List measurable, testable criteria as task checkboxes (- [ ]) that must be satisfied before the issue can be considered resolved.

## 6. Severity & Priority Classification
Label issues accurately according to impact: P0 (Critical/Blocker), P1 (High), P2 (Medium), P3 (Low/Enhancement).

## 7. Automated gh CLI Issue Creation
Create issues via CLI: gh issue create --title '[Bug]: Description' --body-file issue.md --label 'bug,triage' --assignee '@me'.

## 8. Sensitive Data Protection
Audit issue descriptions and attached log traces to guarantee zero exposure of API keys, tokens, customer PII, or internal hostnames.

## 9. Cross-Linking & Dependency Mapping
Reference related issues, pull requests, and architecture design records (ADRs) using GitHub keyword links (#123, blocked by #456).

## 10. Issue Lifecycle Grooming
Keep issues updated with investigation progress, updated reproduction notes, and close them promptly when resolved with a link to the resolving commit.

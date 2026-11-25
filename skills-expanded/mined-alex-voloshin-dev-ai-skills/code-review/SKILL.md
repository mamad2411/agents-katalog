---
name: code-review
description: Use this skill when reviewing a pull request, merge request, or code change before merge, conducting an architecture review, auditing code for security/performance/quality, or running a pre-merge quality gate — including when applied by a Reviewer or QA subagent — to produce a verdict (APPROVE / REQUEST_CHANGES / COMMENT) using Google's eng-practices framing (code health over perfection) and conventional comments vocabulary (nit / suggestion / issue / praise). Distinct from /security-scan (no dependency CVE scan) and /security-audit (no full OWASP audit).
---

<!-- ARCHITECTURAL NOTE: intentional model-invocable companion — deliberately no `context: fork` and no `disable-model-invocation`. This skill is applied by the Reviewer subagent (via `@code-review`) and other workflows; a forked body could not be applied inside a Reviewer/QA subagent, and disabling model-invocation would stop agents auto-loading it on review tasks. Not a defect — do not reclassify. -->

# Code Review

Systematic code review skill with layered checklists. Produces consistent, actionable feedback across all review types.

## When to Use

- Reviewing pull requests or merge requests
- Conducting architecture reviews
- Auditing code for security, performance, or quality
- Pre-merge quality gates

## When NOT to Use

- Writing new code (use `/feature-dev` or `/bugfix` instead)
- Validating plugin-shipped AI asset files (use `/plugin-doctor` for plugin self-diagnostic)
- Running automated checks before commit (use `/pre-commit`)

## Reviewer Principles

Adapted from [Google's eng-practices "The Standard of Code Review"](https://google.github.io/eng-practices/review/reviewer/standard.html). Primary purpose: **improve code health over time, not chase perfection**.

Apply at every review:

1. **Code health over time** — does this CL improve the codebase, even if not perfect? If yes, approve. Do not block on hypothetical future improvements.
2. **Technical facts override preferences** — opinion vs fact. If the reviewer prefers style A but the author wrote style B and both are valid, defer to the author. Disagreement on style without a documented standard is non-blocking.
3. **Forward progress vs importance of suggestions** — small improvements should not block merge unless they prevent code health from improving long-term. Convert non-blocking suggestions to follow-up issues.

Effectiveness ceilings (Microsoft Research on code review):

| Signal | Ceiling | Implication |
|---|---|---|
| Defect-finding rate | Plateaus past ~60-min sessions | Split large CLs |
| Throughput | ~200 LoC/hour | Push back on >400 LoC PRs |
| Reviewers | 1 sufficient for most CLs | Add a 2nd reviewer only for high-risk changes (auth, payments, schema, infra) |

## Review Process

### 0. Gather Context

Read `CLAUDE.md` (or `AGENTS.md`) at the project root to identify:
- Tech stack (determines which language-specific patterns to check)
- Code conventions (naming, structure, formatting rules)
- Architecture patterns in use (helps evaluate structural decisions)

### 1. Understand the Change

Before reviewing code, answer:
- **What** is being changed? (feature, bugfix, refactor, dependency update)
- **Why** is it being changed? (linked issue, PRD, bug report)
- **Scope**: How many files, which modules, what's the blast radius?

### 2. Apply Checklists

Use the appropriate checklist(s) based on change type:

| Change Type | Checklists to Apply |
|---|---|
| New feature | `review-checklist.md` + `security-checklist.md` |
| Bug fix | `review-checklist.md` (focus: root cause, regression test) |
| Refactor | `review-checklist.md` (focus: behavior preservation, tests) |
| API change | `review-checklist.md` + `security-checklist.md` |
| Infrastructure | `security-checklist.md` |
| Dependencies | `security-checklist.md` (focus: supply chain) |

### 3. Provide Feedback

Use [Conventional Comments](https://conventionalcomments.org) vocabulary so each comment signals intent. Format: `<label>[(decoration)]: <subject>`.

| Label | Use for | Blocks merge? |
|---|---|---|
| `praise:` | Positive feedback (research links praise to productivity — do not skip) | No |
| `nitpick:` / `nit:` | Minor / preference / style | No |
| `suggestion:` | Concrete change request | Sometimes |
| `issue:` | Problem requiring change before merge | Yes |
| `todo:` | Leftover work for a follow-up CL | No |
| `question:` | Clarification needed | Maybe |
| `thought:` | Speculative / tangential | No |
| `chore:` | Small task (e.g., update docs) | No |

Optional decoration: `(blocking)`, `(non-blocking)`, `(if-minor)`. Example:

```
issue (blocking): SQL query is concatenated, not parameterized — risk of injection.
nit (non-blocking): inconsistent naming — `userId` elsewhere, `user_id` here.
praise: nice extraction of the retry logic into a helper.
```

Verdict template:

```
## Review Summary

**Verdict**: APPROVE | REQUEST_CHANGES | COMMENT

### Blocking (issue / suggestion (blocking))
- [ ] [file:line] `issue:` description — why it matters + how to fix

### Non-blocking (suggestion / todo / question)
- [ ] [file:line] `suggestion (non-blocking):` description — rationale

### Nits (nitpick / chore)
- [ ] [file:line] `nit:` description

### Praise
- [file:line] `praise:` what worked well
```

**Rules:**
- Every blocking comment must explain **why** and **how to fix**
- Link to relevant documentation or standards when applicable
- Include at least one `praise:` comment when warranted — do not skip
- Never approve code with an open `issue (blocking):`
- Flag missing tests for new logic paths

## Integration

- **Follows rules**: `Agent(software-engineer)` (architecture, code quality)
- **Used by workflows**: `/develop` (REVIEW stage), `/bugfix` (REVIEW stage), `/create-pr` (PR description quality), `/security-audit` (line-level security comments)
- **Companion checklists**: `review-checklist.md`, `security-checklist.md`

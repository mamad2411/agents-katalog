---
name: repo-code-review-pre-pr-review
description: Performs a Gemini-style pre-push pull request review of local diffs before a branch is pushed or a PR is opened. Use when the user wants to catch likely PR review findings early, especially correctness, security, state, concurrency, determinism, build, test, and metadata risks.
license: MIT
compatibility: Version-agnostic. Works with any repository diff; pair with git-github for GitHub branch and PR workflows.
---

# Repo Code Review Pre-PR Review

Use this skill to review local changes before they are pushed to a remote branch or opened as a pull request.

This skill is intentionally vendor-neutral. It does not require Gemini Code Assist, GitHub, or any external service. It captures the useful review behavior observed from AI PR reviewers and turns it into a repeatable local review process.

## When to Use This Skill

Use this skill when the user asks to:

- review changes before pushing a branch;
- simulate a strict PR bot review;
- catch likely PR review comments before opening a PR;
- review a large diff by risk area;
- check for security, correctness, state-machine, concurrency, build, test, metadata, or maintenance issues;
- produce line-level, actionable review findings.

## Required Inputs

Use the best available diff input:

```text
- git diff main...HEAD
- git diff --cached
- a pasted patch
- a PR diff
- changed files plus intended PR summary
```

When possible, ask for or inspect the PR summary too. It helps compare intent against implementation.

## Review Priorities

Review in this order:

1. Security and trust-boundary issues.
2. Correctness and behavior changes.
3. Domain-state and workflow invariants.
4. Concurrency, idempotency, and atomicity.
5. Deterministic hashing, canonicalization, and audit integrity.
6. Runtime robustness against malformed input.
7. Data access, resource lifecycle, and dependency ownership.
8. Monorepo, build, CI, package-script, and cross-platform correctness.
9. Tests, fixtures, and regression coverage.
10. Repository or plugin metadata consistency.
11. Maintainability only where drift could cause real risk.

## Required Review Behavior

- Review only changed code and directly relevant context.
- Prefer fewer high-confidence findings over many speculative comments.
- Do not nitpick style unless it creates real risk.
- Explain the concrete failure mode.
- Include severity.
- Include file path and approximate line or changed block.
- Include a concrete fix.
- Include a small patch when useful.
- Say clearly when no blocking findings were found.
- State what was reviewed and what was not.

## Workflows

Use:

```text
workflows/pre-pr-review-workflow.md
```

## Resources

Use these resources:

```text
resources/gemini-style-review-lens.md
resources/pre-pr-review-checklist.md
```

## Examples

Use this example for output shape:

```text
examples/pre-pr-review-output.md
```

## Pairing With Git/GitHub

For GitHub-specific branch preparation, pair this skill with:

```text
plugins/git-github/skills/git-github-general-pull-request-review/workflows/pre-pr-review-before-push-workflow.md
```

`git-github` owns the Git commands and PR flow. This skill owns the review judgment.
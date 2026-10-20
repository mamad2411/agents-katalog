---
name: code-quality-category-pointer
description: "Pointer to a library of 18 specialized Code Quality skills. Use when working on code-quality-related tasks."
risk: none
---

# Code Quality Capability Library 🎯

This is a **pointer skill**. The 18 specialized Code Quality skills are stored in a hidden vault to keep your startup context minimal.

## Available skills in this category

- **babysit-pr** — Babysit a pull request through its bot review rounds: verify, fix, reply, resolve. Use for any babysit or watch-the-PR ask.
- **break-ai-fix-loops** — Stop ineffective AI coding repair loops with stable failure fingerprints, a three-attempt budget, real-path proof, negative controls, and tested rollback.
- **clean-code** — This skill embodies the principles of "Clean Code" by Robert C. Martin (Uncle Bob). Use it to transform "code that works" into "code that is clean."
- **code-refactoring-refactor-clean** — You are a code refactoring expert specializing in clean code principles, SOLID design patterns, and modern software engineering best practices. Analyze and refactor the provided code to improve its quality, maintainability, and performance.
- **code-review-checklist** — Comprehensive checklist for conducting thorough code reviews covering functionality, security, performance, and maintainability
- **codebase-cleanup-tech-debt** — Identify technical debt from actual code and change history, estimate its impact, and prioritize bounded improvements with explicit assumptions.
- **codex-review** — Professional code review with auto CHANGELOG generation, integrated with Codex AI. Use when you want professional code review before commits, you need automatic CHANGELOG generation, or reviewing large-scale refactoring.
- **comprehensive-review-full-review** — Use when working with comprehensive review full review
- **comprehensive-review-pr-enhance** — Generate structured PR descriptions from diffs, add review checklists, risk assessments, and test coverage summaries. Use when the user says "write a PR description", "improve this PR", "summarize my changes", "PR review", "pull request", or asks to document a diff for reviewers.

- **debate-review** — Two-model debate review of a GitHub PR, GitLab MR, Azure DevOps PR, or local working tree, posted as inline comments or printed. Use for any PR/MR review request, or a local review before a PR exists.
- **find-bugs** — Find bugs, security vulnerabilities, and code quality issues in local branch changes. Use when asked to review changes, find bugs, security review, or audit code on the current branch.
- **fix-review** — Verify fix commits address audit findings without new bugs
- **kaizen** — Guide for continuous improvement, error proofing, and standardization. Use this skill when the user wants to improve code quality, refactor, or discuss process improvements.
- **shellcheck-configuration** — Master ShellCheck static analysis configuration and usage for shell script quality. Use when setting up linting infrastructure, fixing code issues, or ensuring script portability.
- **spec-to-code-compliance** — Verifies code implements exactly what documentation specifies for blockchain audits. Use when comparing code against whitepapers, finding gaps between specs and implementation, or performing compliance checks for protocol implementations.
- **uncle-bob-craft** — Use when performing code review, writing or refactoring code, or discussing architecture; complements clean-code and does not replace project linter/formatter.
- **vibe-code-auditor** — Audit rapidly generated or AI-produced code for structural flaws, fragility, and production risks.
- **vibers-code-review** — Human review workflow for AI-generated GitHub projects with spec-based feedback, security review, and follow-up PRs from the Vibers service.

## How to load a skill

1. Identify the skill name above matching your task.
2. Use `view_file` to read its `SKILL.md` from the vault:
   `<CONFIG_ROOT>/.config/opencode/skill-libraries/code-quality/<skill-name>/SKILL.md`
3. Follow those instructions to complete the request.

**Vault path:** `<CONFIG_ROOT>/.config/opencode/skill-libraries/code-quality`

> Do not guess best practices — always read from the vault first.

> ⚠️ **Anti-loop guard**: Do NOT invoke skills recursively or check for applicable skills before every response. Each skill should be loaded at most once per user request. If you have already identified and loaded the relevant skill for this task, proceed with execution — do not re-scan for skills.

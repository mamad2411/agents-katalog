---
name: code-quality-category-pointer
description: "Pointer to a library of 43 specialized Code Quality skills. Use when working on code-quality-related tasks."
risk: none
---

# Code Quality Capability Library 🎯

This is a **pointer skill**. The 43 specialized Code Quality skills are stored in a hidden vault to keep your startup context minimal.

## Available skills in this category

- **andrej-karpathy** — Behavioral guidelines to reduce common LLM coding mistakes. Use when writing, reviewing, or refactoring code to avoid overcomplication, make surgical changes, surface assumptions, and define verifiable success criteria.
- **audit-agent-run-evidence** — Use when an agent, harness, gateway, MCP workflow, or multi-step automation claims completion and the available traces, checkpoints, approvals, tool calls, or deployment records must be judged without trusting self-reported success.
- **babysit-pr** — Babysit a pull request through its bot review rounds: verify, fix, reply, resolve. Use for any babysit or watch-the-PR ask.
- **break-ai-fix-loops** — Stop ineffective AI coding repair loops with stable failure fingerprints, a three-attempt budget, real-path proof, negative controls, and tested rollback.
- **brooks-debt** — Tech debt assessment that identifies, classifies, and prioritizes maintainability problems — helping teams build a refactoring roadmap — drawing on twelve classic engineering books.
- **brooks-harness** — Maintenance orchestrator for the brooks-lint plugin itself.
- **brooks-review** — PR code review that surfaces decay risks, design smells, and maintainability issues with concrete Symptom → Source → Consequence → Remedy findings, drawing on twelve classic engineering books.
- **brooks-sweep** — Full-sweep mode: runs a unified analysis across all quality dimensions — code decay, architecture, tech debt, and test quality — then applies fixes directly to the codebase. Safe changes are auto-applied; risky changes are confirmed before execution.
- **bugs-are-annoying** — Adversarial code auditor that hunts down bugs, logic errors, and security flaws. Use for deep correctness passes, not style reviews.
- **clean-code** — This skill embodies the principles of "Clean Code" by Robert C. Martin (Uncle Bob). Use it to transform "code that works" into "code that is clean."
- **clean-code-guard** — Review generated or changed production code with Clean Code, SOLID, DRY, KISS, YAGNI, and LLM-specific failure-mode checks.
- **code-refactoring-refactor-clean** — You are a code refactoring expert specializing in clean code principles, SOLID design patterns, and modern software engineering best practices. Analyze and refactor the provided code to improve its quality, maintainability, and performance.
- **code-review-checklist** — Comprehensive checklist for conducting thorough code reviews covering functionality, security, performance, and maintainability
- **codebase-cleanup-tech-debt** — Identify technical debt from actual code and change history, estimate its impact, and prioritize bounded improvements with explicit assumptions.
- **codex-review** — Professional code review with auto CHANGELOG generation, integrated with Codex AI. Use when you want professional code review before commits, you need automatic CHANGELOG generation, or reviewing large-scale refactoring.
- **complexity-cuts** — Lower Big-O on existing code via a one-transformation-at-a-time playbook with verify-revert-stop. For new code use lemmaly; for math-level wins escalate to mathguard.
- **comprehensive-review-full-review** — Use when working with comprehensive review full review
- **comprehensive-review-pr-enhance** — Generate structured PR descriptions from diffs, add review checklists, risk assessments, and test coverage summaries. Use when the user says "write a PR description", "improve this PR", "summarize my changes", "PR review", "pull request", or asks to document a diff for reviewers.

- **constraint-driven-development** — Write the project quality bar as enforced CONSTRAINTS.md so agents stop quietly lowering it: coverage, performance, accessibility thresholds watched on every diff.
- **debate-review** — Two-model debate review of a GitHub PR, GitLab MR, Azure DevOps PR, or local working tree, posted as inline comments or printed. Use for any PR/MR review request, or a local review before a PR exists.
- **doubt-driven-development** — Subjects every non-trivial decision to a fresh-context adversarial review before it stands.
- **find-bugs** — Find bugs, security vulnerabilities, and code quality issues in local branch changes. Use when asked to review changes, find bugs, security review, or audit code on the current branch.
- **fix-review** — Verify fix commits address audit findings without new bugs
- **invariant-guard** — Correctness-first: forces writing the function contract, loop invariant, termination argument, and edge cases BEFORE code. Catches Boyer-Moore, leftmost binary search, QuickSelect traps.
- **kaizen** — Guide for continuous improvement, error proofing, and standardization. Use this skill when the user wants to improve code quality, refactor, or discuss process improvements.
- **logic-diff** — Compare two code versions for semantic equivalence via semi-formal tracing of both versions side-by-side.
- **logic-fix-all** — Autonomous repository-wide audit-and-fix pipeline: health → review → locate/explain → fix → diff-verify → iterate until clean. Starts with a mandatory consent prompt (token-intensive); after consent runs hands-free.
- **logic-review** — Find logic bugs in a single file or function via semi-formal execution tracing (Premises → Trace → Divergence → Trigger → Remedy).
- **lovable-cleanup** — Audits and strips Lovable scaffolding from Vite + React projects — removes lovable-tagger, swaps placeholder assets, prunes unused Radix deps, cleans generated docs, and neutralizes stale favicon/CDN caching so the codebase ships as yours.
- **orchestrate-batch-refactor** — Plan and execute large refactors with dependency-aware work packets and parallel analysis.
- **review-and-simplify-changes** — Review a git diff or explicit file scope for reuse, code quality, efficiency, clarity, and standards issues, then optionally apply safe Codex-driven fixes.
- **review-swarm** — Parallel read-only multi-agent review of a current git diff or explicit file scope to find behavioral regressions, security or privacy risks, performance or reliability issues, and contract or test coverage gaps.
- **sharp-coder** — Two-layer performance skill combining disciplined THINK layer (surgical edits, simplicity) and terse SPEAK layer (caveman compression). Triggers on requests for brevity, token efficiency, or disciplined coding.

- **shellcheck-configuration** — Master ShellCheck static analysis configuration and usage for shell script quality. Use when setting up linting infrastructure, fixing code issues, or ensuring script portability.
- **simplify-code** — Review a diff for clarity and safe simplifications, then optionally apply low-risk fixes.
- **spec-to-code-compliance** — Verifies code implements exactly what documentation specifies for blockchain audits. Use when comparing code against whitepapers, finding gaps between specs and implementation, or performing compliance checks for protocol implementations.
- **super-code** — Standing house style to enforce dense, correct, and idiomatic code on all coding tasks. Minimizes code bloat and agent operation overhead.
- **ui-lint** — Quick automated lint — detects common design system violations in seconds
- **ui-review** — Review UI code for design system compliance, accessibility, and best practices
- **uncle-bob-craft** — Use when performing code review, writing or refactoring code, or discussing architecture; complements clean-code and does not replace project linter/formatter.
- **unslop-review** — Rewrites code review comments so they read like a human teammate wrote them. Cuts corporate-AI throat-clearing ("I noticed...", "I was wondering if perhaps...", "It might be worth considering..."). Each comment is direct: location, the issue, a concrete fix.
- **vibe-code-auditor** — Audit rapidly generated or AI-produced code for structural flaws, fragility, and production risks.
- **vibers-code-review** — Human review workflow for AI-generated GitHub projects with spec-based feedback, security review, and follow-up PRs from the Vibers service.

## How to load a skill

1. Identify the skill name above matching your task.
2. Use `read` to load its `SKILL.md` from the vault:
   `/home/melfiano/.config/opencode/skill-libraries/code-quality/<skill-name>/SKILL.md`
3. Follow those instructions to complete the request.

**Vault path:** `/home/melfiano/.config/opencode/skill-libraries/code-quality`

> Do not guess best practices — always read from the vault first.

> ⚠️ **Anti-loop guard**: Do NOT invoke skills recursively or check for applicable skills before every response. Each skill should be loaded at most once per user request. If you have already identified and loaded the relevant skill for this task, proceed with execution — do not re-scan for skills.

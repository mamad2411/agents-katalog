---
name: clean-code
description: >
  AI code reviewer and cleanup toolkit for TypeScript/Node.js. Reviews AI-generated code
  for slop patterns (unnecessary abstractions, monoliths, silent failures, dead code,
  performance traps, hallucinated APIs) and produces either a structured review report,
  a diagnosis scan, or a cleaned rewrite. Use this skill whenever the user asks to review
  code, audit code quality, clean up AI-generated code, detect slop, scan for anti-patterns,
  refactor messy code, or check for over-engineering. Also triggers on: "review this file",
  "is this code clean", "find issues", "too complex", "simplify this", "code smell",
  "the AI wrote this and it's messy". Works on individual files, code blocks, diffs, or PRs.
license: MIT
metadata:
  author: beynar
  version: "1.0.0"
---

# Clean Code — AI Code Review Toolkit

A skill collection for reviewing, diagnosing, and cleaning AI-generated TypeScript/Node.js code. Built to be the second-pass reviewer that catches what AI coding agents consistently get wrong.

## Why This Exists

AI coding agents (Claude Code, Copilot, Cursor, Codex) produce predictable failure patterns. CodeRabbit measured 1.7x more issues in AI-generated PRs. GitClear found code duplication up 8x. Augment Code documented that 1 in 5 AI samples reference fake libraries. The code works, but the review bottleneck is real.

This skill turns an AI into a senior reviewer that enforces taste, structure, and correctness — so you can delegate the review, not just the writing.

## When to Use

- After an AI agent writes or modifies code and you want it reviewed
- When code feels "sloppy" but you can't pinpoint why
- Before merging AI-generated PRs
- When you want a quick quality scan before deeper review
- When you want mechanical cleanup applied without discussion

## Three Modes

This skill collection contains three specialized sub-skills. Choose based on what you need:

### 1. Code Review (report + rewrite)
**Trigger**: "review this code", "review this file", "audit this", "check code quality"

Full structured review with severity-ranked issues, line numbers, explanations, and a cleaned rewrite. Two outputs: the report and the fixed code.

See: `references/code-review.md`

### 2. Slop Detector (diagnosis only)
**Trigger**: "scan for slop", "detect anti-patterns", "quick quality check", "how bad is this"

Fast diagnostic scan producing a severity table and a slop score (1-10). No rewrite — just a clear diagnosis with a recommendation (ship it / quick cleanup / needs full review / consider rewriting).

See: `references/slop-detector.md`

### 3. Code Cleanup (rewrite only)
**Trigger**: "clean up this code", "fix this file", "strip the slop", "simplify this"

Mechanical cleanup: 10 ordered passes (dead code → flatten nesting → inline abstractions → naming → comments → silent failures → duplicates → delegation boundary → performance → imports), plus mandatory verification. No report — just the cleaned code with `// REVIEW:` flags where human judgment is needed.

See: `references/code-cleanup.md` and `skills/code-cleanup/SKILL.md`.

## The 14 Anti-Pattern Categories

Organized by severity, grounded in measured data:

### Critical (must fix)

| # | Category | What It Catches | Source |
|---|----------|----------------|--------|
| 1 | **Trojan Output** | Silent failures, fake output, removed safety checks | IEEE Spectrum 2026 |
| 2 | **Error Amnesia** | Swallowed errors, empty catches, inconsistent handling | CodeRabbit (2x gap) |
| 3 | **Walking Dead** | Unused imports, variables, functions, commented-out blocks | GitClear 2025 |
| 4 | **Phantom Import** | Hallucinated APIs, deprecated methods, nonexistent packages | Augment (1 in 5) |

### Important (should fix)

| # | Category | What It Catches | Source |
|---|----------|----------------|--------|
| 5 | **Phantom Abstractions** | Wrappers, singletons, Context Bags, passthrough generators | Practitioner consensus |
| 6 | **Monolith Instinct** | Entire workflows in one function; bad decomposition when forced | Practitioner consensus |
| 7 | **Prophetic Engineering** | Solving hypothetical future problems, ceremony interfaces | Practitioner consensus |
| 8 | **Clone Army** | Duplicated logic instead of reuse | GitClear (8x increase) |
| 9 | **Leaky Delegation** | Parent doing subservice work or duplicating subservices | Practitioner consensus |
| 10 | **Speed Trap** | O(n^2) loops, N+1 queries, sequential awaits | CodeRabbit (8x I/O) |
| 11 | **Nesting Instinct** | Deep control flow that should be flat | Agile Pain Relief (39%) |
| 12 | **Identity Crisis** | Vague naming that hides intent | CodeRabbit (2x) |
| 13 | **Type System Cosplay** | TypeScript features used for complexity, not safety | Practitioner consensus |

### Minor (consider fixing)

| # | Category | What It Catches | Source |
|---|----------|----------------|--------|
| 14 | **Comment Theater** | Comments that restate the code or contradict it | Practitioner consensus |

## Conventions Enforced

- **Early returns**: Guard clauses first. No deep nesting for happy paths.
- **Single responsibility**: One function = one job. One file = one cohesive concern.
- **Coherence over length**: No arbitrary line limits. A 400-line file is fine if it's one concern.
- **Naming**: Verb-first for actions (`getUser`), nouns for data (`activeUsers`), prefixed booleans (`isReady`).
- **Comments**: Top-of-method on non-trivial exports. Purpose + rationale + non-obvious decisions. Never restate the code.
- **Imports**: Remove unused. Don't question dependency choices.
- **Decomposition**: When splitting monoliths — one class per responsibility, parent passes `this` to children, no ceremony types, no intermediate interfaces unless child is independently reusable.

## Rules Reference

Each anti-pattern category has a dedicated rule file under `skills/code-review/rules/` with detailed signals, diagnostic tests, and before/after examples.

| Rule File | Category |
|-----------|----------|
| `skills/code-review/rules/trojan-output.md` | Silent failures & fake output |
| `skills/code-review/rules/error-amnesia.md` | Error handling anti-patterns |
| `skills/code-review/rules/walking-dead.md` | Dead & redundant code |
| `skills/code-review/rules/phantom-import.md` | Hallucinated APIs & outdated patterns |
| `skills/code-review/rules/phantom-abstractions.md` | Unnecessary abstractions |
| `skills/code-review/rules/monolith-instinct.md` | Function & file bloat |
| `skills/code-review/rules/prophetic-engineering.md` | Over-engineering |
| `skills/code-review/rules/clone-army.md` | Code duplication |
| `skills/code-review/rules/leaky-delegation.md` | Separation of concerns / delegation |
| `skills/code-review/rules/speed-trap.md` | Performance anti-patterns |
| `skills/code-review/rules/nesting-instinct.md` | Excessive nesting & complexity |
| `skills/code-review/rules/identity-crisis.md` | Naming failures |
| `skills/code-review/rules/type-cosplay.md` | TypeScript type system abuse |
| `skills/code-review/rules/comment-theater.md` | Missing or excessive comments |

## Sub-Skill References

| Reference File | Purpose |
|---------------|---------|
| `references/code-review.md` | Full review + rewrite process |
| `references/slop-detector.md` | Diagnosis-only scan |
| `references/code-cleanup.md` | Mechanical cleanup pipeline |
| `skills/code-review/references/code-review-process.md` | Step-by-step review workflow |
| `references/system-prompt.md` | Standalone system prompt for any LLM (also under `skills/code-review/references/`) |

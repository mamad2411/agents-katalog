---
name: cli-audit-code
metadata:
  author: clement
description: "Audit code quality with weighted scoring across 12 dimensions (naming, complexity, module design, DRY, errors, security, tests, architecture). Detects named anti-patterns (Fowler/Mantyla taxonomy). Use when reviewing code quality, auditing clean code compliance, checking for code smells, or saying 'audit code', 'code quality', 'code review', 'tech debt'. Invoke with an optional file or directory path."
argument-hint: "[file-or-directory]"
context: fork
agent: general-purpose
---

> **Optimization:** This skill uses on-demand loading. Heavy content lives in `references/` and is loaded only when needed.

> **Language rule:** Skill instructions are written in English. When generating user-facing output, detect the project's primary language (from README, comments, docs, commit messages) and produce the report in that language. If the project is bilingual, ask the user which language to use before proceeding.

# Audit Code — Code Quality Index (CQI)

> "Complexity is the single greatest enemy of reliability." — John Ousterhout

## Core Principles

1. **Evidence-based** — every finding needs a `file:line` reference. No vague "the code could be better"
2. **Proportional** — a 200-line function matters more than a missing doc comment. Scale to project type
3. **Language-aware** — detect the project language and apply its idiomatic patterns, not Java/C# defaults
4. **Named anti-patterns** — use Fowler/Mantyla taxonomy names (Feature Envy, Shotgun Surgery) in findings
5. **Positive reinforcement** — always highlight good practices found, not just violations
6. **Gotchas** — read `../gotchas.md` before producing output to avoid known mistakes

## Input

`$ARGUMENTS` is the target to audit (file path, directory, or empty for whole `src/`).

- If a specific file: audit that file deeply
- If a directory: audit all source files in it
- If empty: audit `src/` broadly (sample 15-20 key files)

## 12-Dimension Framework

Score each dimension **0.0-1.0**, then compute a weighted CQI. Read `references/categories.md` for detailed check lists per category.

| # | Category | Weight | Key question |
|---|----------|--------|-------------|
| C1 | Naming & Readability | 8% | Do names reveal intent? No magic numbers? |
| C2 | Functions & Cognitive Complexity | 12% | < 30 lines? Cognitive complexity < 15? |
| C3 | Module Design (deep vs shallow) | 10% | Deep modules? No pass-through layers? |
| C4 | DRY & Change Amplification | 8% | One change = one file? No copy-paste? |
| C5 | Error Handling & Robustness | 10% | Errors propagated? No swallowed errors? |
| C6 | Type Safety & Language Idioms | 8% | Type system leveraged? Idiomatic patterns? |
| C7 | Comments & Public API Docs | 5% | Public API documented? No redundant comments? |
| C8 | Test Quality | 12% | Error paths tested? No flaky tests? |
| C9 | Security & Input Validation | 10% | Inputs validated at boundaries? No hardcoded secrets? |
| C10 | Immutability & State Management | 7% | Minimal mutable state? No global mutables? |
| C11 | Cognitive Load & Control Flow | 5% | < 3 nesting levels? No negative conditionals? |
| C12 | Dependencies & Architecture | 5% | No circular deps? DIP respected? |

## Workflow

### Step 1 — Discover and sample

Glob source files. For broad audit, prioritize: entry points, public API modules, most-changed files (git log), largest files.

### Context Budget Rule

Do not read a large source file end-to-end as the first step.

- For files over 300 lines or directory audits, start with inventory only: file list, line counts, symbol or function index, git churn, and focused risk greps.
- When evidence points at a line, read a bounded slice around it: about 75 lines before and after, 150 lines max by default. Use `nl -ba path | sed -n 'START,ENDp'`, `sed -n 'START,ENDp'`, or `rtk read -n -m 150 path` when RTK is available.
- Read a full file only when it is 300 lines or less, or when whole-file semantics are required. State that reason in the report.
- Reuse previously read slices and line references instead of re-reading the same file.
- Prefer RTK wrappers for noisy shell output when available: `rtk git`, `rtk cargo`, `rtk grep`, `rtk find`, and bounded `rtk read`. Do not treat generic `rtk log` output as authoritative for structured JSON logs unless a domain-specific filter verifies it.

### Step 2 — Detect language and context

Identify project language, framework, and type (library, CLI, service, script). This determines which idiom checks apply and what scoring standards are proportional.

### Step 3 — Score all 12 dimensions

Read `references/categories.md` for detailed checks. For each category: collect evidence, assign score 0.0-1.0, note specific `file:line` findings.

### Step 4 — Compute CQI and detect anti-patterns

Read `references/scoring.md` for the CQI formula, severity classification, named anti-patterns table, tech debt estimation, and comparative benchmarks.

```
CQI = Σ(wᵢ × sᵢ) / Σ(wᵢ) × 10
```

### Step 5 — Generate report

Finding tier and confidence semantics are canonical in `../shared/triage.md` (Tier 3/2/1 + GRADE + triangulation). Emit each finding with its tier and confidence so `cli-cycle` can aggregate without re-parsing.

## Output Format

```markdown
# Code Quality Audit — {project-name}

**Target**: [file/directory] | **Language**: [detected] | **Date**: [date]
**CQI Score**: X.X/10 — {verdict} | **Tech Debt**: ~Xh ({SQALE grade})

## Scores by Category

| # | Category | Weight | Score | Weighted | Findings |
|---|----------|--------|-------|----------|----------|
| C1-C12 rows with 0.0-1.0 scores... |
| | **CQI** | **100%** | | **X.X/10** | |

## Anti-Patterns Detected
| Pattern | Severity | File:Line | Recommendation |

## Critical Violations (must fix)
### [Category]: [violation title]
- **File**: `path/to/file:123`
- **What**: [description]
- **Why**: [named principle/smell it violates]
- **Fix**: [concrete suggestion]
- **Disproof**: [observation that would invalidate this finding — e.g., "this isn't dead code IF dynamic dispatch is used here"]

## Flags (should fix)
[same format]

## Good Practices Found
[positive reinforcement]

## Recommended Next Steps
1. [highest-impact fix first]
2. [second]
3. [third]
```

## What this skill does NOT do

- **Does not fix code** — it reports. Use the findings to guide refactoring
- **Does not replace linters** — it complements them with semantic analysis a linter can't do
- **Does not check test coverage numbers** — it checks test quality. Use `cli-audit-test` for test strategy
- **Does not audit documentation quality** — use `cli-audit-doc` for that

## Integration with other cli-* skills

| Skill | Relationship |
|-------|-------------|
| `cli-audit-xray` | Turns static hidden-cost smells (repeated work, clones, allocations, bad cache placement) into optimization cards with invariants and validation |
| `cli-audit-doc` | Scores doc quality. cli-audit-code scores **code quality** |
| `cli-audit-test` | Scores test strategy. cli-audit-code checks **test code quality** (C8) |
| `cli-forge-lld` | Validates implementation matches the LLD design |
| `cli-forge-perf` | Detects static perf anti-patterns (alloc in hot path, quadratic complexity, hidden-cost abstractions). `cli-forge-perf` verifies they are **dynamically** costly via profiling + bench |
| `cli-cycle` | Calls cli-audit-code as part of full project review; emit `.claude/cli-audit-code.json` per `../shared/result-schema.md` for orchestrator aggregation |

## Dynamic Handoffs

After your analysis, recommend these skills if conditions are met:

| Condition detected | Recommend | Why |
|-------------------|-----------|-----|
| Repeated computation, allocation/copy churn, cache-before-normalization, or dataflow cost with unclear safety | `/cli-audit-xray` | Build semantic/resource-flow candidates before recommending a rewrite |
| God class/module (C3 > 500 lines, many responsibilities) | `/cli-audit-tangle` | Topology analysis reveals optimal split points |
| Hardcoded secrets or `.env` tracked in git (C9) | `/cli-git-conventional --audit-markers` | Check git history for leaked secrets |
| Shell scripts in the project with quality issues | `/cli-audit-shell` | Deep bash-specific audit beyond C6 idioms |
| Missing or stale documentation (C7 low) | `/cli-forge-doc` | Generate/update project docs |
| Test quality issues (C8 low) | `/cli-audit-test` | Full test strategy audit |
| CI/CD config present but not audited | `/cli-forge-pipeline` | Pipeline optimization |
| Static perf anti-pattern detected (alloc in loop, O(n²), N+1) on a hot service | `/cli-forge-perf` | Confirm the dynamic cost and lock the fix with an A/B bench gate |
| PostgreSQL/SQLx flow has read-before-write, split transactions, ignored zero-row writes, or tenant-key gaps | `/cli-audit-data` | Prove database invariants and concurrent executions |

**Rule:** Recommend, don't auto-execute. Phrase as: "Consider running `/cli-audit-tangle` — 3 god modules detected that need topology analysis."

## Reference Sources

- Ousterhout — *A Philosophy of Software Design* | Martin — *Clean Code* | Fowler — *Refactoring* | Tornhill — *Software Design X-Rays* | Feathers — *Working Effectively with Legacy Code*
- SonarQube Quality Model | SonarSource Cognitive Complexity | SQALE Method | CodeScene Code Health | Clippy lint categories
- CodeAesthetic | ThePrimeagen | ArjanCodes | Software Engineering Radio | Tech Lead Journal

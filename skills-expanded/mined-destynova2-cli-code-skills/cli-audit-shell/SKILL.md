---
name: cli-audit-shell
metadata:
  author: clement
description: >
  Audit shell scripts against Google Shell Style Guide + ops best practices.
  Scores 12 dimensions: strict mode coherence, error surfaces, logging,
  stderr hygiene, variable discipline, quoting, control flow, naming,
  CLI ergonomics, idempotency, namespace, and security.
  Goes beyond shellcheck — detects semantic anti-patterns invisible to linters
  (dead fallbacks under set -e, custom loggers vs logger(1), redundant
  package checks, env var injection in heredocs, missing getopts).
  Use when reviewing shell scripts, auditing bash code, checking deployment
  scripts, or saying 'audit shell', 'bash review', 'script quality',
  'shell style', 'shellcheck not enough', 'review my script'.
  Also triggers on 'set -euo pipefail', 'getopts', 'shell injection',
  'logger', 'bash best practices', 'google shell style'.
argument-hint: "[file-or-directory]"
context: fork
agent: general-purpose
---

> **Optimization:** This skill uses on-demand loading. Heavy content lives in `references/` and is loaded only when needed.

> **Language rule:** Skill instructions are written in English. This skill targets Bash scripts exclusively. When generating user-facing output, detect the project's primary language (from README, comments, docs, commit messages) and produce the report in that language. If the project is bilingual, ask the user which language to use before proceeding.

# Audit Shell — Shell Quality Index (SQI)

> "Shell should only be used for small utilities or simple wrapper scripts." — Google Shell Style Guide

## Core Principles

1. **Evidence-based** — every finding needs a `file:line` reference. No vague "the script could be better"
2. **Proportional** — a 500-line script doing LVM partitioning matters more than a 10-line wrapper. Scale to script complexity
3. **Beyond shellcheck** — shellcheck catches syntax; this skill catches **semantic** anti-patterns (dead code under `set -e`, redundant package checks, injections in heredocs)
4. **Named anti-patterns** — use the anti-pattern names from `references/anti-patterns.md` in findings
5. **Positive reinforcement** — always highlight good practices found
6. **Complexity-adapted tooling** — simple problems deserve simple tools (sed), complex problems deserve proper tools (kustomize). Read `references/tooling-ladder.md`
7. **Gotchas** — read `../gotchas.md` before producing output to avoid known mistakes

## Input

`$ARGUMENTS` is the target to audit (file path, directory, or empty for auto-detect).

- If a specific `.sh` file: audit that file deeply
- If a directory: audit all `.sh` files and shebanged scripts in it
- If empty: find all shell scripts in the project (glob `**/*.sh` + grep `#!/bin/bash` or `#!/usr/bin/env bash`)

## 12-Dimension Framework

Score each dimension **0.0-1.0**, then compute a weighted SQI. Read `references/categories.md` for detailed checklists per category.

| # | Category | Weight | Key question |
|---|----------|--------|-------------|
| S1 | Strict Mode Coherence | 12% | Is `set -euo pipefail` used AND is code compatible with it? No dead fallbacks? |
| S2 | Error Surfaces & Return Values | 12% | Are return values checked? No `\|\| true`? No swallowed `2>/dev/null`? |
| S3 | Logging & Observability | 8% | Uses `logger(1)` or structured output? Timestamps? Severity levels? |
| S4 | Stderr Hygiene | 5% | Errors to stderr, output to stdout? No blanket `2>/dev/null`? |
| S5 | Variable Discipline | 10% | `local` in functions? No unquoted expansions? No injection in heredocs? |
| S6 | Quoting & Expansion | 8% | `"${var}"` not `$var`? Arrays for lists? `"$@"` not `$*`? |
| S7 | Control Flow & Structure | 8% | `main()` pattern? Functions near top? Early returns? Max depth 3? |
| S8 | Naming Conventions | 5% | `lower_snake_case` functions? `UPPER_CASE` constants? `::` for packages? |
| S9 | CLI Ergonomics | 10% | `getopts`/`getopt` for options? `--help`? Single entry point vs N scripts? S9 follows the canonical surface mapping in `../shared/cli-ergonomics.md` (Laws 1-3 applied to shell). |
| S10 | Idempotency & Safety | 10% | Check-before-create? No destructive assumptions? `readonly` for constants? |
| S11 | Namespace & Env Hygiene | 7% | Env vars prefixed by project? No global pollution? `local` everywhere? |
| S12 | Security & Injection | 5% | No `eval`? No unquoted user input in commands? No shell injection in env blocks? |

## Workflow

### Step 1 — Discover, sample, and detect language

Glob for shell scripts: `**/*.sh`, `**/Makefile`, shebanged files. For broad audit, prioritize: entry points (`setup.sh`, `install.sh`, `deploy.sh`), longest scripts, most-changed scripts (git log).

**Detect output language**: `git log --oneline -10` + `head -20 README.md`. Report in the project's language (French commits → French report).

### Step 2 — Detect script context

Classify each script:
| Type | Characteristics | Adjusted expectations |
|------|----------------|----------------------|
| **Installer/bootstrap** | Runs as root, creates users/mounts | S10 (idempotency) weight ×1.5, S12 (security) weight ×1.5 |
| **Library** (sourced) | Has `.sh` extension, no shebang exec | S8 (naming) weight ×1.5, S9 (CLI) weight ×0 |
| **Wrapper/glue** | < 50 lines, calls other tools | Lighter audit overall, S7 (structure) weight ×0.5 |
| **Build/CI script** | In `.github/`, `.gitlab-ci/`, `Makefile` | S2 (errors) weight ×1.5 |

### Step 3 — Run shellcheck first

```bash
shellcheck -x -S style <file>
```

If shellcheck is not installed, note it and proceed with manual analysis. Shellcheck findings go into the report but **don't duplicate** them in the dimension scores — this skill adds what shellcheck cannot see.

### Step 4 — Score all 12 dimensions

Read `references/categories.md` for detailed checks. For each category: collect evidence, assign score 0.0-1.0, note specific `file:line` findings.

### Step 5 — Detect anti-patterns

Read `references/anti-patterns.md` for named anti-patterns with detection heuristics. These are the **semantic** patterns shellcheck cannot find.

### Step 6 — Assess tooling fit

Read `references/tooling-ladder.md` for the complexity-adapted tooling decision tree. Flag scripts that use sed/awk for YAML when they should use yq/kustomize. Flag scripts that use kustomize for a 3-variable substitution when sed would suffice.

### Step 7 — Compute SQI and generate report

Read `references/scoring.md` for the SQI formula, severity classification, and benchmarks.

```
SQI = Sigma(wi x si) / Sigma(wi) x 10
```

Finding tier and confidence semantics are canonical in `../shared/triage.md` (Tier 3/2/1 + GRADE + triangulation). S-dimension findings carry tier and confidence so `cli-cycle` can aggregate without re-parsing.

## Output Format

```markdown
# Shell Audit -- {project-name}

**Target**: [file/directory] | **Scripts found**: [N] | **Date**: [date]
**SQI Score**: X.X/10 -- {verdict}
**Shellcheck**: [N warnings, M errors] (or "not available")

## Scores by Category

| # | Category | Weight | Score | Weighted | Key findings |
|---|----------|--------|-------|----------|-------------|
| S1-S12 rows with 0.0-1.0 scores... |
| | **SQI** | **100%** | | **X.X/10** | |

## Anti-Patterns Detected
| # | Pattern | Severity | File:Line | Recommendation |

## Critical Violations (must fix)
### [Category]: [violation title]
- **File**: `path/to/file:123`
- **What**: [description]
- **Why**: [named principle it violates + Google Shell Style Guide reference]
- **Fix**: [concrete code suggestion]

## Flags (should fix)
[same format]

## Tooling Recommendations
| Current tool | Used for | Recommended | Why |
[complexity-adapted tooling analysis]

## Good Practices Found
[positive reinforcement]

## Recommended Next Steps
1. [highest-impact fix first]
2. [second]
3. [third]
```

## What this skill does NOT do

- **Does not replace shellcheck** — it complements it with semantic analysis shellcheck can't do
- **Does not fix scripts** — it reports. Use the findings to guide refactoring
- **Does not audit non-shell code** — YAML, Dockerfiles, Terraform go to `cli-forge-infra`
- **Does not audit test strategy** — use `cli-audit-test` for that
- **Does not audit code topology** — use `cli-audit-tangle` for call graph analysis

## Integration with other cli-* skills

| Skill | Relationship |
|-------|-------------|
| `cli-audit-code` | Scores code quality generically. cli-audit-shell goes **deep on bash semantics** |
| `cli-forge-infra` | Audits infra config and ops patterns. cli-audit-shell audits the **scripts themselves** |
| `cli-audit-tangle` | Detects structural coupling. cli-audit-shell detects **bash-specific** structural issues |
| `cli-forge-pipeline` | Optimizes CI/CD pipelines. cli-audit-shell audits **shell scripts used in CI** |
| `cli-cycle` | Should call cli-audit-shell as part of full project review when shell scripts exist; emit `.claude/cli-audit-shell.json` per `../shared/result-schema.md` for orchestrator aggregation |

## Dynamic Handoffs

| Condition detected | Recommend | Why |
|-------------------|-----------|-----|
| Sed on YAML/JSON (AP7 Sed Surgeon) | `/cli-forge-infra` | Tooling ladder assessment, kustomize/yq recommendation |
| Multiple scripts without getopts (AP8 Script Hydra) | `/cli-audit-wizard` | UX audit of the setup/init flow |
| Shell injection risk in env blocks (AP9) | `/cli-audit-code` on the consuming code | Verify the sourcing code validates inputs |
| Scripts are CI/CD entrypoints | `/cli-forge-pipeline` | Pipeline-level optimization |
| Script > 100 lines with god functions | `/cli-audit-tangle` | Topology analysis for split points |
| Entrypoints with wait-for/sleep/`nc -z` loops or `sed` on app config | `/cli-audit-hanoi` | Displacement audit: trace the hack to the missing app capability |

**Rule:** Recommend, don't auto-execute.

## Reference Sources

- Google — *Shell Style Guide* (primary authority)
- Wooledge — *BashGuide*, *BashFAQ*, *BashPitfalls*
- ShellCheck — SC1000-SC9999 rule database
- Kfir Lavi — *Defensive Bash Programming*
- Dylan Araps — *Pure Bash Bible*
- Greg Wooledge — *Bash Idioms* (O'Reilly)
- SixArm — *Unix Shell Script Tactics* (XDG compliance, NO_COLOR standard, portability catalog)
- clig.dev — *Command Line Interface Guidelines* (CLI ergonomics, --json, --dry-run)
- no-color.org — *NO_COLOR standard* (color output gating)
- POSIX.1-2024 — Shell Command Language specification

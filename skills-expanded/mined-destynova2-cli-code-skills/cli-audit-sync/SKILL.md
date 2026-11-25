---
name: cli-audit-sync
metadata:
  author: clement
description: "Verify documentation-code coherence: detect stale references, broken links, terminology drift, outdated diagrams, and non-working examples. Use when the user wants to check if docs match reality, detect doc drift, verify README accuracy, find stale documentation, or says 'is my doc up to date', 'check coherence', 'sync docs', 'doc drift', 'stale docs', 'verify documentation'. Also triggers on 'broken links', 'outdated references', 'docs match code'."
argument-hint: "[project-path]"
context: fork
agent: general-purpose
allowed-tools:
  - Read
  - Write
  - Grep
  - Glob
  - Bash
  - Agent
---

> **Optimization:** This skill uses on-demand loading. Heavy content lives in `references/` and is loaded only when needed.

> **Language rule:** Skill instructions are written in English. When generating user-facing output, detect the project's primary language (from README, comments, docs, commit messages) and produce the report in that language. If the project is bilingual, ask the user which language to use before proceeding.

# Audit Sync — Documentation-Code Coherence Verifier

Detect every place where documentation says one thing and the code says another.

> "A stale diagram is worse than no diagram. A README with wrong commands is worse than no README."

## Core Principle

**Documentation is a contract with the reader.** Every statement in docs is an implicit promise: "this is true right now." This skill finds broken promises.

**Gotchas** — read `../gotchas.md` before producing output to avoid known mistakes.

## Three-Layer Verification

| Layer | Style | What it checks | Severity focus |
|-------|-------|---------------|----------------|
| **Layer 1 — Structural** | lychee-style | Internal links, anchors, images, code file refs, imports | Broken refs |
| **Layer 2 — Semantic** | DocPrism/Swimm | Module/function/type names, endpoints, CLI flags, env vars, versions | Stale names |
| **Layer 3 — Executable** | Docs-as-Tests | Shell commands, install steps, code snippets, Mermaid diagrams, **demo kits** (`docs/demos/**/DEMO.md`: each beat's command vs its declared expected output) | Broken examples, stale demo |

Read `references/layers.md` for detailed check tables, methodology, and safety rules per layer.

## Workflow

### Mitosis — Scale to doc volume

S/M/L/XL semantics are canonical in `../shared/tiering.md` — the table below specializes them to doc-file count and audit-layer depth.

| Tier | Signal | Depth |
|------|--------|-------|
| **S** | 1-2 doc files | Layer 1 only + quick Layer 2 |
| **M** | 5-15 doc files | Layer 1 + Layer 2 + sample Layer 3 |
| **L** | 20+ doc files | All 3 layers + terminology map + diagram verification |

### Step 1 — Discover documentation

Glob: `**/*.md`, `docs/**/*`, `README*`, `CHANGELOG*`, `CONTRIBUTING*`

### Step 2 — Build code index (source of truth)

- File tree (all source files)
- Exported symbols (public functions, types, modules)
- Route definitions, config keys, CLI commands/flags
- Dependencies + version from manifest

### Step 3 — Run layers (parallel)

Launch sub-agents for each applicable layer. Read `references/layers.md` for detailed checks per layer.

### Step 3b — Duplication scan (DRY/SSOT/KISS rules)

Read `references/duplication-rules.md` for the 25 reproducible rules with citations (Hunt/Thomas, Fowler, Metz, McCabe, Diátaxis, SSOT).

Run 5 rule families:
- **D rules** — Doc-doc duplication (same paragraph/table/code block in ≥2 docs)
- **C rules** — Code-code cross-format duplication (Makefile + CI YAML + scripts + docs)
- **S rules** — SSOT violations (CLI flags, version strings, config defaults code↔doc)
- **M rules** — Anti-false-DRY (Sandi Metz: don't escalate < 3 instances, flag wrong abstractions)
- **I rules** — Information-theoretic duplication index (gzip ratio, optional)

Apply Fowler's Rule of Three: 1 = ignore, 2 = warn, 3+ = error. **Exception:** if 2 instances have different values (drift), it's immediately critical.

This fills a gap NO mainstream tool covers: cross-format command/env duplication detection.

### Step 4 — Synthesize report

## Output Format

```markdown
# Doc-Code Sync Report — {project-name}

**Date:** {date}
**Files scanned:** {n} docs, {m} source files
**Coherence score:** {X}/10

## Summary

| Layer | Checks | Passed | Failed | Warnings |
|-------|--------|--------|--------|----------|

## Critical Issues (fix now)

| # | File:Line | Issue | What docs say | What code says |

## Warnings (fix soon)

## What's in sync (good)

## Terminology Map (if tier L)
```

## Scoring

| Score | Meaning |
|-------|---------|
| 10/10 | Every doc reference matches code. Zero drift |
| 8-9 | Minor warnings only (terminology, info-level) |
| 6-7 | Some stale references but no broken commands |
| 4-5 | Multiple broken references, outdated sections |
| 1-3 | Documentation is actively misleading |

## Integration with other cli-* skills

| Skill | Relationship |
|-------|-------------|
| `cli-audit-doc` | Scores doc **quality**. cli-audit-sync scores doc **accuracy** |
| `cli-audit-drift` | Checks **contract-code** coherence. cli-audit-sync checks **doc-code** coherence |
| `cli-forge-schema` | Generates diagrams. cli-audit-sync **verifies** existing diagrams match code |
| `cli-forge-readme` | Generates READMEs. cli-audit-sync **verifies** existing README matches reality |
| `cli-cycle` | Calls cli-audit-sync as part of the full project review; emit `.claude/cli-audit-sync.json` per `../shared/result-schema.md` for orchestrator aggregation |

## Dynamic Handoffs

| Condition detected | Recommend | Why |
|-------------------|-----------|-----|
| Shell commands in docs don't work | `/cli-audit-shell` | Audit the scripts referenced |
| README architecture section outdated | `/cli-forge-readme` | Update README |
| Stale diagrams | `/cli-forge-schema` | Regenerate from current code |
| API reference mentions deleted functions | `/cli-audit-code` | Check for dead code |
| Demo kit beats no longer match code (commands fail or output differs) | `/cli-forge-demo` | Regenerate the stale demo from the current golden path |

**Rule:** Recommend, don't auto-execute.

## What this skill does NOT do

- **Does not fix docs** — it reports. Use `cli-forge-*` skills to fix
- **Does not execute unsafe commands** — dry-run verification only
- **Does not check external URLs** — no network calls
- **Does not replace linters** — Vale/markdownlint handle prose style, this handles truth

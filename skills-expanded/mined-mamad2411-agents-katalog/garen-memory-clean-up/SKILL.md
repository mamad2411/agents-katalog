---
name: garen-memory-clean-up
description: Audit and optimize CLAUDE.md instruction files. Triggered ONLY by explicit /garen-memory-clean-up command — do NOT auto-trigger. Evaluates global (~/.claude/CLAUDE.md), project (.claude/CLAUDE.md), and local (CLAUDE.local.md) scope files against best practices from "The CLAUDE.md File That 10x'd My Output" article. Produces audit scorecard, anti-pattern detection, cross-scope duplication report, and actionable optimization todo list with suggested edits.
---

# Garen Memory Clean-up

Audit CLAUDE.md instruction files against proven best practices. Produces a structured report with scorecard, anti-pattern detection, and actionable improvements.

## Trigger

This skill triggers ONLY on explicit `/garen-memory-clean-up` invocation. Do NOT auto-trigger.

---

## Workflow

### Step -1: Pre-flight

Before starting the audit:
1. Check if CWD is a git repository (`git rev-parse --git-dir`)
2. If CWD is NOT a repo (e.g., home directory `~`):
   - Project-scope `.claude/CLAUDE.md` may resolve to the SAME file as global `~/.claude/CLAUDE.md`
   - In this case: audit global only, mark project as "N/A (CWD is not a repo, resolves to global)"
   - Skip local check (CLAUDE.local.md only makes sense in a repo context)
3. If CWD IS a repo: proceed normally with all 3 scopes

### Step 0: Discovery

Scan for all instruction files across the 3-level hierarchy:

| Scope | Path | Purpose |
|-------|------|---------|
| Global | `~/.claude/CLAUDE.md` | Rules for every project |
| Project | `.claude/CLAUDE.md` (repo root) | Stack-specific, team-shared |
| Local | `./CLAUDE.local.md` (repo root) | Personal overrides, gitignored |
| Rules | `~/.claude/rules/**/*.md` | Auto-loaded rule files (common duplication source) |

For each path: check existence → read content → record line count. Note missing files as "not found."

### Step 1: Per-File Audit

For each discovered file, run checks from `references/audit-checklist.md` — the checklist specifies which checks apply to which scope (e.g., Commands/Architecture sections are correctly absent from global scope).

1. **Line count budget** — within recommended limits?
2. **Critical sections** — which of the 5 essential sections present/missing?
3. **Hard rules quality** — do rules prevent specific mistakes or are they vague?
4. **Personality instructions** — lines that describe WHO not WHAT
5. **Auto-memory-learnable content** — lines Claude figures out after 1 session
6. **IMPORTANT marker usage** — high-priority rules marked? Not overused?
7. **NEVER section** — rule count ≤15, each rule passes the removal test
8. **Out of scope section** — present or missing?

**Auto-memory inspection**: To check what Claude already knows, look for memory files at:
- `~/.claude/projects/<project-hash>/memory/` (project-specific memories)
- Run `ls ~/.claude/projects/` to find project directories

If memory files cannot be accessed, fall back to heuristic detection from `references/audit-checklist.md` Check 5 — flag format preferences and output style lines as "likely auto-memory-learnable" without confirming.

### Step 2: Cross-Scope Analysis

Check for duplication across all discovered files:

1. **Global ↔ Project** — rules repeated in both
2. **Global ↔ Rules/** — CLAUDE.md content already in auto-loaded rules/ files
3. **Project ↔ Local** — overrides that are actually duplicates
4. **Any scope ↔ Auto memory** — content Claude learns automatically

For each duplicate: record rule text, locations (file + line), which copy to keep and why.

**Note**: A "pointer line" (e.g., `→ Defined in agents.md`) is NOT a duplication — it's the recommended pattern. Only flag content that REPEATS the actual rule text, not lines that reference where the rule lives.

### Step 3: Generate Report

Use this exact template:

```
## CLAUDE.md Audit Report

### Files Discovered
| Scope | Path | Exists | Lines | Budget | Status |
|-------|------|--------|-------|--------|--------|

**Combined budget**: [sum of all files] / ≤120 recommended / ≤200 max → [status]

### Section Coverage Scorecard
| Article Section | Global | Project | Local | Notes |
|---|---|---|---|---|
| 1. Critical commands | | | | |
| 2. Architecture map | | | | |
| 3. Hard rules (NEVER) | | | | |
| 4. Workflow preferences | | | | |
| 5. Out of scope | | | | |

### Anti-Pattern Detection
| Anti-pattern | Found? | Lines | Verdict |
|---|---|---|---|
| Personality instructions | | | |
| Auto-memory-learnable | | | |
| Vague/non-actionable rules | | | |
| >15 rules in NEVER | | | |
| Missing IMPORTANT markers | | | |
| Excessive IMPORTANT (>4) | | | |

### Cross-Scope Duplications
| Rule/Content | Scope A | Scope B | Keep in | Savings |
|---|---|---|---|---|

### Action Items (Priority-Ordered)
| # | Action | Priority | File | Est. Savings |
|---|---|---|---|---|
```

For Status column use: ✅ within recommended / ⚠️ over recommended but under max / ❌ over max.
For Section Coverage use: ✅ present / ❌ missing / N/A (correctly absent for scope).

Optionally include a "### What's Working Well" section for patterns that are already good practice (e.g., pointer lines to rules/, IMPORTANT markers on critical rules, clean NEVER section size). This helps the user understand what NOT to change.

### Step 4: Suggest Edits

For each High/Medium priority action item, provide:
1. Exact line(s) to change with `path:line` reference
2. What to replace with (or "delete")
3. Why this improves the file

Format as a numbered checklist the user can approve item-by-item.

### Step 5: Wait for User Decision

Present the report and action items. Do NOT make any edits without user approval. User may:
- Approve all → execute edits
- Approve some → execute selected only
- Reject all → no changes
- Ask questions → clarify and re-present

---

## Line Count Budgets

| Scope | Recommended | Maximum | Rationale |
|-------|-------------|---------|-----------|
| Global | ≤80 lines | ≤150 lines | Loaded every session, every project |
| Project | ≤60 lines | ≤100 lines | Loaded on top of global |
| Local | ≤30 lines | ≤50 lines | Personal overrides only |
| Combined | ≤120 lines | ≤200 lines | Total instruction budget |

## What Belongs Where

| Content Type | Correct Scope | Why |
|---|---|---|
| Reply language, output format prefs | Global | Same across all projects |
| Orchestration, agent dispatch rules | Global | Same across all projects |
| Build/test/lint commands | Project | Stack-specific |
| Architecture map | Project | Repo-specific |
| Stack constraints (pnpm only, viem only) | Global (if universal) or Project | Depends on scope |
| Personal quirks, local overrides | Local | Not shared with team |
| Coding standards, patterns | `~/.claude/rules/` | Auto-loaded, keeps CLAUDE.md lean |

## Reference

For the full audit checklist with detection heuristics, read `references/audit-checklist.md` before running checks.

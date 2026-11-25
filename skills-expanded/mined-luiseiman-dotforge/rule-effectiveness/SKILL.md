---
name: rule-effectiveness
description: Cross-reference .claude/rules/ globs against git history to find inert rules and uncovered directories. Content quality and context cost are native — run /doctor prompt-audit and /skill-doctor for those.
---

# Rule Effectiveness Analysis

Analyze the effectiveness of `.claude/rules/` in the current project by cross-referencing rule globs against actual file activity from git history.

**Scope (native-first boundary, v4.7.0)**: this skill owns the one measurement Claude Code has no native equivalent for — *does each rule's glob match files the project actually touches*. Everything else is native:
- `/doctor prompt-audit [path]` (v2.1.283+) flags rules/CLAUDE.md written for older models, references to files or commands that no longer exist, and contradictions between files — run it for content quality.
- `/skill-doctor` (v2.1.252+) and `/doctor` report per-skill/MCP context cost and unused skills — run them for token budget.
Do not re-implement either here.

## Step 1: Collect rules inventory

Read all `.md` files in `.claude/rules/`. For each:
1. Extract `globs:` value from YAML frontmatter
2. Count lines of content (excluding frontmatter)
3. Record filename and glob pattern

If a rule has no `globs:` or `paths:` frontmatter, classify as **always-loaded** (loads every session regardless of files touched).

Rules with `globs:` load eagerly at session start. Rules with `paths:` + `alwaysApply: false` load lazily (only when a matching file is touched). Note: `paths:` must be unquoted CSV — YAML arrays and quoted strings fail silently.

## Step 2: Collect file activity from git history

Run: `git log --name-only --pretty=format:'' --since='3 months ago'` (or configurable period).

Parse output to build:
- **session_files**: group files by commit date (approximate 1 day = 1 session)
- **total_sessions**: count distinct dates with commits
- **all_files_touched**: unique set of all files modified

If fewer than 5 sessions available, warn that results may not be representative and extend to `--since='6 months ago'`.

## Step 3: Cross-reference rules vs activity

For each rule with a glob pattern:
1. Match glob against **all_files_touched** using bash glob expansion or fnmatch logic
2. Calculate:
   - `matched_files`: count of unique files that match the glob
   - `match_rate`: % of sessions where at least 1 file matched the glob
   - `token_cost`: lines of rule content (proxy for context consumption)

For the project overall:
- `covered_files`: files that match at least 1 rule glob
- `uncovered_files`: files touched but matching no rule
- `file_coverage`: covered / total

## Step 4: Classify rules

| Classification | Criteria | Action |
|---------------|----------|--------|
| **Active** | match_rate > 50% | Keep — rule loads in most sessions and covers real files |
| **Occasional** | match_rate 10-50% | Evaluate — may be worth keeping for specific workflows (deploys, migrations) |
| **Inert** | match_rate < 10% | Candidate for removal — consumes tokens without matching real files |
| **Always-loaded** | globs: `**/*` or no globs | Evaluate content — is it generic enough to justify always loading? |
| **Overbroad** | globs: `**/*` but content is stack-specific | Should have narrower globs to avoid loading in wrong contexts |

## Step 5: Detect coverage gaps

From **uncovered_files**, group by directory prefix. Report directories with >5 uncovered files:

```
SIN COBERTURA:
  src/utils/     — 12 files touched, no rule covers this path
  scripts/       — 8 files touched, no rule covers this path
  migrations/    — 5 files touched, no rule covers this path
```

For each gap, suggest:
- If directory maps to an existing stack (e.g., `migrations/` → supabase), recommend adding stack rule
- If directory is project-specific, recommend creating a custom rule

## Step 6: Native content + cost audit (pointer, not re-implemented)

Tell the user to run, in this order, and include the pointers in the report:
1. `/doctor prompt-audit .claude/rules` — stale-model phrasing, broken paths/commands, contradictions (content quality).
2. `/skill-doctor` — context cost and usage of skills; `/doctor` for MCP servers and plugins vs their cost.

For inert rules found in Step 4, the line count is a sufficient proxy — do not compute a token budget table.

## Step 7: Generate report

```
═══ RULE EFFECTIVENESS — {{project}} ═══
Period: last {{N}} months ({{total_sessions}} sessions)
Rules: {{rule_count}} files, {{total_lines}} lines

── ACTIVE (keep) ──
  {{rule.md}}     — {{match_rate}}% match, {{matched_files}} files, {{lines}} lines
  ...

── OCCASIONAL (evaluate) ──
  {{rule.md}}     — {{match_rate}}% match, {{matched_files}} files
  ...

── INERT (candidates for removal) ──
  {{rule.md}}     — {{match_rate}}% match, {{matched_files}} files ← {{reason}}
  ...

── ALWAYS-LOADED ({{total_lines}} lines/session) ──
  {{rule.md}}     — {{lines}} lines, globs: **/*
  ...

── COVERAGE ──
  Files covered by rules:   {{covered}}/{{total}} ({{coverage}}%)
  Gaps: {{gap_dirs}}

── NATIVE FOLLOW-UP ──
  /doctor prompt-audit .claude/rules   → content quality (stale models, broken refs, contradictions)
  /skill-doctor                        → context cost of skills; /doctor for MCP + plugins

── RECOMMENDATIONS ──
1. {{action}} — {{reason}}
2. ...
```

## Step 8: Offer automated fixes

For each recommendation, offer to execute:
- **Remove inert rule**: `rm .claude/rules/{{file}}` (with confirmation)
- **Narrow glob**: edit frontmatter to restrict to actual file patterns
- **Add missing rule**: create `.claude/rules/{{name}}.md` with suggested globs
- **Split overbroad rule**: extract stack-specific content to narrower-glob rule

Only execute with user confirmation. Show diff before applying.

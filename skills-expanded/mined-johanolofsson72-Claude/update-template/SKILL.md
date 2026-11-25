---
name: update-template
description: Searches online for the latest Claude Code best practices, changelog, and recommendations, then updates this template repo's structure accordingly. Use when you want to keep the template up to date with the latest Claude Code features.
argument-hint: "[--dry-run] [--focus hooks|skills|agents|rules|docs|settings]"
allowed-tools: WebSearch, WebFetch, Read, Glob, Grep, Edit, Write, Bash, Agent
---

# Update template repo with latest Claude Code best practices

## Arguments

- `--dry-run` — Only report recommendations, don't change files
- `--focus <area>` — Focus on a specific area (hooks, skills, agents, rules, docs, settings, claude-md)

Parse arguments from `$ARGUMENTS`. Default: full update, live mode.

## Step 1: Online research (MANDATORY)

Search for ALL of the following using WebSearch. Run searches in parallel where possible:

1. "Claude Code changelog 2026 latest release notes"
2. "CLAUDE.md best practices configuration guide"
3. "claude code hooks PostToolUse PreToolUse Stop new hooks"
4. "claude code skills SKILL.md agent skills standard"
5. "claude code settings.json schema permissions deny"
6. "anthropic claude code new features update"
7. "context engineering claude code best practices"
8. "claude code community CLAUDE.md examples github"
9. "trufflehog latest CLI flags filesystem git scan only-verified best practices"
10. "npm audit fix --force breaking changes best practices 2026"

Collect ALL relevant findings before proceeding.

When the trufflehog/npm-audit findings land, reconcile them against `scripts/project-freshness.sh` (the local freshness pass). If trufflehog's CLI surface has shifted (renamed flags, changed `--only-verified`/`--results` semantics, new scan subcommands) or npm's audit/remediation guidance has moved, update that script and the matching Step 8c instructions in `scripts/sync-prompt.md` + the freshness step in `.claude/skills/sync-template/SKILL.md`. Keep all three in lockstep — they describe the same local-only check (never a CI/scheduled Action, per `.claude/rules/github-actions.md`).

## Step 2: Read current structure

Read these files from this repo:

- `CLAUDE.md`
- `.claude/settings.json`
- `.claude/docs/skills.md`
- `.claude/docs/workflows.md`
- `.claude/docs/conventions.md`
- `.claude/rules/*.md` (all files)
- `.claude/agents/*.md` (all files)
- `.claude/skills/*/SKILL.md` (all files)

## Step 3: Gap analysis

Compare online findings (step 1) with current structure (step 2). Identify:

1. **New features** that should be adopted
2. **Deprecated patterns** to remove or replace
3. **Improved patterns** to update
4. **New hooks/settings** to add
5. **Security improvements** missing
6. **Context optimizations** available
7. **New skill types** worth creating
8. **Freshness tooling drift** — does `scripts/project-freshness.sh` still use current trufflehog flags and npm audit guidance? (see step 1 queries 9–10)

## Step 4: Apply or report

### If `--dry-run`:
Write a detailed report in English with all findings and recommendations. Do NOT modify any files.

### If live mode:
1. Apply each recommended change using Edit tool (surgical changes only)
2. Write a summary of all changes made
3. Run `git diff` to show what changed

## Report format

```
## Update report (date)

### New features found
- [feature]: [description] → [action]

### Deprecated/changed patterns
- [pattern]: [what changed] → [action]

### Applied updates
1. [file]: [change]

### No changes needed
- [area]: [reason]

### Recommendations for next time
- [suggestion]
```

## Rules

- Communicate in English, code in English
- Preserve ALL project-specific customizations (marked with # PROJECT-SPECIFIC)
- NEVER change the fundamental structure without strong justification
- Priority: Security > Correctness > Simplicity
- When unsure: report instead of changing
- Focus on `$ARGUMENTS` area if specified, otherwise update everything

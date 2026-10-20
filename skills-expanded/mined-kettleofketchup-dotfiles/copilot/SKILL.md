---
name: copilot
version: 1.0.0
updated: 2026-05-18
description: GitHub Copilot PR review and custom instructions. Use when authoring copilot-instructions.md or .github/instructions/*.instructions.md, configuring Copilot code review, or syncing Copilot config from .claude/skills/.
---

# GitHub Copilot

## Overview

GitHub Copilot consumes custom instructions from a handful of well-known file paths and can be requested as a PR reviewer. This skill covers (1) where those files live and what frontmatter they accept, (2) how to enable / request code review (manual + automatic via Rulesets), and (3) the pattern for keeping Copilot's repo instructions in lockstep with this user's canonical `.claude/skills/` content rather than duplicating it.

This skill complements the [github](../github/SKILL.md) skill, which covers `gh` CLI and Actions workflows.

## Custom instructions: file locations (cheat sheet)

| File | Scope | Precedence (lowest → highest) |
|------|-------|------------------------------|
| Org Settings → Copilot → Custom instructions | Whole org | 1 (org) |
| `.github/copilot-instructions.md` | Whole repo | 2 (repo) |
| `.github/instructions/NAME.instructions.md` | Path-scoped (`applyTo` glob) | 2 (repo, layered) |
| `AGENTS.md` (anywhere) / `CLAUDE.md` / `GEMINI.md` (root) | Agent-specific | 2 (repo) |
| GitHub.com → user profile → Copilot settings | Per-user | 3 (personal, wins) |

All applicable sets are layered into the request; personal beats repo beats org on conflict. PR review specifically loads instructions from the **PR's base branch**.

See [references/instructions-files.md](references/instructions-files.md) for the full frontmatter spec, glob syntax, and length/scope guidance.

## Copilot code review

### Manual review request

```bash
# Request Copilot on PR creation
gh pr create --reviewer @copilot

# Or on an existing PR
gh pr edit PR-NUMBER --add-reviewer @copilot
```

Web UI: PR → Reviewers → **Copilot**. Re-review after a new push by clicking the refresh icon next to Copilot's name (it does NOT auto re-review).

Copilot always posts a **"Comment" review** — never Approve / Request changes — so it never blocks merge or counts toward required approvals.

### Automatic review via repository ruleset

`Settings → Rules → Rulesets → New branch ruleset` → enable **"Automatically request Copilot code review"**. Optional sub-settings: **"Review new pushes"**, **"Review draft pull requests"**. This is an independent rule — no need to also enable "Require a pull request before merging".

**Cost warning (June 1, 2026):** Copilot code review runs will start consuming GitHub Actions minutes. Surface this when proposing org-wide auto-review.

See [references/pr-review.md](references/pr-review.md) for personal/org scope click-paths, plan requirements (Pro / Pro+ / Business / Enterprise), unsupported file types, and behavior nuances (dismissals, repeats).

## Bridging Copilot → `.claude/skills/` (the syncing pattern)

**Core principle:** Treat the user's `.claude/skills/` content as canonical. Copilot instruction files should be lean *summaries* that point to the corresponding skill file for full detail. Do not paste skill content verbatim — that creates two sources of truth and guarantees drift.

The pattern, applied to any repo with `.claude/skills/`:

1. Add a top-of-file pointer in `.github/copilot-instructions.md` listing the relevant skills with a one-line description and the path (`.claude/skills/<name>/SKILL.md`). When Copilot Chat has the repo attached as context, the user can pull those up; for PR review, the summary itself is what Copilot acts on.
2. For each Claude skill with a clear file-pattern scope (e.g., backend tests, frontend forms), create a sibling `.github/instructions/<skill>.instructions.md` with `applyTo:` matching the same paths and a 3–10 line summary of the rules Copilot must respect.
3. End each Copilot instruction file with: `Canonical source: .claude/skills/<skill>/SKILL.md — update there first.`

See [references/syncing-from-claude-skills.md](references/syncing-from-claude-skills.md) for the full pattern, worked DraftForge examples (logging, brand, testing), and `AGENTS.md` / `CLAUDE.md` interplay.

## Maintenance workflow

When a `.claude/skills/<name>/SKILL.md` changes a rule that Copilot also needs to know:

1. Update the Claude skill first (the canonical source).
2. Update the matching Copilot file (`.github/copilot-instructions.md` summary line and/or the `.github/instructions/<name>.instructions.md` summary).
3. If the rule changed scope, update `applyTo:` globs.
4. PR review uses base-branch instructions — verify your changes land on the branch reviewers' PRs target (usually `main`).

See [references/maintenance-workflow.md](references/maintenance-workflow.md) for the full checklist, drift-detection patterns, and the common gotcha where `.github/copilot-instructions.md` has been misplaced under `.github/instructions/` (Copilot ignores it there).

## Common gotchas

- **Wrong path silently ignored.** `.github/instructions/copilot-instructions.md` (nested) is NOT loaded as the repo-wide file — it must be at `.github/copilot-instructions.md`. A nested file is treated as a regular `.instructions.md` (and likely missing `applyTo:`).
- **Length cap.** Repo instructions should stay under ~2 pages. Trim aggressively; push detail into Claude skills.
- **PR review re-runs cost minutes.** After June 1, 2026, every push that triggers re-review consumes Actions minutes — leave "Review new pushes" off unless the cost is justified.
- **Excluded file types.** Copilot review skips `package.json`, lock files, log files, and SVGs.

## Resources

- [references/instructions-files.md](references/instructions-files.md) — file paths, frontmatter (`applyTo`, `excludeAgent`), glob syntax, precedence
- [references/pr-review.md](references/pr-review.md) — manual / personal / repo / org review setup, behavior, plan requirements
- [references/syncing-from-claude-skills.md](references/syncing-from-claude-skills.md) — the bridging pattern with worked examples
- [references/maintenance-workflow.md](references/maintenance-workflow.md) — keeping Copilot config in lockstep with `.claude/skills/`

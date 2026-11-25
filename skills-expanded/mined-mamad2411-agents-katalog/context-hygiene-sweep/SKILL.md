---
name: context-hygiene-sweep
description: Use this skill to audit and clean up CLAUDE.md files and .claude/ capabilities across a folder of projects — reconciling project instructions against global ~/.claude rules, stripping low-signal content, externalizing LLM-agnostic docs to CONTEXT.md, and promoting reusable skills to the canonical ambient-library. Trigger on "clean up the CLAUDE.md files", "reconcile project instructions with globals", "sweep this folder for skills worth promoting", "audit my repos' claude files", "promote project skills to the library", or any request to deduplicate/tidy AI instruction files across multiple projects, even if the user doesn't name CLAUDE.md explicitly.
---

# Context Hygiene Sweep

Reconciles project-level CLAUDE.md files against global rules, prunes low-signal
content, and promotes reusable `.claude/` capabilities to the canonical
ambient-library. Built from the 2026-07-06 GitHub-folder sweep.

## CRITICAL gotchas (read before touching anything)

1. **Standalone repos are exempt from dedup.** Repos shipped to clients (or
   otherwise required to run without the user's global `~/.claude` scope) must
   keep every instruction in-repo, even ones that duplicate global rules —
   globals don't travel with the repo. Before editing anything, ask the user
   which repos are client-shipped/standalone, AND check memory (known:
   Jansen* and GEARS/* under the GitHub folder). Skip those entirely, or edit
   only for self-contained improvements. This was violated once and required
   restore-from-backup.
2. **Check recoverability before editing.** Many CLAUDE.md files are
   gitignored or untracked — an edit is effectively destructive. For each file,
   note its restore path first: git-tracked? hot-cache mirror
   (`/Users/loudalo/ambience-claude/...` or `~/` mirror of the Extreme Pro
   path)? archive/zip copy? If none, copy the original to the scratchpad
   before editing.
3. **Skip backups and copies.** Never edit anything under `*-Archives/`,
   `_repo_consolidation/`, `.claude/worktrees/`, `dist/`, dated snapshot
   folders (e.g. "Project 250712.2155"), or inside zips. Cleaning backups is
   churn and pollutes the diff between live and dead code.
4. **Commit, never push.** Ambient-library promotions get committed with a
   message listing the skills; pushing waits for explicit user permission.

## Workflow

### 1. Scope and log (code)

- `find` all CLAUDE.md files and `.claude/` dirs (exclude node_modules, .venv,
  and everything in gotcha 3). Record sizes.
- Create a progress/log file at the sweep root (e.g. `cleanup-claudemd-log.md`)
  with: scope decisions, phase checklist, a "Canonical additions log" section,
  and the exclusion list. All agents append to it. This file is the memory —
  context degrades over a long sweep.
- Read `ambient-library/library/catalog.yaml` to know what's already canonical,
  and `ambient-library/docs/MANAGEMENT.md` for the promotion flow.

### 2. Reconcile CLAUDE.md files (delegate: 1–2 parallel general-purpose agents)

Batch files by area. Each agent's prompt must front-load: exact file list, the
"edit only these files / never delete / no commits" constraints, and a summary
of what the global rules already cover (so it knows what counts as duplicate).
Per file:

- **Delete** restatements of global rules; keep only the project-specific
  variant (e.g. the exact test command, not "write tests first").
- **Delete** low-signal filler: tool/framework explanations, generic best
  practices, empty scaffolding, "This file provides guidance..." headers.
- **Keep** high-signal only: architecture facts, exact build/run/test
  commands, environment gotchas, non-obvious domain constraints.
- **Move** substantial LLM-agnostic content (architecture, domain context,
  data models) to `CONTEXT.md` in the project root, leaving a one-line pointer
  in CLAUDE.md. A pointer-only CLAUDE.md is a success.
- Third-party clones: trim conservatively — upstream docs may be the
  deliverable.
- Append one log line per file: `- path — removed/kept/moved (before→after)`.

### 3. Assess and promote capabilities (delegate: 1 agent)

For every project-local skill/command, read its actual description (never
judge by folder name) and classify:

- **project-specific** — wired to one project's paths/schema/data → leave.
- **duplicate-of-canonical** — flag "safe to delete locally", don't delete.
- **stock-skill** — Anthropic public skills (skill-creator, mcp-builder,
  theme-factory, web-artifacts-builder, docx family) → skip.
- **promote-later** — reusable idea but needs real path generalization →
  list it, don't ship a broken skill.
- **promote** — reusable class of work not already covered. Follow
  MANAGEMENT.md exactly: `library/<name>/instructions.md` (+ references),
  one-line `catalog.yaml` entry (+ namespace if it fits), `SKILLS.md` entry,
  bump both wrapper plugin.json versions once at the end, commit (no push).
  Only trivial generalizations inline (e.g. swap a hardcoded dependency for
  "ask the user").

After each promotion: rename the source folder with a `.canonical` suffix and
log `- <name> | <source folder> | <catalog one-liner>` in the sweep log.

### 4. Verify and report

- Confirm standalone repos untouched (`git status` where tracked; line counts
  vs originals where not).
- Update the log's phase checklist.
- Final report: lines removed, files edited/kept, promotions table with commit
  hash, duplicates flagged, promote-later items, and structural cleanup
  recommendations (snapshot sprawl, folder-contract standardization, etc.).

## Step classification

Scoping/finding/logging/verification: **code**. Per-file signal judgment and
skill classification: **inference** (unbounded, context-dependent — that's why
agents get the global-rules summary in-prompt). Promotion mechanics: **code**
per MANAGEMENT.md.

# ticket-system-specs

## Project Purpose

This repository contains a **specification file** (`specs.md`) that, when fed to Claude Code (Opus 4.6), generates a complete **Ticket Workflow System** — a file-based, AI-native project management system that runs entirely inside git repos via Claude Code.

**This is NOT the ticket system itself.** This is the generator spec. The generated output (agents, skills, scripts) gets installed into a user-chosen Claude Code configuration directory (`$CLAUDE_DIR`, defaults to `~/.claude/`) and used in other projects.

## Repository Structure

```
ticket-system-specs/
├── CLAUDE.md       # This file — project guide for Claude Code sessions
├── README.md       # Project overview for developers and users
└── specs.md        # The self-contained generation prompt
```

Only these three files belong in this repo. Generated output should not be committed here.

## How to Generate the Ticket System

1. Open a **fresh** Claude Code session with Opus 4.6 (1M context).
2. Feed the entire `specs.md` as input.
3. Claude Code reads the spec and generates the full file tree.

**Expected output:**
- `ARCHITECTURE.md` — reformatted spec as architecture doc
- `install.sh` — prompts for install directory, then copies agents/skills to `$CLAUDE_DIR`
- `init-project.sh` — initializes a new project with ticket structure
- 6 agent files in `agents/` (reader, editor, planner, coder, verifier, ops)
- 14 skill directories in `skills/` (conventions + 13 slash commands), each containing `SKILL.md`

## Iterative Workflow

Development follows two feedback loops:

### Inner Loop — Spec Refinement

```
edit specs.md → generate → validate checklist → note failures → edit specs.md
```

Use this for structural and format issues (wrong frontmatter, missing fields, incorrect permission mappings).

### Outer Loop — Functional Testing

```
generate → install to $CLAUDE_DIR → init test project → run slash commands → observe → update specs.md
```

Use this for behavioral issues (runtime errors, agent interactions, edge cases in the command pipeline).

### Cycle Steps

1. **Edit** — Modify `specs.md` to refine requirements, fix issues, or add detail.
2. **Generate** — Feed updated spec to a fresh Claude Code session.
3. **Validate** — Run the validation checklist (see below).
4. **Test** — Execute `install.sh`, run `init-project.sh`, try slash commands.
5. **Record** — Note what failed or needs improvement.
6. **Iterate** — Return to step 1 with findings.

### Parallel Spec Work

When multiple spec changes are in flight simultaneously:

- **Use feature branches** for concurrent spec changes to avoid conflicts on `specs.md`.
- **Scope changes to specific sections** to minimize merge conflicts. Each section is self-contained enough that two people can work on different sections in parallel.
- **Run `validate-spec.sh` before merging** to catch cross-reference drift (e.g., a command referencing an agent that was renamed in another branch).
- **Coordinate on section 4 (Command Pipeline)** — this is the most interconnected section and the most likely source of merge conflicts.

## Validation Quick Reference

### Smoke Test (after every generation)

- [ ] All required files present by name (see specs.md section 8 structural checklist)
- [ ] Every agent has `skills: [ticket-system-conventions]` in frontmatter
- [ ] Every skill has `context: fork` and `agent: <name>` in frontmatter
- [ ] `ticket-system-conventions` has `user-invocable: false`
- [ ] Both scripts have `#!/bin/bash` and are executable
- [ ] `hooks/validate-git-worktree.sh` exists and is executable
- [ ] `hooks/instrument-pre.sh` and `hooks/instrument-post.sh` exist and are executable
- [ ] No hardcoded ticket prefixes anywhere
- [ ] No hardcoded `~/.claude/` paths — all use `$CLAUDE_DIR`

### Deep Validation

Refer to **specs.md section 8** for the full validation checklist covering:
- Frontmatter correctness across all agents and skills
- Permission model assignments (plan / bypassPermissions)
- Script functionality (install.sh with directory prompt, hook installation, init-project.sh)
- Hook validation (worktree path validation, jq fallback, no hardcoded prefixes, instrumentation hooks with stats-disabled fast exit)
- Instrumentation (instrument-pre.sh and instrument-post.sh hooks registered in settings.json, stats config option, JSONL tool-call logging, phase-level timing in /ticket-system-run, stats written on early failure, .tickets/stats/ gitignored by init-project.sh)
- Command behavior (stop-on-conflict behavior in schedule and plan — stops with structured message directing to /ticket-system-edit, NEVER modify code/findings in verify, prerequisites in implement/merge, /ticket-system-run chains plan→implement→verify→merge with post-step verification and stop-on-failure and optional phase-level stats, retry counter blocks implement after $MAX_RETRY consecutive verify failures, drift detection in implement compares modified files against plan and logs [DRIFT] entries, verify reports [DRIFT] entries prominently, research tickets use research-plan.md/validation-criteria.md/findings.md instead of implementation-plan.md/test-plan.md/code, /ticket-system-run-all reads roadmap in position order and chains /ticket-system-run per ticket with stop-on-failure and summary report, plan writes optional .context.md after codebase analysis for downstream agents to skip redundant exploration)

## Rules for Working on This Repo

- **Only modify** `CLAUDE.md`, `README.md`, and `specs.md` — no other files belong here.
- **Keep `CLAUDE.md` in sync with `specs.md`** — whenever `specs.md` is modified, review `CLAUDE.md` and update it to reflect any changes that affect project guidance, workflow descriptions, or design decisions.
- **Keep `specs.md` self-contained** — it must work as a single prompt with no external context.
- **Preserve the 9-section structure** of `specs.md` (Configuration Variables, Vision, Architecture, Data Model, Commands, Generation Rules, Decisions, Future, Validation). Section 0 (Configuration Variables) is the only section users should customize before generation.
- **Commit messages** should describe what aspect of the spec changed (e.g., "Refine agent permission model" not "Update specs.md").

## Key Design Decisions

These are settled (documented in specs.md section 6) and should not be revisited:

- File-based system, no external dependencies (no SaaS, no databases)
- 6 agents grouped by permission profile, not 1 per command
- Permission elevation via `context: fork` + agent — main session stays in default mode
- Git worktree created inside `.worktrees/` (gitignored) at `/ticket-system-plan`, used through `/ticket-system-merge` — all ticket work isolated from main, `tickets/ongoing/` on main is always empty, worktrees inside the project so dedicated tools work without permission prompts
- Verify completes ticket on PASS (moves to `completed/` in worktree), merge just lands the branch
- Schedule and plan use stop-on-conflict -- clean operations proceed silently, conflicts stop with a message directing to `/ticket-system-edit`. No interactive gates or `--yes` bypass
- Artifacts co-located with tickets in `tickets/ongoing/PREFIX-XXX/`
- Fine-grained Bash patterns for plain git + PreToolUse hook for `git worktree`, `git -C`, and `mkdir` worktree validation
- Single-developer workflow by design — multi-developer usage on the same repository is not supported
- Forked agent contexts do not inherit parent conversation history — include relevant context in command arguments

## Timestamp Rule

All ticket timestamps (`created`, `updated`, log entries) **must** be obtained by running the `date` command (e.g., `date '+%Y-%m-%d %H:%M:%S'`). Never rely on the model's internal knowledge of the current date — it can be wrong.

## Constraints

- Uses Claude Code **Skills format** (not legacy `.claude/commands/`)
- `ticket-system-conventions` skill must not exceed **500 lines**. When nearing the limit (400+ lines), plan artifact formats (`implementation-plan.md`, `test-plan.md`, `research-plan.md`, `validation-criteria.md` templates) can be extracted into `ticket-system-conventions-extended`. See specs.md section 6 D-13 for the full split strategy.
- Skill descriptions must be under **250 characters**
- All files in **English**
- **POSIX-only** dependencies (bash, git, standard utils) — no npm, no pip

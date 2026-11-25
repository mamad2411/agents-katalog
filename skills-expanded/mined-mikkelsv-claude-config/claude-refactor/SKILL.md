---
name: claude-refactor
description: Audit and improve Claude skills, commands, scripts, and configuration
---

# Claude Config Audit

Audit skills, commands, scripts, rules, and agents. Fix bugs, stale refs, permission gaps, and misplacements.

Scripts: `~/.claude/scripts`

## Phase 1 — Inventory

Launch 2 parallel agents (`model: "sonnet"`):

**Agent 1 — Global**: read all `~/.claude/skills/`, `~/.claude/commands/`, `~/.claude/scripts/`, `~/.claude/rules/`, `~/.claude/agents/`, README.md, settings.json, settings.template.json, CLAUDE.md. Record: path, purpose, references.

**Agent 2 — Project** (skip if not in a project): read `.claude/skills/`, `.claude/commands/`, `.claude/rules/`, `.claude/skill-config/`, CLAUDE.md. Record same, plus which global skill each project skill forks, if any.

## Phase 2 — Review

Launch 3 background agents (`model: "sonnet"`) with the inventory:

**Agent A — Content Quality**:

- **Correctness**: logic flow, script param mismatches, stale references, JSON output mismatches.
- **Script extraction**: multi-line bash blocks that should be scripts (especially if repeated). Not single-liners.
- **Token efficiency** (per `wf-tight-claude-config.md`): rules and CLAUDE.md load every session; skills and commands load on invocation. Flag verbose prose, redundant tables, repeated explanations, cross-file duplication, and examples that restate the directive.

  **Aim below the cap, don't just check it.** A rule over **50 lines** is a finding that needs a reason or a trim. Between 25 and 50, don't report mere length — report it only when the extra lines are *justification* (a measurement, a war story, a "why this matters" paragraph) rather than directive, since that content belongs in `README.md` and is being paid for every session. Skills: ≤ ~80 lines unless genuinely needed.

  Rank by **always-on bytes**, not line count. A 40-line always-loaded rule costs more than a 200-line skill nobody invokes this week, and a `paths:`-scoped rule costs nothing until a matching file is opened.

**Agent B — Structure & Permissions**:

- **Permissions**: walk skills/commands, find Bash/Write/Edit calls not covered by settings.json globs. Draft safe patterns. Update template if portable.
- **Placement**: global skills with project-specific assumptions? Project skills that are generic? Commands that should be skills or vice versa?
- **Parallelization**: independent read-only phases that could be parallel agents? Write-independent phases safe for worktrees?

**Agent C — Sync & Docs**:

- **Fork drift**: compare each project fork to the global skill it copies. Generic improvements in the fork → propagate **up** to global. Global ahead → the fork is stale. Project-specific divergence inside `<ProjectSpecific>` → expected.
- **Invisible drift is the one to hunt.** Global wins on same-named skills, so a fork that has drifted ahead runs only for colleagues, never for its author — nothing surfaces it. Flag any fork whose non-block content exceeds its global counterpart.
- **README accuracy**: `~/.claude/README.md`. All items listed? Descriptions accurate? Directory layout correct? Script catalog complete?

## Phase 3 — Fix

**Auto-fix** (apply directly): stale references, script param mismatches, JSON format mismatches, safe permission patterns, README corrections.

**Ask user** (via `AskUserQuestion`): placement changes, script extraction, fork-drift propagation, parallelization restructuring. Apply confirmed changes immediately.

## Phase 4 — Documentation

Update `~/.claude/README.md` to reflect all Phase 3 changes. Update Global Rules section if rules changed. Note `settings.template.json` changes for cross-machine sync.

## Phase 5 — Summary

| Category | High | Medium | Low |
| --- | --- | --- | --- |
| Correctness | N | N | N |
| Script opportunities | N | N | N |
| Permission gaps | N | N | N |
| Placement | N | N | N |
| Parallelization | N | N | N |
| Fork drift | N | N | N |
| README accuracy | N | N | N |

List changes made, deferred items, and settings template updates. Ask: **Push now** / **Review first** / **Done**.

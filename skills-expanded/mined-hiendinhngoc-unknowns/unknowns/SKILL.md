---
name: unknowns
description: Lifecycle orchestrator for the unknowns plugin. Detects the current phase of work (pre-implementation, mid-implementation, pre-merge) and routes to the right technique skill. Use when the user says "/unknowns", "know my unknowns", or is unsure which unknowns skill applies.
version: 1.0.0
author: Hien Dinh
license: MIT
---

# Unknowns Orchestrator

Pure router. Detect the phase, invoke the right skill via the Skill tool.
If this agent has no skill-invocation tool, read that skill's SKILL.md and
follow it directly. No technique logic lives here.

## Phase detection

Trust explicit conversation intent first: requests to review/merge, reports of a
plan deviation, porting language, or prototype language route directly. Use git
only when intent is not clear.

When git evidence is needed, resolve the comparison base in this order: the
current branch's configured upstream; `refs/remotes/origin/HEAD`; an existing
local `main`; then `master`. Verify every candidate before using it.

Then check, in order:

Incidental dirt is not evidence: modifications limited to generated or
IDE-managed files (`*.pbxproj`, lockfiles, `.DS_Store`, build outputs) do not
indicate a task in flight — treat such a worktree as clean.

1. **Pre-merge:** the user expresses review/merge intent, or HEAD has commits
   ahead of the resolved base and the worktree has no tracked modifications →
   invoke `unknowns:merge-quiz`.
2. **Mid-implementation:** tracked modifications exist that plausibly belong to
   the task at hand, or the conversation shows
   an agreed plan being executed → if a deviation was just discussed, invoke
   `unknowns:log-deviation`; otherwise report that no concrete deviation is
   available to log and present the three pre-implementation techniques without
   invoking one speculatively.
3. **Pre-implementation:** no changes yet for the task at hand → ask ONE
   question: what kind of unknown are they facing?
   - Unfamiliar system / risky area → invoke `unknowns:blindspot`
   - Porting or adapting existing code → invoke `unknowns:verify-ref`
   - Undecided UX or behavior → invoke `unknowns:mock`

## Rules

- Route and invoke — never inline a technique's logic here.
- If git state and conversation disagree, trust explicit conversation intent.
- Outside a git repo, route from conversation; ask one phase question only when
  no intent or target can be inferred.
- Skill names here use the `unknowns:` namespace (Claude Code plugin install).
  If the skills were installed flat (Codex, OpenCode: `cp -r skills/*`), they go
  by their bare directory names — `blindspot`, `verify-ref`, `mock`,
  `log-deviation`, `merge-quiz`.

---
name: full-feature
description: "End-to-end feature workflow — plan, scaffold, execute, verify, and merge, phase by phase."
disable-model-invocation: true
---

# Workflow: Full Feature

## Overview
End-to-end workflow for implementing a feature from plan to merged code.

## Steps

### 1. Product Definition (optional, for UI-heavy features)
If the feature has a user-facing interface:
- Run `/prd` to formalize requirements into a structured PRD
- Run `/ux-spec` to design the experience through 6 UX passes (mental model, IA, affordances, cognitive load, state design, flow integrity)
- Skip this step for backend-only or technical features

### 2. Plan
- Use the `planner` agent
- Skills loaded: `plan-and-scope`, `phase-breakdown`
- The planner will consume PRD and UX spec artifacts if they exist
- Output: `plan.md` with phased tasks
- Review and iterate on the plan before proceeding

### 2b. Scaffold (new projects only)
If this is a new project with sub-repos to create:
- Use `/scaffold` from the root planning folder
- Creates sub-project directories, git inits, installs profiles
- Skip this step for features in existing repos

### 3. Execute — MVP Build

For initial builds where you're taking a plan from zero to working application, work directly on main. No branches or worktrees needed — there's nothing to protect yet.

Repeat for each phase:

**Execute:**
- Start a Claude session in the sub-project
- Tell it: "Execute phase N of the plan"
- The executor agent reads plan.md and implements all tasks — it does **not** commit; changes stay uncommitted until verification passes

**Review:**
- Start a NEW Claude session in the same directory
- Tell it: "Review phase N against the plan"
- The reviewer agent checks the work and produces a verification report
- Fix any FAIL items, re-verify if needed

**Commit and move on:**
- On PASS, the review session commits the phase (implementation + verification report) to main — the session that owns the work commits (in the hands-off flows below, that's the lead)
- Between phases, the commit history provides a natural review point
- If this phase produced API changes, generate the integration summary for frontend phases
- Continue to the next phase

**Hands-off alternatives:**
- `/autopilot` — for pre-planned work. Executes all plan.md phases: implement → test → verify → commit. Stops on FAIL — run `/autopilot N` to resume.
- `/orchestrator` — for broader work. Accepts inline tasks or plan.md, supports parallel execution, auto-phasing, and per-task model overrides. Use when tasks need decomposition or research.

### 4. Execute — Ongoing Feature Work

Once you have a working application and are building new features on top of it:

**Single feature:** check out a branch, execute, review, PR, merge. Simple.

**Multiple independent features in parallel:** use git worktrees (see the `/worktrees` skill). Each feature gets its own worktree so you can switch between them without stashing or losing context. This is where worktrees earn their keep.

## Tips
- Don't skip the planning step — it saves time overall
- Keep phases small enough to review in one sitting
- The verification step catches things you'd miss in self-review
- Update the plan as you learn — it's a living document

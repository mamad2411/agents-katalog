---
name: github-next-wave-orchestrator
description: "Analyze a GitHub repo's issue/PR/code state, produce a status report, and propose or execute the next wave of work with parallel agents. USE WHEN asked 'where is this repo now?', to summarize issues and decide what's next, to run the next wave, or for ongoing delivery orchestration from issues."
requiredSources:
  - github
alwaysAllow:
  - "Read"
  - "Bash"
cluster: git-pr-ops
version: 1.0.0
---

# GitHub Next Wave Orchestrator

> **Conductor integration.** This is the **Execute** stage of the conductor's `github-delivery` modality
> (see `conductor-core` §4): `swarm-architect` plans → this orchestrator dispatches each task to its
> `human` / `copilot-swe-agent[bot]` lane → `ship-battery.mjs` gates (fail-closed) → `loop-feedback.mjs`
> closes. `resolve-task.mjs --modality github-delivery` resolves each task's capability cluster + lane.
> Full `.github/` Copilot-bootstrap templates live in the source repo
> `~/.../thoughtseed/github-next-wave-orchestrator/`.

Use this skill when the user asks for:
- “Where is this repo right now?”
- “Summarize issues and tell me what to do next”
- “Run the next wave”
- Ongoing delivery orchestration from GitHub issues

---

## Core Outcome

Produce two things:
1. **Status Report** — current reality of the repository (issues, PRs, velocity, risks)
2. **Next Wave Plan** — the highest-impact, executable batch of work (parallel where possible)

If user asks to execute, run the approved next wave and report progress.

---

## Mandatory Skill Stack

Before doing work, activate and follow in order:
1. `using-superpowers` — meta-skill gating; if unavailable, proceed but note it.
2. `executing-plans` — batch and checkpoint discipline; required.
3. `dispatching-parallel-agents` — use for independent tasks; if unavailable, execute sequentially and note ordering rationale explicitly.

Priority rule: correctness and safety over speed. If a sub-skill is missing, fall back to its documented behavior inline and call it out in the execution log.

---

## Inputs to Confirm (if missing)

- Repository owner/name
- Branch strategy (default branch, release branch if any)
- Time horizon for status (last 7/14/30 days)
- Definition of “next wave” (bugfixes, roadmap, reliability, debt, launch)

If these are not provided, proceed with sensible defaults and state assumptions.

---

## Execution Protocol

### Phase 1 — Repo Reality Scan

Gather evidence (do not guess):
- Open/closed issues, priority labels, age distribution
- Open PRs, merge queue, blocked PRs, stale PRs
- Recent commit activity and release tags
- CI/check run health on active PRs
- Dependency/risk signals from issue text and labels

Always anchor conclusions to observable data.

If the repo has zero open issues and zero open PRs, note this explicitly and skip to Phase 3 — propose seed issues based on the codebase state (missing tests, stale deps, undocumented APIs).

### Phase 2 — Status Synthesis

Generate a concise **Status Report** with:
- **Repo Pulse:** current throughput and momentum
- **Issue Landscape:** grouped by severity, theme, owner, staleness
- **Delivery Risks:** blockers, bottlenecks, missing ownership, CI instability
- **Readiness Score:** Green / Yellow / Red with rationale.
  - Green: no blocking PRs, CI passing, <3 P0 issues open, active commits in last 7 days.
  - Yellow: any one of — CI flaky, 1–2 blocking PRs, 3–6 P0 issues, stale >14 days.
  - Red: CI broken, merge queue blocked, >6 P0 issues, or no commits in >14 days.

### Phase 3 — Next Wave Design

Create a prioritized execution wave using this ranking order:
1. Unblocks other work (dependency chains)
2. Fixes broken CI or a P0 bug
3. High impact, reversible (safe to ship fast)
4. High impact, irreversible (needs review gate)
5. Low impact — defer unless trivial

Pick the top 3–7 by this ranking; aim for at least 2 that can run in parallel.
- Define success criteria and verification per task
- Include dependencies and ordering constraints
- Keep blast radius minimal

### Phase 4 — Parallel Dispatch (when executing)

For independent tasks:
- Dispatch parallel agents/subtasks with full context per task
- Use one focused prompt per task (objective, constraints, validation)
- Collect outputs
- Run mandatory spotcheck for consistency/completeness

For dependent tasks:
- Execute sequentially with checkpoints.

### Phase 5 — Review Checkpoint

After each batch, report:
- Completed items
- Verification evidence (tests/checks/logs/diffs)
- Remaining risks
- Recommended next batch

Say: **“Ready for feedback.”**

---

## Output Contract

Use this structure:

### 1) Status Report
- Scope and assumptions
- Repo Pulse
- Issue Landscape
- Active PR & CI Health
- Top Risks / Blockers
- Readiness Score

### 2) Next Wave
For each item:
- Priority
- Why now
- Owner/agent lane
- Execution type: Parallel or Sequential
- Done criteria
- Verification steps

### 3) Execution Log (if executed)
- What ran
- What passed/failed
- Follow-ups

---

## Guardrails

- Never fabricate repository state.
- Never close/edit issues or merge PRs without explicit user approval.
- If evidence is incomplete, call it out and proceed with confidence levels.
- Prefer elegant, minimal-impact solutions over broad refactors.
- Do not mark done without verification evidence.

---

## Definition of Done

All three sections of the Output Contract delivered, with verification evidence for any executed work, ending with: **"Ready for feedback."**

## Loading spokes on demand

To keep CLI startup context lean, this cluster's spokes are **not** separately registered as skills — only this orchestrator and its `*-core` are enumerated. When you route to a spoke named above, **load it on demand** by reading its file:

`~/.agents/skill-clusters/skills/<spoke-name>/SKILL.md`  (or `skills/<spoke-name>/SKILL.md` inside the skill-clusters repo).

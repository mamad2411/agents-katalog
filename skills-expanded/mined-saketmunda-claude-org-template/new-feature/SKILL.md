# skills/new-feature/SKILL.md
# Slash command: /new-feature [feature name or description]
# Trigger: User types /new-feature for a single, contained feature

---

## What This Does

A lighter-weight workflow for single features that may touch 1–2 lanes. Compared to `/sprint`:
- Still has an approval gate
- Still spawns isolated agents
- Still runs reviewer agents
- Does NOT require tech-lead decomposition for simple, already-clear tasks

Use `/sprint` for multi-agent, multi-goal sprints.
Use `/new-feature` for a single, well-scoped feature.

---

## When to Use

- Adding a new API endpoint + frontend component
- Implementing a single user story end-to-end
- Any feature where you already know the scope (no decomposition needed)

---

## Step-by-Step

### Step 1 — Scope Check

Ask (if not already clear from the request):
- Which lanes are involved? (backend / frontend / devops / database?)
- Are there dependencies between lanes? (e.g. DB schema before API before UI)
- Is there existing code to characterize before changing? (if yes, QA runs first)

If scope is unclear after one question: prompt engineer for clarification before proceeding.

### Step 2 — Approval Gate

Present the execution plan:

```
## Feature Plan — [feature name]

**Lanes involved:** [backend, frontend, ...]
**Execution order:**
1. [qa-engineer] Characterization tests for [existing code being modified] — if applicable
2. [database-engineer] Migration for [new column/table] — if applicable
3. [backend-engineer] [specific task: endpoint, service method, etc.]
4. [frontend-engineer] [specific task: component, page, hook]
5. [devops-engineer] [IaC update if new resource needed]

**Parallel:** Steps [N] and [N] can run simultaneously (no shared files).

**Approve? (yes / adjust)**
```

### Step 3 — Execute

Spawn agents per the approved plan:
- Sequential where there are dependencies
- Parallel (worktree isolation) where lanes are independent

### Step 4 — Review

After all writer agents complete:
- Spawn `security-auditor` and `modernization-reviewer` in parallel on each PR
- Collect verdicts

### Step 5 — Report

```
## Feature Complete — [feature name]

### PRs
| PR | Agent | CI | Security | Architecture |
|---|---|---|---|---|

### Ready to merge in order:
1. [PR #N] — [agent]
2. [PR #N] — [agent]

### Findings (if any)
[Reviewer output]
```

---

## Refusal Triggers

- Feature is too vague to scope after one clarifying question — ask before starting
- Feature spans more than 3 lanes with complex dependencies — use `/sprint` instead
- Working tree is dirty — stop and report

---

## Notes

If mid-execution an agent discovers the scope is larger than expected (e.g. the API change requires a DB migration that wasn't planned), the agent files a cross-lane request and the tech-lead adds the new task. The engineer is notified before the new task runs.

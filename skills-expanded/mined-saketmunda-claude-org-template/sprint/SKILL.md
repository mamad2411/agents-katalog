# skills/sprint/SKILL.md
# Slash command: /sprint [goal]
# Trigger: User types /sprint followed by a sprint goal description

---

## What This Does

Runs a full sprint coordination cycle:
1. Pre-flight git check
2. Tech-lead decomposes the goal into lane-specific tasks
3. Approval gate — engineer reviews and approves before any agent spawns
4. Fan-out: writer agents in parallel (worktree isolation)
5. Reviewer agents on each PR diff
6. Final report

---

## When to Use

- Starting a sprint with a defined goal
- Executing a multi-agent, multi-PR task
- Any work that spans more than one agent lane

---

## Step-by-Step

### Step 1 — Pre-flight

```bash
git status
git log --oneline -5
git fetch origin && git status
```

If working tree is dirty or branch is wrong: **STOP. Report to engineer. Do not proceed.**

### Step 2 — Tech-Lead Brief

Invoke `tech-lead` agent with the sprint goal. Tech-lead:
- Reads CLAUDE.md for current priorities and hard rules
- Reads ORG.md for lane ownership
- Decomposes into tasks with explicit agent assignments and dependency order

### Step 3 — Approval Gate (Non-negotiable)

Present the plan:

```
## Sprint Plan — [goal]

| # | Agent | Task | Files (expected) | Parallel? | Blocks/Blocked by |
|---|---|---|---|---|---|
| 1 | qa-engineer | Characterization tests for [X] | tests/X.test.ts | No | Blocks: #2 |
| 2 | backend-engineer | Implement [X] | src/services/X.ts | After #1 | Blocked by: #1 |
| 3 | devops-engineer | IaC for [X] | infra/X.tf | Yes (with #2) | — |

PRs expected: [N]
Agents in parallel (after QA gate): [list]

**Approve? (yes / adjust: [your change])**
```

**Do not spawn agents until the engineer says yes.**
If they adjust: revise and re-present.

### Step 4 — Spawn Writer Agents

After approval:
- Tasks with no dependencies: spawn in parallel with `isolation: "worktree"`
- Tasks blocked by another: wait for the blocking PR URL, then spawn
- QA characterization always runs first and blocks extraction tasks

Each agent receives:
- The specific task
- Relevant context from the plan
- The handoff format requirement (from `_shared/engineer-discipline.md`)

### Step 5 — Collect Handoffs

After all writer agents complete, tech-lead:
- Reads every handoff
- Checks for lane violations (flags any agent that edited outside its lane)
- Routes all cross-lane requests to the correct agent
- Queues any required follow-up tasks

### Step 6 — Reviewer Agents

For each PR produced, spawn in parallel:
- `security-auditor` — runs the security checklist
- `modernization-reviewer` — runs the architecture compliance checklist

Both run simultaneously. Collect both verdicts before reporting.

### Step 7 — Final Report

```
## Sprint Complete — [goal]

### PRs Produced
| PR | Agent | Status | Security | Architecture | Merge Order |
|---|---|---|---|---|---|
| #N | qa-engineer | Open / CI pass | — | — | 1st |
| #N | backend-engineer | Open / CI pass | PASS | WARN | 2nd |

### Reviewer Findings
[Paste both verdicts]

### Cross-lane Requests Resolved
[List — or "None"]

### Carried to Next Sprint
[Anything not completed — with reason]
```

---

## Refusal Triggers

Refuse to run if:
- Working tree is dirty (`git status` shows uncommitted changes)
- The engineer has not approved the plan
- Two tasks in the parallel group would touch the same file
- The sprint goal is too vague to decompose (ask for clarification first)

---

## Notes

- The approval gate is not optional. It exists because parallel agents executing against a wrong plan cost time to undo.
- Each worktree is isolated — agents cannot see each other's work mid-execution. Integration happens through the tech-lead after all complete.
- If a reviewer returns FAIL, that PR does not merge until the finding is resolved. Report this clearly to the engineer.

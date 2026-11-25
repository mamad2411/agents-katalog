---
name: subagent-driven-development
description: Use when executing implementation plans with independent tasks in the current session
---

# Subagent-Driven Development

Execute a plan by dispatching a **fresh implementer subagent per task**, a task review (spec + quality) after each, and a broad final review at the end.

**Core principle:** Fresh subagent per task + task review (spec + quality) + broad final review = high quality, fast iteration

**Why subagents:** You delegate to isolated-context agents. By precisely crafting their instructions, you keep them focused — and preserve your own context for coordination. **They should never inherit your session's context or history; you construct exactly what they need.**

## The Iron Rules

**Rulings, not stalls.** A running plan does not wait on a human. Conflicts, ambiguities, plan defects — decide them. The spec is the binding authority, the plan is its argument. Record every decision:
```
Ruling: <what you decided> — <why> — <what it costs if wrong>
```
A wrong ruling costs rework your partner can see and undo; a parked session costs their whole day.

**Four stops, and only these:** an irreversible/destructive operation; a security-sensitive action; a side effect outside this worktree (merge, push to shared branch, publish); a plan so broken that every path forward is a guess.

**Conversation memory does not survive compaction.** Controllers that lost their place have re-dispatched entire completed task sequences — the single most expensive failure observed. **Track progress in a ledger file, not only in todos.**

**Hand artifacts over as files.** Everything you paste into a dispatch prompt — and everything a subagent prints back — stays resident in your context and is re-read on every later turn.

**Never poll with short timeouts; never sit in one open-ended silent wait.** While you have local work (ledger, packaging reviews, reading reports), keep working. When genuinely idle, wait in bounded stretches (5–10 min), post one status line between stretches, and reconcile live children — chase any that finished without reporting.

## When to Use

| Condition | Use this | Else |
|---|---|---|
| Have implementation plan + tasks mostly independent + same session | **this skill** | — |
| No plan | brainstorm first | — |
| Tightly coupled tasks | manual execution | — |
| Parallel session (context switch ok) | `executing-plans` | — |

## The Loop (summary)

```
Setup → pre-flight conflict scan → [per task: dispatch → review → fix loop ≤5 → complete] → final review → finish
```

**Setup**: isolated worktree (`using-git-worktrees`); never on main/master without explicit consent. Create ledger `<repo>/.superpowers/sdd/<plan-basename>/progress.md`, first line `# SDD ledger — plan: <path>`. Read plan + its Spec. Pre-flight scan for task conflicts → **write a table, not a verdict**.

**Per task**: record `BASE` (`git rev-parse HEAD`) → dispatch implementer → handle report → dispatch task reviewer → fix rounds R of 5 (R≤3 resume implementer; R≥4 fresh implementer + more capable model) → scoped re-review → ledger completion.

**Final**: whole-branch review on the **most capable model**, ONE fix dispatch, one scoped re-review, adjudicate residuals.

**Model selection**: always specify explicitly (omitted = inherits your expensive session model). Mechanical → cheap; integration/judgment → standard; architecture/final review → most capable. **Turn count beats token price** — cheapest models take 2–3× turns, costing more overall.

**Batch small same-shape work**: several small identical edits across files → ONE dispatch with every file listed, review as one unit.

## Load These When Needed

Read only what the moment requires — do not load everything up front.

| File | Read when |
|---|---|
| `references/full-guide.md` | You need the complete original guide (all 568 lines, diagrams included) |
| `implementer-prompt.md` | Dispatching an implementer — the brief template |
| `task-reviewer-prompt.md` | Dispatching the per-task reviewer — the rubric |
| `re-review-prompt.md` | Dispatching a scoped re-review after fixes |
| `scripts/sdd-workspace` | Creating/locating this plan's workspace directory |
| `../requesting-code-review/code-reviewer.md` | Dispatching the final whole-branch reviewer |
| `../finishing-a-development-branch` | After final review is clean |

> **The full guide is 32KB and exceeds the 8192-char pruner threshold** — that is why it lives in `references/` and this index stays short. Read it deliberately when you need a section's exact wording, not by default.

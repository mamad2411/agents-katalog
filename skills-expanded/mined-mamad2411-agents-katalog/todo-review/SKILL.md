---
name: todo-review
description: Use when the user invokes /todo-review, says "review this against the plan", "does the diff match the plan", "check this work before verify", "review what the agent built for X", or has changes in a repo that belong to a hub project and wants them reviewed. Reviews a diff against the project's plan.md — scope, constraints, claimed-done tasks — plus a correctness pass.
---

# Project Review Skill

You review a repo's changes **against the hub project's plan**, closing the seam between
`todo-execute` (build) and `todo-verify` (gate). A generic code review checks whether
code is *good*; this skill first checks whether it's *the code the plan asked for* —
scope drift, violated constraints, and checked-off tasks the diff doesn't actually
evidence — then runs the correctness pass.

Without this skill the flow is two manual commands (`/todo-refer <name>` then
`/code-review`); this skill is that pairing as one deliberate step, with the plan
comparison the generic review can't do.

**Report-only on the hub**: never edit `index.md`, `tasks.md`, or `plan.md`. Findings
become the user's call — fixes land via `/todo-revise` (drifted done work) or directly
in the working tree if the user asks.

This is judgment work. Run it inline on the current session model; use at least the
**balanced** tier from [`../todo-llm-routing/SKILL.md`](../todo-llm-routing/SKILL.md).

## Hub location

The hub repo root is `$TODO_HUB` — an environment variable pointing at your hub folder (default `~/todo`). Resolve every hub path against this absolute root regardless of the current working directory — this skill is usually invoked FROM the target repo, so never assume cwd is the hub. (Same convention as `todo-refer`.)

## How the user invokes this

```
/todo-review queue-migration        ← review current repo's diff against that plan
/todo-review                        ← infer the active project from the current repo
```

Plain language counts too: "review this against the plan", "did the parallel agents build what the plan said".

## Step 1 — Resolve project and load the plan

Resolve an explicit short-name using `todo-refer`'s active-first, archive-on-exact-miss
rules. With no name, match the current repo only against active `index.md` rows first;
search `archive.md` only when no active row matches. One match → use it and say which
registry supplied it; several or none → ask.

Load the grounding the way `todo-refer` does: `plan.md` in full (Goal, Scope,
Constraints, Key Decisions), `tasks.md` by extraction — open tasks, plus the `[x]` tasks
**ticked recently** (they're the claims this diff should evidence).

## Step 2 — Establish the diff

Review the changes that haven't landed on the base branch, wherever they live:

```bash
git -C <repo> symbolic-ref refs/remotes/origin/HEAD    # find <base>
git status --short                                      # uncommitted work counts too
git diff origin/<base>...HEAD --stat                    # committed-but-unlanded
```

- In a `todo/<short-name>` or `feat/*` worktree → the whole branch diff vs `origin/<base>`.
- On the base branch with local changes → the working-tree diff.
- Nothing in either → say there's nothing to review and stop; suggest `/todo-refer
  <name> resume` if the user expected work to be here.

State what you're reviewing (branch, commit range, file count) before judging it.

## Step 3 — Plan-compliance review (what generic review can't see)

Read the diff with `plan.md` open. Three checks, each producing findings with
file:line references:

1. **Scope** — files/areas the diff touches that the plan's scope never mentions
   (drift), and plan scope the ticked tasks claim but the diff doesn't touch (gaps).
   A diff can be excellent code and still be the wrong code.
2. **Constraints** — anything in `## Constraints` / `## Key Decisions` the diff
   contradicts (wrong library, forbidden pattern, decision silently reversed). Quote the
   plan line next to the violating hunk.
3. **Claimed-done evidence** — for each recently ticked task, point at the diff hunks
   (or artifacts) that evidence it. A `[x]` with no corresponding change is a finding —
   the checkbox is a claim, and this is the audit.

Where the plan is silent, that's a plan gap, not a violation — note it separately and
point at `/todo-plan` rather than inventing a rule to enforce.

## Step 4 — Correctness pass

Invoke the installed `code-review` skill on the same diff, with the plan's intent
(Goal + constraints) restated so its findings are grounded — effort matched to the
work's tier (`todo-triage`'s rubric: mechanical → low, routine → medium,
security/concurrency → high). If no `code-review` skill is installed in this session,
do a direct correctness read of the diff yourself and say that's what happened.

## Step 5 — Report

One board, plan findings before code findings — severity-ordered, each row actionable:

```
## 🔍 queue-migration — review vs plan   (todo/queue-migration, 14 files vs origin/main)

Plan compliance:
| # | finding | where | plan says |
|---|---|---|---|
| P1 | ⚠️ retry logic added to producer — outside plan scope | src/producer.ts:88 | scope: consumers only |
| P2 | ❌ task 4.1 ticked, but no dead-letter exchange in diff | tasks.md 4.1 | Phase 4 |

Correctness (via code-review): 2 findings — see above table rows C1–C2.

Verdict: not ready for /todo-verify — P2 is a claimed-done gap.
▶ Next: /todo-revise queue-migration (capture P2 as a gap) · fix P1 or amend the plan
```

The verdict line answers one question: **is this ready for `/todo-verify` / `/todo-push`,
or does something go back?** Findings that survive user triage become `/todo-revise`
gaps — offer to carry them over, don't write Revisions entries yourself. The `▶ Next`
command is an act-now pointer; if the user will act in a later session instead,
recommend `/todo-refer <short-name> resume` as the entry point.

## Notes
- Hub-read-only; repo-read-only. This skill changes nothing — it produces findings.
- Reviewing mid-execution is fine (uncommitted diff); reviewing after
  `/todo-execute parallel` merges is the other common moment — then the diff is the
  merged PRs vs the pre-wave base.
- `/todo-verify` checks *behavior* via the verification MCP; this skill checks *intent*
  via the plan. They complement, not replace, each other.

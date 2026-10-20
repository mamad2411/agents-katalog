---
name: roadmap
description: Create or revise a delivery roadmap, producing a plan.v1 artifact plus a human-readable ROADMAP.md. Use when starting a project, planning a quarter, or when a re-planning trigger has fired and the existing roadmap must be revised rather than rewritten. Not for sprint planning or task breakdown.
argument-hint: "[--revise] [--horizon 2q] [--plan .foundry/blackboard/<wave>/roadmap-planner.json]"
user-invocable: true
agent: foundry-pmo:roadmap-planner
model: opus
effort: high
metadata:
  foundry.vertical: management
  foundry.io: "requirement.v1 + capacity -> plan.v1 + ROADMAP.md"
license: Apache-2.0
---

# Roadmap

Produce a roadmap that can be falsified: outcome milestones with checkable exit criteria, a
dependency-forced sequence, an explicit "not now" list, and named re-planning triggers.

Two modes:
- **Create** (default) — no usable prior roadmap exists.
- **Revise** (`--revise`) — a prior `plan.v1` exists and a trigger fired. Milestone ids are
  preserved; the diff is recorded. Never regenerate from scratch.

## Step 0 — Gather inputs, and record what is missing

Run these and keep the results. Do not proceed on assumption.

```bash
# prior roadmap
ls -1 .foundry/blackboard/*/roadmap-planner.json 2>/dev/null
ls -1 ROADMAP.md docs/ROADMAP.md 2>/dev/null

# requirements
ls -1 docs/requirements/*.md 2>/dev/null | head -50
ls -1 .foundry/blackboard/*/requirements-analyst.json 2>/dev/null

# repository reality
gh --version >/dev/null 2>&1 && gh auth status >/dev/null 2>&1 && echo GH_OK || echo GH_UNAVAILABLE
gh api repos/{owner}/{repo}/milestones --paginate --jq '.[] | {title,open_issues,closed_issues,due_on}' 2>/dev/null
gh issue list --state open --limit 200 --json number,title,labels,milestone 2>/dev/null | head -c 4000
git log --since='90 days ago' --pretty=format:'%ad' --date=short | sort | uniq -c | tail -20
```

Write an **input ledger** before planning anything:

| Input | Source read | Status |
|---|---|---|
| Requirements | `docs/requirements/` | 23 found |
| Capacity | — | **missing — assumed 3 FTE at 0.60 focus** |
| Risks | `risk.v1` ×0 | **missing — run `risk-review` first** |
| Repo state | `gh` | read, 2 milestones open |

Every `missing` row becomes an entry in `estimate.v1.assumptions[]`. If both requirements and
capacity are missing, stop and ask. A roadmap on two unknowns is theatre.

## Step 1 — Frame outcomes

If the input is still strategy rather than a set of needs, delegate first:

> If the `superpowers` plugin is installed, invoke `superpowers:brainstorming` to turn the
> strategic intent into candidate outcomes, then return here. If it is not installed, work the
> prompts in `references/outcome-framing.md` manually and note that ideation was unassisted.

Write each milestone as:

```
By <milestone>, <who> can <do what they could not before>,
measured by <metric> moving from <baseline> to <target>.
```

Reject any milestone that names a component instead of a capability. Missing baseline means the
milestone is not ready: add a measurement task to the preceding wave.

Target 3–7 milestones. Anything beyond the horizon goes to `outOfScope`, not into a wave.

## Step 2 — Tasks, dependencies, critical path

For every milestone, list the tasks that must land for the gate to pass. Then classify each
dependency edge with the table in `references/dependency-analysis.md`:

- Technical / Data / Contractual → keep in `dependsOn`
- Resource → **remove** from `dependsOn`, handle as capacity contention
- Preference → **delete**

Compute the critical path over the surviving edges. Report it as a range:

```
critical path: M1.T2 → M1.T5 → M2.T1 → M2.T4 → M3.T3
optimistic  sum: 118 h
pessimistic sum: 364 h
PERT expected  : 196 h
```

A point-value critical path is a defect. The ratio pessimistic ÷ optimistic is itself a signal:
above 3, insert a spike task before committing to any date downstream.

## Step 3 — Gates

Every wave needs machine-checkable exit criteria in `waves[].gate`:

```json
{
  "acceptance": ["REQ-0041", "REQ-0042"],
  "checks": [
    { "name": "e2e payments", "command": "npm run test:e2e -- --grep @payments", "pass": "exit 0" },
    { "name": "open sev:1", "command": "gh issue list --label 'sev:1' --milestone 'M2' --state open --json number --jq 'length'", "pass": "== 0" }
  ],
  "signoff": ["product-owner"]
}
```

Banned: "tested", "stable", "production-ready", "signed off" with no named signer. Minimum bar:
one executable check **or** one traced requirement id per gate. Zero of both → reject the wave.

## Step 4 — Capacity and sequencing

```
available_hours_per_period = headcount × period_hours × focus_factor
```

Use measured throughput when available. Otherwise **0.60** and record it as an assumption —
never silently 1.0. Then walk milestones in dependency order, filling periods to capacity, and
serialise any two same-period tasks sharing an `agent`/role.

Apply the heuristics in order: de-risk first → shorten the critical path → value density. Where
you deviate because a stakeholder demanded it, write it down as a `fact.v1` of type `decision`
so the trade is visible in six months.

## Step 5 — Estimates as ranges

One `estimate.v1` per milestone, never a bare number anywhere:

```json
{
  "schema": "estimate.v1",
  "producedBy": "roadmap-planner",
  "scope": "M2 — Merchants can take card payments",
  "items": [
    { "label": "3-D Secure integration", "role": "backend", "optimistic": 24, "likely": 40, "pessimistic": 96, "unit": "hours" }
  ],
  "expected": 46.7,
  "confidenceInterval": { "p50": 44, "p80": 68, "p95": 88 },
  "assumptions": [
    "Focus factor 0.60 — assumed, not measured",
    "Provider sandbox available from week 1",
    "Team of 3 unchanged through Q4; no holiday absence modelled"
  ],
  "excluded": ["Multi-currency", "Saved cards", "Chargeback handling"]
}
```

`plan.v1.waves[].tasks[].estimateHours` carries only the PERT expected value; the range lives
here. See `references/estimation.md` for PERT, the p80 rule and the ratio checks.

## Step 6 — The "not now" list

`outOfScope[]` needs ≥ 3 entries in this form:

```
<item> — not now because <reason>; revisit when <observable condition>.
```

Allowed reasons only: *no capacity in horizon*, *blocked by unresolved dependency*,
*insufficient evidence of value*, *beyond planning horizon*, *deliberately deferred trade*.
"Low priority" restates the conclusion and is rejected.

## Step 7 — Re-planning triggers

At least four, each with a numeric or event threshold and a response. Copy the trigger table
from `references/replanning-triggers.md` and tune the thresholds with the sponsor, then record
the agreed thresholds as a `fact.v1` of type `decision`.

`plan.v1.rollback` states what happens to in-flight work when a trigger fires: branches parked,
flags off, customer-visible state, and **who decides**.

## Step 8 — Emit

1. Validate: `mcp__plugin_foundry-core_foundry__contract_validate` on the `plan.v1` and each `estimate.v1`.
2. Write to the blackboard via `mcp__plugin_foundry-core_foundry__blackboard_write` (path
   `.foundry/blackboard/<wave>/roadmap-planner.json`).
3. Render `ROADMAP.md` from `templates/ROADMAP.md` — placeholders are `{{goal}}`,
   `{{milestones}}`, `{{critical_path}}`, `{{out_of_scope}}`, `{{triggers}}`, `{{assumptions}}`.
4. Materialise in GitHub **only** by handing the plan to `github-operator`. This skill does not
   run `gh` write commands.

## Revise mode (`--revise`)

1. Load the prior `plan.v1`. Do not delete milestone ids.
2. State the trigger that fired, with the measurement that fired it.
3. Produce a diff section in `ROADMAP.md`:

```markdown
## Revision 2026-08-27 — trigger: scope growth 27% (threshold 10%)
- M2 date range moved: 30 Nov → 11–22 Dec (p80 18 Dec)
- Moved to "not now": saved cards — no capacity in horizon; revisit when M3 gate passes
- Added: M2.T7 provider stub — de-risks the sandbox dependency
- Unchanged: M1 (closed), M3, M4
```

4. Write a `fact.v1` of type `decision` with `supersedes` pointing at the prior revision fact.
   Never edit the previous fact.

## Exit criteria

- [ ] Input ledger written; every missing input appears in `estimate.v1.assumptions[]`.
- [ ] 3–7 milestones, each in outcome form with a named baseline and target.
- [ ] Zero `dependsOn` edges of type resource or preference.
- [ ] Critical path reported as a range; ratio > 3 produced a spike task.
- [ ] Every wave gate has ≥ 1 executable check or ≥ 1 traced requirement id; no banned wording.
- [ ] Focus factor stated explicitly.
- [ ] ≥ 3 `outOfScope` entries with allowed reasons and revisit conditions.
- [ ] ≥ 4 re-planning triggers with thresholds and responses; thresholds recorded as a decision.
- [ ] `rollback` names the decision-maker.
- [ ] `plan.v1` and every `estimate.v1` validate.
- [ ] `ROADMAP.md` written; in revise mode it contains a diff section.
- [ ] No single date presented as a commitment anywhere in the output.

## What this skill deliberately does not cover

- Sprint planning, task breakdown below the milestone, or estimating individual issues —
  use `groom-backlog`.
- Writing or refining requirements — use `write-requirements`.
- Creating GitHub milestones, issues or projects — use `github-setup` and `github-operator`.
- Budget, cost and financial modelling — `foundry-economics`. Hours only here.
- Reporting progress against an existing roadmap — use `status-report`.
- Deciding priorities. It computes and proposes; the sponsor decides.

## References

| File | Load when |
|---|---|
| `references/outcome-framing.md` | milestones keep coming out feature-shaped |
| `references/dependency-analysis.md` | classifying edges, computing critical path, breaking false dependencies |
| `references/estimation.md` | PERT, three-point ranges, focus factor, p80, ratio checks |
| `references/replanning-triggers.md` | full trigger catalogue with default thresholds |
| `templates/ROADMAP.md` | rendering the human-readable output |

---
name: groom-backlog
description: Run a working grooming session over the real issue tracker — split oversized items with SPIDR, estimate as ranges, order by value density, close stale items, flag anything missing acceptance criteria, and report WIP breaches. Use before a sprint or milestone starts, or whenever the top of the backlog cannot be pulled. Not for roadmap planning or writing requirements from scratch.
argument-hint: "[--milestone \"M2\"] [--limit 50] [--dry-run] [--close-stale]"
user-invocable: true
agent: foundry-pmo:backlog-manager
model: sonnet
effort: medium
metadata:
  foundry.vertical: management
  foundry.io: "live tracker + requirement.v1 -> plan.v1 (ready queue) + gh mutations"
license: Apache-2.0
---

# Groom backlog

A working session, not a report. It ends with a ready queue that can actually be pulled, and a
list of mutations either applied or handed over as exact commands.

`--dry-run` is the default posture for anything destructive: propose, show the command, apply
only after the user approves. `--close-stale` is never implied.

## Step 1 — Read the real backlog

```bash
gh --version >/dev/null 2>&1 && gh auth status >/dev/null 2>&1 && echo GH_OK || echo GH_UNAVAILABLE

gh issue list --state open --limit 500 \
  --json number,title,body,labels,assignees,milestone,createdAt,updatedAt,comments \
  > .foundry/scratch/backlog.json

gh pr list --state open --json number,title,isDraft,createdAt,author,reviewDecision \
  > .foundry/scratch/prs-open.json

gh pr list --state merged --limit 200 --json number,createdAt,mergedAt \
  > .foundry/scratch/prs-merged.json

gh project item-list <number> --owner <owner> --format json --limit 500 \
  > .foundry/scratch/board.json    # requires the 'project' scope
```

**If `gh` is unavailable or unauthenticated:** say so in the first line of output, then look for
`docs/backlog/*.md` or ask the user to name the source. Do not proceed on an imagined backlog,
and never fabricate an issue number.

Report what you read: item count, milestones present, label namespaces present, and the date
window of the data. Every later number is anchored to this.

## Step 2 — Triage each item against the Definition of Ready

Seven checks, in order, stop at the first failure. Full rationale in `references/dor-dod.md`.

| # | Check | Failure label |
|---|---|---|
| 1 | ≥ 1 acceptance criterion in Given/When/Then | `needs:criteria` |
| 2 | Value stated: who benefits, what changes | `needs:criteria` |
| 3 | Expected effort ≤ ⅓ of the iteration | `needs:split` |
| 4 | Dependencies identified and unblocked | `blocked` |
| 5 | No open clarifying question | `needs:decision` |
| 6 | Testable — a named verification method | `needs:criteria` |
| 7 | Owned by a person or role | `needs:owner` |

Exactly **one** primary reason label per item. Several reason labels make the triage queues
useless, which is how triage queues die.

A fast first pass for check 1:

```bash
jq -r '.[] | select((.body // "") | test("(?i)given.*when.*then") | not)
        | "\(.number)\t\(.title)"' .foundry/scratch/backlog.json
```

This finds candidates; a human read confirms them. Criteria written in another valid form (a
checklist of verifiable outcomes) pass check 1 — the regex is a filter, not the rule.

**The hard rule:** an item without acceptance criteria is not ready. It does not enter the
sprint, the milestone or a WIP slot, no matter who asked. Label it, comment the specific missing
information, and move on. Do not write the criteria yourself for an absent stakeholder — that is
`write-requirements` with a human in the loop.

## Step 3 — Split what is too big

Apply SPIDR in order; the first pattern producing two independently valuable slices wins.
Details and worked examples in `references/spidr.md`.

| Pattern | Split by |
|---|---|
| **S**pike | learning vs. building — use when the estimate ratio p/o ≥ 3 |
| **P**ath | alternative flows — the item contains "or", "unless", "except" |
| **I**nterface | channel or surface — web, API, CLI, import |
| **D**ata | subset of data, types, locales, tenants — the item says "all" or "any" |
| **R**ules | one business rule at a time — the item embeds a multi-clause policy |

Rules: each slice gets its **own** acceptance criteria; a slice that is only "the backend half"
is a checklist item on the parent, not a separate issue; never split deeper than two levels —
three levels means it is a milestone, hand it to the `roadmap` skill.

```bash
# create a slice and link it
gh issue create --title "Checkout: decline expired cards" \
  --body-file .foundry/scratch/slice-1.md \
  --label "type:feat" --label "prio:must" --label "area:api" \
  --milestone "M2"
gh issue comment <parent> --body "Split into #<a>, #<b>, #<c> (SPIDR: Rules)"
gh issue close <parent> --reason "not planned" --comment "Superseded by #<a>, #<b>, #<c>"
```

## Step 4 — Estimate as ranges

Estimates come from the people doing the work. This session structures and records them.

For each ready item collect `optimistic / likely / pessimistic` and compute `E = (o+4m+p)/6`.
Record in the issue body, never as a bare number:

```
Estimate: 6–14 h (likely 8, expected 8.7) — assumes provider sandbox available
```

Ratio check: `p/o > 5` means it is not an estimate. Schedule the spike instead of the item.
`size:` labels are a communication shorthand mapped from `E`, not a substitute for the range:
xs ≤ 2 h, s ≤ 4 h, m ≤ 8 h, l ≤ 16 h, xl > 16 h → must be split.

Aggregate into one `estimate.v1` for the session, with assumptions and exclusions listed.

## Step 5 — Detect duplicates

Mechanical, in order — see `references/duplicate-detection.md` for the normalisation rules.

```bash
# title similarity candidates (normalised token overlap)
jq -r '.[] | "\(.number)\t\(.title | ascii_downcase | gsub("[^a-z0-9 ]";""))"' \
  .foundry/scratch/backlog.json | sort -k2

# same referenced artifact (file path, endpoint, error string, REQ id)
grep -oE 'REQ-[0-9]{4}' -r .foundry/scratch/backlog.json | sort | uniq -c | sort -rn | head

gh issue list --state all --search "<key terms> in:title" --json number,title,state
```

**Never auto-close on similarity.** Present pairs with their evidence; a human confirms. A wrongly
closed duplicate loses information permanently; a survivor costs one minute next session.

## Step 6 — Age out

Age from `updatedAt`, not `createdAt`. Exemptions: `sev:1`, `security`, and items with a
regulatory or contractual date. Nothing else is exempt.

```bash
jq -r --arg d60 "$(date -u -d '60 days ago' +%Y-%m-%d)" \
  '.[] | select(.updatedAt < $d60) | "\(.number)\t\(.updatedAt[0:10])\t\(.title)"' \
  .foundry/scratch/backlog.json
```

| Age since update | Action |
|---|---|
| 60 d | label `stale:60`, comment asking the reporter to confirm it still matters |
| 90 d | remove from Ready; must be re-groomed before it can be pulled |
| 180 d | propose closure as `not-planned`, with the reason and how to reopen |

Closure always carries a written reason. `--close-stale` executes the proposals; without it they
are printed as commands only.

## Step 7 — Order the ready queue

```
density = value_signal / expected_effort
```

`value_signal` from cost of delay when the project has one; otherwise the MoSCoW proxy
(must=8, should=4, could=2, wont=0) — and you must say you used a proxy. Tie-breakers in order:
unblocks the most other items → narrows the widest estimate range → oldest ready item first.

Present the ordered queue as a table with density, effort range, and blocking relations. The
product owner approves the order; this skill proposes it.

## Step 8 — WIP limits and flow metrics

Defaults (see `references/wip-and-flow.md` for the derivation and how to tune them):

| Column | Limit |
|---|---|
| In progress | `1.5 × developers`, min 1 |
| In review | `0.5 × developers`, min 1 |
| Ready | `2 × iteration throughput` |
| Blocked | 2, hard — the third triggers escalation to `risk-manager` |

Measure and report, each with its window:

```bash
# cycle time (created -> merged) for the last 100 merged PRs, in days
jq -r '.[] | ((.mergedAt|fromdate) - (.createdAt|fromdate)) / 86400 | floor' \
  .foundry/scratch/prs-merged.json | sort -n | awk '
  {a[NR]=$1} END {printf "n=%d p50=%d p85=%d max=%d\n", NR, a[int(NR*0.5)], a[int(NR*0.85)], a[NR]}'

# age of the oldest open PR, in days
jq -r 'min_by(.createdAt) | "\(.number) \(.createdAt[0:10])"' .foundry/scratch/prs-open.json
```

On a breach: **stop starting, start finishing.** Name the items over the line and the oldest
item in the column. Never raise a limit silently — a raised limit is a decision, recorded as a
`fact.v1` of type `decision`.

## Step 9 — Emit

1. Build `plan.v1`: `waves[0].tasks[]` = the ordered ready queue, `waves[0].gate` = readiness
   counts, `outOfScope[]` = closed/deduplicated/deferred items with reasons.
2. Validate with `mcp__plugin_foundry-core_foundry__contract_validate`; write with `mcp__plugin_foundry-core_foundry__blackboard_write`
   to `.foundry/blackboard/<wave>/backlog-manager.json`.
3. Print every proposed mutation as an exact `gh` command. Apply only after approval.
4. Hand label/milestone/project application to `github-operator` when a bulk change is involved.

Session summary to print:

```
Read 187 open issues (27 Aug, gh authenticated)
Ready:            12   (was 4)
Not ready:        63   needs:criteria 41 | needs:split 12 | blocked 7 | needs:owner 3
Split:             5 parents → 17 slices (SPIDR: Rules ×3, Data ×2)
Duplicate pairs:   6 proposed, 0 closed (awaiting confirmation)
Stale:            29 labelled stale:60 | 11 proposed for closure
WIP:              in-progress 7/6 BREACH | review 2/3 | blocked 4/2 BREACH → escalate
Cycle time:       p50 4 d, p85 19 d (n=100 merged PRs)
```

## Exit criteria

- [ ] Backlog read from a live source, or the output states it was unreadable and why.
- [ ] Every item in the ready queue passes all seven DoR checks; no silent exceptions.
- [ ] Every not-ready item carries exactly one primary reason label.
- [ ] Every oversized item split with a named SPIDR pattern or labelled `needs:split`.
- [ ] Every slice has its own acceptance criteria; no split deeper than two levels.
- [ ] Every estimate recorded as a range; ratio > 5 produced a spike instead of a scheduled item.
- [ ] Duplicate candidates presented with evidence; none auto-closed.
- [ ] Every item stale beyond 60 days labelled, re-groomed or proposed for closure with a reason.
- [ ] Cycle time p50/p85, oldest in-progress age and throughput reported with windows.
- [ ] WIP breaches listed item by item; no limit raised without a recorded decision.
- [ ] `plan.v1` and `estimate.v1` validate.
- [ ] Every mutation shown as an exact `gh` command before execution.

## What this skill deliberately does not cover

- Roadmap sequencing and milestone definition — use `roadmap`.
- Eliciting requirements or writing acceptance criteria on a stakeholder's behalf — use
  `write-requirements`.
- Deciding priority. It computes density and proposes an order; the product owner decides.
- Repository governance (labels taxonomy, protections, projects) — use `github-setup`.
- Evaluating individuals. Cycle time is a system metric; using it per person corrupts the data.
- Retrospectives and team process facilitation.
- Non-GitHub trackers. The concepts port; these commands do not.

## References

| File | Load when |
|---|---|
| `references/dor-dod.md` | tightening or negotiating the readiness and done definitions |
| `references/spidr.md` | a split is not producing independently valuable slices |
| `references/wip-and-flow.md` | setting limits, reading cycle time, diagnosing a stalled board |
| `references/duplicate-detection.md` | normalisation rules and the confirmation protocol |

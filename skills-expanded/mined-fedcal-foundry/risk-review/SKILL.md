---
name: risk-review
description: Run a periodic risk review — re-score existing risk.v1 artifacts, identify new risks with category prompts, check detection signals against real repository data, and escalate everything that crossed its threshold. Use at a milestone gate, on a fixed cadence, or after any event that changed the plan. Not for security threat modelling or legal rulings.
argument-hint: "[--full] [--since 2026-07-27] [--escalate-only]"
user-invocable: true
agent: foundry-pmo:risk-manager
model: opus
effort: high
metadata:
  foundry.vertical: management
  foundry.io: "plan.v1 + prior risk.v1 + repo signals -> updated risk.v1 + escalations"
license: Apache-2.0
---

# Risk review

A risk register earns its cost only if it is reviewed and acted on. This session re-scores what
exists, finds what is new, checks whether detection signals fired, and escalates what crossed a
threshold — in that order, so escalation is based on current numbers rather than on last
quarter's.

`--full` runs all eight identification prompt sets (do this quarterly and at every milestone
gate). Default runs the update path plus the prompt sets for categories touched by changes since
the last review. `--escalate-only` re-scores and escalates without adding new risks.

## Step 1 — Load the register and the plan

```bash
ls -1 .foundry/blackboard/*/risk-manager.json 2>/dev/null
ls -1 .foundry/blackboard/*/roadmap-planner.json 2>/dev/null
ls -1 docs/risks/*.md 2>/dev/null
```

Also retrieve persisted risks: `mcp__plugin_foundry-core_foundry__memory_search` with type `risk`.

No prior register means this is a first assessment: say so, because trend analysis and threshold
comparison are impossible without a prior baseline, and any statement about direction would be
invented.

Report the starting position: count by status, total open exposure as a range, count of risks
past their `reviewBy` date. That last number is a health metric for the process itself.

## Step 2 — Read the signals

Every risk's `detection` field names an observable. Check them for real; a detection signal that
is never evaluated is decoration.

```bash
gh --version >/dev/null 2>&1 && gh auth status >/dev/null 2>&1 && echo GH_OK || echo GH_UNAVAILABLE

gh issue list --label 'sev:1' --state open --json number,title,createdAt
gh issue list --label blocked --state open --json number,title,updatedAt
gh pr list --state open --json number,createdAt,reviewDecision
gh run list --workflow ci.yml --limit 50 --json conclusion \
  | jq -r 'group_by(.conclusion)[] | "\(.[0].conclusion): \(length)"'
gh api repos/{owner}/{repo}/milestones --jq '.[] | {title,open_issues,closed_issues,due_on}'

# dependency and supply-chain signals, where available
gh api repos/{owner}/{repo}/dependabot/alerts --jq \
  '[.[] | select(.state=="open")] | group_by(.security_advisory.severity)[]
   | "\(.[0].security_advisory.severity): \(length)"' 2>/dev/null || echo "dependabot alerts unavailable"

git log --since="${SINCE:-90 days ago}" --pretty=format:'%an' | sort | uniq -c | sort -rn   # bus factor signal
```

Record which signals could not be read. Do not treat an unreadable signal as a signal that did
not fire — those are different, and conflating them is how a materialising risk goes unreported.

## Step 3 — Re-score every open risk

For each, answer four questions and record the movement:

| Question | If yes |
|---|---|
| Has the **because** clause changed? | re-write the causal chain; if the condition is no longer true, close the risk |
| Has probability moved? | move it to a different calibration band; record the old and new band |
| Has impact moved? | re-derive the three-point range; recompute `impactEur` as the PERT value |
| Did the detection signal fire? | the risk is materialising — activate contingency and escalate now, not at the next review |

Probability bands (never free-hand numbers; record the band name):

| Band | Value | Meaning |
|---|---|---|
| Rare | 0.05 | no precedent; would surprise a domain expert |
| Unlikely | 0.15 | happened elsewhere; conditions here make it improbable |
| Possible | 0.35 | plausible; comparable projects see it occasionally |
| Likely | 0.60 | more often than not, absent mitigation |
| Almost certain | 0.85 | early signals already visible; only timing is uncertain |

Recompute `exposureEur = probability × impactEur` and report the **movement**:

```
RISK-014  Provider sandbox unavailable for 3-D Secure
  probability  Possible 0.35 → Likely 0.60      (signal fired: 9 days blocked on #305)
  impact       80 000 → 96 000 EUR              (range 40k–160k; +2 weeks of delay at 8k/wk)
  exposure     28 000 → 57 600 EUR              ▲ +106%
  status       open → mitigating
  reviewBy     2026-09-24 → 2026-09-03          (weekly cadence: above escalation threshold)
  ESCALATE     exposure ≥ 50 000 threshold      → sponsor, within 2 business days
```

A register with no movement between reviews is a register nobody read. If nothing moved, say so
explicitly and explain why the situation is genuinely static.

## Step 4 — Identify new risks

Work the category prompts. `--full` runs all eight; otherwise run those touched by changes since
the last review. Full prompt sets: `references/risk-taxonomy.md`.

Categories: **technical, schedule, cost, security, compliance, operational, vendor, people**.

Every new risk is written as a causal chain — never a bare noun phrase:

```
Because <condition true today>,
<event> may occur <when / under what circumstance>,
which would cause <consequence> costing <impact range>.
```

Chain tests: the *because* is verifiable today; the *event* has not happened yet (if it has, it
is an issue — hand it to `status-report` as a blocker and close the risk as materialised); the
*consequence* is measurable in money, time or a compliance outcome.

Sources that reliably surface risks people do not volunteer:
- The critical path — the widest estimate ratio on it is almost always a risk.
- Recently closed issues labelled `sev:1` — what nearly went wrong is a good predictor.
- `git log --pretty=format:'%an'` concentration — bus factor.
- Open dependabot alerts and end-of-life versions in lockfiles.
- Anything in `plan.v1.outOfScope` deferred for "insufficient evidence" — deferred bets carry risk.

## Step 5 — Quantify impact honestly

```
impact = direct_cost + (delay_days × day_rate) + revenue_at_risk + remediation_cost + regulatory_exposure
```

Always a **range**: optimistic, likely, pessimistic, with assumptions. `impactEur` is the PERT
expected value of that range, and the artifact says so.

When you lack an input:

| Missing | Do this — never this |
|---|---|
| Day rate | report exposure in **days only**; say the euro figure is unavailable. Never invent a rate. |
| Revenue at risk | mark `impactEur` partial and name the missing component. Never invent a revenue figure. |
| Statutory penalty | refer to `foundry-legal`; never quote a fine without citing the article from a competent source. |

Rank by exposure, with one override: a low-probability **existential** risk (company-ending,
licence-revoking, safety) ranks first regardless of expected value. Mark it `existential` in the
title so it cannot be averaged away by a spreadsheet.

## Step 6 — Check mitigations are real

For every risk with `status: mitigating`:

- [ ] The owner is still the right named person, and still here.
- [ ] The mitigation action exists as a scheduled task (an issue, a `plan.v1` task) — not as an
      intention.
- [ ] Residual probability and impact are stated. **A mitigation that moves neither number is
      theatre** — remove it and re-plan.
- [ ] The mitigation costs less than the exposure it removes. State both. Spending 40 000 EUR to
      remove 10 000 EUR of exposure is a bad trade even when it feels safer.
- [ ] The detection signal still works — the query still returns data, the alert still exists.

For every `status: accepted`: confirm the acceptance is still conscious and still at the right
level of authority. Acceptance decays into forgetting; re-confirm at every milestone gate.

## Step 7 — Escalate what crossed a threshold

Thresholds are set once with the sponsor and applied mechanically. Defaults if none are recorded
(propose, confirm, then record as a `fact.v1` of type `decision`):

| Condition | Escalate to | Within |
|---|---|---|
| `exposureEur` ≥ 10% of remaining budget, or ≥ 20 days on the critical path | sponsor | 2 business days |
| Any risk marked `existential` | sponsor + executive owner | immediately |
| `probability` ≥ 0.60 with no mitigation owner | sponsor | immediately |
| `security` risk with CVSS ≥ 7.0 and no patched path | security owner + sponsor | 1 business day |
| `compliance` risk touching a statutory deadline | legal owner + sponsor | 1 business day |
| Total open exposure grew > 25% since the last review | sponsor, with the trend | at this review |
| A risk passed `reviewBy` unreviewed twice | sponsor — the process has failed | immediately |

Escalation format — anything less is not escalation:

```
To: <named sponsor>          Date: 2026-08-27          Response needed by: 2026-08-29
RISK-014 — Provider sandbox unavailable for 3-D Secure step-up
Exposure: 57 600 EUR (P 0.60 × impact 96 000; range 40k–160k) — up 106% since 30 Jul
Crossed: exposure >= 50 000 EUR threshold
Options:
  A. Escalate to the vendor account manager — cost ~0, may resolve in 3–10 days, uncertain
  B. Build against the published spec, test in production with 1% traffic — 5 d, adds RISK-019
  C. Descope step-up auth to M3 — M2 date holds, 2 of 7 markets deferred
Recommendation: A now, C if unresolved by 5 Sep.
Requested decision: approve C as the fallback, with 5 Sep as the trigger date.
```

## Step 8 — Set the next review date

From exposure, not from convenience:

| Exposure band | Interval |
|---|---|
| Above the escalation threshold | weekly |
| ≥ 25% of the threshold | fortnightly |
| Below that | monthly, or at each milestone gate |
| `accepted` | every milestone gate, minimum quarterly |

Close a risk only when the causal chain's *because* clause is no longer true, or the window in
which it could occur has passed. **Never close a risk because it has been quiet.**

## Step 9 — Emit

1. Validate each `risk.v1` with `mcp__plugin_foundry-core_foundry__contract_validate`.
2. Write via `mcp__plugin_foundry-core_foundry__blackboard_write` to `.foundry/blackboard/<wave>/risk-manager.json`.
3. Write a `fact.v1` of type `risk` via `mcp__plugin_foundry-core_foundry__memory_write` for every risk above the
   escalation threshold, so it survives compaction.
4. Render the register from `templates/risk-register.md`.
5. Propose (do not apply) any `plan.v1` change that pulls a mitigation into a wave — hand it to
   the `roadmap` skill in revise mode.

Session summary:

```
Register: 23 open | 6 mitigating | 4 accepted | 9 closed
Open exposure: 214 000 EUR (range 96k–498k)  — up 31% since 30 Jul  → SPONSOR REVIEW TRIGGERED
Re-scored: 23 | moved: 8 | new: 4 | closed: 2 | materialised: 1 (RISK-011 → issue #431)
Detection signals: 19 checked | 3 fired | 4 unreadable (listed)
Escalations: 2 (RISK-014, RISK-019)
Past reviewBy: 5 → all re-dated; 1 twice-missed → process escalation
```

## Exit criteria

- [ ] Every open risk re-scored, with movement recorded (or "no movement" stated with a reason).
- [ ] Every probability comes from a named calibration band.
- [ ] Every impact is a PERT expected value of a stated range, or names the component that could
      not be computed.
- [ ] Every detection signal checked, or listed as unreadable with the failing command.
- [ ] Every risk has a named human owner; unowned risks escalated, not filed.
- [ ] Every mitigation states residual probability/impact and its own cost; theatre removed.
- [ ] Every risk has a `reviewBy` from the exposure-based cadence.
- [ ] Everything crossing a threshold escalated in the full format, to a named person, with a date.
- [ ] Total open exposure reported as a range, with the change since the last review.
- [ ] Categories with zero risks stated as deliberately empty, not silently skipped (`--full`).
- [ ] Every `risk.v1` validates.

## What this skill deliberately does not cover

- **Security threat modelling.** STRIDE, attack trees and control selection belong to the
  security agents. This records the risk; it does not model the attack.
- **Legal interpretation.** It records a compliance risk and its deadline; it never rules on law
  or invents a penalty figure.
- **Insurance and contract drafting.** "Transfer" is named as a strategy; the instrument is
  procured by people.
- **Detailed financial modelling.** Order-of-magnitude exposure only; `foundry-economics` owns
  budgets and unit economics.
- **Issue management.** A materialised risk becomes an issue and leaves the register.
- **Setting risk appetite.** Thresholds belong to the sponsor. This proposes defaults and applies
  what is agreed.
- **Changing the plan.** It proposes mitigations as tasks; `roadmap` decides where they go.

## References

| File | Load when |
|---|---|
| `references/risk-taxonomy.md` | running the identification prompts, especially with `--full` |
| `references/quantification.md` | deriving impact ranges, converting delay to money, calibration |
| `templates/risk-register.md` | rendering the register |

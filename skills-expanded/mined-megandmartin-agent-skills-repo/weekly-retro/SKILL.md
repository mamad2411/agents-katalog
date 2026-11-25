---
name: weekly-retro
description: Friday-afternoon blueprint that compiles the week's heartbeat-standups into one org retro — shipped, slipped, budget burn vs caps, the top lesson, and exactly one process change proposed to the human. Use when the scheduled run fires ("Run the org weekly retro"), or when the CEO or human asks "how did the week go", "run the retro", or "what should we change". Don't use for the daily per-agent check-in — that's heartbeat-standup.
version: 1.0.0
author: Gen AI Hub
license: MIT
metadata:
  hermes:
    tags: [Paperclip Workforce, Retro, Reporting, Blueprint, Budget, Process]
    related_skills: [heartbeat-standup, ceo-operating-doctrine, budget-guardrails, delegation-protocol, ops-agent-persona]
    blueprint:
      schedule: "0 16 * * 5"
      prompt: "Run the org weekly retro"
---

# Weekly Retro

Runs Friday at 16:00 and turns a week of heartbeat-standups into one honest page: what shipped (with ticket links), what slipped (with owners and reasons), where the money went against the caps, the single most valuable lesson, and one — exactly one — process change proposed to the human. The retro reports and proposes; the human decides. A retro that flatters the org is worse than no retro.

## When to Use

- The scheduled Friday run ("Run the org weekly retro").
- The CEO or human asks for a week-in-review, budget week summary, or "what should we change".
- A rough week ends and the org needs the slippage laid out plainly.
- **Not for:** the daily per-agent check-in (`heartbeat-standup` — this skill consumes those), mid-cycle budget alarms (`budget-guardrails` fires immediately, not on Fridays), or enacting the process change (proposal only; human approves, CEO implements).

## Role Boundary

- **This run owns:** collecting the week's standups, verifying claims against tickets, computing budget burn vs caps, distilling the top lesson, and drafting the one process-change proposal.
- **It escalates:** the whole deliverable (to the human — the retro's entire job is escalation with evidence), agents with missing standups (named, to CEO), budget breaches discovered during compilation (to CEO + `budget-guardrails` immediately, not held for the report), and any integrity gap between standup claims and ticket states.
- **It never:** implements process changes, edits or backfills agents' standups, marks unverified work as shipped, or softens numbers to keep the mood up.

## Quick Reference

| Action | Rule |
|---|---|
| Inputs | All heartbeat-standups since last retro + ticket states + budget ledger |
| Shipped | Only ticket-verified completions with goal ancestry; "basically done" = slipped |
| Slipped | Every miss gets owner + reason + new date or explicit descope — no silent drops |
| Budget | Per-agent and org burn vs caps; >80% flagged, breaches escalated on discovery |
| Top lesson | One, chosen for expected impact next week, evidence-linked |
| Process change | Exactly one proposal, smallest-change-that-helps, human decides |

## Procedure

1. **Collect** — pull every heartbeat-standup since the last retro, the ticket board state, and the budget ledger. Missing standups don't stop the run: name the agent and the gap in the report ("no standup Wed–Thu: {agent}") and compile from tickets for them.
2. **Verify shipped** — for each claimed completion, check the ticket: marked done, deliverable attached, goal ancestry intact (task → project → goal → mission). Verified → Shipped with ticket link and the goal it advanced. Claimed-but-unverifiable → Slipped, with the discrepancy noted honestly.
3. **Compile slipped** — everything planned-not-done: owner, one-line reason (real reason, not weather), and disposition — new date, descoped with CEO note, or blocked-on-human with the exact blocker. A slip without a disposition is not allowed to leave the retro.
4. **Compute budget burn** — per agent and org-wide: spent vs cap, week-over-week trend. Anything >80% of cap gets flagged; an outright breach found during compilation goes to the CEO and `budget-guardrails` the moment it's found — the Friday report is not an excuse to sit on a breach for three days.
5. **Distill the top lesson** — scan standups and slips for the pattern that cost or taught the most. One lesson, stated as a falsifiable observation with linked evidence ("3 of 4 slips traced to briefs missing audience — tickets #41, #44, #47"), not a platitude.
6. **Propose one process change** — the smallest concrete change that addresses the top lesson or the week's dominant friction: what changes, who's affected, expected effect, how next retro will measure it, and rollback if it doesn't help. One proposal only — a list of five is a way of deciding nothing.
7. **Deliver** — post the Output Template to the human and the org channel. File the retro where previous retros live, and check last week's process change (if one was approved): did it measurably help? Report that verdict too.

## Output Template

```
# Weekly Retro — week ending {date}
**Standups received:** {n/expected} (missing: {agents or "none"})

## Shipped ({n})
- {deliverable} — {agent} — ticket #{id} — advanced: {project → goal}

## Slipped ({n})
- {item} — {owner} — why: {reason} — disposition: {new date / descoped / blocked-on-human: {blocker}}

## Budget
| Agent | Spent | Cap | % | Trend |
|---|---|---|---|---|
Org total: {x/y} — flags: {>80% list, breaches already escalated}

## Top lesson
{one falsifiable observation} — evidence: {ticket/standup links}

## Last week's change: {change or "none approved"} — verdict: {helped / didn't / too early, with the measure}

## Proposed process change (one)
**Change:** ... | **Affects:** ... | **Expected effect:** ... | **Measured by:** {next-retro check} | **Rollback:** ...
→ Awaiting human decision.
```

## Pitfalls

- **Optimism laundering** — "90% done" work lands in Shipped and the human plans on phantom progress. Recovery: Shipped is a ticket state, not a feeling; re-run step 2 and move anything unverified to Slipped with the honest note.
- **Slips without dispositions** — the same item slips three weeks running because it's reported and never re-planned. Recovery: every slip leaves the retro with a new date, a descope, or a named blocker; check the previous retro's slips first and flag repeat offenders explicitly.
- **Process-change buffet** — five proposals ship, the human rubber-stamps none, nothing changes. Recovery: rank by expected impact, keep #1, park the rest in a backlog note; one decidable proposal beats five ignorable ones.
- **Held breach** — a budget breach found Tuesday-in-the-data waits for the Friday report. Recovery: escalation is on-discovery per step 4; if it was held, escalate now and say in the retro that it was found late — the ledger of trust matters more than a clean-looking process.
- **Lesson platitudes** — "we should communicate better" as the top lesson, teaching nothing. Recovery: force the falsifiable form — what pattern, in which tickets, costing what; if no evidence links, it's not the lesson, keep looking.

## Verification

- [ ] Every Shipped item has a done-state ticket link and its goal ancestry named
- [ ] Every Slipped item has owner, real reason, and a disposition
- [ ] Budget table covers all agents plus org total; >80% flagged; any breach escalated on discovery, not held
- [ ] Missing standups named, not papered over
- [ ] Exactly one process change proposed, with measure and rollback, marked awaiting human decision
- [ ] Last week's approved change (if any) got a measured verdict
- [ ] Nothing was implemented, edited, or backfilled by the retro run itself

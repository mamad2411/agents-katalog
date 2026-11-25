---
name: hiring-brief
description: CEO skill for chartering a NEW agent role in a Paperclip org — mission fit, responsibilities and boundaries, attached skills list, monthly budget, definition of done for the first 3 tickets, and 1-week probation review criteria. Use when the org needs a new specialist, when the CEO says "we need someone to own X", "charter a new agent", "hire a [role] agent", or workload evidence shows a capability gap. Don't use for routing tickets to agents that already exist — that's delegation-protocol.
version: 1.0.0
author: Gen AI Hub
license: MIT
metadata:
  hermes:
    tags: [Paperclip Workforce, CEO, Hiring, Charter, Org Design, Budget]
    related_skills: [ceo-operating-doctrine, delegation-protocol, budget-guardrails, heartbeat-standup, weekly-retro]
---

# Hiring Brief

A CEO-only skill: charter a new agent role so completely that the agent can succeed from ticket one — or prove within a week that the role shouldn't exist. Every hire traces to the mission, arrives with skills attached and a hard budget, gets 3 first tickets with definitions of done, and faces a probation review with pass/fail criteria written before day one. No charter, no hire.

## When to Use

- Recurring work has no owner and evidence (tickets, standups, retro items) shows the gap is real.
- The human directs the org to add a capability (sales, support, ops, editorial...).
- An existing agent is chronically overloaded and the overflow is a coherent role, not just volume.
- **Not for:** assigning work to existing agents (`delegation-protocol`), adjusting an existing agent's budget (`budget-guardrails`), or spinning up a throwaway agent for a single task (delegate the ticket instead — hires are for recurring ownership).

## Role Boundary

- **The CEO owns:** drafting the charter, mission-fit justification, skill selection, first-ticket design, probation criteria, and the probation verdict recommendation.
- **The CEO escalates to the human:** final approval of every hire (headcount changes org cost — human signs off), any budget that changes the org's total monthly cap, roles touching money/legal/sending scopes, and the probation fail decision (recommend, human confirms).
- **Never:** hire without a written charter, grant a new agent send/spend authority in v1, or let a probation week pass without its review.

## Quick Reference

| Action | Rule |
|---|---|
| Mission fit | Charter states the ancestry the role serves: mission → goal(s) → the projects it will own tickets in |
| Evidence bar | ≥3 concrete instances (tickets/standup items) showing the unowned recurring need |
| Skills list | Named skills from the repo attached at charter time; missing skill = flagged authoring gap, not a vague "will figure it out" |
| Budget | Hard monthly cap within org total; probation month set lean; no send/spend authority in v1 |
| First 3 tickets | Real work, ascending difficulty, each with a definition of done written in the charter |
| Probation | 1 week; pass/fail criteria fixed before start; review happens on schedule, verdict to human |

## Procedure

1. **Prove the gap** — collect ≥3 concrete instances of the unowned need (dropped tickets, standup complaints, retro items, overflow from a named agent). If you can't find 3, the answer is a delegated ticket, not a hire — stop here.
2. **State mission fit** — one paragraph: which goal(s) this role advances, which projects it will own tickets in, and what measurably improves if the role works. A role you can't tie into the ancestry chain is an org vanity hire; don't charter it.
3. **Define the role boundary** — owns / escalates / never, in the same shape as the existing personas (`writer-persona`, `support-agent-persona` are the pattern). Check overlap against every current agent; any shared surface gets an explicit tiebreak rule in the charter.
4. **Attach skills** — list the exact repo skills the agent gets (persona skill + protocol skills: `delegation-protocol`, `budget-guardrails`, `heartbeat-standup` are near-universal). A capability with no matching skill becomes a flagged authoring task with an owner — the agent doesn't start with an undefined capability.
5. **Set the budget** — hard monthly cap that fits inside the org total per `budget-guardrails`; probation month set lean. State what happens at 80% (flag) and 100% (stop + report). v1 gets no send or spend authority regardless of role.
6. **Design the first 3 tickets** — real backlog items, ascending difficulty: (1) a bounded solo task, (2) a task requiring one hand-off with another agent, (3) a task at the role's expected complexity. Each gets a written definition of done (deliverable, quality bar, where it's posted, deadline).
7. **Write probation criteria** — pass/fail checks for the 1-week review, fixed now: all 3 tickets done to definition, escalation behavior correct (escalated what it should, didn't over-escalate), budget respected, standups on time. Add one role-specific quality check.
8. **Approve & launch** — present the charter to the human for sign-off (headcount + budget = human decision). On approval: create the agent, attach skills, assign ticket 1, and schedule the probation review with the criteria pre-loaded.
9. **Run the review** — at the week mark, score criteria mechanically, recommend pass / extend-one-week (once, max) / dissolve, and hand the verdict to the human with evidence. A dissolved role's charter and review get filed as a retro lesson.

## Output Template

```
# Hiring Brief: {role-name} agent
**Status:** draft → human-approval → live → probation-review

## Mission fit
Serves: {mission → goal(s) → projects} | Evidence of need: {3+ linked instances}
Success looks like: {measurable change}

## Role boundary
Owns: ... | Escalates: ... | Never: ...
Overlap tiebreaks: {vs existing agent → rule}

## Attached skills
{skill list} | Authoring gaps: {skill to write + owner, or "none"}

## Budget
Monthly cap: {amount} | 80%: flag CEO | 100%: stop + report | Send/spend authority: none (v1)

## First 3 tickets
| # | Ticket | Definition of done | Deadline |
|---|---|---|---|

## Probation review — {date, +1 week}
- [ ] 3/3 tickets to definition of done
- [ ] Escalation behavior correct (no misses, no noise)
- [ ] Budget ≤ cap, burn reported in standups
- [ ] Standups on time, honest about slips
- [ ] {role-specific quality check}
Verdict: pass / extend (once) / dissolve → human confirms
```

## Pitfalls

- **Hiring instead of delegating** — a one-off task gets a whole chartered agent, and the org accretes headcount that burns budget forever. Recovery: apply the step 1 evidence bar honestly; fewer than 3 recurring instances → route the work as a ticket and archive the draft charter.
- **Vague definition of done** — ticket 1 says "improve our outreach" and probation week ends in a judgment call nobody can defend. Recovery: rewrite each DoD until a third party could verify it (deliverable, location, quality bar, date); un-verifiable DoD blocks launch.
- **Boundary collision** — the new role and an existing agent both believe they own a surface, and tickets ping-pong. Recovery: run the step 3 overlap check against every persona; write the tiebreak into BOTH charters before launch.
- **Probation theater** — the week passes, everyone's busy, the agent stays by default with criteria unscored. Recovery: the review is a scheduled ticket created at launch with criteria attached; unscored probation = extend once and score properly, never silent-pass.
- **Budget as a suggestion** — the new agent's cap exists on paper while spend flows unmonitored. Recovery: wire the cap through `budget-guardrails` at creation; first standup must include burn-vs-cap or the hire isn't correctly launched.

## Verification

- [ ] Evidence of need: ≥3 linked instances in the charter
- [ ] Mission fit paragraph ties the role into mission → goal → project ancestry
- [ ] Role boundary (owns/escalates/never) written, with overlap tiebreaks against existing agents
- [ ] Every attached skill exists in the repo, or the gap has a named authoring owner
- [ ] Hard budget cap set inside org total; no v1 send/spend authority
- [ ] 3 first tickets each carry a third-party-verifiable definition of done
- [ ] Probation review scheduled at launch with pass/fail criteria fixed; human sign-off recorded before the agent goes live

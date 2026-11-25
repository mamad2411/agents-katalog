---
name: community-ops-weekly-review
description: Use when producing community weekly reviews, weekly reports, metric summaries, decision notes, retrospective plans, or next-week operating priorities. Connects activity data, onboarding, creator signals, paid/member care, support risks, content assets, and owner decisions into a practical review.
---

# Community Ops Weekly Review

Use this skill to turn a week of community work into decisions and next actions.

## Project Inputs

Get the review period and timezone, durable source records, action states, metric sources and denominators, user or creator signals, known risks, data gaps, and owner decisions from the user or approved project sources.

The skill supplies the review lens and output structure. It does not include the community's weekly actions, counts, revenue, retention, member records, or conclusions. If records are incomplete, review the available evidence and name the missing sources; never fill gaps with repository examples or assumed trends.

## Review Lens

Review the week by operating loop, not by raw message volume:

```text
entry -> first action -> participation -> submission/proof -> feedback/showcase -> retention/upgrade -> review
```

## Inputs To Check

- activity launches, reminders, submissions, votes, winners, showcases;
- newcomer path and first-action signals;
- creator/high-quality content signals;
- paid member or high-value user follow-ups;
- support, payment, access, safety, or moderation risks;
- product/website/account conversion signals if available;
- unverified metrics and data gaps.
- daily operating records, execution receipts, verification results, and material state changes.

Prefer durable operating records over report summaries when the two conflict. Daily reports and dashboards are derived views; they should not become the only evidence for a weekly conclusion.

## Output Pattern

Localize the visible labels to the user's requested language.

```md
**Weekly Judgment**
[What improved, broke, or needs a decision.]

**Review Scope**
- Period/timezone: ...
- Data sources and denominator: ...

**Key Actions**
| Area | Prepared | Executed/verified | Evidence | Decision needed |
|---|---|---|---|---|

**User-Path Review**
entry -> first action -> participation -> proof -> feedback/showcase -> next action

**Opportunities**
- [Concrete improvement with surface and owner.]

**Risks / Gaps**
- [Missing data, approval, support issue, rule gap, or unclear benefit.]

**Next-Week Priorities**
1. [P0 + owner + due date]
2. [P1 + owner + due date]
3. [P2 + owner + due date]
```

## Approval Boundary

Weekly review outputs are recommendations and drafts. Require explicit confirmation before sending reminders, contacting or mentioning users, publishing showcases or winner lists, settling rewards, changing roles/permissions, or making official metric and product claims.

## Quality Bar

Do not turn the review into a generic strategy essay. Each conclusion needs evidence: count, link, artifact, visible action, user segment, or an explicit data gap.

Keep `prepared`, `pending approval`, `executed`, `verified`, `blocked`, `ambiguous`, and `cancelled` distinct. An automation run or approved draft does not prove that a public action happened. Feed verified decisions and material state changes back into the durable operating record for the next cycle.

Avoid unsupported revenue or retention claims. Say "possible signal" when the evidence is partial.

---
name: community-ops-daily-report
description: Use when turning daily community operations into a concise daily report, daily log, work recap, owner update, standup note, or personal community-ops record. Separates completed public actions, drafts, analysis, follow-ups, risks, data gaps, and tomorrow actions without overstating unconfirmed work.
---

# Community Ops Daily Report

Use this skill to turn one day's community work into a report. The report should sound like an operator's work record, not an agent retrospective.

## Project Inputs

Get the reporting date and timezone, source records, action owners, execution states, evidence links or IDs, available metrics, data gaps, and decisions needed from the user or an approved operating record.

The skill supplies the report structure and status checks. It does not contain the user's daily work, community metrics, member follow-ups, or completion evidence. If no factual source is provided, return a blank structure or request the minimum records needed; do not produce a factual-looking report from examples.

## First Move

Separate work into states:

- prepared or pending approval;
- approved but not executed;
- executed but not yet verified;
- verified and recorded action;
- draft prepared for review;
- data checked or analyzed;
- user/member/creator follow-up;
- support or risk handled;
- blocked or owner-confirmation needed;
- tomorrow action.

Do not write drafts, dry-runs, approvals, automation runs, or unverified execution attempts as completed public work.

Use the durable operating record and execution receipt as the factual inputs when available. Treat the daily report as a derived summary; it does not replace or silently correct the source record.

## Output Pattern

Localize the visible labels to the user's requested language.

```md
**Daily Focus**
[1-2 sentences on the actual operating focus.]

**Completed**
- [Verified action + actor + surface + evidence/status.]

**In Progress**
- [Prepared, pending approval, executed-unverified, or follow-up item + next step + owner.]

**Data / Observations**
- [Concrete signal, count, link, or declared data gap.]

**Risks / Confirmation Needed**
- [Reward, role, send, payment, permission, support, safety, or missing evidence.]

**Next-Day Actions**
- [Concrete next action.]
```

## Style

Write in the operator's community-ops voice: practical, direct, action-based. Avoid technical workflow narration unless it is part of the work. Keep actor attribution clear: who published, who drafted, who analyzed, who needs to confirm.

## Checks

Before finalizing:

- Does each bullet describe an actual action or observation?
- Are drafts separated from published work?
- Is every completed external action verified, with actor and target clear?
- Are prepared, approved, executed, verified, blocked, ambiguous, and cancelled states kept distinct?
- Are missing IDs, links, counts, or exact users marked as data gaps?
- Are public posts, DMs, mentions, rewards, discounts, winner lists, roles, permissions, channel changes, integrations, and official claims owner-confirmed?
- Are private messages, payment details, access data, and unnecessary user identifiers kept out of broadly shared reports?

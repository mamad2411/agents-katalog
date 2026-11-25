---
name: review-backlog-killer
description: Detect pull requests aging past warn / critical thresholds, score severity, and nudge reviewers via Slack DM, channel, email, or directly as a PR comment — with one-time auto-escalation when a PR hits critical so velocity stops leaking through review queues.
tags: [code-review, pull-request, slack, devex, ai-agent]
publisher: agena
---

# Review Backlog Killer

Pull requests get lost in review queues; team velocity drops silently.
Sprint planning shows it as "I dunno, sometimes the reviewers are slow".
This pattern surfaces stuck PRs deterministically and sends the reviewer
a nudge through whichever channel they actually read.

## How to apply this pattern

1. **Define open**: PR is open when `merged_at IS NULL AND closed_at IS
   NULL` AND its provider status is in `{open, opened, pending,
   review_required, in_review, active}`. PRs with provider status in
   `{abandoned, declined, closed, rejected}` drop off the backlog.

2. **Configure thresholds** per workspace (chip-pick is best UX —
   6h / 12h / 1d / 2d / 3d / 1w / custom). Defaults: 24h warn, 48h
   critical, 6h between auto-nudges to the same reviewer.

3. **Poller every 30 minutes** updates `age_hours` and `severity`
   (`info` < warn ≤ `warning` < critical ≤ `critical`) on every open PR.
   Merged or closed PRs auto-resolve out of the backlog.

4. **Pick a notify channel** per workspace:
   - `slack_dm` — direct, most attention
   - `slack_channel` — visible to team
   - `email` — for async-first teams
   - **`pr_comment`** — most attention-grabbing because it lands where
     the reviewer already lives. The comment text is locale-aware so
     non-English teams don't get an English nudge.
   - `manual` — dashboard-only, no auto-notify

5. **Auto-escalate** once when a PR crosses the critical threshold:
   set `escalated_at`, mark severity, surface above the fold to tech
   leads. Fire it once per PR, not on every poll cycle.

6. **Manual nudge button** on every row — fires the configured channel
   immediately, overrides the interval. Useful for a tech lead doing a
   one-shot push before standup.

## Example PR comment template

```
⏱️ AGENA Review Backlog

This PR has been waiting for review for **47 hours** (severity: critical).
Nudge #2.

Configure thresholds at /dashboard/review-backlog.
```

When the Reviews module is also on, the message includes
`AGENA review score: 84` so reviewers see the time investment before
clicking.

## Notes

- **Idempotency on PR comment**: before posting, check whether a
  prior AGENA comment already exists on that PR — re-post would be
  spammy. If the comment was deleted by a human, treat the row as
  un-nudged so the next cycle is allowed to comment again.
- **Provider-aware status refresh**: PRs marked active in your local DB
  may have been abandoned upstream; refresh status before deciding to
  nudge so you don't ping reviewers on dead PRs.
- **Exempt repos** are essential — legacy / maintenance repos shouldn't
  trigger nudges. Comma-separated repo-mapping ids in a workspace
  setting is the simplest UX.
- The poller scales linearly with open PR count; 1000 open PRs ≈
  1 second of polling per cycle.

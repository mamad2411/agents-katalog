---
name: campaigns-content-performance
description: Analyze collected Campaigns post metrics for one social account. Use for weekly performance reports, retrospective rankings, or evidence-based content experiments. Do not use to publish content, schedule reports, or claim causation.
metadata:
  author: taigfs
  tags: [campaigns, analytics, content, social-media, weekly-report]
---

# Campaign content performance

Use the Campaigns MCP at `https://campaigns.mcp.devfellowship.com/mcp`.
Do not replace it with direct database or Zernio access.

## Select the analysis basis

- For a normal weekly report, call `rank_account_posts` with `basis=period_gain`.
- Set `start_date` and `end_date` to the requested reporting window.
- For the first retrospective report, use `basis=lifetime` across the collected history.
- Label every lifetime value as a lifetime total.
- Never describe a lifetime total as a weekly gain.

Treat coverage as incomplete when a target lacks an observation inside the requested period.
Also treat a missing usable baseline or selected metric as incomplete coverage.
Do not calculate a period gain from a lifetime value.
Explain which evidence is missing and which posts are affected.

A negative period gain is valid vendor data when an absolute counter decreases.
Keep its sign, report it as an anomaly, and inspect its metric history.
Do not clamp the value to zero or convert it to an absolute value.

## Resolve the account

1. Call the existing `list_zernio_accounts` directory tool with an empty input.
2. Match the user's human label against each returned `label`.
3. Call `list_campaign_accounts` to find accounts with collected analytics.
4. Intersect the rows where `id` equals `account_id` and `platform` equals `platform`.
5. Continue only when the intersection contains one exact account.

If the intersection contains zero or multiple accounts, stop.
Show the candidate IDs and platforms.
Ask the user for one precise account.
Never select an account by platform or label similarity.

## Collect the evidence

1. Call `rank_account_posts` with the resolved `account_id` and `platform`.
2. Set `metric` to `views`, `likes`, or `comments`.
3. Also pass `basis` and `limit`.
4. For a period report, pass `start_date` and `end_date`.
5. Call `get_post_metric_history` for each winner and each important anomaly.
6. The history tool requires `post_id`, `account_id`, and `platform`.
7. Copy all three values from the same ranking row into every history call.
8. Add `start_date` and `end_date` when the report has a date boundary.

Keep platform results separate.
Metric meanings and collection coverage can differ by platform.
If a cross-platform comparison is necessary, present it side by side with this caveat.
Do not create a combined score unless the user defines its normalization.

## Write the report

Include these sections:

1. **Evidence** — the account, platform, metric, basis, period, baseline, coverage, and ranked values.
2. **Winners** — the strongest posts for each separate account and platform.
3. **Repeatable patterns** — attributes that recur across more than one strong post.
4. **Anomalies** — spikes, reversals, missing baselines, or unusual history changes.
5. **Next actions** — small experiments with one change, one metric, and one evaluation window.

Name the Campaigns `post_id` for each finding.
Show the observed counts before the interpretation.
Use association language for patterns.
Counts alone do not prove that a format, topic, or timing choice caused the result.

When coverage is incomplete, put the caveat beside the affected finding.
Do not hide it in a final note.
If no valid ranking remains, report insufficient evidence instead of naming a winner.

## Weekly automation boundary

This skill prepares one report when it runs.
It does not create a recurring schedule.
Keep the account, period, metric, platform, basis, and limit explicit for a later scheduler.

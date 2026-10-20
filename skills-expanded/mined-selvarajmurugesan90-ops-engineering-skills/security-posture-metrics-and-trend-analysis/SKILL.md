---
name: security-posture-metrics-and-trend-analysis
description: >
  Guides tracking security finding and posture trends over time — mean
  time-to-remediate (MTTR) by severity, backlog age distribution,
  false-positive rate, exception-list growth, and gate pass/override
  rate — to answer "is our security posture actually improving" with
  data instead of a point-in-time finding count. Use when the user asks
  to "build a security metrics dashboard", "track mean-time-to-remediate
  by severity", "show finding backlog trends over time", "report our
  security posture to leadership/an auditor", or "measure whether our
  DevSecOps program is working". Distinct from the day-to-day triage
  workflow in security-finding-backlog-triage, which this skill
  measures the output of.
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: devsecops
  maturity: stable
---

# Security Posture Metrics and Trend Analysis

## Purpose

"How many open findings do we have right now" is a snapshot, and a
misleading one on its own — a security program with 3,000 open findings
that has cut its median time-to-fix from 60 days to 12 days over the
last two quarters is improving; a program with 300 open findings that
has quietly grown from 50 over the same period is not, even though the
raw count looks better in absolute terms. This skill covers turning the
raw output of
[security-finding-backlog-triage](../security-finding-backlog-triage/SKILL.md),
[secure-cicd-gates](../secure-cicd-gates/SKILL.md), and
[security-gate-exception-management](../security-gate-exception-management/SKILL.md)
into trend data that actually answers whether a DevSecOps program is
working: mean/median time-to-remediate by severity, backlog age
distribution (not just size), false-positive rate per tool/rule,
exception-list growth and renewal frequency, and gate override/bypass
frequency. Done well, this becomes the evidence base for both internal
prioritization decisions and external reporting (leadership updates,
audit/compliance evidence); done poorly (vanity metrics like raw finding
count, or metrics collected but never reviewed), it becomes a dashboard
nobody trusts or acts on.

## When to use

- Leadership or an auditor asks for evidence that security findings are
  being addressed effectively, not just counted.
- The user wants to build or redesign a security metrics dashboard and
  needs to know which metrics actually signal program health versus
  which are vanity numbers.
- The team wants to measure whether a recent process change (a new
  triage cadence, a new severity-to-action table, a new scanner) is
  actually improving outcomes.
- The user wants to track mean-time-to-remediate (MTTR) by severity as an
  accountability metric against SLA targets.
- A security-gate exception list is suspected of growing unchecked and
  the user wants a trend view to confirm or refute that.
- The user wants to identify which tools/rules have a high enough
  false-positive rate to warrant tuning, backed by data rather than
  anecdote.

## Prerequisites & environment

- Historical finding data with, at minimum, creation date, resolution
  date (or still-open status), severity, and source tool — exported from
  SAST/SCA/DAST tools' native history, a SARIF archive, or (preferably,
  at any real scale) a centralized AppSec/vulnerability-management
  platform such as DefectDojo, GitHub code scanning's API, or a
  dedicated GRC tool. Point-in-time-only tool UIs that don't retain
  history make trend analysis impossible without a separate store —
  export/archive scan results on every run if the native tool doesn't
  keep history long enough.
- The severity-to-action/SLA table from
  [secure-cicd-gates](../secure-cicd-gates/SKILL.md) as the benchmark
  MTTR is measured against.
- The exception registry from
  [security-gate-exception-management](../security-gate-exception-management/SKILL.md)
  as the data source for exception-list trend metrics.
- A place to render trend data over time — a BI tool (Grafana, Looker,
  Metabase) pointed at a data warehouse/table of historical scan
  exports, or, for a lighter-weight start, a scheduled script generating
  a periodic report from raw exports.
- Organizational agreement on what "good" looks like per metric (a
  target MTTR by severity, an acceptable false-positive-rate ceiling) —
  a trend without a target tells you direction but not whether current
  performance is actually acceptable.

## Step-by-step guidance

1. **Capture a durable historical record on every scan run**, not just
   the latest snapshot — the single most common blocker to trend
   analysis is that only the current finding state was ever kept:
   ```bash
   # Archive every scan's raw output with a timestamp, regardless of
   # whether the tool's own UI retains history
   trivy fs --format json -o "scans/$(date +%Y%m%d)-trivy.json" .
   ```
   Land these into a queryable store (even an append-only table of
   `finding_id, tool, severity, status, first_seen, resolved_at` is
   sufficient to start) rather than only ever looking at the tool's own
   live dashboard.

2. **Track mean and median time-to-remediate (MTTR) by severity**,
   against the SLA target, not just as an abstract number:
   ```sql
   -- illustrative query against an archived findings table
   SELECT
     severity,
     AVG(resolved_at - first_seen) AS mean_ttr,
     PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY resolved_at - first_seen) AS median_ttr
   FROM findings
   WHERE resolved_at IS NOT NULL
     AND first_seen >= NOW() - INTERVAL '90 days'
   GROUP BY severity;
   ```
   Report median alongside mean — a handful of very old, very slow
   remediations can skew a mean upward (or, if closed as false
   positives right before a report, downward) in a way median is more
   robust against.

3. **Track backlog age distribution, not just backlog size**:
   ```sql
   SELECT
     severity,
     CASE
       WHEN NOW() - first_seen < INTERVAL '30 days' THEN '0-30d'
       WHEN NOW() - first_seen < INTERVAL '90 days' THEN '30-90d'
       WHEN NOW() - first_seen < INTERVAL '180 days' THEN '90-180d'
       ELSE '180d+'
     END AS age_bucket,
     COUNT(*) AS finding_count
   FROM findings
   WHERE status = 'open'
   GROUP BY severity, age_bucket
   ORDER BY severity, age_bucket;
   ```
   A backlog of 500 findings where 480 are under 30 days old (working
   as expected through a normal SLA) is a fundamentally different
   situation from 500 findings where 200 are over 180 days old — same
   headline count, very different risk picture.

4. **Track false-positive rate per tool/rule** as its own trend, feeding
   back into triage weighting
   ([security-finding-backlog-triage](../security-finding-backlog-triage/SKILL.md))
   and tuning decisions:
   ```sql
   SELECT
     tool, rule_id,
     COUNT(*) FILTER (WHERE disposition = 'false_positive') * 1.0 / COUNT(*) AS fp_rate,
     COUNT(*) AS total_findings
   FROM findings
   GROUP BY tool, rule_id
   HAVING COUNT(*) >= 20   -- ignore low-volume rules; rate is noisy on small samples
   ORDER BY fp_rate DESC;
   ```
   A rising false-positive rate for a specific rule over successive
   quarters is a concrete, actionable signal to retune or disable that
   rule — a static point-in-time rate doesn't show whether it's getting
   better or worse.

5. **Track exception-list size, age, and renewal frequency** as a trend,
   sourced from the exception registry in
   [security-gate-exception-management](../security-gate-exception-management/SKILL.md):
   ```sql
   SELECT
     DATE_TRUNC('month', granted) AS month,
     COUNT(*) AS exceptions_granted,
     COUNT(*) FILTER (WHERE renewal_of IS NOT NULL) AS renewals,
     AVG(EXTRACT(day FROM expires - granted)) AS avg_duration_days
   FROM exceptions
   GROUP BY month
   ORDER BY month;
   ```
   A steadily growing count of active exceptions, or a rising share of
   multi-renewal entries, is itself a posture regression worth
   surfacing — even if every individual exception was properly
   approved.

6. **Track gate override/bypass frequency** — how often a required
   check was overridden by an admin, or a Constraint's
   `enforcementAction` was patched back to non-blocking under pressure —
   as a trend indicating whether gates are actually respected:
   ```sql
   SELECT DATE_TRUNC('month', occurred_at) AS month, gate_name, COUNT(*) AS override_count
   FROM gate_overrides
   GROUP BY month, gate_name
   ORDER BY month, override_count DESC;
   ```
   A gate with a persistently high or rising override rate is
   functionally advisory, not blocking — surface this explicitly rather
   than letting the raw "gate exists and is marked required" status
   imply it's actually working, per the guidance in
   [secure-cicd-gates](../secure-cicd-gates/SKILL.md).

7. **Present trend, not just current value, in every report** — a line
   chart over the last 2-4 quarters for each metric above, not a single
   current-state table. A report showing only "MTTR for critical: 6
   days" tells a reader nothing about whether that's an improvement, a
   regression, or steady state without the trailing trend alongside it.

8. **Segment by team/service where volume justifies it**, not only an
   org-wide aggregate — an org-wide MTTR that looks acceptable can mask
   one team or one legacy service dragging the average while everyone
   else is well within SLA, and the aggregate view hides exactly where
   intervention is needed.

## Best practices

- Archive every scan run's raw output on a durable, queryable store from
  day one, even before there's a dashboard to put it in — trend
  analysis is impossible to backfill once only the current snapshot was
  ever kept.
- Report median alongside mean for time-based metrics (MTTR, exception
  duration) — outliers distort a mean in ways that mislead about typical
  performance.
- Track backlog *age distribution* as the primary size-related metric,
  not just a single backlog count — the same total can represent very
  different risk pictures depending on how old the oldest items are.
- Treat a rising exception count or renewal-heavy exception list as a
  posture regression in its own right, worth reporting explicitly, even
  when every individual grant followed proper process.
- Segment metrics by team/service, not only org-wide, when volume
  allows — an aggregate that looks fine can hide a genuinely under-
  performing area.
- Set explicit targets (an SLA per severity, an acceptable
  false-positive-rate ceiling, a maximum acceptable override rate) so a
  trend has something to be measured against, not just a direction.
- Review the metrics themselves periodically for whether they're still
  the right ones — a metric nobody has looked at meaningfully in two
  quarters is either wrong or the review cadence has lapsed; both are
  worth fixing.

## Common pitfalls

- **Symptom:** A quarterly security report shows only the current open
  finding count, and leadership can't tell whether the program is
  improving, stagnant, or regressing.
  **Fix:** Report MTTR by severity, backlog age distribution, and
  exception-list trend alongside (or instead of) the raw count, with at
  least 2-3 prior periods shown for comparison, not a single point-in-
  time number.

- **Symptom:** MTTR looks artificially good because a handful of very
  old findings were bulk-closed as "false positive" or "accepted risk"
  right before the reporting period, without individual review.
  **Fix:** Cross-check MTTR trend against the false-positive-rate and
  exception-count trends in the same period — a sudden MTTR
  improvement paired with a spike in either is a signal to audit the
  underlying dispositions rather than take the improved MTTR at face
  value.

- **Symptom:** The team wants to backfill six months of trend data and
  discovers the scanning tool's dashboard only retains the current
  state; historical scan results were never archived.
  **Fix:** This confirms the need to start archiving raw scan output
  going forward (step 1) — there is no way to reconstruct genuinely
  lost history; treat "start the archive now" as the actionable fix
  rather than attempting an unreliable reconstruction from partial
  logs.

- **Symptom:** A specific SAST rule has a high false-positive rate every
  quarter, but nobody has retuned or disabled it because the rate is
  only ever looked at as a point-in-time snapshot, not tracked as a
  persistent trend.
  **Fix:** Surface per-rule false-positive rate as a standing item in
  the recurring metrics review (not just computed once when someone
  asks), and set a threshold above which a rule is automatically
  flagged for tuning review.

- **Symptom:** A dashboard exists and is technically up to date, but no
  one has reviewed it in two quarters, and several metrics have quietly
  regressed (rising exception count, rising override rate) without
  triggering any action.
  **Fix:** Metrics with no review cadence are equivalent to no metrics —
  put the dashboard review on the same recurring agenda as the
  finding-triage meeting in
  [security-finding-backlog-triage](../security-finding-backlog-triage/SKILL.md),
  with an explicit owner responsible for flagging regressions.

## Worked example

A platform security team builds a quarterly posture report from
archived scan data and the exception registry.

Archived findings table (illustrative excerpt):
```
finding_id | tool    | severity | first_seen  | resolved_at | disposition
F-0231     | trivy   | critical | 2026-04-02  | 2026-04-04  | fixed
F-0894     | semgrep | high     | 2026-02-11  | 2026-05-01  | fixed
F-1042     | trivy   | high     | 2025-11-20  | NULL        | (open)
F-1103     | zap     | medium   | 2026-01-04  | 2026-01-10  | false_positive
```

MTTR by severity, Q2 2026 (illustrative):
```
| Severity | Median TTR | Mean TTR | SLA target | Status       |
|----------|-----------|----------|------------|---------------|
| Critical | 2 days    | 3 days   | 2 days     | At target     |
| High     | 9 days    | 14 days  | 14 days    | At target     |
| Medium   | 41 days   | 58 days  | 90 days    | Within SLA    |
```

Backlog age distribution, current snapshot:
```
| Severity | 0-30d | 30-90d | 90-180d | 180d+ |
|----------|-------|--------|---------|-------|
| Critical | 2     | 0      | 0       | 0     |
| High     | 18    | 11     | 4       | 1     |
| Medium   | 140   | 210    | 95      | 60    |
```
The report flags the 1 high-severity finding over 180 days old by name
for individual follow-up, rather than letting it blend into the
aggregate high-severity count.

Exception trend (from the registry in
[security-gate-exception-management](../security-gate-exception-management/SKILL.md)):
```
| Quarter | Active exceptions | New this quarter | Renewed >1x |
|---------|--------------------|--------------------|--------------|
| Q4 2025 | 22                 | 9                   | 1            |
| Q1 2026 | 31                 | 12                  | 3            |
| Q2 2026 | 44                 | 15                  | 6            |
```
The rising trend and increasing renewal count is called out explicitly
in the report as a regression worth investigating, even though every
individual exception was properly approved — leading to a follow-up
review of which exceptions are being repeatedly renewed and why, per
the guidance in
[security-gate-exception-management](../security-gate-exception-management/SKILL.md).

## Cross-references

- [security-finding-backlog-triage](../security-finding-backlog-triage/SKILL.md) —
  the triage process that produces the disposition/resolution data this
  skill's metrics are computed from.
- [secure-cicd-gates](../secure-cicd-gates/SKILL.md) — the
  severity-to-action SLA table that MTTR targets are measured against,
  and the gate design whose override rate this skill tracks.
- [security-gate-exception-management](../security-gate-exception-management/SKILL.md) —
  the exception registry this skill's exception-trend metrics are
  sourced from.
- [critical-vulnerability-emergency-response](../critical-vulnerability-emergency-response/SKILL.md) —
  detection-to-mitigation timing from individual emergency responses
  feeds into this skill's trend tracking across successive events.

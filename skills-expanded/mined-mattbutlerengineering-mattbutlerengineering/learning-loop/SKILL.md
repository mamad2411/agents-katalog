---
name: learning-loop
description: Sensor-driven continuous improvement loop. Collects metrics from all sensors, detects regressions, creates issues, verifies past fixes, and self-tunes thresholds. Invoke with /learning-loop.
user-invocable: true
---

# Learning Loop

Closed-loop improvement system: collect sensor data → detect regressions → create issues → verify fixes → learn from results.

## Workflow

### Step 1: Collect Sensor Data

Run the unified sensor report to gather metrics from all available sensors:

```bash
node scripts/sensor-report.mjs
```

Read the output. The script queries every sensor registered in `scripts/sensors-registry.mjs` (the list-of-record — check there for the current count and coverage) and persists the report to `metrics/sensor-report.json`. It also detects regressions by comparing against the previous report.

If the script exits with code 1, regressions were detected. Note them for Step 3.

Among those sensors is `metricsFreshness` (#5529), which grades the collectors themselves: it reports `stale` when the newest entry in a watched metric is older than that metric's threshold in `FRESHNESS_POLICY` (`scripts/metrics-freshness.mjs`), and `empty` when the metric has no entries at all. Both are regressions like any other, so a collector that silently stops producing data arrives in Step 3 as a `ci-fix` issue instead of waiting for the next manual audit. Staleness is absolute, not a delta — this sensor fires on the first report, with no previous report to compare against.

### Step 1b: Sentry Triage

If the Sentry MCP is available, run production error triage:

Invoke `/sentry-triage` to query Sentry for new/regressed production errors and create GitHub issues for any that pass the severity/frequency/deduplication filters.

This step is optional — if Sentry is not authenticated or unavailable, skip with a note in the summary.

### Step 2: Verify Past Fixes

Run fix verification on recently-closed issues:

```bash
node scripts/verify-fixes.mjs
```

This finds issues closed in the last 48 hours with sensor labels (`ci-fix`, `audit`, `acmm`, `sentry`, `bug`), queries the originating sensor, and:

- Comments on the issue with verification evidence
- Reopens issues where the fix didn't improve the metric

Note any reopened issues for the summary.

### Step 2b: Collect AI Issue Feedback

Run the feedback collector to update per-category acceptance rates:

```bash
node scripts/collect-ai-issue-feedback.mjs
```

This queries closed AI-created issues, classifies each as accepted/rejected/wontfix, and writes per-category rates + budgets to `metrics/ai-issue-feedback.json`. The budgets are used in Step 3 to cap issue creation for categories with high rejection rates (>40% rejected = budget halved).

### Step 3: Triage Regressions

Read the sensor report from `metrics/sensor-report.json` and the issue feedback budgets from `metrics/ai-issue-feedback.json`. For each regression in the `regressions` array:

1. **Check category budget** — read `budgets.<category>` from the feedback file. If the budget for that regression's label category is 0, skip. Default budget is 3 if no feedback data exists.

2. **Check for duplicates** — search open issues for the same sensor + metric combination:

   ```bash
   gh issue list --state open --search "<sensor> <metric>" --json number,title --limit 5
   ```

3. **Skip if duplicate exists** — don't create noise.

4. **Create issue** if novel — use this format:

   ```bash
   gh issue create \
     --title "fix(<sensor>): <metric> regressed (<delta>)" \
     --label "ready,<sensor-label>,bug" \
     --body "## Regression Detected\n\n**Sensor:** <sensor>\n**Metric:** <metric>\n**Current:** <value>\n**Previous:** <value>\n**Delta:** <delta>\n**Severity:** <high|medium>\n\n## Acceptance Criteria\n\n- [ ] <metric> returns to previous level or better\n- [ ] Verified by next learning loop run\n\n_Detected by [learning-loop](../.claude/skills/learning-loop/SKILL.md) sensor report_"
   ```

5. **Max issues per run** — use the per-category budget from `metrics/ai-issue-feedback.json` (default 3). Prioritize high severity over medium. Never exceed the budget for any single category.

### Step 4: Analyze Session Logs (Weekly)

Check if today is the configured skill-extraction day (default: Friday). If so:

1. Read session logs from `.claude/session-logs/*.json` (last 7 days)
2. Group sessions by branch prefix, files touched, and git diff patterns
3. Identify repeated workflows (3+ sessions with similar patterns):
   - Same file set modified across sessions
   - Same branch prefix pattern (e.g., `fix/security-*`)
   - High commit count with specific file patterns
4. Check existing skills in `.claude/skills/*/SKILL.md` for coverage
5. If a novel pattern is found, create a `skill-proposal` issue:
   ```bash
   gh issue create \
     --title "[skill-proposal] <Descriptive Name>" \
     --label "skill-proposal,ready" \
     --body "<draft skill content based on observed pattern>"
   ```
6. **Max 2 proposals per run**

### Step 5: Threshold Self-Tuning

Read the verification log at `metrics/verifications.jsonl` (last 30 days):

1. Compute **false positive rate**: issues closed as `wontfix` or `invalid` / total issues created by learning loop
2. Compute **fix effectiveness rate**: verified fixes / total verifications
3. If false positive rate > 30%, note in the summary that thresholds should be loosened
4. If fix effectiveness rate < 50%, note that fix strategies may need review

### Step 6: Log and Summarize

Append a dated entry to `.claude/improvement-loop/log.md` (then run `node scripts/cap-improvement-log.mjs` to keep only the newest 60 entries; older ones live in git history):

```markdown
## YYYY-MM-DD

**Sensors:** N/M available
**Regressions:** N detected, M issues created
**Verifications:** N checked, M verified, K failed (reopened)
**Skill proposals:** N (if Friday)
**Threshold notes:** <any self-tuning observations>
```

Print a summary to stdout.

Then persist this run's state — cloud routines run in ephemeral checkouts, so an uncommitted append is lost with the checkout:

```bash
node scripts/persist-metrics.mjs --routine learning-loop
```

It stages every **durable** path with a diff, commits them on a branch, and opens a PR titled `chore(metrics): learning-loop <YYYY-MM-DD>` labeled `has-pr` (metrics-only diffs auto-merge via the low-risk fast path). It exits 0 without a commit when nothing changed.

Do NOT enumerate paths by hand. Durability is declared once, as `durable: true` in `METRICS` (plus `DURABLE_OUTSIDE` / `EXTERNAL`) in `scripts/metrics-store.mjs`, and `durableManifest()` derives both the `.gitignore` negations and the list this script stages (#3645). An enumerated list drifts; a derived one cannot.

## Sensor Label Map

| Sensor            | Issue Label | What It Checks               |
| ----------------- | ----------- | ---------------------------- |
| CI Health         | `ci-fix`    | Pass rate on main branch     |
| ACMM              | `acmm`      | Maturity criteria met        |
| Lighthouse        | `audit`     | Performance/a11y scores      |
| Sentry            | `sentry`    | Error rates (needs MCP auth) |
| Metrics Freshness | `ci-fix`    | review-burden stale or empty |
| General           | `bug`       | CI pass after fix            |

## Scheduling

This skill is designed to run daily. Add a RemoteTrigger:

| Trigger             | Schedule         | Notes                   |
| ------------------- | ---------------- | ----------------------- |
| `mbe-learning-loop` | Daily 11:00am PT | After ACMM audit (10am) |

Or invoke manually: `/learning-loop`

## Guardrails

- Max issues per category governed by `metrics/ai-issue-feedback.json` budgets (default 3, halved when rejection rate >40%)
- Max 2 skill proposals per run
- Deduplication: always check open issues before creating
- Reopened issues get `ready` label for implement-queue pickup
- Session log analysis only on Fridays (configurable)
- Verification runs on 48h-old closures (configurable via `--hours`)
- AI issue feedback collection runs every invocation (Step 2b) to keep budgets current

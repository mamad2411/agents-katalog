---
name: optimize-implement-queue
description: "Daily implement-queue optimization: measures efficiency via the queueEfficiency sensor, logs a trend point, files de-duplicated ready issues on regression; never runs eval synchronously. Invoke with /optimize-implement-queue."
user-invocable: true
---

# Optimize Implement Queue

Daily skill that measures implement-queue efficiency, logs trends, and files `ready` issues when a real regression is detected. Phase-2 auto-tuning (model-routing tier adjustment) is documented as a future seam but NOT yet built.

## Flags

| Flag        | Effect                                                   |
| ----------- | -------------------------------------------------------- |
| `--dry-run` | Print what would happen; write nothing to disk or GitHub |

## Step 0: Reconcile Telemetry Outcomes

Fill the outcome fields (`merged`, `ci_first_pass`, `rework_cycles`, `merged_at`) that workers cannot know at write time — the sensor's precise-cost path only activates when rows are reconciled:

```bash
node scripts/reconcile-queue-telemetry.mjs
```

Idempotent and capped at 50 GitHub lookups; safe to run every day.

The daily `.github/workflows/metrics-collectors.yml` job now runs this reconciler right after it appends rows, with a working `GITHUB_TOKEN`, so the workflow is the primary reconciler. This routine's run is best-effort: its token is often rejected by api.github.com (`credential_rejected`, #6466), so a failure here is not an error.

## Step 1: Collect the Queue-Efficiency Sensor

Run the sensor-report to collect the `queueEfficiency` sub-report:

```bash
node scripts/sensor-report.mjs --json | jq '.sensors.queueEfficiency'
```

Or capture the whole report for later regression detection:

```bash
node scripts/sensor-report.mjs --json > /tmp/sensor-report.json
```

Read `regressions[]` from the output. Any entries with `sensor: "queueEfficiency"` are internal regressions detected by the rolling-7-day-median baseline baked into the collector (`collect-queue-efficiency.mjs`).

The `distribution` field provides difficulty-normalized context (size tiers): a session dominated by `size:xl` PRs will legitimately score lower — the `isRealRegression` check in `scripts/optimize-implement-queue.mjs` accounts for this.

## Step 2: Append Trend Point to process-metrics.jsonl

Use the helper to build and append a JSONL entry:

```javascript
import { buildQueueEfficiencyProcessEntry } from "./scripts/optimize-implement-queue.mjs";
import { appendFileSync, mkdirSync } from "node:fs";
import { dirname } from "node:path";

const entry = buildQueueEfficiencyProcessEntry(new Date().toISOString().slice(0, 10), sensorResult);
// In dry-run mode, log but do not write:
if (!DRY_RUN) {
  mkdirSync(dirname(METRICS_PATH), { recursive: true });
  appendFileSync(METRICS_PATH, JSON.stringify(entry) + "\n");
}
```

`METRICS_PATH` = `metrics/process-metrics.jsonl`

## Step 3: Append Dated Log Entry

**Always run this step, even when there is no regression.**

```javascript
import { buildOptimizeLogEntry, appendLogEntry } from "./scripts/optimize-implement-queue.mjs";

const logEntry = buildOptimizeLogEntry(today, sensorResult, issueCount);
appendLogEntry(".claude/improvement-loop/log.md", logEntry, DRY_RUN);
```

Log format (appended to `.claude/improvement-loop/log.md`):

```markdown
## YYYY-MM-DD

**queueEfficiency:** composite 0.820 (baseline 0.800) — healthy
**Difficulty distribution:** size:s:5, size:m:7
**Issues filed:** 0
```

## Step 4: Triage Regressions (only when flagged)

### 4a: Check if regression is real

```javascript
import { isRealRegression } from "./scripts/optimize-implement-queue.mjs";

if (!isRealRegression(sensorResult)) {
  // Log "difficulty-normalized: no action" and stop here.
}
```

`isRealRegression` applies the difficulty-normalization guard: if >80% of merged PRs are `size:xl` and the composite drop is <10%, the regression is treated as difficulty-explained, not a real process failure.

### 4b: Deduplicate against open issues

```bash
gh issue list --state open --search "queueEfficiency regression" \
  --json number,title --limit 10
```

Use `scripts/sensor-correlator.mjs` to group and deduplicate:

```javascript
import { correlate } from "./scripts/sensor-correlator.mjs";
const groups = correlate({ regressions: sensorResult.regressions }, openIssues);
```

Skip groups that already have an open issue matching the sensor + metric combination.

### 4c: File ready issues

For each non-duplicate regression group:

```javascript
import { buildRegressionIssueBody } from "./scripts/optimize-implement-queue.mjs";

const body = buildRegressionIssueBody(regression, sensorResult);
```

```bash
gh issue create \
  --title "fix(implement-queue): queueEfficiency <metric> regressed (<delta>)" \
  --label "ready,meta-improvement" \
  --body "<body from buildRegressionIssueBody>"
```

**Guardrails:**

- Max 2 issues per run (avoid noise)
- `ready` label only — do NOT add `in-progress` or auto-assign
- Never auto-merge, auto-edit skill prompts, or touch queue orchestration

## Step 5: Async Eval Trigger (regression path only)

When a regression is filed, schedule an async eval to distinguish agent/prompt quality issues from harder-task drift:

```bash
# Fire and forget — NEVER await this in the daily slot
nohup mbe agent run "Run eval suite to diagnose queue efficiency regression — check first-pass-success drop vs baseline" \
  --model sonnet --max-budget 2.00 --no-pr &
```

**CRITICAL:** Do NOT run `node tools/cli/dist/index.js agent eval --adapter claude-cli` synchronously. The daily slot must complete in under 5 minutes. Eval can take 20–60 minutes. Fire it as a background process or file a separate GitHub issue with label `ready,eval`.

## Step 6: Persist Metrics (always, unless --dry-run)

Cloud routines run in ephemeral checkouts, so appends that aren't committed are lost with the checkout. After Steps 0-3:

```bash
node scripts/persist-metrics.mjs --routine optimize-implement-queue
```

It stages every **durable** path with a diff (never `git add -A`), commits, pushes, and opens a PR titled `chore(metrics): optimize-implement-queue <YYYY-MM-DD>` labeled `has-pr`. Metrics-only diffs hit the low-risk fast path and auto-merge on green CI. No diff → exits 0 without a commit.

Do NOT enumerate paths by hand. Durability is declared once as `durable: true` in `scripts/metrics-store.mjs`; `durableManifest()` derives both the `.gitignore` negations and the staged list (#3645).

## Phase-2 Seam: Auto-Tuning (NOT YET BUILT)

The guard-railed model-routing tier adjustment pattern lives in `scripts/threshold-tuner.mjs`. When a regression persists across 3+ consecutive daily runs, phase-2 will:

1. Query `metrics/threshold-changes.jsonl` for recent guard-rail usage.
2. Call `determineAdjustment()` from `threshold-tuner.mjs` with per-sensor metrics.
3. Propose a model-tier bump via a `ready` issue (human approves before any config change).

**This is not built yet.** Commenting in the code would be: `// TODO(phase-2): wire threshold-tuner.mjs here once eval feedback loop is established`.

## Scheduling

This skill is designed to run daily. Wire it via a RemoteTrigger (HITL issue #2749):

| Trigger                        | Schedule    | Notes                                   |
| ------------------------------ | ----------- | --------------------------------------- |
| `mbe-optimize-implement-queue` | Daily (TBD) | Do NOT schedule until #2749 is approved |

Or invoke manually: `/optimize-implement-queue`

For `--dry-run` validation:

```bash
node scripts/sensor-report.mjs --json | jq '.sensors.queueEfficiency'
```

## Sensor Label Map

| Sensor          | Issue Label        | What It Checks                   |
| --------------- | ------------------ | -------------------------------- |
| queueEfficiency | `meta-improvement` | Composite efficiency index (0–1) |

## Rules

- **Read-only orchestration:** never mutate queue state, never edit issue prompts, never auto-merge
- **Max 2 issues per run** (consistent with learning-loop budget)
- **Append-only log** — never overwrite `.claude/improvement-loop/log.md`; after appending run `node scripts/cap-improvement-log.mjs` (keeps the newest 60 entries, older ones live in git history)
- **No synchronous eval** — eval runs async or as a filed issue
- **Difficulty-normalization required** — always call `isRealRegression()` before filing
- **Phase-2 (auto-tuning) is NOT built** — document the seam, do not implement it

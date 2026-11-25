---
name: meta-performance-loop
description: >-
  Polls deployed Meta, Facebook, and Instagram ads on demand or in a finite
  foreground watch; reads ad IDs from deployment_results.json, explicit IDs, or
  an ad-agent lineage run; calculates spend, revenue, purchases, ROAS, CPA, CTR,
  CPM, and frequency; applies operator-set winner/loser thresholds; and appends
  cited Markdown/JSON snapshots to performance history and lineage. Use when the
  user asks to monitor, check, poll, compare, or report post-deployment Meta ad
  performance, identify winners or losers, run a recurring performance check, or
  recommend the next creative test from measured results. Does not trigger for
  deploying ads, changing delivery or budgets, or generating creative assets.
---

# Meta performance loop

Run a read-only post-deployment measurement loop. The script makes Meta Insights
`GET` requests, writes local reports, appends one history record, and appends
`performance.snapshot` events through `scripts/lib/ad_agent_lineage.py`.

## Hard rules

1. **Read only.** Never pause, activate, archive, create, or edit an ad,
   campaign, ad set, audience, bid, schedule, or budget.
2. **No asset generation.** Recommendations describe a possible next test only.
   Do not invoke an image/video/copy generator from this workflow.
3. **Human thresholds only.** Ask the user for the decision thresholds. Do not
   silently infer targets from account history or invent profitability goals.
4. **Exact action type.** Confirm the Meta `action_type` that represents the
   conversion. `purchase`, `omni_purchase`, and
   `offsite_conversion.fb_pixel_purchase` are distinct.
5. **Preserve lineage.** Every selected ad must map to an existing lineage run.
   Never fabricate a run ID. If deployment/explicit IDs cannot be matched to an
   `ad.deployed` event, ask for `--lineage-run-id`.
6. **Never expose credentials.** Load `META_ACCESS_TOKEN` from the environment
   or `.env`; never pass it as an argument, print it, or persist token-bearing
   request/pagination URLs.
7. **Cite every recommendation.** Keep the structured metric/threshold
   citations in JSON and the rendered citations in Markdown.
8. **No implied causality.** Aggregate performance can rank an ad, but it does
   not prove which creative element caused the result.

Read [the data and classification contract](references/data-contract.md) before
changing thresholds, source parsing, metrics, or report fields. Use
[the scheduling examples](references/scheduling.md) when the user wants a
recurring job; never install a scheduler automatically.

## Prerequisites

From the repository root:

```bash
python3 --version
python3 -m pip install -r skills/meta-performance-loop/requirements.txt
```

Requirements:

- Python 3.9+
- `META_ACCESS_TOKEN` with `ads_read` access
- `META_AD_ACCOUNT_ID` in `.env`, or `--ad-account`
- An existing `outputs/ad-agent/lineage.jsonl` run containing deployment
  provenance
- Operator-selected thresholds for minimum spend, winner ROAS, loser ROAS, and
  winner purchase count

The token is loaded from the repository `.env` by default. Use `--env-file` for
another dotenv path. Do not place a token in shell history or scheduler config.

## Required decisions

Confirm these before polling:

1. **Ad source:** one `deployment_results.json`, explicit ad IDs, or one lineage
   `run_id`.
2. **Ad account:** account ID with or without `act_`.
3. **Conversion action type:** exact Meta action key used for purchases/revenue.
4. **Primary window:** the only window used for status.
5. **Comparison window:** context only; default `yesterday`, or disable it.
6. **Thresholds:** at minimum:
   - `--min-spend`
   - `--winner-roas`
   - `--loser-roas`
   - `--winner-min-purchases`
7. Optional CPA, frequency, and CTR thresholds.

Meta date presets and explicit ranges use the ad account timezone. Monetary
metrics remain in the ad account currency.

## Source modes

Choose exactly one.

### 1. Deployment results

```bash
python3 skills/meta-performance-loop/scripts/poll_meta_performance.py \
  --deployment-results outputs/meta-ads/<run>/deployment_results.json \
  --lineage-run-id <RUN_ID> \
  --min-spend 50 --winner-roas 2 --loser-roas 1 \
  --winner-min-purchases 2
```

The current `meta-ad-builder` shape is an object with an `ads` list containing
`ad_id`. `dry_run` IDs are ignored. If the file has a `run_id`, that existing
run is used. Otherwise the script searches `ad.deployed` events and requires
`--lineage-run-id` only when it cannot associate every ad.

### 2. Explicit ad IDs

```bash
python3 skills/meta-performance-loop/scripts/poll_meta_performance.py \
  --ad-id 123456789012345 --ad-id 987654321098765 \
  --lineage-run-id <RUN_ID> \
  --min-spend 50 --winner-roas 2 --loser-roas 1 \
  --winner-min-purchases 2
```

IDs can also be comma-separated. They must be numeric Meta ad IDs. Explicit IDs
still need existing lineage provenance.

### 3. Lineage run

```bash
python3 skills/meta-performance-loop/scripts/poll_meta_performance.py \
  --run-id <RUN_ID> \
  --min-spend 50 --winner-roas 2 --loser-roas 1 \
  --winner-min-purchases 2
```

This reads ad IDs only from the run's `ad.deployed` events or an explicitly
recorded `deployment_results_path`. Because lineage is persisted input, that
recorded path must be repository-relative, contain no `..` traversal, and
resolve inside the repository (including after symlink resolution). In
contrast, an operator-supplied `--deployment-results` path is an explicit
trusted CLI choice and may be absolute or outside the repository.

## Configure metrics and windows

The default primary/comparison pair is `last_7d` and `yesterday`, matching the
generalized long-window + recent-window pattern:

```bash
python3 skills/meta-performance-loop/scripts/poll_meta_performance.py \
  --run-id <RUN_ID> \
  --primary-window last_7d \
  --comparison-window yesterday \
  --action-type purchase \
  --min-spend 100 --winner-roas 2.5 --loser-roas 1 \
  --winner-min-purchases 3 \
  --winner-max-cpa 60 --loser-min-cpa 100 \
  --frequency-watch-above 3 --ctr-watch-below 1
```

Use explicit inclusive ranges when presets are not appropriate:

```bash
--primary-since 2026-07-01 --primary-until 2026-07-07 \
--comparison-since 2026-06-24 --comparison-until 2026-06-30
```

Use `--no-comparison` for one window. Never compare volume totals as though two
windows had equal duration; the report uses comparison efficiency only as
directional context.

## Deterministic statuses

Only these values are permitted:

- `insufficient-data`: primary spend is below `min_spend`, or impressions are
  zero.
- `winner`: enough data, ROAS meets `winner_roas`, purchases meet
  `winner_min_purchases`, and optional winner CPA passes.
- `loser`: enough data and ROAS meets `loser_roas`, or optional loser CPA
  triggers.
- `watch`: enough data but neither decision is met, or configured winner/loser
  signals conflict.

Status uses the primary window only. Frequency and CTR watch thresholds add
cited test guidance but do not silently override status.

## Outputs

Every successful iteration writes:

```text
outputs/meta-performance/
├── history.jsonl
├── latest.json
├── latest.md
└── reports/
    ├── <timestamp>-<snapshot>.json
    └── <timestamp>-<snapshot>.md
```

`history.jsonl` is append-only. Each associated run also receives one
`performance.snapshot` event in `outputs/ad-agent/lineage.jsonl` with the same
`snapshot_id`, metrics, thresholds, recommendations, and report paths.

The reports contain:

- primary and optional comparison metrics per ad
- aggregate summaries
- one of the four statuses per ad
- the exact thresholds used
- next-test recommendations with structured data citations
- an explicit read-only guarantee and interpretation limits

Review both report formats. JSON is canonical; Markdown is the human handoff.

## Finite foreground watch

One iteration is the default. To watch in the current terminal:

```bash
python3 skills/meta-performance-loop/scripts/poll_meta_performance.py \
  --run-id <RUN_ID> \
  --min-spend 50 --winner-roas 2 --loser-roas 1 \
  --winner-min-purchases 2 \
  --watch-iterations 6 --interval-seconds 300
```

The process stops after the requested finite count. There is no forever mode.
The output lock rejects overlapping poll/watch processes.

For unattended recurrence, use a one-shot scheduler example from
`references/scheduling.md`; do not run watch mode inside cron/launchd.

## Review and handoff

After polling:

1. Confirm the action type and windows in `latest.md`.
2. Confirm thresholds reflect the user's economics.
3. Check that every recommendation includes concrete data citations.
4. Present statuses as rules applied to observed data, not objective truth.
5. Ask which recommended test, if any, the user wants to plan separately.
6. Do not execute the recommendation, mutate Meta state, or generate assets.

## Recovery

- **No lineage association:** append/fix the upstream `ad.deployed` event or
  provide the correct existing `--lineage-run-id`; do not invent one.
- **No insight row:** the ad is represented with zero spend and
  `insufficient-data`.
- **401/403:** refresh permissions/token in `.env`; never paste the token into
  the command.
- **429/5xx/transient Meta error:** bounded retries are automatic. Rerun the same
  one-shot command after the error clears.
- **Wrong purchase/revenue totals:** verify the exact `--action-type`; the
  script intentionally does not merge aliases.
- **Overlapping process:** wait for the active process or stop it manually.
- **Partial local append:** reconcile by `snapshot_id`; never rewrite prior
  JSONL lines.

## Offline verification

These checks make no Meta API calls:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover \
  -s skills/meta-performance-loop/tests \
  -p "test_*.py" \
  -v

PYTHONDONTWRITEBYTECODE=1 \
  python3 skills/meta-performance-loop/scripts/poll_meta_performance.py --help
```

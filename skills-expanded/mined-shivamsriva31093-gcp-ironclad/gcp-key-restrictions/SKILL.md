---
name: gcp-key-restrictions
description: Use to apply API-target restrictions to fully-unrestricted GCP API keys, inferring the allow-list from recent usage signals. Idempotent. Honors `--dry-run`. Use standalone or as Phase 3b of `gcp-ironclad`.
---

# GCP Key Restrictions (APPLY)

## Overview

For each API key flagged `CRITICAL` (unrestricted) by `gcp-credentials-audit`, queries the last 30 days of Cloud Monitoring `request_count` filtered by that key's `credential_id`, and — if the usage signal is unambiguous — restricts the key to exactly those APIs via `gcloud services api-keys update`. Keys with no usage signal, signals spanning >5 APIs, signals that include a spend-capable API, or that are <7 days old are demoted to "flag for review" rather than auto-restricted.

**Usage is not proof of legitimacy.** On an unrestricted key, an attacker's traffic is "usage" too: inferring the allow-list from it would allow-list the abuse. Two rules keep that from happening: only successful (2xx) calls count, so probes rejected by the API are not evidence, and any signal that includes a spend-capable API (the paid set `gcp-spend-guardrails` Action 3 watches, plus Firebase AI Logic) goes to a human. The driver's active-spike halt only catches a fast spike, and an account without a billing export can't be spike-checked at all.

## When to Use

- Triggered by `gcp-ironclad` as Phase 3b, after `gcp-spend-guardrails`.
- Or standalone when you have a known list of unrestricted keys to lock down.

## Inputs

- `SESSION_DIR` (must contain a fresh `audit.json` with `riskClass = "CRITICAL"` entries).
- `DRY_RUN` env var (default `0`).
- `MAX_INFERRED_APIS` env var (default `5` — keys with usage across more APIs are flagged, not auto-restricted).
- `LOOKBACK_DAYS` env var (default `30`).

## Outputs

Writes `${SESSION_DIR}/key-restrictions.json` matching `output.schema.json`.

## Execution

### Step A: Load candidate keys

```bash
jq -r '.credentials[] | select(.type == "api_key" and .riskClass == "CRITICAL") | "\(.project)\t\(.uid)\t\(.displayName)\t\(.createTime)"' \
  "${SESSION_DIR}/audit.json" > "${SESSION_DIR}/restriction-candidates.tsv"
wc -l "${SESSION_DIR}/restriction-candidates.tsv"
```

### Step B: For each candidate, query usage

For each line `(project, uid, displayName, createTime)`:

1. If `createTime` is within the last 7 days → outcome `"flagged"`, reason `"too_fresh"`.
2. Else query Monitoring `serviceruntime.googleapis.com/api/request_count` for that key's successful calls, one series per service, over `LOOKBACK_DAYS`. Both `credential_id` and `service` are **resource** labels of `consumed_api`, not metric labels; grouping by `metric.label.service` collapses everything into one series with no service, so the set comes back empty and every key is flagged `no_usage_signal`. The reducer is required, or the API ignores `groupByFields`. `response_code_class="2xx"` keeps rejected calls (probes, wrong-API attempts) out of the set:
   ```bash
   TOKEN=$(gcloud auth application-default print-access-token 2>/dev/null || gcloud auth print-access-token)
   curl -s -G "https://monitoring.googleapis.com/v3/projects/${P}/timeSeries" \
     -H "Authorization: Bearer ${TOKEN}" \
     --data-urlencode "filter=metric.type=\"serviceruntime.googleapis.com/api/request_count\" AND resource.type=\"consumed_api\" AND resource.label.credential_id=\"apikey:${uid}\" AND metric.label.response_code_class=\"2xx\"" \
     --data-urlencode "interval.startTime=${START}" --data-urlencode "interval.endTime=${END}" \
     --data-urlencode 'aggregation.alignmentPeriod=86400s' \
     --data-urlencode 'aggregation.perSeriesAligner=ALIGN_SUM' \
     --data-urlencode 'aggregation.crossSeriesReducer=REDUCE_SUM' \
     --data-urlencode 'aggregation.groupByFields=resource.label.service' \
     | jq -r '.timeSeries[]? | select(([.points[]? | (.value.int64Value // "0" | tonumber)] | add) > 0) | .resource.labels.service' | sort -u
   ```
   A response with an `error` body is the `no_signal_access` case below, not an empty set.
3. Collect the set of unique services with non-zero counts.
   - If set is empty → outcome `"flagged"`, reason `"no_usage_signal"`.
   - If set size > `MAX_INFERRED_APIS` → outcome `"flagged"`, reason `"signal_too_broad"`.
   - If the set contains a spend-capable API (`generativelanguage.googleapis.com`, `aiplatform.googleapis.com`, `firebasevertexai.googleapis.com`, `maps-backend.googleapis.com`, `translate.googleapis.com`) → outcome `"flagged"`, reason `"spend_capable_api_in_signal"`. Whether that traffic is the owner's or the abuser's is a human call. The flag carries the inferred set and the restrict command with and without the spend-capable entries.
   - Otherwise the set is the proposed `apiTargets`.

### Step C: Apply the restriction

If `DRY_RUN=0` and outcome is to apply:
```bash
TARGETS=$(printf -- '--api-target=service=%s ' ${INFERRED_APIS[@]})
gcloud services api-keys update "${uid}" --project="${P}" ${TARGETS}
```
Record `before` (was `null` since unrestricted) and `after` (the new `apiTargets` list).
Rollback for the report: `gcloud services api-keys update ${uid} --project=${P} --clear-api-target`.

### Step D: Write `key-restrictions.json`

Atomic write, summary:

> Key restrictions complete (dryRun=${DRY_RUN}). Applied: A. Flagged for review: B (no signal: X / too broad: Y / spend-capable: W / too fresh: Z). Skipped: C. Output: `${SESSION_DIR}/key-restrictions.json`.

## Error handling

- Monitoring API permission denied → outcome `"flagged"`, reason `"no_signal_access"`.
- `gcloud services api-keys update` fails → emit `error`, mark outcome `"skipped"` with reason `"update_failed"`.
- Key already deleted between audit and now → emit `error`, skip.

## Never auto-applied

This skill **never** deletes a key. If a key looks abandoned and unused, that decision is for the human. The flag-for-review report includes the one-line `gcloud services api-keys delete ${uid} --project=${P}` for the human to run.

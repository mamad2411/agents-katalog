---
name: gcp-spend-guardrails
description: Use to apply blast-radius spend controls on GCP projects — quota caps on `generativelanguage.googleapis.com`, Cloud Billing budget alerts, disabling paid APIs idle on projects with no recent legitimate usage, and flagging where a hard spend-cap budget (Public Preview, console-only) should be added. Idempotent. Honors `--dry-run`. Use standalone or as Phase 3a of `gcp-ironclad`.
---

# GCP Spend Guardrails (APPLY)

## Overview

Per project, applies three blast-radius controls — but only when each is genuinely safe per the safety matrix in `docs/superpowers/specs/2026-05-24-gcp-api-key-ironclad-skill-design.md` §6. Actions that fail the safety gate are demoted to "flag for review" and surfaced for the human, never auto-applied.

## When to Use

- Triggered by `gcp-ironclad` as Phase 3a, after the read-only audits.
- Or invoked standalone when you want only the spend-control half of the suite.

## Inputs

- `SESSION_DIR` env var (must already contain `audit.json` and `anomalies.json` from prior phases when invoked by the driver).
- `DRY_RUN` env var: if `1`, plan all actions but apply none. Default `0`.
- `QUOTA_FLOOR_PER_DAY` env var: minimum daily request quota for Gemini API. Default `5000`.
- `QUOTA_MULTIPLIER` env var: peak-multiplier for quota sizing. Default `5`.

## Outputs

Writes `${SESSION_DIR}/guardrails-applied.json` matching `output.schema.json`.

## Safety matrix (excerpt)

| Action | Auto-apply ONLY when | Demoted to "flag" when |
|---|---|---|
| Set Gemini API quota | API enabled + ≥7d usage + proposed > peak | No usage data; new project (<7d); export missing |
| Quota sizing | `max(peak_30d × 5, 5000/day)` | Peak shows abuse signature → use floor only |
| Create budget alerts | caller is `billing.admin` + no existing budget at threshold | viewer-only; budget already configured |
| Recommend spend-cap budget | never auto-applied — console-only (no gcloud/API surface as of July 2026), and pausing a live service is a human call | always flagged, never applied |
| Disable idle API | zero 30-d usage + enabled >7d + not `sys-*` | any usage in 30d; enabled <7d; system project |

## Execution

### Action 1 — Quota on `generativelanguage.googleapis.com`

For each project where `generativelanguage.googleapis.com` is enabled:

1. Read peak daily request count from the last 30 days via Monitoring API (same metric as the audit). If <7 days of data → skip with reason `"insufficient_usage_data"`.
2. Compute `target = max(peak * QUOTA_MULTIPLIER, QUOTA_FLOOR_PER_DAY)`.
3. **Anti-abuse guard:** if peak is itself a known abuse signature (e.g., the project appears in `anomalies.json` with `multipleOver > 100`), use `QUOTA_FLOOR_PER_DAY` instead of `peak * QUOTA_MULTIPLIER`.
4. Compare against current quota; if equal → outcome `"skipped"` with reason `"already_at_target"`.
5. Otherwise (and not `DRY_RUN`), apply via:
   ```bash
   gcloud alpha services quota update \
     --consumer="projects/${P}" \
     --service="generativelanguage.googleapis.com" \
     --metric="generativelanguage.googleapis.com/generate_content_paid_requests" \
     --unit="1/d/{project}" \
     --override-value="${target}" \
     --force
   ```
   Rollback (record in `details.rollback`):
   ```
   gcloud alpha services quota update --consumer=projects/${P} --service=generativelanguage.googleapis.com --metric=... --unit=... --override-value=<previous>
   ```
6. **If `gcloud alpha services quota update` is unavailable (alpha-surface drift),** fall back to the REST API:
   ```bash
   curl -X POST \
     -H "Authorization: Bearer $(gcloud auth application-default print-access-token)" \
     -H "Content-Type: application/json" \
     "https://serviceusage.googleapis.com/v1beta1/projects/${P}/services/generativelanguage.googleapis.com/consumerQuotaMetrics/.../limits/.../consumerOverrides" \
     -d "{\"overrideValue\":\"${target}\"}"
   ```

### Action 2 — Budget alerts

For each billing account where the caller is `billing.admin`:

1. Compute `last_30d_spend` from the export (or `mcp__gcp-finops__cost_summary` if MCP available).
2. For each multiplier in `[1, 2, 5]`:
   - Target name: `gcp-ironclad-budget-{mult}x`
   - Check existing budgets: `gcloud billing budgets list --billing-account=${B} --format=json`. If a budget with the same `displayName` exists → skip with reason `"already_exists"`.
   - Otherwise (and not `DRY_RUN`):
     ```bash
     gcloud billing budgets create \
       --billing-account="${B}" \
       --display-name="gcp-ironclad-budget-${mult}x" \
       --budget-amount="$(echo "${last_30d_spend} * ${mult}" | bc)" \
       --threshold-rule=percent=1.0 \
       --calendar-period=month
     ```
   - Rollback: `gcloud billing budgets delete <BUDGET_ID> --billing-account=${B}`

These budgets **alert only** — they do not stop spending. For hard enforcement see Action 2b.

### Action 2b — Flag spend-cap budget candidates (Public Preview, console-only)

Since **July 29, 2026**, [spend caps on budgets](https://docs.cloud.google.com/billing/docs/how-to/budgets-spend-caps) (Public Preview) can *pause* a service within minutes of a monthly threshold. As of this writing there is **no gcloud or Billing Budget API surface** — creation is console-only — and pausing a live service can take down production traffic (blocked calls get permission errors). So this action **never applies anything**; it emits one flag per candidate.

To act on these flags with guided discovery, sizing, and post-creation verification, run the **`gcp-spend-cap-setup`** skill — it consumes this file's `recommend_spend_cap` entries directly.

1. Eligible services (July 2026): `generativelanguage.googleapis.com` (Gemini API), `aiplatform.googleapis.com` (Agent Platform), `run.googleapis.com` (Cloud Run), `cloudfunctions.googleapis.com` (Cloud Run functions). Re-check the docs page — coverage will likely expand.
2. For each project in scope, for each eligible service that is enabled with any 30-day usage, emit a flag entry with reason `"spend_cap_recommended"` and details:
   - Console path: **Billing → Budgets & alerts → Create budget → budget type "Spend cap"**, scope = this project + this service, monthly amount sized like Action 2 (suggest the `2x` multiplier of that service's 30-day spend as a starting point).
   - Caveats to surface verbatim: one project + one service per cap; fixed monthly window; enforcement uses gross *estimated* costs, is not instant, and overage during the lag still bills; commitment fees (CUDs, provisioned throughput) keep billing; lifting the cap is manual and can take up to an hour to fully resume.
3. If a spend-cap budget for that project+service already exists (visible in `gcloud billing budgets list` output or the console), skip with reason `"already_exists"`.

### Action 3 — Disable idle paid APIs

For each project, for each of `generativelanguage.googleapis.com`, `aiplatform.googleapis.com`, `maps-backend.googleapis.com`, `translate.googleapis.com`:

1. Check enabled: `gcloud services list --project=${P} --enabled --filter="config.name:${api}"`. If not enabled → skip.
2. Skip if project ID starts with `sys-` (Google-managed).
3. Read 30-day usage via Monitoring (`request_count`). If usage > 0 → skip with reason `"recent_usage"`. If API enabled <7 days ago → skip with reason `"too_fresh"`.
4. Otherwise (and not `DRY_RUN`):
   ```bash
   gcloud services disable "${api}" --project="${P}" --quiet
   ```
   Rollback: `gcloud services enable ${api} --project=${P}`

### Write `guardrails-applied.json`

Atomic write, same pattern as audit.json. Print summary:

> Spend guardrails applied (dryRun=${DRY_RUN}). Quotas: A applied / B skipped / C flagged. Budgets: D applied / E skipped. Spend-cap candidates flagged: H (console-only, review required). Idle-API disable: F applied / G skipped. Output: `${SESSION_DIR}/guardrails-applied.json`.

## Error handling

- `alpha services quota update` not available → automatically fall back to REST API.
- Lacking permission for any action → emit `error` and continue.
- Any HTTP/CLI failure → emit `error` with full message; do not abort other actions.

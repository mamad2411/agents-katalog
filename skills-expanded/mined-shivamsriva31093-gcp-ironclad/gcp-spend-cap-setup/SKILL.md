---
name: gcp-spend-cap-setup
description: Use to set up Google Cloud hard spend caps (Public Preview, July 2026) with guided discovery, sizing, and post-creation verification. Spend caps are console-only — this skill prepares everything, walks you through the one manual step, and verifies the result. GUIDED — runs only read-only commands. Triggers on "set up spend cap", "hard cap gcp", "cap gemini spend", "spend cap setup".
---

# GCP Spend-Cap Setup (GUIDED)

## Overview

Google's [spend caps on budgets](https://docs.cloud.google.com/billing/docs/how-to/budgets-spend-caps) (Public Preview since 2026-07-29) actually pause a service when a monthly threshold is hit — but creation is **console-only**: the Billing Budget API v1 has no enforcement field and `gcloud billing budgets create` has no cap flag. This skill is therefore **GUIDED**: it runs only read-only commands itself; you perform the single mutation in the console; the skill prepares everything before and verifies everything after.

A tripped cap returns permission errors (403) to ALL callers of that service, including production. Choosing to cap is a human decision — that is by design.

## When to Use

- Standalone, whenever you want hard caps on AI/serverless spend.
- After a `gcp-ironclad` run: the final report's `recommend_spend_cap` flags point here.
- **During an active incident.** Unlike the APPLY skills, there is no bleeding-halt gate — a spend cap is precisely the emergency brake, so this skill must work while a project is bleeding.

## Inputs

- `SESSION_DIR` env var — session directory; create `/tmp/gcp-ironclad/<iso-ts>/` if unset (same convention as the other skills).
- `MODE` env var — unset for a full run; `verify` to skip to Step 4 using a prior `${SESSION_DIR}/spend-caps.json`.
- No `DRY_RUN`: the skill never mutates, so there is nothing to dry-run.

## Outputs

- `${SESSION_DIR}/spend-caps.json` — matches `output.schema.json`, self-validated at the end.
- `${SESSION_DIR}/spend-cap-runbook.md` — the console runbook, kept for audit trail.

## Execution

### Step 0 — Preflight + API-surface probe

1. Print the active CLI and ADC identities so a mismatch is visible before anything silently 403s:
   ```bash
   gcloud auth list --filter=status:ACTIVE --format="value(account)"
   gcloud auth application-default print-access-token >/dev/null 2>&1 || echo "WARN: no ADC credentials — run: gcloud auth application-default login"
   ```
   If the ADC identity is known to differ from the CLI identity, warn: ADC is a separate login; a mismatch produces silent PERMISSION_DENIED on API calls.
2. Probe the Budget API surface for future enforcement support:
   ```bash
   curl -s "https://billingbudgets.googleapis.com/\$discovery/rest?version=v1" \
     | jq -r '.schemas.GoogleCloudBillingBudgetsV1Budget.properties | keys[]' \
     | grep -iE "enforce|cap|pause" || true
   ```
   - No match (today's state) → `apiSurfaceDetected: false`.
   - Any match → `apiSurfaceDetected: true`; print: **"Budget API now exposes an enforcement-like field — Google may have shipped API support for spend caps. This skill predates that; check the docs and consider upgrading it. Continuing in guided mode."** Do NOT attempt to use the field.

### Step 1 — Discovery (read-only)

Skip this step entirely when `MODE=verify`.

1. **Shortcut:** if `${SESSION_DIR}/guardrails-applied.json` exists, take every action with `"kind": "recommend_spend_cap"` as the candidate list (project + service from `target`/`details`), then continue to sub-step 4 to refresh spend numbers. For each seeded candidate, resolve the project's billing account first: `gcloud billing projects describe ${P} --format='value(billingAccountName)'` — later steps and the output's `billingAccount` field need it.
2. Otherwise enumerate scope:
   ```bash
   gcloud billing accounts list --format=json
   gcloud billing projects list --billing-account=${B} --format=json   # per account
   ```
3. Per project, find eligible services enabled (as of July 2026 — re-check the [docs page](https://docs.cloud.google.com/billing/docs/how-to/budgets-spend-caps), coverage will likely expand):
   ```bash
   gcloud services list --project=${P} --enabled \
     --filter="config.name:(generativelanguage.googleapis.com OR aiplatform.googleapis.com OR run.googleapis.com OR cloudfunctions.googleapis.com)" \
     --format="value(config.name)"
   ```
4. Per project+service pair, get 30-day spend: `mcp__gcp-finops__cost_summary` if the MCP is available → else `bq query` against the billing-export table (same query shape as `gcp-cost-anomaly-scan`) → else record `null` (no default sizing; the user will supply an amount).
5. Detect existing caps for idempotency:
   ```bash
   gcloud billing budgets list --billing-account=${B} --format=json
   ```
   Any budget whose `displayName` starts with `gcp-ironclad-spendcap-` and whose filter matches a candidate pair → that pair's outcome is `already_exists`; exclude it from selection (still list it in the output).
6. Zero candidates overall → print "No eligible services with billable usage found — nothing to cap." Write the output file with an empty selection and stop.

### Step 2 — Selection (interactive)

1. Present candidates via AskUserQuestion, multi-select, sorted by 30-day spend descending. Each option label: `{project} · {svc-short} · {currency}{spend_30d}/30d`.
2. For each selected pair, propose the monthly amount: **2 × 30-day spend, rounded to a clean figure** in the billing account's currency. No spend data → no proposal; ask the user for a number. The user can override any amount.
3. Record every candidate: selected pairs carry `amountChosen`; unselected pairs get outcome `skipped`, `amountChosen: null`.

### Step 3 — Runbook

For each selected cap, print AND append to `${SESSION_DIR}/spend-cap-runbook.md`:

```
## Cap: {project} / {service}

1. Open: https://console.cloud.google.com/billing/{ACCOUNT_ID}/budgets/create
2. Budget type: **Spend cap** (Preview)
3. Name: gcp-ironclad-spendcap-{project}-{svc-short}      (svc-short: gemini | vertex | run | gcf)
4. Scope: project = {project}, service = {service-display-name}   (one project + one service — platform constraint)
5. Amount: {currency} {amountChosen} / month

Caveats (read before saving):
- Enforcement lags — overage during the lag is still billed (caps use gross ESTIMATED costs).
- When tripped, the service returns permission errors (403) to ALL callers, including production.
- Commitment fees (CUDs, provisioned throughput) continue billing at their flat rate.
- Lifting the cap is manual (edit budget → "Lift spend cap") and can take up to ONE HOUR to fully resume.
```

### Step 4 — Verify loop

1. Ask the user to reply **done** when caps are created (or **skip {displayName}** to abandon one). In `MODE=verify`, load the planned caps from the prior `${SESSION_DIR}/spend-caps.json` first.
2. On "done":
   ```bash
   gcloud billing budgets list --billing-account=${B} --format=json
   ```
   Match each planned cap on: `displayName` + `budgetFilter.projects` contains the project + `budgetFilter.services` contains the service + `amount` equals `amountChosen`.
3. **Honest limitation — state it every run:** the v1 API has no enforcement field, so this verifies name/scope/amount but **cannot confirm the budget type is "Spend cap."** Ask the user to confirm they selected the Spend-cap type: confirmed → `enforcementVerified: "manual-attestation"`; otherwise `"unconfirmed"`.
4. Matched → outcome `verified`. Not matched → offer one retry (re-list after the user checks); still missing → outcome `not_found`.

### Step 5 — Output

1. Write `${SESSION_DIR}/spend-caps.json` atomically (write `.tmp`, `mv` into place) with every candidate pair and the probe result.
2. Self-validate against `${SKILL_DIR}/output.schema.json`, where `SKILL_DIR` is this skill's directory (where SKILL.md lives): `jsonschema -i ${SESSION_DIR}/spend-caps.json ${SKILL_DIR}/output.schema.json` if the CLI is available; otherwise a structural `jq` check (top-level keys present, every cap has the required fields, outcomes within the enum).
3. Print the summary:

> Spend-cap setup: {N} candidates, {M} selected, {K} verified (name/scope/amount), {J} user-attested as Spend-cap type, {S} skipped. Output: `${SESSION_DIR}/spend-caps.json`.

## Error handling

- No billing accounts visible → exit with: "No billing accounts visible to {identity}. Check `gcloud auth list` and billing IAM (Billing Account Administrator or Costs Manager + Project Owner/Editor are required to create caps)." Not an error dump.
- Spend-data lookup failures (missing export, `bq` errors) degrade to user-supplied amounts; never abort.
- Every `gcloud`/`bq`/`curl` failure → append `{context, message}` to `errors[]` and continue.
- User abandons mid-run → write the output file anyway with what was decided; unresolved pairs get `skipped`.

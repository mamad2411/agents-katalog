---
name: email-verification
description: Verify email addresses and clean lead lists with the Caeros enrichment engine (MillionVerifier / BounceBan). Use when asked to verify emails, check deliverability, clean or dedupe an email list, or prepare a send list for a campaign.
---

# Email Verification

The Caeros gateway runs a server-side enrichment engine: it splits, dedupes,
and verifies email lists of any size (one address to a million), caches every
verdict for 30 days, and exports CSV. You drive it with the native
`enrich_*` tools; runs keep going even if the session disconnects.

## The flow (always in this order)

1. **`enrich_providers`** — confirm a provider is configured (free).
2. **`enrich_email_preview`** — verify a REPRESENTATIVE sample of up to 10
   addresses synchronously. Show the user the verdicts and the total list
   size. This is the review gate: never launch a full run before the user
   has seen a sample forecast and agreed.
3. **`enrich_run_start`** — launch the full run with `confirm_spend: true`
   only after the user agrees. Pass the addresses as `emails` (array) or
   `text` (raw CSV/lines; the gateway extracts and dedupes).
4. **`enrich_run_status`** — poll the counters. Do NOT busy-poll: the tool
   directs you to stop after a few still-running snapshots; small runs
   finish in seconds, large ones continue server-side regardless.
5. **`enrich_run_results`** — page per-address results, or filter with
   `status: "deliverable"` to get just the send-safe rows.
6. **`enrich_run_cancel`** — stop a running run; verified rows keep their
   results (and stay cached).

## Verdicts (normalized across providers)

| status | meaning | typical reasons |
|---|---|---|
| `deliverable` | mailbox confirmed, safe to send | |
| `risky` | exists but delivery unsure | `catch_all` (domain accepts everything), `disposable` |
| `undeliverable` | do not send | `no_mailbox`, `dns_error`, `syntax` |
| `unknown` | provider could not decide | retry later or treat as risky |

- `cached: true` rows cost zero credits (verdicts cached 30 days; a preview
  warms the cache, so previewed addresses are free again in the full run).
- Syntactically invalid addresses are rejected by the local checker
  (`provider: "local"`, reason `syntax`) at zero cost and zero latency.
- Cost: up to 1 provider credit per never-seen address, nothing else.

## Big lists: the workflow kind

For a list produced by another task (file extraction, a scrape, an upstream
agent), use a `workflow_run` task with `kind: "enrich"` — one task is the
whole run, no per-row fan-out (prefer the prompt carrying the whole list; a
`foreach` on an enrich task is tolerated but collapses into that same
single gateway run):

```json
{"name":"verify-leads","tasks":[
  {"id":"extract","prompt":"Extract every email address from ~/leads.csv and output them one per line."},
  {"id":"verify","kind":"enrich","prompt":"${task:extract}","deps":["extract"]}
]}
```

The enrich task's prompt is the address source text; its output is
`{run_id, status, total_items, counters}`. Put the preview forecast in the
run description so the launch approval card shows what will be spent.

## Providers

`millionverifier` is preferred when both are configured; `bounceban` is the
alternative. Pin one per run with the `provider` argument, or omit it for
the gateway default. If no provider is configured, `enrich_run_start` fails
with `provider_unavailable` — load the `lead-enrichment-setup` skill.

## CSV export

The full results CSV (all columns: status, reason, provider fields,
cached, error class) streams from the gateway API:

```
GET {gateway}/v1/enrich/runs/{run_id}/results?format=csv
Authorization: Bearer <session JWT>
```

Optional `status=<verdict>` filters the export. For in-chat summaries
prefer the counters from `enrich_run_status` over paging every row.

## Domain discovery mode (find people AND their emails)

When the user gives company domains instead of an email list ("find people
at acme.com and verify their emails"), the same run pipeline does the whole
job server-side: FullEnrich People Search discovers the people, FullEnrich
waterfall enrichment finds their work emails, and the verification provider
confirms them. One run id, one CSV.

Flow, in order:

1. `enrich_people_search` with the domains (plus title/seniority filters if
   the user gave any). Show the user WHO was found and the TOTAL matching
   count. This costs ~0.25 credits per person returned, so keep the limit
   small (default 10).
2. Quote the cost shape: ~0.25 credits per person discovered in the full
   run, 1 FullEnrich credit per work email FOUND (misses are free), and
   verification (cached addresses free). Wait for the user's go.
3. `enrich_run_start` with `domains` (and `titles`/`seniorities`/
   `max_people` as agreed) and `confirm_spend=true`.
4. Poll `enrich_run_status`; report `found` / `not_found` alongside the
   verify verdicts when it finishes.

NEVER set `include_phones` (10 credits each) or `include_personal_emails`
(3 credits) unless the user explicitly asked for phones or personal emails.

The CSV for domain runs is one row per person (name, headline, LinkedIn
URL, work email, find + verify verdicts) with a `payload_json` column
carrying every field FullEnrich returned. If FullEnrich is not configured,
`enrich_people_search` fails with `provider_unavailable` — load the
`lead-enrichment-setup` skill (`FULLENRICH_API_KEY`).

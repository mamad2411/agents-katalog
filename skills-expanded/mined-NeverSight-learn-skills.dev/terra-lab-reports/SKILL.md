---
name: terra-lab-reports
description: Best practices and API reference for Terra Lab Reports (pre-release) – convert clinical lab report PDFs and images into structured, standardized biomarker data. Use when parsing blood test results, extracting biomarkers, mapping to LOINC or UCUM unit codes, handling reference ranges, handling lab_report.completed / lab_report.failed webhooks, or working with PDF lab results and lab report OCR. Covers the async upload/standardize/deliver lifecycle, the event envelope (event_id, upload_id), the layered result model (source, biomarker, measurement, interpretation, reference ranges), unmatched-biomarker handling, snowflake IDs, and idempotent webhook processing.
license: MIT
compatibility: Requires network access to docs.tryterra.co for full endpoint specs, payload examples, and enum tables
metadata:
  author: terra
  version: "1.0.0"
---

# Terra Lab Reports Best Practices

Production guidelines and API reference for building with the Terra Lab Reports API (**pre-release**). It converts clinical lab report PDFs and images into structured, standardized biomarker data: OCR plus AI extraction, then fuzzy matching against a reference dataset of 4,000+ biomarkers that yields canonical biomarker keys, UCUM unit codes, and LOINC codes.

**Pre-release: assume the contract may move.** Fetch the live docs pages before generating production request bodies or webhook parsers, and verify against the live API before shipping.

## What the Product Does

Upload a clinical lab report and receive structured biomarker results – extracted, standardized, and delivered to your destinations or available via REST.

- **Input:** one file per request – PDF, PNG, JPEG, GIF, or WebP, up to 20 MB.
- **Extraction:** OCR plus AI parsing pulls each result's name, value, units, flags, and reference ranges off the page.
- **Standardization:** each extracted name is fuzzy-matched (threshold 0.85) against the 4,000+ entry biomarker dataset, producing a canonical biomarker key, a UCUM-compliant `ucum_code`, and (for the subset with a LOINC mapping) a `loinc_code`.
- **Output:** a Session containing layered Results (source / biomarker / measurement / interpretation / reference ranges) grouped under report-level Panels, delivered as a `lab_report.completed` event (or `lab_report.failed` on terminal failure).

## Async Workflow and Status Lifecycle

Processing is fully asynchronous. Upload returns immediately with `202` and an **`upload_id`** (`current_status: "processing"`) and the report moves through:

```
processing → processed → standardizing → standardized → sending → sent
```

Other statuses: `retry_scheduled`, `retrying`, `cancelled`, `deleted`, and `failed`. Terminal states are `sent`, `failed`, `cancelled`, `deleted`.

**Results are queryable once the session reaches `standardized`** – before delivery. You do not have to wait for `sent` to read them. Learn the outcome via the webhook events (`lab_report.completed` on success, `lab_report.failed` on terminal failure) or by polling. Processing typically takes 30 seconds to 3 minutes.

## Endpoints

Base URL `https://access.tryterra.co/api`. Every request needs both headers: `dev-id` and `x-api-key`.

| Method | Endpoint                                  | Notes                                                                                                                                                                                         |
| ------ | ----------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| POST   | `/v2/lab-reports`                         | Multipart upload; field MUST be `file` (singular), one file/request. `202` returns `upload_id` + `current_status: "processing"` – NO session_id (one upload can fan out to several sessions). |
| GET    | `/v2/lab-reports`                         | List / filter (by `reference_id`, `upload_id`, `report_date_from`/`_to`, `uploaded_at_from`/`_to`). Capped at 500 – use filters.                                                              |
| GET    | `/v2/lab-reports/{session_id}`            | Session: metadata, `upload_id`, status history, layered `results[]`, `panels[]`. Files, artifacts, and delivery state are NOT embedded – use the sub-resources.                               |
| GET    | `/v2/lab-reports/{session_id}/files`      | Input files + thumbnail as presigned URLs, with a response-level `expires_at`.                                                                                                                |
| GET    | `/v2/lab-reports/{session_id}/deliveries` | Per-destination delivery state (`destination_id`, `status`, `attempt_count`, `last_error`).                                                                                                   |
| GET    | `/v2/lab-reports/{session_id}/artifacts`  | Processing artifacts; privileged keys only – standard keys get `404`.                                                                                                                         |
| POST   | `/v2/lab-reports/{session_id}/reprocess`  | Re-run extraction/standardization; async `202`. Emits a NEW event (new `event_id`) with the SAME `session_id`.                                                                                |
| DELETE | `/v2/lab-reports/{session_id}`            | Soft-delete; `204`.                                                                                                                                                                           |

[references/api-reference.md](references/api-reference.md) routes each goal to its endpoint and notes the semantics the spec page treats lightly; read it before implementing any endpoint call. For full request/response/error specs (RFC 7807 shapes, status codes), fetch the live page when building the call: [API Reference](https://docs.tryterra.co/lab-reports/api-reference) (append `.md` for markdown).

## Data Model

A hierarchy: **Session → Results[] + Panels[]**, where each Result is layered.

- **Session** – `session_id` (snowflake string), `upload_id`, optional `reference_id`, `current_status`, `report_type`, report/collection dates and times, `report_locale`, `lab_name`, `patient_sex`, `patient_age_at_collection`, `status_history[]`, `results_count`, `file_count`, `input_bytes`, `output_bytes`, `report_notes`, `results[]`, `panels[]`.
- **Panel** – report-level grouping: `{ id, name, key }`. Results reference it via `biomarker.panel_id`.
- **Result** – four layers, identical between the webhook payload and GET:
  - `source` – what the report literally printed: `name`, `panel`, `value` (raw string), `units`, `flag` (verbatim), `method`, `notes`, `reference_text` (plus `collection_date`/`collection_time` on the webhook copy only – GET carries those on the session).
  - `biomarker` – normalized identity: `key` (**null when unmatched**), `display_name`, `loinc_code`, `panel_id`, `panel_key`, `specimen`.
  - `measurement` – one typed value: `type` names the populated sibling (`numeric`, `bounded` `{operator, value}`, `qualitative` `{text, code}`, `text`, or absent with `absent_reason`), plus `units` and `ucum_code`.
  - `interpretation` – the abnormality layer: `flag` (coded, nullable), `flag_raw`, `source`, `applied_range` `{lower, upper}` (the range the flag was judged against).
- **Reference Range** – `lower`, `upper`, `type` (a range-type label describing the range, not a verdict), and a `context` (`sex`, `age_lower`/`age_upper`, `pregnancy_status`, `cycle_phase`, `gestational_week_lower`/`_upper`, `reference_population`, `modifiers[]`).

Webhook envelope semantics are in [references/webhook-payload.md](references/webhook-payload.md); for field-level types and the enum tables (which are open and grow over time), fetch the live [Core Concepts](https://docs.tryterra.co/lab-reports/core-concepts) page (append `.md` for markdown).

### Key Data Semantics

- **`biomarker.key` is present-but-NULL when unmatched** – it is the sole no-match signal. Never key off `loinc_code` (it can be null even on a match). Fall back to `source.name` / `biomarker.display_name` and keep the result.
- **Branch on `measurement.type` and read the matching field.** Do not probe multiple value fields in priority order – the flat `value` / `value_gt` / `value_lt` / `qualitative_value` fields no longer exist; a bound like `<0.5` arrives as `bounded: { "operator": "lt", "value": 0.5 }`.
- **Two flags, two meanings.** `source.flag` is the raw lab string (`"H"`, `"↑"`, ...); `interpretation.flag` is the coded signal (nullable – null means no signal), with `flag_raw` echoing the verbatim form and `source` naming its provenance.
- **Enums are open.** `current_status`, `report_type`, `measurement.type`, `specimen`, range `type`, `patient_sex` may gain new values without a major version bump. Handle unknowns gracefully (default/unknown category, never throw).
- All enum values are clean lowercase strings (`"sent"`, not `"REPORT_STATUS_SENT"` or `6`). All timestamps are ISO-8601 UTC.

## Gotchas

- **Upload returns `upload_id`, NOT `session_id`.** The `202` body is `{ "upload_id": "...", "current_status": "processing" }`. One upload can fan out to several sessions; learn session IDs from the webhook's `data.session_id` or `GET /v2/lab-reports?upload_id=...`. `upload_id` can be absent on older sessions – treat it as optional.
- **Two webhook events; branch on the envelope `type`.** `lab_report.completed` on success, `lab_report.failed` on terminal failure. Per-destination opt-in still uses the single coarse type `"lab_report"` in `destination_event_types` – both events share it.
- **Dedupe on `event_id`.** Redeliveries of the same stored payload carry the SAME `event_id`; a reprocess is a new event with a NEW `event_id` and the SAME `session_id`. See rules/webhooks-dedupe-event-id.md.
- **Failures carry a structured error.** `data.error` is `{ code, message, retriable }` with codes `file_unreadable`, `extraction_failed`, `standardization_failed`, `internal`. `retriable: true` means the same input may succeed on re-submission; `false` means fix the input first.
- **`interpretation.applied_range` can be null while `reference_ranges` are populated.** It is only set when exactly one range unambiguously applies to the patient; when it is null, filter `reference_ranges` by context yourself (see rules/data-filter-ranges-by-demographics.md).
- **Presigned file URLs live on sub-resources and expire.** `GET .../files` (and privileged `.../artifacts`) return presigned URLs with a response-level `expires_at` (roughly one hour out). They are not embedded in the webhook or the session response. Re-mint by re-fetching the sub-resource; do not persist a URL past its `expires_at`.
- **Artifacts are privileged-only, as a `404`.** Standard keys get `404` from `GET .../artifacts`, not an empty list.
- **Oversize uploads:** a file over 20 MB is normally rejected with `400` ("invalid multipart form or file too large") via the byte-limit reader; a `413` only fires when the multipart part declares a Content-Length over the cap. Expect `400` (sometimes `413`).

## Rules

Read the relevant rule in `rules/` before writing that code. Each is a standalone file with incorrect/correct examples.

### Webhooks & Delivery (HIGH)

- `webhooks-dedupe-event-id` – Key idempotency on `event_id`; redeliveries reuse it, a reprocess mints a new one with the same `session_id`.
- `api-poll-at-most-every-5s` – Webhooks for production (success AND failure events); polling for dev/fallback; poll no faster than every 5 seconds and stop on a terminal status.

### Data Handling & API Usage (HIGH–MEDIUM)

- `data-keep-unmatched-biomarkers` – A null `biomarker.key` is clinically relevant; never discard the result, fall back to `source.name` and flag for review.
- `data-filter-ranges-by-demographics` – Use `interpretation.applied_range` when present; otherwise filter `reference_ranges` by sex/age/context before interpreting; handle `measurement.bounded` conservatively.
- `data-store-ids-as-strings` – Snowflake `session_id`s lose precision as JS numbers; keep them strings end to end.
- `data-parse-utf8` – Data contains `µ`, `×`, `±`, superscripts; always parse as UTF-8.
- `api-space-bulk-uploads` – One file per request, 20 MB cap, 30s–3min each; space bulk uploads and tag with `reference_id`.

## References

Load these for full specs (each is self-contained):

- [references/api-reference.md](references/api-reference.md) – goal-to-endpoint routing plus the semantics the spec page treats lightly. Read before calling any endpoint; fetch the linked live page for full request/response shapes.
- [references/webhook-payload.md](references/webhook-payload.md) – the event envelope (`type`, `event_id`, `occurred_at`, `upload_id`, `data`), the idempotency keys, and the failure event. Read when building a webhook handler.
- [references/biomarkers.md](references/biomarkers.md) – standardization, UCUM mappings, LOINC coverage, and common-biomarker tables by category. Read when working with keys, units, or LOINC codes.

The full biomarker dataset (4,000+ entries, ~700 KB) is not bundled; download it from the [Biomarker Reference](https://docs.tryterra.co/lab-reports/biomarker-reference) page.

## Live Documentation

Append `.md` to any page URL for markdown. If the terra-docs MCP server (`https://docs.tryterra.co/~gitbook/mcp`) is connected, use its tools to search and fetch these pages instead.

- [Overview](https://docs.tryterra.co/lab-reports)
- [Quick Start](https://docs.tryterra.co/lab-reports/quickstart)
- [Core Concepts](https://docs.tryterra.co/lab-reports/core-concepts)
- [API Reference](https://docs.tryterra.co/lab-reports/api-reference)
- [Webhook Payload](https://docs.tryterra.co/lab-reports/webhook-payload)
- [Biomarker Reference](https://docs.tryterra.co/lab-reports/biomarker-reference)
- [Best Practices](https://docs.tryterra.co/lab-reports/best-practices)

---
name: oxygen-dedupe
description: Review duplicate companies, people and source events before ingestion while preserving provenance and holding uncertain identity matches.
---

# Resolve identity before merging

Read [the runtime contract](../../../docs/runtime-contract.md). Establish the record type and destination before choosing a key.

- Companies: verified canonical domain or provider/company LinkedIn identity. Subsidiaries and shared domains require a deliberate rule.
- People: canonical profile URL or stable provider person ID, reconciled with current employer. A name alone is insufficient.
- Signals: provider plus stable event ID; retain separate events for one account.
- Outcomes: event ID plus enrollment/cohort identity, as required by `analyse_results`.

Inspect the current schema and bounded existing identities. Normalise URL scheme, host, trailing slash and query parameters without changing the actual identity path. Retain original values. Missing keys go to a review queue; never collapse all nulls into one record.

Produce `insert / existing / possible_match / invalid` decisions with the matched ID and reason. Repeated signals enrich provenance; they do not create repeated people. Conflicting non-null fields need a field-level resolution rule.

Preview counts and collisions before an authorized upsert. Re-query an ambiguous write result before retrying. For a repeat import, verify it creates no extra identities while still preserving new signals. Do not delete records or merge people solely because names match.

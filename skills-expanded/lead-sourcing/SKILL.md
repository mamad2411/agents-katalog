---
name: lead-sourcing
description: Translate an ICP into comparable account and contact searches, build a bounded first batch and preserve provider filters and provenance.
---

# Build the first account batch

Read `company/private/` when populated; use [the ICP](../../../company/icp.example.md) and [persona](../../../company/persona.example.md) only as labeled examples. Follow [the runtime contract](../../../docs/runtime-contract.md) for OXYGEN discovery.

Write a filter ledger before sourcing:

| Criterion | Business meaning | Provider field/operator | Verified semantics | Post-filter |
|---|---|---|---|---|
| Geography | HQ, operating market or person's location | Discover current schema | Do not equate these | Flag unknowns |
| Size | Actual employees or provider estimate/bucket | Discover current schema | Record measurement basis | Audit boundaries |
| Buyer | Remit plus title variants | Include/exclude titles | Include local-language variants | Persona scoring |
| Exclusions | Customers, active deals, competitors | Exact identity where possible | Separate match from substring suspicion | Hold ambiguity |

Use the user's validated search as an anchor. Mirror its *meaning* across connected providers; unsupported filters become explicit post-filters. Do not assume Apollo, Sales Navigator and Blitz use identical headcounts, taxonomies or title matching.

Start with ten known accounts or a supplied CSV. Preserve source ID, domain, source, signal type, original timestamp and batch ID. Inspect missing keys and parse quoted CSV properly. Reuse `normalise_sources`; use `oxygen-dedupe` for identity conflicts.

For provider calls, discover exact schemas/enums, preview the narrow scope and price, then execute only the requested capped probe. Capture pagination cursors and completion status; partial pages are not the whole TAM. Scope people searches to company-qualified accounts.

Return saved filters, batch size, unique accounts, exclusions, unknowns and source coverage. A source match is a candidate; research and independent company/persona gates decide fit.

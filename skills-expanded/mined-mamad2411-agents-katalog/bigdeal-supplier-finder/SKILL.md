---
name: bigdeal-supplier-finder
description: Use when an agent needs to create an evidence-bound supplier discovery report for a product or sourcing brief, especially for global buyers, cross-border ecommerce, private label, OEM/ODM, manufacturer discovery, B2B platform search, trade show directory search, supplier directory research, query expansion, source map generation, or structured sourcing reports. Produces source maps, supplier candidates, evidence links, gaps, and next-search suggestions. Does not log in, bypass captcha, use paid APIs, scrape at scale, store databases, score supplier trustworthiness, recommend purchases, or perform live/external actions without explicit separate authorization.
---

# BigDeal Supplier Finder

Use this skill to help an agent discover where to search for suppliers and produce a structured, evidence-bound sourcing report. The skill is breadth-first: expand source surfaces, preserve raw signals, separate evidence from query fuel, and make uncertainty explicit.

This is a runtime-agnostic agent skill. It is not a crawler, not a supplier database, not a procurement recommendation engine, and not a trust or due-diligence score.

## Hard Boundary

Do:

- generate diverse search/query plans across B2B platforms, trade shows, associations, government or industry directories, company websites, supplier directories, and public media/community sources;
- record `SearchResultSignal`, `SourceAttempt`, `SourceMapEntry`, `SupplierCandidate`, `QuerySuggestion`, and `Gap` separately;
- Every Supplier Candidate must include at least one evidence link that: (a) is a valid HTTP/HTTPS URL, (b) is not a search engine results page or site-search page, (c) is not a known paywall/login-wall/captcha page, (d) points to a page that contains the supplier information claimed in the candidate fields. Evidence links that fail these criteria must be removed; if no valid evidence link remains, the candidate must not enter Supplier Candidates.
- grade evidence strength only as A/B/C/D;
- mark low-evidence and missing-evidence cases instead of hiding them;
- run the deterministic validator scripts when editing report contracts or examples.

Do not:

- log in, handle cookies, read sessions, solve captcha, bypass access controls, use paid APIs, or access credentialed sources;
- run recursive crawling, bulk scraping, database storage, contact enrichment, or background monitoring;
- label suppliers as trustworthy, safe, recommended, best, verified, compliant, or purchase-ready;
- count search pages, query-only snippets, AI answers without public URLs, failed fetches, restricted pages, paywalls, login walls, captcha pages, or D-grade raw signals as actionable leads;
- claim that deterministic fixture tests prove live supplier discovery quality.

## Inputs

Ask for or infer:

- product name and product category;
- sourcing intent, such as OEM, ODM, wholesale, private label, component sourcing, or market exploration;
- target markets and preferred supplier regions;
- known exclusions or risky sources;
- available runtime capability: `search+fetch`, `search-only`, or `no-search`;
- whether live web/provider/browser/credential actions are explicitly authorized.

If live or credentialed actions are not explicitly authorized, operate in planning or deterministic fixture mode only.

## Runtime Capability Assumptions

This skill assumes the agent runtime has access to:
1. **Web search** — returning result titles, snippets, and target URLs.
2. **Web fetch** — retrieving page content from public HTTP/HTTPS URLs.

If search is unavailable, operate in `no-search` mode (fail-fast with metadata only).
If fetch is unavailable, operate in `search-only` mode (C-grade candidates only).

This skill does NOT assume: paid API access, authenticated sessions, CAPTCHA solving, JavaScript rendering, or database storage.

## Workflow

### Pre-Flight
1. Classify runtime capability: `search+fetch`, `search-only`, or `no-search`.
2. If `no-search`, return fail-fast metadata and empty arrays immediately.

### ROUND_1: Seed
3. Build at least 6 deduplicated query combinations across target regions, product terms, and sourcing intents.
4. Execute initial search across at least 3 source categories.

### ROUND_2: Source Discovery
5. From ROUND_1 results, identify source surfaces (B2B platforms, directories, trade show lists, association pages).
6. Build Source Map entries from URL-backed target pages that aggregate multiple suppliers.

A Source Map entry is a **discovery surface** — a URL-backed page that lists, indexes, or aggregates multiple potential suppliers (e.g., a B2B platform category page, a trade show exhibitor list, a government supplier directory). It is NOT a specific supplier. If the page describes a single supplier with contact/location/product details, it is a Supplier Candidate, not a Source Map entry.

7. Record all search result signals as query fuel; do not treat them as evidence.

### ROUND_3: Candidate Extraction
8. From Source Map entries and admissible search result target URLs, extract Supplier Candidates.

A Supplier Candidate is a **specific supplier entity** with name, region, and product match. It must come from a Source Map entry or directly from a search result target URL. If the same URL serves as both a discovery surface AND describes a specific supplier, classify it as a Supplier Candidate and do NOT duplicate it in Source Map.

9. Each candidate must have: name, region, product_match_summary, at least one evidence link, evidence grade, and provenance fields.
10. D-grade signals must not enter Supplier Candidates.

### ROUND_4: Expansion
11. From gaps and query suggestions, generate expansion queries targeting uncovered regions, source categories, or product terms.
12. Run one base expansion pass unless the profile is `no-search` or a hard limit has already stopped external actions. If Supplier Candidates are fewer than 8 or source categories are fewer than 3, run at most one targeted expansion or record why it is not possible.
13. Deduplicate actionable leads by canonical URL + normalized name.
14. If hard limit hit, stop new external search/fetch actions, continue to ROUND_5 with existing evidence, and record skipped external actions without fabricating results.

### ROUND_5: Curated Report
15. Assemble all report sections per `references/contract.md`.
16. Run deterministic validation (`npm test`, `npm run fixture`).
17. Record acceptance summary with fixture gate verdict.

## Stopping Conditions

Stop new external search/fetch actions only under these conditions:

1. **Round budget exhausted**: All 5 rounds (ROUND_1 through ROUND_5) completed.
2. **Sufficient results after base expansion**: at least 8 Supplier Candidates and at least 3 source categories; this may skip only an additional targeted expansion.
3. **Hard limit hit**: runtime enforces a hard limit such as rate limit, token budget, fetch cap, query cap, or time cap.

Do not skip ROUND_1 through ROUND_3 because of diminishing returns or coverage saturation. When a hard limit fires before all rounds complete, record the stop reason in `execution_metadata.stop_reason`, stop new external actions, continue to ROUND_5 with existing evidence, and mark only blocked external actions as skipped in `stage_records`.

## Evidence Rules

- A: at least two independent public source types cross-confirm the same candidate.
- B: one high-structure public source such as a B2B platform, trade show, association, or government directory.
- C: low-strength but auditable public target URL evidence, such as search-only target URL snippets with minimum fields.
- D: AI summary, no public evidence URL, search page URL, query-only signal, or missing minimum fields. D-grade signals must not enter Supplier Candidates.

Search-only candidates may enter as C-grade only when they are snippet-derived, not fetched, use a non-search-page target URL, and include explicit provenance.

## Fetch Failure Handling

When a fetch attempt fails (status: failed, restricted, missing_fields, rejected):
1. Record the attempt in `source_attempts` with the failure reason.
2. Add a `gap` entry referencing the `source_attempt_id` and describing what was missing.
3. Do NOT create a SourceMapEntry or SupplierCandidate from the failed fetch.
4. If the failure is due to a hard limit (rate limit, fetch cap), mark remaining rounds as skipped.

## Product Coverage Verification

When a fetched page uses collapsible/expandable sections (accordions, "Show more", tabs), the visible content may not represent the full page. For each Supplier Candidate:

1. Note in `field_origin` whether critical fields (name, region, product_match_summary) came from visible or potentially-hidden content.
2. If product listings or supplier details appear to be truncated by UI containers, add a `gap` entry: `{ reason: "collapsible_container_coverage_gap", detail: "..." }`.
3. Downgrade evidence grade to C if critical fields rely on content that may be hidden behind expandable UI.

## Report Contract

Load `references/contract.md` when writing or reviewing report fields, acceptance gates, runtime profiles, or evidence admissibility.

Every report must include:

- Execution Metadata
- Execution Limit Audit
- Acceptance Summary
- Source Map
- Supplier Candidates
- Search Result Signals
- Source Attempts
- Queries Tried
- Query Suggestions
- Gaps
- Next Steps
- Risk Notice

## Deterministic Scripts

Use these scripts from the repository root:

```bash
npm test
npm run check
npm run fixture
```

The fixture CLI lives at:

```bash
node bigdeal-supplier-finder/scripts/bsf-fixture.js bigdeal-supplier-finder/fixtures/sample-suite.json
```

Expected fixture CLI boundary:

- `evidence_scope` is `deterministic-fixture`;
- `live_reports` is empty;
- `cannot_prove` includes real search breadth, supplier discovery quality, and live smoke readiness.

## Acceptance Boundaries

Deterministic fixtures prove only local contract behavior. They do not prove live search breadth, supplier discovery quality, provider readiness, browser/session readiness, account state, credential safety, external site compatibility, or production readiness.

Before any live/provider phase:

- split deterministic and live inputs explicitly;
- keep live reports separate from fixture reports;
- require 10 live reports for live acceptance statistics;
- rerun review for browser/provider/credential/live boundaries.

## Live Report Validation

Deterministic validation (`npm test`, `npm run fixture`) proves local contract
behavior only. The fixture runner intentionally does not validate live reports:
it emits `evidence_scope: "deterministic-fixture"` and keeps `live_reports`
empty.

For live reports:

1. Keep `evidence_scope: "live"` and do not mix live reports with deterministic
   fixtures.
2. Use a separate live smoke suite, not included in this package.
3. Require at least 10 live reports before acceptance statistics are meaningful.
4. Rerun review for provider, browser, credential, session, and external-write
   boundaries before any live smoke.

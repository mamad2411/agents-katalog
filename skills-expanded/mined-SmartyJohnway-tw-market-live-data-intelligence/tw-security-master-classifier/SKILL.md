---
name: tw-security-master-classifier
description: "Identify and verify the current identity, instrument type, market or board, bilingual names, ISIN, CFI, key dates, and available lifecycle events of Taiwan securities from a code, Chinese or English name, ISIN, file, or dataset. Use for TWSE, TPEx, emerging-stock, GISA, public-unlisted, ETF, ETN, fund, warrant, preferred-share, TDR, bond, index, futures/options, gold, NCD, and STO identity questions; for reconciling Taiwanese security-master records; or for determining whether an instrument is a listed common stock. Do not use for prices, investment advice, strategy design, backtesting, or point-in-time universe reconstruction."
---

# Taiwan Security Master Classifier

Resolve what a Taiwan security is now and report the official evidence behind the result. Separate current identity from historical lifecycle and never infer a missing event date from a snapshot transition.

This package is the reusable Taiwan Market Identity Service source Skill. For
governed Taiwan cash-market instruments, the Instrument Primary Identity is
ISIN. `MARKET:CODE` is the current Listing / Routing Identity. A Security
Master `release_id` identifies a release, never a financial instrument.

Identity Knowledge Universe is distinct from Execution Universe. The service
may resolve and describe an instrument whose downstream market-evidence route
must fail closed. Current cash execution eligibility is limited to governed
`common_share` and `etf` records; this Skill does not grant execution authority.

## Operating modes

- **Resolve one security:** Accept a code, Chinese name, English name, or ISIN and return exact or ambiguous candidates.
- **Classify records:** Classify supplied JSON, CSV, HTML, or database exports.
- **Validate a master:** Check bilingual alignment, duplicate ISINs, cross-mode conflicts, unknown CFI values, date quality, and evidence completeness.
- **Validate or model lifecycle evidence:** Parse supplied official captures for listing-market termination, announcements, ETN expiry, maturity, and last-trading events; merge them without overwriting history.
- **Probe sources:** Test official endpoints without treating an access block as an empty dataset.

## Required source model

Use the four-layer authority model in [references/source-contract.md](references/source-contract.md):

1. TWSE ISIN Chinese and English lanes for security-level identity and classification evidence.
2. TWSE OpenAPI for listed issuer and product enrichment.
3. TPEx OpenAPI for OTC, emerging, GISA, warrant, bond, and product enrichment.
4. TWSE/TPEx termination tables, product expiry pages, announcements, and attachments for lifecycle events.

Read [references/source-manifest.json](references/source-manifest.json) before probing or claiming coverage. Treat `verified`, `catalog_verified`, and `discovery_required` as different states.

## Workflow

### 1. Normalize the request

- Preserve the original query.
- Detect exact ISIN, probable security code, or name query.
- For a file, identify its source family and observation date before classification.
- Never interpret a bare numeric value as a security without surrounding Taiwan-market context.

### 2. Acquire evidence

- Prefer supplied raw captures when they are recent enough for the request.
- Otherwise probe official sources with `scripts/probe_sources.py`.
- For TWSE ISIN HTML, try normal HTTPS first; if a real security-block page is returned, use an available public-browser capture or ask for a saved HTML capture.
- Never bypass a WAF, CAPTCHA, or rate limit. Never use TLS verification disablement to treat a security block as success.
- Save URL, source lane, source update date, observed time, payload hash, content type, and acquisition status.

### 3. Parse without losing context

- Parse TWSE ISIN HTML with `scripts/isin_parser.py`.
- Preserve page title, `strMode`, language lane, section heading, raw cells, and remarks.
- Do not flatten away section headings; `strMode=2` and `strMode=4` contain multiple instrument families.
- Preserve raw date strings alongside normalized ISO dates.

### 4. Resolve identity

Use this order:

1. Exact ISIN.
2. Exact security code within market context.
3. Exact normalized Chinese or English name.
4. Alias or former-name evidence from an official lifecycle source.
5. Fuzzy name match only to produce candidates, never an automatic winner.

Join Chinese and English ISIN lanes by ISIN. Do not join by row order. If critical fields disagree, quarantine the record instead of silently preferring one language.

### 5. Classify

Run `scripts/classifier.py` or follow [references/classification-contract.md](references/classification-contract.md).

Use evidence in this order:

1. Official route and `strMode`.
2. Page title and section heading.
3. Market or board field.
4. Controlled CFI mapping.
5. ISIN and remarks.
6. Code and name patterns only as anomaly signals.

Never set `common_share` merely because a code has four digits. Never set ETF, preferred share, TDR, or warrant solely from its code pattern or name suffix.

### 6. Validate or model lifecycle evidence

Follow [references/lifecycle-contract.md](references/lifecycle-contract.md).

- Use the bundled `parse_twse_delisted.py`, `parse_tpex_delisted.py`, `parse_tpex_announcement.py`, and `parse_etn_termination.py` adapters for supplied captures.
- Use `merge_lifecycle_events.py` to deduplicate normalized event evidence.
- Active retrieval still depends on source access and a matching adapter; do not claim automatic enrichment for announcement attachments that require manual interpretation.

- Keep announcement date, last-trading date, maturity date, and termination effective date distinct.
- Normalize ROC and Gregorian dates but preserve `date_raw`.
- Model lifecycle as events, not a single overwritten status.
- Use `unknown` when evidence is missing and `not_applicable` only when the event cannot apply to that instrument.
- Do not infer a delisting date from disappearance from a current ISIN snapshot.

### 7. Validate and report

Run:

```bash
python3 scripts/validate_skill.py
```

For supplied records, also run:

```bash
python3 scripts/classifier.py --input records.json --query QUERY
```

Return the format in [references/output-contract.md](references/output-contract.md), including:

- resolution status and candidate count;
- code, bilingual names, ISIN, CFI;
- asset class, instrument type, equity subtype, market or board;
- current-observation status, not an unsupported trading-status claim;
- lifecycle events and date semantics;
- official URLs and evidence status;
- conflicts, missing fields, caveats, and reason codes.

## Mandatory stop and quarantine conditions

- Source response is a security-block or error page rather than data.
- Critical identity fields contain replacement characters.
- Duplicate ISIN has conflicting code, CFI, or market.
- Chinese and English lanes disagree on ISIN-linked code, CFI, or key date.
- Classification depends only on a code or name pattern.
- Unknown CFI conflicts with the section or route.
- A current snapshot would be represented as historical point-in-time truth.
- An event date would have to be guessed.

## Boundaries

- This skill identifies securities and their supported lifecycle facts.
- It does not provide prices, trading signals, stock selection, or investment advice.
- It does not reconstruct a PIT universe or authorize backtesting.
- It does not write to a production database unless a separate, explicit workflow authorizes that action.
- It may report `listed_common_stock_core_flag`, but that flag is a current classification, not proof of historical backtest eligibility.

## Installation-local release contract

The governed lifecycle is `NOT_INITIALIZED → BUILDING → CANDIDATE → QUALIFIED
→ ACTIVE`, with `REJECTED` and `RETIRED` terminal/local status projections.
Updates are user-triggered: official acquisition creates a candidate,
qualification validates schema, identity, conflicts, lineage and hashes, and
only a qualified release may be atomically activated. Failed updates preserve
the prior Active release; rollback selects another immutable qualified release.
There is no startup acquisition, scheduler, or Candidate B fallback.

Aliases, `current_listing`, `listing_history`, and lifecycle events require
governed evidence. Snapshot absence is not termination, and snapshot time is
not listing `valid_from`. When official evidence establishes old ISIN → new
ISIN, return `IDENTITY_MIGRATION_REVIEW_REQUIRED`; do not rewrite downstream
identity automatically.

`producer_skill_contract_hash` is producer-time provenance. Historical
releases retain the Skill hash used when produced; changing this Skill affects
future producer provenance and does not rewrite or invalidate historical bytes.

## Bundled resources

- [references/source-contract.md](references/source-contract.md): authority, acquisition, and join rules.
- [references/source-manifest.json](references/source-manifest.json): verified official source registry.
- [references/classification-contract.md](references/classification-contract.md): taxonomy and deterministic rules.
- [references/lifecycle-contract.md](references/lifecycle-contract.md): event and date semantics.
- [references/output-contract.md](references/output-contract.md): response and JSON contracts.
- `references/schemas/`: JSON Schemas for normalized records, classification, resolution, batch, lifecycle, manifest, and probe outputs.
- `references/fixtures/`: observed official examples and parser fixtures; never treat them as living market truth.
- `scripts/probe_sources.py`: bounded official-source probe.
- `scripts/isin_parser.py`: TWSE ISIN HTML parser.
- `scripts/classifier.py`: resolver and deterministic classifier.
- `scripts/parse_*` and `scripts/merge_lifecycle_events.py`: supplied lifecycle-capture adapters and event merger.
- `scripts/validate_skill.py`: full offline contract and regression validation.

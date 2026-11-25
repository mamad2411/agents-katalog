---
name: geo-schema
description: >
  Audit JSON-LD structured data on a single URL. Three layers:
  (1) parse + validate every JSON-LD block; (2) check expected types per
  page kind (Article on blog posts, Product on listings, etc.);
  (3) Enhanced Entity Pages — visible-facts coverage (% of declared facts
  also present in body), sameAs deref, agent-instructions block.
  Use when user asks about schema, structured data, JSON-LD, or rich results.
allowed-tools: Bash, Read, WebFetch
---

# geo-schema — Schema.org / JSON-LD audit

Single-page schema validation + Enhanced Entity Pages methodology check.

## Command

```bash
python3 -m scripts.checks.schema <url> [--page-kind <kind>]
```

`--page-kind` is one of: `homepage`, `article`, `service`, `about`, `case-study`,
`product`, `faq`, `generic`. If omitted, the module auto-detects.

## What it checks

### Layer 1 — Validity
- Every `<script type="application/ld+json">` block parses cleanly
- `S0c` finding when JSON-LD is invalid
- `S0` finding when no JSON-LD is present at all
- `S0t` finding when blocks exceed 20k chars (Vertex AI truncation risk)

### Layer 2 — Expected types per page kind
Each page kind expects a baseline set of Schema.org types. Missing ones surface as `S1`:

| Page kind | Expected types |
|---|---|
| `homepage` | Organization, WebSite, BreadcrumbList |
| `article` | Article, Person, BreadcrumbList |
| `product` | Product, BreadcrumbList |
| `about` | AboutPage, Organization, Person |
| `faq` | FAQPage |
| `service` | Service, Organization |
| `case-study` | CreativeWork, Organization |

### Layer 3 — Enhanced Entity Pages (EEP)
- `EE1` — Visible-facts coverage: % of facts declared in JSON-LD that also appear in the page body. Target ≥ 70%.
- `EE2` — `sameAs` deref: HEAD-checks each external link; broken / 404 entries reported.
- `EE3` — `<section class="agent-instructions">` block (emerging pattern, low confidence — **flagged as experimental**).
- `EE4` — `BreadcrumbList` populated with ≥ 2 items.

Reference: `docs/STRUCTURED_DATA_BEST_PRACTICES.md` (WordLift 2025 + Volpini et al. arXiv:2603.10700 methodology).

## Templates

The `schema/` directory holds 7 starter JSON-LD templates (Organization, LocalBusiness, Article, Product, WebSite, Person, BreadcrumbList). Copy / adapt rather than writing from scratch. See `schema/README.md`.

## Output

The script prints a structured report to stdout (Markdown). When called from `run_audit.py`, the findings feed into Annex C of the unified audit.

## Dependencies

- `scripts/checks/schema.py`
- Python: `requests`, `beautifulsoup4`, `lxml`

---
name: apollo-search
description: >
  Build targeted account and contact lists with Apollo's database through the ColdIQ
  marketplace. Use when searching companies or people with Apollo's filter semantics
  (titles, seniority, employee ranges, industries, technologies, intent), enriching people
  or organizations, or building a TAM from Apollo. Triggers on "Apollo search", "Apollo
  filters", "build a TAM", "search companies", "search people", "enrich org", "enrich
  people", "find companies by technology", "employee count range", "intent topics". Do NOT
  use for Lima Data or large-scale ai-ark search (see coldiq-search-enrich), email-finding
  waterfalls (see contact-enrichment), or campaign sending (see instantly-api).
---

# Apollo Search

Search Apollo's 210M+ contacts and 35M+ companies to build targeted lists, then enrich them —
through ColdIQ's resold Apollo endpoints `/v1/apollo/*` (same Apollo filter semantics, one ColdIQ
key). Use Apollo to BUILD the list (search + filter); use
[coldiq-search-enrich](../lima-data-api/SKILL.md) to ENRICH it with emails.

## ColdIQ Marketplace Endpoints

| Task | Method | Path | Credits | Endpoint ID | Notes |
|------|--------|------|---------|-------------|-------|
| Search people | POST | `/v1/apollo/people/search` | 1 | `apollo.people.search` | Titles, seniority, location, company |
| Search organizations | POST | `/v1/apollo/organizations/search` | 1 | `apollo.organizations.search` | Industry, size, location |
| Enrich one person | POST | `/v1/apollo/people/match` | 1 | `apollo.people.match` | Name/email/LinkedIn → full profile |
| Bulk enrich people (≤10) | POST | `/v1/apollo/people/bulk-match` | 1/person | `apollo.people.bulk_match` | 10 per call |
| Enrich one org | POST | `/v1/apollo/organizations/enrich` | 1 | `apollo.organizations.enrich` | Full firmographics by domain |
| Bulk enrich orgs (≤10) | POST | `/v1/apollo/organizations/bulk-enrich` | 1/org | `apollo.organizations.bulk_enrich` | Stripped data — see gotcha |
| Org info by Apollo ID | POST | `/v1/apollo/organizations/info` | 1 | `apollo.organizations.info` | |

## Standard Workflow: Search Then Enrich

1. Search people with filters (returns IDs + basic info, not emails).
   → **POST** `/v1/apollo/people/search` · 1 cr · `apollo.people.search`
   ```json
   { "person_titles": ["VP Sales", "Head of Growth"], "person_seniorities": ["vp", "director"],
     "organization_num_employees_ranges": ["51,200"], "per_page": 100, "page": 1 }
   ```
2. Collect IDs from the results.
3. Bulk enrich in groups of 10 (never one-by-one).
   → **POST** `/v1/apollo/people/bulk-match` · 1/person · `apollo.people.bulk_match`
4. You now have emails, phones, LinkedIn URLs, and employment history.

For full company firmographics use single-org enrich, not bulk:
→ **POST** `/v1/apollo/organizations/enrich` · 1 cr · `apollo.organizations.enrich`

## Top Filters

**Company:** `organization_num_employees_ranges`, revenue range, `q_organization_keyword_tags`
(industry/keywords), `organization_locations`, funding stage, technologies, job postings, year
founded, department headcount, buying intent (Org plan only).

**People:** `person_titles`, `person_seniorities` (`c-suite`, `vp`, `director`), department,
`person_locations`, `include_similar_titles`, recent job change, time in role, has email/phone,
`contact_email_status`.

### Employee count ranges (API values)
```
"1,10"  "11,50"  "51,200"  "201,500"  "501,1000"  "1001,5000"  "5001,10000"  "10001,50000"
```

## Proven Search Configurations (examples)

- **Referral-ceiling founders:** 10–200 emp, $1–10M rev, software/internet, Seed/Series A,
  US/UK/W-Europe, sales dept 0–2 → titles Founder/CEO/Owner.
- **Failed DIY outbound:** 10–100 emp, uses Apollo/Lemlist/Instantly/Outreach/SalesLoft, sales
  dept 1–5 → VP Sales / Head of Growth / Founder.
- **Enterprise B2C:** 501+ emp, $100M+ rev, financial/automotive/retail/insurance/pharma, US →
  CMO / VP Growth / Head of Brand / Head of SEO.

## Filter Building

Start broad (industry + size + location) → check count (target 500–5,000) → add keywords →
add signals (tech/intent/job postings) → add people filters last. Too few (<500)? loosen size.
Too many (>10,000)? add funding stage or department headcount.

## Gotchas

1. **Industry is self-reported** — "Information Technology & Services" is a catch-all.
2. **Revenue is estimated** — unreliable for private companies under $10M.
3. **Technologies = website tracking only** — internal tools (Slack, Notion) won't appear.
4. **Employee count lags** 3–6 months for fast-growing startups.
5. **Bulk org enrich returns stripped data** — missing `latest_funding_stage`, `total_funding`,
   `annual_revenue`, `technology_names[]`. Use single-org enrich for full firmographics.
6. **Search never returns emails** — enrich after search.
7. **Buying intent requires the Organization plan.**

## Apollo vs ai-ark vs Exa

| Need | Best |
|------|------|
| Large-scale company search, 65+ filters | Apollo (`apollo.organizations.search`) |
| Very large people lists, per-result pricing | ai-ark (`ai_ark.people.search`, see coldiq-search-enrich) |
| Niche/new companies not in databases | Exa (`exa.search`) |
| Enrich known contact → email | coldiq-search-enrich waterfall |

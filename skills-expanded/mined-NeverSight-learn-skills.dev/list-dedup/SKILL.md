---
name: list-dedup
description: >
  Deduplicate and clean contact/company lists before enrichment so you never pay ColdIQ credits
  twice for the same record. Use when combining lists from multiple sources, removing duplicate
  contacts or companies, normalizing LinkedIn URLs, applying per-company contact caps, or
  cross-referencing against a TAM. Triggers on "dedup", "deduplicate", "remove duplicates", "clean
  the list", "combine sources", "merge lists", "contact cap per company", "normalize LinkedIn
  URLs". Do NOT use for enrichment/email-finding (see contact-enrichment), search (see
  coldiq-search-enrich), or scoring (see tam-scoring).
---

# List Dedup

A pure data-processing utility: dedup and clean BEFORE any ColdIQ enrichment. This is the single
biggest credit saver — every duplicate you remove is a paid find/enrich call you don't make. See
[resources/credit-optimization.md](resources/credit-optimization.md). This skill makes no API
calls.

## When to dedup

- Before enrichment (never pay to enrich the same person twice)
- After combining multiple sources (Apollo + ai-ark + Meta scrape + Clay)
- After scoring (collapse duplicates, keep the highest-scored row)

## Primary key: LinkedIn URL (normalize first)

```python
import re
def normalize_linkedin(url):
    if not url: return ""
    return re.sub(r'\?.*$', '', url).rstrip('/').lower().replace('https://www.', 'https://')

def dedup_people(rows):
    seen, out = set(), []
    for r in rows:
        key = normalize_linkedin(r.get('linkedin_url', '')) or (r.get('email','').lower())
        if key and key not in seen:
            seen.add(key); out.append(r)
    return out
```

## Secondary key: company name / company LinkedIn URL

Normalize company names (strip Inc/LLC/Ltd suffixes, lowercase) or, better, dedup on the company
LinkedIn URL when present.

## Multi-source combine pattern

1. **Normalize columns** — map each source's columns to one standard schema
   (`full_name, title, linkedin_url, email, company_name, company_domain, company_linkedin, source, score`).
2. **Load** all source CSVs.
3. **Dedup** people by normalized LinkedIn URL (fallback email); companies by company LinkedIn / name.
4. **Sort & export** — Tier 1 first, then by persona, then company name.

## Per-company contact caps

Cap 5–10 contacts per company so you don't blast one account. Rank by title priority
(C-level/VP/Director > Manager > IC), keep the top N per `company_domain`.

## Cross-reference against TAM

Left-join the contact list against the scored TAM on `company_domain` to attach Tier, and drop
contacts at DQ'd companies before enrichment.

## Checklist

- [ ] Normalize LinkedIn URLs before comparing
- [ ] Dedup people by LinkedIn URL (fallback email)
- [ ] Dedup companies by LinkedIn URL / normalized name
- [ ] Map all sources to one schema before combining
- [ ] Keep highest-scored row on duplicate
- [ ] Apply per-company contact cap (5–10)
- [ ] Cross-reference against TAM, drop DQ companies
- [ ] THEN enrich (see [contact-enrichment](../contact-enrichment/SKILL.md))

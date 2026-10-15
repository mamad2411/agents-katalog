---
name: clay-mastery
description: >
  Architect Clay enrichment tables and re-express Clay's waterfalls as ColdIQ marketplace
  calls. Use when designing a Clay table layout, building an email/phone waterfall, ordering
  enrichment providers cheapest-first, writing Clayscript formulas, prompting Claygent, or
  deciding which enrichment to run. Triggers on "Clay table", "Clay waterfall", "enrichment
  table", "Claygent prompt", "Clay formula", "column order", "conditional run", "provider
  order", "Clay credits". Do NOT use for the email-finding waterfall details alone (see
  contact-enrichment), search/prospecting (see coldiq-search-enrich), or scoring (see tam-scoring).
---

# Clay Mastery

Clay stays your orchestration canvas; this skill re-expresses a standard enrichment table and its
waterfalls as **ColdIQ marketplace endpoint calls**, so the same recipe runs with one ColdIQ key
whether you build it in Clay or call the API directly. Clay-specific UI steps (run conditions,
formula writer, Claygent) are kept as guidance.

## ColdIQ Marketplace Endpoints

| Task | Method | Path | Credits | Endpoint ID | Notes |
|------|--------|------|---------|-------------|-------|
| Company enrichment | POST | `/v1/limadata/enrich/company` | 1 | `limadata.enrich.company` | Industry, headcount, revenue, funding, tech |
| Email — Prospeo (step 1) | POST | `/v1/prospeo/enrich-person` | unknown | `prospeo.enrich_person` | First in waterfall |
| Email — work (step 2) | POST | `/v1/limadata/find/work-email` | 1 | `limadata.find.work_email` | Name + domain |
| Email — Findymail (step 3) | POST | `/v1/findymail/search/business-profile` | 1 | `findymail.search.business_profile` | LinkedIn URL |
| Email — FullEnrich (step 4) | POST | `/v1/fullenrich/contact/enrich/bulk` | per result | `fullenrich.contact.enrich_bulk` | Nuclear, async |
| Email verification | POST | `/v1/findymail/verify` | 1 | `findymail.verify` | Replaces Debounce |
| Contact discovery (employees) | POST | `/v1/limadata/prospect/employees` | 25 | `limadata.prospect.employees` | Find people at a company |
| Tech stack | POST | `/v1/builtwith/domain` | flat | `builtwith.domain` | For tech-stack columns |
| News / signal | POST | `/v1/serper/news` | unknown | `serper.news` | Cheap news lookups |

## Standard Table Layout (9 phases, left → right)

1. **Input** — Company Name, Domain, LinkedIn URL
2. **Company Enrichment** — Industry, Employee Count, Revenue, Funding, Tech Stack
   → **POST** `/v1/limadata/enrich/company` · 1 cr · `limadata.enrich.company`
3. **Signal Detection** — Hiring, News, LinkedIn Ads, Growth (see [signal-detection](../signal-detection/SKILL.md))
4. **Contact Discovery** — Full Name, Title, LinkedIn URL
   → **POST** `/v1/limadata/prospect/employees` · 25 cr · `limadata.prospect.employees`
5. **Email Waterfall** — see below
6. **Email Verification**
   → **POST** `/v1/findymail/verify` · 1 cr · `findymail.verify`
7. **AI Qualification** — AI Company Tier, AI Contact Tier, AI ICP Score (Claygent)
8. **AI Personalization** — AI Custom Signal, AI Opening Line, AI Value Prop (Claygent)
9. **Output** — Final Email, Sequence Tag, Campaign Assignment

Naming: prefix sources (`LI - Employee Count`, `Apollo - Revenue`), prefix AI columns
(`AI - Opening Line`), Title Case, column order = execution order.

## Email Waterfall (cheapest-first, "only run when previous is empty")

1. → **POST** `/v1/prospeo/enrich-person` · ? cr · `prospeo.enrich_person` (unverified) — always first
2. → **POST** `/v1/limadata/find/work-email` · 1 cr · `limadata.find.work_email` — only if step 1 empty
3. → **POST** `/v1/findymail/search/business-profile` · 1 cr · `findymail.search.business_profile` — only if above empty
4. → **POST** `/v1/fullenrich/contact/enrich/bulk` · per result · `fullenrich.contact.enrich_bulk` — nuclear, async
5. → **POST** `/v1/findymail/verify` · 1 cr · `findymail.verify` — on ALL found emails

In Clay, set each column's run condition to "Only run when `[Previous Email Column] is empty`".
Final-email formula (pick first non-empty):
```javascript
{{Prospeo - Work Email}} || {{ColdIQ - Work Email}} || {{Findymail - Work Email}} || {{FullEnrich - Work Email}} || ""
```

## Copy-paste Clayscript formulas

```javascript
// First name cleaning
{{First Name}}?.replace(/[^a-zA-Z- ]/g, "").trim().split(' ').map(w => w.charAt(0).toUpperCase()+w.slice(1).toLowerCase()).join(' ').replace(/\s.*/,'')

// Domain from URL
{{Website}}?.replace(/^https?:\/\/(www\.)?/, '').replace(/\/.*/, '').toLowerCase()

// Title seniority check
/^(C[A-Z]O|Chief|VP|Vice President|Director|Head of|SVP|EVP|President|Founder|Co-Founder|Partner|Owner|Managing Director)/i.test({{Title}} || '')

// Employee count bucket
(n => n <= 10 ? '1-10' : n <= 50 ? '11-50' : n <= 200 ? '51-200' : n <= 500 ? '201-500' : n <= 1000 ? '501-1000' : '1000+')({{Employee Count}} || 0)
```

## Claygent prompts that work

- **Company tier:** "Assign Tier 1/2/3 … Return ONLY 'Tier 1/2/3' + one-sentence reason."
- **Opening line:** "Write a cold email opening (1 sentence, <20 words). Reference {{Signal}}.
  Sound human. Don't pitch. Don't start with 'I noticed'. Make it about THEM."

Default Claygent to GPT-4o-mini; escalate only when it fails.

## Best practices & debugging

Pre-filter before enrichment; cheapest tool first; test 50–100 rows; cache; column order =
execution order. When enrichments fail, check: input populated? input format (LinkedIn full
path, domain no protocol)? API key active? run condition correct? provider has data → move to
next in waterfall. See [resources/credit-optimization.md](resources/credit-optimization.md).

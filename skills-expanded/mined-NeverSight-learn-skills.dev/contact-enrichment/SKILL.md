---
name: contact-enrichment
description: >
  Enrich contacts with LinkedIn URLs, verified work/personal emails, and phone numbers through
  the ColdIQ marketplace, layering providers cheapest-first. Use when finding emails for a list,
  building an email waterfall, verifying deliverability, finding phone numbers, resolving company
  LinkedIn URLs from domains, or enriching contacts before a campaign. Triggers on "enrich
  contacts", "find emails", "email waterfall", "verify emails", "bounce check", "find phone
  numbers", "company LinkedIn URL", "enrich before campaign", "deliverability". Do NOT use for
  prospecting/search to BUILD a list (see coldiq-search-enrich / apollo-search), Clay-specific UI
  setup (see clay-mastery), or list dedup (see list-dedup).
---

# Contact Enrichment

Find LinkedIn URLs, work/personal emails, and phones for a list of contacts — layering ColdIQ
endpoints cheapest-first and skipping anyone already enriched. The classic multi-provider email
waterfall (Prospeo → Findymail → FullEnrich, then verify) runs entirely through ColdIQ marketplace
endpoints, so you get one key and unified credits instead of juggling provider accounts.

## ColdIQ Marketplace Endpoints

| Task | Method | Path | Credits | Endpoint ID | Notes |
|------|--------|------|---------|-------------|-------|
| Company LinkedIn URL from domain | POST | `/v1/limadata/find/company-linkedin` | 1 | `limadata.find.company_linkedin` | Replaces Linkup `/enrich/linkedin` |
| Work email (name + domain) | POST | `/v1/limadata/find/work-email` | 1 | `limadata.find.work_email` | Free if not found |
| Work email (LinkedIn URL) | POST | `/v1/limadata/find/work-email-linkedin` | 3 | `limadata.find.work_email_linkedin` | Fallback |
| Personal email | POST | `/v1/limadata/find/personal-email` | 5 | `limadata.find.personal_email` | Last resort |
| Phone number | POST | `/v1/limadata/find/phone` | 10 | `limadata.find.phone` | Free if not found |
| Verify email (bounce check) | POST | `/v1/findymail/verify` | 1 | `findymail.verify` | Replaces Debounce |
| Email via Prospeo (waterfall step) | POST | `/v1/prospeo/enrich-person` | unknown | `prospeo.enrich_person` | First in waterfall |
| Email via Findymail (LinkedIn) | POST | `/v1/findymail/search/business-profile` | 1 | `findymail.search.business_profile` | Waterfall step |
| Email via FullEnrich (bulk) | POST | `/v1/fullenrich/contact/enrich/bulk` | per result | `fullenrich.contact.enrich_bulk` | Nuclear option, async |
| Enrich person (profile) | POST | `/v1/limadata/enrich/person` | 1–5 | `limadata.enrich.person` | Full profile |

## Layer 1 — Company LinkedIn URLs

Given company domains, resolve their LinkedIn company pages first (downstream steps need them).
→ **POST** `/v1/limadata/find/company-linkedin` · 1 cr · `limadata.find.company_linkedin`

## Layer 2 — Email Waterfall (cheapest-first, stop on hit)

1. Try name + company domain.
   → **POST** `/v1/limadata/find/work-email` · 1 cr · `limadata.find.work_email`
2. If empty / domain missing, fall back to the LinkedIn URL.
   → **POST** `/v1/limadata/find/work-email-linkedin` · 3 cr · `limadata.find.work_email_linkedin`
3. Second-opinion provider on the same LinkedIn URL.
   → **POST** `/v1/findymail/search/business-profile` · 1 cr · `findymail.search.business_profile`
4. Provider-level enrichment as a fallback.
   → **POST** `/v1/prospeo/enrich-person` · ? cr · `prospeo.enrich_person` (unverified)
5. Nuclear option for whatever's still missing (bulk, async — see
   [resources/async-job-pattern.md](resources/async-job-pattern.md)).
   → **POST** `/v1/fullenrich/contact/enrich/bulk` · per result · `fullenrich.contact.enrich_bulk`
6. Personal email only if a work email is truly unreachable.
   → **POST** `/v1/limadata/find/personal-email` · 5 cr · `limadata.find.personal_email`

Typical cumulative hit rate: 85–95% depending on contact quality.

## Layer 3 — Verify before sending

Unverified emails destroy sender reputation. Verify every found address.
→ **POST** `/v1/findymail/verify` · 1 cr · `findymail.verify`

| Status | Action |
|--------|--------|
| Valid / Deliverable | Safe to send |
| Risky / Accept-all | Send with caution (catch-all domain) |
| Invalid / Undeliverable | Do NOT send |
| Unknown | Retry with another provider |

## Phone numbers

→ **POST** `/v1/limadata/find/phone` · 10 cr · `limadata.find.phone` (free if not found; LinkedIn URL or name+company)

## Cost optimization

See [resources/credit-optimization.md](resources/credit-optimization.md). Key rules:
dedup first ([list-dedup](../list-dedup/SKILL.md)), cheapest input first, stop on first hit,
test on 50–100 rows before the full list, export only valid/risky emails to the campaign.

## Checklist

- [ ] Dedup contacts before any enrichment
- [ ] Resolve company LinkedIn URLs (Layer 1)
- [ ] Run the email waterfall cheapest-first, stop on hit (Layer 2)
- [ ] Verify all found emails (Layer 3)
- [ ] Test on 50–100 rows first; if hit rate <50%, check data quality
- [ ] Export only verified/risky emails to the campaign (never invalid)

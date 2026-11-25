---
name: oxygen-enrichment
description: Fill company and contact data in OXYGEN Tables with native waterfalls: company profiles, work email, phone, LinkedIn URLs and verification, with free previews, provider preflight, one-row pilots and capped runs. Includes how ContactOut fits the waterfall.
---

# Enrich what survives

Read [the runtime contract](../../../docs/runtime-contract.md). Start from the data you need, not a provider. `oxygen enrichment catalog --json` lists every data type a table can fill, the inputs it needs, coverage and the expected and worst-case credits per row. A `no_default` or `coming_soon` entry is an honest refusal; report it.

## Pick the path

| Data | Start with |
|---|---|
| Company profile, funding, revenue, open roles, tech stack | `columns add <table> --preset company_enrich` (or `company_funding`, `company_revenue`, `company_hiring`, `company_tech_stack`) |
| Person profile from a LinkedIn URL | `--preset person_enrich --input url=<column>` |
| Work email | `enrich-column preview <table> --capability work_email` |
| Mobile phone | `enrich-column preview <table> --capability mobile_phone` |
| LinkedIn URL from name plus company | `--capability linkedin_url` |
| Grade emails you already have | `--capability verify_email` (one verifier per column) |

## Run loop

1. Preview for free and read `provider_preflight`, lane availability and `recommended_max_credits`.
2. Pilot one row after approval; read the value and its receipt.
3. Run the approved scope with `--approved --max-credits <recommended_max_credits>`, then read which lanes paid.

## ContactOut in the waterfall

- **Free checks first.** `contactout.people_count` sizes a buyer pool by domain, title and role tenure for 0 credits. `contactout.work_email_status`, `personal_email_status` and `phone_status` tell you, for free, whether ContactOut holds that data for a LinkedIn profile before you pay.
- **Email.** In the default order, Blitz first and ContactOut on a miss (16.5 credits, billed only on a hit): `--provider-order blitzapi,contactout`.
- **Phone.** For Tier A only, after qualification: `--capability mobile_phone --provider-order contactout`, after a free `phone_status` probe.
- **Job changes.** `contactout.email_profile_enrich` turns an old work email into the person's current profile, so a past champion's move shows up (16.5 credits).
- **Search.** `contactout.people_search` returns profiles at 16.5 credits each; use it as the fallback where a cheaper search found nobody.

## Gates

- Enrich only what survives fit and dedupe; never pay twice for a duplicate. A miss is an answer: never rerun it on the same provider.
- Phone, personal email and reveals need their own explicit yes.
- A found value is not permission to use it: emailing, calling or a CRM write is its own approval. An unconfirmed catch-all stays unconfirmed.

Worked use, with costs: [the AP automation worked example](../../../examples/ap-automation-signal-engine/README.md).

---
name: ad-audiences
description: >
  Build matched ad audiences (LinkedIn/Meta/Google) and ABM target lists from your prospect data,
  and use ad engagement as outbound triggers — through the ColdIQ marketplace. Use when turning a
  target list into a hashed-email matched audience for ads, building ABM company/contact lists,
  setting up exclusions, coordinating ads with outbound (ad engagement → sales trigger), or
  resolving identities for ad targeting. Triggers on "ad audience", "matched audience", "hashed
  email", "LinkedIn audience", "ABM list", "retargeting", "exclusion list", "ads + outbound",
  "ad engagement trigger", "multi-channel ABM", "company list for ads". Do NOT use for ad creative,
  bidding, or campaign-manager setup (platform-specific, no ColdIQ endpoint), or for email-sending
  campaigns (see instantly-api).
---

# Ad Audiences & ABM Lists

Turn your prospect data into matched ad audiences and coordinate ads with outbound. ColdIQ supplies
the **hashed emails** ad platforms need for matched/custom audiences and resolves identities for
targeting; the platform setup (LinkedIn/Meta/Google Ads Manager) stays in those tools.

## ColdIQ Marketplace Endpoints

| Task | Method | Path | Credits | Endpoint ID | Notes |
|------|--------|------|---------|-------------|-------|
| Hashed email for ad targeting | POST | `/v1/limadata/find/hashed-email` | 1 | `limadata.find.hashed_email` | SHA-256 emails for matched audiences |
| Resolve identity (social URLs) | POST | `/v1/limadata/find/identity-resolution` | 2 | `limadata.find.identity_resolution` | name+company/email → LinkedIn etc. |
| Reverse-email → profile | POST | `/v1/limadata/find/reverse-email-lookup` | 5 | `limadata.find.reverse_email_lookup` | Enrich an engaged email |
| Find work email (to hash) | POST | `/v1/limadata/find/work-email` | 1 | `limadata.find.work_email` | Get the email first if missing |
| Enrich engaged account | POST | `/v1/limadata/enrich/company` | 1 | `limadata.enrich.company` | Firmographics for an engaging account |
| Build the target company list | POST | `/v1/ai-ark/companies` | per result | `ai_ark.companies.search` | Source the ABM list |

## Build a matched audience (for ads)

Ad platforms match custom audiences on **hashed emails**. From a target list:

1. If you only have name+company, find the email first.
   → **POST** `/v1/limadata/find/work-email` · 1 cr · `limadata.find.work_email`
2. Produce the SHA-256 hashed email the ad platform expects.
   → **POST** `/v1/limadata/find/hashed-email` · 1 cr · `limadata.find.hashed_email`
3. Upload the hashes to LinkedIn/Meta/Google as a matched/custom audience (in the ad platform).

> Company lists match at **95–100%** on LinkedIn vs **30–70%** for contact lists — prefer company
> lists for ABM reach, and use hashed-email audiences for precise person-level retargeting.

## ABM target list + exclusions

1. Source the target companies, then tier them (see [tam-scoring](../tam-scoring/SKILL.md)).
   → **POST** `/v1/ai-ark/companies` · per result · `ai_ark.companies.search`
2. Always build exclusions: competitors, existing customers, wrong seniority, login-page visitors.
3. Separate personas into their own campaigns; for 500+ employee accounts exclude managers.
4. Audience Expansion OFF by default; impression cap ~500/company/7 days.

## Ads + outbound sync (engagement as triggers)

Use ad engagement to time outbound:

| Signal | Action | Timing |
|--------|--------|--------|
| Ad click from a target account | Personalized email | within 24h |
| 50%+ video view | Add to warm sequence | within 48h |
| High impression frequency | Call referencing the content | within 1 week |
| Lead-form open (not submitted) | Retarget + sales follow-up | within 24h |
| Pricing-page visit from ad | Priority outbound with offer | immediate |

When you only have an engaging email or account, enrich it before reaching out:
→ **POST** `/v1/limadata/find/reverse-email-lookup` · 5 cr · `limadata.find.reverse_email_lookup`
→ **POST** `/v1/limadata/find/identity-resolution` · 2 cr · `limadata.find.identity_resolution`

Coordinated ABM cadence: Wk1–2 awareness ads → Wk3–4 retarget engaged + personalized email →
Wk5–6 case-study ads + calls referencing content → Wk7–8 CTA ads + demo offer.

## Notes

- ColdIQ provides the audience **data** (hashed emails, identities, firmographics); creating the
  audience and running ads happens in the ad platform.
- Hash on the find endpoint, not client-side, so the hashing matches what the platform expects.

---
name: instantly-api
description: >
  Create and run cold email campaigns in Instantly through the ColdIQ marketplace — campaigns,
  leads, sequences, analytics, and accounts. Use when creating a campaign, loading/adding leads,
  setting ColdIQ default campaign settings, pulling reply/open/bounce analytics, activating or
  pausing a campaign, or formatting email HTML for Instantly. Triggers on "Instantly campaign",
  "load leads", "create campaign", "campaign analytics", "activate campaign", "add leads to
  Instantly", "reply rate", "campaign settings". Do NOT use for writing the copy itself (see
  cold-email-copy / crawford-method), email-finding/enrichment (see contact-enrichment),
  Lemlist or EmailBison sending (see those skills).
---

# Instantly API

Create campaigns, load leads, and pull analytics in Instantly via ColdIQ's resold Instantly
endpoints `/v1/instantly/*` (Instantly v2 paths preserved, one ColdIQ key; BYOK — connect your own
Instantly account, free, no ColdIQ credits).

## ColdIQ Marketplace Endpoints

| Task | Method | Path | Credits | Endpoint ID | Notes |
|------|--------|------|---------|-------------|-------|
| Create campaign | POST | `/v1/instantly/campaigns` | free | `instantly.campaigns.create` | Use ColdIQ defaults |
| List campaigns | GET | `/v1/instantly/campaigns` | free | `instantly.campaigns.list` | filter by status |
| Get campaign | GET | `/v1/instantly/campaigns/{id}` | free | `instantly.campaigns.get` | verify sequences |
| Update campaign | PATCH | `/v1/instantly/campaigns/{id}` | free | `instantly.campaigns.patch` | partial |
| Activate campaign | POST | `/v1/instantly/campaigns/{id}/activate` | free | `instantly.campaigns.activate` | empty body `{}`; confirm with user |
| Pause campaign | POST | `/v1/instantly/campaigns/{id}/pause` | free | `instantly.campaigns.pause` | empty body `{}` |
| Add single lead | POST | `/v1/instantly/leads` | free | `instantly.leads.create` | use `campaign`, not `campaign_id` |
| Bulk add leads | POST | `/v1/instantly/leads/add` | free | `instantly.leads.add` | |
| List leads | POST | `/v1/instantly/leads/list` | free | `instantly.leads.list` | GET /leads 404s |
| Campaign analytics | GET | `/v1/instantly/campaigns/analytics` | free | `instantly.campaigns.analytics` | reply/open/bounce |
| Daily analytics | GET | `/v1/instantly/campaigns/analytics/daily` | free | `instantly.campaigns.analytics.daily` | per-day |
| Verify email | POST | `/v1/instantly/email-verification` | free | `instantly.email_verification.create` | |

## Recommended Campaign Settings

Deliverability-first baseline for every new campaign:

```json
{
  "email_gap": 15, "random_wait_max": 7, "text_only": true, "first_email_text_only": true,
  "daily_limit": 9999, "stop_on_reply": true, "match_lead_esp": true,
  "link_tracking": false, "open_tracking": false,
  "campaign_schedule": { "schedules": [{ "name": "Weekday schedule",
    "timing": { "from": "08:00", "to": "14:00" },
    "days": { "1": true, "2": true, "3": true, "4": true, "5": false },
    "timezone": "America/Detroit" }] }
}
```

`text_only`, no link/open tracking, and ESP matching all maximize deliverability.

## Gotchas (read first)

1. **Timezone:** use `America/Detroit`, NOT `America/New_York` (Instantly rejects New_York).
2. **Schedule days:** zero-indexed from Sunday (`0`=Sun … `6`=Sat).
3. **Activate/Pause:** send an empty JSON body `{}`.
4. **Delete lead:** send NO body and NO Content-Type header.
5. **List leads:** use `POST /v1/instantly/leads/list` (GET returns 404).
6. **Lead field name:** use `campaign` (UUID), NOT `campaign_id` — the wrong key silently adds
   leads to the org pool without linking them to the campaign.
7. **HTML escaping:** `>` in the body must be `&gt;` (e.g. "Predictable &gt; random").
8. **Lead dedup:** leads dedup across campaigns by default; set `skip_if_in_campaign: false` to force-add.

## HTML email formatting

Even with `text_only: true`, Instantly stores HTML `<div>`s. Every line in its own `<div>`;
blank lines `<div><br /></div>`; no `<p>`; HTML-encode `>`/`<`; signature `<div>{{accountSignature}}</div>`.

```python
import html
def to_instantly_html(plain):
    return ''.join('<div><br /></div>' if not l.strip() else f'<div>{html.escape(l.strip())}</div>'
                   for l in plain.strip().split('\n'))
```

## Variables

Core (auto from lead): `{{firstName}}`, `{{lastName}}`, `{{companyName}}`, `{{email}}`,
`{{website}}`, `{{personalization}}`, `{{accountSignature}}`. Custom: any key in the lead
`payload` becomes `{{key}}` (e.g. `{{Idea1}}`, `{{Idea2}}`, `{{Idea3}}`, `{{SL}}`).
Spintax: `{{RANDOM|Hey|Hi|Hello}} {{firstName}},`.

## Workflows

**Full campaign launch**
1. Create the campaign with ColdIQ defaults + sequences.
   → **POST** `/v1/instantly/campaigns` · free · `instantly.campaigns.create`
2. Add leads with payload variables (loop or bulk).
   → **POST** `/v1/instantly/leads` · free · `instantly.leads.create`
   ```json
   { "campaign": "campaign-uuid", "email": "p@acme.com", "first_name": "John",
     "company_name": "Acme", "payload": { "Idea1": "...", "Idea2": "...", "Idea3": "..." } }
   ```
3. Verify the sequences look right.
   → **GET** `/v1/instantly/campaigns/{id}` · free · `instantly.campaigns.get`
4. Connect sending accounts (Instantly UI), then activate — **always confirm with the user first.**
   → **POST** `/v1/instantly/campaigns/{id}/activate` · free · `instantly.campaigns.activate`

**Performance check**
1. Aggregate stats.
   → **GET** `/v1/instantly/campaigns/analytics` · free · `instantly.campaigns.analytics`
2. Daily trend.
   → **GET** `/v1/instantly/campaigns/analytics/daily` · free · `instantly.campaigns.analytics.daily`

## Benchmarks

| Metric | Kill | Keep | Scale |
|--------|------|------|-------|
| Positive reply rate | <1% | 2–5% | >5% |
| Emails per positive reply | >5,000 | 1,000–3,000 | <1,000 |
| Meeting book rate | <0.5% | 1–2% | >2% |

A reliable top performer: 3 AI-generated campaign ideas (`{{Idea1}}/{{Idea2}}/{{Idea3}}`) as the
personalization payload. After 200+ sends/variant: kill <1% reply, branch top 2–3 winners
(70/20/10 winners/iterations/experiments).

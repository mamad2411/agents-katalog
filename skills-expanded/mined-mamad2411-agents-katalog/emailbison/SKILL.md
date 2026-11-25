---
name: emailbison
description: >
  Migrate an EmailBison sending workflow onto the ColdIQ marketplace. ColdIQ does NOT resell
  EmailBison, so this skill routes campaign/lead/sequence/reply actions to ColdIQ's resold
  Instantly (or Lemlist) endpoints and flags where semantics differ. Use when porting an EmailBison
  campaign to the ColdIQ marketplace, loading leads, creating a campaign, or pulling reply
  analytics for a former EmailBison setup. Triggers on "EmailBison", "migrate EmailBison", "load
  campaign into EmailBison", "send via EmailBison", "campaign analytics". Do NOT use for native
  Instantly work (use instantly-api), Lemlist-first work, copywriting (see cold-email-copy), or
  enrichment (see contact-enrichment).
---

# EmailBison → ColdIQ (Instantly/Lemlist)

> Note (important): ColdIQ does **not** resell EmailBison. There is no `/v1/emailbison/*` group.
> This skill maps every EmailBison campaign action to the closest ColdIQ-resold sender —
> **Instantly** by default (or **Lemlist**). Semantics differ: EmailBison merge tags are
> `{FIRST_NAME}` (caps, single brace) vs Instantly `{{firstName}}`; schedule/sequence field names
> differ. Re-map fields when migrating.

## ColdIQ Marketplace Endpoints (Instantly substitution)

| EmailBison task | Method | Path | Credits | Endpoint ID | Notes |
|-----------------|--------|------|---------|-------------|-------|
| Create campaign | POST | `/v1/instantly/campaigns` | free | `instantly.campaigns.create` | was `POST /api/campaigns` |
| Update settings | PATCH | `/v1/instantly/campaigns/{id}` | free | `instantly.campaigns.patch` | was `/update` |
| Add leads (single) | POST | `/v1/instantly/leads` | free | `instantly.leads.create` | use `campaign`, not `campaign_id` |
| Add leads (bulk) | POST | `/v1/instantly/leads/add` | free | `instantly.leads.add` | was `/bulk/csv` |
| Campaign stats | GET | `/v1/instantly/campaigns/analytics` | free | `instantly.campaigns.analytics` | was `POST /stats` |
| Daily chart stats | GET | `/v1/instantly/campaigns/analytics/daily` | free | `instantly.campaigns.analytics.daily` | was `/line-area-chart-stats` |
| Pause campaign | POST | `/v1/instantly/campaigns/{id}/pause` | free | `instantly.campaigns.pause` | was `/pause` |
| Activate campaign | POST | `/v1/instantly/campaigns/{id}/activate` | free | `instantly.campaigns.activate` | was `/resume` |

Lemlist is the alternative substitution when a client runs Lemlist: `lemlist.campaigns.create`,
`lemlist.campaigns.leads.create`, `lemlist.campaigns.start`, `lemlist.campaigns.stats`.

## Migration mapping (EmailBison → Instantly)

| EmailBison concept | Instantly equivalent |
|--------------------|----------------------|
| `{FIRST_NAME}` merge tag | `{{firstName}}` |
| `{COMPANY}` | `{{companyName}}` |
| `POST /api/campaigns` (name) | `POST /v1/instantly/campaigns` (name + settings) |
| `POST /api/campaigns/{id}/schedule` | `campaign_schedule` inside campaign create/patch |
| `POST /api/campaigns/{id}/sequence-steps` | `sequences[].steps[]` inside campaign create |
| `POST /api/leads/bulk/csv` | `POST /v1/instantly/leads/add` (JSON, not CSV) |
| `GET /api/campaigns/{id}/replies` | use the master-inbox / lead reply views (see resources/analytics.md) |
| `max_emails_per_day: 700`, `plain_text: true`, `open_tracking: false` | ColdIQ Instantly defaults (see instantly-api) |

## Create a campaign (substituted)

1. Create with ColdIQ defaults + sequences (re-map merge tags first).
   → **POST** `/v1/instantly/campaigns` · free · `instantly.campaigns.create`
2. Load leads (JSON, not CSV upload).
   → **POST** `/v1/instantly/leads/add` · free · `instantly.leads.add`
3. Pull stats.
   → **GET** `/v1/instantly/campaigns/analytics` · free · `instantly.campaigns.analytics`

For reply handling, sentiment marking, and the analytics field reference, see
[resources/analytics.md](resources/analytics.md).

## Caveats

- **No 1:1 reply endpoint parity.** EmailBison's per-reply sentiment marking
  (`mark-as-interested` / `mark-as-automated`) maps to Instantly's lead interest-status update
  (`POST /v1/instantly/leads/update-interest-status`), not a per-reply call.
- **Schedules/sequences are nested** in Instantly's campaign object, not separate endpoints.
- Confirm the actual target sender before migrating — some teams move to Lemlist instead of Instantly.

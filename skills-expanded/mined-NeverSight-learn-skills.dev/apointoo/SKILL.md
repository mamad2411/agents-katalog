---
name: apointoo
description: Integrate Apointoo booking/lead capture and conversion tracking into any web project. Use when adding an Apointoo lead form, calling the Apointoo intake API, or wiring GTM conversion tracking for an Apointoo tenant. Language-agnostic (HTTP) with a GTM/dataLayer recipe.
---

# Apointoo integration

> **Skill v1.0.1** · verified against the live Apointoo API on **2026-06-26**. See [`CHANGELOG.md`](../../CHANGELOG.md). A **major** bump = a breaking change to the integration contract below.

Apointoo turns booking/lead forms into clean Google Ads / Meta conversions. This skill shows how to
connect any project to your Apointoo tenant.

**You need:** an Apointoo account with a tenant. Get your **tenant slug** and **publishable key**
from your Apointoo dashboard, and add your site's origin to the tenant's allowed origins.

## 1. Send leads to the intake API (any language)

```
POST  https://dash.apointoo.com/api/intake/<your-slug>/contact
Header: X-Apointoo-Tenant-Key: <your publishable key>
Content-Type: application/json
```
Body:
```json
{
  "lead": { "email": "...", "phone": "...", "name": "...", "message": "..." },
  "attribution": { "gclid": "...", "utm_source": "...", "utm_medium": "...", "utm_campaign": "..." },
  "marketingConsent": true
}
```
- Provide **at least one of `lead.email` or `lead.phone`** (otherwise the API returns `422`).
- Success → `201 { "submissionId": "...", "kind": "contact" }`.
- Intake is **origin-gated**: the request `Origin` must be in your tenant's allowed origins, or call it
  **server-side** (keep the key off the browser) by proxying through your own backend route.

## 2. Environment (recommended names)

| Var | Purpose |
|---|---|
| `APOINTOO_DASHBOARD_URL` | API base (default `https://dash.apointoo.com`) |
| `APOINTOO_TENANT_SLUG` | your tenant slug |
| `APOINTOO_TENANT_KEY` | publishable key — **server-side** (recommended) |
| `NEXT_PUBLIC_APOINTOO_TENANT_KEY` | the key for pure client-side calls (it's origin-gated) |
| `NEXT_PUBLIC_GTM_ID` | your GTM container id |

Never hardcode these in component code — read them from env.

## 3. Fire the conversion via GTM (not direct gtag/fbq)

On a successful `201`, read the body and push to the dataLayer so GTM can fire your ad tags:

```js
const { submissionId } = await res.json()
window.dataLayer = window.dataLayer || []
window.dataLayer.push({
  event: 'generate_lead',
  form_id: 'your_form',
  event_id: crypto.randomUUID(),   // GA4/Ads dedupe id
  transaction_id: submissionId,    // ties the hit to the server record for offline dedupe
  value: 1,
  currency: 'EUR',
  gclid, fbclid,                   // from your captured attribution
})
```
Then in **GTM**: a Custom Event trigger on `generate_lead`, bound to your GA4 event tag and your
Google Ads (and/or Meta) conversion tag. Use `event_id` / `transaction_id` for deduplication.
Keep the conversion id + label in GTM, not in code.

## Rules that keep it clean

- **All tracking via GTM + dataLayer** — never hardcoded `gtag()` / `fbq()` in components.
- **IDs, keys, endpoints from env** — never hardcoded.
- **One conversion source per event** — fire it client-side (GTM) *or* server-side, not both (double-count).
- **Respect consent** — gate ad-click data on the user's choice (Consent Mode v2).

## Verify

```bash
curl -X POST "$APOINTOO_DASHBOARD_URL/api/intake/$SLUG/contact" \
  -H "X-Apointoo-Tenant-Key: $KEY" -H 'content-type: application/json' \
  -d '{"lead":{"email":"test@example.com"},"attribution":{}}'
# expect: 201 {"submissionId":"...","kind":"contact"}
```
Then in GTM Preview, confirm `generate_lead` fires once and your conversion tag receives it.

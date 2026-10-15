---
name: check-demo-analytics
description: "Report on InboxMate demo page visits, email engagement, and pipeline health. Queries Ackee analytics and CRM to show which demos are getting traffic, which leads are converting, and which need attention."
---

# Check Demo Analytics

> **Announce:**
> ```
> ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
> Demo Analytics Report
> Checking environment...
> ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
> ```

---

## STEP 0 — Check Environment

Read `.env` in the current directory and source it.

Required tokens (variable names should be obvious from context):
- **CRM API** — contains "CRM" + "TOKEN"
- **Ackee API** — contains "ACKEE" + "TOKEN", and an "ACKEE" + "DOMAIN" URL

Stop if missing.

**Ackee config:**
- API: `$<ACKEE_DOMAIN_VAR>/api` (GraphQL)
- Demo domain ID: `4bdddc8c-11d9-4d7e-ab94-aeb7866f0bb2`
- Auth: `Authorization: Bearer $<ACKEE_TOKEN_VAR>`

> **Once verified:** `Environment OK. Pulling analytics...`

---

## STEP 1 — Get Demo Page Views from Ackee

Query Ackee for page-level statistics on the demo domain:

```bash
curl -s -X POST "$<ACKEE_DOMAIN_VAR>/api" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $<ACKEE_TOKEN_VAR>" \
  -d '{"query":"{ domain(id: \"4bdddc8c-11d9-4d7e-ab94-aeb7866f0bb2\") { statistics { pages(sorting: TOP, range: LAST_30_DAYS) { id value count } views(interval: DAILY, type: UNIQUE, limit: 30) { id count } } } }"}'
```

From the `pages` results, extract views per demo page. The `value` field contains the URL path (e.g., `/?id=abc123`). Map each `id` parameter to a demo.

Also get total unique views over the last 30 days from the `views` array.

---

## STEP 2 — Get Pipeline State from CRM

Query CRM for all active opportunities at SCREENING stage:

```bash
curl -s -X POST https://crm.psquared.dev/graphql \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $<CRM_TOKEN_VAR>" \
  -d '{"query":"{ opportunities(filter: { stage: { eq: SCREENING } }, first: 100) { edges { node { id name demoStatus demoUrl { primaryLinkUrl } company { name } createdAt } } } }"}'
```

Also get recently converted (PROPOSAL stage):

```bash
curl -s -X POST https://crm.psquared.dev/graphql \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $<CRM_TOKEN_VAR>" \
  -d '{"query":"{ opportunities(filter: { stage: { eq: PROPOSAL } }, first: 20) { edges { node { id name company { name } createdAt } } } }"}'
```

---

## STEP 3 — Cross-Reference & Analyze

For each SCREENING opportunity with a demoUrl:
1. Extract the demoId from the URL (`?id=xxx`)
2. Find matching Ackee page views (match on `/?id=xxx` path)
3. Calculate days since outreach was sent (from demoStatus timestamps)

Categorize each opportunity:

| Category | Criteria | Action needed |
|----------|----------|--------------|
| **Hot** | Views > 0 + demoStatus = SENT/FOLLOW_UP_SENT | Prospect is engaging — consider direct outreach |
| **Warm** | Views > 0 + not yet sent | Demo is getting organic traffic — prioritize sending |
| **Cold** | Views = 0 + SENT > 7 days ago | No engagement — follow-up or deprioritize |
| **Fresh** | SENT < 5 days ago | Too early to judge |
| **Pending** | PENDING_REVIEW or OK_TO_SEND | Still in pipeline — not yet sent |
| **Converted** | Stage = PROPOSAL | Already signed up |

---

## STEP 4 — Report

> **Announce:**
> ```
> ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
> Demo Analytics Report — [date]
>
> CONVERSION FUNNEL
> ─────────────────
> Leads in CRM:           [N]
> Demos built:            [N]  ([%] of leads)
> Emails sent:            [N]  ([%] of demos)
> Demo page viewed:       [N]  ([%] of sent — email→click rate)
> CTA clicked:            [N]  ([%] of viewed — interest rate)
> Signed up (PROPOSAL):   [N]  ([%] of CTA — conversion rate)
> Paying (CUSTOMER):      [N]  ([%] of signups — close rate)
>
> Overall: [N] leads → [N] customers = [%] conversion
> At current rate: need ~[X] leads to get 1 paying customer
>
> ACKEE EVENTS (last 30 days)
> ───────────────────────────
> Demo page views:        [N] unique visitors
> Widget opened:          [N] ([%] of views — engagement)
> Plan selected:          [N] (Starter: [N], Pro: [N], Business: [N])
> Activate CTA clicked:   [N]
> Discover platform:      [N]
>
> PIPELINE STATUS
> ───────────────
> Pending review:    [N]
> Ready to send:     [N]
> Sent:              [N]
> Follow-up sent:    [N]
> Converted:         [N]
>
> HOT LEADS (views + email sent)
>   - [Company A] — [N] views, sent [N] days ago
>   - [Company B] — [N] views, sent [N] days ago
>
> COLD LEADS (no views, 7+ days)
>   - [Company C] — 0 views, sent [N] days ago
>
> RECOMMENDATIONS
>   [Based on funnel bottleneck:]
>   - If email→view rate is low: "Subject lines may need work, or emails landing in spam"
>   - If view→CTA rate is low: "Demo pages aren't converting — check offer text, countdown, widget"
>   - If CTA→signup rate is low: "Signup friction too high — check onboarding flow"
>   - If signup→paid rate is low: "Trial experience or pricing needs adjustment"
>   - Plus specific company-level recommendations
> ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
> ```

---

## STEP 5 — Query Ackee Events

To get event counts, query each event:

```bash
curl -s -X POST "$<ACKEE_DOMAIN_VAR>/api" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $<ACKEE_TOKEN_VAR>" \
  -d '{"query":"{ event(id: \"[eventId]\") { statistics { chart(interval: DAILY, type: TOTAL) { id count } list(sorting: TOP, type: TOTAL) { id value count } } } }"}'
```

**Event IDs:**
- CTA Click: Claim Bot — `0f037f1c-c2c0-4205-b90d-3cb9bf66f9c2`
- CTA Click: Discover Platform — `1911cb2c-96a9-478e-8a45-82ae8fa71bc8`
- Widget Opened — `df5c0d51-1e96-43a9-8d73-13e0e82e99b3`
- Plan Selected — `8693d36c-09a1-4b86-bf29-763e612f4843`

The `list` query with `sorting: TOP` shows which demo pages / plans got the most actions. The `key` field contains the demoId or planId.

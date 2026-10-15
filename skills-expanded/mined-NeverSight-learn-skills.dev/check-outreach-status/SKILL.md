---
name: check-outreach-status
description: "Check status of sent demo outreach emails. Creates follow-up drafts for prospects who haven't responded after 5+ days. Run periodically after /setup-email-drafts has been used."
---

# Check Outreach Status & Create Follow-ups

> **Announce:**
> ```
> ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
> Outreach Status Check started.
> Checking environment...
> ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
> ```

---

## STEP 0 — Check Environment

Read `.env` in the current directory and source it.

Required tokens:
- **`PSQUARED_CRM_TOKEN`** — CRM GraphQL API
- **`EMAIL_DRAFT_ONLY_BEARER`** — notification service draft API (can read, create, update drafts — cannot send)

Stop if missing.

> **Once verified:** `Environment OK. Checking sent outreach...`

---

## STEP 1 — Find SENT Opportunities

Query CRM for opportunities with `demoStatus = SENT`:

```bash
curl -s -X POST https://crm.psquared.dev/graphql \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $PSQUARED_CRM_TOKEN" \
  -d '{"query":"{ opportunities(filter: { stage: { eq: SCREENING }, demoStatus: { eq: SENT } }, first: 50) { edges { node { id name outreachSentAt demoUrl { primaryLinkUrl } company { id name domainName { primaryLinkUrl } people(first: 5) { edges { node { id name { firstName lastName } emails { primaryEmail } } } } } } } } }"}'
```

For each opportunity:
- Use `outreachSentAt` timestamp to calculate days since sent

> **Announce:**
> ```
> Found [N] opportunities with SENT status:
> 1. [Company] — sent [N] days ago
> 2. [Company] — sent [N] days ago
> ```

---

## STEP 2 — Determine Follow-up Actions

For each opportunity, decide:

| Days since sent | Action |
|-----------------|--------|
| < 5 days | Skip — too early for follow-up |
| 5-10 days | Create follow-up draft |
| > 10 days | Create follow-up draft + flag as "cold" |

Also check: if the opportunity stage has moved beyond SCREENING (e.g., MEETING, PROPOSAL), skip — they've already responded.

---

## STEP 3 — Determine Follow-up Template ID

**Template UUIDs (hardcoded — do NOT query any API or MCP for these):**

| Template | Locale | UUID |
|----------|--------|------|
| demo-followup | de | `6f49ef62-d62d-4a88-a58b-313340322d51` |
| demo-followup | en | `956b815b-4061-48e7-a351-e3215ae85f86` |

Match locale to company (same logic: .at/.de/.ch → de, else en).

---

## STEP 4 — Create Follow-up Drafts

For each opportunity needing follow-up:

**If no contact email:** Skip with note.

The follow-up uses the same template shell as outreach. Write a shorter, more casual follow-up. Don't repeat the original pitch — just check in and make it easy to click the demo link again.

```bash
curl -s -X POST https://notifications.psquared.dev/drafts/create \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $EMAIL_DRAFT_ONLY_BEARER" \
  -d '{
    "templateId": "[followup template UUID from step 3]",
    "locale": "[de|en]",
    "recipientEmail": "[contact email]",
    "recipientName": "[contact first name]",
    "variables": {
      "companyName": "[Company Name]",
      "demoUrl": "[demo playground URL]",
      "greeting": "[casual greeting — same tone as initial outreach]",
      "bodyParagraph1": "[short check-in — did you get a chance to look at the demo?]",
      "buttonText": "[e.g. Demo nochmal ansehen / View Demo Again]",
      "closingText": "[brief — offer to adjust the demo or answer questions]",
      "signoff": "[matching tone]",
      "senderName": "Martin"
    },
    "crmCompanyId": "[company ID]",
    "crmOpportunityId": "[opportunity ID]",
    "crmCompanyName": "[Company Name]",
    "draftType": "followup"
  }'
```

> **Announce after each:** `Follow-up draft created: [Company] → [email] (sent [N] days ago)`

**Note:** This skill does NOT update CRM fields. When the follow-up is actually sent from the admin UI, the notification service automatically sets:
- `demoStatus` → `FOLLOW_UP_SENT`
- `followupSentAt` → current timestamp

---

## STEP 5 — Report

> **Announce:**
> ```
> ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
> Outreach Status Check complete.
>
> Follow-up drafts created: [N]
>   - [Company A] → email (sent 6 days ago)
>   - [Company B] → email (sent 8 days ago)
>
> Too early for follow-up: [N]
>   - [Company C] — sent 2 days ago
>
> Already progressed: [N]
>   - [Company D] — stage moved to MEETING
>
> Cold leads (10+ days, no response): [N]
>   - [Company E] — sent 12 days ago ⚠️
>
> Next step: Review and send follow-ups at
> → notifications.psquared.dev/drafts
> ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
> ```

---

## CRM Fields Reference

**Reads:** `demoStatus` (filter SENT), `outreachSentAt` (days since sent), `demoUrl`, `stage`, contact info

**Does NOT write any fields.** The notification service handles CRM updates on actual send.

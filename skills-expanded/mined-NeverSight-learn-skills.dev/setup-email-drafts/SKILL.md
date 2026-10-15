---
name: setup-email-drafts
description: "Create email drafts for approved InboxMate demos. Verifies all demos are ready, pulls contacts from CRM, creates CRM tasks, and creates draft emails via the notification service. Run after /review-demos has processed all pending demos."
---

# Setup Email Drafts for Demo Outreach

---

## Product Context — What You're Selling

InboxMate is a white-label AI chatbot that businesses embed on their website. It answers customer questions 24/7 using the company's own knowledge base (products, pricing, FAQ). Visitors chat with it directly on the site. It handles lead qualification, appointment scheduling, and support — in the company's brand colors and language. Built by psquared, an Austrian AI company.

**The demo we built for them is a live, working chatbot already configured with THEIR products and knowledge.** This is the key differentiator — we're not pitching a generic tool, we're showing them something that already works for their business.

---

## Cold Outreach Principles

Follow these when writing every email. Based on Hormozi's value-first framework and proven B2B cold email patterns.

**1. Lead with value, not a pitch.**
Don't open with "we are" or "our product does." Open with something you DID for them. "We built a chatbot for [Company] that knows your products" — that's value delivered before they even reply.

**2. Make it about THEM, not you.**
Every sentence should be about their business, their customers, their problems. If you catch yourself writing about InboxMate features, rewrite it as a benefit for THEM. Not "InboxMate can qualify leads" → "Your website visitors get instant answers about [their specific product] instead of waiting for a callback."

**3. Show, don't tell.**
The demo link IS the pitch. Don't over-explain what it does — make them curious enough to click. "We configured it with your pricing, FAQ, and team info — see for yourself" beats a feature list.

**4. Be specific, not generic.**
Reference something concrete from their website. A product name, a service, a team member, their pricing structure. This proves you actually looked at their business and didn't just spray-and-pray.

**5. Keep it short.**
3-5 short paragraphs max. Every sentence must earn its place. If they stop reading after the first paragraph, that paragraph alone should make them want to click the demo.

**6. One clear CTA.**
The demo button. That's it. Don't ask for a call, a meeting, and a demo review all at once. Just click the demo.

**7. The highlight box is your power move.**
Use it to describe what InboxMate does for THIS company in their language. If they're a real estate agency: "Immobilienanfragen sofort beantworten, Besichtigungstermine vorschlagen, Exposés teilen — rund um die Uhr." If they're an IT company: "Kunden zum richtigen Service leiten, Angebote vorbereiten, Support-Tickets erstellen." Make them see their own workflow automated.

**8. Subject line = curiosity gap.**
Don't give away the punchline. "[Company] — etwas für euch gebaut" beats "[Company] — Ihr persönlicher KI-Chatbot Demo". The first makes them open it to find out what. The second tells them everything and they can decide to skip.

---

> **Announce:**
> ```
> ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
> Email Draft Pipeline started.
> Checking environment...
> ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
> ```

---

## STEP 0 — Check Environment

**Read `.env` using the Read tool** (do NOT `source` it — values may contain semicolons or special characters that break shell parsing). Extract the token values by reading the file content directly.

The `.env` file should contain:
- **`PSQUARED_CRM_TOKEN`** — for querying opportunities and creating tasks
- **`EMAIL_DRAFT_ONLY_BEARER`** — for creating email drafts via the notification service. This token can **read, create, and update** drafts but **cannot send, schedule, or delete** them.

If the `.env` file is missing either token, **stop immediately** and ask the user to provide them.

> **Once verified, announce:** `Environment OK. Checking demo readiness...`

---

## Shell Quoting for CRM GraphQL Queries

**IMPORTANT:** When sending GraphQL queries to the CRM via curl, **always use double-quoted `-d` strings** with escaped inner quotes. Single-quoted strings cause intermittent parse failures with the Twenty CRM GraphQL endpoint when queries contain nested object fields like `demoUrl { primaryLinkUrl }`.

**Do this:**
```bash
curl -s -X POST https://crm.psquared.dev/graphql \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $CRM_TOKEN" \
  -d "{\"query\":\"{ opportunities(first: 5) { edges { node { id name } } } }\"}"
```

**NOT this** (breaks with nested fields):
```bash
curl -s -X POST https://crm.psquared.dev/graphql \
  -d '{"query":"{ opportunities(first: 5) { edges { node { id name demoUrl { primaryLinkUrl } } } } }"}'
```

All curl examples below use the safe double-quoted form.

---

## STEP 1 — Verify All Demos Are Ready

Query CRM for ANY opportunities at SCREENING stage with `demoStatus = PENDING_REVIEW`:

```bash
curl -s -X POST https://crm.psquared.dev/graphql \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $PSQUARED_CRM_TOKEN" \
  -d "{\"query\":\"{ opportunities(filter: { stage: { eq: SCREENING }, demoStatus: { eq: PENDING_REVIEW } }, first: 5) { edges { node { id name } } } }\"}"
```

**If any PENDING_REVIEW found:** Stop and announce:

> ```
> ❌ [N] demos still pending review:
>   - [Company A]
>   - [Company B]
> Run /review-demos first before setting up email drafts.
> ```

**If none found:** Continue.

---

## STEP 2 — Collect OK_TO_SEND Opportunities

Query CRM for opportunities with `demoStatus = OK_TO_SEND`, including `taskTargets` in the response so we can filter out already-processed ones client-side:

**IMPORTANT:** The Twenty CRM does NOT support relation filters like `taskTargets: { is: NULL }` on `OpportunityFilterInput`. The `taskTargets` field is only available as a response field on the `Opportunity` type, not as a filter. You MUST fetch `taskTargets` in the response and filter client-side.

```bash
curl -s -X POST https://crm.psquared.dev/graphql \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $PSQUARED_CRM_TOKEN" \
  -d "{\"query\":\"{ opportunities(filter: { stage: { eq: SCREENING }, demoStatus: { eq: OK_TO_SEND } }, first: 150) { edges { node { id name taskTargets { edges { node { id } } } demoUrl { primaryLinkUrl } company { id name domainName { primaryLinkUrl } people(first: 5) { edges { node { id name { firstName lastName } emails { primaryEmail } } } } } } } } }\"}"
```

**Client-side filtering:** After receiving the response, **skip any opportunity where `taskTargets.edges` is non-empty** (length > 0). These have already been processed by a previous run. Add them to a "Skipped (already processed)" list in the report.

For each remaining opportunity, extract:
- `opportunityId`, `opportunityName`
- `companyId`, `companyName`, `companyDomain`
- `demoUrl` (from `demoUrl.primaryLinkUrl`)
- Contact: from `company.people` — pick the first person with an email. For multi-contact companies, prefer a named person (not "Office") if available.

**If company has no people or no email:** Add to skip list with reason "No contact email found". Continue to next.

**If no OK_TO_SEND opportunities (after filtering):** Announce "No demos ready to send" and stop.

> **Announce:**
> ```
> Found [N] demos ready for outreach:
> 1. [Company Name] → [contact email]
> 2. [Company Name] → [contact email]
> ...
> Skipped (no contact): [list if any]
> ```

---

## STEP 3 — Determine Template ID

**Template UUIDs (hardcoded — do NOT query the notification service API or Supabase MCP for these):**

| Template | Locale | UUID |
|----------|--------|------|
| demo-outreach | de | `b98926be-5977-40a6-9be6-ffe38989fc5a` |
| demo-outreach | en | `47381011-a737-4157-a177-f7646bb4aee3` |

For each opportunity, determine the locale:
- If company domain is .at, .de, .ch → locale `de`
- If company website was in German during demo review → locale `de`
- Otherwise → locale `en`

Use the matching UUID above.

---

## STEP 4 — For Each Opportunity

### 4a — MANDATORY: Check if draft already exists in notification service

**THIS CHECK IS NOT OPTIONAL. Do NOT skip it. Do NOT proceed to 4b without running this check.**

Note: CRM task deduplication is already handled in Step 2 by fetching `taskTargets` and filtering client-side. This step only checks the notification service.

**Query notification service for existing drafts by opportunity ID:**

```bash
curl -s -X GET "https://notifications.psquared.dev/drafts?crmOpportunityId=[opportunityId]&pageSize=1" \
  -H "Authorization: Bearer $EMAIL_DRAFT_ONLY_BEARER"
```

If the response contains any drafts (array length > 0, regardless of status) → **SKIP**. Announce: `SKIP: [Company Name] — draft already exists`

**Only proceed to 4b if no drafts found.**

### 4b — Create CRM Task

```bash
curl -s -X POST https://crm.psquared.dev/graphql \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $PSQUARED_CRM_TOKEN" \
  -d "{\"query\":\"mutation { createTask(data: { title: \\\"Send initial outreach for Demo [Company Name]\\\", status: TODO }) { id } }\"}"
```

**Save the `taskId` from the response** — it will be passed to the draft creation so we can reliably delete this exact task if the draft is deleted.

Then link to opportunity:

```bash
curl -s -X POST https://crm.psquared.dev/graphql \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $PSQUARED_CRM_TOKEN" \
  -d "{\"query\":\"mutation { createTaskTarget(data: { taskId: \\\"[taskId]\\\", opportunityId: \\\"[opportunityId]\\\" }) { id } }\"}"
```

### 4c — Create Email Draft

The email template is a pure layout shell — **you write ALL the text**. The template only provides the InboxMate header, green CTA button, highlight box, signoff area, and p² footer. Everything else comes from your variables.

**Writing style:**
- Write like a real person, not a marketing bot. Short sentences. Direct.
- The email should feel like Martin personally wrote it for this specific company
- No corporate filler ("wir freuen uns...", "hiermit möchten wir..."). Get to the point.
- Make the reader curious about the demo — don't explain everything, tease it
- The highlight box should make them think "oh that's exactly what I need"

**Determine tone (du vs Sie) for German emails — THIS IS CRITICAL, DO NOT SKIP:**

For EACH company, before writing any text, check for prior communication:

```bash
curl -s -X POST https://crm.psquared.dev/graphql \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $PSQUARED_CRM_TOKEN" \
  -d "{\"query\":\"{ people(filter: { companyId: { eq: \\\"[companyId]\\\" } }, first: 5) { edges { node { emails { primaryEmail } } } } }\"}"
```

Then check if we have email threads with any of those email addresses in the agenthub DB:

```bash
curl -s -X POST https://crm.psquared.dev/graphql \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $PSQUARED_CRM_TOKEN" \
  -d "{\"query\":\"{ noteTargets(filter: { companyId: { eq: \\\"[companyId]\\\" } }, first: 20) { edges { node { note { title body } } } } }\"}"
```

Look at the note/email content for "du/dir/dein" vs "Sie/Ihnen/Ihr" patterns.

**Rules:**
1. If prior emails/notes use "du" → use "du" (Hallo [Vorname],)
2. If the company website prominently uses "du" throughout → mirror it
3. If no prior contact exists → **default to Sie** (Guten Tag Herr/Frau [Nachname],)
4. When in doubt → Sie

**Verify your choice:** After writing all text for a company, re-read every sentence and check that du/Sie is consistent. A single "Ihre" in an otherwise du-Form email is a dealbreaker.

**Template variables:**

- **`greeting`** — Personal. e.g. "Hallo [Vorname]," (du) or "Guten Tag Herr/Frau [Nachname]," (Sie)
- **`bodyParagraph1`** — The hook. What you did and why it matters to THEM. One strong sentence.
- **`bodyParagraph2`** — (optional) The personalized insight. Something specific about their website/business that shows you actually looked. This is what makes them keep reading.
- **`bodyParagraph3`** — (optional) The nudge toward the demo. Keep it short.
- **`buttonText`** — CTA button label. "Demo ansehen" / "View Demo" / or something more specific
- **`highlightTitle`** — (optional) Bold title for the green box. e.g. "Was der Bot für [Company] tun kann:" or "What this means for [Company]:"
- **`highlightText`** — (optional) One punchy line about what InboxMate does for THIS company specifically. Not generic features.
- **`closingText`** — (optional) Brief closing. "Bei Fragen einfach antworten." / "Just reply if you have questions."
- **`signoff`** — "Beste Grüße" / "Liebe Grüße" / "Best regards" — match the tone
- **`senderName`** — "Martin"
- **`demoUrl`** — the demo playground URL
- **`companyName`** — used in email title
- **`emailSubject`** — the rendered subject line (same as what you set on the draft)

```bash
curl -s -X POST https://notifications.psquared.dev/drafts/create \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $EMAIL_DRAFT_ONLY_BEARER" \
  -d '{
    "templateId": "[template UUID from step 3]",
    "locale": "[de|en]",
    "subject": "[curiosity-driven subject line — see principle #8]",
    "recipientEmail": "[contact email]",
    "recipientName": "[contact first name]",
    "variables": {
      "companyName": "[Company Name]",
      "demoUrl": "[demo playground URL]",
      "greeting": "[personal greeting]",
      "bodyParagraph1": "[the hook — what you did, why it matters]",
      "bodyParagraph2": "[personalized insight about their business]",
      "bodyParagraph3": "[nudge toward the demo]",
      "buttonText": "[CTA button text]",
      "highlightTitle": "[bold title for green box]",
      "highlightText": "[what InboxMate does for THIS company — one punchy line]",
      "closingText": "[brief closing]",
      "signoff": "[matching tone signoff]",
      "senderName": "Martin"
    },
    "crmCompanyId": "[company ID]",
    "crmOpportunityId": "[opportunity ID]",
    "crmCompanyName": "[Company Name]",
    "crmTaskId": "[taskId from step 4b]"
  }'
```

> **Announce after each:** `Draft created: [Company Name] → [email]`

**Note:** This skill does NOT update CRM fields. The notification service updates them automatically when emails are sent from the admin UI:

| On send | Field | Value |
|---------|-------|-------|
| Outreach email sent | `demoStatus` | `SENT` |
| Outreach email sent | `outreachSentAt` | current timestamp |
| Follow-up email sent | `demoStatus` | `FOLLOW_UP_SENT` |
| Follow-up email sent | `followupSentAt` | current timestamp |

---

## STEP 5 — Report

> **Announce:**
> ```
> ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
> Email Draft Setup complete.
>
> Drafts created: [N]
>   - [Company A] → kontakt@firma.at
>   - [Company B] → info@company.com
>
> Skipped (draft already exists): [N]
>   - [Company C] — task already linked
>
> Skipped (no contact email): [N]
>   - [Company D] — no contact with email found
>
> CRM tasks created: [N]
>
> Next step: Review and send drafts at
> → notifications.psquared.dev/drafts
> ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
> ```

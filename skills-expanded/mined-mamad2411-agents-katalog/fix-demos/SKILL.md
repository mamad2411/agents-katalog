---
name: fix-demos
description: "Fix InboxMate demos flagged as NEEDS_FIX during QA review. Reads review issues from CRM, applies fixes via MCP (colors, prompts, knowledge, questions), and resubmits for review. Run after /review-demos has flagged issues."
---

# Fix Flagged InboxMate Demos

> **Announce:**
> ```
> ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
> Fix Demos started.
> Finding demos that need fixes...
> ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
> ```

---

## STEP 0 — Check Environment

**Read `.env` using the Read tool.** Required tokens:
- `PSQUARED_CRM_TOKEN` — CRM API bearer token
- `NUXT_MCP_DEMO_TOKEN` — InboxMate MCP server token
- `OPENBRAND_API_KEY` — OpenBrand color extraction API key

**MCP connection:**
- URL: `https://app.psquared.dev/api/mcp`
- Auth: `Authorization: Bearer <NUXT_MCP_DEMO_TOKEN>`
- Transport: JSON-RPC 2.0 over HTTP POST

**Call `tools/list` on the MCP server** to confirm connectivity and get available tools.

> **Once verified:** `Environment OK. Connecting to MCP...`

---

## STEP 1 — Find Demos Needing Fixes

Query CRM for opportunities at SCREENING stage with `demoStatus = NEEDS_FIX`:

```bash
curl -s -X POST https://crm.psquared.dev/graphql \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $PSQUARED_CRM_TOKEN" \
  -d '{"query":"{ opportunities(filter: { stage: { eq: SCREENING }, demoStatus: { eq: NEEDS_FIX } }, first: 50) { edges { node { id name stage demoStatus demoId demoReviewIssues demoUrl { primaryLinkUrl } company { id name domainName { primaryLinkUrl } } pointOfContact { id name { firstName lastName } emails { primaryEmail } } } } } }"}'
```

> **Announce:**
> ```
> Found [N] demos needing fixes:
> 1. [Company Name] — Issues: [demoReviewIssues summary]
> 2. [Company Name] — Issues: [demoReviewIssues summary]
> ...
> ```

If none found, announce "No demos need fixing" and stop.

---

## STEP 2 — Fix Each Demo

For each opportunity with `NEEDS_FIX`, parse the `demoReviewIssues` field and apply the appropriate fixes.

### 2a — Parse Issues

The `demoReviewIssues` field contains a text description of what failed QA. Common issues and their fix actions:

| Issue keyword | Fix action |
|---------------|------------|
| **color** / **brand** / **Farbe** | Re-extract brand color via OpenBrand, update widget via MCP `update_widget_style` |
| **greeting** / **Begrüßung** | Fetch company website, rewrite greeting, update via MCP `update_widget_style` |
| **language** / **Sprache** | Fix language mismatch — update `uiLang`, greeting, questions via MCP |
| **questions** / **Fragen** / **cards** | Rewrite quick questions based on actual company content, update via MCP `update_quick_questions` |
| **knowledge** / **content** / **hallucination** | Re-scrape the company website, update/add knowledge items via MCP `add_to_bucket` |
| **wrong company** | Critical — demo was built for wrong company. Skip and flag for manual rebuild |
| **prompt** / **system prompt** | Rewrite system prompt based on company website, update via MCP `update_prompt` |
| **offer** / **countdown** | Update demo page offer text/expiry via MCP `update_demo_page` |

### 2b — Fetch Company Website

Use WebFetch on the company's domain (`company.domainName.primaryLinkUrl`) to get current content. This is needed for most fixes — always do it.

Check key pages:
- Homepage
- `/kontakt` or `/contact`
- `/impressum` or `/imprint`
- `/leistungen` or `/services`

### 2c — Apply Fixes

**For color issues:**

```bash
curl "https://openbrand.sh/api/extract?url=https://[domain]" \
  -H "Authorization: Bearer $OPENBRAND_API_KEY"
```

Use the `primary` color from the response. **Never use pure black (`#000000`) or pure white (`#ffffff`)** — if primary is black/white, use `secondary`. If too light or too dark, pick the next best color. Then update:

```json
{
  "method": "tools/call",
  "params": {
    "name": "update_widget_style",
    "arguments": {
      "agentId": "[demoId from CRM]",
      "primaryColor": "[corrected hex]"
    }
  }
}
```

**For greeting issues:**

Write a new greeting that's specific to the company (not generic). Must reference the company name and product/service.

```json
{
  "method": "tools/call",
  "params": {
    "name": "update_widget_style",
    "arguments": {
      "agentId": "[demoId]",
      "greetingMessage": "[new EN greeting or omit]",
      "greetingMessageDe": "[new DE greeting or omit]"
    }
  }
}
```

**For question issues:**

Rewrite quick questions based on actual website content. Always use card format.

```json
{
  "method": "tools/call",
  "params": {
    "name": "update_quick_questions",
    "arguments": {
      "agentId": "[demoId]",
      "style": "cards",
      "questionsEn": [{ "text": "...", "title": "...", "description": "...", "icon": "..." }],
      "questionsDe": [{ "text": "...", "title": "...", "description": "...", "icon": "..." }]
    }
  }
}
```

**For knowledge/content/hallucination issues:**

Re-scrape the relevant pages and update knowledge items. Use `add_to_bucket` with the existing bucket. Each item MUST have a `sourceUrl`.

```json
{
  "method": "tools/call",
  "params": {
    "name": "add_to_bucket",
    "arguments": {
      "bucketId": "[existing bucketId]",
      "title": "[corrected title]",
      "content": "[corrected content from actual website]",
      "sourceUrl": "https://[domain]/[page]"
    }
  }
}
```

**For prompt issues:**

Rewrite the system prompt to be specific to this company. Follow the template from the inboxmate-demo skill (Phase 2c).

```json
{
  "method": "tools/call",
  "params": {
    "name": "update_prompt",
    "arguments": {
      "agentId": "[demoId]",
      "prompt": "[rewritten system prompt]"
    }
  }
}
```

**For offer/countdown issues:**

```json
{
  "method": "tools/call",
  "params": {
    "name": "update_demo_page",
    "arguments": {
      "demoId": "[demoId]",
      "offerText": "[corrected offer text]",
      "offerExpiresAt": "[7 days from today, ISO 8601]"
    }
  }
}
```

### 2d — Republish Agent

After all fixes are applied, republish the agent:

```json
{
  "method": "tools/call",
  "params": {
    "name": "publish_agent",
    "arguments": { "agentId": "[demoId]" }
  }
}
```

### 2e — Verify Fix

Use WebFetch on the demo URL (`demo.inboxmate.psquared.dev/?id=[demoId]`) to confirm the fixes are visible.

Quick sanity check:
- Color matches brand? ✓/✗
- Greeting is company-specific? ✓/✗
- Questions are relevant? ✓/✗
- Content looks accurate? ✓/✗

### 2f — Update CRM

Set `demoStatus` back to `PENDING_REVIEW` and clear `demoReviewIssues`:

```bash
curl -s -X POST https://crm.psquared.dev/graphql \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $PSQUARED_CRM_TOKEN" \
  -d '{"query":"mutation { updateOpportunity(id: \"[opportunityId]\", data: { demoStatus: PENDING_REVIEW, demoReviewIssues: \"\" }) { id demoStatus } }"}'
```

> **Announce after each:** `Fixed: [Company Name] — [what was fixed]. Resubmitted for review.`

---

## STEP 3 — Handle Unfixable Demos

If a demo has a critical issue that can't be fixed by updating (e.g., "wrong company", fundamentally broken):

1. **Do NOT attempt to fix** — flag for manual rebuild
2. Add a note explaining why it can't be auto-fixed:

```bash
curl -s -X POST https://crm.psquared.dev/graphql \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $PSQUARED_CRM_TOKEN" \
  -d '{"query":"mutation { updateOpportunity(id: \"[opportunityId]\", data: { demoReviewIssues: \"REQUIRES REBUILD: [reason]. Run /inboxmate-demo to recreate from scratch.\" }) { id } }"}'
```

> **Announce:** `SKIP: [Company Name] — requires full rebuild. Reason: [reason]`

---

## STEP 4 — Report

> **Announce:**
> ```
> ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
> Fix Demos complete.
>
> Fixed & resubmitted:
>   - [Company A] — [what was fixed]
>   - [Company B] — [what was fixed]
>
> Skipped (need rebuild):
>   - [Company C] — [reason]
>
> Next step: Run /review-demos to re-review fixed demos
> ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
> ```

---

## Important Reminders

- **Always re-scrape the company website** before fixing — don't guess from memory
- **OpenBrand for colors** — don't eyeball CSS, use the API
- **Republish after changes** — MCP changes don't go live until `publish_agent` is called
- **Card format for questions** — always objects with `{ text, title, description, icon }`, always set `style: "cards"`
- **Every knowledge item needs `sourceUrl`** — the exact page URL it was scraped from
- **Clear `demoReviewIssues`** when resubmitting — prevents stale issue text from confusing the next review
- **Don't force-fix unfixable demos** — flag for rebuild instead

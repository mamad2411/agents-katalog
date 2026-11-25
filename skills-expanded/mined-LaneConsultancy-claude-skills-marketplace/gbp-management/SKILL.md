---
name: gbp-management
description: Use when operating a Google Business Profile for an agency client — responding to reviews, publishing posts/offers, updating hours/services/photos — or when the user asks to "reply to that review", "post an update to GBP", or manage business.google.com. NOT for rank-and-rent sites (standing no-GBP policy).
---

# Google Business Profile Management

## Overview

Operate (not just audit — that's `seo-local`) client GBPs via browser automation on business.google.com. The GBP API is application-gated, so the browser IS the tool: use Claude-in-Chrome or Playwright, logged into the client's managing Google account.

## Hard Rules

1. **Rank-and-rent sites never get a GBP.** If the business is on the rank-and-rent portfolio, stop and remind the user of the policy. Agency clients only.
2. **Nothing publishes without George's explicit approval of the exact text.** Review responses, posts, profile edits — draft first, show the draft, publish only after "yes". A GBP action is public and often irreversible.
3. **Facts come from the client's FACTS.md** (see client-intake skill). No invented offers, hours, or service claims in posts.
4. **Screenshot before and after every change** — the before-state is the rollback reference.
5. **Never change the primary category, business name, or address without George asking for exactly that** — these trigger re-verification and ranking resets.

## Operations

### Review responses
- Respond to every review, newest first, within 48 hours of it appearing (Google confirms responding lifts rankings; the lift is amplified inside 24–48h). Match length to the review (2–4 sentences max).
- Response text gets indexed: mention the service performed and the town naturally in the reply where the review states them. Never force keywords.
- Voice: the business owner, first person, warm, specific — reference what the job actually was if stated. No corporate boilerplate ("We strive to...").
- Negative reviews: build the reply from exactly these four parts, in order, nothing else:
  1. Thanks + apology for the experience (not an admission the claims are true)
  2. Name the specific complaint back ("the timing and the billing difference you mentioned")
  3. One corrective statement about process, not remedy ("I want to understand what happened")
  4. Take it offline: "call me on [FACTS.md phone]"
  The remedy (refund, redo, discount) is discussed on the phone — any remedy word appearing in the public reply means the draft is wrong; rewrite it. Never argue, never admit legal fault. If the review looks fake/wrong-business, draft a flag-for-removal instead of a reply.

### Posts / offers
- Types: update, offer (needs start/end dates), event. Keep to ~80–150 words, one CTA button, one photo (from client assets or `generate-image` — sample-before-batch rule applies).
- Offers must exist in FACTS.md pricing. Expired offers: check for and delete on every visit.
- Posts are an engagement/CTR tool, not a ranking lever (Sterling Sky: zero ranking movement across 441 keywords over 9 weeks). Do them lightly when there's something genuine to say; never invent occasions to post.

Note: GBP Q&A was removed by Google (Dec 2025). Common questions (parking, pricing, service area, emergency availability) now belong as FAQ content on the client's website instead.

### Profile hygiene (each monthly visit)
- Hours correct (incl. upcoming bank holidays) — being open at the time of search is a top-5 pack factor, and rankings degrade while closed. If the client genuinely takes emergency calls out of hours, hours should say so. Never leave a profile marked temporarily closed.
- Services list matches FACTS.md, and every predefined service Google suggests for the category is added (predefined services jumped #81 to #22 in ranking importance; they feed AI Overview answers directly).
- Website link points at a strong service or location page, not a homepage that already ranks organically (Diversity Update), and carries UTM parameters. Flag to George if it doesn't; changing it is a draft-and-approve edit like any other.
- Photos: add 1–2 recent real job photos if supplied (geotagging does nothing, Google strips EXIF), check for and dispute wrong third-party edits ("Suggested edits" section).

### Quarterly (in addition to monthly)
- Re-check primary/secondary categories against Google's evolving list (report findings; rule 5 still applies — never change the primary category without George asking).
- Audit the services section against FACTS.md; check for duplicate or "permanently closed" listings.

Source for the ranking claims above: `~/.agents/skills/references/shared-seo/local-seo-playbook-2026.md`.

## Workflow

1. Confirm client + FACTS.md exists; confirm this is NOT a rank-and-rent property.
2. Open business.google.com in the browser, select the correct location — verify business name in a screenshot before touching anything.
3. Do the requested operation as drafts; present all drafts to George in one batch.
4. On approval: publish, screenshot each published item, report with links.
5. Log what was done in the client project (e.g. `gbp-log.md`) so the next monthly visit has history.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Publishing a "harmless" review reply without approval | Rule 2 has no exceptions — public + irreversible. |
| Generic thank-you replies to every review | Reference the specific job/detail; generic replies read as automated and hurt trust. |
| Writing an offer post from memory of pricing | Pricing changes; FACTS.md or ask. The discontinued list applies to GBP too. |
| Working on the wrong location in a multi-location account | Screenshot-verify the location name before any edit. |
| Treating this as an SEO audit | Auditing signals is `seo-local`; this skill is operations. |

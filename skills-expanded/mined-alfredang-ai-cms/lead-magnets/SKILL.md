---
name: lead-magnets
description: Plan and build lead-magnet flows for Tertiary Infotech — gated guides, checklists, calculators, webinars, and consultation forms — wired into the existing leads pipeline (`/api/contact` → `leads` table → admin notification email). Use whenever the task involves capturing emails, generating qualified leads, or designing a CTA/landing page for SSG ATO, TPQA, LMS/TMS, or AI services.
---

# Lead Magnets — Tertiary Infotech

You are the lead-magnet strategist for **Tertiary Infotech**. Your job is to plan magnets that capture emails, qualify intent, and feed warm leads into our consulting and AI-LMS-TMS pipeline.

## Before You Start

1. If `.claude/product-marketing-context.md` exists, read it first.
2. Read [src/app/api/contact/route.ts](src/app/api/contact/route.ts) — this is the single lead intake endpoint. All forms POST to `/api/contact` with `{ name, email, phone?, company?, message, source }`. Use the `source` field to identify which magnet/page produced the lead (e.g. `"ssg-ato-page"`, `"tpqa-checklist"`, `"lms-demo"`).
3. Read [src/components/sections/ContactForm.tsx](src/components/sections/ContactForm.tsx) for the canonical form pattern (glass card, kicker labels, `btn-primary`, status states).
4. Confirm the `leads` table in [src/db/schema.ts](src/db/schema.ts) and the admin notification flow in [src/lib/email.ts](src/lib/email.ts) before adding new fields. Don't expand the schema casually — re-use `message` for magnet-specific context unless the field is queried in admin views.

## Business Context (anchor your plan on this)

- **Company**: Tertiary Infotech — Singapore-based AI-LMS-TMS + SSG ATO/TPQA/WSQ consultancy.
- **Ideal customer profiles**:
  1. **Aspiring TPs** — Singapore SMEs or trainers who want to become an SSG-registered training provider (ATO). High intent, high LTV. Pain: TPGateway paperwork is dense, audit is intimidating, $545 fee is non-refundable.
  2. **Existing ATOs** — already registered, need TPQA mock audits, evidence remediation, or LMS to pass attendance/funding-claim requirements.
  3. **Corporate L&D** — needs LMS/TMS for internal training (in-house TP track).
  4. **SMEs / agencies** — need bespoke AI automation, web/mobile builds.
- **Primary conversion goals** (in order):
  1. Booked consultation call (highest value — sales-qualified lead).
  2. Magnet download with phone number (marketing-qualified lead, can be nurtured to call).
  3. Newsletter subscriber (top of funnel).
- **Acceptable cost per lead**: high — consulting AOV is S$10k–50k+ per ATO engagement, so even paid leads at S$50–150 each pay off if call-conversion is ≥10%.

## Magnet Inventory (use these, don't reinvent)

| ICP | Magnet | Format | Effort | Why it works |
|-----|--------|--------|--------|--------------|
| Aspiring TP | "SSG ATO Application Readiness Checklist" | 1-page PDF or interactive web checklist | Low | Mirrors actual TPGateway requirements — answers a question they're already Googling |
| Aspiring TP | "ATO Application Cost & Timeline Calculator" | Interactive form on-page | Medium | Concrete numbers (the $545 fee + our consulting fee) qualifies budget |
| Aspiring TP | "How to Apply SSG RTP in Singapore" guide | Long-form web page (gated final CTA, not gated content) | Medium | SEO play — captures top-funnel search intent, converts on inline form |
| Existing ATO | "TPQA Mock Audit Self-Assessment" | 15-question form, scored result + PDF report | High | Diagnostic format gets emails; the report itself is the deliverable |
| Existing ATO | "WSQ Course Submission Checklist" | 1-page PDF | Low | Tactical, downloadable, easy to share internally |
| Corporate L&D | "Free 30-day LMS trial" | App signup | High | Trial = the magnet; trial users self-select to call |
| Corporate L&D | "LMS vs TMS — buyer's guide" | PDF | Medium | Top-of-funnel comparison content |
| SME / agency | "AI Automation ROI Calculator" | Interactive | Medium | B2B numeric magnet — qualifies budget and use case |

**Default for service pages**: inline consultation form (not gated download). Singapore B2B buyers in the training space respond better to "Book a free 30-minute consultation" than to gated PDFs. Reserve gated downloads for cold-traffic paid campaigns and SEO landers.

## Form Design Rules

- **Fields by stage**:
  - **Cold traffic / TOFU**: `email` only (or `email` + `name`).
  - **Service pages / MOFU**: `name`, `email`, `company`, `phone`, `message` (the standard `/api/contact` shape — reuse it).
  - **BOFU / consultation request**: above + qualifying question via the `message` field (e.g. *"Where are you in the ATO application process?"* as the textarea placeholder).
- **Never** ask for: company size, role, budget dropdowns. They lower conversion and we can ask on the call.
- **Trust signals next to the form**: "We reply within 1 business day", "Trusted by [N] Singapore training providers", "No spam — your details are not shared".
- **Submit button copy**: action-specific, not "Submit". Use "Book my consultation", "Send me the checklist", "Start my ATO application".
- **Thank-you state**: do not navigate away — show inline success message with next step ("We'll call you within 1 business day. In the meantime, [read the SSG ATO guide]"). The existing `ContactForm.tsx` pattern is correct.

## Landing Page Anatomy (for any magnet)

In order, top to bottom:

1. **Above the fold**: H1 with the outcome ("Become an SSG-registered Training Provider in 90 days"), one-line subhead with the offer, primary form OR primary CTA button anchoring to the form.
2. **Social proof bar**: client logos, "Trusted by X TPs", or quote.
3. **Problem agitation**: 3 bullet points of pain the visitor recognises ("$545 fee is non-refundable", "Onsite audit is intimidating", "Documentation requirements are dense").
4. **The offer**: what they get (consultation, checklist, audit). Concrete deliverables.
5. **Process / timeline visual**: Discovery → Consultation → Quotation → Start Project → Outcome. Reinforces predictability.
6. **What's included** / detailed scope.
7. **FAQ**: 5–8 questions answering objections (cost, timeline, refunds, scope).
8. **Final CTA + form repeated** (don't make them scroll back up).
9. **Footer** with secondary trust signals.

## Distribution

- **SEO**: every magnet has a dedicated SEO-optimised landing page (see the [seo-audit](../seo-audit/SKILL.md) skill). Target one money keyword per page.
- **Blog CTAs**: every long-form post on `/blog` ends with a contextual lead-magnet CTA, not a generic "Contact us".
- **Exit-intent / scroll popup**: skip for now — Singapore B2B audience tolerates them poorly and they hurt CWV.
- **LinkedIn organic**: founder/team posts excerpting magnet content with a link.
- **Partnerships**: cross-promotion with adjacent service providers (accountants, business registration agents) — they have aspiring-TP audiences.

## Measurement

Track per `source` value in the `leads` table:

- **Page CVR**: leads / unique sessions on the landing page. Target ≥ 3% for service pages, ≥ 1% for blog-driven traffic.
- **MQL → SQL rate**: % of leads that book a call. Target ≥ 25%.
- **SQL → customer**: ≥ 20% for warm consultation leads.
- **Time-to-first-reply**: ≤ 1 business day (the form copy promises this — enforce it operationally).

Add new sources by passing `source: "<slug>"` in the form payload. Then filter the admin leads view by source to see per-magnet performance.

## Deliverable Format

When asked to plan a magnet, return:

1. **Recommended magnet** (one, with rationale tied to the ICP and stage).
2. **Headline + subhead + CTA copy** (3 variants of each for A/B testing).
3. **Form shape** (exact field list with the `source` value).
4. **Landing page outline** (H2 sections, in order).
5. **Distribution plan** (3 channels, ranked).
6. **Success metric** (the specific number we should hit in 30/60/90 days).

When **building** a magnet page in this repo:

1. Reuse the `glass`, `kicker`, `btn-primary`, `gradient-text` utility classes from `src/app/globals.css`.
2. Create the form as a `"use client"` component that POSTs to `/api/contact` with a page-specific `source`.
3. Match the existing `ContactForm.tsx` UX (status states, inline success message, no redirect).
4. Wire the SEO metadata per the [seo-audit](../seo-audit/SKILL.md) skill.
5. Add the page to `sitemap.ts` and link it from the homepage Services grid + footer.

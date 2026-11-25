---
name: conversion-patterns
description: Structure a lead-generation page so it can convert, and change it only under measurement — structural CRO for es-MX service businesses on this stack, never persuasive copywriting. Use when designing a landing page structure for leads, deciding the primary conversion action (form, WhatsApp, or phone), placing calls to action, adding trust signals for Mexican customers, or planning a conversion experiment. Standing rule — instrumentation first, because without analytics running there is no CRO, only guessing; edge-logic's A/B pattern is the instrument, the event vocabulary the ruler. Covers the one-primary-CTA rule, landing hierarchy, short forms, WhatsApp-first Mexico, verifiable social proof under the canon's no-fabricated-claims rules, and the anti-patterns. Trigger on landing page structure, conversion rate, more leads, CTA placement, or trust signals. Not for brand copy (brand-canon-ingest owns voice), the form itself or analytics wiring (the playbook's recipes), or the A/B mechanics (edge-logic).
---

# Conversion Patterns — structural CRO under measurement

> A THIN skill with a hard boundary on both sides. It owns STRUCTURE (what sections exist, where the action is, what earns trust) and SEQUENCE (measure, then hypothesize, then test, then decide) — never copy (the brand's voice is governed canon) and never numbers this catalog cannot source. Its claims are mechanical and structural, argued from how pages and attention work, not quantitative industry statistics; where a claim would need a percentage, this skill demands the site's OWN data instead. That demand is the skill.

## Contents

- The instrumentation-first rule
- The primary-conversion decision
- Landing hierarchy
- The one-primary-CTA rule
- Forms, WhatsApp, and phone — the MX conversion surface
- Trust signals for es-MX
- Social proof under the canon
- Anti-patterns
- The experiment loop
- Limitations

## The instrumentation-first rule

CRO without measurement is redecorating. The sequence this skill enforces:

1. The analytics recipe is LIVE (events flowing, `lead_submit` server-side) — not stubbed.
2. A baseline accumulates: 2–4 weeks or a few hundred sessions of funnel data (pageviews → `plan_view` → contact intents → `lead_submit`), whichever comes second.
3. A hypothesis names the LEAK ("plans are viewed but WhatsApp is not clicked"), not a preference ("the button should be green").
4. One change tests at a time — the A/B pattern from edge-logic assigns, `ab_expose` plus the funnel events measure.
5. The decision is the data's; ties go to the simpler variant.

A brief that says "improve conversion" on an unmeasured site gets step 1 as the deliverable, and this skill says so explicitly. Structural defaults below may ship on day one WITHOUT measurement — they are the starting layout, not experiments.

## The primary-conversion decision

Every lead-gen page has exactly ONE primary conversion. Decide it from how the business actually closes, not from web convention:

| Business reality | Primary | Secondary |
|---|---|---|
| Closes in chat, responds fast on the phone (most MX local services) | WhatsApp deep link | Short form |
| Needs qualifying info before responding (quotes, scheduling) | Short form | WhatsApp |
| Closes by voice, older clientele | `tel:` click-to-call | Form |
| Emergency or time-critical service | `tel:` above the fold, repeated | WhatsApp |

The secondary EXISTS but never competes visually (see the one-CTA rule). All three intents are already events in the analytics vocabulary (`whatsapp_click`, `tel_click`, `lead_submit`) — the decision is measurable retroactively, which is exactly why it is testable later.

## Landing hierarchy

Sections in reading order, each earning the next scroll:

1. Above the fold — what this is, for whom, and the primary CTA. The visitor should be able to convert without scrolling; never NEED to scroll to understand the offer.
2. Evidence — how it works, what it includes (the plans section), real proof (below).
3. Objection ground — the questions that stall a decision (price transparency where the brand allows, process, coverage area, response time).
4. The ask, again — a closing CTA block repeating the SAME primary action.

The order is the argument; a section that cannot say which objection it retires or which evidence it adds is decoration and competes with the funnel.

## The one-primary-CTA rule

One page, one primary action, repeated — not one page, five equivalent actions. Mechanically the same argument as the LCP `priority` rule: two things claiming the same attention both lose. Concretely on this stack:

- The primary CTA appears above the fold, after evidence, and at the close — same action, same styling (the brand's action tokens), same wording.
- Secondary actions exist at reduced visual weight (text links, outline style) and never adjacent to a primary at equal size.
- Navigation on a landing page is a distraction budget: fewer places to go means more visitors reach the ask. Reducing nav is a testable hypothesis, not a default.

## Forms, WhatsApp, and phone — the MX conversion surface

- The form IS the playbook's forms recipe — this skill only defends its SHORTNESS. Three visible fields plus consent is the ceiling for a first contact; every added field must name the lead it disqualifies. Qualification belongs in the follow-up conversation, not the form.
- WhatsApp is a first-class conversion in MX, not a nice-to-have — for many local services it out-converts forms. It costs zero (a `wa.me` anchor, zero CSP, zero JS) and is fully measurable (`whatsapp_click`). Placement follows the primary-conversion decision above.
- `tel:` links on every phone number, always — on mobile they are one-tap conversions; unlinked numbers are silent conversion leaks.

## Trust signals for es-MX

Trust is the conversion currency for small MX service businesses; these are structural (slots on the page), and every one is canon-gated content:

- Physical address and coverage area — visible, not buried in the footer.
- Horarios and expected response time — an honest "respondemos el mismo día" outperforms silence, but ONLY if true (canon rule: no service-time claims the owner has not ratified).
- Factura/CFDI availability — a one-line signal that filters serious buyers and marks formality.
- The aviso de privacidad visibly linked at the form (the legal recipe's template) — absence reads as informality to exactly the customers who convert.
- Real identity: the brand's actual name, the owner where the brand allows it — anonymous sites do not get contacted with real problems.

## Social proof under the canon

Social proof converts only when verifiable, and this catalog's brand discipline makes fabrication structurally impossible: testimonials, client counts, years in business, and partner logos are CANON-GATED content — they enter through the brand repo or the owner, never authored by Claude (no-fabricated-claims is a standing brand rule, the same G-rule family that gates service-time promises). The skill's contribution is the SLOT: a proof section exists in the hierarchy, marked placeholder until real proof arrives — an empty marked slot is honest; an invented quote is a violation, not a conversion tactic.

## Anti-patterns

Each is banned for a mechanical or canon reason, not taste:

- Fake urgency and countdown timers — fabricated claims; violates the canon's truth-gating outright.
- Entry popups and interstitials before content — pay attention-cost before value; also a CWV/CLS tax the perf gates will catch.
- Carousels for value propositions — rotation hides content; if three messages matter, they are three sections.
- Multiple equivalent CTAs — see the one-CTA rule.
- Long first-contact forms — see form shortness.
- Dark-pattern consent (pre-checked boxes, buried opt-ins) — the forms recipe already forbids it; repeated here because CRO advice elsewhere recommends it.

## The experiment loop

When measurement exists and a leak is named: hypothesis → ONE structural variant (hero promise, CTA placement, section order — variant-sized, per edge-logic's A/B pattern) → `ab_expose` + funnel events over a comparable window → decide → remove the losing variant (dead experiment markup is weight). Experiments queue; they do not run in parallel on the same page — two concurrent tests on one funnel read each other's noise.

## Limitations

- This skill does NOT write copy. Headlines, promises, and voice are the brand's (brand-canon-ingest); this skill places the SLOT and states the job of the section.
- No quantitative claims — this skill carries no "X% lift" numbers because it cannot source them honestly; the site's own funnel data is the only statistic it trusts. Industry CRO literature is directional inspiration, never citation.
- Scoped to lead-gen service sites (this catalog's archetype). E-commerce funnels (cart, checkout) are a different discipline and out of scope.
- The es-MX trust signals reflect the catalog's market focus; other markets re-derive that section, not the skill.

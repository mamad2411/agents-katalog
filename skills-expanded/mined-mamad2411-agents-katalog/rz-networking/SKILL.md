---
name: rz-networking
description: >
  Use when working on relationship building, outreach, introductions, follow-ups, conference prep, event follow-ups, DM drafting, warm intro requests, speaker pitch emails, advisory relationships, alumni network activation (Techstars, Antler, IBM, Hill Holliday, Phase2), or community engagement (Slack groups, ProductTank, in-person events). Trigger for any interpersonal professional communication that serves audience or career strategy.
---

# Networking — Riché Zamor

You help Riché build mutual-value relationships where both parties are smarter for knowing each other. Networking is career infrastructure, not contact collecting.

## Before beginning work

The corpus has migrated to Notion. Notion is the source of truth — the local `corpus/*` paths cited below are historical and may drift. Always load these references via the Notion MCP (`mcp__bc2cd475-c3cd-49fa-a4ab-02ee9f795171__notion-fetch`) before executing this skill:

1. **Strategy Stack README** — Notion page `357ac0ea-4f65-81b8-98b4-ffd0f376198c` (`Brand > README — Strategy Stack`). Doc ownership, canonical constants, and the Decision-of-Record log. Note: networking is the 1:1 motion distinct from 1:many audience development. Honor it; flag drift.
2. **Your sections of the Corpus** at `Projects > RZ Claude Skills > Corpus`:
   - `networking` → page `357ac0ea-4f65-8140-8b76-f1d2e745abd3` (canonical: tiers, outreach, philosophy, communities, conferences, CRM, import-pipeline)
   - `voice` → page `357ac0ea-4f65-8194-ae1e-e5147adad60c` (every drafted message must pass voice rules)
   - `growth` → page `357ac0ea-4f65-812a-a480-d3b7ab463bc2` (ICP definition, audience flywheel — networking ladders into 1:many)
   - `pm-frameworks` → page `357ac0ea-4f65-8161-9826-e44ea7c16373` (when networking serves a product/founder goal)
   - `brand-system` → page `357ac0ea-4f65-8163-b0a9-c51f37062fc0` (when an outreach asset has a visual component)

Each Corpus directory page lists its child entries. Fetch only the specific entries you need.

## Quick Reference

| Situation | Load | Notes |
|---|---|---|
| Drafting any message (cold, warm, dormant, advisory) | `corpus/networking/outreach/{template}.md` | Match template to situation; never first-message ask |
| Assigning or moving someone between tiers | `corpus/networking/tiers/` | 4 tiers, distinct cadence per tier |
| Conference or event prep | `corpus/networking/conferences/` | Before, during, 48-hour follow-up sequence |
| Framing decision (is this read-aloud test passing?) | `corpus/networking/philosophy/` | Mutual-value test gates every send |
| Slack or in-person community engagement | `corpus/networking/communities/` | 2:1 answer-to-promotion ratio |
| Tracking and weekly review of contacts | `corpus/networking/crm/` | 5-field data model, lightweight tooling |

## Load from corpus

**Philosophy** — `corpus/networking/philosophy/`:
- `mutual-value-test.md` — both parties smarter for knowing each other
- `read-aloud-test.md` — would they read this aloud and say "this person gets it" or "this person wants something"?
- `connect-around-shared-problems.md` — Riché doesn't pitch; he connects around context-architecture problems

**Relationship tiers** — `corpus/networking/tiers/`:
- `tier-1-inner-circle.md` — 5-10 deep relationships, regular contact, mutual mentorship
- `tier-2-active-network.md` — 30-50 people, LinkedIn comments + occasional DMs
- `tier-3-extended-network.md` — 200+ people aware of his work via content
- `tier-4-dormant-network.md` — Techstars, Antler, IBM, Hill Holliday, Phase2 alumni

**Outreach templates** — `corpus/networking/outreach/`:
- `cold-linkedin-connection.md` — context-first, no first-message ask
- `warm-follow-up-after-engagement.md` — reference specific exchange, extend, specific next step
- `speaker-pitch.md` — hook + differentiation + audience takeaway + credentials + logistics
- `network-activation-dormant.md` — reconnect with shared memory + brief update + soft ask
- `advisory-inquiry-response.md` — be generous first, then explore deeper engagement

**Conference preparation** — `corpus/networking/conferences/`:
- `before-event-prep.md`, `during-event-posture.md`, `within-48h-follow-up.md`
- `conversational-pitch-line.md`, `question-templates.md`, `intent-driven-contact-exchange.md`

**Community engagement** — `corpus/networking/communities/`:
- Slack: `slack-mind-the-product.md`, `slack-cpo-club.md`, `slack-product-school.md`, `slack-lennys-newsletter.md`
- In-person: `in-person-venues.md` (ProductTank NYC monthly, Lean Product Meetup virtual, PMs of NY Luma)
- `engagement-rules.md` — substantive perspective; 2:1 answer-to-promotion ratio

**Relationship CRM** — `corpus/networking/crm/`:
- `data-model.md` — 5 fields: name/company/role / how-met / what-they-care-about / value-to-offer / next-action
- `weekly-review-cadence.md`, `tier-movement-rules.md`, `lightweight-tooling.md`

**Cross-skill principles** — `corpus/networking/cross-skill/`:
- `voice-discipline.md`, `segment-priority.md`

## How to apply

1. Pull the philosophy entry for the framing decision (is this read-aloud test passing?).
2. Pull the relevant tier entry to assign or move someone between tiers.
3. Pull the matching outreach template (cold / warm / speaker / dormant / advisory) for any draft.
4. Use the conference prep + during + 48-h follow-up sequence for events.

## Common Mistakes

| Mistake | What goes wrong | Fix |
|---|---|---|
| Cold pitching with first-message ask | Fails the read-aloud test, signals "this person wants something" | Lead with context or specific observation; no ask in message one |
| Connecting without a context-architecture angle | Generic outreach blends in, gets ignored | Anchor every message in a shared problem or specific work |
| Following up without referencing specific exchange | Reads as templated, breaks the mutual-value frame | Quote or reference the exact conversation, post, or session |
| Treating Tier 4 dormant contacts like Tier 2 | Cold reactivations land flat without shared memory | Use `network-activation-dormant.md` pattern: shared memory plus brief update plus soft ask |
| Promoting in Slack groups before contributing | Violates 2:1 answer-to-promotion ratio, gets muted | Ship 2 substantive answers before any self-reference |

## Cross-skill connections

**Upstream (reads from these for canonical knowledge):**
- `rz-copywriting`. Voice rules for every message Riché sends, lives at `corpus/voice/`.
- `rz-growth-marketing`. Audience segments and prioritization, lives at `corpus/growth/segments/`. Speaker hook lives at `corpus/growth/speaking/the-hook.md`.
- `rz-product-management`. Substance for advisory inquiry responses, lives at `corpus/pm-frameworks/`.

**Downstream (hands off to these for execution):**
- `rz-graphic-design`. Triggered when speaker one-sheet styling is needed (`corpus/brand-system/`).
- `rz-networking-hand-curated-import`. Triggered when a Sales Nav CSV import is part of the workflow.

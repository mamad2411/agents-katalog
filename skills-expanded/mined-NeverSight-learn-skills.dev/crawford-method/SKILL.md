---
name: crawford-method
description: >
  Write cold emails using the Crawford Method — the list IS the message, built on tension
  heuristics from public data, then delivered as PQS (pain-qualified) or PVP (permissionless
  value) copy. Use when designing the targeting + message together, finding the "tension triangle"
  for a segment, choosing PQS vs PVP, or writing data-driven emails that describe the buyer's
  situation. Triggers on "Crawford method", "tension triangle", "PVP", "PQS", "permissionless
  value", "list is the message", "data-driven email", "7-component email", "write backwards from
  the message". Do NOT use for subject-line/CTA mechanics alone (see cold-email-copy), campaign
   operations (see campaign-delivery), or signal sourcing (see signal-detection).
---

# The Crawford Method

> "The list is the message. If you have a good list, you have a good message."

Targeting IS messaging. Build the list on data heuristics that reflect the buyer's real
situation, then describe that situation back to them. This skill is methodology; it sources its
tension heuristics from ColdIQ endpoints (see callouts) but writes no API calls of its own.

## Two message types

- **PQS — Pain-Qualified Segment:** 2–5 public heuristics identify prospects in the same painful
  situation as an existing customer; tell the story of how your customers navigated it. Formula:
  name the obvious choice → why your customers made the non-obvious choice → the benefit.
- **PVP — Permissionless Value Prop (always superior):** synthesize 3–5 public data sources into a
  non-obvious insight that is independently valuable. **Acid test:** would the recipient pay to
  receive this even if they never buy? If yes → PVP. Use PVP whenever you can.

## The Tension Triangle

Tension = a specific, data-provable, time-bound situation that makes them need you NOW. Not a
single signal — multiple data points pulling against each other.

- **Heuristic 1** — a unique, data-provable characteristic
- **Heuristic 2** — a second characteristic that PULLS AGAINST the first
- **Growth amplifier** — funding / headcount / revenue growth that increases the pull
- **Existential data point** — the metric that separates good-fit from bad-fit (sweet-spot range)

Source these heuristics from public data via ColdIQ:
→ **GET** `/v1/signalbase/funding-signals` · ? cr · `signalbase.funding_signals` (unverified) — funding amplifier
→ **POST** `/v1/limadata/jobs` · 2 cr · `limadata.jobs` — hiring / no-SDR heuristics
→ **POST** `/v1/limadata/research/ai-search` · 0.3 cr · `limadata.research.ai_search` — filings, regulation, public events
→ **POST** `/v1/limadata/enrich/company` · 1 cr · `limadata.enrich.company` — growth, tech, firmographic heuristics

## 7-component email architecture

1. **Visceral emotional opening** — a moment they've physically felt, not a fact.
2. **Connection to existing behavior** — frame the offer as an extension of what they already do.
3. **The insight (contrarian)** — "Most people think X, but it turns out Y." Must pass the
   recognition + articulation tests.
4. **Social proof / authority (light)** — one line, founder credentials not company stats.
5. **Information gap** — enough to create curiosity, never enough to answer everything.
6. **Qualification as disqualification** — a threshold that excludes non-fits.
7. **Soft CTA (ask for truth, not time)** — "Am I close, or is it different at {{companyName}}?"
   NEVER "Do you have 15 minutes?" / "Book a time."

## 11 rules (condensed)

Never mention your product in step 1 · write about their situation not your solution · target on
events not roles · use Cialdini systematically · create information gaps · use their language ·
sell against incumbent behavior not competitors · acknowledge multiple solutions exist · one
perfect email > ten mediocre · data-driven > surface personalization · quantify the meeting in dollars.

## Gold-standard example (PVP — Texada)

```
Earl, your CAT 365 excavator seems to be not on the move right now.
They just filed a large construction project for 123 Main Street — half a mile from you.
AI says it'll likely need your tool for ~six weeks.
Public rental rates put that at about a $170,000 job.
Here's the foreman, their email, their phone. Hope this was useful.
```
Independently valuable, no product mention, three public sources synthesized, quantified — the
message IS the demo.

## The process (zero → finished email)

1. Understand best customers (call transcripts: what was their situation when they bought?).
2. Extract tension (H1, H2, growth amplifier, existential data point).
3. Find the data sources — can you get the heuristics programmatically? (filings, jobs, tech,
   ad libraries, funding — source via the ColdIQ endpoints above).
4. Build the list on tension, NOT firmographics.
5. Write backwards: define the perfect message, then find the data that makes it true.
6. Choose PQS or PVP. 7. Apply the 7-component architecture. 8. Run the quality checklist.

## Anti-patterns

"I noticed" openings · "companies like yours" · "do you have 15 minutes" · features dump ·
surface personalization (location, mutual connections, LinkedIn posts) · horizontal targeting ·
over-sequencing (max 2–3 touches, each adding new information).

---
name: feature-gap-analysis
description: "Identify and prioritize feature gaps between your product and competitors. Not just what's missing but which gaps matter, which don't, and which you should intentionally keep. Use when losing deals to missing features, planning roadmap with competitive context, or evaluating build-buy-partner decisions."
---

# Feature Gap Analysis

Identify which competitive feature gaps matter, which don't, and which should stay gaps.

## How to use

- `/feature-gap-analysis` Apply gap analysis constraints to this conversation.
- `/feature-gap-analysis <competitors>` Analyze gaps against named competitors.

## Constraints

### Feature Landscape
- Map every feature across three layers: must-have (table stakes), differentiating (changes deal outcomes), and nice-to-have (sounds impressive, rarely drives decisions)
- For each feature: Do we have it? (Yes / Partial / No / Planned) vs. each competitor
- MUST track how often each gap comes up in sales and support conversations

### Gap Scoring
Score each missing feature on four dimensions:
- Customer demand (1-5): how often do customers ask for this?
- Revenue impact (1-5): does this gap cost you deals?
- Strategic importance (1-5): does this affect your positioning?
- Build effort (1-5, inverted — 5 means easy to build)
- Priority Score = (Demand + Revenue + Strategy) × Effort ÷ 3

### Gap Classification
Every gap MUST go into one of four buckets:
- Close it: high priority, clear demand, reasonable effort. Put on the roadmap.
- Leapfrog it: don't match — build something better. Turn weakness into strength.
- Acknowledge it: not worth closing, but you need a story for when it comes up.
- Ignore it: low demand, low impact, high effort. Don't waste time.
- MUST explicitly classify. No ambiguous "maybe later" bucket.

### Segment Mapping
- MUST map each gap to customer segments. A gap critical for Segment A may be irrelevant to Segment B.
- NEVER build for a segment you're not targeting just because a competitor has it
- If a gap only matters to a segment you don't serve, it's not actually your gap

### Intentional Gaps
- Some gaps SHOULD stay gaps. Missing a feature that adds complexity can be an advantage.
- MUST document intentional gaps with reasoning
- Simplicity is a feature. Focus is a feature.

### Anti-Patterns
- Building everything competitors have without asking if your users need it
- Treating all gaps as equal priority
- Never acknowledging gaps to the sales team, forcing them to improvise
- Confusing "they have it" with "our customers need it"

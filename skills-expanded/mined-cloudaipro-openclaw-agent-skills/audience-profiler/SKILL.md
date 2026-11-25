---
name: audience-profiler
description: Audience intelligence analyst for deriving segmentation, persona profiles, and decision-journey insights from brand and product context. Use when users request market targeting, buyer persona definition, or messaging-angle analysis.
---

# Audience Profiler

## Objective
Produce segmentation and persona outputs that directly inform positioning and messaging decisions.

## Trigger Rules
Use when market audience understanding is the main request.

Positive cues:
- "Who is our target customer?"
- "Build personas for this product."
- "Analyze buyer journey and messaging angles."

Do not use when:
- User asks only for ad visuals.
- User asks only for day planning.
- User asks only for task prioritization.

## Inputs
Required:
- Product or offer context.
- Value proposition.

Optional:
- Price point.
- Market or region.
- Existing customer signals.

## Output Schema
Return universal envelope from `../shared/references/output-schemas.md`.

Artifacts order:
1. Audience insight brief.
2. Segment and persona table.
3. Decision journey and messaging plan.
4. Validation checklist.

## Workflow
1. Extract value proposition and adoption friction.
2. Build segments by motivation and constraints.
3. Create personas with pain points and buying triggers.
4. Map awareness-to-conversion journey.
5. Propose messaging angles and channel implications.

## Quality Bar
- Personas must be behavior-based, not demographic-only.
- Segments must be distinct and actionable.
- Journey stages must include measurable next actions.

## Safety Rules
- Avoid discriminatory profiling.
- Mark inferred data as assumptions.
- Avoid fabricated market statistics.

## Resources
- Domain framework: `references/domain.md`
- Envelope validator: `scripts/validate_output.py`
- Operations artifact validator: `scripts/validate_operations_artifacts.py`

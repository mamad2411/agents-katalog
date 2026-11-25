---
name: customer-insight-synthesizer
description: Synthesize patterns across multiple interviews, calls, reviews, surveys, or support messages into evidence-backed needs, language, objections, and actions.
---

# Customer Insight Synthesizer

Turn a body of customer evidence into decisions without flattening individual voices or inventing consensus.

## Job contract

- Owns: patterns across multiple customer sources.
- Does not own: one meeting, a single-customer story, or general market research without customer evidence.
- Required evidence: at least two customer items or one source containing multiple distinct responses.
- Finished deliverable: insight report with evidence, confidence, tensions, and recommended moves.

## Choose a mode

- `Interviews and calls`: transcripts or call notes.
- `Reviews and responses`: surveys, reviews, support messages, comments, or forms.
- `Mixed evidence`: combines different source types while preserving their provenance.

If only one meeting is supplied, route to `meeting-miner`. If the requested output is a customer success story, route to `case-study-builder`.

## Workflow

1. Inventory the sources, dates, customer types, and known outcomes.
2. Separate direct evidence from the user's interpretation.
3. Tag recurring jobs, desired outcomes, objections, triggers, alternatives, and exact language.
4. Count source coverage, not repeated mentions from one unusually vocal customer.
5. Look for contradictions and meaningful minority views.
6. Translate supported patterns into messaging, offer, product, service, or research moves.
7. Mark confidence as high, medium, or low and explain why.

## Output

```markdown
# Customer Insight Report

## Evidence Reviewed
[Sources, customer groups, limits]

## Strongest Patterns
### [Pattern]
- Evidence: [source references and short quotes where available]
- Coverage: [how broadly it appeared]
- Confidence: [high / medium / low]
- Why it matters: [business consequence]

## Customer Language Worth Reusing
[Exact short phrases with source labels]

## Objections And Friction
[What delays, confuses, or stops action]

## Tensions And Minority Views
[Contradictions that should not be averaged away]

## Recommended Moves
1. [Specific move tied to evidence]

## What To Learn Next
[Smallest useful next research question]
```

## Guardrails

- Never invent quotes, counts, identities, outcomes, or customer intent.
- Do not call a pattern strong when it comes from one source.
- Redact unnecessary personal information from the report.
- Keep source labels so every conclusion can be checked.

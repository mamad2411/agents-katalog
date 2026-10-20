---
name: customer-feedback-synthesis
description: Use when converting support tickets, UX findings, product signals, and user research into prioritised, roadmap-ready insights with explicit source traceability.
---

# Customer Feedback Synthesis

## Specialization

Collect feedback signals from multiple sources — support tickets, usability findings, NPS or satisfaction data, user interviews, analytics — and synthesise them into a prioritised insight set with source traceability and roadmap-ready recommendations.

This skill sits at the intersection of UX, Product Management, and Support disciplines. It does not produce the original research (that belongs to UX research workflows) or own backlog prioritisation (that belongs to `product-scope-slicing`) — it converts raw signals into structured, evidence-backed insights that those assets can act on.

## Trigger Conditions

- Feedback from multiple channels needs to be consolidated before a planning or design decision.
- A release or increment has shipped and user response signals need to be captured and prioritised.
- A product review, roadmap update, or UX iteration cycle requires evidence-grounded input.
- Support ticket volume is rising and the root themes need to be surfaced for product or design action.
- Discovery is about to start and existing user feedback should inform its framing.

## Inputs

- Feedback source list: specify each source type and volume (e.g., 120 support tickets, 3 usability session recordings, 2 NPS comment exports).
- Time window: the period the feedback covers.
- Product or feature context: what is being evaluated.
- Known hypotheses or priority questions the synthesis should test.
- Originating plan or workstream ID for traceability.

## Required Outputs

| Output | Description |
|---|---|
| Signal inventory | Structured list of raw signals by source type, count, and date range. Confirms what was and was not included. |
| Theme map | Clustered themes extracted from signals. Each theme: name, signal count, representative examples (2–3), and frequency rank. |
| Priority insight list | Ranked insights with evidence strength (High / Medium / Low) and recommended action type (Fix, Investigate, Design, Monitor). |
| Roadmap input note | One synthesised paragraph per high-priority insight explaining the user impact, evidence basis, and recommended next step for planning. |
| Source traceability log | Reference from each insight back to the source signal(s) that support it. Required for audit and challenge resolution. |

## Workflow

1. Confirm the feedback source list, time window, and product context. Record what was excluded and why.
2. Build the signal inventory: count signals by source and confirm date coverage.
3. Cluster signals into themes: group by symptom, user goal, or failure type. Label each theme and count supporting signals.
4. Rank themes by frequency and severity. Apply severity weighting: blocking issues rank above frustrations even at lower volume.
5. Convert top themes into priority insights. Assign evidence strength based on signal volume, source diversity, and consistency.
6. Write roadmap input notes for every High evidence-strength insight.
7. Build the source traceability log: for each insight, list at least two source references.
8. Record the originating plan or workstream ID on the output artifact.

## Evidence Strength Classification

| Strength | Criteria |
|---|---|
| High | Three or more independent source types agree; signal volume is consistent over time. |
| Medium | Two source types agree or one source type with high volume and consistency. |
| Low | Single source, low volume, or ambiguous signals that could have multiple interpretations. |

## Done Criteria

- Signal inventory covers all stated sources with counts and date ranges.
- Theme map has at least three themes (or states explicitly that fewer were found).
- Priority insight list covers all High evidence-strength themes.
- Every High insight has a roadmap input note.
- Source traceability log links each insight to at least two source references.
- Originating plan or workstream ID is on the output.

## Guardrails

- Do not present a single-source signal as a High evidence-strength insight.
- Do not include unverified anecdotes from memory or verbal briefings as primary sources — only documented signals qualify.
- Do not prescribe solutions in the insight; describe the user problem and recommended action type, leaving solution design to the appropriate specialist.

## References

- Related skills: `analysis-execution`, `product-scope-slicing`, `design-web-ux`, `design-mobile-ux`, `operability-design`

## Execution Context

### Input Context

- Request objective and scope boundary.
- Applicable constraints and required outputs.

### Process Context

- Follow this skill's deterministic workflow from intake to closure.
- Record ownership and decisions for required outputs.

### Output Context

- Deliverables with explicit completion status.
- Residual risks and next actions.
## References Assets

- [Reference assets](./references/README.md)

---
name: anomaly-triage
description: Investigate a cost anomaly end-to-end. Triggers on phrases like "cost spike", "unexpected spend", "anomaly", "what's driving this cost". Pulls billing data, identifies the top contributing SKUs/projects/labels, drafts a hypothesis about cause, and produces both the engineering Slack message and the CFO digest paragraph in house style.
---

# Anomaly Triage

When invoked, walk the practitioner through a structured cost anomaly investigation and produce the stakeholder communications. This skill exists so anomalies are investigated and communicated the same way every time, regardless of who's on call.

## Inputs to confirm before starting

If any of these are missing, ask before proceeding:

- The service or product where the anomaly was detected (e.g., BigQuery, GKE, Datadog)
- The dollar delta or expected vs. actual spend
- The time window (start and end dates)
- The affected account, project, team, or cost center, if known
- Any deployments, feature launches, or known events in that window

## Steps

1. **Pull the breakdown.** Query the billing export for the affected service over the anomaly window, broken down by SKU, project, label, and (where relevant) API operation. Compare to the equivalent period one week prior.

2. **Identify the top contributors.** Surface the top 3–5 line items that account for the bulk of the delta. For each, note:
   - The dollar amount and percentage of the total delta
   - Whether it's a new line item or a magnitude change on an existing one
   - The most likely owning team or project (best guess from labels/creators)

3. **Form a hypothesis.** Based on the contributors and any deployment context, draft one or two candidate explanations. Phrase them as hypotheses to test, not conclusions.

4. **Generate communications.** Produce both pieces below.

5. **Run the skeptic check.** Before delivering, ask: what assumptions did we make? What might be wrong? What additional data would change the recommendation? Append the answer below the communications so the practitioner sees it before sending.

## Communications — house style

### Engineering Slack message (4 sentences max)

For the channel of the team that likely owns the spike (`#data-eng`, `#platform`, etc.). Peer tone, no acronym-explaining. Must include:

- The anomaly in numbers (one sentence)
- Suspected cause (one sentence)
- One specific ask (review query plan / confirm intentional / investigate)
- When you'll follow up

End with one follow-up question the channel is likely to ask but the message hasn't pre-empted.

### CFO weekly digest (one paragraph)

Lead with dollar impact. No service names if the audience won't recognize them. Include:

- What's been done to investigate
- Resolution timeline
- One sentence on whether this changes the monthly forecast

End with one follow-up question Finance is likely to ask but the paragraph hasn't pre-empted.

## Output format

Always produce in this order:

```
## Top contributors
[bulleted list with dollar amounts and likely owners]

## Hypothesis
[one or two candidate explanations]

## Slack message — #channel-name
[the message]

## CFO digest paragraph
[the paragraph]

## Skeptic check
- Assumptions made: ...
- What might be wrong: ...
- What additional data would help: ...
```

## Customization notes

- Default time window: 7 days, comparing to the prior 7. Override if the user specifies.
- If the billing export query returns nothing, do not fabricate numbers. Tell the user the query came back empty and ask for the right table or window.
- If the user has connected an MCP for their billing data, prefer that over assuming the standard table name.

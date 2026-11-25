---
name: feedback-themes
description: Use this skill to extract the three customer-feedback themes worth escalating from a large batch of unstructured signal (support tickets, app store reviews, customer Slack channels, NPS comments, sales call transcripts). Triggers on phrases like "feedback themes for [period]", "what are customers saying", "extract the patterns from these tickets", or when the user shares a batch of customer signal data. Filters for action, not for completeness.
---

# Customer Feedback Theme Extractor

## When to use this skill

The user has hundreds or thousands of pieces of customer feedback. They want to know what to do about it. Most analytics tools produce 30 themes, which is too many to act on. This skill is calibrated to produce three patterns worth escalating, with the rest filtered down to noise.

## Input the user provides

- The feedback batch (tickets, reviews, NPS comments, call transcripts, channel messages)
- Time window covered
- Optionally: customer segment context (who the high-value customers are)
- Optionally: known recent product changes or incidents that might explain spikes

## What this skill does

1. Reads through the entire batch
2. Classifies by theme, severity, customer segment, and frequency
3. Distinguishes loud-minority complaints from silent-majority signal
4. Identifies regressions vs. ongoing patterns vs. one-off events
5. Selects the three themes worth escalating, leaving the rest in a "background noise" section
6. Produces a one-page customer signal report

## Output structure

```
# Customer Signal Report: [Time window]
*Batch size: [n items]. Customer segments represented: [list].*

## The three themes worth escalating
These are the three patterns where action would create the most value. Other themes exist; these are the three.

### Theme 1: [Specific issue or request]
- Volume: [n items, % of batch]
- Segment skew: [where these customers cluster]
- Severity: [revenue at risk / churn signal / satisfaction degradation / opportunity]
- Representative quote: "[customer phrase]"
- Recommended action: [specific, concrete]
- Owner: [who should pick this up]

### Theme 2: [Same structure]

### Theme 3: [Same structure]

## Background noise (themes we are NOT escalating, and why)
- [Theme A]: high volume but low severity, no action recommended
- [Theme B]: low volume but coming from one loud customer, do not generalize
- [Theme C]: legacy issue already in the backlog, no new signal here
- [Theme D]: one-off event, no pattern

## Regressions vs. ongoing
- New themes that did not exist last period: [list]
- Themes that have grown in volume vs. last period: [list with % change]
- Themes that have decreased: [list]

## Customer voice highlights
3-5 direct quotes worth circulating internally. Real customer language is more persuasive than aggregate themes.
```

## Calibration notes

- The selection of three themes is the highest-leverage decision. Resist the urge to expand to four or five. Three forces real prioritization.
- Volume alone is not severity. A high-volume complaint from low-value customers may rank below a low-volume complaint from your top 20 accounts.
- Distinguish "customers want X" (preference) from "customers cannot do their job without X" (functional gap). The second category outranks the first.
- For each theme, the recommended action must be specific enough that someone could start work on it Monday morning. "Improve onboarding" is not an action. "Reduce time-to-first-value in step 4 of onboarding by removing the API key requirement" is.
- The "background noise" section is important. It tells leadership what is being filtered out and why. Without it, the report can read as cherry-picking.

## Bias awareness

When classifying themes, watch for:
- Over-weighting articulate customers (who write more) vs. silent customers (who churn quietly)
- Anchoring on themes that match leadership's existing hypothesis
- Conflating different customer segments into one theme
- Treating a single very large customer as a "theme" rather than a single account issue

## When NOT to use this skill

- Single customer feedback (use a different account-management workflow)
- Pre-launch beta feedback where themes are emerging too fast to stabilize
- Quantitative survey data (different analytical lens)

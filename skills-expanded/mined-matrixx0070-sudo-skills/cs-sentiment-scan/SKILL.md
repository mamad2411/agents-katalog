---
name: cs-sentiment-scan
version: 1.0.0
description: Cluster a batch of tickets or feedback into themes with sentiment, size each by frequency x severity x trend, and produce a ranked "fix these 3" list.
author: matrixx0070
tags: [customer-support, sentiment, feedback, analytics, prioritization, themes]
capabilities: []
---

## When to use

Use this when you have a pile of tickets, reviews, survey responses, or chat logs and need to know what customers actually feel and what to fix first. Turn noise into a short, ranked action list.

**Not for:** a single ticket (cs-ticket-triage or cs-draft-response), formal statistical analysis, or batches too small to trend (under ~10 items — just read them). If the batch spans unrelated products, split it first.

## Method

1. Read the full batch before categorizing. Record volume and time window so trends mean something ("40 tickets, last 7 days").
2. Cluster by underlying problem, not wording — "can't find export," "export button hidden," and "where is download" are one theme.
3. Tag each item's sentiment (Positive / Neutral / Negative / Angry) and intensity. Capture a representative verbatim quote per theme — real words carry weight.
4. Size each theme: frequency (count), severity (blocked vs. annoyed), trend (rising/steady/falling). Flag account-value or churn signals.
5. Rank by frequency x severity x trend. **Decision point:** separate quick wins (cheap, high relief) from deeper investments so a rising cheap fix isn't buried under a large slow one.
6. Produce "fix these 3" — the three highest-leverage actions, each with theme, evidence, expected impact, and suggested owner. Note positives worth reinforcing.

## Example

> **Scope:** 62 tickets, last 14 days.
> **Top theme:** "Export is confusing" — 18 mentions, Negative, rising. Quote: "I spent 10 minutes hunting for the download button."
> **Fix these 3:** 1) Relabel/move export button (18 tickets, Negative→rising) → expected -25% export tickets → @design. 2) ... 3) ...
> **Quick win:** button relabel (1-day change). **Bigger bet:** export pipeline rework.

## Pitfalls

- Clustering by surface wording — you split one real problem into three weak themes.
- Reporting counts with no time window — trend claims become meaningless.
- Ranking by raw volume alone — a small rising churn signal can outrank a large stable annoyance.
- Paraphrasing away the verbatim quotes — real customer words move stakeholders; summaries don't.

## Output format

```
Scope: <volume + time window>
Themes:
  | theme | count | sentiment | trend | sample quote |
Fix these 3:
  1. <action> — evidence: <...> — expected impact: <...> — owner: <@name>
Quick wins vs. bigger bets: <split>
What's working: <positive signals to keep>
```

---
name: yt-analytics
description: >-
  Analyze YouTube Studio data for Shorts or long-form videos, distinguish
  traffic surfaces, and identify evidence-backed performance hypotheses.
  Use for "read my analytics", "which video worked", "my views dropped",
  "what's my CTR telling me", or a pasted Studio export.
---

# yt-analytics

Read the [shared operating guide](../yt/references/operating-guide.md) for profile lookup, helper paths,
capability limits, and cross-skill routing before using this workflow.

Start by identifying the format, traffic sources, publication age, and comparable channel baseline.
A low view count alone cannot tell you whether the cause was topic, packaging, retention, or timing.
Do not apply long-form CTR thresholds to Shorts-feed views.

## Long-form Browse or Search analysis

```bash
python3 "$YT_SKILL_DIR/funnel.py" --impressions 42000 --ctr 3.1 --avd 2:10 --length 9:40
python3 "$YT_SKILL_DIR/funnel.py" stats.csv
```

Use impressions, impression click-through rate, average view duration, and actual video length.
An Overview export may lack runtime or traffic-source detail; obtain the missing fields rather than
substituting watch time, views, or AVD for them. Inspect the output for incomplete inputs.

The helper's bands suggest what to inspect first, not a proven single cause:
- **Limited impressions:** compare video age, topic demand, traffic source, and the channel's prior
  comparable uploads. [$yt-idea](../yt-idea/SKILL.md) can help test a topic hypothesis.
- **Low CTR for the same surface:** examine the title/thumbnail promise together through
  [$yt-package](../yt-package/SKILL.md) and [$yt-thumbnail](../yt-thumbnail/SKILL.md).
- **Weak retention for comparable videos:** examine the curve and footage using
  [$yt-retention](../yt-retention/SKILL.md), rather than assuming a title rewrite fixes it.

## Shorts-feed analysis

```bash
python3 "$YT_SKILL_DIR/funnel.py" shorts.csv --format shorts
```

Use the Shorts mode to keep the long-form funnel heuristic out of the report. Assess available
**shown in feed**, **stayed to watch / viewed versus swiped away**, **engaged views**, average view
duration, average percentage viewed, retention curve, and repeat viewing. Note which metrics are
missing and each denominator. Distinguish raw Shorts starts/replays from engaged views; do not
compare raw view totals across a metric-definition change without accounting for it.

If feed exposure is limited, gather more evidence before blaming SEO or posting frequency. If
viewers swipe away early, inspect the first frame and opening promise. If they stay but leave
before the payoff, inspect pacing and payoff timing. Loops can produce percentage viewed above
100%; this is not automatically an error. Search/Browse packaging may matter for those surfaces,
but is not an explanation for Shorts-feed performance by itself.

## What to hand back

- A compact metric table with format, source, date range, sample size, and missing inputs.
- The best-supported hypothesis, evidence for it, and important alternative explanations.
- One practical experiment and what metric would support or reject it.
- For a batch, compare like-for-like cohorts rather than ranking by lifetime views alone.

Use a channel-specific baseline when available. Built-in CTR/APV thresholds are illustrative;
never promise that the suggested change will increase distribution or guarantee views.

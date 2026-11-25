---
name: survey-design
description: Design unbiased survey instruments — question order, wording, scales (Likert, NPS, SUS), sampling and analysis reporting — to measure attitudes at scale. Use when you need quantitative breadth on user needs or satisfaction, or to quantify qualitative findings. Not for discovering unknown problems (that is interview research) and not for behavioural experiments.
license: MIT license
category: docs
metadata: {"version": "1.0", "skill-author": "MC Dean (designer-skills)"}
---

# Survey Design

Design surveys that produce reliable, actionable data rather than noise. 中文触发：问卷设计、用研量表、
NPS/SUS 计算、样本量估算。

## When a survey is the right instrument
Use surveys to measure prevalence, frequency and attitude at scale:
- How many users share a need, problem or opinion (not merely whether some do)
- Quantify or validate findings from interviews and usability tests
- Measure change over time (satisfaction scores, NPS trends)
- Cover a representative sample of a population segment

Do not use a survey to discover problems you do not yet know exist — interviews explore and reveal,
surveys confirm and quantify.

## Structure

### Introduction
- State the purpose: "We're improving [X] and want to hear your experience."
- State the time required: "This takes about 3 minutes."
- State anonymity/confidentiality where applicable
- No leading pre-framing of what the "right" answers are

### Question order
1. Screen and demographic questions (if needed) — short, at the start
2. Behavioural questions (what users do) — before attitudinal ones
3. Attitudinal/satisfaction questions — after behavioural context is established
4. Open-ended questions — at the end; they cost the most effort

### Closing
Thank participants; optionally offer a route to follow-up.

## Question types

| Type | Use for | Caution |
|---|---|---|
| Single choice (radio) | Mutually exclusive options | Options must be exhaustive; include "Other" |
| Multi-select | Several applicable answers | Not for ranking; not for exclusive options |
| Likert scale | Attitudes, agreement, satisfaction | Consistent direction (1=low, 5=high); label both ends |
| Rating scale (1–10, NPS) | One-dimension measurement | State what each end means |
| Ranking | Relative importance | Limit to 5–7 items; cognitively expensive |
| Open text | Explanation, surprises | Use sparingly; expensive to analyse |

## Question writing

Avoid:
- **Leading**: "How much do you enjoy using our product?" → "How would you describe your experience?"
- **Double-barrelled**: "How easy and enjoyable is checkout?" → split it
- **Loaded language**: "How satisfied are you with our fast shipping?" → drop "fast"
- **Recall overload**: "In the past 12 months, how many times…" → shorten the recall window
- **Jargon**: use the words users use, not internal product names

Do instead: one question per question; behaviourally grounded wording; mutually exclusive and
collectively exhaustive options; neutral phrasing.

## Scales

### Likert
- 5-point and 7-point are both defensible; 5-point is easier for respondents
- Keep a midpoint unless the question is genuinely binary
- Always label endpoints: "1 = Strongly disagree, 5 = Strongly agree"
- One direction across the whole survey

### NPS
- 0–10: "How likely are you to recommend [product] to a friend or colleague?"
- Promoters 9–10, Passives 7–8, Detractors 0–6; **NPS = %Promoters − %Detractors**
- One comparable metric — not a complete satisfaction measure

### SUS
- Validated 10-question instrument for perceived usability
- Score 0–100; **68 is the average, above 80 is good**
- Use verbatim; do not reword the items

## Sampling
- **Sample size**: ~385 responses gives ±5% margin of error at 95% confidence in a large population
- **Representativeness**: match the demographic profile of the studied population
- **Non-response bias**: respondents differ from non-respondents; state this limitation
- **Fatigue**: keep it under 5 minutes; quality drops sharply beyond 10–15 questions

## Analysing and reporting
- Report mean, median and distribution — not "most people said X"
- Likert data: show the full distribution, not only the average
- Code open text into themes; report the top themes with example quotes
- Cross-tabulate by segment when segments differ (new vs returning, mobile vs desktop)
- Report response rate and sample size beside every finding

## Working rules
- Pilot with 3–5 people before sending; cognitive pretesting reveals confusing questions
- Every added question lowers completion and data quality
- Write the analysis plan before the questions: "what decision will this answer?"
- Pair with qualitative work: surveys tell you what and how many, interviews tell you why

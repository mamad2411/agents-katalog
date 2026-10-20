---
name: claude-revenue-system-45-agents
description: The six-column "Claude Revenue System" infographic variant (45 named agent roles in Discover and Identify, Engage and Outreach, Qualify and Convert, Grow and Expand, Manage and Optimize, Enable and Operate, ending with a "comment CLAUDE for free access" hook) - how it differs from the 58-agent version already in this repo, where its list repeats roles, and how to turn a role into a prompt. Use when picking a role for a sales or revenue task or comparing the two versions.
---

# Claude Revenue System, 45-role version

Source: a "Claude Revenue System: The Complete AI-Powered Revenue System" infographic with the call to action "Comment CLAUDE for free access". It is a list of role names, not prompts. The repo already has `claude-revenue-system-58-agents` (a different layout of the same idea). Text was read at small size from an 800 px image; read it as approximate.

| Column | Roles shown (numbers as printed) |
|---|---|
| 01 Discover and identify | 01 Total Addressable Market Mapper; 02 Ideal Customer Profile Builder; 03 Account Intelligence Agent; 04 Buying Signal Detector; 05 Prospect List Builder and Scorer; 06 Champion Identifier; 07 Trigger Event Outreach Agent; 08 Referral Pipeline Builder; 09 Inbound Lead Qualifier; 10 Pipeline Gap Analyser |
| 11 Engage and outreach | 11 Hyper-Personalised Email Writer; 12 Multi-Touch Sequence Builder; 13 LinkedIn Outreach Agent; 14 Cold Calling Script Builder; 15 Video Prospecting Script Writer; 16 Re-engagement Sequence Builder; 17 Outreach Reply Handler; 18 A/B Test Variant Generator |
| 19 Qualify and convert | 19 Executive Forecast Writer; 20 Competitor Displacement Agent; 21 Discovery Call Preparation Agent; 22 MEDDIC/MEDDPICC Qualification Agent; 23 Business Case Builder; 24 Win/Loss Analysis Agent; 25 Customer Success Plan Builder |
| 26 Grow and expand | 26 Pipeline Review Agent; 27 Account Health Monitor; 28 Churn Risk Identifier; 29 Expansion Revenue Identifier; 30 QBR Preparation Agent; 31 Renewal Preparation Agent |
| 32 Manage and optimize | 32 Sales Tech Stack Audit Agent; 33 Escalation Recovery Agent; 34 Executive Relationship Builder; 35 Investor Revenue Narrative Builder; 36 Account Health Monitor; 37 Churn Risk Identifier |
| 38 Enable and operate | 38 Expansion Revenue Identifier; 39 QBR Preparation Agent; 40 Renewal Preparation Agent; 41 Customer Feedback to Revenue Insight Agent; 42 NPS Response Agent; 43 Executive Relationship Builder; 44 Sales Playbook Builder; 45 Rep Performance Coach |

## What to notice [Likely]

- **Repeats:** Account Health Monitor, Churn Risk Identifier, Expansion Revenue Identifier, QBR Preparation Agent, Renewal Preparation Agent and Executive Relationship Builder each appear twice, so there are fewer than 45 distinct roles. The 58-agent version names different roles; neither list is a tested system.
- **No evidence:** roles are job titles. Whether an AI agent does each one well depends on your data, prompts and review.
- **The hook:** "comment for free access" is lead generation for the poster; nothing was requested or followed up.

## Turn a role into a prompt

```
Act as the [ROLE] from the Claude Revenue System. Input: [PASTE ACCOUNT NOTES, CRM EXPORT OR EMAIL THREAD]. Produce [DELIVERABLE] in [FORMAT]. List what you assumed, what is missing, and what I must verify before using it. Do not contact anyone.
```

Use `/revenue-agent-pick`. Related: `outbound-sales-system-5stage`, `gtm-outbound-engine`.

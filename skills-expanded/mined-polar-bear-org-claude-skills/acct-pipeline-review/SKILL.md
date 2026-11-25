---
name: acct-pipeline-review
description: Prepares your pipeline review with each deal placed at the stage its evidence supports, the exit criterion written, the gaps per deal, the deals with no movement, one action per deal or "take out" and the three deals to push this week. Use for "run acct-pipeline-review", "pipeline review", "review my pipeline", "clean up my pipeline", "pipeline inspection", "which deals should I take out", "qualify my open deals", "prepare my pipeline call", part of the Claude for Account Executives Pack by 90n.
---

# Pipeline Review

## When To Use
Your pipeline fills with deals nobody dares take out. CRM stages reflect hope more than facts, and the review with your manager becomes a trade of impressions. Run this weekly. It answers: for each deal, what is proven in writing, what is missing, and which action moves it forward or out?

## When Not To Use
To commit amounts for the period, run Sales Forecast. For quiet deals you need to write to, use Stalled Deals Review. To go deep on one deal, run MEDDPICC Qualification. This review does not plan your week: Weekly Sales Plan takes its three deals.

## Inputs
- Your pipeline export: deal, stage, amount, close date, last activity. Salesforce in Claude (beta) reads it directly; any CRM works by export or copy and paste.
- Your recent call notes per deal: these are the written evidence.
- Your stages and their exit criteria, if your company has them.
If you have none of this, I start from a list of your deals with their stage, ask you to write one exit criterion per stage, and mark the output as a first draft.

## Approach
Stages with written exit criteria are common practice, described generically: a deal leaves a stage when the customer has done something you can check, not when you sent something. For large deals the gaps are read with MEDDPICC, created inside PTC in 1996 (meddicc.com). A stage with no evidence is a wish. The review looks for written proof, not intuition, and it assesses deals: never the buyer, never the seller.

## Workflow
1. I ask at most three questions: what are your stages and their exit criteria, above which amount or cycle length does a deal get the MEDDPICC read, and after how long with no movement is a deal stuck.
2. I write each stage's exit criterion as a customer action that can be checked (a meeting held with the signer, criteria shared in writing, a proposal walked through). You correct them once and keep them.
3. I place each deal at the stage its evidence supports, with the proof and its source. A gap with the CRM stage is flagged, not corrected for you, and a deal that moves back a stage is the review working.
4. For each large deal, the eight MEDDPICC letters, each "written proof" (with source), "assumed" or "unknown". Champion is a role in the decision shown by dated actions, not a judgment of a person.
5. No movement: deals with no change of stage or of evidence for the time you set.
6. One action per deal, with an owner and a date, or "take out". No health score, no percentage: evidence and gaps.
7. I name the three deals to push this week, each with the reason drawn from its evidence.

## Output Format
```markdown
# Pipeline Review
Review of [date] · Source: [CRM export of date] · Stuck after: [your threshold]
## Stages and exit criteria (yours)
1. [stage]: [customer action that can be checked]
## Deals by evidence
| Deal | CRM stage | Stage the evidence supports | Written proof (source) | Gap to close |
|---|---|---|---|---|
| [deal] | [stage] | [stage] | [proof, notes of date] | [gap] |
## Large deals: MEDDPICC letters
| Deal | Written proof | Assumed | Unknown |
|---|---|---|---|
| [deal] | [letters] | [letters] | [letters] |
## Actions
| Deal | No movement since | Action or "take out" | Owner | Date |
|---|---|---|---|---|
| [deal] | [date] | [action] | [name] | [date] |
## Three deals to push this week
1. [deal]: [reason drawn from the evidence]
## Decision
[Name] decides by [date] which deals come out of the pipeline and confirms the three to push.
```

## Done When
- Every deal sits at a stage supported by written proof, or the gap is flagged.
- Every letter is proven, assumed or unknown, never guessed.
- Every deal has a dated action with an owner, or reads "take out".
- The three deals to push are named with their reason.

## Quality Bar
- No deal score, no percentage, no comparison between sellers.
- Amounts and dates come from the CRM; I change none without your approval, and with Salesforce in Claude (beta) each write waits for it.
- Nothing describes a buyer's character: roles in the decision and dated words only.
- Taking a deal out is an honest decision, not a failure to hide.
- Deals are placed on written evidence, and nothing rates the buyer or the seller.

## Next
Run acct-sales-forecast (Sales Forecast) to place these deals in commit, best case or pipeline for the period.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).

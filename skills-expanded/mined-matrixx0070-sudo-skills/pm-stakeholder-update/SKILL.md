---
name: pm-stakeholder-update
version: 1.0.0
description: Write an audience-tailored stakeholder update — headline first, honest status, evidence sized to the reader, and a specific ask with owner and deadline.
author: matrixx0070
tags: [product, communication, stakeholders, reporting, updates, status]
capabilities: []
---

# Stakeholder Update

## When to use
Use this when you need to communicate progress, status, or a decision to a specific audience and want it framed for what they care about, not one generic memo forwarded to everyone.

**Not for:** the detailed spec engineers build from (use pm-write-spec), a public changelog or marketing announcement, or an internal decision doc that needs full options analysis. If you do not know who the reader is, define that first, audience drives everything here.

## Method
1. Identify the audience and their stake. **Decision point:** executives want outcomes/risk/asks; engineering wants scope/dependencies/tradeoffs; customers want value/timing/impact, pick one and tailor depth and vocabulary.
2. Lead with the headline: the single most important thing this reader needs, in the first line.
3. Report status honestly: on-track / at-risk / off-track with the reason. **Decision point:** if it is bad news, surface it early with a plan, never bury it.
4. Give evidence proportional to the audience: metrics and dates for execs, technical detail for engineers, concrete benefits for customers.
5. State the ask: a decision, resource, or unblock, each with owner and deadline. An update with no ask is often noise.
6. Keep it scannable and short.

## Example
Audience: executives. Headline: "Checkout redesign is at-risk for the March launch; need a payments-vendor decision by Friday." Status: at-risk, reason = vendor contract unsigned. Evidence: conversion in beta up 12%, but integration blocked. Ask: approve Stripe vs Adyen (owner: VP Eng) by Feb 28, else launch slips two weeks.

## Pitfalls
- Sending one generic update to execs, engineers, and customers, serving none of them.
- Burying "at-risk" three paragraphs down instead of leading with it.
- Reporting activity ("we had five meetings") instead of outcomes and status.
- Ending with no ask, so the reader does not know what you need from them.

## Output format
```
# Update: [subject] — for [audience] — [date]
Headline: one line.

Status: on-track / at-risk / off-track — reason.

## What shipped / what's next
- [audience-appropriate detail]

## Risks & mitigations
- [risk] → [mitigation]

## Asks
- [decision or help needed] — owner — by when
Targeted audience: [named]. Tone/length tuned accordingly.
```

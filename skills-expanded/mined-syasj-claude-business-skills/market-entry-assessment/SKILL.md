---
name: market-entry-assessment
description: "Test whether a new segment or geography deserves a real bet, using the user's evidence rather than a borrowed market-size slide. Use when the user mentions should we enter, new market, new segment, geographic expansion, or asks for a market entry assessment. Strategy and leadership skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: strategy
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'market-entry-assessment' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Market Entry Assessment

Test whether a new segment or geography deserves a real bet, using the user's evidence rather than a borrowed market-size slide.

## When to use this skill

Use this skill when the user:

- should we enter
- new market
- new segment
- geographic expansion
- market entry

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Strategy work recommends a direction. It does not guarantee market outcomes.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The segment definition
- Why now, in the user's words
- Access to the first customers
- Cost and constraint of a test

## Workflow


### 1. Define the segment

Who is in, who is out, and what problem they already spend time or money on. Vague 'SMBs' is not a segment.
### 2. Test access

How will you reach the first ten buyers? If the answer is 'marketing later,' the entry plan is not ready.
### 3. Estimate the cost of learning

Recommend a small test with a budget, a time box, and a kill metric. Do not build a full business case on invented TAM.
### 4. Name the adaptation

What must change in offer, pricing, support, or compliance. Flag legal and regulatory questions for a specialist rather than answering them.
### 5. Compare with the current bet

What existing work slows down if you enter. Opportunity cost belongs in the memo.
### 6. Recommend

Enter with a test, wait, or decline. One recommendation, with the fact that would change it.

## Output

Deliver a **market entry assessment**.

- Purpose of this market entry assessment, in two sentences.
- Facts the user supplied, listed separately from assumptions.
- The work itself, in the structure the workflow names.
- Open questions, risks, and the single next action with an owner.
- What a qualified reviewer still needs to confirm, if the domain is regulated.

## Quality bar

- Every number, date, name, and citation came from the user or is marked as an assumption.
- The artifact can be used without reading this skill again.
- Recommendations are specific enough that someone could accept or reject them.
- Boundaries were respected: no credentials requested, no unsupported professional claim, no deception.

## Example

### Scenario

Mara Chen, founder at Northline Studio in Calgary, needs a market entry assessment by 30 September 2026. A domestic software company asks whether to open a UK motion next quarter because two inbound leads arrived.

### Example data

```text
From: Mara Chen, founder
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

A domestic software company asks whether to open a UK motion next quarter because two inbound leads arrived.

The segment definition: Harbor & Co, recorded 14 September 2026. No supporting file attached
Why now, in the user's words: A domestic software company asks whether to open a UK motion next quarter because two inbound leads arrived
Access to the first customers: Bright Axle, last reviewed 14 September 2026. No owner named since
Cost and constraint of a test: CAD 36 direct. Overhead not in this line
```

### Example outcome

**Market entry assessment**
To: Mara Chen, founder, Northline Studio
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Defines the segment, prices a 90-day test, names the compliance questions for counsel, and does not treat two leads as a market.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The segment definition | Harbor & Co, recorded 14 September 2026. No supporting file attached | Needs confirmation |
| Why now, in the user's words | A domestic software company asks whether to open a UK motion next quarter because two inbound leads arrived | Carried into the draft |
| Access to the first customers | Bright Axle, last reviewed 14 September 2026. No owner named since | Carried into the draft |
| Cost and constraint of a test | CAD 36 direct. Overhead not in this line | Needs confirmation |

**How this draft was built**

**1. Define the segment**  
Who is in, who is out, and what problem they already spend time or money on. Vague 'SMBs' is not a segment.

**2. Test access**  
How will you reach the first ten buyers? If the answer is 'marketing later,' the entry plan is not ready.

**3. Estimate the cost of learning**  
Recommend a small test with a budget, a time box, and a kill metric. Do not build a full business case on invented TAM.

**4. Name the adaptation**  
What must change in offer, pricing, support, or compliance. Flag legal and regulatory questions for a specialist rather than answering them.

**5. Compare with the current bet**  
What existing work slows down if you enter. Opportunity cost belongs in the memo.

**Deliberately not done**
- Leading with a huge market-size number from memory.
- Treating a segment slide as permission to hire a full team.
- Ignoring regulatory or licensing questions by waving them away.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Mara Chen by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Leading with a huge market-size number from memory.
- Treating a segment slide as permission to hire a full team.
- Ignoring regulatory or licensing questions by waving them away.

## Related skills

- `strategic-plan-builder`
- `scenario-planning`
- `go-to-market-brief`

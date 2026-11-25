---
name: saas-weekly-metrics
description: "Read a weekly SaaS export and say what moved, without a benchmark from memory. Use when the user mentions SaaS metrics, weekly SaaS, MRR review, subscription metrics, or asks for a metrics note. SaaS skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: saas
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'saas-weekly-metrics' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# SaaS Weekly Metrics

Read a weekly SaaS export and say what moved, without a benchmark from memory.

## When to use this skill

Use this skill when the user:

- SaaS metrics
- weekly SaaS
- MRR review
- subscription metrics

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Do not invent churn, revenue, retention, or a security certification. If the export is missing, say so.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The export
- The definitions they use
- Last week's figures
- A metric that is missing

## Workflow


### 1. Step 1

Use their definitions.
### 2. Step 2

Show this week and last week from the export.
### 3. Step 3

A missing metric stays blank.
### 4. Step 4

Do not add a benchmark.
### 5. Step 5

Name the one move that matters.
### 6. Step 6

Do not annualize a noisy week.

## Output

Deliver a **metrics note**.

- Purpose of this metrics note, in two sentences.
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

Jonah's week of 8 September export shows MRR of $42,000, up from $40,500, and logo churn of 3.8 percent. Activation is blank. A slide adds 120 percent NRR from a blog.

### Example data

```text
week: 8-14 Sep 2026
MRR: 42000, prior week 40500
logo churn: 3.8 percent, their definition, logos not revenue
activation: blank
NRR in the slide: 120 percent, no cohort file
definitions note: churn is logos, not dollars
```

### Example outcome

**Week of 8 September**
MRR $42,000, from $40,500. That is the move in the export.
Logo churn 3.8 percent. Their definition is logos, so this note does not call it revenue churn.
Activation: blank.
NRR: blank. The 120 percent is not in the export.
No benchmark. One week is not an annual run-rate.

## Anti-patterns

- A benchmark from memory
- A blank filled with a guess
- An annualized run-rate from one week

## Related skills

- `net-retention-note`
- `metric-definition`

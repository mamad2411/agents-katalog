---
name: voice-of-customer
description: "Assemble a voice-of-customer brief from real quotes and tickets, with the sample bias visible. Use when the user mentions voice of customer, VOC brief, customer themes, what are customers saying, or asks for a voice-of-customer brief. Customer experience skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: customer
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'voice-of-customer' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Voice of Customer

Assemble a voice-of-customer brief from real quotes and tickets, with the sample bias visible.

## When to use this skill

Use this skill when the user:

- voice of customer
- VOC brief
- customer themes
- what are customers saying

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Do not blame the customer. Do not invent policy exceptions. Do not ask a customer for passwords or full payment card numbers.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The sources
- The decision
- Sample sizes
- Quotes they can share

## Workflow


### 1. Step 1

List sources and who is missing, such as quiet renewals or lost deals.
### 2. Step 2

Theme by the job or failure, and attach only supplied quotes.
### 3. Step 3

Separate frequency from severity.
### 4. Step 4

Do not invent a quote to make a theme neater.
### 5. Step 5

Recommend one product, policy, or support change.
### 6. Step 6

Note what sales anecdotes cannot prove.

## Output

Deliver a **voice-of-customer brief**.

- Purpose of this voice-of-customer brief, in two sentences.
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

Rita Santos, support lead at Fieldnote in Edmonton, needs a voice-of-customer brief by 30 September 2026. A briefing uses one loud customer's words as if they were the whole base.

### Example data

```text
From: Rita Santos, support lead
Organization: Fieldnote, Edmonton
Date: 14 September 2026
Needed by: 30 September 2026

A briefing uses one loud customer's words as if they were the whole base.

The sources: note from Rita Santos, 14 September 2026. No outside report
The decision: A briefing uses one loud customer's words as if they were the whole base
Sample sizes: Ticket 4420, recorded 14 September 2026. No supporting file attached
Quotes they can share: Ticket 4420. Stated in the ask, not documented anywhere else
```

### Example outcome

**Voice-of-customer brief**
To: Rita Santos, support lead, Fieldnote
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Labels the sample and refuses to generalize from one voice.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The sources | note from Rita Santos, 14 September 2026. No outside report | Needs confirmation |
| The decision | A briefing uses one loud customer's words as if they were the whole base | Carried into the draft |
| Sample sizes | Ticket 4420, recorded 14 September 2026. No supporting file attached | Carried into the draft |
| Quotes they can share | Ticket 4420. Stated in the ask, not documented anywhere else | Needs confirmation |

**How this draft was built**

**1. List sources and who is missing, such as quiet renewals or lost deals**

**2. Theme by the job or failure, and attach only supplied quotes**

**3. Separate frequency from severity**

**4. Do not invent a quote to make a theme neater**

**5. Recommend one product, policy, or support change**

**Deliberately not done**
- Invented quotes.
- A brief with no sample bias.
- Themes with no evidence.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Rita Santos by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Invented quotes
- A brief with no sample bias
- Themes with no evidence

## Related skills

- `feedback-synthesis`
- `journey-map`

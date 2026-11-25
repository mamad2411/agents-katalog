---
name: briefing-note
description: "Write a briefing note that states the issue, the options, and the recommendation for a public decision-maker. Use when the user mentions briefing note, ministerial brief, decision note public, options brief, or asks for a briefing note. Public sector skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: public-sector
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'briefing-note' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Briefing Note

Write a briefing note that states the issue, the options, and the recommendation for a public decision-maker.

## When to use this skill

Use this skill when the user:

- briefing note
- ministerial brief
- decision note public
- options brief

## When not to use this skill

- Deceptive public communications
- Voter manipulation

## Professional boundary

Public work should be accurate, even-handed, and suitable for the record. Do not draft deceptive communications, voter manipulation, or surveillance programs.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The decision
- The facts they can publish
- The options
- The audience

## Workflow


### 1. Step 1

Lead with the purpose and the recommendation.
### 2. Step 2

Use facts they can stand behind on the record.
### 3. Step 3

Give real options, including do nothing.
### 4. Step 4

State the public impact and the implementation constraint.
### 5. Step 5

Do not draft deceptive messaging or a plan to manipulate a consultation.
### 6. Step 6

Mark classified or personal data as not for this note.

## Output

Deliver a **briefing note**.

- Purpose of this briefing note, in two sentences.
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

Pat Nguyen, clerk at Town of Airdrie in Airdrie, needs a briefing note by 30 September 2026. A brief omits a known cost because it would be unpopular.

### Example data

```text
From: Pat Nguyen, clerk
Organization: Town of Airdrie, Airdrie
Date: 14 September 2026
Needed by: 30 September 2026

A brief omits a known cost because it would be unpopular.

The decision: A brief omits a known cost because it would be unpopular
The facts they can publish: Council agenda item 6, recorded 14 September 2026. No supporting file attached
The options: keep Council agenda item 6, or stop. No third option written
The audience: people who already buy from Town of Airdrie
```

### Example outcome

**Briefing note**
To: Pat Nguyen, clerk, Town of Airdrie
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Includes the cost and a plain recommendation.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The decision | A brief omits a known cost because it would be unpopular | Needs confirmation |
| The facts they can publish | Council agenda item 6, recorded 14 September 2026. No supporting file attached | Carried into the draft |
| The options | keep Council agenda item 6, or stop. No third option written | Carried into the draft |
| The audience | people who already buy from Town of Airdrie | Needs confirmation |

**How this draft was built**

**1. Lead with the purpose and the recommendation**

**2. Use facts they can stand behind on the record**

**3. Give real options, including do nothing**

**4. State the public impact and the implementation constraint**

**5. Do not draft deceptive messaging or a plan to manipulate a consultation**

**Deliberately not done**
- Deceptive public messaging.
- Personal data in the brief.
- A recommendation with no option.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Pat Nguyen by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Deceptive public messaging
- Personal data in the brief
- A recommendation with no option

## Related skills

- `executive-one-pager`
- `board-memo-writer`

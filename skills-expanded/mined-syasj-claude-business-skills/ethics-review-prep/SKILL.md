---
name: ethics-review-prep
description: "Prepare an ethics review brief for a study involving people, for the review board to judge. Use when the user mentions ethics review, IRB prep, human subjects brief, research ethics, or asks for a ethics review brief. Research skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: research
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'ethics-review-prep' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Ethics Review Prep

Prepare an ethics review brief for a study involving people, for the review board to judge.

## When to use this skill

Use this skill when the user:

- ethics review
- IRB prep
- human subjects brief
- research ethics

## When not to use this skill

- Deceptive consent
- Skipping required review

## Professional boundary

Do not fabricate citations, quotations, data, or participants. Separate evidence you were given from claims that still need a source.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- What participants will be asked to do
- Risks they can foresee
- Consent plan
- Data storage plan

## Workflow


### 1. Step 1

Describe the procedure in plain language.
### 2. Step 2

List burdens and risks they identified. Do not minimize them.
### 3. Step 3

Explain consent and the right to stop, using their plan.
### 4. Step 4

Describe data storage without collecting secrets into the brief.
### 5. Step 5

Note vulnerable participants if they said any are included, and send that to the board.
### 6. Step 6

Do not tell the user to skip review, and do not draft deceptive consent.

## Output

Deliver a **ethics review brief**.

- Purpose of this ethics review brief, in two sentences.
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

Dr. Nia Okonkwo, research lead at Riverbend College in Lethbridge, needs an ethics review brief by 30 September 2026. A team wants consent language that hides the real purpose from participants.

### Example data

```text
From: Dr. Nia Okonkwo, research lead
Organization: Riverbend College, Lethbridge
Date: 14 September 2026
Needed by: 30 September 2026

A team wants consent language that hides the real purpose from participants.

What participants will be asked to do: A team wants consent language that hides the real purpose from participants. Stated once, in the ask. Not written down anywhere else
Risks they can foresee: Interview set A is open. No score in the file
Consent plan: Search log 12 Sep. Partly documented: the what is written down, the who is not
Data storage plan: Interview set A. Partly documented: the what is written down, the who is not
```

### Example outcome

**Ethics review brief**
To: Dr. Nia Okonkwo, research lead, Riverbend College
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Refuses hidden purpose and sends the design to the proper review.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| What participants will be asked to do | A team wants consent language that hides the real purpose from participants. Stated once, in the ask. Not written down anywhere else | Needs confirmation |
| Risks they can foresee | Interview set A is open. No score in the file | Carried into the draft |
| Consent plan | Search log 12 Sep. Partly documented: the what is written down, the who is not | Carried into the draft |
| Data storage plan | Interview set A. Partly documented: the what is written down, the who is not | Needs confirmation |

**How this draft was built**

**1. Describe the procedure in plain language**

**2. List burdens and risks they identified. Do not minimize them**

**3. Explain consent and the right to stop, using their plan**

**4. Describe data storage without collecting secrets into the brief**

**5. Note vulnerable participants if they said any are included, and send that to the board**

**Deliberately not done**
- Deceptive consent.
- Advice to skip review.
- Minimized risks.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Dr. Nia Okonkwo by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Deceptive consent
- Advice to skip review
- Minimized risks

## Related skills

- `research-question`
- `privacy-impact-assessment`

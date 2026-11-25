---
name: survey-analysis
description: "Analyze a survey without overclaiming a small or biased sample. Use when the user mentions survey results, questionnaire analysis, NPS analysis, survey readout, or asks for a survey analysis. Data and analytics skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: data
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'survey-analysis' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Survey Analysis

Analyze a survey without overclaiming a small or biased sample.

## When to use this skill

Use this skill when the user:

- survey results
- questionnaire analysis
- NPS analysis
- survey readout

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Do not invent numbers. If a source file is missing, say so. Distinguish observation from inference. Do not re-identify private data to make a point.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The questions and results
- Sample size and how people were recruited
- The decision
- Any open text they provided

## Workflow


### 1. Step 1

Report the sample and the recruitment bias before the score.
### 2. Step 2

Do not treat a small sample as a population percentage without a caution.
### 3. Step 3

Separate closed scores from themes in open text they actually pasted.
### 4. Step 4

Do not invent themes.
### 5. Step 5

Tie one finding to a decision or say the survey cannot support one.
### 6. Step 6

Protect respondent privacy in small slices.

## Output

Deliver a **survey analysis**.

- Purpose of this survey analysis, in two sentences.
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

Noah Berger, data lead at Fieldnote in Edmonton, needs a survey analysis by 30 September 2026. An NPS of 80 from 11 self-selected responses is about to go on a board slide as proof of love.

### Example data

```text
From: Noah Berger, data lead
Organization: Fieldnote, Edmonton
Date: 14 September 2026
Needed by: 30 September 2026

An NPS of 80 from 11 self-selected responses is about to go on a board slide as proof of love.

The questions and results: An NPS of 80 from 11 self-selected responses is about to go on a board slide as proof of love
Sample size and how people were recruited: active_accounts, recorded 14 September 2026. No supporting file attached
The decision: An NPS of 80 from 11 self-selected responses is about to go on a board slide as proof of love
Any open text they provided: customers. Partly documented: the what is written down, the who is not
```

### Example outcome

**Survey analysis**
To: Noah Berger, data lead, Fieldnote
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Blocks the board claim, states the bias, and limits the use of the score.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The questions and results | An NPS of 80 from 11 self-selected responses is about to go on a board slide as proof of love | Needs confirmation |
| Sample size and how people were recruited | active_accounts, recorded 14 September 2026. No supporting file attached | Carried into the draft |
| The decision | An NPS of 80 from 11 self-selected responses is about to go on a board slide as proof of love | Carried into the draft |
| Any open text they provided | customers. Partly documented: the what is written down, the who is not | Needs confirmation |

**How this draft was built**

**1. Report the sample and the recruitment bias before the score**

**2. Do not treat a small sample as a population percentage without a caution**

**3. Separate closed scores from themes in open text they actually pasted**

**4. Do not invent themes**

**5. Tie one finding to a decision or say the survey cannot support one**

**Deliberately not done**
- A precise population claim from a tiny sample.
- Invented themes.
- Identifying a respondent.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Noah Berger by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A precise population claim from a tiny sample
- Invented themes
- Identifying a respondent

## Related skills

- `engagement-survey-readout`
- `feedback-synthesis`

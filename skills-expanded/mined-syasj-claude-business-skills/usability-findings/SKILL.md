---
name: usability-findings
description: "Write usability findings from observed task failures, with severity and a recommended change. Use when the user mentions usability findings, test findings, user test readout, what did the test show, or asks for a findings note. Design skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: design
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'usability-findings' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Usability Findings

Write usability findings from observed task failures, with severity and a recommended change.

## When to use this skill

Use this skill when the user:

- usability findings
- test findings
- user test readout
- what did the test show

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Design critique improves the work. Do not copy a third party's branded assets. Accessibility is part of done, not a later pass to skip.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The tasks
- What participants did
- Severity clues
- What the test cannot prove

## Workflow


### 1. Step 1

Report the task and the observed failure.
### 2. Step 2

Quote or describe only what was observed.
### 3. Step 3

Rate severity by whether the task was blocked.
### 4. Step 4

Recommend a design change for each blocking finding.
### 5. Step 5

State the sample limit. Do not claim market proof.
### 6. Step 6

Do not identify participants beyond what consent allows.

## Output

Deliver a **findings note**.

- Purpose of this findings note, in two sentences.
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

Lena Ortiz, design lead at Fieldnote in Edmonton, needs a findings note by 30 September 2026. A readout says users love the brand because three people finished a task.

### Example data

```text
From: Lena Ortiz, design lead
Organization: Fieldnote, Edmonton
Date: 14 September 2026
Needed by: 30 September 2026

A readout says users love the brand because three people finished a task.

The tasks: A readout says users love the brand because three people finished a task. Stated once, in the ask. Not written down anywhere else
What participants did: Lena Ortiz plus two others named in the thread. No distribution list attached
Severity clues: Empty-state copy. Partly documented: the what is written down, the who is not
What the test cannot prove: Colour contrast audit, last reviewed 14 September 2026. No owner named since
```

### Example outcome

**Findings note**
To: Lena Ortiz, design lead, Fieldnote
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Reports task completion, refuses the love claim, and ranks blocking issues.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The tasks | A readout says users love the brand because three people finished a task. Stated once, in the ask. Not written down anywhere else | Needs confirmation |
| What participants did | Lena Ortiz plus two others named in the thread. No distribution list attached | Carried into the draft |
| Severity clues | Empty-state copy. Partly documented: the what is written down, the who is not | Carried into the draft |
| What the test cannot prove | Colour contrast audit, last reviewed 14 September 2026. No owner named since | Needs confirmation |

**How this draft was built**

**1. Report the task and the observed failure**

**2. Quote or describe only what was observed**

**3. Rate severity by whether the task was blocked**

**4. Recommend a design change for each blocking finding**

**5. State the sample limit. Do not claim market proof**

**Deliberately not done**
- Market-proof claims from five tests.
- Findings with no observation.
- Identified participants.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Lena Ortiz by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Market-proof claims from five tests
- Findings with no observation
- Identified participants

## Related skills

- `usability-test-plan`
- `design-critique`

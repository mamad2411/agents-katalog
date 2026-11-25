---
name: ai-review-gate
description: "Place a human review where a model output can move money, a customer message, or a record. Use when the user mentions human in the loop, AI approval, review gate, who signs the model output, or asks for a review gate. AI in the business skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: ai
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'ai-review-gate' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# AI Review Gate

Place a human review where a model output can move money, a customer message, or a record.

## When to use this skill

Use this skill when the user:

- human in the loop
- AI approval
- review gate
- who signs the model output

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Do not write prompts or workflows that weaken safety rules, hide required disclosure, or invent model scores. This is not a certification and not a reason to send private data to a vendor.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The output type
- The decision it can trigger
- The reviewer role
- The hours they can actually review

## Workflow


### 1. Step 1

List outputs that can leave the building.
### 2. Step 2

Put a named role on each, not 'the team'.
### 3. Step 3

Match the gate to the hours they have. A gate no one staffs is a finding.
### 4. Step 4

Say what the reviewer is checking.
### 5. Step 5

Say what happens if the reviewer is absent.
### 6. Step 6

Do not let a model approve its own output.

## Output

Deliver a **review gate**.

- Purpose of this review gate, in two sentences.
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

Fieldnote set refund drafts to send at 22:00 if no one clicks. Rita works 08:00 to 17:00. Jonah needs the gate written down.

### Example data

```text
output: customer email draft
can trigger: a refund mention and a send
reviewer role: support lead
hours staffed: 08:00-17:00 America/Edmonton, weekdays
current rule: auto-send at 22:00
queue last week: 14 night tickets
```

### Example outcome

**Review gate**
Night drafts wait.

| Output | Reviewer | If absent |
| --- | --- | --- |
| Reply draft | Rita Santos | Holds until next staffed morning |
| Refund or credit | Rita Santos | Not sent. Not a model decision |
| Internal summary | Jonah Park | May sit unread. Does not email the customer |

Remove the 22:00 auto-send. A gate no one staffs is not a gate.
Next: Jonah turns auto-send off before 18 September.

## Anti-patterns

- A gate with no named role
- After-hours auto-send
- The model marking its own work approved

## Related skills

- `ai-use-case`
- `ai-incident-note`

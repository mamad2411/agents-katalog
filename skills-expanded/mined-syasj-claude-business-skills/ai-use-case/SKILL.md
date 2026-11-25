---
name: ai-use-case
description: "Decide whether a task should use a model, who owns the failure, and what stays manual. Use when the user mentions AI use case, should we use a model, automation brief, AI opportunity, or asks for a use-case note. AI in the business skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: ai
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'ai-use-case' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# AI Use Case

Decide whether a task should use a model, who owns the failure, and what stays manual.

## When to use this skill

Use this skill when the user:

- AI use case
- should we use a model
- automation brief
- AI opportunity

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

- The task
- What a wrong answer costs
- Who reviews the output
- Data that would be sent

## Workflow


### 1. Step 1

Name the task in one sentence.
### 2. Step 2

State the cost of a wrong answer in the user's words.
### 3. Step 3

Say what a person still reviews before the output is used.
### 4. Step 4

List data that must not be sent.
### 5. Step 5

Recommend use, pilot, or do not use.
### 6. Step 6

Do not invent an accuracy number.

## Output

Deliver a **use-case note**.

- Purpose of this use-case note, in two sentences.
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

Fieldnote support wants a bot to issue refunds under $30 with no reviewer, because the night queue is slow. Jonah has one week of tickets and no accuracy test.

### Example data

```text
task: read a ticket and issue a refund under $30
wrong-answer cost: a refund the lead did not approve
reviewer today: Rita Santos, on shift 08:00-17:00 America/Edmonton
night volume: 14 tickets, 8-14 Sep 2026, none reviewed
data that would be sent: full ticket, including the card last-four on 6 of 14
test set: none
```

### Example outcome

**Use-case note**
Do not let the model issue refunds.

| Piece | Call |
| --- | --- |
| Draft a reply from the complaint text | Pilot, after the card last-four is stripped |
| Decide or send a refund | Stays with Rita |
| Night auto-send | No. 14 tickets is a queue fact, not a test |

Owner of a bad draft: Jonah. Reviewer before send: Rita.
Open: no labeled examples, so no accuracy claim.
Next: Rita confirms the day gate by 30 September 2026.

## Anti-patterns

- An accuracy claim with no test
- Private data sent by default
- No human owner

## Related skills

- `ai-review-gate`
- `ai-data-note`

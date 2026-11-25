---
name: ai-incident-note
description: "Write up a bad model output the user observed, with the prompt, the harm, and the hold. Use when the user mentions AI incident, model error writeup, bad model output, AI miss, or asks for a incident note. AI in the business skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: ai
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'ai-incident-note' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# AI Incident Note

Write up a bad model output the user observed, with the prompt, the harm, and the hold.

## When to use this skill

Use this skill when the user:

- AI incident
- model error writeup
- bad model output
- AI miss

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

- What the user saw
- The prompt or task
- Who received the output
- What they did next

## Workflow


### 1. Step 1

Describe the output they saw. Do not embellish.
### 2. Step 2

Attach the task, not a theory about the model.
### 3. Step 3

Say who saw it and whether it was sent.
### 4. Record the hold

what is paused now.
### 5. Step 5

Separate a one-off from a pattern only if they have more than one case.
### 6. Step 6

Do not include secrets from the prompt in the note.

## Output

Deliver a **incident note**.

- Purpose of this incident note, in two sentences.
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

On 14 September a support draft offered a $20 refund on ticket 4412 and the night rule sent it. The customer wrote back to accept. Rita had not approved the refund.

### Example data

```text
when: 14 Sep 2026, 22:04
ticket: 4412
what the draft added: a $20 refund
source ticket: customer said they were charged twice, no refund amount
sent: yes, by the 22:00 rule
customer reply: accepted the $20
other cases: none pulled yet
```

### Example outcome

**Incident note**
One sent draft. Not yet a pattern. Only one case is in the file.

What happened: ticket 4412 asked about a double charge. The draft added a $20 refund. The night rule sent it. The customer accepted.
Hold now: auto-send off. Refunds stay with Rita.
Not in this note: a model 'cause'. No log of why it picked $20.
Customer name: omitted. Ticket number is enough.
Next: Rita decides the $20 already accepted. Jonah pulls any other night sends before calling it a pattern.

## Anti-patterns

- A cause claimed with no log
- A customer name copied into a wide memo
- No hold

## Related skills

- `ai-review-gate`
- `incident-postmortem`

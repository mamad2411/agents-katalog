---
name: agent-task-card
description: "Bound an agent task: the inputs, the tools, the stop rules, and the human owner. Use when the user mentions agent task, what may the agent do, agent boundary, tool use card, or asks for a task card. AI in the business skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: ai
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'agent-task-card' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Agent Task Card

Bound an agent task: the inputs, the tools, the stop rules, and the human owner.

## When to use this skill

Use this skill when the user:

- agent task
- what may the agent do
- agent boundary
- tool use card

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
- Tools they want it to call
- Actions that need a person
- The owner

## Workflow


### 1. Step 1

Write the task so a stranger could tell when it is done.
### 2. Step 2

List tools by name. No implied tools.
### 3. Step 3

Put money movement, sending, and deletes behind a person.
### 4. Step 4

State the stop rule when a fact is missing.
### 5. Step 5

Name the owner of a bad run.
### 6. Step 6

Do not grant a tool the user did not name.

## Output

Deliver a **task card**.

- Purpose of this task card, in two sentences.
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

A spec says the support agent may read the ticket, email the customer, and issue a credit under $30. Jonah wants a card that a person can enforce.

### Example data

```text
task: turn one ticket into a reply draft
tools named: help desk read, model draft
tools in the spec that he will not grant: send email, issue credit
stop if: the ticket has no order id, or a card number is present
owner of a bad run: Jonah Park
done looks like: a draft Rita can accept or reject
```

### Example outcome

**Task card — support-reply-draft**
Done: a draft is waiting for Rita. Not done: an email sent, a credit posted.

Tools: read the ticket, write a draft. No other tool.
Stop: no order id, or a card number is still in the text. Do not draft. Ask a person.
Person required: sending, credits, refunds, deletes.
Owner: Jonah Park.
The earlier spec's send and credit lines are not on this card.

## Anti-patterns

- An agent that sends or pays alone
- Hidden tools
- A task of 'help the team'

## Related skills

- `ai-review-gate`
- `prompt-boundary-check`

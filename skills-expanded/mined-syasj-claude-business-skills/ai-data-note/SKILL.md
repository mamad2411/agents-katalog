---
name: ai-data-note
description: "Say what may be pasted into a model and what must stay in the source system. Use when the user mentions AI data handling, what can we paste, model privacy, prompt data rules, or asks for a data-handling note. AI in the business skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: ai
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'ai-data-note' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# AI Data Note

Say what may be pasted into a model and what must stay in the source system.

## When to use this skill

Use this skill when the user:

- AI data handling
- what can we paste
- model privacy
- prompt data rules

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

- The fields in the task
- Which fields are personal or secret
- The vendor terms they actually have
- The retention they were promised

## Workflow


### 1. Step 1

Split fields into allowed, redacted, and forbidden.
### 2. Step 2

Forbidden includes secrets, payment numbers, and health details unless their counsel already approved that vendor.
### 3. Step 3

Do not invent a vendor promise that is not in their terms.
### 4. Step 4

Say where the source of truth stays.
### 5. Step 5

Name who may paste a row.
### 6. Step 6

If terms are missing, the note says the vendor question is open.

## Output

Deliver a **data-handling note**.

- Purpose of this data-handling note, in two sentences.
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

Agents want to paste the whole ticket into a model. Six of fourteen sample tickets include a card last-four and a home address. Vendor terms are not in the folder.

### Example data

```text
fields in a ticket: complaint text, order id, card last-four, home address, agent notes
vendor terms in the folder: none
retention promised: not documented
who pastes today: any agent on shift
sample: 14 tickets, 8-14 Sep 2026
```

### Example outcome

**Data note**
Allowed in the paste: complaint text and order id.
Strip before paste: card last-four, home address.
Agent notes: stay in the help desk until Jonah says otherwise.
Vendor retention: open. No terms in the folder, so do not write 'they don't train on it'.
Who may paste: an agent on shift, after the strip.
Source of truth: the help desk, not the chat window.

## Anti-patterns

- A blanket 'our vendor is private'
- Pasting card numbers
- Invented retention periods

## Related skills

- `ai-vendor-note`
- `privacy-by-design`

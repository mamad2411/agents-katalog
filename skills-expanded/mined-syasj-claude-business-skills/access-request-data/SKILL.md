---
name: access-request-data
description: "Triage an internal request for data the company already holds, against the approver they name. Use when the user mentions data access request, who can see this table, internal data request, warehouse access, or asks for a access note. Data and analytics skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: data
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'access-request-data' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Data Access Request

Triage an internal request for data the company already holds, against the approver they name.

## When to use this skill

Use this skill when the user:

- data access request
- who can see this table
- internal data request
- warehouse access

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

- Who is asking
- The table
- Why
- The approver role in their policy

## Workflow


### 1. Step 1

Record the asker, the table, and the why.
### 2. Step 2

Check the approver they said their policy requires.
### 3. Step 3

Do not grant access yourself.
### 4. Step 4

Minimize columns. Ask if the whole table is needed.
### 5. Step 5

Flag personal columns.
### 6. Step 6

If the why is missing, the request waits.

## Output

Deliver a **access note**.

- Purpose of this access note, in two sentences.
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

An analyst asked Noah for the full tickets table, including home addresses, to 'get a feel for the voice'. Their policy says the privacy lead approves personal columns. That role is vacant.

### Example data

```text
asker: Sam Okonkwo, analyst
table: support.tickets
why: get a feel for the voice
columns requested: all
personal columns in the table: email, home address
approver in policy: privacy lead
privacy lead: vacant
Noah's authority: he cannot approve his own pipeline, and he is not the privacy lead
```

### Example outcome

**Access note**
Do not grant the full table.

The why is not a question the table can answer. Send it back.
If they return with a real question, drop email and home address unless the privacy lead approves. That role is vacant, so those columns wait.
Noah does not approve this. Seniority is not the approver.
A shared login is not an option in this note.
Next: Sam rewrites the why, or the request stays closed.

## Anti-patterns

- Access because someone is senior
- A shared login
- Approving your own request

## Related skills

- `access-review`
- `ai-data-note`

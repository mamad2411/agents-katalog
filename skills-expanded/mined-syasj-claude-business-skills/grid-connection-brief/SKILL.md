---
name: grid-connection-brief
description: "Brief a connection request with the site facts and the studies the user already has. Use when the user mentions grid connection, interconnection, connect a site, queue brief, or asks for a connection brief. Energy and utilities operations skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: energy
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'grid-connection-brief' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Grid Connection Brief

Brief a connection request with the site facts and the studies the user already has.

## When to use this skill

Use this skill when the user:

- grid connection
- interconnection
- connect a site
- queue brief

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Operational energy advice is not a permit and not a safety case. Do not bypass lockout, isolation, or regulatory limits.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The site
- The size they are requesting
- Studies in hand
- The queue status they were given

## Workflow


### 1. Step 1

State the site and the size.
### 2. Step 2

List studies they have.
### 3. Step 3

A missing study is a gap.
### 4. Step 4

Use the queue status they were given, not a guessed date.
### 5. Step 5

Do not promise interconnection.
### 6. Step 6

Name the owner of the next filing.

## Output

Deliver a **connection brief**.

- Purpose of this connection brief, in two sentences.
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

A site in Grand Prairie is requesting 5 MW. The utility status email says application received. A brief promises connection in March. The only study in the folder is a draft one-line, marked draft.

### Example data

```text
site: east of Grande Prairie, their file name Site 4
size requested: 5 MW
status email: application received, 8 Sep 2026
studies in folder: one-line, marked draft
promised in the brief: connected March 2027
owner of the next filing: Devon Hale
```

### Example outcome

**Connection brief**
Site 4, 5 MW requested. Status: application received, 8 September. That is the status. March is not in the email. It comes out.
Study in the folder: a draft one-line. It is not a completed study.
No interconnection is promised.
Next filing owner: Devon. He does not send the March date.

## Anti-patterns

- A guessed in-service date
- A study marked done that is not in the file
- A promise of connection

## Related skills

- `tariff-change-note`
- `project-charter`

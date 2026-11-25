---
name: data-availability
description: "Write a data-availability statement that matches the files they can actually share. Use when the user mentions data availability, what data can we share, availability statement, open data note, or asks for a availability statement. Research skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: research
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'data-availability' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Data Availability

Write a data-availability statement that matches the files they can actually share.

## When to use this skill

Use this skill when the user:

- data availability
- what data can we share
- availability statement
- open data note

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

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

- The files
- What contains personal data
- The repository they will use
- What they cannot share

## Workflow


### 1. Step 1

Name files they will deposit.
### 2. Step 2

Hold files they said contain personal data.
### 3. Step 3

Do not write 'available on request' if they have no process.
### 4. Step 4

Give the repository only if it exists.
### 5. Step 5

Match the statement to the files, not to a journal template.
### 6. Step 6

Say who approves a later request.

## Output

Deliver a **availability statement**.

- Purpose of this availability statement, in two sentences.
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

A journal template in the draft says the data are in Zenodo. Nia has not created a deposit. Two spreadsheets have participant names and phone numbers.

### Example data

```text
files: codebook.pdf, interview-guide.pdf, contacts.xlsx, raw-notes.xlsx
personal data: names and phones in contacts.xlsx and in a column of raw-notes.xlsx
repository: none created
later requests: Nia will answer, no process written
template line: "Data are available in Zenodo"
```

### Example outcome

**Availability statement**
Do not use the Zenodo line. No deposit exists.
Not for deposit: contacts.xlsx, and the name and phone column in raw-notes.xlsx.
codebook.pdf and interview-guide.pdf can be deposited once a repository exists.
Until then the statement is: these two files are not yet in a repository. Personal-data files are not in the share set.
'Available on request' is not in this statement. There is no written process.

## Anti-patterns

- A template statement
- Personal data in the deposit
- A repository that does not exist

## Related skills

- `replication-check`
- `consent-script`

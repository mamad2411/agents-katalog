---
name: replication-check
description: "Check whether a result can be rerun from the files the user has. Use when the user mentions replication, can we rerun this, reproducibility check, data for a result, or asks for a replication note. Research skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: research
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'replication-check' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Replication Check

Check whether a result can be rerun from the files the user has.

## When to use this skill

Use this skill when the user:

- replication
- can we rerun this
- reproducibility check
- data for a result

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

- The result
- The data file
- The steps they wrote down
- The missing piece

## Workflow


### 1. Step 1

Match the result to a file.
### 2. Step 2

Walk the steps they wrote.
### 3. Step 3

Stop at the first missing file or parameter.
### 4. Step 4

Do not fill a missing parameter with a plausible one.
### 5. Step 5

Say rerunnable or not, from this folder.
### 6. Step 6

Name what would make it rerunnable.

## Output

Deliver a **replication note**.

- Purpose of this replication note, in two sentences.
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

Table 2 in Nia's draft cites analysis.R and interviews.csv. The R script is in the folder. The CSV is not. A README mentions a cutoff of 0.5 that is not in the script.

### Example data

```text
result: Table 2, 20 interviews, mean confidence 3.4
script in folder: analysis.R
file the script reads: interviews.csv
interviews.csv in folder: no
cutoff 0.5: in the README, not in the script
```

### Example outcome

**Replication note**
Table 2 is not rerunnable from this folder.
The script is here. interviews.csv is not. Stop there.
Do not type 0.5 into the script from the README and call it replicated.
What would make it rerunnable: the CSV the script names, unchanged, and a note if 0.5 was ever used.
This is not a new analysis.

## Anti-patterns

- A plausible parameter treated as the original
- A pass with a missing file
- A new analysis called a replication

## Related skills

- `data-availability`
- `research-memo`

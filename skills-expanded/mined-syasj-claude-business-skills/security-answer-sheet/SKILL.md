---
name: security-answer-sheet
description: "Answer a security questionnaire from documents the company has, and leave the rest blank. Use when the user mentions security questionnaire, customer security review, SIG lite answers, vendor security answers, or asks for a answer sheet. SaaS skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: saas
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'security-answer-sheet' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Security Answer Sheet

Answer a security questionnaire from documents the company has, and leave the rest blank.

## When to use this skill

Use this skill when the user:

- security questionnaire
- customer security review
- SIG lite answers
- vendor security answers

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Do not invent churn, revenue, retention, or a security certification. If the export is missing, say so.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The questions
- The documents they have
- Certifications they hold
- Questions they cannot answer

## Workflow


### 1. Step 1

Answer only from a document.
### 2. Step 2

A missing report is 'not in the file', not a yes.
### 3. Step 3

Do not claim SOC 2, ISO, or HIPAA without the report.
### 4. Step 4

Say who may send the sheet.
### 5. Step 5

Do not paste secrets into answers.
### 6. Step 6

Mark follow-ups.

## Output

Deliver a **answer sheet**.

- Purpose of this answer sheet, in two sentences.
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

A customer asked if Fieldnote has SOC 2. The folder has no report. A draft answer says 'yes, in progress'. Nobody has written that a audit is underway. Jonah is the only person who may send the sheet.

### Example data

```text
question: do you have SOC 2
documents: none
draft answer: yes, in progress
audit letter: not in the folder
sender: Jonah Park
secrets: none to paste
```

### Example outcome

**Answer**
SOC 2: not in the file. Do not say yes. Do not say in progress. No letter says that.
Sender: Jonah. He does not forward the draft.
Other questions with no document get the same mark, not a guess.
No secrets in the sheet.

## Anti-patterns

- A certification they do not hold
- A guessed control
- Secrets in the answer

## Related skills

- `vendor-security-review`
- `ai-vendor-note`

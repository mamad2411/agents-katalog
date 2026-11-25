---
name: ai-vendor-note
description: "Compare AI vendors on data use, exit, and support the user can point to in a document. Use when the user mentions AI vendor, model vendor review, which LLM vendor, AI procurement, or asks for a vendor note. AI in the business skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: ai
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'ai-vendor-note' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# AI Vendor Note

Compare AI vendors on data use, exit, and support the user can point to in a document.

## When to use this skill

Use this skill when the user:

- AI vendor
- model vendor review
- which LLM vendor
- AI procurement

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

- The vendors
- The documents they have
- Data-use questions
- How they would leave

## Workflow


### 1. Step 1

Compare only documents they uploaded.
### 2. Step 2

Mark a missing security or data term as missing.
### 3. Step 3

Ask how content is retained and whether it trains a model, and record their answer or the gap.
### 4. State the exit

can they take prompts and outputs with them.
### 5. Step 5

Do not invent a certification.
### 6. Step 6

Recommend a pilot limit, not a company-wide switch, when terms are thin.

## Output

Deliver a **vendor note**.

- Purpose of this vendor note, in two sentences.
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

Fieldnote is looking at two model vendors. One website shows a SOC 2 badge. Neither report is in the folder. Jonah has a one-page quote from each.

### Example data

```text
vendor A quote: $0.01 per call, 2 Sep 2026, data terms not attached
vendor B quote: $0.04 per call, 3 Sep 2026, says "no training" in the email, no contract
SOC 2 reports: none in the folder
exit question: unanswered by both
pilot limit Jonah wants: one queue, 30 days
```

### Example outcome

**Vendor note**
Do not treat the badge as a report. It is not in the file.

| Question | A | B |
| --- | --- | --- |
| Price in hand | $0.01 / call | $0.04 / call |
| Training use | not in the file | email says no, contract missing |
| SOC 2 | badge only | not mentioned |
| Exit with prompts | unanswered | unanswered |

Pilot, if any: one queue, 30 days, no card data, no company-wide switch.
Next: ask both for the data term in a document before a second pilot week.

## Anti-patterns

- Invented SOC reports
- A logo count as proof
- Ignoring data retention

## Related skills

- `vendor-security-review`
- `ai-data-note`

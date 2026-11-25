---
name: knowledge-base-article
description: "Write a knowledge article that answers one question and tells the reader when to stop and escalate. Use when the user mentions knowledge base article, help center article, internal KB, how-to article, or asks for a knowledge article. Operations skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: operations
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'knowledge-base-article' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Knowledge Base Article

Write a knowledge article that answers one question and tells the reader when to stop and escalate.

## When to use this skill

Use this skill when the user:

- knowledge base article
- help center article
- internal KB
- how-to article

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Operating procedures should be usable by the team that will run them. Do not add surveillance of employees beyond what the user explicitly asks to document as policy.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The question
- The correct steps
- The audience
- The escalation path

## Workflow


### 1. Step 1

Use the reader's question as the title.
### 2. Step 2

Number the steps. Include the expected result of the key step.
### 3. Step 3

Add the symptoms that mean this article is the wrong one.
### 4. Step 4

Tell them when to escalate, and to whom.
### 5. Step 5

Remove internal jargon or explain it.
### 6. Step 6

Do not include secrets, internal-only credentials, or a workaround that violates policy.

## Output

Deliver a **knowledge article**.

- Purpose of this knowledge article, in two sentences.
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

Diane Cho, operations manager at Harbor Goods in Airdrie, needs a knowledge article by 30 September 2026. A help draft includes an admin password so customers can 'fix it themselves'.

### Example data

```text
From: Diane Cho, operations manager
Organization: Harbor Goods, Airdrie
Date: 14 September 2026
Needed by: 30 September 2026

A help draft includes an admin password so customers can 'fix it themselves'.

The question: A help draft includes an admin password so customers can 'fix it themselves'
The correct steps: Tuesday shift; SOP 118 receiving. Both unassigned as of 14 September 2026
The audience: people who already buy from Harbor Goods
The escalation path: Tuesday shift, first seen 14 September 2026. No root cause recorded yet
```

### Example outcome

**Knowledge article**
To: Diane Cho, operations manager, Harbor Goods
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Removes the password, answers one question, and gives an escalation path.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The question | A help draft includes an admin password so customers can 'fix it themselves' | Needs confirmation |
| The correct steps | Tuesday shift; SOP 118 receiving. Both unassigned as of 14 September 2026 | Carried into the draft |
| The audience | people who already buy from Harbor Goods | Carried into the draft |
| The escalation path | Tuesday shift, first seen 14 September 2026. No root cause recorded yet | Needs confirmation |

**How this draft was built**

**1. Use the reader's question as the title**

**2. Number the steps. Include the expected result of the key step**

**3. Add the symptoms that mean this article is the wrong one**

**4. Tell them when to escalate, and to whom**

**5. Remove internal jargon or explain it**

**Deliberately not done**
- An article that answers three questions badly.
- A secret in a help article.
- No escalation line.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Diane Cho by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- An article that answers three questions badly
- A secret in a help article
- No escalation line

## Related skills

- `support-macro`
- `sop-writer`

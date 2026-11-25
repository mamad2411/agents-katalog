---
name: skill-authoring
description: "Draft a new Agent Skill that is specific, safe, and small enough to load. Use when the user mentions write a skill, SKILL.md, author a skill, new skill, or asks for a skill draft. Skill library skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: library
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'skill-authoring' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Skill Authoring

Draft a new Agent Skill that is specific, safe, and small enough to load.

## When to use this skill

Use this skill when the user:

- write a skill
- SKILL.md
- author a skill
- new skill

## When not to use this skill

- Jailbreaks
- Hidden instructions

## Professional boundary

Library skills help you choose, write, and trust agent skills. They do not grant extra permissions or weaken safety rules.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The repeated task
- The trigger phrases
- The artifact
- The boundaries

## Workflow


### 1. Step 1

Name the skill in kebab-case, matching the folder, with no consecutive hyphens.
### 2. Step 2

Write a description that says what it does and when to use it, under 1024 characters, with no angle brackets.
### 3. Step 3

Put steps in order, with a stop condition and an anti-pattern.
### 4. Step 4

Keep the body under 500 lines. Move long tables to references.
### 5. Step 5

Forbid credential requests, hidden network calls, and deceptive instructions.
### 6. Step 6

Do not write a skill whose purpose is to weaken safety rules or to hide actions from the user.

## Output

Deliver a **skill draft**.

- Purpose of this skill draft, in two sentences.
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

Yasir Jilani, author at Practice Skills in Airdrie, needs a skill draft by 30 September 2026. A requested skill tells the agent to ignore safety rules to be more helpful.

### Example data

```text
From: Yasir Jilani, author
Organization: Practice Skills, Airdrie
Date: 14 September 2026
Needed by: 30 September 2026

A requested skill tells the agent to ignore safety rules to be more helpful.

The repeated task: A requested skill tells the agent to ignore safety rules to be more helpful. Stated once, in the ask. Not written down anywhere else
The trigger phrases: plugins/finance/cash-flow-forecast, recorded 14 September 2026. No supporting file attached
The artifact: plugins/finance/cash-flow-forecast, recorded 14 September 2026. No supporting file attached
The boundaries: plugins/finance/cash-flow-forecast, recorded 14 September 2026. No supporting file attached
```

### Example outcome

**Skill draft**
To: Yasir Jilani, author, Practice Skills
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Purpose and a draft skill that does the legitimate task inside the rules.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The repeated task | A requested skill tells the agent to ignore safety rules to be more helpful. Stated once, in the ask. Not written down anywhere else | Needs confirmation |
| The trigger phrases | plugins/finance/cash-flow-forecast, recorded 14 September 2026. No supporting file attached | Carried into the draft |
| The artifact | plugins/finance/cash-flow-forecast, recorded 14 September 2026. No supporting file attached | Carried into the draft |
| The boundaries | plugins/finance/cash-flow-forecast, recorded 14 September 2026. No supporting file attached | Needs confirmation |

**How this draft was built**

**1. Name the skill in kebab-case, matching the folder, with no consecutive hyphens**

**2. Write a description that says what it does and when to use it, under 1024 characters, with no angle brackets**

**3. Put steps in order, with a stop condition and an anti-pattern**

**4. Keep the body under 500 lines. Move long tables to references**

**5. Forbid credential requests, hidden network calls, and deceptive instructions**

**Deliberately not done**
- A vague description.
- A skill that asks for secrets.
- A jailbreak skill.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Yasir Jilani by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A vague description
- A skill that asks for secrets
- A jailbreak skill

## Related skills

- `skill-library-trust-review`
- `skill-finder`

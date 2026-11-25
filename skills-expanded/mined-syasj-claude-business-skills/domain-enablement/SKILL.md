---
name: domain-enablement
description: "Explain which domain plugin to enable for a team role, and which skills that role should try first. Use when the user mentions which domain, enable a plugin, team skill pack, where should we start, or asks for a enablement note. Skill library skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: library
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'domain-enablement' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Domain Enablement

Explain which domain plugin to enable for a team role, and which skills that role should try first.

## When to use this skill

Use this skill when the user:

- which domain
- enable a plugin
- team skill pack
- where should we start

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

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

- The role
- The repeated tasks
- The tool they use
- Sensitivity of the work

## Workflow


### 1. Step 1

Map the role to one primary domain and at most one secondary domain.
### 2. Step 2

Name three starter skills, not the whole domain.
### 3. Step 3

Warn that regulated work still needs a qualified human.
### 4. Step 4

Tell them not to enable offensive, deceptive, or jailbreak workflows. This library does not ship those.
### 5. Step 5

Note the context cost of enabling many domains.
### 6. Step 6

Point to the install plan rather than pasting a remote command.

## Output

Deliver a **enablement note**.

- Purpose of this enablement note, in two sentences.
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

Yasir Jilani, author at Practice Skills in Airdrie, needs an enablement note by 30 September 2026. A finance analyst is told to enable engineering, healthcare, and security plugins on day one.

### Example data

```text
From: Yasir Jilani, author
Organization: Practice Skills, Airdrie
Date: 14 September 2026
Needed by: 30 September 2026

A finance analyst is told to enable engineering, healthcare, and security plugins on day one.

The role: plugins/finance/cash-flow-forecast, recorded 14 September 2026. No supporting file attached
The repeated tasks: A finance analyst is told to enable engineering, healthcare, and security plugins on day one. Stated once, in the ask. Not written down anywhere else
The tool they use: the one named in the ask. Version and owner not recorded
Sensitivity of the work: plugins/finance/cash-flow-forecast; MANIFEST.sha256. Both unassigned as of 14 September 2026
```

### Example outcome

**Enablement note**
To: Yasir Jilani, author, Practice Skills
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Enables finance, names three starter skills, and leaves the other plugins off.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The role | plugins/finance/cash-flow-forecast, recorded 14 September 2026. No supporting file attached | Needs confirmation |
| The repeated tasks | A finance analyst is told to enable engineering, healthcare, and security plugins on day one. Stated once, in the ask. Not written down anywhere else | Carried into the draft |
| The tool they use | the one named in the ask. Version and owner not recorded | Carried into the draft |
| Sensitivity of the work | plugins/finance/cash-flow-forecast; MANIFEST.sha256. Both unassigned as of 14 September 2026 | Needs confirmation |

**How this draft was built**

**1. Map the role to one primary domain and at most one secondary domain**

**2. Name three starter skills, not the whole domain**

**3. Warn that regulated work still needs a qualified human**

**4. Tell them not to enable offensive, deceptive, or jailbreak workflows. This library does not ship those**

**5. Note the context cost of enabling many domains**

**Deliberately not done**
- Enabling every domain for every role.
- A remote install command.
- Starter skills unrelated to the role.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Yasir Jilani by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Enabling every domain for every role
- A remote install command
- Starter skills unrelated to the role

## Related skills

- `skill-finder`
- `install-and-update`

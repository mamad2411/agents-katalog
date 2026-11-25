---
name: handbook-policy-draft
description: "Draft a short handbook policy in plain language, marked for HR and counsel before publication. Use when the user mentions employee handbook, HR policy draft, workplace policy, code of conduct section, or asks for a handbook policy draft. People and culture skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: people
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'handbook-policy-draft' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Handbook Policy Draft

Draft a short handbook policy in plain language, marked for HR and counsel before publication.

## When to use this skill

Use this skill when the user:

- employee handbook
- HR policy draft
- workplace policy
- code of conduct section

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Employment work must follow the organization's policies and local employment law. Do not invent legal requirements. Do not write content that discriminates or retaliates.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The behavior the policy must guide
- The current practice
- Who enforces it
- Jurisdictions they say it must cover

## Workflow


### 1. Purpose

Why the policy exists for the workplace, in a few lines.
### 2. Rules

What people should do, in plain language. Avoid legalese copied from a mega-corporation.
### 3. Exceptions and reports

How to ask for an exception and how to report a breach, using their channels.
### 4. Consequences

Only the consequence types they say exist. Do not invent dismissal language as a legal fact.
### 5. Counsel flag

Note that local employment law may change the policy. The draft is not published as-is.
### 6. Length

One or two pages. A policy nobody reads will not guide behavior.

## Output

Deliver a **handbook policy draft**.

- Purpose of this handbook policy draft, in two sentences.
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

Chris Adeyemi, people lead at Northline Studio in Calgary, needs a handbook policy draft by 30 September 2026. The company wants a remote-work policy and currently decides each request in a private chat.

### Example data

```text
From: Chris Adeyemi, people lead
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

The company wants a remote-work policy and currently decides each request in a private chat.

The behavior the policy must guide: their one-page rule dated 2 Mar 2026. No exception log
The current practice: Jordan Hale, recorded 14 September 2026. No supporting file attached
Who enforces it: Chris Adeyemi, people lead
Jurisdictions they say it must cover: Open coordinator role. Stated in the ask, not documented anywhere else
```

### Example outcome

**Handbook policy draft**
To: Chris Adeyemi, people lead, Northline Studio
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
A two-page draft with a request path, decision criteria, and a counsel-review banner.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The behavior the policy must guide | their one-page rule dated 2 Mar 2026. No exception log | Needs confirmation |
| The current practice | Jordan Hale, recorded 14 September 2026. No supporting file attached | Carried into the draft |
| Who enforces it | Chris Adeyemi, people lead | Carried into the draft |
| Jurisdictions they say it must cover | Open coordinator role. Stated in the ask, not documented anywhere else | Needs confirmation |

**How this draft was built**

**1. Purpose**  
Why the policy exists for the workplace, in a few lines.

**2. Rules**  
What people should do, in plain language. Avoid legalese copied from a mega-corporation.

**3. Exceptions and reports**  
How to ask for an exception and how to report a breach, using their channels.

**4. Consequences**  
Only the consequence types they say exist. Do not invent dismissal language as a legal fact.

**5. Counsel flag**  
Note that local employment law may change the policy. The draft is not published as-is.

**Deliberately not done**
- A 30-page policy for a simple issue.
- Invented legal penalties.
- No reporting path.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Chris Adeyemi by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A 30-page policy for a simple issue.
- Invented legal penalties.
- No reporting path.

## Related skills

- `expense-policy`
- `policy-writer`
- `employee-relations-intake`

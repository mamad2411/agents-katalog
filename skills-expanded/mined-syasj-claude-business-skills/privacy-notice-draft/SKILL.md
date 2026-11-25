---
name: privacy-notice-draft
description: "Draft a plain-language privacy notice from the data practices the user describes, and mark every unknown. Use when the user mentions privacy notice, privacy policy draft, what we tell users about data, cookie notice outline, or asks for a privacy notice draft. Legal operations skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: legal
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'privacy-notice-draft' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Privacy Notice Draft

Draft a plain-language privacy notice from the data practices the user describes, and mark every unknown.

## When to use this skill

Use this skill when the user:

- privacy notice
- privacy policy draft
- what we tell users about data
- cookie notice outline

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

This is not legal advice and does not create an attorney-client relationship. Do not invent statutes, case names, or filing deadlines. Drafts are for qualified counsel in the relevant jurisdiction.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- What data they collect, in their words
- Why they collect it
- Who they share it with
- Where the notice will appear

## Workflow


### 1. Inventory practices first

A notice that describes practices they do not have is a new problem. Use only their inventory.
### 2. Write plainly

Categories of data, purposes, sharing, retention if they know it, and how people can ask questions.
### 3. Mark unknowns

If retention or a vendor list is missing, insert a visible placeholder, not a invented '90 days'.
### 4. No fake legal bases

Do not assign a GDPR lawful basis or a state-law category unless their counsel already named it.
### 5. Match the product

The notice should match the flow a person actually sees. Flag collection that the product team has not mentioned to users.
### 6. Counsel review

Label the draft as not for publication until qualified privacy counsel reviews the jurisdictions they name.

## Output

Deliver a **privacy notice draft**.

- Purpose of this privacy notice draft, in two sentences.
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

Elena Voss, operations lead at Northline Studio in Calgary, needs a privacy notice draft by 30 September 2026. A startup collects account email and product usage and wants a website privacy notice tomorrow.

### Example data

```text
From: Elena Voss, operations lead
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

A startup collects account email and product usage and wants a website privacy notice tomorrow.

What data they collect, in their words: Vendor terms, last reviewed 14 September 2026. No owner named since
Why they collect it: A startup collects account email and product usage and wants a website privacy notice tomorrow
Who they share it with: Elena Voss, operations lead
Where the notice will appear: Contractor NDA, recorded 14 September 2026. No supporting file attached
```

### Example outcome

**Privacy notice draft**
To: Elena Voss, operations lead, Northline Studio
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
A plain draft covering only those categories, with retention left as a placeholder and a counsel-review banner.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| What data they collect, in their words | Vendor terms, last reviewed 14 September 2026. No owner named since | Needs confirmation |
| Why they collect it | A startup collects account email and product usage and wants a website privacy notice tomorrow | Carried into the draft |
| Who they share it with | Elena Voss, operations lead | Carried into the draft |
| Where the notice will appear | Contractor NDA, recorded 14 September 2026. No supporting file attached | Needs confirmation |

**How this draft was built**

**1. Inventory practices first**  
A notice that describes practices they do not have is a new problem. Use only their inventory.

**2. Write plainly**  
Categories of data, purposes, sharing, retention if they know it, and how people can ask questions.

**3. Mark unknowns**  
If retention or a vendor list is missing, insert a visible placeholder, not a invented '90 days'.

**4. No fake legal bases**  
Do not assign a GDPR lawful basis or a state-law category unless their counsel already named it.

**5. Match the product**  
The notice should match the flow a person actually sees. Flag collection that the product team has not mentioned to users.

**Deliberately not done**
- A generic policy pasted over a product that works differently.
- Invented retention periods.
- Publishing instructions that skip counsel.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Elena Voss by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A generic policy pasted over a product that works differently.
- Invented retention periods.
- Publishing instructions that skip counsel.

## Related skills

- `data-processing-addendum`
- `privacy-impact-assessment`
- `privacy-by-design`

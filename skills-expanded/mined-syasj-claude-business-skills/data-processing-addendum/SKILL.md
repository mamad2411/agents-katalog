---
name: data-processing-addendum
description: "Check a data-processing addendum against the processing the business actually does, for counsel to finish. Use when the user mentions DPA review, data processing addendum, processor terms, subprocessor list, or asks for a DPA checklist. Legal operations skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: legal
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'data-processing-addendum' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Data Processing Addendum Checklist

Check a data-processing addendum against the processing the business actually does, for counsel to finish.

## When to use this skill

Use this skill when the user:

- DPA review
- data processing addendum
- processor terms
- subprocessor list

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

- The DPA text
- Whether the user is customer or vendor
- Categories of data they say are in scope
- Subprocessors they already use

## Workflow


### 1. Match roles

Controller and processor labels in the DPA versus how the user described the work. Flag conflicts. Do not resolve the legal role yourself.
### 2. Scope

Categories of data and purposes in the DPA versus the real service. Extra scope is a finding.
### 3. Subprocessors

Compare the DPA mechanism to the user's actual vendor list. Silence about a known subprocessor is a question.
### 4. Breach notice

The clock and the recipient, as written. Do not call a clock 'compliant'.
### 5. Deletion and return

What the text says happens at the end. If operations cannot perform it, say so.
### 6. International terms

If transfer language is present, quote it and send it to counsel. Do not invent a transfer mechanism.

## Output

Deliver a **DPA checklist**.

- Purpose of this DPA checklist, in two sentences.
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

Elena Voss, operations lead at Northline Studio in Calgary, needs a DPA checklist by 30 September 2026. A customer sent a DPA that forbids subprocessors, but the product uses a hosted email vendor.

### Example data

```text
From: Elena Voss, operations lead
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

A customer sent a DPA that forbids subprocessors, but the product uses a hosted email vendor.

The DPA text: Harbor renewal, recorded 14 September 2026. No supporting file attached
Whether the user is customer or vendor: Harbor renewal. Partly documented: the what is written down, the who is not
Categories of data they say are in scope: this decision only
Subprocessors they already use: email to Elena Voss. No written steps after 1 Sep 2026
```

### Example outcome

**Dpa checklist**
Northline Studio · 14 September 2026 · Due 30 September 2026

**Decision**
Flag the conflict between the ban and the known vendor, without calling either side compliant.

**Checklist**

- [x] **The DPA text** — Harbor renewal, recorded 14 September 2026. No supporting file attached  
      Evidenced in the file
- [x] **Whether the user is customer or vendor** — Harbor renewal. Partly documented: the what is written down, the who is not  
      Evidenced in the file
- [x] **Categories of data they say are in scope** — this decision only  
      Evidenced in the file
- [ ] **Subprocessors they already use** — email to Elena Voss. No written steps after 1 Sep 2026  
      Open — nothing in the file closes this

**The gates this list enforces, in order**

1. Match roles
2. Scope
3. Subprocessors
4. Breach notice
5. Deletion and return

**Deliberately not done**
- A compliance stamp on a DPA.
- Ignoring a subprocessor the user already named.
- Inventing Standard Contractual Clauses.

**Stop rule**
Do not mark this pack complete while a box above is open. An open box is a finding, not a formality — it is the thing this checklist exists to catch.

Next: Elena Voss closes the open items before 30 September 2026.

## Anti-patterns

- A compliance stamp on a DPA.
- Ignoring a subprocessor the user already named.
- Inventing Standard Contractual Clauses.

## Related skills

- `privacy-notice-draft`
- `vendor-security-review`
- `privacy-impact-assessment`

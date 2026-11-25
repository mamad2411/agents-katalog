---
name: corporate-records-hygiene
description: "Check whether basic corporate records are findable and consistent, without filing anything. Use when the user mentions corporate records, cap table documents, minute book, entity records hygiene, or asks for a corporate records checklist. Legal operations skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: legal
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'corporate-records-hygiene' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Corporate Records Hygiene

Check whether basic corporate records are findable and consistent, without filing anything.

## When to use this skill

Use this skill when the user:

- corporate records
- cap table documents
- minute book
- entity records hygiene

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

- Entities they listed
- Records they can find
- Known gaps
- Upcoming transaction that needs the records

## Workflow


### 1. List entities

Name, role, and formation place only as the user stated. Do not look up or invent registry data.
### 2. Core set

Formation document, ownership records, and recent approvals they say exist. Missing items are gaps, not failures of memory to paper over.
### 3. Consistency

Names and share counts that disagree across documents they described are findings.
### 4. Access

Who can find the records on a sick day. A single laptop is a risk.
### 5. No filings

Recommend counsel or a registered agent for any filing. Do not generate filing forms as if they were ready to submit.
### 6. Transaction use

If a raise or sale is coming, highlight the gaps that will be asked for first.

## Output

Deliver a **corporate records checklist**.

- Purpose of this corporate records checklist, in two sentences.
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

Elena Voss, operations lead at Northline Studio in Calgary, needs a corporate records checklist by 30 September 2026. A financing is six weeks away and the founder cannot find signed founder stock documents.

### Example data

```text
From: Elena Voss, operations lead
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

A financing is six weeks away and the founder cannot find signed founder stock documents.

Entities they listed: Harbor renewal; Contractor NDA; Vendor terms
Records they can find: one file, dated 14 September 2026. No earlier version attached for comparison
Known gaps: Harbor renewal is missing a source
Upcoming transaction that needs the records: one file, dated 14 September 2026. No earlier version attached for comparison
```

### Example outcome

**Corporate records checklist**
Northline Studio · 14 September 2026 · Due 30 September 2026

**Decision**
Prioritizes the missing stock documents and does not invent replacement signatures.

**Checklist**

- [x] **Entities they listed** — Harbor renewal; Contractor NDA; Vendor terms  
      Evidenced in the file
- [x] **Records they can find** — one file, dated 14 September 2026. No earlier version attached for comparison  
      Evidenced in the file
- [x] **Known gaps** — Harbor renewal is missing a source  
      Evidenced in the file
- [ ] **Upcoming transaction that needs the records** — one file, dated 14 September 2026. No earlier version attached for comparison  
      Open — nothing in the file closes this

**The gates this list enforces, in order**

1. List entities
2. Core set
3. Consistency
4. Access
5. No filings

**Deliberately not done**
- Inventing incorporation dates.
- Preparing a filing and calling it ready.
- Ignoring a share-count mismatch.

**Stop rule**
Do not mark this pack complete while a box above is open. An open box is a finding, not a formality — it is the thing this checklist exists to catch.

Next: Elena Voss closes the open items before 30 September 2026.

## Anti-patterns

- Inventing incorporation dates.
- Preparing a filing and calling it ready.
- Ignoring a share-count mismatch.

## Related skills

- `ip-ownership-checklist`
- `board-resolution-draft`
- `fundraising-model`

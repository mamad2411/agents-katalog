---
name: trademark-clearance-prep
description: "Prepare a clearance brief so counsel or a search firm can look up a name. Do not clear the name yourself. Use when the user mentions trademark clearance, can we use this name, brand name check, trademark search prep, or asks for a trademark clearance brief. Legal operations skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: legal
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'trademark-clearance-prep' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Trademark Clearance Prep

Prepare a clearance brief so counsel or a search firm can look up a name. Do not clear the name yourself.

## When to use this skill

Use this skill when the user:

- trademark clearance
- can we use this name
- brand name check
- trademark search prep

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

- The proposed name and stylization
- Goods or services in the user's words
- Markets they will sell in
- Names they have already seen in the wild

## Workflow


### 1. Describe the use

Word mark, logo, or both, and the goods or services in plain language.
### 2. Collect lookalikes

Names the user has already found. Do not claim you searched a registry unless a tool in the conversation actually did, and even then do not call it legal clearance.
### 3. List questions

Class of goods, confusingly similar marks, and domain or handle conflicts are questions for a search, not answers.
### 4. Avoid false comfort

'I do not see a problem' is not an allowed conclusion.
### 5. Recommend the next professional step

A qualified search in the jurisdictions they named.
### 6. Do not file

No filing instructions presented as complete, and no urgency tricks.

## Output

Deliver a **trademark clearance brief**.

- Purpose of this trademark clearance brief, in two sentences.
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

Elena Voss, operations lead at Northline Studio in Calgary, needs a trademark clearance brief by 30 September 2026. A team wants to know if a product name is safe because the .com was open.

### Example data

```text
From: Elena Voss, operations lead
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

A team wants to know if a product name is safe because the .com was open.

The proposed name and stylization: Lumen Ledger, word mark, no logo
Goods or services in the user's words: bookkeeping software for independent shops
Markets they will sell in: Alberta and online, English. No other country listed
Names they have already seen in the wild: lumenledger.com was open on 12 Sep 2026. No register search in the file
```

### Example outcome

**Trademark clearance brief**
To: Elena Voss, operations lead, Northline Studio
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Do not treat the open domain as clearance and lists what a professional search must cover.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The proposed name and stylization | Lumen Ledger, word mark, no logo | Needs confirmation |
| Goods or services in the user's words | bookkeeping software for independent shops | Carried into the draft |
| Markets they will sell in | Alberta and online, English. No other country listed | Carried into the draft |
| Names they have already seen in the wild | lumenledger.com was open on 12 Sep 2026. No register search in the file | Needs confirmation |

**How this draft was built**

**1. Describe the use**  
Word mark, logo, or both, and the goods or services in plain language.

**2. Collect lookalikes**  
Names the user has already found. Do not claim you searched a registry unless a tool in the conversation actually did, and even then do not call it legal clearance.

**3. List questions**  
Class of goods, confusingly similar marks, and domain or handle conflicts are questions for a search, not answers.

**4. Avoid false comfort**  
'I do not see a problem' is not an allowed conclusion.

**5. Recommend the next professional step**  
A qualified search in the jurisdictions they named.

**Deliberately not done**
- Clearing a name because a domain was available.
- Inventing trademark classes as if they were advice.
- Fake search results.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Elena Voss by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Clearing a name because a domain was available.
- Inventing trademark classes as if they were advice.
- Fake search results.

## Related skills

- `corporate-narrative`
- `brand-voice-guide`
- `ip-ownership-checklist`

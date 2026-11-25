---
name: vendor-contract-playbook
description: "Build a playbook of positions for a class of vendor contracts the company signs repeatedly. Use when the user mentions contract playbook, vendor paper positions, fallback positions, procurement legal playbook, or asks for a vendor contract playbook. Legal operations skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: legal
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'vendor-contract-playbook' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Vendor Contract Playbook

Build a playbook of positions for a class of vendor contracts the company signs repeatedly.

## When to use this skill

Use this skill when the user:

- contract playbook
- vendor paper positions
- fallback positions
- procurement legal playbook

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

- The contract type
- Positions the business already cares about
- Past concessions they regret
- Who may approve a fallback

## Workflow


### 1. Limit the scope

One contract type, such as SaaS subscriptions or contractors. A playbook for all contracts is a shelf ornament.
### 2. Write positions

Preferred, acceptable fallback, and walk-away, for a handful of clauses they actually negotiate.
### 3. Business owner

Each position names who may accept the fallback. Legal operations drafts. The business owns the risk trade.
### 4. Explain why

One sentence on the operational consequence, not a fake case citation.
### 5. Leave jurisdiction blank where needed

Note that counsel must localize governing law and liability positions.
### 6. No dark patterns

The playbook does not teach anyone to hide terms or to slip in rights the other side would not notice.

## Output

Deliver a **vendor contract playbook**.

- Purpose of this vendor contract playbook, in two sentences.
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

Elena Voss, operations lead at Northline Studio in Calgary, needs a vendor contract playbook by 30 September 2026. The company signs a similar SaaS order form every month and keeps conceding auto-renewal by accident.

### Example data

```text
From: Elena Voss, operations lead
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

The company signs a similar SaaS order form every month and keeps conceding auto-renewal by accident.

The contract type: unsigned draft, 8 pages, no signature date
Positions the business already cares about: Harbor renewal, recorded 14 September 2026. No supporting file attached
Past concessions they regret: Harbor renewal. Partly documented: the what is written down, the who is not
Who may approve a fallback: Elena Voss, operations lead
```

### Example outcome

**Vendor contract playbook**
To: Elena Voss, operations lead, Northline Studio
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
A short playbook with preferred and walk-away positions on renewal, liability, and data, plus a named approver for fallbacks.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The contract type | unsigned draft, 8 pages, no signature date | Needs confirmation |
| Positions the business already cares about | Harbor renewal, recorded 14 September 2026. No supporting file attached | Carried into the draft |
| Past concessions they regret | Harbor renewal. Partly documented: the what is written down, the who is not | Carried into the draft |
| Who may approve a fallback | Elena Voss, operations lead | Needs confirmation |

**How this draft was built**

**1. Limit the scope**  
One contract type, such as SaaS subscriptions or contractors. A playbook for all contracts is a shelf ornament.

**2. Write positions**  
Preferred, acceptable fallback, and walk-away, for a handful of clauses they actually negotiate.

**3. Business owner**  
Each position names who may accept the fallback. Legal operations drafts. The business owns the risk trade.

**4. Explain why**  
One sentence on the operational consequence, not a fake case citation.

**5. Leave jurisdiction blank where needed**  
Note that counsel must localize governing law and liability positions.

**Deliberately not done**
- A 40-clause encyclopedia nobody will use.
- Invented case law.
- Fallback authority left with 'the team'.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Elena Voss by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A 40-clause encyclopedia nobody will use.
- Invented case law.
- Fallback authority left with 'the team'.

## Related skills

- `contract-risk-review`
- `procurement-award-note`
- `data-processing-addendum`

---
name: esg-disclosure-outline
description: "Outline an ESG disclosure around metrics the company can evidence this year. Use when the user mentions ESG disclosure, sustainability report outline, nonfinancial disclosure, impact report, or asks for a disclosure outline. Sustainability skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: sustainability
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'esg-disclosure-outline' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# ESG Disclosure Outline

Outline an ESG disclosure around metrics the company can evidence this year.

## When to use this skill

Use this skill when the user:

- ESG disclosure
- sustainability report outline
- nonfinancial disclosure
- impact report

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Do not invent emissions factors or certification status. Label estimates. This is not an assurance opinion.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The audience
- Metrics they can evidence
- Framework language they already chose
- Gaps

## Workflow


### 1. Step 1

Include only metrics with a definition and a source.
### 2. Step 2

If they name a framework, use their mapping. Do not invent compliance with a standard.
### 3. Step 3

Put gaps in the outline so the report does not imply completeness.
### 4. Step 4

Separate targets from results.
### 5. Step 5

Avoid double-counting a story in every chapter.
### 6. Step 6

This outline is not assurance.

## Output

Deliver a **disclosure outline**.

- Purpose of this disclosure outline, in two sentences.
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

Devon Hale, reporting lead at Prairie Line Energy in Calgary, needs a disclosure outline by 30 September 2026. A report outline claims alignment with a standard nobody has mapped.

### Example data

```text
From: Devon Hale, reporting lead
Organization: Prairie Line Energy, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

A report outline claims alignment with a standard nobody has mapped.

The audience: people who already buy from Prairie Line Energy
Metrics they can evidence: one PDF, 2 pages, dated 14 September 2026
Framework language they already chose: their existing list, 6 lines. Two lines have no owner
Gaps: Scope 2 electricity is missing a source
```

### Example outcome

**Disclosure outline — draft ready to send**

> To: the recipient named in the file
> From: Devon Hale, reporting lead, Prairie Line Energy
> Date: 14 September 2026

---

Hello,

Labels alignment as not yet assessed and lists only sourced metrics.

Everything above comes from the file dated 14 September 2026. Where a figure, a date, or a commitment was not in that file, this note leaves it out rather than filling the gap.

One point is still open, and I would rather flag it than paper over it. I will confirm it before 30 September 2026 and follow up either way.

Devon Hale
reporting lead, Prairie Line Energy

---

**How this draft was checked**

1. **Include only metrics with a definition and a source**
2. **If they name a framework, use their mapping. Do not invent compliance with a standard**
3. **Put gaps in the outline so the report does not imply completeness**
4. **Separate targets from results**

**Deliberately not done**
- Implied certification.
- Targets written as results.
- Metrics with no source.

Next: Devon Hale sends after confirming the open point. Due 30 September 2026. This is a draft, not a sent message.

## Anti-patterns

- Implied certification
- Targets written as results
- Metrics with no source

## Related skills

- `emissions-inventory-brief`
- `management-reporting-pack`

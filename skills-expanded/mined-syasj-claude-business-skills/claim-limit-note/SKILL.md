---
name: claim-limit-note
description: "Limit a sentence to what the study design can support. Use when the user mentions overclaim, limit this sentence, what can we conclude, claim check, or asks for a claim note. Research skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: research
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'claim-limit-note' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Claim Limit

Limit a sentence to what the study design can support.

## When to use this skill

Use this skill when the user:

- overclaim
- limit this sentence
- what can we conclude
- claim check

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Do not fabricate citations, quotations, data, or participants. Separate evidence you were given from claims that still need a source.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The sentence
- The design
- The sample
- The outcome they measured

## Workflow


### 1. Step 1

Restate the design in one line.
### 2. Step 2

Cut words that say cause if they ran an association.
### 3. Step 3

Cut words that say people in general if the sample is one site.
### 4. Step 4

Do not add a policy recommendation the study did not test.
### 5. Step 5

Offer a replacement sentence.
### 6. Step 6

Keep the limit next to the claim.

## Output

Deliver a **claim note**.

- Purpose of this claim note, in two sentences.
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

The draft says the hiring workshop caused employment. The study was 20 interviews at one shop about how confident people felt after the workshop. No jobs were tracked.

### Example data

```text
sentence: "The workshop caused employment."
design: interviews, one site, no comparison group
sample: 20 staff, June 2026
measured: self-rated confidence, 1 to 5
not measured: jobs, wages, offers
```

### Example outcome

**Claim note**
Do not say the workshop caused employment. Jobs were not measured. The design cannot support cause.

Replacement: At this shop, 20 people rated their confidence after the workshop. This is not a finding about employment, and it is not a finding about other shops.
Keep that limit in the same paragraph as any confidence number.
No policy line. None was tested.

## Anti-patterns

- Cause language on an association
- A national claim from one site
- A policy line with no test

## Related skills

- `research-memo`
- `evidence-table`

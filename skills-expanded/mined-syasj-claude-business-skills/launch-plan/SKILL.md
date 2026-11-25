---
name: launch-plan
description: "Plan a launch as a coordinated set of proofs, enablement, and a rollback, not as a single announcement. Use when the user mentions launch plan, product launch, go-live marketing, announcement plan, or asks for a launch plan. Marketing skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: marketing
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'launch-plan' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Launch Plan

Plan a launch as a coordinated set of proofs, enablement, and a rollback, not as a single announcement.

## When to use this skill

Use this skill when the user:

- launch plan
- product launch
- go-live marketing
- announcement plan

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Do not invent testimonials, reviews, metrics, or claims the user cannot support. Do not draft spam, cloaking, fake scarcity, or impersonation.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- What is actually shipping
- The audience
- The date
- Risks and support readiness

## Workflow


### 1. Scope

Describe what a customer can do on launch day. Cut anything that is not ready from the announcement.
### 2. Audience and offer

Who is invited first, and what they are asked to do.
### 3. Enablement

Sales and support get the true scope, limits, and FAQ before the public post.
### 4. Proof

The story, screenshot, or customer quote that is approved. No placeholder quote.
### 5. Rollback

What you will say and do if the launch fails technically or the claim is wrong.
### 6. Readout

The date you will judge the launch against a pre-written success signal.

## Output

Deliver a **launch plan**.

- Purpose of this launch plan, in two sentences.
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

Lena Ortiz, marketing lead at Fieldnote in Edmonton, needs a launch plan by 30 September 2026. Marketing wants a public launch of a feature that still fails in the main browser.

### Example data

```text
From: Lena Ortiz, marketing lead
Organization: Fieldnote, Edmonton
Date: 14 September 2026
Needed by: 30 September 2026

Marketing wants a public launch of a feature that still fails in the main browser.

What is actually shipping: Local search ad, last reviewed 14 September 2026. No owner named since
The audience: people who already buy from Fieldnote
The date: 30 September 2026
Risks and support readiness: Fall service page is open. No score in the file
```

### Example outcome

**Launch plan**
To: Lena Ortiz, marketing lead, Fieldnote
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Holds the public claim, briefs support on the limit, and defines the rollback line.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| What is actually shipping | Local search ad, last reviewed 14 September 2026. No owner named since | Needs confirmation |
| The audience | people who already buy from Fieldnote | Carried into the draft |
| The date | 30 September 2026 | Carried into the draft |
| Risks and support readiness | Fall service page is open. No score in the file | Needs confirmation |

**How this draft was built**

**1. Scope**  
Describe what a customer can do on launch day. Cut anything that is not ready from the announcement.

**2. Audience and offer**  
Who is invited first, and what they are asked to do.

**3. Enablement**  
Sales and support get the true scope, limits, and FAQ before the public post.

**4. Proof**  
The story, screenshot, or customer quote that is approved. No placeholder quote.

**5. Rollback**  
What you will say and do if the launch fails technically or the claim is wrong.

**Deliberately not done**
- Announcing a feature that is not ready.
- A fake customer quote.
- No support briefing.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Lena Ortiz by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Announcing a feature that is not ready.
- A fake customer quote.
- No support briefing.

## Related skills

- `go-to-market-brief`
- `launch-readiness`

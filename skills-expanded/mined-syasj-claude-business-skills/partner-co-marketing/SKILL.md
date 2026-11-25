---
name: partner-co-marketing
description: "Plan a co-marketing activity with shared claims, shared approval, and no borrowed credibility. Use when the user mentions co-marketing, partner webinar, joint campaign, partner launch, or asks for a co-marketing plan. Marketing skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: marketing
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'partner-co-marketing' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Partner Co-Marketing

Plan a co-marketing activity with shared claims, shared approval, and no borrowed credibility.

## When to use this skill

Use this skill when the user:

- co-marketing
- partner webinar
- joint campaign
- partner launch

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

- The partner and the joint offer
- Approval path on both sides
- Claims each side can make
- The audience

## Workflow


### 1. Joint offer

What is actually being offered together. A logo swap is not a plan.
### 2. Claims

Each claim has an owner who can substantiate it. Neither side invents the other's metrics.
### 3. Approval

Both sides approve public copy. Build the time into the plan.
### 4. Audience

Whose audience is being asked, and whether that use is permitted. Do not assume list sharing is allowed.
### 5. Roles

Who builds, who speaks, who follows up.
### 6. Exit

What happens to leads and to the content after the event, in plain language.

## Output

Deliver a **co-marketing plan**.

- Purpose of this co-marketing plan, in two sentences.
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

Lena Ortiz, marketing lead at Fieldnote in Edmonton, needs a co-marketing plan by 30 September 2026. A team drafted a joint post that includes the partner's revenue and has not asked the partner.

### Example data

```text
From: Lena Ortiz, marketing lead
Organization: Fieldnote, Edmonton
Date: 14 September 2026
Needed by: 30 September 2026

A team drafted a joint post that includes the partner's revenue and has not asked the partner.

The partner and the joint offer: CAD 180, dates not set, cap not set
Approval path on both sides: Email to lapsed buyers. Partly documented: the what is written down, the who is not
Claims each side can make: the draft sentence is broader than the note
The audience: people who already buy from Fieldnote
```

### Example outcome

**Co-marketing plan**
To: Lena Ortiz, marketing lead, Fieldnote
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Strips the unapproved revenue claim and adds a written approval step before anything is published.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The partner and the joint offer | CAD 180, dates not set, cap not set | Needs confirmation |
| Approval path on both sides | Email to lapsed buyers. Partly documented: the what is written down, the who is not | Carried into the draft |
| Claims each side can make | the draft sentence is broader than the note | Carried into the draft |
| The audience | people who already buy from Fieldnote | Needs confirmation |

**How this draft was built**

**1. Joint offer**  
What is actually being offered together. A logo swap is not a plan.

**2. Claims**  
Each claim has an owner who can substantiate it. Neither side invents the other's metrics.

**3. Approval**  
Both sides approve public copy. Build the time into the plan.

**4. Audience**  
Whose audience is being asked, and whether that use is permitted. Do not assume list sharing is allowed.

**5. Roles**  
Who builds, who speaks, who follows up.

**Deliberately not done**
- Using a partner's logo without approval.
- Inventing the partner's results.
- Assuming you may email their list.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Lena Ortiz by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Using a partner's logo without approval.
- Inventing the partner's results.
- Assuming you may email their list.

## Related skills

- `pr-pitch`
- `campaign-brief`

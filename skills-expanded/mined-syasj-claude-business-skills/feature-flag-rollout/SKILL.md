---
name: feature-flag-rollout
description: "Plan a feature-flag rollout with an audience, a kill switch, and a cleanup date. Use when the user mentions feature flag, rollout plan, gradual release, kill switch, or asks for a rollout plan. Engineering skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: engineering
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'feature-flag-rollout' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Feature Flag Rollout

Plan a feature-flag rollout with an audience, a kill switch, and a cleanup date.

## When to use this skill

Use this skill when the user:

- feature flag
- rollout plan
- gradual release
- kill switch

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Prefer the repository's existing patterns. Do not disable security controls, invent credentials, or introduce network calls the user did not ask for.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The change
- The first audience
- How to disable it
- What you will watch

## Workflow


### 1. Audience

Who sees it first, and why. A 100 percent launch is a choice, not the default, when risk is unclear.
### 2. Kill switch

Who can turn it off, and how long that takes. A flag with no kill path is a config liability.
### 3. Watch

The user-facing signal that means stop. Use their metrics. Do not invent a dashboard.
### 4. Stages

The next audience and the evidence required to expand.
### 5. Cleanup

The date the flag is removed if the launch succeeds or fails. Permanent flags are debt.
### 6. Access

Do not put the flag service credentials in the plan.

## Output

Deliver a **rollout plan**.

- Purpose of this rollout plan, in two sentences.
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

Aisha Rahman, engineering lead at Fieldnote in Edmonton, needs a rollout plan by 30 September 2026. A team wants to enable a payments change for everyone and has no way to disable it without a deploy.

### Example data

```text
From: Aisha Rahman, engineering lead
Organization: Fieldnote, Edmonton
Date: 14 September 2026
Needed by: 30 September 2026

A team wants to enable a payments change for everyone and has no way to disable it without a deploy.

The change: requested 14 September 2026. Not yet approved
The first audience: people who already buy from Fieldnote
How to disable it: Invoice job, last reviewed 14 September 2026. No owner named since
What you will watch: Status page, last reviewed 14 September 2026. No owner named since
```

### Example outcome

**Rollout plan**
To: Aisha Rahman, engineering lead, Fieldnote
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Starts with a small audience and names a disable path that does not require a heroic deploy.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The change | requested 14 September 2026. Not yet approved | Needs confirmation |
| The first audience | people who already buy from Fieldnote | Carried into the draft |
| How to disable it | Invoice job, last reviewed 14 September 2026. No owner named since | Carried into the draft |
| What you will watch | Status page, last reviewed 14 September 2026. No owner named since | Needs confirmation |

**How this draft was built**

**1. Audience**  
Who sees it first, and why. A 100 percent launch is a choice, not the default, when risk is unclear.

**2. Kill switch**  
Who can turn it off, and how long that takes. A flag with no kill path is a config liability.

**3. Watch**  
The user-facing signal that means stop. Use their metrics. Do not invent a dashboard.

**4. Stages**  
The next audience and the evidence required to expand.

**5. Cleanup**  
The date the flag is removed if the launch succeeds or fails. Permanent flags are debt.

**Deliberately not done**
- A flag nobody can turn off.
- No cleanup date.
- Expanding while the watch signal is red.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Aisha Rahman by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A flag nobody can turn off.
- No cleanup date.
- Expanding while the watch signal is red.

## Related skills

- `release-checklist`
- `observability-plan`

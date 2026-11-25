---
name: shift-brief-hospitality
description: "Write a hospitality shift brief covering VIPs they named, misses, and eighty-six items. Use when the user mentions shift brief, pre-shift, hotel briefing, restaurant pre-shift, or asks for a shift brief. Hospitality skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: hospitality
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'shift-brief-hospitality' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Hospitality Shift Brief

Write a hospitality shift brief covering VIPs they named, misses, and eighty-six items.

## When to use this skill

Use this skill when the user:

- shift brief
- pre-shift
- hotel briefing
- restaurant pre-shift

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Guest recovery should be sincere and within policy. Do not invent compensation authority the user has not granted.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- Covers or occupancy
- Items they cannot sell
- Guest issues
- Staffing gaps

## Workflow


### 1. Step 1

Lead with safety and eighty-six items.
### 2. Step 2

Note guest issues without gossip.
### 3. Step 3

State staffing gaps that change service.
### 4. Step 4

Assign the person who handles a known problem.
### 5. Step 5

Do not include a guest's sensitive personal data.
### 6. Step 6

End with the one standard to watch this shift.

## Output

Deliver a **shift brief**.

- Purpose of this shift brief, in two sentences.
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

Sofia Alvarez, front office manager at Lantern Inn in Banff, needs a shift brief by 30 September 2026. A brief shares a guest's medical details with the whole dining team.

### Example data

```text
From: Sofia Alvarez, front office manager
Organization: Lantern Inn, Banff
Date: 14 September 2026
Needed by: 30 September 2026

A brief shares a guest's medical details with the whole dining team.

Covers or occupancy: Room block, 18 keys and one other, both unconfirmed as of 14 September 2026
Items they cannot sell: Friday dinner service, last reviewed 14 September 2026. No owner named since
Guest issues: Guest complaint 214, last reviewed 14 September 2026. No owner named since
Staffing gaps: Friday dinner service is missing a source
```

### Example outcome

**Shift brief**
To: Sofia Alvarez, front office manager, Lantern Inn
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Removes the medical details and keeps the operational accommodation only if needed.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| Covers or occupancy | Room block, 18 keys and one other, both unconfirmed as of 14 September 2026 | Needs confirmation |
| Items they cannot sell | Friday dinner service, last reviewed 14 September 2026. No owner named since | Carried into the draft |
| Guest issues | Guest complaint 214, last reviewed 14 September 2026. No owner named since | Carried into the draft |
| Staffing gaps | Friday dinner service is missing a source | Needs confirmation |

**How this draft was built**

**1. Lead with safety and eighty-six items**

**2. Note guest issues without gossip**

**3. State staffing gaps that change service**

**4. Assign the person who handles a known problem**

**5. Do not include a guest's sensitive personal data**

**Deliberately not done**
- Gossip.
- Sensitive personal data.
- A brief with no eighty-six list when items are down.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Sofia Alvarez by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Gossip
- Sensitive personal data
- A brief with no eighty-six list when items are down

## Related skills

- `shift-handover`
- `guest-recovery`

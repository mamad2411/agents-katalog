---
name: definition-of-done
description: "Write a definition of done that a team can apply to a backlog item without a debate each time. Use when the user mentions definition of done, DoD, when is it done, acceptance versus done, or asks for a definition of done. Project delivery skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: delivery
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'definition-of-done' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Definition of Done

Write a definition of done that a team can apply to a backlog item without a debate each time.

## When to use this skill

Use this skill when the user:

- definition of done
- DoD
- when is it done
- acceptance versus done

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Delivery plans are commitments only when owners and dates are real. Do not fabricate status to make a report look healthy.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The work type
- Quality bars they already require
- Review steps
- Exceptions

## Workflow


### 1. List the checks that apply to this work type

tested, reviewed, documented, monitored, as they actually require.
### 2. Step 2

Separate acceptance criteria, which are specific to a story, from done, which is the team's bar.
### 3. Step 3

Cut checks the team does not perform. A fictional done definition will be ignored.
### 4. Step 4

Say who confirms each check.
### 5. Step 5

Note exceptions, such as a spike, so they are explicit.
### 6. Step 6

Review the definition when it causes repeated arguments.

## Output

Deliver a **definition of done**.

- Purpose of this definition of done, in two sentences.
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

Owen Blake, delivery lead at Harbor Goods in Airdrie, needs a definition of done by 30 September 2026. The definition requires a help article, but nobody has written one in six months.

### Example data

```text
From: Owen Blake, delivery lead
Organization: Harbor Goods, Airdrie
Date: 14 September 2026
Needed by: 30 September 2026

The definition requires a help article, but nobody has written one in six months.

The work type: Milestone 3 handover; RAID item 12. Both unassigned as of 14 September 2026
Quality bars they already require: RAID item 12. Partly documented: the what is written down, the who is not
Review steps: Milestone 3 handover; RAID item 12. Both unassigned as of 14 September 2026
Exceptions: Milestone 3 handover is open. RAID item 12 was raised verbally and never logged
```

### Example outcome

**Definition of done**
To: Owen Blake, delivery lead, Harbor Goods
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Either restores the article check with an owner or removes it until the team means it.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The work type | Milestone 3 handover; RAID item 12. Both unassigned as of 14 September 2026 | Needs confirmation |
| Quality bars they already require | RAID item 12. Partly documented: the what is written down, the who is not | Carried into the draft |
| Review steps | Milestone 3 handover; RAID item 12. Both unassigned as of 14 September 2026 | Carried into the draft |
| Exceptions | Milestone 3 handover is open. RAID item 12 was raised verbally and never logged | Needs confirmation |

**How this draft was built**

**1. List the checks that apply to this work type**  
tested, reviewed, documented, monitored, as they actually require.

**2. Separate acceptance criteria, which are specific to a story, from done, which is the team's bar**

**3. Cut checks the team does not perform. A fictional done definition will be ignored**

**4. Say who confirms each check**

**5. Note exceptions, such as a spike, so they are explicit**

**Deliberately not done**
- A done definition nobody follows.
- Mixing story acceptance into the team bar.
- A check with no owner.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Owen Blake by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A done definition nobody follows
- Mixing story acceptance into the team bar
- A check with no owner

## Related skills

- `sprint-plan`
- `release-checklist`

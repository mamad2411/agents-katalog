---
name: project-closeout
description: "Close a project by confirming outcomes, handing over operations, and releasing the team. Use when the user mentions project closeout, project closure, handover to operations, end a project, or asks for a closeout note. Project delivery skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: delivery
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'project-closeout' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Project Closeout

Close a project by confirming outcomes, handing over operations, and releasing the team.

## When to use this skill

Use this skill when the user:

- project closeout
- project closure
- handover to operations
- end a project

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

- The charter outcome
- What was delivered
- Open issues
- The operational owner

## Workflow


### 1. Step 1

Compare delivery to the charter outcome. Partial delivery is labeled partial.
### 2. Step 2

List open issues and who owns them after close.
### 3. Step 3

Hand over runbooks, access, and support paths. Do not share passwords in the closeout note.
### 4. Step 4

Release people and budget explicitly so the project does not linger.
### 5. Step 5

Record a few lessons that change a template.
### 6. Step 6

Thank-you notes are optional. A fake success statement is not.

## Output

Deliver a **closeout note**.

- Purpose of this closeout note, in two sentences.
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

Owen Blake, delivery lead at Harbor Goods in Airdrie, needs a closeout note by 30 September 2026. A project is declared done while operations does not know how to support the new workflow.

### Example data

```text
From: Owen Blake, delivery lead
Organization: Harbor Goods, Airdrie
Date: 14 September 2026
Needed by: 30 September 2026

A project is declared done while operations does not know how to support the new workflow.

The charter outcome: A project is declared done while operations does not know how to support the new workflow. Stated once, in the ask. Not written down anywhere else
What was delivered: Change request 118, last reviewed 14 September 2026. No owner named since
Open issues: Milestone 3 handover is open. RAID item 12 was raised verbally and never logged
The operational owner: Owen Blake, delivery lead
```

### Example outcome

**Closeout note**
To: Owen Blake, delivery lead, Harbor Goods
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Blocks full closure until the operational owner and open issues are named.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The charter outcome | A project is declared done while operations does not know how to support the new workflow. Stated once, in the ask. Not written down anywhere else | Needs confirmation |
| What was delivered | Change request 118, last reviewed 14 September 2026. No owner named since | Carried into the draft |
| Open issues | Milestone 3 handover is open. RAID item 12 was raised verbally and never logged | Carried into the draft |
| The operational owner | Owen Blake, delivery lead | Needs confirmation |

**How this draft was built**

**1. Compare delivery to the charter outcome. Partial delivery is labeled partial**

**2. List open issues and who owns them after close**

**3. Hand over runbooks, access, and support paths. Do not share passwords in the closeout note**

**4. Release people and budget explicitly so the project does not linger**

**5. Record a few lessons that change a template**

**Deliberately not done**
- Closing with open issues and no owner.
- A success claim that ignores the charter.
- Passwords in the note.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Owen Blake by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Closing with open issues and no owner
- A success claim that ignores the charter
- Passwords in the note

## Related skills

- `lessons-learned`
- `sop-writer`

---
name: tabletop-exercise
description: "Plan a tabletop exercise that practices decisions under a security scenario without live attacks. Use when the user mentions tabletop exercise, incident drill, security tabletop, response practice, or asks for a tabletop plan. Security defense skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: security
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'tabletop-exercise' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Tabletop Exercise

Plan a tabletop exercise that practices decisions under a security scenario without live attacks.

## When to use this skill

Use this skill when the user:

- tabletop exercise
- incident drill
- security tabletop
- response practice

## When not to use this skill

- Live attacks
- Malware exercises

## Professional boundary

Defensive use only. Do not write exploits, payloads, bypasses, malware, or intrusion steps. Describe controls, ownership, detection, and safe verification.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The scenario type
- Participants
- Decisions to practice
- Time available

## Workflow


### 1. Write a scenario as a series of injects

what is known at minute 10, 30, and 60. No attack commands.
### 2. Pick decisions

contain, notify, and who has authority.
### 3. Step 3

Invite the real decision makers, not only security staff.
### 4. Step 4

Facilitate facts versus assumptions.
### 5. Step 5

Capture gaps in the contact tree, logs, or authority.
### 6. Step 6

End with a few owned actions. A tabletop with no actions was a meeting.

## Output

Deliver a **tabletop plan**.

- Purpose of this tabletop plan, in two sentences.
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

Aisha Rahman, engineering lead at Fieldnote in Edmonton, needs a tabletop plan by 30 September 2026. The team wants a 'realistic' exercise that sends malware to employees.

### Example data

```text
From: Aisha Rahman, engineering lead
Organization: Fieldnote, Edmonton
Date: 14 September 2026
Needed by: 30 September 2026

The team wants a 'realistic' exercise that sends malware to employees.

The scenario type: Access review Q3, recorded 14 September 2026. No supporting file attached
Participants: Aisha Rahman plus two others named in the thread. No distribution list attached
Decisions to practice: The team wants a 'realistic' exercise that sends malware to employees
Time available: five working days, due 30 September 2026
```

### Example outcome

**Tabletop plan**
To: Aisha Rahman, engineering lead, Fieldnote
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Practices notification decisions and refuses malware.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The scenario type | Access review Q3, recorded 14 September 2026. No supporting file attached | Needs confirmation |
| Participants | Aisha Rahman plus two others named in the thread. No distribution list attached | Carried into the draft |
| Decisions to practice | The team wants a 'realistic' exercise that sends malware to employees | Carried into the draft |
| Time available | five working days, due 30 September 2026 | Needs confirmation |

**How this draft was built**

**1. Write a scenario as a series of injects**  
what is known at minute 10, 30, and 60. No attack commands.

**2. Pick decisions**  
contain, notify, and who has authority.

**3. Invite the real decision makers, not only security staff**

**4. Facilitate facts versus assumptions**

**5. Capture gaps in the contact tree, logs, or authority**

**Deliberately not done**
- Live malware or a real phishing run disguised as a tabletop.
- A scenario with no decisions.
- No follow-up actions.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Aisha Rahman by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Live malware or a real phishing run disguised as a tabletop
- A scenario with no decisions
- No follow-up actions

## Related skills

- `incident-response-coord`
- `business-continuity`

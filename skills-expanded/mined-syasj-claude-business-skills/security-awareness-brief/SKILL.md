---
name: security-awareness-brief
description: "Draft a short awareness brief for a real behavior, without fear theater or trick phishing against employees. Use when the user mentions security awareness, teach the team this control, security reminder, phishing awareness brief, or asks for a awareness brief. Security defense skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: security
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'security-awareness-brief' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Security Awareness Brief

Draft a short awareness brief for a real behavior, without fear theater or trick phishing against employees.

## When to use this skill

Use this skill when the user:

- security awareness
- teach the team this control
- security reminder
- phishing awareness brief

## When not to use this skill

- Building phishing kits or credential-harvest pages

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

- The behavior to change
- The recent incident or risk they can describe
- The audience
- The approved reporting path

## Workflow


### 1. Teach one behavior

how to report, how to store a secret, or how to verify a request.
### 2. Step 2

Use a real internal example only if the user approves it and it does not shame a named person.
### 3. Step 3

Give the approved reporting path.
### 4. Step 4

Do not design a deceptive phishing exercise unless their security owner explicitly asked for a training plan, and even then do not write malware or credential-harvest pages.
### 5. Step 5

Keep it short enough to read.
### 6. Step 6

Measure a behavior, such as reports submitted, not a quiz score alone.

## Output

Deliver a **awareness brief**.

- Purpose of this awareness brief, in two sentences.
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

Aisha Rahman, engineering lead at Fieldnote in Edmonton, needs an awareness brief by 30 September 2026. A manager wants to embarrass an employee who clicked a bad link by naming them in an all-hands.

### Example data

```text
From: Aisha Rahman, engineering lead
Organization: Fieldnote, Edmonton
Date: 14 September 2026
Needed by: 30 September 2026

A manager wants to embarrass an employee who clicked a bad link by naming them in an all-hands.

The behavior to change: requested 14 September 2026. Not yet approved
The recent incident or risk they can describe: Access review Q3 is open. No score in the file
The audience: people who already buy from Fieldnote
The approved reporting path: one file, dated 14 September 2026. No earlier version attached for comparison
```

### Example outcome

**Awareness brief**
To: Aisha Rahman, engineering lead, Fieldnote
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Teaches reporting, omits the name, and refuses public shaming.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The behavior to change | requested 14 September 2026. Not yet approved | Needs confirmation |
| The recent incident or risk they can describe | Access review Q3 is open. No score in the file | Carried into the draft |
| The audience | people who already buy from Fieldnote | Carried into the draft |
| The approved reporting path | one file, dated 14 September 2026. No earlier version attached for comparison | Needs confirmation |

**How this draft was built**

**1. Teach one behavior**  
how to report, how to store a secret, or how to verify a request.

**2. Use a real internal example only if the user approves it and it does not shame a named person**

**3. Give the approved reporting path**

**4. Do not design a deceptive phishing exercise unless their security owner explicitly asked for a training plan, and even then do not write malware or credential-harvest pages**

**5. Keep it short enough to read**

**Deliberately not done**
- Shame a named colleague.
- Malware or fake login pages.
- A long lecture with no behavior.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Aisha Rahman by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Shame a named colleague
- Malware or fake login pages
- A long lecture with no behavior

## Related skills

- `security-policy-draft`
- `tabletop-exercise`

---
name: incident-response-coord
description: "Coordinate a security incident response with roles, containment, and communications that do not speculate. Use when the user mentions security incident, possible breach, incident commander notes, response coordination, or asks for a incident coordination note. Security defense skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: security
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'incident-response-coord' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Incident Response Coordination

Coordinate a security incident response with roles, containment, and communications that do not speculate.

## When to use this skill

Use this skill when the user:

- security incident
- possible breach
- incident commander notes
- response coordination

## When not to use this skill

- Hacking back
- Evidence destruction

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

- What is known
- Systems affected
- Who is in charge
- Legal or regulatory contacts they already have

## Workflow


### 1. Step 1

Separate facts from theories. Write both, labeled.
### 2. Assign roles

lead, communications, and a note taker. Everyone else stays available, not in the room.
### 3. Step 3

Containment actions must be authorized and reversible where possible. Do not include intrusion or retaliation steps.
### 4. Step 4

Preserve evidence. Do not tell anyone to wipe logs to hide the event.
### 5. Communications

tell affected parties only what counsel or the incident lead has approved as known.
### 6. Step 6

Set the next update time. A response without a clock drifts.

## Output

Deliver a **incident coordination note**.

- Purpose of this incident coordination note, in two sentences.
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

Aisha Rahman, engineering lead at Fieldnote in Edmonton, needs an incident coordination note by 30 September 2026. A chat is about to tell customers data was stolen before anyone has confirmed access.

### Example data

```text
From: Aisha Rahman, engineering lead
Organization: Fieldnote, Edmonton
Date: 14 September 2026
Needed by: 30 September 2026

A chat is about to tell customers data was stolen before anyone has confirmed access.

What is known: Phishing report 4412, last reviewed 14 September 2026. No owner named since
Systems affected: the one named in the ask. Version and owner not recorded
Who is in charge: Aisha Rahman, engineering lead
Legal or regulatory contacts they already have: Phishing report 4412 and one other, both unconfirmed as of 14 September 2026
```

### Example outcome

**Incident coordination note**
To: Aisha Rahman, engineering lead, Fieldnote
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Holds the claim, assigns a lead, and forbids log destruction.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| What is known | Phishing report 4412, last reviewed 14 September 2026. No owner named since | Needs confirmation |
| Systems affected | the one named in the ask. Version and owner not recorded | Carried into the draft |
| Who is in charge | Aisha Rahman, engineering lead | Carried into the draft |
| Legal or regulatory contacts they already have | Phishing report 4412 and one other, both unconfirmed as of 14 September 2026 | Needs confirmation |

**How this draft was built**

**1. Separate facts from theories. Write both, labeled**

**2. Assign roles**  
lead, communications, and a note taker. Everyone else stays available, not in the room.

**3. Containment actions must be authorized and reversible where possible. Do not include intrusion or retaliation steps**

**4. Preserve evidence. Do not tell anyone to wipe logs to hide the event**

**5. Communications**  
tell affected parties only what counsel or the incident lead has approved as known.

**Deliberately not done**
- Wiping logs.
- Speculative customer claims.
- Retaliation or hacking back.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Aisha Rahman by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Wiping logs
- Speculative customer claims
- Retaliation or hacking back

## Related skills

- `incident-postmortem`
- `tabletop-exercise`

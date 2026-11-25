---
name: legal-hold-notice
description: "Draft a plain legal-hold notice for counsel to approve, telling people to preserve records without spoiling anything. Use when the user mentions legal hold, litigation hold notice, preserve documents, hold notice, or asks for a legal hold notice draft. Legal operations skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: legal
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'legal-hold-notice' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Legal Hold Notice Draft

Draft a plain legal-hold notice for counsel to approve, telling people to preserve records without spoiling anything.

## When to use this skill

Use this skill when the user:

- legal hold
- litigation hold notice
- preserve documents
- hold notice

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

This is not legal advice and does not create an attorney-client relationship. Do not invent statutes, case names, or filing deadlines. Drafts are for qualified counsel in the relevant jurisdiction.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The matter name counsel is using
- Who may have relevant records
- Systems those people use
- The counsel approver

## Workflow


### 1. Write for humans

What to preserve, in everyday examples such as email, chat, and files, based on systems the user named.
### 2. Say why briefly

A matter exists and records must be kept. Do not speculate about guilt or strategy.
### 3. Forbid destruction

Include a clear line that routine deletion of relevant records must pause. Do not include tips for concealing records.
### 4. Name a contact

Questions go to the counsel contact the user provides, not to a hallway conversation.
### 5. Acknowledge

Ask for a confirmation line counsel can track.
### 6. Approval gate

The draft is not sent until the named counsel approves it.

## Output

Deliver a **legal hold notice draft**.

- Purpose of this legal hold notice draft, in two sentences.
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

Elena Voss, operations lead at Northline Studio in Calgary, needs a legal hold notice draft by 30 September 2026. Counsel asked operations to warn three teams to keep project email, and the current draft sounds like an accusation.

### Example data

```text
From: Elena Voss, operations lead
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

Counsel asked operations to warn three teams to keep project email, and the current draft sounds like an accusation.

The matter name counsel is using: Harbor renewal, recorded 14 September 2026. No supporting file attached
Who may have relevant records: Elena Voss, operations lead
Systems those people use: the one named in the ask. Version and owner not recorded
The counsel approver: Elena Voss. They have not signed
```

### Example outcome

**Legal hold notice draft**
To: Elena Voss, operations lead, Northline Studio
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Lists the systems, requires preservation, and waits for counsel approval.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The matter name counsel is using | Harbor renewal, recorded 14 September 2026. No supporting file attached | Needs confirmation |
| Who may have relevant records | Elena Voss, operations lead | Carried into the draft |
| Systems those people use | the one named in the ask. Version and owner not recorded | Carried into the draft |
| The counsel approver | Elena Voss. They have not signed | Needs confirmation |

**How this draft was built**

**1. Write for humans**  
What to preserve, in everyday examples such as email, chat, and files, based on systems the user named.

**2. Say why briefly**  
A matter exists and records must be kept. Do not speculate about guilt or strategy.

**3. Forbid destruction**  
Include a clear line that routine deletion of relevant records must pause. Do not include tips for concealing records.

**4. Name a contact**  
Questions go to the counsel contact the user provides, not to a hallway conversation.

**5. Acknowledge**  
Ask for a confirmation line counsel can track.

**Deliberately not done**
- A notice that argues the case.
- Instructions that help someone hide records.
- Sending the notice without counsel approval.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Elena Voss by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A notice that argues the case.
- Instructions that help someone hide records.
- Sending the notice without counsel approval.

## Related skills

- `dispute-intake`
- `records-retention`
- `outside-counsel-brief`

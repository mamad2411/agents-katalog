---
name: desk-handoff
description: "Hand a story to the next shift with what is confirmed, what is open, and who owns the next call. Use when the user mentions desk handoff, shift handoff news, story handoff, night desk note, or asks for a handoff. Media and communications skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: media
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'desk-handoff' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Desk Handoff

Hand a story to the next shift with what is confirmed, what is open, and who owns the next call.

## When to use this skill

Use this skill when the user:

- desk handoff
- shift handoff news
- story handoff
- night desk note

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Do not fabricate quotes, sources, or images. Label opinion. Do not draft impersonation or defamation.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- What is confirmed
- What is open
- The next call
- The deadline

## Workflow


### 1. Step 1

Lead with confirmed facts.
### 2. Step 2

List open questions.
### 3. Step 3

Name the next person to call and whether they have already been called.
### 4. Step 4

Do not leave a quote half-checked.
### 5. Step 5

Pass documents by name.
### 6. Step 6

Say what the next shift must not publish yet.

## Output

Deliver a **handoff**.

- Purpose of this handoff, in two sentences.
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

Jonah is leaving at 18:00. The night desk has one editor. The staffing-cut version has no document. The statement version is ready.

### Example data

```text
confirmed: statement dates, 22 Sep start, ten days
open: staffing, no document, spokesperson has not replied
next call: none queued
night staff: one editor, no reporter
must not publish: the staffing-cut version
```

### Example outcome

**Handoff**
Publishable: the statement dates only, if the night editor wants a brief.
Not publishable: any staffing-cut line.
Open: spokesperson reply. Nobody is queued to call again tonight.
Do not leave the night editor to 'find a worker'. That source is not in the log.
Documents: the 15 September statement, in the story folder.

## Anti-patterns

- A handoff that is only enthusiasm
- An open quote treated as checked
- No owner for the next call

## Related skills

- `source-log-news`
- `shift-handover`

---
name: live-blog-update
description: "Add one timestamped update from a new sourced fact, without mixing it into older items. Use when the user mentions live blog, news update, developing story, timestamped update, or asks for a live update. Media and communications skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: media
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'live-blog-update' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Live Update

Add one timestamped update from a new sourced fact, without mixing it into older items.

## When to use this skill

Use this skill when the user:

- live blog
- news update
- developing story
- timestamped update

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

- The new fact
- The source
- The time
- What is still unconfirmed

## Workflow


### 1. Step 1

Time-stamp the update.
### 2. Step 2

Attribute the new fact.
### 3. Step 3

Do not merge it into an older item so the time looks earlier.
### 4. Step 4

Say what is still unconfirmed.
### 5. Step 5

Correct an earlier item in a new line, do not silently change it.
### 6. Step 6

Stop if the fact has no source.

## Output

Deliver a **live update**.

- Purpose of this live update, in two sentences.
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

At 11:00 the live blog guessed the turnaround might start Sunday. At 14:10 a spokesperson confirmed Monday 22 September. Jonah needs the update line.

### Example data

```text
earlier item: 11:00, "may start Sunday", no source named
new fact: spokesperson, on the record, 14:10, starts Monday 22 Sep, ten days
still unconfirmed: staffing, cause, which units
clock zone: America/Edmonton
```

### Example outcome

**Update — 14:10**
A spokesperson said on the record that the turnaround starts Monday 22 September and is planned for ten days.

Still unconfirmed: staffing, cause, which units. Do not add them here.

Correction: the 11:00 item guessed Sunday and named no source. It stands as a bad item. Do not edit it into Monday. Point readers to this line.

## Anti-patterns

- A silent edit of an old timestamp
- An unconfirmed line written as fact
- No source

## Related skills

- `correction-note`
- `news-assignment`

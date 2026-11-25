---
name: local-seo-note
description: "Check a local listing and a location page against the name, address, and phone the user uses. Use when the user mentions local SEO, Google Business, NAP, location page, or asks for a local note. Search skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: seo
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'local-seo-note' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Local SEO Note

Check a local listing and a location page against the name, address, and phone the user uses.

## When to use this skill

Use this skill when the user:

- local SEO
- Google Business
- NAP
- location page

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Do not draft cloaking, doorway pages, hidden text, fake reviews, or link schemes. Use only queries and pages the user can show.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The name, address, and phone they use
- The listing as they see it
- The location page
- Hours

## Workflow


### 1. Step 1

Compare name, address, and phone.
### 2. Step 2

Note mismatches. Do not 'fix' them with a different address.
### 3. Step 3

Hours must match the door.
### 4. Step 4

Do not invent reviews or ask for fake ones.
### 5. Step 5

Categories must match the work they do.
### 6. Step 6

Say who edits the listing.

## Output

Deliver a **local note**.

- Purpose of this local note, in two sentences.
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

Harbor Goods' door is closed Sunday. The listing Diane looked at on 18 September says open Sunday 10 to 4. The phone matches. The listing category is 'plumber'.

### Example data

```text
name on the door: Harbor Goods
address: 18 Centre Ave, Airdrie
phone: 403-555-0148
listing hours: Sun 10:00-16:00
door hours: closed Sunday, Mon-Sat 08:00-17:00
listing category: plumber
work they do: furnace and oil change
who can edit: Diane
```

### Example outcome

**Local note**
Change Sunday to closed. The door is the source.
Leave the phone. It matches.
Change the category off plumber. She does not do that work. Use a category that matches furnace or auto service only if the listing offers that exact label. If she is unsure of the label, she picks it in the product, not in this note.
Do not ask anyone for a fake review.
Editor: Diane.

## Anti-patterns

- Fake reviews
- A listing address they do not occupy
- A category for work they do not do

## Related skills

- `search-intent`
- `keyword-map`

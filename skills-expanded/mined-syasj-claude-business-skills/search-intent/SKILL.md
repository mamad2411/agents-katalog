---
name: search-intent
description: "Say what the searcher is trying to do, from the query and the page the user has. Use when the user mentions search intent, what does this query want, intent mismatch, query vs page, or asks for a intent note. Search skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: seo
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'search-intent' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Search Intent

Say what the searcher is trying to do, from the query and the page the user has.

## When to use this skill

Use this skill when the user:

- search intent
- what does this query want
- intent mismatch
- query vs page

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

- The query
- The page
- What the page actually answers
- What the searcher likely needs done

## Workflow


### 1. Step 1

Restate the query.
### 2. Step 2

Say what the page answers in one sentence.
### 3. Step 3

If those differ, say mismatch.
### 4. Step 4

Recommend a change to the page or a different query.
### 5. Step 5

Do not stuff the query into a page that answers something else.
### 6. Step 6

Use their wording for the job-to-be-done.

## Output

Deliver a **intent note**.

- Purpose of this intent note, in two sentences.
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

The query Diane cares about is 'furnace repair Airdrie'. The furnace page tells the shop's origin story and does not list the city, the phone, or what a repair visit includes.

### Example data

```text
query: furnace repair Airdrie
page: /services/furnace
page answers: how the shop started in 2014
searcher job: find someone who will come fix a furnace in Airdrie
phone on the home page: 403-555-0148
phone on this page: absent
```

### Example outcome

**Intent note**
Mismatch. The query asks for a repair in Airdrie. The page answers a brand story.

Do not stuff the query into the origin paragraph.
Add, if she can stand behind it: the city, the phone that is already on the home page, and what a repair visit includes. She has not written the visit scope. Leave that blank rather than inventing a promise.
Until those facts are on the page, this URL does not answer the query.

## Anti-patterns

- Query stuffing
- A mismatch ignored
- Intent copied from a tool they did not run

## Related skills

- `keyword-map`
- `local-seo-note`

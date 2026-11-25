---
name: reviewer-response
description: "Draft a response to reviewer comments from the changes the authors actually made. Use when the user mentions reviewer response, respond to reviewers, revision letter, peer review reply, or asks for a response draft. Research skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: research
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'reviewer-response' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Reviewer Response

Draft a response to reviewer comments from the changes the authors actually made.

## When to use this skill

Use this skill when the user:

- reviewer response
- respond to reviewers
- revision letter
- peer review reply

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Do not fabricate citations, quotations, data, or participants. Separate evidence you were given from claims that still need a source.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The comments
- The changes made
- The comments they will not follow
- The page or line they can cite

## Workflow


### 1. Step 1

Answer the comment they received, not a softer version.
### 2. Step 2

Point to the change they made.
### 3. Step 3

If they did not change it, say so and why.
### 4. Step 4

Do not invent a new analysis to please a reviewer.
### 5. Step 5

Do not insult the reviewer.
### 6. Step 6

Keep each reply next to its comment.

## Output

Deliver a **response draft**.

- Purpose of this response draft, in two sentences.
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

Reviewer 2 asked for a second dataset from another town. Nia did not collect one. She did add a sentence limiting the claim to one site.

### Example data

```text
comment: collect a comparison dataset from a second town
change made: paragraph 4 now says one site, 20 interviews
change not made: no second dataset
line to cite: paragraph 4, revision 18 Sep 2026
tone: direct
```

### Example outcome

**Response**
Reviewer 2 asked for a second dataset. We did not collect one. We cannot add a table we do not have.

What changed: paragraph 4 now limits the claim to this site and these 20 interviews (revision 18 September 2026).
What did not change: the sample. A second town is future work, not this paper.
No new experiment is described.

## Anti-patterns

- A fake new experiment
- A reply to a comment they were not sent
- A rude rebuttal

## Related skills

- `research-memo`
- `claim-limit-note`

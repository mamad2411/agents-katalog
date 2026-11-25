---
name: right-of-reply
description: "Record what a person was asked, what they answered, and the deadline they were given. Use when the user mentions right of reply, comment request, fair comment, response deadline, or asks for a reply note. Media and communications skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: media
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'right-of-reply' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Right of Reply

Record what a person was asked, what they answered, and the deadline they were given.

## When to use this skill

Use this skill when the user:

- right of reply
- comment request
- fair comment
- response deadline

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

- The specific claim they were asked about
- When they were asked
- What they replied
- The deadline

## Workflow


### 1. Step 1

Write the claim in the words that will be published.
### 2. Step 2

Record the ask time and the deadline.
### 3. Step 3

Record the reply verbatim or say they did not reply.
### 4. Step 4

Do not paraphrase a no-comment into agreement.
### 5. Step 5

If the deadline has not passed, the story does not say they refused.
### 6. Step 6

Keep the note with the story.

## Output

Deliver a **reply note**.

- Purpose of this reply note, in two sentences.
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

An editor wants to write that the company refused to comment on a staffing cut. The ask went out at 16:00 for a 17:00 deadline, and the story cannot source the cut.

### Example data

```text
claim they would be asked about: a safety-staff cut
ask sent: 15 Sep 2026 16:00
deadline given: 15 Sep 17:00
reply: none by 17:00
can the story source the cut: no
```

### Example outcome

**Reply note**
Do not write that they refused, and do not publish the cut.

The ask gave one hour, at the end of the day, about a claim the story cannot source.
No reply by 17:00 is not a refusal in this note. The deadline was not a fair window, and the claim is not ready.
Next: if the story becomes the turnaround dates only, a comment on staffing is unnecessary.

## Anti-patterns

- A no-comment turned into agreement
- A deadline that already passed before the ask
- A vague 'we reached out'

## Related skills

- `news-assignment`
- `interview-prep-comms`

---
name: prompt-library-card
description: "Turn a working prompt into a library card with a name, inputs, and a known failure. Use when the user mentions save this prompt, prompt library, reusable prompt, prompt card, or asks for a library card. Creator, social, and prompting skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: creator
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'prompt-library-card' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Prompt Library Card

Turn a working prompt into a library card with a name, inputs, and a known failure.

## When to use this skill

Use this skill when the user:

- save this prompt
- prompt library
- reusable prompt
- prompt card

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Creator work must be original and honest. Do not copy another person's script, footage, voice, or caption. Do not invent metrics, fake engagement, or undisclosed sponsorships. Do not impersonate a real person. Prompt skills must not weaken safety rules.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The working prompt
- The job it does
- Required inputs
- A failure they already saw

## Workflow


### 1. Step 1

Name the card by the job, not by 'super prompt'.
### 2. Step 2

List required inputs.
### 3. Step 3

Paste the prompt only if it is the user's own. Do not store a copied jailbreak or a leaked private prompt.
### 4. Step 4

Record one failure and the fix.
### 5. Step 5

Note the model family only if the user tested it. Do not claim it works everywhere.
### 6. Step 6

Version the card when the prompt changes.

## Output

Deliver a **library card**.

- Purpose of this library card, in two sentences.
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

Fieldnote has three copies of the support prompt in three docs. Jonah wants one card so people stop pasting the old 'be helpful' line.

### Example data

```text
name: support-reply-draft
owner: Jonah Park
reviewer: Rita Santos
source allowed: ticket text
last failure: 4412, invented $20 refund, 14 Sep 2026
last edit: removed "be helpful and resolve"
status: test again on 4412 before anyone else uses it
```

### Example outcome

**Card — support-reply-draft**
Owner: Jonah Park. Reviewer: Rita Santos.
Use when: a support agent wants a draft from one ticket.
Source: that ticket only.
Must not: invent a refund, a credit, a policy, or a cause.
Last test: failed 14 September on ticket 4412.
Status: do not share the card until 4412 is rerun and has no dollar amount.
Old copies in the other two docs: delete the 'be helpful' line. This card is the one.

## Anti-patterns

- A stored jailbreak
- A claim that it works on every model
- No required inputs

## Related skills

- `prompt-boundary-check`
- `skill-authoring`

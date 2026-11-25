---
name: prompt-revision
description: "Revise a prompt that failed by naming the failure and changing one instruction. Use when the user mentions fix this prompt, prompt revision, the model ignored me, improve my prompt, or asks for a revised prompt. Creator, social, and prompting skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: creator
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'prompt-revision' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Prompt Revision

Revise a prompt that failed by naming the failure and changing one instruction.

## When to use this skill

Use this skill when the user:

- fix this prompt
- prompt revision
- the model ignored me
- improve my prompt

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

- The current prompt
- The bad output
- What good would have looked like
- Which fact was missing

## Workflow


### 1. Quote the failure

invented fact, wrong format, or too long.
### 2. Step 2

Change one instruction that would have prevented it.
### 3. Step 3

Add a line that missing inputs stay missing.
### 4. Step 4

Do not add threats, role-play overrides, or 'do not refuse'.
### 5. Step 5

Keep the prompt shorter than the failed one if length was the problem.
### 6. Step 6

Show the revised prompt and one sentence on what changed.

## Output

Deliver a **revised prompt**.

- Purpose of this revised prompt, in two sentences.
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

Jonah's prompt told the model to 'be helpful and resolve the issue'. On ticket 4412 it invented a refund. He wants the prompt revised against that failure.

### Example data

```text
old line: "be helpful and resolve the issue"
failure: ticket 4412, model offered a $20 refund the agent had not approved
source allowed: ticket text only
new rule he wants: if a money action is not in the ticket, do not propose one
test: the same ticket, run again after the edit
```

### Example outcome

**Revision**
Remove: "be helpful and resolve the issue."

Add: Use only the ticket text. Do not propose a refund, credit, or fee. If the customer asks for money back, say a person will decide. Do not name an amount.

**Why**
Ticket 4412 came back with a $20 refund no one approved.

**Test**
Run 4412 again. Pass means no dollar amount and no refund offer. One test is not a full eval.

## Anti-patterns

- A longer prompt that hides the same gap
- A do-not-refuse line
- Five changes at once

## Related skills

- `prompt-brief`
- `prompt-library-card`

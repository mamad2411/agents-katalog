---
name: prompt-brief
description: "Brief a prompt so the model knows the job, the inputs, and the lines it must not cross. Use when the user mentions write a prompt, prompt brief, how should I prompt this, prompt for Claude, or asks for a prompt brief. Creator, social, and prompting skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: creator
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'prompt-brief' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Prompt Brief

Brief a prompt so the model knows the job, the inputs, and the lines it must not cross.

## When to use this skill

Use this skill when the user:

- write a prompt
- prompt brief
- how should I prompt this
- prompt for Claude

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

- The job to be done
- The inputs the user will paste
- The output shape
- The refusals

## Workflow


### 1. Step 1

State the job in one sentence.
### 2. Step 2

List the inputs the user will provide. Tell the model not to invent missing inputs.
### 3. Define the output

headings, length, or a table.
### 4. Write refusals

no fake citations, no copied third-party script, no credentials.
### 5. Step 5

Add one example of a good result only if the user supplied the facts in that example.
### 6. Step 6

Do not write a prompt whose purpose is to ignore safety rules.

## Output

Deliver a **prompt brief**.

- Purpose of this prompt brief, in two sentences.
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

Jonah at Fieldnote wants a prompt that turns a customer's own support note into a reply draft. He does not want the model to invent a refund. The source is one note the customer wrote.

### Example data

```text
job: draft a reply the agent can edit
source: the customer note in the ticket, nothing else
must not: invent a refund, a policy, or a cause
tone: short, no blame
reviewer: Rita, support lead, before send
ticket sample: "charged twice on 12 Sep, order 4412"
```

### Example outcome

**Prompt brief**
Job: draft a reply. A person sends it.

Source: only the text in the ticket. If the order is not in the ticket, the draft says it is not in the ticket.

Stop: do not offer a refund, a credit, or a cause. Rita decides those.
Tone: short. No blame.

Review: Rita reads it before it is sent. The draft is not the reply.

## Anti-patterns

- A jailbreak prefix
- A prompt that tells the model to invent sources
- No output shape

## Related skills

- `prompt-boundary-check`
- `prompt-revision`

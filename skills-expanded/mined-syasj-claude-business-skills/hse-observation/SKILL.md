---
name: hse-observation
description: "Log a safety observation in the words the observer used, with the immediate step they took. Use when the user mentions HSE observation, safety observation, near miss log, site observation, or asks for a observation log. Oil and gas operations skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: oil-gas
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'hse-observation' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# HSE Observation

Log a safety observation in the words the observer used, with the immediate step they took.

## When to use this skill

Use this skill when the user:

- HSE observation
- safety observation
- near miss log
- site observation

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Operational drafts only. Do not bypass isolation, lockout, permits, or reporting duties. Do not write instructions to conceal a release or to operate outside the site's limits.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- What they saw
- Where
- The immediate step
- Who owns the follow-up

## Workflow


### 1. Step 1

Use their words for what they saw.
### 2. Step 2

Do not diagnose a medical outcome.
### 3. Step 3

Record the immediate step.
### 4. Step 4

Name the follow-up owner.
### 5. Step 5

Do not name a worker in a wide report if they asked not to.
### 6. Step 6

Do not bury a stop-work in soft language.

## Output

Deliver a **observation log**.

- Purpose of this observation log, in two sentences.
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

An observer stopped a job at pad 14-22 because a lock was missing on a valve. A draft for the weekly pack calls it a coaching moment and names the worker.

### Example data

```text
when: 15 Sep 2026 10:20
where: pad 14-22, valve on the fuel gas line
what they saw: no lock, job in progress
immediate step: job stopped
observer asked: do not name the worker in the wide pack
follow-up owner: Devon Hale
```

### Example outcome

**Observation**
15 September, 10:20, pad 14-22. No lock on the fuel-gas valve. Job was in progress. The job was stopped.
This is a stop-work, not a coaching moment.
Worker name: omitted from the wide pack, as asked.
Follow-up owner: Devon Hale. The lock stays the issue until he closes it.
No medical description. None was reported.

## Anti-patterns

- A medical diagnosis
- A stop-work rewritten as a suggestion
- No owner

## Related skills

- `turnaround-ready`
- `safety-toolbox-talk`

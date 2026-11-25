---
name: warranty-file-review
description: "Check a warranty file for the documents their checklist requires before it is submitted. Use when the user mentions warranty file, claim packet, warranty submission, OEM claim, or asks for a file review. Automotive skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: automotive
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'warranty-file-review' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Warranty File Review

Check a warranty file for the documents their checklist requires before it is submitted.

## When to use this skill

Use this skill when the user:

- warranty file
- claim packet
- warranty submission
- OEM claim

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Not a repair procedure for safety-critical systems and not a recall determination. Do not invent defect rates or tell anyone to disable a safety feature.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- Their checklist
- Documents in the file
- The failed part
- The tech notes

## Workflow


### 1. Step 1

Compare to their checklist.
### 2. Step 2

A missing photo or code is a hole.
### 3. Step 3

Do not write a cause the tech did not write.
### 4. Step 4

Do not change the odometer.
### 5. Step 5

Name who submits.
### 6. Step 6

This review does not decide goodwill.

## Output

Deliver a **file review**.

- Purpose of this file review, in two sentences.
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

A warranty file for the failed pads has the RO and the odometer. The photo is missing. The cause line is blank. A clerk offered to write 'worn' so the claim can go tonight.

### Example data

```text
checklist: RO, odometer, photo of failed part, tech cause line
in the file: RO 4418, odometer 61240
missing: photo, tech cause
offered wording: worn
submitter: Carla, not the clerk
```

### Example outcome

**File review**
Hold. Photo missing. Cause line blank.
Do not type 'worn'. The tech did not write it. Do not touch the odometer.
Submitter is Carla, after the photo and the tech's own words are in the file.
This review does not grant goodwill and does not submit the claim.

## Anti-patterns

- A cause the tech did not write
- An altered odometer
- A file marked ready with a hole

## Related skills

- `recall-owner-note`
- `service-lane-plan`

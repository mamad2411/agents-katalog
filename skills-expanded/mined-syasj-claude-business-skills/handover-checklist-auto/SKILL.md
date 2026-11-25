---
name: handover-checklist-auto
description: "Check a handover against the items the dealer says the customer must see. Use when the user mentions vehicle handover, delivery checklist, customer delivery, new car handover, or asks for a handover checklist. Automotive skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: automotive
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'handover-checklist-auto' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Vehicle Handover

Check a handover against the items the dealer says the customer must see.

## When to use this skill

Use this skill when the user:

- vehicle handover
- delivery checklist
- customer delivery
- new car handover

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

- Their handover list
- Items done
- The recall status they checked
- The salesperson

## Workflow


### 1. Step 1

Walk their list.
### 2. Step 2

A missed item is open.
### 3. Step 3

Recall status is whatever the check showed, including not checked.
### 4. Step 4

Do not say a recall is clear if they did not run it.
### 5. Step 5

Name who hands over the keys.
### 6. Step 6

Do not skip a safety item to make a delivery time.

## Output

Deliver a **handover checklist**.

- Purpose of this handover checklist, in two sentences.
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

A delivery is booked for 3 p.m. The handover list includes a recall check. It was not run. The draft checklist marks recall clear so the keys can go.

### Example data

```text
delivery: 16 Sep 2026 15:00
list: walkaround, recall check, second key, payment receipt
done: walkaround, second key
not done: recall check
payment receipt: in the file
salesperson: Jon
draft mark: recall clear
```

### Example outcome

**Handover**
Keys do not go at 3 p.m. The recall check was not run. Clear is a false mark. Remove it.
Done: walkaround, second key, payment receipt in the file.
Open: recall check.
Who hands the keys after the check: Jon. Not before.

## Anti-patterns

- Keys handed over with an open safety item
- A recall marked clear without a check
- A checklist copied as done

## Related skills

- `recall-owner-note`
- `dealer-launch-check`

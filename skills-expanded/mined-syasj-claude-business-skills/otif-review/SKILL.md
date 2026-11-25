---
name: otif-review
description: "Review on-time-in-full from the shipments the user counted, split by cause. Use when the user mentions OTIF, on time in full, supplier OTIF, delivery score, or asks for a OTIF note. Supply chain skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: supply-chain
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'otif-review' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# OTIF Review

Review on-time-in-full from the shipments the user counted, split by cause.

## When to use this skill

Use this skill when the user:

- OTIF
- on time in full
- supplier OTIF
- delivery score

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Inventory and supplier recommendations depend on the user's lead times and service targets. Do not invent supplier performance.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The shipments
- Their on-time rule
- Causes they coded
- The target

## Workflow


### 1. Step 1

Count from their file.
### 2. Step 2

Use their on-time rule, not a generic one.
### 3. Step 3

Split buyer-caused late orders from supplier misses if they coded them.
### 4. Step 4

Do not invent a penalty.
### 5. Step 5

Compare to the target they set.
### 6. Step 6

Name the largest cause.

## Output

Deliver a **OTIF note**.

- Purpose of this OTIF note, in two sentences.
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

Diane counted 94 shipments in August. 86 were on time in full. Her rule is on the promised day and full quantity. Target is 95 percent. She coded 6 misses to a same-week forecast change.

### Example data

```text
shipments: 94
on time in full: 86
rule: promised day and full quantity
target: 95 percent
coded buyer forecast change: 6 misses
other misses: 2, not coded
penalty clause: none in the file
```

### Example outcome

**OTIF note — August**
86 of 94 is 91 percent, under her 95 percent target. Count is hers. I am not inventing a penalty.

| Misses | Code in her file |
| --- | --- |
| 6 | same-week forecast change |
| 2 | not coded |

Do not give the supplier all 8. Six are coded to the buyer. Two are open.
Next: Diane codes the two before any supplier meeting.

## Anti-patterns

- A score with no file
- Penalties invented
- Buyer lateness hidden

## Related skills

- `supplier-scorecard`
- `demand-plan-review`

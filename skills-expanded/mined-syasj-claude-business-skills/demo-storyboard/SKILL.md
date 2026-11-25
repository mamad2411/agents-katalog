---
name: demo-storyboard
description: "Storyboard a demo around the buyer's job, with proof points and a stop time, not a feature tour. Use when the user mentions demo script, product demo, storyboard a demo, sales demo, or asks for a demo storyboard. Sales skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: sales
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'demo-storyboard' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Demo Storyboard

Storyboard a demo around the buyer's job, with proof points and a stop time, not a feature tour.

## When to use this skill

Use this skill when the user:

- demo script
- product demo
- storyboard a demo
- sales demo

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Sell honestly. Do not invent customer proof, discounts, or competitor facts. Do not write deceptive, phishing, or high-pressure scripts.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The buyer's job and problem
- The three things the demo must prove
- Time available
- Features that are tempting but irrelevant

## Workflow


### 1. Open with their scene

A day-in-the-life moment from discovery. If you lack it, ask before building a tour.
### 2. Three proofs

Each proof is a scene, a click path, and the line that connects it to their problem.
### 3. Cut

Remove features that do not serve the three proofs, and list them as parking lot.
### 4. Risks

Where the demo environment is fragile. Plan a screenshot backup rather than a live apology.
### 5. Close

The question that checks whether the proof landed, plus the next step.
### 6. Honesty

Do not demo a roadmap item as if it exists. Label future work as future.

## Output

Deliver a **demo storyboard**.

- Purpose of this demo storyboard, in two sentences.
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

Samir Qureshi, account executive at Fieldnote in Edmonton, needs a demo storyboard by 30 September 2026. A 45-minute demo deck has 30 features, and the buyer only asked how exceptions get resolved.

### Example data

```text
From: Samir Qureshi, account executive
Organization: Fieldnote, Edmonton
Date: 14 September 2026
Needed by: 30 September 2026

A 45-minute demo deck has 30 features, and the buyer only asked how exceptions get resolved.

The buyer's job and problem: A 45-minute demo deck has 30 features, and the buyer only asked how exceptions get resolved. Stated once, in the ask. Not written down anywhere else
The three things the demo must prove: Harbor Goods, recorded 14 September 2026. No supporting file attached
Time available: five working days, due 30 September 2026
Features that are tempting but irrelevant: Harbor Goods, last reviewed 14 September 2026. No owner named since
```

### Example outcome

**Demo storyboard**
To: Samir Qureshi, account executive, Fieldnote
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
A storyboard with one exception-resolution scene, two supporting proofs, and the other features parked.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The buyer's job and problem | A 45-minute demo deck has 30 features, and the buyer only asked how exceptions get resolved. Stated once, in the ask. Not written down anywhere else | Needs confirmation |
| The three things the demo must prove | Harbor Goods, recorded 14 September 2026. No supporting file attached | Carried into the draft |
| Time available | five working days, due 30 September 2026 | Carried into the draft |
| Features that are tempting but irrelevant | Harbor Goods, last reviewed 14 September 2026. No owner named since | Needs confirmation |

**How this draft was built**

**1. Open with their scene**  
A day-in-the-life moment from discovery. If you lack it, ask before building a tour.

**2. Three proofs**  
Each proof is a scene, a click path, and the line that connects it to their problem.

**3. Cut**  
Remove features that do not serve the three proofs, and list them as parking lot.

**4. Risks**  
Where the demo environment is fragile. Plan a screenshot backup rather than a live apology.

**5. Close**  
The question that checks whether the proof landed, plus the next step.

**Deliberately not done**
- A feature tour with no buyer scene.
- Showing roadmap as current product.
- No time left for the buyer to talk.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Samir Qureshi by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A feature tour with no buyer scene.
- Showing roadmap as current product.
- No time left for the buyer to talk.

## Related skills

- `discovery-call`
- `sales-playbook`

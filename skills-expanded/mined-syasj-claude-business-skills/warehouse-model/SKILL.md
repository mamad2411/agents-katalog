---
name: warehouse-model
description: "Review a warehouse model for grain mistakes and double-counted joins. Use when the user mentions warehouse model, star schema review, grain check, fact table review, or asks for a model review. Data and analytics skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: data
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'warehouse-model' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Warehouse Model Review

Review a warehouse model for grain mistakes and double-counted joins.

## When to use this skill

Use this skill when the user:

- warehouse model
- star schema review
- grain check
- fact table review

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Do not invent numbers. If a source file is missing, say so. Distinguish observation from inference. Do not re-identify private data to make a point.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The fact grain they claim
- The joins
- A sample of duplicate keys if they have one
- The metric that looks wrong

## Workflow


### 1. Step 1

Restate the grain.
### 2. Step 2

Check the join they showed for fan-out.
### 3. Step 3

If they have duplicate keys, count them from their sample, do not invent a rate.
### 4. Step 4

Say which metric moves if the grain is wrong.
### 5. Step 5

Recommend a fix as a question for the modeler, not a silent rewrite.
### 6. Step 6

Stop if they did not include the join.

## Output

Deliver a **model review**.

- Purpose of this model review, in two sentences.
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

active_accounts jumped from 1,100 to 4,600 on 12 September after Noah joined the fact to payments. Payments has many rows per workspace. He has a 20-row sample.

### Example data

```text
claimed grain: one row per workspace per day
join added 12 Sep: payments on workspace_id
sample of 20 workspace-days: 17 have more than one payment row
metric before: 1,100 on 11 Sep
metric after: 4,600 on 12 Sep
modeler: Noah Berger
```

### Example outcome

**Model review**
Do not use the 12 September active_accounts figure.

The claimed grain is one row per workspace per day. The payments join is many rows per workspace.
In the 20-row sample, 17 keys fan out. That is the sample, not a rate for the whole table.
The jump from 1,100 to 4,600 fits a fan-out. It is not proof of 3,500 new workspaces.
Fix to ask Noah for: count of workspace-days with more than one row, and a join that does not multiply the flag.
This review does not rewrite the model.

## Anti-patterns

- A new model drawn from scratch with no source
- Ignoring a duplicate key sample
- A guessed row count

## Related skills

- `data-lineage`
- `metric-definition`

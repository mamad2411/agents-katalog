---
name: headline-check
description: "Check a headline against the story's sourced facts. Use when the user mentions headline check, does this hed work, news headline, front-page line, or asks for a headline check. Media and communications skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: media
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'headline-check' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Headline Check

Check a headline against the story's sourced facts.

## When to use this skill

Use this skill when the user:

- headline check
- does this hed work
- news headline
- front-page line

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

- The headline
- The sourced facts
- The words that overclaim
- The editor's deadline

## Workflow


### 1. Step 1

Underline every factual word in the headline.
### 2. Step 2

Match each to a sourced sentence.
### 3. Step 3

Cut a number, cause, or blame the story does not have.
### 4. Step 4

Offer two headlines that match.
### 5. Step 5

Do not write a clever line that adds a fact.
### 6. Step 6

If the story is thin, say the headline has to be thin.

## Output

Deliver a **headline check**.

- Purpose of this headline check, in two sentences.
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

The copy desk wrote 'Plant cuts safety staff before 10-day shutdown'. The story only has the 22 September start and the ten-day length from the statement.

### Example data

```text
headline: Plant cuts safety staff before 10-day shutdown
sourced: turnaround starts 22 Sep 2026, ten days, company statement 15 Sep
not sourced: safety staff, cuts, blame
deadline: 19 Sep 16:00
```

### Example outcome

**Headline check**
No. 'Cuts safety staff' is not in the story.

Options that match:
1. Company says plant turnaround starts 22 September
2. Statement: ten-day turnaround from Monday

Use 1. It is the date in the document.
Do not add a cause to make the line sharper.

## Anti-patterns

- A cause the story does not prove
- A number not in the copy
- Blame in the hed only

## Related skills

- `news-assignment`
- `blog-title-pack`

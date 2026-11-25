---
name: route-result-note
description: "Report a route day from the flights and the loads the user exported. Use when the user mentions route performance, flight results, load factor note, route day, or asks for a route note. Airline operations skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: airline
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'route-result-note' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Route Result

Report a route day from the flights and the loads the user exported.

## When to use this skill

Use this skill when the user:

- route performance
- flight results
- load factor note
- route day

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Do not advise exceeding a duty limit, skipping a maintenance release, or concealing a safety issue. Passenger messages must match the facts supplied.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The flights
- The loads
- The cancellations
- The target they use

## Workflow


### 1. Step 1

Count flights from the export.
### 2. Step 2

A cancellation stays a cancellation.
### 3. Step 3

Do not invent a yield.
### 4. Step 4

Compare load to their target only if both are in the file.
### 5. Step 5

Name the worst flight by their metric.
### 6. Step 6

Do not drop a cancel to improve the day.

## Output

Deliver a **route note**.

- Purpose of this route note, in two sentences.
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

Luis exported 16 September for the YYC routes he watches. Four flights were planned. One cancelled. The three that flew had loads of 80, 91, and 70 percent. His target is 85. No yield is in the export.

### Example data

```text
day: 16 Sep 2026
planned: 4
cancelled: KA188
flew: loads 80, 91, 70
target load: 85
yield: not in the export
```

### Example outcome

**Route day**
Four planned. KA188 cancelled. Do not drop it to make the day look full.

| Flight | Load |
| --- | --- |
| three that flew | 80, 91, 70 |
| target | 85 |
| KA188 | cancelled |

Two of the three that flew are under 85. No yield is in this note.
Worst by his metric: the cancel, then the 70.

## Anti-patterns

- A dropped cancellation
- An invented yield
- A target they did not set

## Related skills

- `irrops-brief`
- `saas-weekly-metrics`

---
name: employee-relations-intake
description: "Intake a workplace concern so it is routed fairly, with facts separated from conclusions. Use when the user mentions employee relations, HR complaint, workplace complaint intake, grievance intake, or asks for a employee relations intake. People and culture skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: people
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'employee-relations-intake' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Employee Relations Intake

Intake a workplace concern so it is routed fairly, with facts separated from conclusions.

## When to use this skill

Use this skill when the user:

- employee relations
- HR complaint
- workplace complaint intake
- grievance intake

## When not to use this skill

- Retaliation
- Covering up a complaint

## Professional boundary

Employment work must follow the organization's policies and local employment law. Do not invent legal requirements. Do not write content that discriminates or retaliates.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- What was reported
- Who received it and when
- Immediate safety issues
- The stated company process

## Workflow


### 1. Safety and dignity first

Threats and harassment go to the safety and reporting path. Do not mediate those casually.
### 2. Facts

What was said, when, and who has authority to look into it. Do not add motive.
### 3. Conflicts

The investigator should not be the accused or their close ally. Say so if the user proposes that.
### 4. Confidentiality

Need-to-know. Do not help broadcast the allegation.
### 5. No retaliation

Refuse any request to punish the person who reported.
### 6. Record

A neutral intake note with next step and owner. Not a verdict.

## Output

Deliver a **employee relations intake**.

- Purpose of this employee relations intake, in two sentences.
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

Chris Adeyemi, people lead at Northline Studio in Calgary, needs an employee relations intake by 30 September 2026. A team lead wants HR to 'make a complaint go away' before a client visit.

### Example data

```text
From: Chris Adeyemi, people lead
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

A team lead wants HR to 'make a complaint go away' before a client visit.

What was reported: one file, dated 14 September 2026. No earlier version attached for comparison
Who received it and when: 30 September 2026
Immediate safety issues: Open coordinator role and one other, both unconfirmed as of 14 September 2026
The stated company process: email to Chris Adeyemi. No written steps after 1 Sep 2026
```

### Example outcome

**Employee relations intake**
To: Chris Adeyemi, people lead, Northline Studio
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Records the concern, refuses to bury it, and assigns an investigator who is not the accused.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| What was reported | one file, dated 14 September 2026. No earlier version attached for comparison | Needs confirmation |
| Who received it and when | 30 September 2026 | Carried into the draft |
| Immediate safety issues | Open coordinator role and one other, both unconfirmed as of 14 September 2026 | Carried into the draft |
| The stated company process | email to Chris Adeyemi. No written steps after 1 Sep 2026 | Needs confirmation |

**How this draft was built**

**1. Safety and dignity first**  
Threats and harassment go to the safety and reporting path. Do not mediate those casually.

**2. Facts**  
What was said, when, and who has authority to look into it. Do not add motive.

**3. Conflicts**  
The investigator should not be the accused or their close ally. Say so if the user proposes that.

**4. Confidentiality**  
Need-to-know. Do not help broadcast the allegation.

**5. No retaliation**  
Refuse any request to punish the person who reported.

**Deliberately not done**
- A verdict in the intake.
- Retaliation advice.
- Spreading the allegation as gossip.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Chris Adeyemi by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A verdict in the intake.
- Retaliation advice.
- Spreading the allegation as gossip.

## Related skills

- `whistleblower-intake`
- `conflict-mediation`
- `pip-design`

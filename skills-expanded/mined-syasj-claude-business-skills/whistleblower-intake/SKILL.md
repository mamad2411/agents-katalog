---
name: whistleblower-intake
description: "Structure an internal report of misconduct so it can be handled fairly, without retaliation or a witch hunt. Use when the user mentions whistleblower report, ethics report, internal misconduct report, speak-up intake, or asks for a whistleblower intake note. Legal operations skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: legal
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'whistleblower-intake' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Whistleblower Intake

Structure an internal report of misconduct so it can be handled fairly, without retaliation or a witch hunt.

## When to use this skill

Use this skill when the user:

- whistleblower report
- ethics report
- internal misconduct report
- speak-up intake

## When not to use this skill

- Retaliation
- Covering up a report

## Professional boundary

This is not legal advice and does not create an attorney-client relationship. Do not invent statutes, case names, or filing deadlines. Drafts are for qualified counsel in the relevant jurisdiction.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- What was reported, with identifiers minimized
- Who received it
- Immediate safety concerns
- The company's stated process, if known

## Workflow


### 1. Stabilize

If someone may be in danger, tell the user to use local emergency services and their safety process. Do not investigate a crime scene yourself.
### 2. Record facts

What was alleged, when it was received, and what is still unknown. Do not add motive.
### 3. Minimize data

Include names only as needed to route the report. Do not build a dossier for curiosity.
### 4. No retaliation

Remind the handler that punishing the reporter is not an option you will help with.
### 5. Route

Follow the company's stated channel. If none exists, recommend an independent reviewer rather than the accused person's chain of command.
### 6. Preserve records

Keep the report. Do not draft a plan to delete it.

## Output

Deliver a **whistleblower intake note**.

- Purpose of this whistleblower intake note, in two sentences.
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

Elena Voss, operations lead at Northline Studio in Calgary, needs a whistleblower intake note by 30 September 2026. An employee reported a possible bribe and the manager wants to know if they can quietly move the reporter off the account.

### Example data

```text
From: Elena Voss, operations lead
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

An employee reported a possible bribe and the manager wants to know if they can quietly move the reporter off the account.

What was reported, with identifiers minimized: one file, dated 14 September 2026. No earlier version attached for comparison
Who received it: Elena Voss, operations lead
Immediate safety concerns: Vendor terms and one other, both unconfirmed as of 14 September 2026
The company's stated process, if known: email to Elena Voss. No written steps after 1 Sep 2026
```

### Example outcome

**Whistleblower intake note**
To: Elena Voss, operations lead, Northline Studio
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Routes the allegation to an independent reviewer and refuses the retaliatory move.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| What was reported, with identifiers minimized | one file, dated 14 September 2026. No earlier version attached for comparison | Needs confirmation |
| Who received it | Elena Voss, operations lead | Carried into the draft |
| Immediate safety concerns | Vendor terms and one other, both unconfirmed as of 14 September 2026 | Carried into the draft |
| The company's stated process, if known | email to Elena Voss. No written steps after 1 Sep 2026 | Needs confirmation |

**How this draft was built**

**1. Stabilize**  
If someone may be in danger, tell the user to use local emergency services and their safety process. Do not investigate a crime scene yourself.

**2. Record facts**  
What was alleged, when it was received, and what is still unknown. Do not add motive.

**3. Minimize data**  
Include names only as needed to route the report. Do not build a dossier for curiosity.

**4. No retaliation**  
Remind the handler that punishing the reporter is not an option you will help with.

**5. Route**  
Follow the company's stated channel. If none exists, recommend an independent reviewer rather than the accused person's chain of command.

**Deliberately not done**
- Helping retaliate against a reporter.
- A public accusation draft.
- Investigating by collecting unrelated personal data.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Elena Voss by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Helping retaliate against a reporter.
- A public accusation draft.
- Investigating by collecting unrelated personal data.

## Related skills

- `ethics-hotline-triage`
- `dispute-intake`
- `employee-relations-intake`

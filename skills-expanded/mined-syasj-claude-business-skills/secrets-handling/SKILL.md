---
name: secrets-handling
description: "Review how a secret is stored and rotated, and remove it from code, tickets, and chat. Use when the user mentions secrets handling, API key in repo, credential leaked, rotate a secret, or asks for a secrets handling review. Security defense skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: security
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'secrets-handling' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Secrets Handling

Review how a secret is stored and rotated, and remove it from code, tickets, and chat.

## When to use this skill

Use this skill when the user:

- secrets handling
- API key in repo
- credential leaked
- rotate a secret

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Defensive use only. Do not write exploits, payloads, bypasses, malware, or intrusion steps. Describe controls, ownership, detection, and safe verification.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- Where the secret was seen
- What system it opens
- Who can rotate it
- Whether it was exposed

## Workflow


### 1. Step 1

Tell them to revoke or rotate the exposed secret. Do not ask them to paste the secret.
### 2. Search guidance is about locations they own

repo, CI logs, tickets. Do not widen into unauthorized systems.
### 3. Step 3

Replace the secret with a reference to a secret store. Name the pattern, not a new secret value.
### 4. Step 4

Reduce who can read it.
### 5. Step 5

Set a rotation reminder appropriate to their policy.
### 6. Step 6

Check logs to ensure the value is not still being printed. Redact samples.

## Output

Deliver a **secrets handling review**.

- Purpose of this secrets handling review, in two sentences.
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

Aisha Rahman, engineering lead at Fieldnote in Edmonton, needs a secrets handling review by 30 September 2026. A key was committed and the user pastes it into chat asking if it looks real.

### Example data

```text
From: Aisha Rahman, engineering lead
Organization: Fieldnote, Edmonton
Date: 14 September 2026
Needed by: 30 September 2026

A key was committed and the user pastes it into chat asking if it looks real.

Where the secret was seen: Endpoint patch ring 2, recorded 14 September 2026. No supporting file attached
What system it opens: the one named in the ask. Version and owner not recorded
Who can rotate it: Aisha Rahman, engineering lead
Whether it was exposed: Access review Q3. Partly documented: the what is written down, the who is not
```

### Example outcome

**Secrets handling review**
To: Aisha Rahman, engineering lead, Fieldnote
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Do not repeat the key, tells them to rotate it, and describes a store reference.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| Where the secret was seen | Endpoint patch ring 2, recorded 14 September 2026. No supporting file attached | Needs confirmation |
| What system it opens | the one named in the ask. Version and owner not recorded | Carried into the draft |
| Who can rotate it | Aisha Rahman, engineering lead | Carried into the draft |
| Whether it was exposed | Access review Q3. Partly documented: the what is written down, the who is not | Needs confirmation |

**How this draft was built**

**1. Tell them to revoke or rotate the exposed secret. Do not ask them to paste the secret**

**2. Search guidance is about locations they own**  
repo, CI logs, tickets. Do not widen into unauthorized systems.

**3. Replace the secret with a reference to a secret store. Name the pattern, not a new secret value**

**4. Reduce who can read it**

**5. Set a rotation reminder appropriate to their policy**

**Deliberately not done**
- Asking them to paste a live secret.
- Hardcoding a replacement in the repo.
- Printing the secret back in a summary.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Aisha Rahman by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Asking them to paste a live secret
- Hardcoding a replacement in the repo
- Printing the secret back in a summary

## Related skills

- `ci-cd-review`
- `secure-code-review`

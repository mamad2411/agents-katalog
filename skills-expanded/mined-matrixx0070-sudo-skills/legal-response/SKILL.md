---
name: legal-response
version: 1.0.0
description: Draft a response to a routine legal inquiry from an approved template, with escalation checks that route novel or high-risk questions to counsel before any answer goes out.
author: matrixx0070
tags: [legal, response, templates, intake, escalation]
capabilities: []
---

## When to use
Use this to answer routine, recurring legal questions — "can we use this logo," "is this clause standard," "what's our data-retention period," "can I share this with a partner" — where an approved template exists. It resolves the common case fast and routes anything unusual to a licensed attorney.

**Not for:** novel fact patterns, active or threatened litigation, regulator inquiries, personal legal advice, or exposure above your dollar threshold — all of those escalate. Do not improvise a template where none exists.

## Method
1. **Classify the inquiry.** Match it to a known category (IP use, data handling, contract clause, employment, disclosure, third-party sharing). *Decision point:* no category fits → escalate, stop here.
2. **Run escalation checks first, before drafting.** Flag to counsel if the matter involves litigation, a regulator, a novel fact pattern, dollar exposure above threshold, personal legal advice, or a non-standard jurisdiction. Never template these.
3. **Select the approved template** for the category and confirm it is the current version.
4. **Fill it with the specific facts.** Replace every placeholder; never leave generic language that misstates the situation.
5. **Add caveats.** State your assumptions and the boundary of the answer ("this covers X, not Y").
6. **Mark review need.** Note whether attorney review is required before sending.

## Example
Inquiry: "Can we put a customer's logo on our website?" Category: IP use → template exists. Escalation checks: no litigation, standard jurisdiction, low exposure → pass. Draft (from template): "Yes, provided (a) the customer has signed our reference-rights clause or given written consent, and (b) you use the logo per any brand guidelines they supply." Assumptions: US-based customer, marketing use only. Scope limit: does not cover press releases or paid ads. Attorney review: not required. Next step: confirm signed reference clause with account owner.

## Pitfalls
- **Drafting before running escalation checks.** You'll template a matter that needed a lawyer.
- **Leaving placeholders in.** "[CUSTOMER]" or generic boilerplate that no longer fits the facts misleads the requester.
- **Silent scope creep.** Answering the adjacent question you weren't asked, without flagging it.
- **Using a stale template.** Confirm the version — retention periods and clause language change.

## Output format
```
Inquiry (restated) + category:
Escalation check: pass | ESCALATE — reason:
Response draft: <templated, facts filled>
Assumptions & scope limits:
Attorney review: required | not required
Suggested next step for requester:
```

## Template categories
Match the inquiry to a category, then give the standard answer shape and check the auto-escalate trigger. If none fits, escalate — do not improvise a template.

| Category | Typical question | Standard answer shape | Auto-escalate if |
|----------|------------------|-----------------------|------------------|
| IP / brand use | "Can we use this logo/name?" | Conditional yes: requires signed reference clause or written consent + adherence to brand guidelines | Press, paid ad, or endorsement implication |
| Data handling / retention | "How long do we keep X? Can we store it?" | State the policy retention period and the lawful basis/purpose limit | Litigation hold possible, or regulated data (PHI, financial, biometric) |
| Contract clause standard-ness | "Is this term normal?" | Confirm whether it matches our standard fallback; flag deviations | Non-standard term, or counterparty edits to liability/indemnity/IP |
| Third-party sharing / disclosure | "Can I share this doc/data?" | Yes if recipient is covered by an NDA and data is non-sensitive; state the limit | Personal or regulated data, or no NDA in place |
| Employment basics | "Can I give a reference / confirm employment?" | Provide neutral verification (dates, title) only; direct rest to HR | Anything beyond dates/title, or performance/discipline detail |
| Confidentiality / NDA existence | "Do we have an NDA with X?" | State whether one is on file and its scope/term | No NDA and disclosure is imminent |
| Marketing / claims | "Can we say X?" | Yes if substantiated and non-misleading; add required disclosures | Comparative, superlative, health/financial, or unsubstantiated claim |

## Mandatory escalation triggers
Never template these. Route to a licensed attorney **before any answer goes out**:

- Active or threatened litigation
- Any regulator or government inquiry, or a subpoena
- Personal legal advice to an individual
- Dollar exposure above your defined threshold
- A novel fact pattern with no matching template
- Non-standard or foreign jurisdiction
- Anything touching criminal liability
- Employment termination or discipline specifics
- Securities or insider matters
- IP infringement allegations — whether incoming or outgoing

## Reference
**Caveat discipline.** State your assumptions explicitly, scope-limit the answer to exactly what was asked ("this covers X, not Y"), and add "this is not legal advice — confirm with counsel for your specifics" wherever the requester might over-rely on the answer. A tight scope is what keeps a templated response safe.

**Template version hygiene.** Confirm you are using the current template version before sending. Retention periods, clause language, and disclosure requirements drift over time; a stale template quietly misstates the position. When in doubt about currency, treat the answer as unverified and check the source of truth.

**Your role.** You resolve the common case fast and route everything else. Volume lives in the templated categories; risk lives in the exceptions. When a question sits on the boundary, escalate — the cost of an unnecessary escalation is minutes, the cost of a wrong templated answer is the whole point of this gate.

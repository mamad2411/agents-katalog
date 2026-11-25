---
name: legal-compliance-check
version: 1.0.0
description: Check a proposed action against applicable laws, regulations, and internal policies, then return required approvals and a proceed/hold/escalate verdict.
author: matrixx0070
tags: [legal, compliance, regulatory, approvals, risk, escalation]
capabilities: []
---

## When to use
Use this before doing something with legal exposure — launching a feature, running a promotion, entering a market, processing personal data, sending a mass communication, or making a commitment. It tells you which rules apply, which sign-offs you need, and whether to proceed.

**Not for:** confirming a decision already made (this informs it beforehand), interpreting a genuinely novel or contested regulation (escalate to counsel), or reviewing a contract clause-by-clause (use `legal-review-contract`).

## Method
1. **State the action precisely.** What, by whom, where (jurisdictions), affecting whom, and when. Vague inputs produce useless verdicts.
2. **Map applicable regimes.** List every law, regulation, and internal policy that plausibly governs it — privacy, consumer protection, employment, IP, export, financial, sector-specific — noting jurisdiction per regime.
3. **Test conformance per regime.** State the requirement and mark it compliant / conditional / non-compliant / unclear.
4. **List conditions for the conditionals.** Specify what must be true (consent, disclosure, license, record-keeping) to make each compliant.
5. **Determine required approvals.** Who must sign off (legal, privacy, security, finance) and in what order.
6. **Render the verdict.** *Decision point:* any non-compliant or unclear item, or missing required approval → **hold** or **escalate**; all-compliant-or-conditional-with-owned-conditions → **proceed-with-conditions**; fully clear → **proceed**.

## Example
Action: send a win-back email to lapsed EU customers next Tuesday. Regimes: GDPR (consent/legitimate interest — conditional: needs LIA on file), ePrivacy (conditional: prior opt-in for marketing), internal data-retention policy (compliant). Verdict: proceed-with-conditions. Conditions: attach completed LIA (owner: DPO), confirm suppression of opted-out contacts (owner: CRM lead). Approvals: privacy → marketing lead. Escalate: none.

## Pitfalls
- **A fuzzy action statement.** "Launch marketing" can't be tested; "email 40k EU opt-ins on 7/15" can.
- **Skipping internal policy.** Something legal under statute can still violate a stricter company rule.
- **Treating "unclear" as "compliant."** Unclear is a hold trigger, not a pass.
- **Listing approvals without order.** Parallel sign-offs that should be sequential cause re-work.

## Output format
```
Proposed action + jurisdictions:
Verdict: proceed | proceed-with-conditions | hold | escalate
Regime table:
  | Regime | Requirement | Status | Note |
Conditions to satisfy: <condition> — owner: <name>
Required approvals: <role> (order N)
Residual risk:
Escalation flags:
```

## Regime reference
Map the action to every domain it touches, then to the specific regimes in play. Use this table as a checklist — most actions hit more than one row.

| Domain | Key regimes | Core requirement | Typical trigger |
|--------|-------------|------------------|-----------------|
| Data privacy | GDPR, UK GDPR, CCPA/CPRA, ePrivacy/PECR | Lawful basis, consent, DPIA, DSAR handling, records | Any EU personal data processing → GDPR lawful basis + records; CA resident data → CCPA notice + opt-out |
| Marketing / comms | CAN-SPAM, ePrivacy, TCPA | Opt-in/opt-out, sender identification, prior consent for SMS/calls | Marketing email to consumers → CAN-SPAM unsubscribe + physical address; EU → prior opt-in; US SMS marketing → TCPA prior express written consent |
| Consumer protection | FTC Act, EU UCPD, ASA (UK), UWG (DE) | No deceptive/unfair practices; clear, non-misleading disclosures | Public claims, pricing, or promotions → substantiation + clear disclosure |
| Employment | FLSA, at-will vs. works-council regimes, worker-classification tests | Wage/hour compliance, correct classification, consultation duties | Hiring/engaging workers abroad → local classification + council consultation |
| Export control | EAR, OFAC sanctions, ITAR | Denied-party and destination screening; classification | Shipping tech abroad → EAR classification + OFAC screen |
| IP | Trademark clearance, copyright license, open-source license compliance | Clearance before use; honor license terms | New brand/name → trademark clearance; shipping code → OSS license review |
| Financial / sector | KYC/AML, PCI-DSS, HIPAA, SOX, GLBA | Identity/transaction controls, card-data and PHI safeguards, financial reporting integrity | Handling cards → PCI-DSS; handling health data → HIPAA |
| Accessibility | ADA, WCAG, EAA | Accessible digital products and services | Public web/app or EU digital product → WCAG conformance |

## Approval routing
Sign-offs are sequential, not parallel — the earlier gate can kill the request before the later one spends time on it.

| Trigger | Required sign-offs (in order) |
|---------|-------------------------------|
| Personal data involved | Privacy/DPO → Legal |
| New market entry | Legal → Finance |
| Marketing campaign | Legal/Brand → Marketing lead |
| Security-relevant change | Security → Legal |
| Financial commitment over threshold | Finance → Executive |

## Verdict rubric

| Verdict | When |
|---------|------|
| Proceed | Every applicable regime is compliant; no open conditions or approvals |
| Proceed-with-conditions | Only conditional items remain, each with an owned, dated condition |
| Hold | Any non-compliant item, or any condition without an owner |
| Escalate | Anything unclear or novel, a contested regime, or a missing required approval |

The controlling rule stands: **unclear is a hold, never a pass.** An item you cannot confidently mark compliant is treated as non-compliant until counsel clarifies it. Do not upgrade a verdict to clear the path faster — the point of the check is to catch exposure before it ships.

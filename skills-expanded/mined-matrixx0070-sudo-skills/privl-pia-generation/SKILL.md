---
name: privl-pia-generation
version: 1.0.0
description: Generate a Privacy/Data Protection Impact Assessment — describe the processing, test necessity and proportionality, assess risks to individuals, and specify mitigations.
author: matrixx0070
tags: [privacy, legal, pia, dpia, risk-assessment, gdpr, mitigation]
capabilities: []
---

## When to use

Use this when triage (privl-use-case-triage) flagged a processing activity as high-risk or an Art. 35(3) trigger fired, and you must produce a structured PIA/DPIA before the processing starts. It documents the decision, the risk analysis, and the controls that make the activity defensible.

**Not for:** low-risk activities that triage cleared, reviewing a vendor contract (privl-dpa-review), or assessing an existing program's regulatory gaps (privl-reg-gap-analysis). A DPIA is a pre-processing exercise — run it before launch, not after an incident.

## Method

1. **Systematic description** (Art. 35(7)(a)): the processing operations, purposes, data categories, subjects, recipients, retention, and any legitimate-interest reliance.
2. **Necessity & proportionality** (Art. 35(7)(b)): is the data the minimum needed for the purpose? Could a less intrusive means achieve it? Confirm lawful basis and purpose limitation.
3. **Risk to individuals** (Art. 35(7)(c)): identify harms (discrimination, identity theft, financial loss, reputational, loss of control), then score each by likelihood x severity.
4. **Mitigations** (Art. 35(7)(d)): map controls to each risk — minimization, pseudonymization, access control, retention limits, transparency, opt-outs, human review of automated decisions.
5. Compute residual risk after controls.
6. **Decision point:** consult the DPO (Art. 35(2)) and, where the activity relies on individuals, seek their views where appropriate.
7. **Attorney-escalation gate:** if residual risk stays high, Art. 36 prior consultation with the supervisory authority is likely required — route to counsel; do not self-clear high residual risk.

## Example

> **Activity:** Biometric time-clock for warehouse staff (special-category, Art. 9).
> **Necessity:** badge+PIN achieves attendance with less intrusion → proportionality challenged.
> **Risks:** unlawful special-category processing; breach → irreversible biometric loss (high severity).
> **Mitigations:** switch to badge default, biometric opt-in only, on-device template, 24h retention.
> **Residual:** medium; DPO consulted; counsel engaged on Art. 9 condition.

## Pitfalls

- Writing the DPIA to justify a decision already made instead of testing it.
- Listing risks without scoring likelihood x severity — no basis to prioritize controls.
- Confusing security controls with privacy mitigations; both are needed.
- Never revisiting the DPIA when the processing materially changes.

## Output format

```
DPIA — <activity> | date | DPO consulted: <y/n>
1. Description: <processing, data, subjects, recipients, retention>
2. Necessity/proportionality: <finding>
3. Risks: <harm — likelihood x severity>
4. Mitigations: <control → risk addressed>
Residual risk: <low/med/high>
Art. 36 prior consultation needed: <y/n> | For counsel: <items>
```

## Reference

- **GDPR Art. 35** DPIA requirement and the four mandatory content elements (35(7)); **Art. 35(3)** triggers.
- **Art. 35(2)** DPO consultation; **Art. 36** prior consultation with the supervisory authority for high residual risk.
- **Art. 9(2)** conditions for special-category data; **Art. 5** minimization and purpose limitation.
- Escalate high residual risk and Art. 9 reliance to an attorney.

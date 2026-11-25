---
name: privl-use-case-triage
version: 1.0.0
description: Triage a proposed data-processing use case — classify the data, name a lawful basis, flag high-risk signals, and decide whether a full PIA or attorney review is required.
author: matrixx0070
tags: [privacy, legal, triage, lawful-basis, gdpr, ccpa, dpia]
capabilities: []
---

## When to use

Use this the moment a new processing activity, feature, integration, or vendor is proposed and someone needs a fast, defensible read on privacy exposure before work begins. It is the front door: it decides whether the activity is low-risk and can proceed, or must escalate to a PIA/DPIA (privl-pia-generation), a DPA review (privl-dpa-review), or an attorney.

**Not for:** completing the full impact assessment itself, answering a live data-subject request (privl-dsar-response), or drafting policy. If the activity is already scoped and lawful, do not re-triage.

## Method

1. Describe the activity in one line: what data, from whom, for what purpose, by which systems, shared with whom.
2. Classify the data: ordinary personal data, special-category / sensitive (GDPR Art. 9 — health, biometrics, race, religion, sexuality, politics; CCPA "sensitive personal information"), children's data, or financial/government-ID.
3. Name a candidate lawful basis (GDPR Art. 6: consent, contract, legal obligation, vital interests, public task, legitimate interests). If legitimate interests, note that a balancing test is owed.
4. Scan high-risk signals: large-scale profiling, automated decisions with legal/significant effect, systematic monitoring, novel tech, combining datasets, vulnerable subjects, cross-border transfer.
5. **Decision point:** any Art. 35(3) trigger or special-category-at-scale → require a DPIA and stop the fast track.
6. **Attorney-escalation gate:** new automated decisioning, children's data, sensitive-data monetization, or a novel cross-border transfer → route to counsel before proceeding.

## Example

> **Activity:** New churn model scoring all users from support transcripts + usage logs.
> **Data:** ordinary personal data, large scale; transcripts may contain incidental sensitive data.
> **Basis:** legitimate interests — balancing test owed.
> **Risk signals:** large-scale profiling + dataset combination → Art. 35 trigger.
> **Verdict:** DPIA required (privl-pia-generation); attorney review not yet, revisit if scores drive automated account actions.

## Pitfalls

- Defaulting to consent when contract or legitimate interests is the honest basis.
- Ignoring incidental sensitive data hiding in free-text fields.
- Treating "we already collect it" as authorization for a new purpose (purpose limitation).
- Skipping the balancing test when relying on legitimate interests.

## Output format

```
Activity: <one line>
Data class: <ordinary | sensitive/Art.9 | children | financial/ID>
Lawful basis: <basis + balancing-test-owed?>
Risk signals: <list or none>
Verdict: <proceed | DPIA required | DPA review | attorney>
Escalate to counsel: <yes/no — why>
```

## Reference

- **GDPR Art. 6** lawful bases; **Art. 9** special-category conditions; **Art. 35(3)** DPIA triggers.
- **CCPA/CPRA** "sensitive personal information" category and purpose-limitation duties.
- Attorney escalation is mandatory for automated decisioning with legal effect, children's data, and novel international transfers.

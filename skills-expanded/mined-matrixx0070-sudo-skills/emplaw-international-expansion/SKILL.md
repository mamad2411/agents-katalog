---
name: emplaw-international-expansion
version: 1.0.0
description: Scope the employment-law considerations for hiring in a new country — local counsel, EOR vs entity, mandatory benefits, and termination rules.
author: matrixx0070
tags: [international, global-hiring, eor, entity, compliance]
capabilities: []
---

## When to use
Use this when your org wants to hire its first worker in a country where it has no presence and needs to scope the employment-law surface before committing. It frames the engagement model, statutory minimums, and risk gates. **Not for:** US state expansion — creating a new US state record is emplaw-expansion-kickoff and amending one is emplaw-expansion-update. Also not for: leave tracking (emplaw-leave-tracker / emplaw-log-leave); handbook edits (emplaw-handbook-updates); single-policy drafting (emplaw-policy-drafting); or the initial intake interview (emplaw-cold-start-interview).

## Method
1. Confirm the target country, the role, and whether the worker will be an employee or contractor.
2. Mandatory attorney-escalation gate: engage licensed local counsel in the target country before any offer, engagement, or payment — this is required, not optional, and this skill is not legal advice.
3. Decision point: if you need one or a few hires quickly and want to avoid entity setup, scope an Employer-of-Record (EOR); if you plan durable headcount, deep local operations, or IP localization, scope a legal entity — and weigh cost, control, and permanent-establishment exposure of each.
4. Map statutory minimums with counsel: notice periods, severance, 13th-month pay, paid leave, and any works-council or collective obligations.
5. Decision point: if the country is in the EU/EEA, plan for GDPR-compliant handling of employee data and possible works-council consultation; else confirm the local data-protection regime.
6. Assess misclassification and permanent-establishment tax risk for any contractor-style arrangement.
7. Confirm that no country outside the US is at-will: build for-cause and notice/severance expectations into the plan.

## Example
A US SaaS org wants one engineer in Germany. Counsel confirms EOR is fastest for a single hire. You scope mandatory 13th-month-adjacent norms, statutory notice, and works-council implications, plan GDPR-compliant data handling, and flag that "at-will" does not exist — termination needs cause and notice. A contractor route is rejected over misclassification and permanent-establishment risk.

## Pitfalls
- **Assuming at-will travels.** Outside the US, dismissal requires cause, notice, and often severance; US-style handbooks do not port.
- **Contractor shortcuts.** Misclassification and permanent-establishment findings create back-tax, benefit, and reinstatement liability.
- **Skipping mandatory benefits.** 13th-month pay, statutory leave, and social contributions are non-negotiable in many jurisdictions.
- **Treating GDPR as optional.** EU/EEA employee data carries real obligations from the first record.

## Output format
```
INTERNATIONAL SCOPE — <country> | Role: <title> | Date: <date>
Local counsel engaged: <firm / REQUIRED before offer>
Model: EOR / Entity (rationale: <speed/control/PE risk>)
Statutory minimums: notice <period> | severance <basis> | 13th-month <Y/N> | leave <days>
Collective: works council <Y/N> | Data: GDPR/<regime>
Risks: misclassification <note> | permanent establishment <note>
At-will: NO — termination requires <cause/notice>
```

## Reference
Engaging local counsel in the target country is mandatory before hiring. An Employer-of-Record (EOR) lets you hire without a local entity — faster and lower fixed cost but less control and ongoing per-head fees — while establishing a legal entity suits durable operations at higher setup and compliance cost. Statutory minimums commonly include notice periods, severance, 13th-month pay, and mandated paid leave; works councils and collective bargaining apply across much of the EU. No country outside the US is at-will. Misclassification and permanent-establishment findings create tax and liability exposure, and GDPR governs EU employee data. General reference only, not tailored legal advice.

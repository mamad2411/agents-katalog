---
name: emplaw-expansion-kickoff
version: 1.0.0
description: Kick off employment-law setup when the org first hires into a new US state — register as a foreign employer, map the new-state statutes, and stand up required policies and postings.
author: matrixx0070
tags: [expansion, multi-state, compliance, registration, postings]
capabilities: []
---

## When to use
Use this the first time your org will have an employee in a US state you do not yet operate in. It creates the state's baseline record: registrations, statute map, mandatory policies, and workplace postings. **Not for:** a state you already operate in — when a law changes or headcount crosses a threshold there, use emplaw-expansion-update, which edits the record this skill first creates. Also not for: hiring in another country (emplaw-international-expansion); leave tracking (emplaw-leave-tracker / emplaw-log-leave); handbook edits (emplaw-handbook-updates); drafting a single policy (emplaw-policy-drafting); or the initial intake interview (emplaw-cold-start-interview).

## Method
1. Confirm the trigger: a hire, remote worker, or acquisition establishing presence in the new state.
2. Register as a foreign employer and open state withholding and unemployment-insurance accounts.
3. Decision point: if the state has statutory exceptions to at-will (implied contract, public policy, covenant of good faith), document them; else record baseline at-will.
4. Map state-specific mandates: paid sick leave, meal/rest breaks, final-pay timing, pay-transparency rules, and any non-compete ban.
5. Decision point: if a headcount threshold triggers extra obligations at your projected size (e.g., CA FEHA anti-harassment duties at 5+), enable them now; else note the threshold and the count that will re-trigger later.
6. Deploy required written policies and order the mandatory workplace postings (state + local).
7. Create the state record with all of the above so emplaw-expansion-update has a baseline to amend.
8. Attorney-escalation gate: engage licensed employment counsel in the new state before finalizing registrations, policies, or offer terms — not legal advice.

## Example
An org headquartered in Texas hires its first employee in California. You register as a foreign employer, open EDD withholding and UI accounts, enable FEHA anti-harassment training (5+ threshold met), add CA paid-sick-leave and pay-transparency policies, drop the non-compete clause (void in CA), and order the CA + city postings. The California state record is created and handed to counsel for review.

## Pitfalls
- **Hiring before registering.** Payroll withholding and UI accounts must exist before the first paycheck, not after.
- **Copying the home-state handbook.** At-will language and non-competes valid at HQ can be unenforceable or unlawful in the new state.
- **Missing local ordinances.** Cities and counties layer sick-leave and posting rules above the state floor.
- **Ignoring dormant thresholds.** A threshold you are under today re-triggers as you hire; record the count, not just today's status.

## Output format
```
NEW-STATE KICKOFF — <state> | Trigger: <hire/remote/acquisition> | Date: <date>
Registrations: withholding <#> | UI <#> | foreign-employer <status>
At-will: <baseline/exceptions> | Non-compete: <allowed/banned>
Mandates: sick leave | breaks | final pay | pay transparency
Thresholds: <met / re-triggers at N>
Policies deployed: <list> | Postings ordered: <state + local>
Escalation: counsel reviewed <Y/N>
```

## Reference
Operating in a new state generally requires registering as a foreign employer and opening state withholding and unemployment-insurance accounts. Employment is at-will nationwide except in states recognizing implied-contract, public-policy, or good-faith exceptions. States impose distinct required policies and workplace postings; headcount thresholds re-trigger obligations per state (e.g., California FEHA duties begin at 5+ employees). Pay-transparency mandates and non-compete bans vary widely by state (non-competes are void in California, for example). General reference only, not tailored legal advice.

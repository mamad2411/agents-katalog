---
name: ipl-ip-clause-review
version: 1.0.0
description: Review the IP-related clauses in a contract to flag ownership traps, overbroad grants, and missing assignments, then propose a redline.
author: matrixx0070
tags: [contracts, ip-ownership, assignment, license-grant, work-for-hire, redline, review]
capabilities: []
---

## When to use

Use this when a contract governs who owns or can use intellectual property — an MSA, SOW, employment or contractor agreement, or a license. Reach for it before signing anything where deliverables, code, designs, or inventions change hands.

**Not for:** deep OSS obligation analysis behind an OSS rep (`ipl-oss-review`); triaging whether a third party infringes you (`ipl-infringement-triage`); or intake of a new invention (`ipl-invention-intake`). This reviews IP clauses in an existing contract.

## Method

1. **Identify the deal and parties,** and who should own what: employer/employee, customer/vendor, licensor/licensee.
2. **Read each IP clause:** ownership & assignment, grant scope, work-made-for-hire, background IP, feedback/improvements, OSS reps & warranties, IP indemnity, moral rights.
3. **Flag deviations:** ownership traps, overbroad or perpetual grants, missing or future-tense assignment, absent OSS reps, uncapped indemnity.
4. **Decision point:** assignment vs license for the deliverables. Assignment transfers ownership; a license leaves it with the creator — pick what the deal needs, and never accept "agrees to assign" where a present assignment is required.
5. **Propose a redline** per flagged clause.
6. **ATTORNEY-ESCALATION GATE:** patent and trademark assignments, IP indemnity caps, and novel structures go to a licensed attorney. You assist; you do not advise.

## Example

A contractor SOW says the vendor "agrees to assign" deliverables and is silent on background IP. Two problems: "agrees to assign" is a future promise, not a present transfer, and contractor work is not work-made-for-hire by default. Redline: change to "hereby assigns," add an express written assignment of deliverable IP, and add a background-IP license so pre-existing tools stay the vendor's but you can use them.

## Pitfalls

- **Trusting "work made for hire" for contractors.** It covers employees and nine enumerated categories only; a contractor needs an express written assignment.
- **Accepting "agrees to assign."** A future promise can fail to transfer title — insist on "hereby assigns" (Stanford v. Roche).
- **Missing the background-IP clause.** Without it, your pre-existing IP leaks or you cannot use theirs.
- **Overbroad feedback grants.** A "feedback" clause can quietly assign everything you suggest — narrow it.

## Output format

```
IP CLAUSE REVIEW — <contract type> | parties: <A / B>
Deal & desired ownership: <who should own what>
| Clause | Present? | Issue | Redline |
Ownership: assignment | license (chosen: ...)
Flags: <ownership trap | overbroad grant | missing assignment | OSS rep | indemnity>
Escalated to counsel: <items>
```

## Reference

- **Work made for hire (US Copyright Act §101):** applies to employees within scope, and to contractors only for nine enumerated categories under a written agreement. Otherwise a contractor needs an **express written assignment**.
- **Present vs future assignment:** "hereby assigns" effects a present transfer of title; "agrees to assign" is only a promise and may not vest ownership (Stanford v. Roche).
- **OSS license obligations** (permissive vs copyleft) are the basis for OSS reps & warranties — see `ipl-oss-review`.
- **Value of the IP:** likelihood-of-confusion (trademark) and patentability bars underlie the worth of anything licensed or assigned; weak IP changes what the clause is worth.

Assistive analysis, not legal advice.

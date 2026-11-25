---
name: emplaw-hiring-review
version: 1.0.0
description: Review a hiring process, job posting, or offer for employment-law compliance risk before it goes live.
author: matrixx0070
tags: [employment-law, hiring, compliance, fcra, discrimination]
capabilities: []
---

## When to use
Use this when someone hands you a job posting, screening process, interview plan, background-check flow, or offer letter and asks whether it is legally sound before it reaches candidates. This skill screens for protected-class risk, ban-the-box timing, pay-transparency duties, FCRA background-check steps, and I-9 timing. **Not for:** deciding whether a worker is an employee or contractor (use emplaw-worker-classification), overtime/minimum-wage math (use emplaw-wage-hour-qa), ending an existing relationship (use emplaw-termination-review), investigating a complaint (use emplaw-internal-investigation), leave eligibility (use emplaw-leave-tracker), or writing the handbook (use emplaw-policy-drafting).

## Method
1. Confirm the operating state(s) and headcount — coverage thresholds turn on both. Decision point: if headcount is unknown, flag every federal threshold as conditional and request the number.
2. Scan the posting/description for protected-class signals (age, sex, disability, national origin, religion, pregnancy) and coded language ("recent grad," "digital native," "he"). Decision point: if any appear, mark HIGH and rewrite to job-related criteria.
3. Check pay-transparency duty for each state/city. Decision point: if a covered jurisdiction requires a salary range and none is posted, block until added.
4. Check ban-the-box: is criminal history asked before a conditional offer? Decision point: if yes and a covered jurisdiction applies, defer the inquiry to post-offer.
5. Trace the background-check flow against FCRA: standalone disclosure, written authorization, pre-adverse notice with a copy of the report, waiting period, then final adverse-action notice.
6. Confirm I-9 timing: Section 1 by day one, Section 2 within 3 business days of start.
7. Apply the attorney-escalation gate: any adverse action or close call — confirm with licensed counsel in the operating state; this is not legal advice.

## Example
A posting reads "seeking an energetic recent grad, salary DOE" for a Colorado role, and runs a criminal check at the application stage. You flag: "recent grad" as age-proxy (ADEA) risk; missing salary range (Colorado pay transparency) as a blocker; and the pre-offer criminal inquiry as a ban-the-box violation to defer post-offer. You rewrite the ad and reorder the check.

## Pitfalls
- **Treating FCRA as one notice.** It is a sequence — disclosure, authorization, pre-adverse with report copy, wait, then final adverse. Skipping the pre-adverse step is the classic violation.
- **Copy-pasting a national posting.** Pay-transparency and ban-the-box duties are state- and city-specific; one template rarely clears every jurisdiction.
- **Burying the FCRA disclosure in the application.** It must be a standalone document, not mixed with liability waivers.
- **Assuming small employers are exempt.** Some state laws apply below the federal 15/20-employee thresholds.

## Output format
```
HIRING REVIEW — <role> @ <state(s)>, headcount <n>
RISK LEVEL: <LOW | MEDIUM | HIGH>
PROTECTED-CLASS FLAGS: <language/criteria + basis>
PAY TRANSPARENCY: <required? range posted? gap>
BAN-THE-BOX: <inquiry timing + fix>
FCRA FLOW: <disclosure / auth / pre-adverse / adverse — status each>
I-9 TIMING: <Section 1 day 1 / Section 2 by day 3 — status>
BLOCKERS BEFORE POSTING: <list>
ATTORNEY GATE: Confirm with licensed counsel in <state>; not legal advice.
```

## Reference
General reference only, not tailored legal advice.
- **Title VII** (race, color, religion, sex, national origin) and the **ADA** (disability) apply to employers with **15+ employees**; the **ADEA** (age 40+) applies at **20+**. State/local laws often cover smaller employers and add classes.
- **FCRA** background checks require: a clear standalone written disclosure, the applicant's written authorization, a pre-adverse-action notice including a copy of the report and the CFPB summary of rights, a reasonable waiting period, then a final adverse-action notice.
- **Ban-the-box** laws (many states/cities) bar criminal-history inquiries until at least a conditional offer, and often require individualized assessment.
- **Pay-transparency** laws (e.g., CO, CA, NY, WA) require posting a salary/wage range and sometimes benefits.
- **I-9**: employee completes Section 1 by the first day of work; employer completes Section 2 within **3 business days** of the start date. Thresholds and covered jurisdictions change — direct to current EEOC, CFPB/FTC, and DOL figures.

---
name: hr-policy-lookup
version: 1.0.0
description: Find the governing company policy and explain it accurately in plain language — cite the source, never fabricate, flag when to escalate.
author: matrixx0070
tags: [policy, compliance, handbook, plain-language, employee-support, escalation]
capabilities: []
---

## When to use

Reach for this when an employee or manager asks "what's our policy on X" — PTO, leave, remote work, expenses, conduct, benefits. Answer from the actual policy source and be explicit about what you do and don't know.

**Not for:** binding legal advice (route to counsel), pay-band questions (use hr-comp-analysis), or performance/conduct decisions (use hr-performance-review).

## Method

1. **Clarify the question** — identify the exact policy area, the person's location/employment type (policies vary by jurisdiction and status), and the specific scenario.
2. **Locate the source** — find the governing document (handbook section, policy page, benefits summary) and note its effective date and version. Decision point: if you cannot find it, say so plainly — do not fabricate a rule.
3. **Read for the answer** — extract the rule for this scenario: eligibility, limits, timelines, approvals, exceptions.
4. **Translate to plain language** — explain in a few actionable sentences, with a concrete example if it helps. Avoid legalese.
5. **Give next steps** — who to contact, what form/system to use, any deadline.
6. **Flag boundaries** — note where the policy is silent, where manager/HR discretion applies, and any case needing legal or a benefits specialist. Decision point: when the scenario touches protected leave, termination, or discrimination, stop and escalate rather than interpret.

Cite the source so the reader can verify.

## Example

Q: "I'm in California, full-time — can I carry unused PTO into next year?" Source: Employee Handbook §6.2 "Paid Time Off," effective 2026-01-01. Answer: Yes — you may carry up to 40 hours into the next calendar year; anything above 40 is paid out at year-end at your base rate (CA law prohibits use-it-or-lose-it). Next step: no action needed; carryover is automatic in Workday each January. Caveat: this covers CA full-time only; part-time accrual differs — see §6.3. Escalate to HR if your balance shows an incorrect carryover.

## Pitfalls

- Answering from memory or "what's typical" instead of the actual document.
- Ignoring jurisdiction — a US-wide answer that's wrong in California or the EU.
- Interpreting protected-leave, termination, or discrimination cases instead of escalating.
- Citing a policy without its version/effective date, so the reader can't tell if it's current.

## Output format

```
Direct answer: plain language, 2-4 sentences
The rule: eligibility | limits | timelines | approvals | exceptions
Next steps: who | where/form | deadline
Source: document + section + effective date
Caveats / when to escalate
```

## Reference

### Common policy areas and what governs them

Know which document and which law layer typically applies before you answer.

| Area | Usual governing source | Layered law to watch |
|---|---|---|
| PTO / vacation | Handbook + accrual/carryover policy | State payout & carryover rules (e.g., CA bans use-it-or-lose-it) |
| Sick leave | Sick-leave policy | State/city paid-sick-leave mandates |
| Protected leave | Leave policy | FMLA (US federal), state family/medical leave, ADA |
| Parental leave | Parental-leave policy | State paid-family-leave programs |
| Remote / hybrid | Remote-work policy | Multi-state tax/employment implications |
| Expenses | Expense/T&E policy | State business-expense reimbursement laws (e.g., CA §2802) |
| Conduct / discipline | Code of conduct + progressive-discipline policy | At-will limits, anti-retaliation |
| Benefits | Benefits summary / SPD | ERISA (US), plan documents control |
| Compensation | Pay/overtime policy | FLSA classification, state wage laws |
| Accommodation | Accommodation policy | ADA / state disability law |

The **plan document or official policy always controls** over a summary — if a benefits summary and the SPD conflict, cite and defer to the SPD.

### The jurisdiction/status matrix — ask before you answer

Policy answers vary along at least three axes. Confirm all three before giving a rule:

1. **Location** — country, and within the US, state and sometimes city. A correct US-federal answer can be wrong in California, New York, or the EU.
2. **Employment status** — full-time / part-time / temporary / contractor. Accrual, eligibility, and benefits differ sharply; contractors are usually outside most policies entirely.
3. **Exempt vs. non-exempt** (US) — drives overtime, timekeeping, and some leave rules.

If any axis is unknown, ask rather than assume. A confidently wrong policy answer is worse than "I need to confirm your location first."

### Escalation triggers — stop and route, do not interpret

These scenarios carry legal risk; give general info at most, then route to HR/legal/specialist. Do **not** improvise an interpretation:

- **Protected/statutory leave** — FMLA, ADA accommodation, pregnancy/parental, military (USERRA). Eligibility math and interactions are fact-specific.
- **Termination / discipline** — anything that could end employment or become a performance action.
- **Discrimination, harassment, or retaliation** — any allegation goes straight to HR/legal; do not investigate or opine.
- **Wage & hour disputes** — misclassification, unpaid overtime, final-pay timing.
- **Medical or disability information** — confidentiality obligations; route to a benefits/leave specialist.
- **Anything the policy is silent on**, or where manager/HR discretion applies — say so; don't invent a rule.
- **Cross-border / multi-state** situations where the governing law is unclear.

### The never-fabricate rule

If you cannot locate the governing document, say so plainly and route the person to HR — do **not** answer from memory or "what's typical." A made-up policy is a liability. Every answer cites the document, section, and effective date so the reader can verify. If the source you find looks outdated (effective date old, superseded reference), flag that rather than quoting it as current.

### Plain-language translation pattern

1. **Direct answer first** — the rule for *their* scenario, 2–4 sentences, no legalese.
2. **The mechanics** — eligibility, limits, timelines, approvals, exceptions, as short bullets.
3. **Next step** — who to contact, which system/form, any deadline.
4. **Source** — document + section + effective/version date.
5. **Boundaries** — where the policy is silent, where discretion applies, and the escalation flag if relevant.

Swap jargon for verbs: "carryover is accrued and prorated per §6.2" → "you keep up to 40 unused hours into next year; anything over that gets paid out in your final December paycheck."

### US law quick reference (context, not legal advice)

- **FMLA** — up to 12 weeks unpaid, job-protected leave; employers with 50+ employees within 75 miles; employee needs 12 months + 1,250 hours worked. Interacts with ADA and state PFL.
- **ADA** — reasonable accommodation for qualifying disabilities via an interactive process; employers with 15+ employees.
- **FLSA** — federal overtime (1.5× over 40 hrs/week for non-exempt) and minimum wage; exemption depends on duties + salary threshold, not job title.
- **State overlays** — CA, NY, WA, CO and others add paid sick leave, PFL, expense-reimbursement, and pay-transparency rules that exceed federal minimums.
- **ERISA** — governs benefit plans; the SPD/plan document controls benefits questions.

Treat these as orientation for *which specialist to route to*, never as a substitute for counsel. When a scenario touches any of them in a fact-specific way, escalate.

### Answer-quality checklist

- [ ] Confirmed location, employment status, and exempt/non-exempt where relevant
- [ ] Cited the actual governing document with section + effective date
- [ ] Answered *their* scenario, not the generic rule
- [ ] Gave a concrete next step (who/where/deadline)
- [ ] Flagged where the policy is silent or discretion applies
- [ ] Escalated (didn't interpret) any protected-leave, termination, discrimination, or wage dispute
- [ ] Did not fabricate — said "can't confirm, routing to HR" when the source wasn't found

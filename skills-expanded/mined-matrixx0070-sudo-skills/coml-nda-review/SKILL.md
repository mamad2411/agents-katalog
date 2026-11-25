---
name: coml-nda-review
version: 1.0.0
description: Review an NDA against the confidentiality playbook, flag every deviation from preferred and fallback positions, and return a sign / negotiate / reject verdict with specific edits.
author: matrixx0070
tags: [commercial-legal, nda, confidentiality, review, redline, escalation]
capabilities: []
---

## When to use

Use this when a non-disclosure agreement lands and you need to decide whether to sign as-is, negotiate, or reject. It works for both mutual and one-way NDAs, inbound or outbound, before you exchange anything sensitive.

**Not for:** a full commercial contract or MSA (use coml-saas-msa-review), a services agreement (coml-vendor-agreement-review), or picking which review path applies at all (coml-review). If you have no playbook yet, run coml-cold-start-interview first.

## Method

1. Identify direction and mutuality: are you the discloser, the recipient, or both? A one-way NDA that binds only you as recipient deserves the most scrutiny.
2. Walk each clause against the NDA table below: term, definition of Confidential Information, carve-outs, residuals, remedies, and governing law. Mark each as standard / fallback / walk-away.
3. **Escalation gate:** any walk-away term, a residuals clause, perpetual confidentiality on ordinary information, or non-standard governing law goes to counsel before you respond — do not sign around it.
4. Draft specific edits for each fallback or walk-away deviation, quoting the offending language and the replacement.
5. Set the verdict: sign (all standard/fallback), negotiate (fixable deviations), or reject (walk-away with no movement).

## Example

Inbound one-way NDA binding you as recipient, 5-year term, CI = "all information disclosed", no carve-outs, broad residuals. Deviations: one-way (fallback — you are only receiving, acceptable), no carve-outs (walk-away), broad residuals (walk-away). Verdict: negotiate. Edits: add the four standard carve-outs; strike the residuals clause; cap term at 3 years. Escalated the residuals language to counsel before sending.

## Pitfalls

- Treating "all information disclosed" as harmless — with no carve-outs it captures things you already knew or later develop independently.
- Missing a residuals clause that quietly lets the other side reuse what its people remember.
- Signing a one-way NDA that binds you as recipient without checking whether it should be mutual.
- Accepting the counterparty's home forum plus fee-shifting.

## Output format

```
NDA REVIEW — <parties> | direction: <mutual/one-way> | date
Verdict: SIGN | NEGOTIATE | REJECT
Deviations:
  - <clause>: <standard|fallback|walk-away> — <quote> → <proposed edit>
Escalated to counsel: <items or none>
Next step: <sign / send redline / decline>
```

## Reference

**Attorney-escalation gate** — route to counsel before agreeing, never decide alone, on: uncapped or one-sided liability, IP assignment or ownership shifts, indemnity you would owe for the vendor's own product, data-breach or privacy obligations, non-standard governing law or mandatory arbitration, anything a business owner cannot reverse, or any deal above your signing authority.

### NDA clauses
| Clause | Standard | Fallback | Walk-away |
|---|---|---|---|
| Term | 2-3 yr (trade secrets survive longer) | up to 5 yr | perpetual on ordinary CI |
| Mutuality | mutual | one-way when we only disclose | one-way binding us as recipient |
| CI definition | marked or reasonably identifiable | all disclosed | "anything discussed", no carve-outs |
| Carve-outs | public / independently developed / rightfully received / compelled | narrowed set | none |
| Residuals | none | narrow, memory-only | broad reuse license |
| Remedies / law | mutual injunctive, our or neutral law | neutral law, no bond | one-sided + liquidated damages |

### SaaS / MSA clauses
| Clause | Standard | Fallback | Walk-away |
|---|---|---|---|
| Liability cap | 12 mo fees | 24 mo fees | uncapped for us / their cap ≤3 mo |
| Cap carve-outs | IP, confidentiality, data breach | + willful misconduct | breach uncapped against us only |
| Indemnity | mutual IP; vendor covers data breach | mutual | we indemnify their product |
| Data | customer owns; export on exit | customer owns | vendor licenses or resells data |
| Security / SLA | SOC 2 + 99.9% + credits | 99.5% | no SLA, no security terms |
| Auto-renew | opt-in, 30-day notice | 60-day notice | evergreen, 90-day, uncapped uplift |
| Price increase | CPI or ≤5% | ≤7% | uncapped at renewal |

### Vendor / services clauses
| Clause | Standard | Fallback | Walk-away |
|---|---|---|---|
| Payment | net-30 / net-45 | net-15 | full prepay, no milestones |
| IP in deliverables | work-for-hire to us | perpetual license to us | vendor retains |
| Insurance | ≥$1M GL + cyber | $500K | none |
| Termination | for cause + convenience, 30-day | for cause only | locked full term, no exit |
| Audit / compliance | annual audit right | on cause | none |

### Renewal-notice tracking
| Field | Capture |
|---|---|
| Effective / expiry date | contract dates |
| Notice window | e.g. 60 days pre-expiry |
| Notice deadline | expiry − window (put on the calendar) |
| Auto-renew | yes/no + renewal term |
| Reminders | 90 / 60 / 30-day pings to the owner |

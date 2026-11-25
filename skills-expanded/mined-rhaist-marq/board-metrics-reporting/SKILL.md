---
name: board-metrics-reporting
description: "Guides reporting cyber risk upward to a board or executives: translating technical posture into business-risk language, what belongs on a board deck, reporting cadence, and the questions directors ask. Use when the user needs to prepare a board or exec briefing, a quarterly cyber risk report, or present security posture to non-technical leaders. (Designing the metric set itself: security-metrics.)"
license: Apache-2.0
metadata:
  verified: "2026-11-17"
---

# Board metrics & reporting

The board doesn't want security data; they want to know "are we okay, what's it
cost, what do you need." Translate technical posture into risk and money.
Frame to a recognized model so it travels (NIST CSF function maturity, or
financial risk via FAIR: loss = frequency × magnitude, in dollars).

## Vanity vs actionable metrics

A metric earns its slide only if a _bad number changes a decision_. If nothing
happens when it moves, cut it.

| Vanity (don't lead with)   | Why it's noise                             | Report instead                                              |
| -------------------------- | ------------------------------------------ | ----------------------------------------------------------- |
| # attacks/events blocked   | Big scary number, no decision attached     | Incidents that reached impact + dwell time                  |
| # vulnerabilities found    | Rewards finding, not fixing; grows forever | % critical/exposed remediated within SLA + aging backlog    |
| Patches deployed           | Activity, not outcome                      | Mean time to remediate (MTTR) KEV/critical, internet-facing |
| Training completion %      | Clicking "done" ≠ behavior change          | Phishing-sim click & report rate, trend                     |
| "We're 92% NIST compliant" | Compliance ≠ secure; gameable              | Maturity trend on the functions that gate top risks         |
| Tool/dashboard counts      | Spend, not protection                      | Coverage: % crown jewels with MFA / logging / EDR           |

## Metrics that actually move decisions

- **Coverage gaps on crown jewels**: % of critical assets _without_ MFA / EDR /
  logging / tested backup. Each gap is a specific board ask with a price tag.
- **MTTD / MTTR**: time to detect and to remediate. Dwell time is the number
  attackers care about; shrinking it is the program's headline.
- **Risk reduction over time**: top risks from the register (`load_skill
risk-assessment`), their score now vs last quarter, and what moved them. Shows
  the budget bought something.
- **SLA adherence on exposed criticals**: % patched within tier SLA, and the
  aging backlog (how long the oldest unpatched KEV item has sat). A growing
  backlog is the early-warning light.
- **Third-party / supply-chain exposure**: # critical vendors, # unassessed.
- **Incident trend & cost**: count by severity, dwell time, $ impact / near-misses.

## Framing risk for a board (rules)

1. Lead with the answer: "Top 3 risks, here's where each stands, here's what I
   need." Detail is appendix.
2. Money and business outcome, not CVEs. "A ransomware hit could halt order
   processing for ~5 days, est. $X" beats "we have 40 criticals."
3. Trend > snapshot. An arrow (better/worse since last quarter) means more than
   any single value. Always show direction.
4. Red/amber/green by risk area, but every red needs an owner, an ask, and a date.
   No naked reds.
5. Be honest about residual risk. The board's job is to _accept_ risk; give them a
   clear, owned decision to accept or fund; don't hide it or cry wolf.
6. Tie spend to risk bought down. Every dollar maps to a risk moved, or it's
   questioned next cycle.
7. For US public companies, disclosure is a board clock, not just the CISO's: a
   **material** incident → **Form 8-K Item 1.05 within 4 business days** of the
   materiality determination, plus annual **10-K** cyber governance/oversight
   disclosure (Reg S-K Item 106). Board cyber oversight is itself reportable; brief
   them so the filing isn't the first they hear of a breach.

## Cadence

- **Board: quarterly**: 3 to 5 slides: top risks + trend, posture vs plan, incidents
  since last, the ask. ~10 minutes of talking.
- **Exec/risk committee: monthly**: KPIs, SLA adherence, in-flight initiatives.
- **Out-of-cycle: any Sev-1/2 incident or material change**: don't let the board
  first hear of a breach from the news or a regulator.
- **Annual**: strategy & budget review, independent validation results (pentest /
  red team: commission externally; marq runs none), re-baselined maturity.

## Building the deck from marq output

- `read_file /work/findings.md` and the risk register; the engagement's confirmed
  findings are the evidence behind your risk slide. Aggregate, don't paste raw rows;
  the board wants the 3 themes, not 200 findings.
- Use the prioritized list (`load_skill vulnerability-prioritization`) so "top
  risks" reflects exploitability and exposure, not just CVSS count.
- Keep the technical detail as a `render_report` appendix for the auditor/regulator;
  the board sees the one-page translation.

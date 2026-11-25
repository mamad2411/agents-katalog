---
name: risk-assessment
description: Guides a structured asset-threat-likelihood-impact risk assessment with 5x5 scoring and treatment choice, emitting a risk register. Use when the user asks to run a cyber or information-security risk assessment, build or update a risk register, score risks, or choose risk treatment (mitigate, transfer, accept, avoid).
license: Apache-2.0
metadata:
  verified: "2026-11-17"
---

# Risk assessment workflow

Turn loose findings into a scored, treatable register. Consume recorded findings
first: `read_file /work/findings.md` (or `findings.jsonl`; marq records OSINT exposures, and pentest results
staged in `/work` work too). Each confirmed
finding is a candidate risk. Don't re-discover what the engagement already proved.

## 1. Scope the assets

- List assets in scope: systems, data stores, processes, third parties. One row each.
- Tag each with a value driver: confidentiality / integrity / availability it serves,
  and a rough business value (regulated data? revenue path? safety?).

## 2. Pair asset x threat

- For each asset name the realistic threats (not every STRIDE box: what actually
  applies). A finding from `findings.md` IS a threat with proof: cite its id.
- Skip theoretical threats with no exposure; note why (compensating control exists).

## 3. Score likelihood x impact (5x5)

Likelihood: how plausible in the next 12 months:

| L                | Meaning                                            |
| ---------------- | -------------------------------------------------- |
| 1 Rare           | No known path; needs insider + luck.               |
| 2 Unlikely       | Theoretical, hard, no evidence seen.               |
| 3 Possible       | Plausible; skilled attacker, some barrier.         |
| 4 Likely         | Easy/known technique; exposure confirmed in recon. |
| 5 Almost certain | Trivial / actively exploited / already happening.  |

Impact: worst credible business outcome:

| I            | Meaning                                                   |
| ------------ | --------------------------------------------------------- |
| 1 Negligible | Cosmetic; no data/availability loss.                      |
| 2 Minor      | Single user/record; quick recovery.                       |
| 3 Moderate   | Limited breach, SLA breach, modest fine.                  |
| 4 Major      | Sensitive data loss, multi-day outage, regulatory report. |
| 5 Severe     | Mass breach, safety, existential fine, license loss.      |

Risk = L x I (1-25). Bands: 1-4 Low, 5-9 Medium, 10-15 High, 16-25 Critical.
A pentest finding's severity maps in as a sanity check; if a Critical finding
scores Low here, your likelihood is probably wrong; reconcile, don't average.

## 4. Choose treatment

| Option   | Pick when                                                                                                   |
| -------- | ----------------------------------------------------------------------------------------------------------- |
| Mitigate | Cost-effective control exists and risk > appetite. Default.                                                 |
| Transfer | Loss is insurable / outsourceable; you can't reduce likelihood.                                             |
| Avoid    | Risk has no business upside; kill the feature/asset/integration.                                            |
| Accept   | Residual <= appetite, or mitigation costs more than the loss. Needs a named owner + sign-off + review date. |

## 5. Emit the register

Write `/work/risk-register.md` with `write_file`, one row per risk:

| ID  | Asset | Threat (finding ref) | L   | I   | Score | Band | Treatment | Owner | Target date | Residual |
| --- | ----- | -------------------- | --- | --- | ----- | ---- | --------- | ----- | ----------- | -------- |

- Residual = re-score L x I assuming the treatment lands.
- For each Critical/High, also `report_finding` so it flows into `render_report`
  alongside the technical findings; one deliverable, not two.

## Notes

- Qualitative 5x5 is right for triaging a register; for a **top risk driving a real spend
  decision**, complement it with a quantitative pass (FAIR-style, loss = frequency x
  magnitude in dollars) so treatment cost can be weighed against expected loss.
  `load_skill board-metrics-reporting`.
- Inherent (no controls) vs residual (with controls); state which you scored; be consistent.
- Framework-specific risk methods (ISO 27005, NIST 800-30): `load_skill iso27001,nist-csf` and
  web-fetch the current clause rather than guessing the steps.

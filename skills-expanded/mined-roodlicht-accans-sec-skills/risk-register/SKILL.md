---
name: risk-register
description: Risk-management workflow — risk identification, qualitative and quantitative analysis (likelihood × impact, FAIR basis), evaluation against risk appetite, treatment (avoid/mitigate/transfer/accept), heatmaps and trend, with ISO 31000 and ISO 27005 as the methodology base.
---

# Risk Register

> **Disclaimer**: risk management is a management responsibility. This skill helps with methodology and documentation; risk appetite, acceptance decisions, and treatment choices require ownership at the management body.

## When to use

This skill is methodological, not framework-specific. It is invoked from nearly every other GRC skill — `iso27001` (Cl 6.1), `soc2` (CC3 Risk Assessment), `nis2` (Art 21 first measure), `dora` (Art 5-14), `gdpr-pia` (Art 35 via the risk-analysis phase). Also stand-alone applicable for generic business risk management.

Triggers on:

- A question like "how do we do risk scoring", "which methodology for risk assessment", "build a heatmap", "what is risk appetite", "FAIR vs ISO 27005", "when do we accept a risk".
- A handoff from compliance skills when a risk assessment is needed.
- A periodic (quarterly/yearly) risk review.
- A new product/service/project that has a risk assessment as a precondition.
- An incident where the likelihood/impact estimate turned out skewed in hindsight — revision trajectory.

### When NOT (handoff)

- Framework-specific compliance mapping → the relevant GRC skill. This skill provides the risk method, those skills the compliance wrapping.
- Technical threat modeling at design level → `threat-modeler`. A DFD-plus-STRIDE exercise for a specific system is not an enterprise risk assessment. They complement each other: threat-modeler produces input for the risk register.
- DPIA specifically → `gdpr-pia`. A DPIA is risk analysis from the data subject's perspective, a different lens.
- Security-finding triage from scans → `cve-triage` and `security-review` have their own severity models. Those concern technical findings; this skill is about enterprise-level risks.
- Ops incident handling → `ir-runbook`. Incidents are realized risks; this skill is anticipatory.
- Financial-risk specifically (credit, market risk) is out of scope — different professional expertise.

## Approach

Seven phases. Phases 2–5 form the ISO 31000 cycle; phases 1 and 6 are preconditions, phase 7 is verification.

### 1. Methodology and register setup

Decisions in advance that frame the rest of the cycle.

- **Framework basis**: ISO 31000:2018 for principles, ISO 27005:2022 for infosec-specific implementation, NIST SP 800-30 as an alternative with strong US government adoption, FAIR for quantitative monetary risk analysis. Pick one of these plus optionally FAIR as an overlay for critical risks.
- **Taxonomy**: how do you name risks? Asset-based (per system/dataset), threat-based (per attack class), scenario-based (per business-impact scenario), or hybrid. Infosec context typically scenario-based ("leak of customer data") complemented with asset hooks.
- **Register format**: spreadsheet, GRC tool (ServiceNow, Archer, OneTrust, Drata, SafeBase), or custom DB. A spreadsheet is fine up to ~100 risks; scaling beyond that requires tooling.
- **Fields per risk**: ID, title, description (threat + vulnerability + consequence), owner, category (strategic/operational/financial/compliance/infosec), likelihood score, impact score, inherent risk, selected treatment, residual risk, controls, review date, status.
- **Scale**: 3x3, 5x5, or 10x10. 5x5 is the sweet spot — 3x3 misses nuance, 10x10 produces false precision.

### 2. Risk identification

Sources of risk input:

- **Threat modeling** (handoff to `threat-modeler`): technical threats at design/code level.
- **Incidents and near misses**: what has already happened or nearly happened? The highest-quality risk data is always your own history.
- **Threat intelligence**: ENISA threat landscape, MITRE ATT&CK, ISAC feeds, vendor advisories. See also `ioc-hunter`.
- **Workshops** with stakeholders on business-impact scenarios.
- **Frameworks**: NIS2 Art 21 / OWASP Top 10 / CIS Controls serve as a checklist for "have we forgotten this category".
- **Supplier register**: third-party risks often only become visible at this layer.

Quality check: a well-formulated risk has **threat + vulnerability + consequence** in one sentence. "A ransomware actor exploits an unpatched RDP endpoint and encrypts production data, causing X days of downtime and ~€Y damage" — not "Ransomware".

### 3. Analysis: qualitative and quantitative

**Qualitative** (ISO 27005 style): likelihood 1-5, impact 1-5, score = product.

Likelihood criteria explicit:

- 1 Negligible: < 1× per 5 years, never seen in comparable organizations.
- 2 Low: < 1× per 2 years.
- 3 Moderate: 1× per year ballpark, has occurred in the sector.
- 4 High: more than once per year, known pattern.
- 5 Certain: every month or more often, ongoing.

Impact criteria explicit (multi-dimensional, take the worst):

- Financial: € amounts with size context.
- Operational: downtime hours with criticality.
- Regulatory: fines, enforcement action, consent decree.
- Reputational: media reach, customer loss, trust erosion.
- Safety / human: physical or mental harm (for processes where that touches).

**Quantitative** (FAIR): monetary expectation distributions. Loss Event Frequency × Loss Magnitude, where each variable is a range with a distribution (Beta-PERT or Monte Carlo). Outcome: "risk X between €A and €B with 90% confidence".

When to use which: qualitative as default for the broad register, FAIR for the top-5 critical risks where a board decision on treatment budget is at stake.

Inherent risk: without controls. Residual risk: with current controls. Document both; the difference shows control effectiveness.

### 4. Evaluation: risk appetite and tolerance

A risk score is not enough. You must have a line at which it is or is not acceptable.

- **Risk appetite**: a high-level statement from the board — how much risk is acceptable per category. Example: "Zero tolerance for regulatory non-compliance incidents that result in enforcement action; moderate tolerance for operational disruptions with <4 hour recovery."
- **Risk tolerance**: concrete numerical thresholds per dimension. For example: "Operational risks with impact ≥ 4 require immediate treatment; impact 3 may be accepted with CISO sign-off."
- **Risk capacity**: maximum risk that can be absorbed (business-critical, not appetite). Typically much higher than appetite.

Risks above tolerance must go to treatment (phase 5). Risks below tolerance can be accepted or stay in the register for monitoring.

If an appetite statement is missing: this skill does not deliver a report; it forces a conversation. Without appetite, every risk score is loose change.

### 5. Treatment

Four options (ISO 31000, parallel to `threat-modeler` phase 3):

- **Avoid**: don't do it, drop the feature, stop the activity. Most strongly mitigating, sometimes commercially infeasible.
- **Modify / Mitigate**: add controls to reduce likelihood or impact. See the technical skills for implementation.
- **Share / Transfer**: contractually (SLA, cyber insurance, third-party service) or operationally (outsourcing). Transfer relocates risk; it does not eliminate it.
- **Retain / Accept**: an explicit choice to run the risk, with documentation and a deadline for re-review.

**Per treatment choice**: owner, deadline, budget, expected residual risk post-treatment, review date.

The treatment plan is a living document. Track progress on each treatment path as a project; make resource allocation visible to management.

### 6. Monitoring and review

The risk register is not an annual exercise but a continuous process.

- **Review cadence**: quarterly review of top risks with owners, an annual full review, ad-hoc on significant events (new product, incident, legislative change).
- **Trending**: how have the top-10 risks shifted over 4 quarters? New risks added, old ones gone, score shifts?
- **Heatmap**: 5x5 matrix of likelihood × impact, count per cell. Standard visualization for the board.
- **KRIs (Key Risk Indicators)**: metrics that give early signals that a risk is moving. For example: number of high-severity vulnerabilities open > 30 days as a leading indicator that "incident likelihood is rising".
- **Post-incident review** ties realized impact back to the register: was the estimate correct? Adjust for the future.

### 7. Verification-loop

Layer 1: scope (covers all categories — strategic, operational, financial, compliance, infosec, reputational?), assumptions (risk-appetite statements exist, otherwise evaluation is irrational), gaps (third-party / supply-chain considered separately, or invisibly dependent on internals?), consistency (treatment-plan deadlines lead nowhere without ownership). Layer 2: methodology references (ISO 31000, 27005, NIST 800-30, FAIR) correctly attributed, no false precision (FAIR outcomes without a Monte Carlo basis are not FAIR), heatmaps do not present a 10-dimensional report reduced to one cell.

## Output

```
Risk register — <entity/scope>
Methodology: <ISO 31000 + 27005 | NIST 800-30 | FAIR overlay>
Scale:       <3x3 | 5x5 | 10x10>
Date:        YYYY-MM-DD | Review cycle: <quarterly/yearly>

Risk-appetite statement:
  <board-approved text, per category>

Register summary:
  Total:      N risks
  Top 10:     ranked by residual-risk score
  Distribution: per category + per treatment choice

Per risk:
  ID:           R-NNN
  Title:        <threat + vulnerability + consequence in one sentence>
  Owner:        <name + role>
  Category:     <strategic/operational/financial/compliance/infosec/reputational>
  Inherent:     likelihood × impact = N
  Controls:     <current controls with effectiveness>
  Residual:     likelihood × impact = N
  Treatment:    <avoid|modify|share|retain>
  Action plan:  <owner, deadline, budget>
  Review:       <date>

Top-risks heatmap:
  <5x5 matrix, cell counts>

Trend (vs. previous quarter):
  New risks:                  N
  Accepted/retired:           N
  Score shifts:               <up/down with reason>

KRIs:
  <indicator: threshold: current value: trend>

Verification-loop: ...
```

## References

- **ISO 31000:2018** — [https://www.iso.org/standard/65694.html](https://www.iso.org/standard/65694.html). Risk management principles and guidelines, non-certifiable framework.
- **ISO/IEC 27005:2022** — [https://www.iso.org/standard/80585.html](https://www.iso.org/standard/80585.html). Infosec-specific implementation of 27001 risk management.
- **NIST SP 800-30 Rev. 1** — [https://csrc.nist.gov/pubs/sp/800/30/r1/final](https://csrc.nist.gov/pubs/sp/800/30/r1/final). Risk Assessment Guide.
- **NIST SP 800-39** — [https://csrc.nist.gov/pubs/sp/800/39/final](https://csrc.nist.gov/pubs/sp/800/39/final). Managing Information Security Risk.
- **FAIR Institute** — [https://www.fairinstitute.org/](https://www.fairinstitute.org/). Quantitative risk methodology.
- **The Open Group FAIR Standard** — [https://www.opengroup.org/fair](https://www.opengroup.org/fair). Official standard for FAIR.
- **ENISA Threat Landscape** — [https://www.enisa.europa.eu/topics/cyber-threats/threats-and-trends](https://www.enisa.europa.eu/topics/cyber-threats/threats-and-trends). Annual report, useful for risk-identification input.
- **COSO ERM Framework** — [https://www.coso.org/](https://www.coso.org/). Enterprise Risk Management framework, broader than infosec.

## Categories

- grc

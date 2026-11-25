---
name: aigov-aia-generation
version: 1.0.0
description: Generate a structured Algorithmic Impact Assessment for a specific AI use case — purpose, stakeholders, data provenance, harm taxonomy, mitigations, residual risk, and a go/mitigate/stop recommendation.
author: matrixx0070
tags: [algorithmic-impact-assessment, fria, harm-analysis, residual-risk, nist-ai-rmf, eu-ai-act]
capabilities: []
---

## When to use

Use this when one AI use case has been identified as consequential and needs documented impact analysis before deployment or continued use — typically anything provisionally tiered high-risk, anything touching people's rights or livelihoods, or anything a regulator or board will ask you to justify. Reach for it after triage flags a system, not before. The output is the impact record that supports a deploy/mitigate/stop decision and, where required, an EU AI Act fundamental-rights impact assessment (FRIA).

**Not for:** cataloguing the whole estate (use aigov-ai-inventory), the quick screen that decides whether a use case even needs an AIA (use aigov-use-case-triage), assessing a vendor's product in isolation (use aigov-vendor-ai-review), or measuring your program against a regulation clause-by-clause (use aigov-reg-gap-analysis).

This skill produces decision-support documentation, not legal advice. A qualified attorney must review the assessment — and especially any FRIA, conformity, or residual-risk conclusion — before it is relied on, disclosed, or filed with a regulator.

## Method

1. Describe the system precisely: purpose, decisions it drives, inputs/outputs, model/provider, degree of automation, and human oversight.
2. State the rationale and necessity: what problem it solves, why AI, and what less-intrusive alternatives were considered.
3. Trace data provenance: sources, lawful basis, sensitivity, representativeness, and known gaps or proxies for protected traits.
4. Map affected stakeholders and populations, with explicit attention to vulnerable groups and those who cannot opt out.
5. Enumerate harms across the taxonomy (bias/discrimination, privacy, safety, autonomy/manipulation, transparency, security) with likelihood × severity.
6. For each material harm, specify mitigations and re-rate to a **residual** risk. **Decision:** classify residual risk and choose GO / MITIGATE / STOP — STOP if residual risk to fundamental rights stays high or a prohibited practice is present.
7. Define the monitoring plan (metrics, thresholds, drift checks, incident path) and route to named sign-off, marking legal conclusions PROVISIONAL for counsel.

## Example

A bank assesses an AI loan-triage model. Rationale holds; necessity documented. Data provenance surfaces that ZIP code and shopping history act as proxies for protected characteristics — a bias harm rated high/severe. Mitigations: drop the proxies, add adverse-impact testing across groups, and require a human decision on every decline with a stated reason. Residual bias risk drops to medium. Privacy and transparency harms mitigated with a DPIA and applicant notice. Recommendation: MITIGATE — deploy only after adverse-impact test passes; monitor decline-rate disparity monthly with a rollback threshold. Flagged for counsel as provisional EU AI Act Annex III high-risk.

## Pitfalls

- **Assessing the model, not the decision.** Harm lives in the deployed decision and its context; a fair model wired into an unfair process still harms.
- **Listing harms without severity or residual re-rating.** An AIA that never converts mitigations into a residual score cannot support a defensible go/stop call.
- **Ignoring proxy variables.** Removing a protected attribute while keeping correlated proxies (ZIP, name, device) preserves discrimination and hides it.
- **A recommendation with no monitoring or kill trigger.** "GO" without thresholds, drift checks, and a rollback path means harms surface only after damage is done.

## Output format

```
# Algorithmic Impact Assessment — <use case> — <date> — v<n>
System owner: <name>    Provisional risk tier: <tier> (for counsel)

1. SYSTEM DESCRIPTION — purpose / decisions / inputs-outputs / automation / HITL
2. RATIONALE & NECESSITY — problem, why AI, alternatives considered
3. DATA PROVENANCE — sources / lawful basis / sensitivity / representativeness / gaps & proxies
4. STAKEHOLDERS & AFFECTED POPULATIONS — incl. vulnerable / non-opt-out groups
5. HARM ANALYSIS
   | Harm (bias/privacy/safety/autonomy/transparency/security) | Likelihood | Severity | Inherent |
6. MITIGATIONS -> RESIDUAL
   | Harm | Mitigation | Residual likelihood | Residual severity | Residual rating |
7. RESIDUAL-RISK RATING — overall: low / medium / high
8. RECOMMENDATION — GO / MITIGATE / STOP — conditions
9. MONITORING PLAN — metrics / thresholds / drift / incident path / review cadence
10. SIGN-OFF — owner / risk / legal (PROVISIONAL pending attorney review)

Legal conclusions PROVISIONAL. Attorney must review before reliance, disclosure, or filing.
```

## Reference

Substantive overview below — accurate to the frameworks as commonly described, not legal advice. FRIA scope, conformity conclusions, and tiering must be confirmed by counsel.

### Algorithmic Impact Assessment — canonical structure

An AIA is a structured, auditable record that a specific AI use case was analyzed for impact before and during deployment. Sections converge across the major models (Canada's Directive on Automated Decision-Making, ECP/Dutch IAMA, and the EU AI Act's FRIA):

| Section | Content | Purpose |
|---------|---------|---------|
| **System description** | Purpose, decisions driven, I/O, automation degree, human oversight | Bounds what is being assessed |
| **Rationale / necessity** | Why AI, alternatives, proportionality | Justifies the intervention |
| **Data provenance** | Sources, lawful basis, sensitivity, representativeness, proxies | Roots of bias and privacy harm |
| **Stakeholder / affected-population analysis** | Who is affected, esp. vulnerable & non-opt-out | Fundamental-rights lens |
| **Harm taxonomy** | Enumerated harms with likelihood × severity | Structured, comparable risk |
| **Mitigation measures** | Controls mapped to each harm | Shows risk is actively reduced |
| **Residual-risk rating** | Post-mitigation likelihood × severity | The basis for go/stop |
| **Monitoring plan** | Metrics, thresholds, drift, incident path | Ongoing, not one-time, assurance |
| **Sign-off** | Named accountable approvers | Accountability of record |

### Harm taxonomy (rate likelihood × severity)

- **Bias / discrimination** — disparate impact across protected groups; proxy variables; unrepresentative training data.
- **Privacy** — unlawful processing, re-identification, function creep, inadequate lawful basis (couples with a GDPR DPIA).
- **Safety** — physical or financial harm from erroneous or unsafe outputs.
- **Autonomy / manipulation** — dark patterns, undue influence, erosion of meaningful human choice.
- **Transparency** — affected people cannot tell AI is used, cannot understand or contest a decision.
- **Security** — adversarial inputs, data poisoning, model theft, prompt injection.

Score inherent risk, apply mitigations, re-score residual. Use a likelihood × severity matrix (e.g., low/medium/high each) so the go/stop threshold is explicit rather than intuitive.

### Mapping to NIST AI RMF (MEASURE and MANAGE)

The four RMF functions are GOVERN, MAP, MEASURE, MANAGE. An AIA is where **MEASURE** and **MANAGE** do their work on a single use case:
- **MEASURE** — quantify identified risks (fairness metrics, robustness, privacy leakage), test, and document methods and limits. This populates the harm-analysis and residual-rating sections.
- **MANAGE** — prioritize risks, decide on treatment (accept/mitigate/avoid/transfer), allocate resources, and stand up the monitoring and incident response. This produces the recommendation and monitoring plan.
- MAP supplies the context (from aigov-ai-inventory); GOVERN provides the policy the sign-off enforces.

### EU AI Act: high-risk conformity and the FRIA

For Annex III high-risk systems the Act layers two related but distinct obligations:

- **Conformity assessment** (provider-side): risk-management system, data governance, technical documentation, record-keeping/logging, transparency to deployers, human oversight, and accuracy/robustness/cybersecurity — evidenced before CE marking and registration in the EU database.
- **Fundamental Rights Impact Assessment (FRIA, Art. 27)** (deployer-side, for public bodies and certain private deployers of high-risk systems): describe the deployment process and period, categories of persons affected, specific risks of harm to those persons, human-oversight measures, and the governance/complaint arrangements if risks materialize. An AIA structured as above maps directly onto FRIA fields; a DPIA under GDPR may cover overlapping ground but does not substitute for the FRIA.

Because prohibited practices, high-risk classification, and FRIA applicability are legal determinations that vary by role (provider vs deployer) and jurisdiction, treat every tier and conformity statement in the AIA as PROVISIONAL until an attorney confirms it.

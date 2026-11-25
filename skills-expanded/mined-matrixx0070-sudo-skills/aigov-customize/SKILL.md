---
name: aigov-customize
version: 1.0.0
description: Tailor generic AI-governance templates — policies, AIA forms, triage rubrics, vendor checklists — to a specific organization's sector, jurisdictions, risk appetite, and roles.
author: matrixx0070
tags: [ai-governance, customization, templates, iso-42001, nist-ai-rmf, eu-ai-act]
capabilities: []
---

## When to use

Use this when you have generic governance artifacts and need to fit them to one organization's real context — its sector, the jurisdictions it operates in, its risk appetite, the frameworks it already runs (ISO/IEC 42001, NIST AI RMF), and its internal roles and escalation paths. This adapts existing templates; it does not invent new legal analysis. Run it once per org at program setup, and again when the regime, sector footprint, or org chart materially changes.

**Not for:** producing the fact pack for a specific use case (use aigov-cold-start-interview), rating a use case's risk (use aigov-use-case-triage), generating an impact assessment (use aigov-aia-generation), reviewing a vendor's AI (use aigov-vendor-ai-review), building the inventory (use aigov-ai-inventory), tracking regulatory change (use aigov-policy-monitor), first-draft policy text (use aigov-policy-starter), gap analysis against a regime (use aigov-reg-gap-analysis), or matter-file setup (use aigov-matter-workspace).

This skill is decision-support for adapting templates, not legal advice. A qualified attorney must review every customized artifact before the organization adopts, publishes, or relies on it in any matter with legal stakes.

## Method

1. Profile the organization: sector(s), operating jurisdictions, whether it acts as an AI *provider* or *deployer* (or both), risk appetite, and frameworks already adopted (ISO 42001, NIST AI RMF, sector regimes).
2. Build the regime overlay: intersect jurisdictions × role × sector to list the rules that actually bind this org, so you customize against real obligations, not a generic superset.
3. Map internal roles to accountability points: who owns approval, who signs off on high-risk, who is the escalation authority, who maintains the inventory.
4. **Decision:** does the org sit in a sector that is usually high-risk under the applicable regime (finance, health, employment, public sector, critical infrastructure)? If yes, keep the strict template defaults and tighten thresholds; if no, you may relax non-mandatory thresholds within stated risk appetite — but never relax a legally mandated control.
5. Set the customizable values: risk-tier thresholds, review cadences, approval quorums, retention periods, and the terminology/role names the org actually uses.
6. Wire the escalation gates: insert the org's real attorney-review trigger and named approver into every template rather than the placeholder.
7. Emit a customization record listing every value changed, its source, and open questions for counsel.

## Example

Org: a mid-size EU + US health-tech deployer, ISO 42001 in progress, low risk appetite. Overlay resolves to: EU AI Act (deployer duties; health context → Annex III high-risk likely), GDPR, US state health rules. Step 4 fires — health sector → keep strict defaults. Customizations: triage auto-escalates any patient-facing model to high-risk; AIA template adds a clinical-safety and DPIA-link section; vendor checklist requires training-data provenance warranty + IP indemnity; approver role renamed "AI Review Board"; attorney-review gate set to "Chief Counsel before any patient-facing deployment." Retention aligned to health-record rules. Open question for counsel: whether the org is also a *provider* for its fine-tuned model.

## Pitfalls

- **Relaxing a mandated control to fit appetite.** Risk appetite tunes discretionary thresholds only; legally required controls are floors, not preferences.
- **Ignoring the provider/deployer split.** Obligations differ sharply by role; customizing to the wrong role produces a compliant-looking but wrong artifact.
- **Leaving placeholder escalation gates.** A template that still says "[insert approver]" has no real gate. Wire the named role and attorney trigger every time.
- **Terminology drift.** If the artifact's role names don't match the org chart, no one owns the action. Map to the org's actual titles.

## Output format

```
# Governance Customization Record — <org> — <date>
Profile: sector=[...] | jurisdictions=[...] | role=[provider/deployer/both] | appetite=[low/med/high] | frameworks=[ISO 42001 / NIST AI RMF / ...]

REGIME OVERLAY (binding rules): [jurisdiction × role × sector -> rule]
SECTOR HIGH-RISK DEFAULT: <kept strict | relaxed within appetite — reason>

ROLE MAP: approver=<title> | high-risk sign-off=<title> | escalation=<title> | inventory owner=<title>

CUSTOMIZED VALUES
| Artifact | Field | Generic default | Org value | Source |
| policy   | ...   | ...             | ...       | ...    |
| AIA      | ...   | ...             | ...       | ...    |
| triage   | threshold | ...         | ...       | ...    |
| vendor   | clause | ...            | ...       | ...    |

ESCALATION GATE: attorney review -> <named role> before <trigger>
OPEN FOR COUNSEL: [ ] <question>

Adapted templates only — attorney review required before adoption or reliance.
```

## Reference

### Mapping an org to the applicable regime overlay

Customization starts by resolving which rules bind *this* org. Intersect three axes:

- **Jurisdiction** — where it builds, places on market, and deploys (users' location can pull in a regime even without local establishment).
- **Role** — provider vs deployer under the EU AI Act (see below).
- **Sector** — sector overlays add obligations on top of the horizontal regime.

The output is a scoped list of binding rules; customize against that, not a generic maximum.

### EU AI Act tiers by role: provider vs deployer

The same system carries different duties depending on your role:

| Role | Definition | Core high-risk duties |
|------|-----------|-----------------------|
| **Provider** | Develops/places on market or puts into service under own name | Risk & quality management system, data governance, technical documentation, logging, conformity assessment + CE marking, registration, post-market monitoring |
| **Deployer** | Uses an AI system under its authority in a professional capacity | Use per instructions, human oversight, input-data relevance, monitoring & incident reporting, keep logs, worker/affected-person information, run a fundamental-rights impact assessment where required (public bodies and some services) |

A deployer that substantially modifies a high-risk system, or puts its own name on it, can become a **provider** — a customization trigger, and a question for counsel.

### NIST AI RMF GOVERN function (roles, accountability, culture)

Customization is largely an exercise in the GOVERN function of the NIST AI RMF — the cross-cutting function that sets the culture and structures the other three (MAP, MEASURE, MANAGE) run inside. Tailor these GOVERN categories to the org:

| GOVERN category | What you customize |
|-----------------|--------------------|
| **GOVERN 1 Policies & processes** | Which policies apply; review cadence; thresholds aligned to legal requirements *and* risk appetite |
| **GOVERN 2 Accountability & roles** | Named owners for approval, oversight, escalation; training expectations |
| **GOVERN 3 Workforce & culture** | Diversity of review, competency requirements, reporting-without-fear norms |
| **GOVERN 4 Culture / risk communication** | How risk is surfaced and escalated; the attorney-review trigger |
| **GOVERN 5 Stakeholder engagement** | Channels for affected-party input and complaints |
| **GOVERN 6 Third-party risk** | Vendor and supply-chain requirements → feeds the vendor checklist |

If the org runs **ISO/IEC 42001** (AI management system), map GOVERN outputs to its Annex A controls and management-review cadence so the two frameworks reinforce rather than duplicate.

### Sector overlays (often high-risk)

Certain sectors routinely pull use cases into the high-risk tier or add sector-specific duties. Keep strict defaults here:

- **Finance** — credit scoring and creditworthiness are Annex III high-risk; add model-risk-management, fair-lending/anti-discrimination, and explainability requirements.
- **Health** — patient-facing and diagnostic uses carry clinical-safety, medical-device, and DPIA obligations; tie AIA to clinical governance.
- **Employment** — recruitment, screening, and worker management are Annex III high-risk; layer anti-discrimination and, where applicable, bias-audit and candidate-notice rules.
- **Public sector** — essential-service eligibility and benefits decisions are high-risk; fundamental-rights impact assessments and transparency/appeal rights apply.
- **Critical infrastructure** — safety-component uses trigger heightened reliability and oversight duties.

### Customization checklist: thresholds, gates, terminology

Concretely, tailor at least these:

- **Threshold values** — risk-tier cut-offs, autonomy limits, review cadence, approval quorum, data-retention periods. Discretionary thresholds flex with risk appetite; legally mandated ones do not.
- **Escalation gates** — insert the org's named attorney-review trigger and approver into every template; define what forces a stop (prohibited-practice hit, high-risk classification, novel data use).
- **Terminology & roles** — rename generic roles to the org's actual titles (e.g., "AI Review Board," "Chief Counsel") and align defined terms with existing policy and its ISO 42001 / NIST AI RMF vocabulary so artifacts interlock.

---
name: eu-ai-act
description: Covers the EU AI Act (Regulation (EU) 2024/1689), including provider vs deployer roles, risk tiers and prohibited practices, high-risk obligations, the GPAI track, phased dates as amended by the 2026 AI Omnibus, and penalties. Use when the user asks whether an AI system is high-risk, what obligations apply to building or using AI in the EU, GPAI model duties, or AI Act deadlines.
license: Apache-2.0
metadata:
  verified: "2026-11-17"
---

# EU AI Act

Product-safety-style regulation of AI systems placed on the EU market. Like the
CRA it binds **per system/model**, not per company, and like GDPR it is
**extraterritorial**: a US firm whose AI output is used in the EU is in scope.
Distinct from GDPR (personal data, `load_skill privacy-eu`) and from NIS2/DORA
(operational resilience, `load_skill nis2-dora`).

Canonical text (web-fetch before relying on a date or article number):
EUR-Lex Regulation (EU) 2024/1689, as amended by **Regulation (EU) 2026/1744**
("Digital Omnibus on AI", in force **27 Jul 2026**).
Commission hub: https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai

## Roles: establish this first

- **Provider**: develops/places the system on the market under its own name.
  Carries nearly all the obligations.
- **Deployer**: uses it under its own authority. Lighter duties (human
  oversight, input data, logging, worker notification), but a deployer that
  rebrands, substantially modifies, or repurposes a system to a high-risk use
  **becomes a provider**. Enterprises buying AI commonly miss this.
- Also importer / distributor / authorised representative, each with checks.

## Risk tiers

- **Unacceptable → prohibited** (Art. 5): social scoring, untargeted facial-image
  scraping, emotion inference at work/school, certain biometric categorisation,
  most real-time remote biometric ID in public for law enforcement.
- **High-risk** has two routes: **Annex I** (AI as a safety component of an already
  regulated product) and **Annex III** (listed use cases: biometrics, critical
  infrastructure, education, **employment/HR**, essential services, law
  enforcement, migration, justice). Employment/HR screening is the one that
  catches ordinary companies.
- **Transparency risk** (Art. 50): chatbots must disclose they're AI; synthetic
  content must be machine-readably marked; deepfakes and AI-generated news text
  labelled.
- **Minimal**: everything else, no obligations.
- **GPAI (general-purpose AI models)** are a parallel track, not a tier:
  documentation, copyright policy, training-data summary; **systemic-risk**
  models carry extra evaluation, incident-reporting and cybersecurity duties.

## High-risk obligations (the build list)

Risk-management system across the lifecycle · data governance and
bias-appropriate training data · technical documentation (Annex IV) · automatic
**logging** · instructions for use · **human oversight** designed in ·
accuracy/robustness/**cybersecurity** · quality-management system · conformity
assessment + CE marking + EU-database registration · post-market monitoring ·
serious-incident reporting to the market-surveillance authority.

The cybersecurity requirement is where your existing controls transfer: build
once, map with `load_skill control-mapping`; for AI-specific threats see
`load_skill ai-security`.

## Phased dates (as amended: web-verify, several just moved)

- **2 Feb 2025**: prohibitions + AI-literacy duty. In effect.
- **2 Aug 2025**: GPAI obligations. In effect. GPAI **Code of Practice** has
  been the presumption-of-adequacy route since 1 Aug 2025.
- **2 Aug 2026**: **general application**, including Art. 50 transparency and
  Commission enforcement powers over GPAI. In effect. **This date survived the omnibus.**
- **2 Dec 2026**: grace ends for Art. 50(2) machine-readable marking; new Art. 5
  prohibition on AI-generated NCII/CSAM starts.
- **2 Aug 2027**: national regulatory sandboxes (moved from 2 Aug 2026).
- **2 Dec 2027**: **Annex III high-risk obligations**, moved from 2 Aug 2026 by
  Reg (EU) 2026/1744 (a ~16-month deferral; do not quote the old date).
- **2 Aug 2028**: Annex I embedded high-risk (moved from 2 Aug 2027).

**Only one harmonised standard is cited in the OJ: EN 18286:2026**
(quality-management system, Art. 17; Implementing Decision (EU) 2026/2274,
OJ 14 Oct 2026): presumption of conformity for the QMS only. Everything else
(risk management, data, oversight, robustness, cybersecurity) is still against
the Regulation's text plus Commission guidance (final Art. 50 transparency
guidelines adopted 20 Jul 2026).

## Penalties (Art. 99: tiers unchanged by the omnibus; verify before citing)

Prohibited practices up to **€35M or 7%** of worldwide turnover; most other
obligations up to **€15M or 3%**; supplying incorrect/misleading information up
to **€7.5M or 1.5%**. Caps are lower for SMEs.

## Pitfalls

- **"We only use AI, we don't build it"**: deployers of Annex III systems still
  carry duties, and rebranding or repurposing flips you to provider.
- **HR/recruitment tooling is high-risk.** Most enterprises are in scope through
  this door, not through a flagship AI product.
- **Annex III moved to Dec 2027, but** prohibitions,
  AI literacy, GPAI and transparency are already live.
- **AI Act ≠ GDPR compliance.** Personal data in training or inference triggers
  GDPR independently, usually a DPIA (`load_skill privacy-engineering`).
- The **CRA** applies in parallel to AI shipped as a product with digital
  elements: two conformity regimes, one CE marking exercise.

## Pairs with

- `load_skill ai-security` (securing the systems + ISO 42001 / NIST AI RMF).
- `load_skill eu-cra` (product cybersecurity), `load_skill privacy-eu` (GDPR),
  `load_skill choosing-a-framework` (which regimes apply to you).
- `load_skill gap-analysis`, `load_skill control-mapping` for the build-out.

---
name: aigov-ai-inventory
version: 1.0.0
description: Build and maintain a defensible inventory of every AI system in use across an organization — in-house models, vendor AI, embedded features, and shadow AI — tagged by owner, purpose, data, and risk tier.
author: matrixx0070
tags: [ai-inventory, ai-register, governance, risk-tiering, nist-ai-rmf, eu-ai-act]
capabilities: []
---

## When to use

Use this when an organization needs a single authoritative register of the AI systems it builds, buys, or embeds — the foundation every other governance activity depends on. Reach for it at program stand-up, before an audit or regulatory filing, or when leadership cannot answer "what AI do we actually run and who owns it." The register you produce feeds triage, impact assessment, and gap analysis downstream.

**Not for:** deciding whether one specific system is high-stakes enough to escalate (use aigov-use-case-triage), writing the impact assessment for a system (use aigov-aia-generation), reviewing a single vendor's AI product (use aigov-vendor-ai-review), or comparing your controls against a named regulation (use aigov-reg-gap-analysis).

This skill is decision-support and organizational scaffolding, not legal advice. A qualified attorney must review any classification, risk tier, or regulatory characterization before it is relied on for compliance, disclosed to a regulator, or filed.

## Method

1. Define scope and sources: canvass procurement records, cloud/API spend, SaaS subscriptions with AI features, code repositories, and staff self-reports. Shadow AI hides in expense reports and browser tools.
2. For each system capture the core fields: owner, business purpose, model/provider, data inputs, deployment context, and whether humans are in the loop.
3. Classify data sensitivity and populations touched (personal data, special-category data, minors, employees, or the public).
4. **Decision:** assign a provisional EU AI Act risk tier per entry — prohibited / high-risk / limited-risk-transparency / minimal-risk — and mark it PROVISIONAL until counsel confirms; the tier drives every obligation that follows.
5. Map regulatory hooks per entry (EU AI Act annex, GDPR/DPIA trigger, sector rules) and note the NIST AI RMF MAP context established.
6. Assign a review cadence and a named accountable owner; flag entries with no owner as governance gaps.
7. Version the register and record who last verified each row and when — a stale inventory is not defensible.

## Example

A 400-person firm finds 23 AI touchpoints. Fifteen are embedded vendor features (CRM lead-scoring, an HR resume-screener, a support chatbot). Three are in-house models. Five are shadow AI — staff pasting client data into a public chatbot. The HR resume-screener is flagged PROVISIONAL high-risk (EU AI Act Annex III employment use); the public-chatbot shadow use is flagged as an urgent data-leak and possible prohibited-practice risk pending counsel. Each row gets an owner and a review date.

## Pitfalls

- **Counting only what IT provisioned.** Shadow AI and embedded vendor features are the majority of real exposure; a procurement-only sweep misses them.
- **Treating provisional tiers as final.** Risk-tier tags are legal characterizations — label them PROVISIONAL and route to counsel before acting.
- **Rows with no owner.** An entry no one is accountable for cannot be governed, reviewed, or remediated.
- **A one-time snapshot.** Systems, versions, and providers change; without a cadence and a last-verified date the register rots and misleads.

## Output format

```
# AI System Inventory — <org> — <date> — v<n>
Scope sources: [procurement / cloud spend / SaaS / repos / self-report]

## Register
| ID | System | Owner | Purpose | Model/Provider | Data inputs | Populations | Deployment | HITL | Risk tier (PROVISIONAL) | Reg hooks | Last verified |

## Shadow-AI / unowned flags
- <system> — <risk> — action

## Provisional high-risk & prohibited flags (for counsel)
- <system> — tier — basis (Annex/rule)

Risk tiers are PROVISIONAL. Attorney must confirm classification before reliance or filing.
```

## Reference

Substantive overview below — accurate to the frameworks as commonly described, but not legal advice. Tiers and obligations must be confirmed by counsel for your jurisdiction and version.

### EU AI Act risk tiers (tag every entry)

The Act (Regulation (EU) 2024/1689) sorts systems into four tiers by risk to health, safety, and fundamental rights. Each inventory row should carry a provisional tier.

| Tier | What it covers | Core obligation |
|------|----------------|-----------------|
| **Prohibited** | Unacceptable-risk practices: social scoring by public authorities, untargeted facial-image scraping, real-time remote biometric ID in public (narrow exceptions), manipulative/exploitative systems, most emotion recognition in workplace/education | Banned outright — must be identified and stopped |
| **High-risk** | Annex III use cases (employment, education, essential services, law enforcement, migration, biometrics, critical infrastructure) and safety components of regulated products | Risk management, data governance, logging, human oversight, conformity assessment, registration |
| **Limited-risk (transparency)** | Chatbots, emotion/biometric-categorization systems, deepfakes and AI-generated content | Disclosure — users must know they interact with or see AI |
| **Minimal-risk** | Everything else (spam filters, most recommenders) | No mandatory obligations; voluntary codes |

Note the separate **general-purpose AI (GPAI)** obligations for foundation-model providers (technical documentation, training-data summaries, and added duties for systemic-risk models). If your org fine-tunes or redistributes a foundation model, flag it — you may inherit provider duties.

### NIST AI RMF — the MAP function (inventory is MAP)

The NIST AI Risk Management Framework has four functions: **GOVERN** (culture, policy, accountability — cross-cutting), **MAP** (establish context and catalog risks), **MEASURE** (assess and track), and **MANAGE** (prioritize and respond). An AI inventory is the concrete deliverable of **MAP** — you cannot measure or manage systems you have not catalogued in context.

MAP categories a register operationalizes:
- **Context & purpose** — intended use, business value, and deployment setting per system.
- **Categorization** — system type, model provenance, and interdependencies.
- **Capabilities & limitations** — what each system can and cannot reliably do.
- **Risk mapping** — impacts to individuals, groups, and society; who is affected.
- **Third-party inventory** — vendor/embedded components and their supply-chain risk.

### Fields a defensible AI register needs

| Field | Why it matters |
|-------|----------------|
| Unique ID & name | Stable reference across triage/AIA/gap docs |
| Accountable owner | Governance requires a named human, not a team |
| Business purpose | Drives necessity/proportionality and tiering |
| Model / provider / version | Version changes can change risk and obligations |
| Data inputs & sensitivity | Triggers GDPR/DPIA and data-governance duties |
| Populations affected | Fundamental-rights exposure; vulnerable groups |
| Deployment context | Internal vs public, automated vs advisory |
| Human oversight | High-risk systems require meaningful HITL |
| Provisional risk tier | Sets the obligation set (confirm with counsel) |
| Regulatory hooks | EU AI Act annex, GDPR, sector rules |
| Last-verified date & verifier | Proves the register is current and maintained |

### Shadow AI and embedded AI

The highest-exposure entries are usually the least visible: staff using public chatbots with confidential data, and AI silently embedded in SaaS you already pay for. Sweep expense reports, browser extensions, and vendor release notes — vendors add AI features without renegotiating contracts, which can quietly shift your risk tier and data-processing posture.

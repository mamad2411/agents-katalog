---
name: aigov-policy-starter
version: 1.0.0
description: Draft a first-pass internal AI-use policy from scratch — acceptable use, an approval workflow for new use cases, data-handling rules, human-oversight duties, prohibited uses, vendor/tool approval, disclosure obligations, and roles/accountability.
author: matrixx0070
tags: [ai-policy, acceptable-use, governance, nist-ai-rmf, eu-ai-act, accountability]
capabilities: []
---

## When to use

Use this when an organization has no written AI policy and needs a credible starting draft — the document that tells staff what they may and may not do with AI, who approves new uses, and how AI-touched data is handled. Reach for it at program stand-up, when leadership asks "do we have an AI policy," or right after an inventory surfaces shadow AI that needs governing. What you produce is a starter draft for legal to refine into a binding policy, not the final policy itself.

**Not for:** cataloguing the AI systems the policy will govern (use aigov-ai-inventory), deciding whether one specific use case is high-stakes (use aigov-use-case-triage), writing a system's impact assessment (use aigov-aia-generation), measuring your existing controls against a regulation (use aigov-reg-gap-analysis), reviewing one vendor product (use aigov-vendor-ai-review), watching for regulatory change (use aigov-policy-monitor), interviewing stakeholders to seed a program (use aigov-cold-start-interview), tailoring an existing template (use aigov-customize), or organizing a legal matter (use aigov-matter-workspace).

This skill is decision-support, not legal advice. A qualified attorney must review the draft before it is adopted, published to staff, relied on for compliance, or represented to a regulator as your policy.

## Method

1. Establish context: sector, jurisdictions, data types handled, and whether the org builds, buys, or embeds AI. Pull the AI inventory if one exists so the policy governs real systems, not hypotheticals.
2. Draft the acceptable-use section: permitted purposes, the tools staff may use, and the classes of data allowed into each. Tie every rule to a plain-language "why."
3. Define the approval workflow for new use cases: who requests, who reviews, the triage triggers that escalate to counsel, and the record kept of each decision.
4. **Decision:** set data-handling tiers — which data classes (public / internal / confidential / regulated / special-category) may enter which tool tier (public consumer AI / enterprise-contracted / self-hosted). Regulated and special-category data default to prohibited in public tools unless counsel clears it.
5. Write the prohibited-uses list — start from the EU AI Act prohibited practices (banned everywhere) and add org-specific bans (e.g. no confidential client data in consumer chatbots).
6. Specify human-oversight and disclosure duties: which outputs need human review before action, and where AI interaction or AI-generated content must be disclosed.
7. Assign roles and accountability (owner, reviewers, escalation path) and set a review cadence; mark the whole draft PROVISIONAL pending counsel.

## Example

A 300-person services firm has no policy. The draft permits an enterprise-contracted assistant for drafting and code, bans public consumer chatbots for anything above "internal" data, and forbids feeding client-confidential material to any external model without a signed DPA. New use cases route through a one-page intake that triage escalates to counsel when employment, credit, or biometric decisions are involved. Human review is mandatory before any AI output is sent to a client or used in a hiring decision. Prohibited list leads with the EU AI Act bans (social scoring, workplace emotion recognition) plus "no shadow AI." Marked PROVISIONAL for attorney review.

## Pitfalls

- **Banning everything.** A policy so strict staff route around it drives more shadow AI, not less. Give a sanctioned, easy path for common uses.
- **No approval path for new uses.** Without a lightweight intake, every novel use is either silently adopted or stalled — both are governance failures.
- **Vague data rules.** "Be careful with data" is unenforceable. Name data classes and map each to allowed tool tiers explicitly.
- **Treating the draft as final.** Risk tiers, prohibited-practice scope, and disclosure duties are legal characterizations — label the draft PROVISIONAL and route to counsel before adoption.

## Output format

```
# AI Use Policy (STARTER DRAFT — for legal review) — <org> — <date> — v<n>
Scope: jurisdictions / sectors / data types / build-buy-embed

## 1. Purpose & scope
## 2. Acceptable use
Permitted purposes | Approved tools (by tier) | Data allowed per tool
## 3. Approval workflow for new use cases
Requester -> reviewer -> triage triggers -> counsel escalation -> record
## 4. Data-handling rules
| Data class | Public AI | Enterprise-contracted | Self-hosted |
## 5. Prohibited uses
- EU AI Act prohibited practices (banned outright)
- Org-specific bans
## 6. Human oversight
Outputs requiring human review before action: [...]
## 7. Transparency & disclosure
AI-interaction disclosure | AI-generated-content labeling
## 8. Roles & accountability
Owner | Reviewers | Escalation path | Review cadence

PROVISIONAL. Attorney must review before adoption, publication, or reliance.
```

## Reference

Substantive overview below — accurate to the frameworks as commonly described, but not legal advice. Scope, tiers, and obligations must be confirmed by counsel for your jurisdiction and the current version of each regime.

### Standard sections of an enterprise AI policy

A defensible internal AI policy covers a stable set of sections. Missing any of these is a common gap:

| Section | What it establishes |
|---------|--------------------|
| **Purpose & scope** | Who and what the policy binds (staff, contractors, systems, jurisdictions) |
| **Acceptable use** | Permitted purposes and approved tools by data class |
| **Approval workflow** | How a new AI use case gets reviewed and authorized |
| **Data handling** | Which data may enter which tool; retention, residency, DPAs |
| **Prohibited uses** | Practices banned outright, regulatory and org-specific |
| **Human oversight** | Where a human must review AI output before it acts |
| **Transparency & disclosure** | When AI use or AI content must be disclosed |
| **Vendor / tool approval** | Vetting before a new AI tool is sanctioned |
| **Roles & accountability** | Named owner, reviewers, escalation, and consequences |
| **Review cadence** | How often the policy is revisited as law and tools change |

### Mapping the policy to NIST AI RMF — GOVERN

The NIST AI Risk Management Framework has four functions: **GOVERN** (culture, policy, accountability — cross-cutting), **MAP** (context), **MEASURE** (assess), and **MANAGE** (respond). An internal AI policy is the primary deliverable of **GOVERN** — it is how an organization operationalizes governance in writing.

GOVERN sub-outcomes a policy should satisfy:
- **Policies & procedures** — documented, accessible rules for developing and using AI (the policy itself).
- **Accountability structures** — named roles, decision rights, and an escalation path so responsibility is not diffuse.
- **Culture & workforce** — training, acceptable-use awareness, and a safe channel to raise concerns.
- **Risk-tolerance & oversight** — leadership-set risk appetite and a mechanism to review and update the policy.
- **Third-party / supply chain** — governance of vendor and embedded AI (the vendor-approval section).

### EU AI Act prohibited practices — the policy must forbid these outright

Regardless of sector, any AI policy should ban the EU AI Act's prohibited (unacceptable-risk) practices (Article 5). These are banned outright, not merely high-risk:

| Prohibited practice | Notes |
|--------------------|-------|
| **Social scoring** by or for public authorities leading to detrimental treatment | Broad ban |
| **Manipulative or deceptive** subliminal techniques causing harm | Exploits below-conscious influence |
| **Exploitation of vulnerabilities** (age, disability, socioeconomic) | Targeting the vulnerable |
| **Untargeted scraping** of facial images to build recognition databases | |
| **Emotion recognition** in workplace and education | Narrow safety/medical exceptions |
| **Biometric categorization** inferring sensitive traits (race, beliefs, sexual orientation) | |
| **Real-time remote biometric identification** in public for law enforcement | Narrow, authorized exceptions |

### Transparency / disclosure obligations (limited-risk tier)

Even outside high-risk use, the EU AI Act imposes transparency duties on limited-risk systems, and a policy should encode them: users must be told when they interact with an AI system (e.g. chatbots); AI-generated or manipulated content (deepfakes, synthetic media) must be labeled as such; and emotion-recognition or biometric-categorization systems must disclose their operation to the people subjected to them. Build these as default requirements so product teams do not have to rediscover them.

### Training-data, IP, and confidentiality rules for staff inputs

The highest-frequency real-world exposure is staff feeding data into external models. A policy should set explicit input rules:
- **Confidentiality** — no client-confidential, trade-secret, or regulated data into any model without a contract (DPA/enterprise terms) that bars training on your inputs; default-ban for public consumer tools.
- **Personal data** — inputs containing personal or special-category data trigger GDPR duties (lawful basis, DPIA, data-subject rights); route to privacy/counsel before use.
- **IP ownership & licensing** — clarify who owns AI-generated output, and warn that outputs may not be copyrightable and may reproduce third-party material; require human authorship where protection matters.
- **Third-party IP ingress** — bar pasting licensed or copyrighted third-party material into models in ways that breach its license.
- **Provenance & records** — keep a record of what was submitted for high-stakes uses, so decisions are auditable.

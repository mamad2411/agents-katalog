---
name: ai-governance-15-concepts
description: The 15 essential AI governance and trust concepts from a Sivasankar Natarajan infographic (policy framework, accountability, risk classification, human oversight, data governance, model transparency, bias monitoring, security controls, auditability, explainability, compliance alignment, monitoring and drift, incident response, access and permission control, trust metrics) with its five-stage lifecycle, mapped to this repo's six governance layers, and an evidence question for each concept. Use when auditing whether an AI system has the basics of governance, writing an AI policy, or checking that nothing on a 15-point list was missed.
---

# 15 AI governance and trust concepts

Source: a 12-second video of an infographic by Sivasankar Natarajan (@shiva.bytes), "15 Essential AI Governance & Trust Concepts: the core foundations of responsible and trustworthy AI". The definitions below are the infographic's. The mapping to layers and the evidence questions are mine and are labelled as such.

The graphic draws a building on three pillars (People, Process, Technology) with the 15 concepts around it, and an **End-to-End AI Governance Lifecycle**: Design (plan responsibly and assess risks), Build (develop securely and ethically), Deploy (release with controls), Operate (monitor, oversee and improve), Evolve (the last caption is partly hidden by a watermark and appears to end "stay compliant").

| # | Concept (as printed) | Definition (as printed) | Layer in `ai-governance-layers` [my mapping] | Evidence to ask for [mine] |
|---|---|---|---|---|
| 1 | Policy Framework | Defined rules for how and where AI can be used | 2 Responsible Deployment | A written policy with an owner and a review date |
| 2 | Accountability | Clear ownership for AI decisions and outcomes | 5 Human Oversight | A named owner per system |
| 3 | Risk Classification | Classifying AI systems by potential risk and impact | 1 Inventory | A register with a risk tier per system |
| 4 | Human Oversight | Humans can review or override AI decisions when needed | 5 Human Oversight | Which decisions a person can reverse, and the last time one did |
| 5 | Data Governance | Managing data quality, security and compliance | 3 Security & Access | Data sources, owners and retention rules |
| 6 | Model Transparency | Understanding how AI systems generate their outputs | 6 Compliance & Audit | Model and version documentation |
| 7 | Bias Monitoring | Identifying and reducing unfair or discriminatory results | 4 Testing & Monitoring | A recurring test on defined groups |
| 8 | Security Controls | Protecting AI models and data from misuse or breaches | 3 Security & Access | Threat review, secrets handling, prompt-injection tests |
| 9 | Auditability | Tracking model decisions, updates and system changes | 6 Compliance & Audit | Logs that let you replay a decision |
| 10 | Explainability | Providing clear reasoning behind AI recommendations | 6 Compliance & Audit | A reason a user can read, checked for accuracy |
| 11 | Compliance Alignment | Following legal and ethical standards | 6 Compliance & Audit | A list of applicable rules and who confirmed them |
| 12 | Monitoring & Drift | Tracking performance and detecting model changes | 4 Testing & Monitoring | A metric, a threshold and an alert |
| 13 | Incident Response | Processes to manage AI failures or harmful outcomes | 4 Testing & Monitoring | A runbook and a practised drill |
| 14 | Access & Permission Control | Controlling access to AI systems | 3 Security & Access | Role-based access and a review of who has it |
| 15 | Trust Metrics | Measuring reliability, fairness and safety of AI outputs | 4 Testing & Monitoring | Defined measures reported on a schedule |

## Limits of the source

It is a concept list. It names no regulation, gives no controls and sets no thresholds, so ticking all 15 does not make a system compliant. "Explainability" and "Model Transparency" are easy to claim and hard to evidence. [Certain] Use the repo's `/ai-governance` command for a layer-by-layer audit, and this list as a completeness check.

## Procedure

1. List your AI systems (concept 3 starts here).
2. For each system, score every concept: evidence seen / claimed only / missing.
3. Report the missing ones by lifecycle stage; fix Design gaps before Operate gaps.
4. Never record a concept as met on a verbal assurance alone.

---
name: legal-category-pointer
description: "Pointer to a library of 8 specialized Legal skills. Use when working on legal-related tasks."
risk: none
---

# Legal Capability Library 🎯

This is a **pointer skill**. The 8 specialized Legal skills are stored in a hidden vault to keep your startup context minimal.

## Available skills in this category

- **advogado-criminal** — Advogado criminalista especializado em Maria da Penha, violencia domestica, feminicidio, direito penal brasileiro, medidas protetivas, inquerito policial e acao penal.
- **advogado-especialista** — Advogado especialista em todas as areas do Direito brasileiro: familia, criminal, trabalhista, tributario, consumidor, imobiliario, empresarial, civil e constitucional.
- **customs-trade-compliance** — Codified expertise for customs documentation, tariff classification, duty optimisation, restricted party screening, and regulatory compliance across multiple jurisdictions.
- **employment-contract-templates** — Templates and patterns for creating legally sound employment documentation including contracts, offer letters, and HR policies.
- **fda-food-safety-auditor** — Expert AI auditor for FDA Food Safety (FSMA), HACCP, and PCQI compliance. Reviews food facility records and preventive controls.
- **fda-medtech-compliance-auditor** — Expert AI auditor for Medical Device (SaMD) compliance, IEC 62304, and 21 CFR Part 820. Reviews DHFs, technical files, and software validation.
- **legal-advisor** — Draft privacy policies, terms of service, disclaimers, and legal notices. Creates GDPR-compliant texts, cookie policies, and data processing agreements.
- **lex** — Centralized 'Truth Engine' for cross-jurisdictional legal context (US, EU, CA) and contract scaffolding.

## How to load a skill

1. Identify the skill name above matching your task.
2. Use `view_file` to read its `SKILL.md` from the vault:
   `<CONFIG_ROOT>/.config/opencode/skill-libraries/legal/<skill-name>/SKILL.md`
3. Follow those instructions to complete the request.

**Vault path:** `<CONFIG_ROOT>/.config/opencode/skill-libraries/legal`

> Do not guess best practices — always read from the vault first.

> ⚠️ **Anti-loop guard**: Do NOT invoke skills recursively or check for applicable skills before every response. Each skill should be loaded at most once per user request. If you have already identified and loaded the relevant skill for this task, proceed with execution — do not re-scan for skills.

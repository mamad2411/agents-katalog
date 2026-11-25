---
name: master-02-business-systems
description: 02-BUSINESS-SYSTEMS domain of the master skills library (SaaS, ERP, POS, CRM, accounting, HR, e-commerce, WordPress/WooCommerce/Shopify and business automation). Use when the task needs business-system design, module logic, billing, CRM or HR workflows and no more specific installed skill matches. Not when the task is analytics dashboards (erp-saas-analytics-visualization) or SEO (seo-master).
---

# 02-BUSINESS-SYSTEMS

## Purpose
Index for SaaS, ERP, POS, CRM, accounting, HR, e-commerce, WordPress/WooCommerce/Shopify and business automation: imported skills (read in place) and a pointer to the installed skills in this domain.

## When to use
The task needs business-system design, module logic, billing, CRM or HR workflows.

## When NOT to use
- The task is analytics dashboards (erp-saas-analytics-visualization) or SEO (seo-master).
- Another domain fits better (see `../ROUTER.md`).

## Inputs
The task, project context, and constraints; domain is inferred by the orchestrator.

## Core workflow
1. Check the imported skills below; if one fits, open its `SKILL.md` and follow it.
2. Otherwise open `INSTALLED.md` in this folder (installed skills per subdomain) and invoke the matching skill with the Skill tool.
3. For cross-domain needs follow `../DEPENDENCIES.md` instead of duplicating instructions.
4. Execute, verify, report.

## Decision rules
- Prefer the most specific skill; prefer installed canonical skills over imported generic ones.
- Open one skill at a time; do not read the whole folder.

## Edge cases and failure handling
- No fitting skill -> use general capability and say no adequate skill exists; do not invent one.
- Imported skill depends on an unavailable external service -> use the nearest installed alternative.

## Validation
Check the chosen skill's instructions match the task and that its output is verified with the matching testing/validation approach.

## Output requirements
The task result as a short `DONE`; no routing narration.

## Example
Request in this domain -> orchestrator selects the skill from the list below or `INSTALLED.md` -> follow its steps -> verify -> report.

## Imported skills (read the SKILL.md at the path when relevant)
- `crm/crm-enricher/SKILL.md` - Trigger when the user wants to enrich a CRM record, contact, or company with firmographic or technographic data. Also trigger for "update my
- `crm/lead-research-assistant/SKILL.md` - Identifies high-quality leads for your product or service by analyzing your business, searching for target companies, and providing actionab
- `crm/meeting-prep/SKILL.md` - Trigger when the user is preparing for a sales call, demo, discovery call, QBR, or any prospect or customer meeting. Also trigger for "help 
- `crm/outreach-drafter/SKILL.md` - Trigger when the user wants to write a cold email, outreach sequence, LinkedIn message, or any first-touch sales message. Also trigger for "
- `hr/tailored-resume-generator/SKILL.md` - Analyzes job descriptions and generates tailored resumes that highlight relevant experience, skills, and achievements to maximize interview 
- `saas/stripe-integration/SKILL.md` - Trigger when the user wants to add Stripe payments to their app — subscriptions, one-time charges, webhooks, customer portal, or billing man

## Related skills
`../ROUTER.md`, `../DEPENDENCIES.md`, `../RULES.md`, `INSTALLED.md`.

---
name: tech-stack-architect
description: "Use when researching, recommending, or generating setup guides for technology stacks. Evaluates tools against requirements and produces implementation blueprints."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [tech-stack, tools, architecture, evaluation, setup-guide, saas]
    related_skills: [use-case-architect, sop-architect, gtm-architect]
---

# Tech Stack Architect

## Overview

Evaluates technology options against a defined set of requirements (budget, scale, team skills, compliance, integrations) and produces a recommended stack with rationale, trade-offs, and a step-by-step setup guide. Covers the full spectrum: CRM, marketing automation, analytics, dev tools, infrastructure, and AI/automation platforms.

## When to Use

- A team is evaluating tools and needs a structured comparison (e.g., HubSpot vs. Salesforce, Make vs. Zapier).
- You're building a tech stack from scratch for a new product, team, or company.
- You need a setup/integration guide for a recommended stack (how to connect Tool A to Tool B).
- An existing stack is bloated or underperforming — you need a consolidation audit.
- Don't use for: deep code-level architecture (use a software architecture skill), or hardware/infrastructure procurement.

## How It Works

1. **Requirements intake** — Gathers constraints: budget, team size/technical level, compliance needs (SOC2, GDPR, HIPAA), integration requirements, scale expectations.
2. **Market scan** — Identifies candidate tools in each category, pulling from known ecosystems and the user's existing stack.
3. **Evaluation matrix** — Scores tools across criteria: fit-to-requirement, cost, ease of adoption, ecosystem compatibility, scalability.
4. **Blueprint output** — Produces a recommended stack with a setup sequence and integration map.

## Steps

1. **Gather requirements:** Ask: What problem does the stack solve? What's the budget range? How technical is the team? What tools are already in place? What must it integrate with? Any compliance constraints?
2. **Define stack categories:** Based on the use case, identify which layers are needed (e.g., CRM, email, analytics, CDP, automation, hosting, auth, database).
3. **Evaluate per category:** For each category, present 2-4 options with:
   - Best-fit recommendation
   - Strong alternative
   - Budget option
   - Key trade-off summary
4. **Produce the stack map:** Show all recommended tools in a table: Category | Tool | Role | Monthly Cost (est.) | Integration Notes.
5. **Generate setup guide:** Write a sequenced setup plan — which tool to configure first, integration steps between tools, and configuration checkpoints.
6. **Migration notes (if replacing):** If migrating from existing tools, include data export/import steps and a cutover plan.

## Common Pitfalls

1. **Tool-first thinking:** Don't start by listing tools — start by understanding the workflow and requirements. The right tool for one team is wrong for another.
2. **Ignoring the team's skill level:** A powerful tool the team can't operate is worse than a simpler one they'll actually use.
3. **No integration map:** The best stack breaks if tools don't talk to each other. Always include how data flows between systems.
4. **Hidden costs:** Many tools look cheap at entry but spike at scale. Flag pricing tiers, per-seat costs, and API/usage limits.
5. **Over-provisioning early:** A pre-revenue startup doesn't need enterprise-grade tools. Recommend a "start here, graduate to X at Y scale" path.

## Verification Checklist

- [ ] Every requirement has been addressed in the evaluation
- [ ] At least 2 alternatives per category have been presented
- [ ] Total estimated cost fits within stated budget
- [ ] Integration map shows how tools connect
- [ ] Setup guide is sequenced and actionable
- [ ] Migration path (if applicable) is included
- [ ] Team skill requirements for each tool are noted

## Source

Originally a custom GPT: [TechStack Architect](https://chatgpt.com/g/g-68ae4db1e9e88191a905693f73f2f8b3-tech-stack-architect)

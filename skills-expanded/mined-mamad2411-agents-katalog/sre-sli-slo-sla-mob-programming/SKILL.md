---
name: sre-sli-slo-sla-mob-programming
description: use this skill to run ai-sdlc mob programming sessions for defining service level indicators, service level objectives, service level agreements, error budgets, reliability targets, and customer-impact-driven reliability reporting.
---

# SLI/SLO/SLA AI-SDLC Mob Programming Playbook

## Purpose

Use this SKILL.md as an **AI-SDLC Mob Programming playbook** for SLI, SLO, SLA, and error budget design.

This is not a generic DevOps checklist. It is a facilitation guide for a cross-functional mob session where Product, Engineering, QA, Security, SRE, DevOps, Platform, and AI collaborate to produce implementation-ready DevOps artifacts.

The goal is to leave the session with decisions, designs, checklists, risks, and backlog-ready work items.

---

## When to Use This Skill

Use this playbook when the team needs to collaboratively design, review, modernize, or validate:

- Defining reliability targets for a service
- Translating business expectations into measurable SLIs
- Creating service-level objectives
- Reviewing customer-facing SLAs
- Establishing error budgets
- Reliability reporting
- SLO-driven release decisions

Avoid using this playbook for routine status updates or simple operational tasks that do not require cross-functional design.

---

## AI-SDLC Mob Programming Objective

The mob should answer:

```text
What do we need to understand, design, test, secure, automate, monitor,
operate, and recover before this DevOps capability is implementation-ready?
```

The session should produce actionable engineering artifacts, not meeting notes.

---

## Required Tools

| Tool | Why It Is Needed |
|---|---|
| Observability Platform | Validate available metrics for SLIs |
| Service Catalog | Identify service ownership and criticality |
| Incident History | Review past reliability failures |
| Product Analytics | Understand customer journey impact |
| Alerting Tool | Connect SLO burn to alerts |
| Reporting Tool | Publish SLO and error budget reports |
| Issue Tracker | Track SLO improvement work |

---

## Required Logins / Access

| Access | Why It Is Needed |
|---|---|
| Metrics access | Validate measurable SLIs |
| Incident history access | Understand reliability patterns |
| Service ownership access | Identify accountable owners |
| Product analytics access | Connect SLOs to user impact |
| Reporting access | Publish reliability status |
| Issue tracker access | Create SLO improvement backlog |

---

## Ideal Mob Roles

| Role | Responsibility |
|---|---|
| Product Owner / Delivery Owner | Defines business priority, release impact, and delivery expectations |
| Engineering Lead | Validates technical feasibility and implementation ownership |
| DevOps Engineer | Designs automation, deployment, and environment workflows |
| SRE Engineer | Reviews reliability, monitoring, failure modes, and recovery |
| QA / Quality Engineer | Defines validation, regression, and release quality gates |
| Security Engineer | Reviews secrets, identity, access, scanning, compliance, and risk |
| Platform Engineer | Reviews reusable platform capabilities and developer experience |
| AI / Copilot Operator | Generates draft artifacts, checklists, risks, prompts, and task breakdowns |
| Facilitator | Keeps the mob focused, captures decisions, and drives deliverables |

---

## Recommended Session Flow

### 1. Service Context

Define service purpose, customers, critical journeys, business impact, and service owner.

### 2. SLI Selection

Choose indicators such as availability, latency, error rate, freshness, durability, throughput, and correctness.

### 3. SLO Definition

Define measurable objectives such as:

```text
99.9% successful checkout API responses over 30 days
P95 latency below 300ms for product search
```

### 4. Error Budget

Define budget window, burn rate, release impact, escalation threshold, and reporting cadence.

### 5. SLA Review

Clarify whether objectives are internal SLOs or external commitments.

---

## GitHub Copilot / AI Prompt

Use this prompt inside GitHub Copilot Chat or another AI assistant with repository context:

```text
Use this SKILL.md as context.

Act as an AI-SDLC Mob Programming assistant.

Help the team run a mob session for SLI, SLO, SLA, and error budget design.

Generate:
- required tools
- required access
- ideal participants
- architecture and workflow decisions
- security considerations
- testing strategy
- operational readiness checklist
- risks and edge cases
- implementation-ready deliverables
- backlog-ready stories or tasks

Do not generate generic DevOps notes.
Produce concrete engineering artifacts that can be committed into the repository.
```

---

## Expected Deliverables

The mob session should produce:

- `devops/sre/sli-slo-sla/service-sli-catalog.md`
- `devops/sre/sli-slo-sla/slo-definitions.md`
- `devops/sre/sli-slo-sla/error-budget-policy.md`
- `devops/sre/sli-slo-sla/reliability-reporting.md`
- `devops/sre/sli-slo-sla/slo-improvement-backlog.md`

---

## Implementation Readiness Checklist

- [ ] Critical journeys identified
- [ ] SLIs selected
- [ ] SLO targets defined
- [ ] Measurement source validated
- [ ] Error budget policy defined
- [ ] Alerting tied to SLO burn
- [ ] Reporting cadence defined
- [ ] Improvement backlog created

---

## Definition of Done

The session is complete when:

- The scope is clear.
- Required tools and access are identified.
- Architecture or workflow decisions are documented.
- Security and compliance concerns are reviewed.
- Testing and validation strategy is defined.
- Observability and operational readiness are addressed.
- Risks and edge cases are captured.
- Backlog-ready implementation tasks are created.
- Artifacts are ready to commit to the repository.

---

## Principle

This playbook is designed for **AI-SDLC Mob Programming**, where the team collaborates with AI to create implementation readiness across delivery, reliability, security, and operations.

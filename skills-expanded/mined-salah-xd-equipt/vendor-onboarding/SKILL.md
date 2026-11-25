---
name: vendor-onboarding
description: "Creates vendor onboarding checklists with documentation requirements, compliance checks, and setup procedures for smooth partnerships."
allowed-tools: Read Write Glob
metadata:
  author: Salah-XD
  version: "1.0"
---

# Vendor Onboarding

## When to Use This Skill

Use this skill when you need to:
- Create a standardized process for onboarding new vendors, suppliers, or service providers
- Build documentation checklists to collect before engaging a new vendor
- Set up compliance and quality checks for vendor relationships
- Design a repeatable vendor evaluation and setup workflow

**DO NOT** use this skill for employee onboarding, customer onboarding, or vendor contract negotiation. This is for the operational setup process after a vendor has been selected.

---

## Core Principle

A VENDOR ONBOARDING PROCESS PREVENTS THE TWO BIGGEST PARTNERSHIP FAILURES — MISALIGNED EXPECTATIONS AND MISSING DOCUMENTATION THAT CREATES LIABILITY.

---

## Phase 1: Vendor Profile

Gather context about the vendor relationship before building the checklist.

### Required Inputs

| Input | What to Ask | Default |
|-------|------------|---------|
| **Vendor type** | "What will this vendor provide? (software, physical goods, professional services, manufacturing)" | Professional services |
| **Relationship scope** | "One-time project or ongoing relationship?" | Ongoing |
| **Payment terms** | "How will you pay? (monthly retainer, per project, per unit)" | Monthly |
| **Risk level** | "Does this vendor handle sensitive data, customer interactions, or critical operations?" | Low-medium |
| **Industry** | "What industry are you in? (affects compliance requirements)" | General business |

**GATE: Confirm vendor profile before building the onboarding checklist.**

---

## Phase 2: Build Checklist

Create a comprehensive onboarding checklist tailored to the vendor type.

### Documentation Checklist

```
## Vendor Onboarding Checklist: [Vendor Name]

### Business Documentation
- [ ] W-9 or W-8BEN (tax identification)
- [ ] Certificate of insurance (if applicable)
- [ ] Business license or registration
- [ ] Contact information (primary + backup)
- [ ] Banking/payment details for invoicing

### Agreement Documents
- [ ] Signed contract or statement of work
- [ ] NDA (if handling confidential information)
- [ ] Service level agreement (if applicable)
- [ ] Data processing agreement (if handling personal data)
- [ ] Terms and conditions acknowledged

### Operational Setup
- [ ] Add to project management tool
- [ ] Create shared communication channel
- [ ] Grant necessary system/tool access
- [ ] Share brand guidelines or style guides
- [ ] Provide login credentials for relevant platforms
- [ ] Schedule kickoff meeting

### Compliance Checks
- [ ] Verify business registration
- [ ] Confirm insurance coverage meets requirements
- [ ] Review data handling practices (if applicable)
- [ ] Check references (for new relationships)
```

### Vendor-Type Customization

Adjust the checklist based on vendor type:
- **Software/SaaS:** Add security review, data backup provisions, uptime SLA
- **Physical goods:** Add quality standards, shipping terms, return/defect policy
- **Professional services:** Add portfolio review, deliverable templates, revision process
- **Manufacturing:** Add quality inspection schedule, sample approval process, minimum order terms

**GATE: Present checklist for user review and customization.**

---

## Phase 3: Communication Setup

Define how the vendor relationship will operate day-to-day.

### Kickoff Meeting Agenda

```
## Vendor Kickoff Meeting

**Duration:** 30-45 minutes
**Attendees:** [Your name], [Vendor contact]

1. Introductions and relationship overview (5 min)
2. Scope and deliverables review (10 min)
3. Communication norms — preferred channels, response times (5 min)
4. Reporting and check-in cadence (5 min)
5. Escalation process for issues (5 min)
6. Questions and next steps (5 min)
```

### Communication Framework

```
## Communication Norms

**Primary channel:** [Email / Slack / Project tool]
**Response time expectation:** [Within X hours for standard, X hours for urgent]
**Regular check-ins:** [Weekly / Biweekly / Monthly]
**Invoice submission:** [Process and timeline]
**Issue escalation:** [Contact person and method]
```

---

## Phase 4: Performance Framework

Set up how vendor performance will be tracked.

### Performance Metrics

Define 3-5 measurable KPIs based on vendor type:

```
## Vendor Performance Metrics

| Metric | Target | Review Frequency |
|--------|--------|-----------------|
| On-time delivery rate | 95%+ | Monthly |
| Quality score / error rate | Under 2% | Monthly |
| Response time to requests | Under 24 hours | Quarterly |
| Invoice accuracy | 100% | Per invoice |
```

### 30-60-90 Day Review Schedule

- **30 days:** Check-in on initial deliverables, communication quality, any early issues
- **60 days:** First performance review against KPIs
- **90 days:** Full review — continue, adjust, or terminate the relationship

---

## Anti-Patterns

- **Skipping the NDA** — if a vendor sees any business data, an NDA is not optional.
- **No written scope** — verbal agreements lead to scope disputes. Everything in writing.
- **Granting full system access** — give vendors the minimum access they need, not admin rights to everything.
- **No payment terms documentation** — unclear payment terms are the #1 cause of vendor conflicts.
- **Onboarding without a trial period** — always define a probationary period with clear evaluation criteria.

---

## Recovery

- **Vendor is unresponsive during onboarding:** Set a 48-hour deadline for documentation. If missed, flag it as a reliability risk before the relationship deepens.
- **Vendor pushes back on documentation:** Explain it protects both parties. If they refuse basic documentation, reconsider the partnership.
- **Missing insurance or compliance docs:** Provide templates or links to resources. Set a hard deadline before any work begins.
- **Vendor relationship already started without onboarding:** Create a retroactive checklist and schedule a "reset" meeting to fill gaps.
- **Multiple vendors to onboard at once:** Prioritize by risk level — onboard vendors handling sensitive data or critical operations first.

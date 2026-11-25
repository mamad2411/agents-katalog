---
name: business-continuity-plan
description: "Develops business continuity plans with risk assessment, recovery procedures, and communication protocols to keep operations running during crises."
allowed-tools: Read Write Glob
metadata:
  author: Salah-XD
  version: "1.0"
---

# Business Continuity Plan

## When to Use This Skill

Use this skill when you need to:
- Create a plan for keeping business operations running during disruptions
- Identify critical business functions and their recovery procedures
- Build communication protocols for emergencies and crises
- Prepare for scenarios like tech failures, health emergencies, natural disasters, or key person unavailability

**DO NOT** use this skill for cybersecurity incident response, insurance planning, or legal liability assessments. This is for operational continuity planning.

---

## Core Principle

A BUSINESS CONTINUITY PLAN IS INSURANCE YOU WRITE YOURSELF — THE TIME TO BUILD IT IS WHEN YOU DO NOT NEED IT, BECAUSE WHEN YOU NEED IT, YOU WILL NOT HAVE TIME TO BUILD IT.

---

## Phase 1: Risk Assessment

Identify what could disrupt the business and how severely.

### Required Inputs

| Input | What to Ask | Default |
|-------|------------|---------|
| **Business type** | "What does your business do and how do you deliver value?" | No default — must be provided |
| **Revenue streams** | "What are your main revenue sources?" | No default |
| **Key tools/platforms** | "What tools are critical to daily operations?" | No default |
| **Team structure** | "Is it just you, or do you have team members/contractors?" | Solopreneur |
| **Biggest fear** | "What scenario keeps you up at night business-wise?" | No default |

### Risk Identification

Score each risk on likelihood (1-5) and impact (1-5):

```
## Risk Assessment Matrix

| Risk Scenario | Likelihood | Impact | Risk Score | Priority |
|--------------|-----------|--------|-----------|----------|
| Primary tool/platform goes down | 3 | 5 | 15 | HIGH |
| Key person illness (2+ weeks) | 3 | 4 | 12 | HIGH |
| Data loss / breach | 2 | 5 | 10 | MEDIUM |
| Supplier failure | 2 | 3 | 6 | MEDIUM |
| Natural disaster | 1 | 4 | 4 | LOW |
```

**GATE: Confirm risk assessment before building recovery procedures.**

---

## Phase 2: Recovery Procedures

Build specific recovery plans for each high and medium priority risk.

### Critical Functions Map

```
## Critical Business Functions

| Function | Tools Required | Recovery Time Objective | Responsible | Backup Person |
|----------|---------------|----------------------|-------------|---------------|
| Client delivery | [tools] | 24 hours | [Name] | [Name/None] |
| Payment processing | [tools] | 4 hours | [Name] | [Name/None] |
| Communication | [tools] | 1 hour | [Name] | [Name/None] |
```

### Recovery Procedure Template

For each high-priority risk, document:

```
## Recovery Plan: [Risk Scenario]

**Trigger:** [What indicates this scenario is happening]
**Severity:** [Critical / Major / Minor]
**Recovery Time Objective:** [How fast must you recover]

### Immediate Actions (first 1-2 hours)
1. [Action step with specific instructions]
2. [Action step]
3. [Action step]

### Short-Term Recovery (24-72 hours)
1. [Action step]
2. [Action step]

### Return to Normal
1. [Action step]
2. [Post-incident review]

### Resources Needed
- [Tool, contact, document, or access needed]
```

**GATE: Present recovery procedures for review.**

---

## Phase 3: Communication Protocol

Define who gets told what, when, and how during a disruption.

### Stakeholder Communication Plan

```
## Crisis Communication Plan

| Stakeholder | Notify Within | Method | Message Template | Responsible |
|-------------|--------------|--------|-----------------|-------------|
| Active clients | 4 hours | Email | Service disruption notice | [Name] |
| Team/contractors | 1 hour | Slack/text | Operational update | [Name] |
| Key vendors | 24 hours | Email | Impact assessment | [Name] |
| Social media followers | 24 hours | Platform post | Status update | [Name] |
```

### Message Templates

Provide pre-written templates for each stakeholder group:

```
**Client notification:**
Subject: Service Update from [Business Name]

Hi [Name],

I want to let you know about [brief description of situation]. Here is what this means for you:
- [Impact on their project/service]
- [What you are doing about it]
- [Expected resolution timeline]

I will send another update by [date/time]. If you have urgent questions, [contact method].

[Name]
```

---

## Phase 4: Maintenance

Ensure the plan stays current and accessible.

### Plan Storage and Access

- Store the plan in at least 2 locations (cloud + local backup)
- Share access with any backup person or virtual assistant
- Include login credentials in a secure password manager with emergency access

### Review Schedule

- **Quarterly:** Review contact information and tool access
- **Biannually:** Test one recovery procedure end-to-end
- **Annually:** Full plan review and update
- **After any incident:** Update the plan with lessons learned

### Emergency Contacts Sheet

```
## Emergency Contacts

| Contact | Role | Phone | Email | When to Contact |
|---------|------|-------|-------|----------------|
| [Name] | Backup operator | [#] | [email] | Any major disruption |
| [Name] | Web host support | [#] | [email] | Site goes down |
| [Name] | Accountant | [#] | [email] | Financial issues |
```

---

## Anti-Patterns

- **Plan exists but no one can find it** — a plan locked in a tool that is down during the crisis is useless. Store it accessibly.
- **Too detailed to be usable** — a 50-page plan will not be read during an emergency. Keep recovery steps to 5-7 actions per scenario.
- **Single point of failure ignored** — if only you have the password, the login, or the knowledge, that IS the risk.
- **Never tested** — a plan that has never been tested is a theory, not a plan. Run a tabletop exercise annually.
- **Written once and forgotten** — business changes make old plans irrelevant. Review regularly.

---

## Recovery

- **User has no backup person:** Identify the minimum information a hired emergency VA would need to keep critical functions running for 48 hours. Document that.
- **User has too many risks to plan for:** Focus on the top 3 by risk score. A plan for 3 risks beats no plan for 20.
- **User thinks they are too small to need this:** Ask "What happens to your clients if you are in the hospital for a week?" That is the conversation starter.
- **User already experienced a disruption:** Use the incident as the first case study. Document what happened, what worked, what failed, and build the plan from there.
- **User has no team to delegate to:** Build a "break glass" document — minimum instructions for a trusted person to keep the business alive for 72 hours.

---
name: bcp-plan
description: >
  Create business continuity plans — business impact analysis, recovery strategies,
  critical processes, communication plans, and testing schedules.
  TRIGGER when: user says /bcp-plan, "business continuity plan", "BCP", "disaster recovery plan",
  "what if we lose our office", "continuity planning", or "how do we keep operating during a crisis".
argument-hint: "[business unit, scenario, critical process, or recovery objective]"
user-invocable: true
---

# Business Continuity Planning

You are a business continuity professional. Create comprehensive BCPs that ensure
the organization can maintain or rapidly restore critical operations during and
after a disruption. Plans should be practical, testable, and maintained — not
shelf documents.

## Process

### Step 1: Define BCP Scope and Governance

| Parameter | Description |
|-----------|-------------|
| **Scope** | Enterprise-wide, business unit, department, or specific process |
| **Disruption scenarios** | Natural disaster, cyber attack, pandemic, key vendor failure, facility loss, mass resignation |
| **Regulatory requirements** | Industry-specific continuity requirements (financial services, healthcare, critical infrastructure) |
| **Existing plans** | Current BCP, DR plans, incident response plans, crisis communication plans |
| **Executive sponsor** | Who owns the BCP program at the leadership level |
| **BCP coordinator** | Who maintains and tests the plan operationally |

### Step 2: Business Impact Analysis (BIA)

Identify critical business processes and quantify the impact of their disruption.

#### Process Inventory and Criticality

| Process | Department | Description | Criticality | Revenue Impact | Customer Impact | Regulatory Impact | Reputation Impact |
|---------|-----------|-------------|:-----------:|:--------------:|:--------------:|:-----------------:|:----------------:|
| Order processing | Operations | Receive, validate, fulfill orders | Critical | $[X]/day | Direct — orders stop | Contractual SLA breach | High |
| Payroll | HR/Finance | Process employee compensation | Critical | N/A | Indirect — staff impact | Labor law violation | Medium |
| Customer support | Support | Handle customer inquiries | High | Indirect — churn risk | Direct — no help available | SLA breach | High |
| Financial reporting | Finance | Produce regulatory filings | High | N/A | None | SEC/regulatory violation | High |
| Marketing campaigns | Marketing | Execute planned campaigns | Medium | Delayed pipeline | Minor | None | Low |

#### Recovery Objectives

| Process | RTO (Recovery Time Objective) | RPO (Recovery Point Objective) | MTPD (Max Tolerable Period of Disruption) | Minimum Service Level |
|---------|:-----------------------------:|:-----------------------------:|:-----------------------------------------:|----------------------|
| Order processing | 4 hours | 1 hour | 24 hours | 50% capacity |
| Payroll | 24 hours | Zero (last run) | 5 business days | Full — cannot partial pay |
| Customer support | 2 hours | 1 hour | 8 hours | Email + chat (no phone) |
| Financial reporting | 48 hours | 24 hours | Regulatory deadline | Full accuracy required |
| Marketing campaigns | 1 week | 24 hours | 2 weeks | Pause and resume |

**Recovery objective definitions:**
- **RTO**: Maximum acceptable time from disruption to restored service
- **RPO**: Maximum acceptable data loss measured in time (how far back is the latest recoverable backup)
- **MTPD**: Beyond this duration, the damage becomes unacceptable or unrecoverable

#### Dependency Mapping

| Process | Technology Dependencies | People Dependencies | Vendor Dependencies | Facility Dependencies |
|---------|----------------------|--------------------|--------------------|---------------------|
| Order processing | ERP, payment gateway, inventory DB | Operations team (min 3 staff) | Payment processor, shipping carrier | Office or remote access |
| Customer support | Ticketing system, phone/chat platform, KB | Support agents (min 5 staff) | Cloud hosting provider | Remote-capable |

### Step 3: Develop Recovery Strategies

For each critical process, define how it will be maintained or restored.

| Strategy | Description | Cost | Speed | Suitability |
|----------|-------------|:----:|:-----:|-------------|
| **Hot standby** | Fully operational duplicate environment | High | Immediate | Mission-critical, zero RTO tolerance |
| **Warm standby** | Pre-configured environment, needs activation | Medium | Hours | Critical processes, short RTO |
| **Cold standby** | Infrastructure reserved, needs full setup | Low | Days | Important but tolerant of delay |
| **Manual workaround** | Paper-based or alternate manual process | Minimal | Immediate (degraded) | Simple processes, short-term only |
| **Vendor failover** | Switch to backup vendor or provider | Medium | Hours-Days | Vendor-dependent processes |
| **Work from home** | Staff operates remotely | Low-Medium | Hours | People-dependent processes |
| **Mutual aid agreement** | Partner organization provides capacity | Low | Days | Industry-specific arrangements |

#### Recovery Strategy Assignment

| Process | Primary Strategy | Backup Strategy | Recovery Site | Key Actions |
|---------|-----------------|----------------|--------------|-------------|
| Order processing | Hot standby (cloud failover) | Manual workaround (phone orders) | Cloud DR region | Activate failover; notify customers of potential delay |
| Payroll | Warm standby (backup payroll service) | Manual calculation + emergency payment | Backup provider | Switch to backup provider; process emergency payments for affected period |
| Customer support | Work from home | Reduced channel (email only) | Remote | Activate remote access; redirect phone to email auto-responder |

### Step 4: Communication Plan

| Audience | Message | Channel | Timing | Owner | Template |
|----------|---------|---------|--------|-------|----------|
| **Employees** | Disruption notice, safety instructions, work arrangements | Email, SMS, emergency app | Within 30 minutes | HR / BCP coordinator | Template A |
| **Customers** | Service status, expected resolution, alternative channels | Email, status page, social media | Within 1 hour | Communications | Template B |
| **Vendors / Partners** | Impact assessment, adjusted timelines, coordination needs | Email, phone | Within 2 hours | Procurement | Template C |
| **Regulators** | Incident notification (if required), continuity status | Formal filing, email | Per regulatory requirement | Legal / Compliance | Template D |
| **Media** | Prepared statement (if public-facing disruption) | Press release, spokesperson | As needed | Communications | Template E |
| **Board / Investors** | Impact assessment, recovery progress, financial implications | Email, emergency board call | Within 24 hours | CEO / CFO | Template F |

**Communication escalation:**

| Severity | Communication Level | Decision Maker |
|----------|-------------------|---------------|
| Minor (single process, < 4 hrs) | Internal teams only | Department head |
| Moderate (multiple processes, 4-24 hrs) | Internal + affected customers | VP Operations |
| Major (critical processes, > 24 hrs) | All stakeholders | Executive team |
| Critical (existential threat) | All stakeholders + public | CEO + Board |

### Step 5: Plan Documentation

Document the plan in a format that is usable during an actual crisis — concise,
with clear checklists and contact information.

#### Activation Checklist

| Step | Action | Responsible | Time Target | Complete |
|:----:|--------|-------------|:-----------:|:--------:|
| 1 | Confirm disruption — assess scope and severity | BCP Coordinator | 0-15 min | [ ] |
| 2 | Activate crisis management team | BCP Coordinator | 15-30 min | [ ] |
| 3 | Assess which critical processes are affected | Department heads | 30-60 min | [ ] |
| 4 | Activate recovery strategies for affected processes | Process owners | 1-2 hrs | [ ] |
| 5 | Execute communication plan | Communications lead | Per timing table | [ ] |
| 6 | Monitor recovery progress; escalate if RTO at risk | BCP Coordinator | Ongoing | [ ] |
| 7 | Declare return to normal operations | Executive sponsor | When stable | [ ] |
| 8 | Conduct post-incident review | BCP Coordinator | Within 1 week | [ ] |

### Step 6: Testing and Maintenance

#### Testing Schedule

| Test Type | Description | Frequency | Participants | Duration |
|-----------|-------------|-----------|-------------|----------|
| **Plan review** | Read-through to verify accuracy of contacts, procedures | Quarterly | BCP coordinator, process owners | 1-2 hours |
| **Tabletop exercise** | Walk through a scenario verbally; identify gaps | Semi-annual | Crisis management team + process owners | 2-4 hours |
| **Functional test** | Activate a specific recovery strategy (e.g., failover) | Annual | IT, affected process teams | 4-8 hours |
| **Full simulation** | Simulate a real disruption end-to-end | Annual | All teams | 1-2 days |
| **Surprise drill** | Unannounced activation of specific procedures | Annual | Targeted team | 2-4 hours |

## Output Format

```markdown
## Business Continuity Plan: [Scope]

### Plan Overview
- **Scope**: [What is covered]
- **Owner**: [Executive sponsor]
- **Coordinator**: [BCP coordinator]
- **Last updated**: [Date]
- **Last tested**: [Date and type]
- **Next review**: [Date]

### Business Impact Analysis
[Process criticality table with recovery objectives]

### Dependency Map
[Technology, people, vendor, and facility dependencies per process]

### Recovery Strategies
| Process | Strategy | RTO | RPO | Recovery Actions |

### Communication Plan
| Audience | Channel | Timing | Owner | Template Location |

### Activation Checklist
[Step-by-step checklist for crisis activation]

### Contact Directory
| Role | Primary Contact | Phone | Email | Backup Contact |
|------|----------------|-------|-------|---------------|

### Recovery Procedures
For each critical process:
1. [Step-by-step recovery instructions]
2. [System access and credentials location — not in the plan itself]
3. [Vendor escalation contacts]
4. [Success criteria — how to verify recovery]

### Testing Schedule
| Test | Frequency | Next Date | Owner |

### Appendices
- A: Communication templates
- B: Vendor contact list
- C: System recovery procedures
- D: Floor plans and facility information
- E: Insurance policy summary
```

## Quality Checklist

- [ ] BIA covers all critical processes with quantified impact and recovery objectives
- [ ] Recovery strategies are defined for each critical process — not just IT disaster recovery
- [ ] Communication plan covers all stakeholder groups with specific timing and templates
- [ ] Contact directory is current — names, phones, and emails verified
- [ ] Plan is stored in multiple locations (cloud, offline, physical) so it is accessible during the disruption
- [ ] Testing schedule is defined and executed — untested plans are assumptions, not plans
- [ ] Plan is concise enough to be usable in a crisis — not a 200-page document nobody reads

## Edge Cases

- **Pandemic scenario**: Facility-based recovery strategies are useless; plan for remote operations, staff illness, and extended duration (months, not days)
- **Cyber attack / ransomware**: Recovery may require rebuilding from clean backups; assume all systems are compromised; isolate before recovering
- **Supply chain disruption**: Multi-tier dependencies mean your vendor's vendor can be the point of failure — map at least two levels deep for critical inputs
- **Regional disaster affecting multiple sites**: If primary and backup sites are in the same region, both may be affected — ensure geographic diversity
- **BCP for a startup with no redundancy**: Focus on the minimum viable operations — what must work for the company to survive? Build redundancy incrementally
- **Third-party SaaS dependency**: You cannot control their recovery — ensure you have contractual SLAs, status page monitoring, and manual workarounds for their outage

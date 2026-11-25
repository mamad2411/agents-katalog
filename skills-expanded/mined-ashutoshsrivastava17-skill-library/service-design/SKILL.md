---
name: service-design
description: >
  Design service blueprints — frontstage and backstage actions, support processes,
  physical evidence, failure points, and improvement opportunities.
  TRIGGER when: user says /service-design, "service blueprint", "design the service",
  "frontstage backstage", "service flow", "blueprint the process", or "how does our service work end-to-end".
argument-hint: "[service name, journey stage, or process to blueprint]"
user-invocable: true
---

# Service Design and Blueprinting

You are a senior service designer. Create service blueprints that map the complete
service delivery system — what the customer sees and does, what happens behind the
scenes, what support systems are involved, and where failures are likely to occur.
Blueprints should be actionable for operations, product, engineering, and CX teams.

## Process

### Step 1: Define the Service Scope

| Parameter | Description |
|-----------|-------------|
| **Service name** | The service or process being blueprinted |
| **Customer persona** | Who uses this service |
| **Scenario** | Happy path, error recovery, edge case |
| **Scope boundaries** | Start trigger and end state |
| **Channels** | Which channels are involved (digital, physical, hybrid) |
| **Existing documentation** | Current process maps, SOPs, training materials |

### Step 2: Map the Five Blueprint Lanes

Service blueprints organize information into five horizontal lanes, separated by
three key boundaries.

```
┌─────────────────────────────────────────────────┐
│  PHYSICAL EVIDENCE                              │  (What the customer sees/touches)
├─────────────────────────────────────────────────┤
│  CUSTOMER ACTIONS                               │  (What the customer does)
├─ ─ ─ ─ ─ ─ LINE OF INTERACTION ─ ─ ─ ─ ─ ─ ─ ─┤
│  FRONTSTAGE ACTIONS                             │  (Employee actions visible to customer)
├─ ─ ─ ─ ─ ─ LINE OF VISIBILITY ─ ─ ─ ─ ─ ─ ─ ─ ┤
│  BACKSTAGE ACTIONS                              │  (Employee actions invisible to customer)
├─ ─ ─ ─ ─ ─ LINE OF INTERNAL INTERACTION ─ ─ ─ ─┤
│  SUPPORT PROCESSES                              │  (Systems, tools, partners)
└─────────────────────────────────────────────────┘
```

For each step in the service, populate all five lanes:

| Step # | Physical Evidence | Customer Action | Frontstage Action | Backstage Action | Support Process |
|:------:|-------------------|----------------|-------------------|-----------------|----------------|
| 1 | Website landing page | Visits website, browses services | Chatbot greets, offers help | Content personalization engine selects content | CMS, analytics platform, recommendation engine |
| 2 | Pricing page, comparison table | Selects plan, clicks sign up | Form validates input, confirms eligibility | Credit check, fraud screening | Payment processor, identity verification API |
| 3 | Confirmation email, welcome kit | Receives confirmation, begins setup | Welcome email sent with setup guide | Account provisioned, data migrated | Email platform, provisioning system, CRM |
| 4 | Dashboard, setup wizard | Completes onboarding steps | In-app guide walks through features | Usage tracking begins, health score initialized | Product analytics, CS platform |
| 5 | Support chat, help center | Asks question during setup | Agent responds with solution | Agent consults knowledge base, escalates if needed | Ticketing system, knowledge base, Slack |

### Step 3: Identify Failure Points

Mark each step where the service is likely to break down.

| Step # | Failure Point | Probability | Impact | Detection Method | Current Mitigation | Gap |
|:------:|--------------|:-----------:|:------:|-----------------|-------------------|-----|
| 2 | Payment processor timeout | Medium | High — blocks sign-up | Error monitoring | Retry logic, fallback processor | No customer communication during retry |
| 3 | Welcome email lands in spam | High | Medium — delays onboarding | Delivery rate monitoring | SPF/DKIM configured | No alternative delivery channel |
| 4 | Setup wizard crashes mid-flow | Low | High — frustrates new user | Error tracking (Sentry) | Auto-save progress | No proactive outreach if user abandons |
| 5 | Agent gives incorrect answer | Medium | High — erodes trust | QA review, CSAT survey | Knowledge base, training | No real-time answer verification |

**Failure severity classification:**

| Severity | Definition | Response |
|----------|-----------|----------|
| **Critical** | Service cannot continue; customer is blocked | Immediate fix required; incident process |
| **Major** | Service degrades significantly; customer is frustrated | Fix within 24 hours; proactive communication |
| **Minor** | Service has friction; customer notices but can proceed | Fix in next sprint; monitor for escalation |
| **Cosmetic** | Imperfection noticed by few; no functional impact | Backlog; fix when convenient |

### Step 4: Identify Wait Points and Handoffs

| Step # | Wait Point | Customer Waits For | Expected Wait | Actual Wait | Acceptable? | Improvement |
|:------:|-----------|-------------------|:------------:|:----------:|:-----------:|-------------|
| 2-3 | Account provisioning | Confirmation email | < 1 min | 3-5 min | No | Optimize provisioning pipeline |
| 5 | Support response | Agent reply | < 2 min (chat) | 8 min avg | No | Improve staffing model |

| Step # | Handoff | From | To | Context Transferred | Context Lost | Fix |
|:------:|---------|------|-----|-------------------|-------------|-----|
| 5 | Chat to email escalation | Chat agent | Email specialist | Transcript, account info | Customer's emotional state, urgency | Add sentiment tag and priority flag |

### Step 5: Design Improvements

For each failure point, wait point, and handoff issue, design a specific improvement.

| Issue | Improvement | Blueprint Lane Affected | Effort | Impact | Priority |
|-------|------------|------------------------|--------|--------|----------|
| Payment timeout with no communication | Add real-time status message and retry indicator | Physical Evidence + Frontstage | Low | High | P1 |
| Welcome email in spam | Add in-app welcome notification as backup channel | Physical Evidence + Support Process | Medium | High | P1 |
| Long support wait | Implement AI-assisted response for common questions | Frontstage + Support Process | High | High | P2 |
| Context loss at handoff | Auto-attach transcript and sentiment to escalation | Backstage + Support Process | Medium | Medium | P2 |

### Step 6: Produce the Blueprint Document

## Output Format

```markdown
## Service Blueprint: [Service Name]

### Service Overview
- **Service**: [Name and description]
- **Persona**: [Target customer]
- **Scenario**: [Happy path / recovery / edge case]
- **Scope**: [Start trigger] to [End state]
- **Channels**: [Digital, physical, hybrid]

### Blueprint

#### Visual Blueprint
[Five-lane blueprint table — Step # x Physical Evidence, Customer Action, Frontstage, Backstage, Support Process]

#### Key Boundaries
- **Line of Interaction**: Where customer and employee interact directly
- **Line of Visibility**: What the customer can and cannot see
- **Line of Internal Interaction**: Where employee-facing and system processes divide

### Failure Point Analysis
| # | Step | Failure | Severity | Mitigation | Gap |

### Wait Points and Handoffs
[Wait point and handoff tables]

### Improvement Roadmap
| Priority | Improvement | Issue Addressed | Effort | Impact | Owner | Timeline |

### Service Metrics
| Metric | Current | Target | Measurement |
|--------|---------|--------|-------------|
| End-to-end service time | | | |
| Failure rate | | | |
| Customer effort score | | | |
| First-contact resolution | | | |
| Handoff count per service instance | | | |

### Dependencies
[Systems, teams, and third parties the service depends on]

### Next Steps
- Validate blueprint with frontline staff
- Test failure points with chaos engineering or tabletop exercises
- Review with customers for accuracy of the experience representation
```

## Quality Checklist

- [ ] All five blueprint lanes are populated for every step
- [ ] Three boundary lines (interaction, visibility, internal interaction) are clearly marked
- [ ] Failure points are identified with probability and impact, not just listed
- [ ] Wait points include both expected and actual durations
- [ ] Handoffs specify what context is and is not transferred
- [ ] Improvements are mapped back to specific blueprint lanes and steps
- [ ] Blueprint has been validated with people who actually deliver the service

## Edge Cases

- **Purely digital service with no human frontstage**: The frontstage lane becomes the UI/system responses — still map it; automated experiences still have "frontstage" behavior
- **Service with many branching paths**: Blueprint the primary happy path first, then create variant blueprints for major branches (error recovery, escalation, edge cases)
- **Third-party dependencies**: Include partner/vendor systems in the support process lane and mark them with external dependency indicators
- **Service that crosses organizational boundaries**: Use color coding or swim lanes to show which team owns each backstage and support process step
- **Seasonal or event-driven services**: Note capacity constraints and seasonal failure modes — a process that works at normal volume may break under peak load
- **Legacy systems in the support layer**: Flag technical debt that constrains service improvement — some fixes require system modernization, not just process changes

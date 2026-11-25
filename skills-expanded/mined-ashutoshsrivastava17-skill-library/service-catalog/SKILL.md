---
name: service-catalog
description: >
  Design IT service catalogs with service definition templates, SLA tiers, request fulfillment
  workflows, pricing models, and self-service portal design for streamlined IT service delivery.
  TRIGGER when: user says /service-catalog, "service catalog", "IT service catalog", "service definition",
  "request fulfillment", "service portal", "IT services list", or "service offering".
argument-hint: "[service_name or domain]"
user-invocable: true
---

# IT Service Catalog Design

You are an expert IT service management practitioner specializing in service catalog design. When the user asks you to design or improve an IT service catalog, follow this structured process to deliver a comprehensive, user-friendly, and well-governed catalog.

## Step 1: Service Inventory and Discovery

Identify all IT services to be included in the catalog:

| Discovery Method | Source | Output |
|-----------------|--------|--------|
| Stakeholder interviews | IT team leads, business managers | Service list with ownership |
| Help desk ticket analysis | Ticket categories and request types | Most requested services |
| CMDB review | Configuration item inventory | Technical service components |
| Budget/cost center review | IT financial records | Services with cost allocation |
| Existing documentation | Wiki, runbooks, SOP documents | Documented procedures |
| Shadow IT audit | SaaS subscriptions, department tools | Unmanaged services to formalize |

### Service Classification

| Category | Description | Examples |
|----------|-------------|---------|
| Business services | Directly support business processes | Email, CRM, ERP, Business Intelligence |
| Infrastructure services | Underpin business services | Network, storage, compute, database |
| Support services | Enable IT operations | Monitoring, backup, patching, security |
| End-user services | Directly consumed by employees | Laptop provisioning, software installation, VPN access |
| Project services | Temporary, project-based | New environment setup, migration support, consulting |

## Step 2: Service Definition

Create detailed service definitions for each catalog entry:

### Service Definition Template

| Field | Content |
|-------|---------|
| Service ID | SVC-001 |
| Service name | Email and Collaboration Suite |
| Category | Business Service — Communication |
| Description | Corporate email, calendar, file sharing, and video conferencing powered by Microsoft 365 |
| Service owner | IT Operations — Director of Infrastructure |
| Support team | Collaboration Services Team |
| Availability | 24/7 with 99.9% uptime target |
| Users | All employees, contractors with corporate accounts |
| Included components | Exchange Online, SharePoint, OneDrive, Teams |
| Excluded | Personal device management, third-party integrations |
| Dependencies | Azure AD, network connectivity, DNS |
| SLA tier | Gold (see SLA tier definitions) |
| Request types | New account, distribution list, shared mailbox, storage increase |
| Cost | Included in standard IT allocation / $15 per user per month |
| Documentation | Link to knowledge base articles |
| Status | Active / Under Review / Planned / Retiring |

### Service Relationship Map

```
                    ┌─────────────────────┐
                    │  Business Service    │
                    │  (Email & Collab)    │
                    └──────┬──────────────┘
                           │
              ┌────────────┼────────────┐
              │            │            │
      ┌───────┴──────┐ ┌──┴──────┐ ┌──┴──────────┐
      │ Exchange     │ │ SharePt │ │ Teams       │
      │ Online       │ │ Online  │ │             │
      └───────┬──────┘ └──┬──────┘ └──┬──────────┘
              │            │            │
              └────────────┼────────────┘
                           │
                    ┌──────┴──────────────┐
                    │  Infrastructure      │
                    │  (Azure AD, Network) │
                    └─────────────────────┘
```

## Step 3: SLA Tier Design

Define service level tiers that align with business criticality:

### SLA Tier Definitions

| SLA Element | Platinum | Gold | Silver | Bronze |
|-------------|----------|------|--------|--------|
| Availability target | 99.99% | 99.9% | 99.5% | 99.0% |
| Downtime allowed/month | 4.3 min | 43.8 min | 3.6 hours | 7.3 hours |
| Incident response (P1) | 5 min | 15 min | 30 min | 1 hour |
| Incident resolution (P1) | 1 hour | 4 hours | 8 hours | 24 hours |
| Maintenance window | Off-peak only, pre-approved | Off-peak, 5-day notice | Weekends, 3-day notice | Anytime, 1-day notice |
| Monitoring | 24/7 real-time + proactive | 24/7 real-time | Business hours + alerts | Business hours |
| Support hours | 24/7 | 24/7 for P1/P2, business hours for P3/P4 | Business hours | Business hours |
| DR/failover | Automatic failover, < 5 min RTO | Warm standby, < 1 hour RTO | Cold standby, < 4 hour RTO | Backup restore, < 24 hour RTO |
| Typical services | Revenue-critical, customer-facing | Core business operations | Internal productivity | Non-critical, back-office |

### SLA Assignment Criteria

| Factor | Weight | Assessment |
|--------|--------|-----------|
| Revenue impact of downtime | 30% | Direct revenue loss per hour |
| User count affected | 20% | Percentage of organization |
| Regulatory/compliance requirement | 20% | Mandatory uptime requirements |
| Customer-facing exposure | 15% | External users impacted |
| Alternative/workaround availability | 15% | Can users work without this service? |

## Step 4: Request Fulfillment Workflows

Design efficient workflows for service requests:

### Request Lifecycle

| Stage | Activities | SLA Target |
|-------|-----------|-----------|
| Submission | User submits request via portal/email/chat | N/A |
| Validation | Verify completeness, check entitlements | < 1 hour |
| Approval | Manager/budget/security approval as required | < 1 business day |
| Fulfillment | Technical team executes the request | Per service SLA |
| Verification | Confirm request is fulfilled correctly | < 2 hours |
| Closure | Notify user, close ticket, log completion | Same day |

### Common Request Workflows

| Request Type | Approval | Automation Level | Typical SLA |
|-------------|----------|------------------|-------------|
| Password reset | None (self-service) | Fully automated | < 5 min |
| Software installation (approved list) | None (pre-approved) | Automated with SCCM/Intune | < 1 hour |
| New user onboarding | Manager approval | Semi-automated (provisioning scripts) | < 1 business day |
| VPN access | Manager + Security | Semi-automated | < 4 hours |
| New server/VM | Manager + Budget | Automated provisioning + manual config | < 2 business days |
| Custom software request | Manager + Security + Architecture | Manual review and installation | < 5 business days |
| Data access request | Data owner + Security | Manual review, automated provisioning | < 2 business days |

### Workflow Design Principles

- Minimize approval steps (only add approvals that reduce risk)
- Automate repeatable fulfillment actions
- Provide self-service for high-volume, low-risk requests
- Include clear SLAs visible to the requester
- Enable request tracking and status visibility
- Collect satisfaction feedback after fulfillment

## Step 5: Pricing and Cost Models

Define how services are priced and charged:

### Pricing Model Options

| Model | Description | Best For | Example |
|-------|-------------|----------|---------|
| Fixed allocation | Flat fee per user or department | Standardized services, simplicity | $50/user/month for IT services |
| Tiered pricing | Different prices for different service levels | Multi-tier SLAs | Gold: $75/user, Silver: $50/user, Bronze: $30/user |
| Consumption-based | Pay per use | Variable-demand services | $0.10/GB storage, $0.05/compute-hour |
| Project-based | One-time fee for project services | Implementations, migrations | $15,000 for environment setup |
| Freemium | Basic included, premium charged | Encouraging adoption | Basic email free, advanced security $10/user |
| Cost recovery | Actual cost passed through | Transparency-focused orgs | Monthly actual cost allocated by usage |

### Cost Transparency Template

| Service | Unit Cost | Cost Driver | Allocation Method | Monthly Estimate |
|---------|-----------|-------------|-------------------|-----------------|
| Email & Collaboration | $15/user | License + support | Per user headcount | $15,000 (1000 users) |
| Cloud Infrastructure | $0.10/GB | Storage consumption | Metered usage | $5,000 (50 TB) |
| Help Desk Support | $25/ticket | Support labor | Per ticket volume | $12,500 (500 tickets) |
| Network Services | $5/user | Infrastructure amortization | Per user headcount | $5,000 (1000 users) |

## Step 6: Self-Service Portal Design

Design the user-facing portal experience:

### Portal Structure

| Section | Content | Priority |
|---------|---------|----------|
| Home / Dashboard | Quick links, my requests, announcements | Primary |
| Service catalog browse | Categories, search, featured services | Primary |
| Request forms | Structured forms per service request type | Primary |
| Knowledge base | FAQs, how-to articles, troubleshooting | Primary |
| My requests | Status tracking, history, resubmission | Secondary |
| Approvals | Pending approvals for managers | Secondary |
| Reports | Usage reports, cost reports for managers | Tertiary |
| Feedback | Satisfaction surveys, improvement suggestions | Tertiary |

### Portal UX Principles

| Principle | Implementation |
|-----------|---------------|
| Search first | Prominent search bar with auto-suggest and natural language support |
| Progressive disclosure | Show categories first, then services, then request forms |
| Mobile responsive | Functional on phone and tablet for field workers |
| Personalization | Show relevant services based on role, department, location |
| Status transparency | Real-time request status with expected completion date |
| Minimal fields | Only required fields on request forms; use defaults where possible |
| Integrated help | Contextual help text, links to knowledge articles on each form |

### Portal Technology Options

| Tool | Type | Best For |
|------|------|----------|
| ServiceNow | Enterprise ITSM | Large organizations, full ITIL suite |
| Jira Service Management | Mid-market ITSM | Atlassian shops, agile teams |
| Freshservice | Cloud ITSM | SMBs, quick deployment |
| Zendesk | Help desk + catalog | Customer-facing + internal |
| Custom (React/Angular) | Bespoke portal | Unique requirements, API-first |

## Output Format

Present the service catalog design as:

1. **Catalog Overview** (purpose, scope, governance model)
2. **Service Inventory** (categorized list with ownership and status)
3. **Service Definitions** (detailed template for each service)
4. **SLA Tier Framework** (tier definitions, assignment criteria)
5. **Request Fulfillment Workflows** (lifecycle, workflows by request type)
6. **Pricing Model** (model selected, cost transparency per service)
7. **Portal Design** (structure, UX principles, technology recommendation)
8. **Governance and Maintenance Plan** (review cadence, change process, metrics)

## Quality Checklist

Before delivering the service catalog, verify:

- [ ] All IT services are identified and categorized
- [ ] Each service has a complete definition with owner and support team
- [ ] SLA tiers are defined with measurable targets
- [ ] Request fulfillment workflows are documented for all request types
- [ ] Pricing model is clear and aligned with finance expectations
- [ ] Portal design is user-centric with search, browse, and self-service
- [ ] Service relationships and dependencies are mapped
- [ ] Governance plan includes review cadence and change process
- [ ] Catalog is accessible to all intended users

## Edge Cases

- **Services shared across business units**: Create a single catalog entry with business unit-specific SLA addendums and cost allocation rules
- **Legacy services being retired**: Mark as "Retiring" with end-of-life date and migration path to replacement service
- **Shadow IT services discovered**: Assess risk and value; either formalize into the catalog with proper governance or provide a sanctioned alternative
- **Rapidly changing cloud services**: Use a modular catalog structure; update individual service entries without restructuring the entire catalog
- **Regulated environments requiring audit trails**: Implement version control for service definitions; log all changes with approver and timestamp
- **Multi-language or multi-region organizations**: Design the catalog with localization support; define regional SLA variations where time zones affect support hours

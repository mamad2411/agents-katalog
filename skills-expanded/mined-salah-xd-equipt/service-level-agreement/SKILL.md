---
name: service-level-agreement
description: "Drafts service level agreements with response times, uptime commitments, penalty and credit structures, and performance metrics."
allowed-tools: Read Write Glob
metadata:
  author: Salah-XD
  version: "1.0"
---

# Service Level Agreement

## When to Use This Skill

Use this skill when you need to:
- Draft a service level agreement (SLA) for clients or partners
- Define response times, uptime commitments, and quality standards
- Create penalty and credit structures for SLA breaches
- Formalize service expectations into a measurable agreement

**DO NOT** use this skill for full legal contracts (consult a lawyer), internal OKRs, or project scopes. This is for drafting the SLA portion of a business relationship.

---

## Core Principle

AN SLA SETS THE FLOOR, NOT THE CEILING — IT DEFINES THE MINIMUM ACCEPTABLE SERVICE LEVEL SO BOTH PARTIES KNOW EXACTLY WHAT TO EXPECT AND WHAT HAPPENS WHEN EXPECTATIONS ARE NOT MET.

---

## Phase 1: Define Terms

Establish the scope and context of the SLA.

### Required Inputs

| Input | What to Ask | Default |
|-------|------------|---------|
| **Service description** | "What service are you providing?" | No default |
| **Client type** | "Who is the client? (enterprise, SMB, consumer)" | SMB |
| **Service model** | "How is the service delivered? (SaaS, retainer, project, support)" | Retainer |
| **Current commitments** | "What are you already promising informally?" | No default |
| **Pain points** | "What service issues have caused friction with clients?" | Response time |
| **Measurement tools** | "How do you track service performance?" | Basic (email, project tool) |

**GATE: Confirm service scope before drafting the SLA.**

---

## Phase 2: Draft SLA

Write the service level agreement.

### SLA Template

```
# Service Level Agreement

**Between:** [Your Business Name] ("Provider")
**And:** [Client Name] ("Client")
**Effective date:** [Date]
**Review date:** [Date — typically annual]

---

## 1. Service Description

[2-3 sentences describing the service covered by this SLA]

## 2. Service Availability (if applicable)

| Metric | Commitment |
|--------|-----------|
| Uptime target | [99.5% / 99.9%] monthly |
| Planned maintenance window | [Day/time — with 48-hour advance notice] |
| Excluded downtime | [Scheduled maintenance, force majeure, third-party outages] |

## 3. Response Times

| Priority | Description | Response Time | Resolution Target |
|----------|------------|--------------|-------------------|
| Critical | Service is down / major business impact | [1 hour] | [4 hours] |
| High | Feature impaired / significant impact | [4 hours] | [1 business day] |
| Medium | Minor issue / workaround available | [8 hours] | [3 business days] |
| Low | Question or enhancement request | [1 business day] | [5 business days] |

**Business hours:** [Hours and timezone]
**After-hours support:** [Available / Not available / Emergency only]

## 4. Performance Metrics

| Metric | Target | Measurement Method | Reporting Frequency |
|--------|--------|-------------------|-------------------|
| [Response time compliance] | [95%+] | [Support tool tracking] | [Monthly] |
| [Quality score] | [Target] | [Measurement method] | [Frequency] |
| [Deliverable timeliness] | [95%+] | [Project tool tracking] | [Monthly] |

## 5. Remedies and Credits

| SLA Breach | Credit / Remedy |
|-----------|----------------|
| Uptime below [X]% in a month | [X]% credit on monthly fee |
| Response time missed 3+ times in a month | [X]% credit or free service extension |
| Critical issue unresolved beyond [X] hours | [Escalation to senior team + credit] |

**Credit cap:** Total credits shall not exceed [X]% of monthly service fees.
**Credit process:** Client must request credit within [30] days of the breach.

## 6. Exclusions

This SLA does not apply to:
- Issues caused by client actions or third-party systems
- Force majeure events
- Scheduled maintenance (with advance notice)
- Features or services not covered by the agreement

## 7. Reporting

Provider will deliver a monthly service report including:
- Uptime percentage
- Response time compliance
- Open and resolved issues
- Any SLA breaches and remedies applied

## 8. Review and Amendment

This SLA will be reviewed [annually / at contract renewal]. Changes require written agreement from both parties.

---

**Provider signature:** _______________  Date: ___
**Client signature:** _______________  Date: ___
```

**GATE: Present the SLA draft for review and negotiation.**

---

## Phase 3: Customize

Tailor the SLA to the specific service and relationship.

### Service-Specific Additions

**For SaaS / Digital Products:**
- Data backup frequency and recovery time
- Security incident notification timeline
- API uptime and rate limits

**For Retainer / Agency Services:**
- Deliverable revision limits
- Communication response expectations
- Scope change process

**For Managed Services:**
- Proactive monitoring commitments
- Regular reporting cadence
- Escalation procedures with named contacts

### Credit Structure Guidelines

- Credits should be meaningful enough to incentivize performance but not bankrupt the provider
- Typical range: 5-25% of monthly fee per breach type
- Cap total credits at 50-100% of one month's fees
- Always require the client to request credits (do not auto-apply)

---

## Phase 4: Operationalize

Set up tracking and reporting to meet SLA commitments.

### SLA Tracking Dashboard

```
## Monthly SLA Report — [Month]

| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| Uptime | [X]% | [X]% | Met / Missed |
| Avg response time (Critical) | [X hours] | [X hours] | Met / Missed |
| Deliverable timeliness | [X]% | [X]% | Met / Missed |

**Breaches this month:** [#]
**Credits owed:** $[X]
**Notes:** [Context for any misses]
```

### Internal Alerts

Set up notifications before SLA breaches:
- Alert at 50% of response time window ("You have 2 hours left on this critical ticket")
- Alert when uptime approaches threshold
- Weekly review of SLA compliance

---

## Anti-Patterns

- **Promising what you cannot deliver** — set targets you can consistently meet, then exceed them. Under-promise, over-deliver.
- **No measurement system** — an SLA without tracking is just words. You need data.
- **Overly complex SLAs** — a 10-page SLA for a $500/month retainer is overkill. Match complexity to the relationship.
- **No exclusions** — without clear exclusions, you are liable for third-party failures and acts of nature.
- **Credits without caps** — uncapped credits can bankrupt your business in a bad month. Always cap.

---

## Recovery

- **Client demands unrealistic SLA terms:** Counter with data on industry standards. Offer a premium tier with tighter SLAs at a higher price.
- **SLA was breached:** Acknowledge it proactively, apply the credit before being asked, and explain what you are doing to prevent recurrence.
- **User has no tracking tools:** Start with a simple spreadsheet. Track response times manually until volume justifies a tool investment.
- **Client never reads the SLA:** Walk through the key commitments in a meeting. Highlight what they can expect and how to report issues.
- **SLA is too expensive to fulfill:** The SLA targets may be too aggressive, or the pricing does not account for the required service level. Adjust one or both.

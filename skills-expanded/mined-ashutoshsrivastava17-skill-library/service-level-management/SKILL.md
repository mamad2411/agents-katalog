---
name: service-level-management
description: >
  Manage service levels with SLA definition, OLA/UC alignment, monitoring setup, reporting cadence,
  and continuous improvement planning for reliable and measurable IT service delivery.
  TRIGGER when: user says /service-level-management, "service level management", "SLA definition", "SLA monitoring",
  "OLA", "underpinning contract", "service level agreement", "SLA reporting", or "SLA improvement".
argument-hint: "[service_name or SLA_scope]"
user-invocable: true
---

# Service Level Management

You are an expert IT service management practitioner specializing in service level management. When the user asks you to define, monitor, or improve service levels, follow this structured process to deliver measurable, achievable, and business-aligned service level agreements.

## Step 1: Business Requirements Gathering

Understand what the business needs from IT services before defining SLAs:

| Requirement Area | Questions to Answer |
|------------------|---------------------|
| Business criticality | How critical is this service to business operations? |
| Revenue impact | What is the cost per hour of downtime? |
| User expectations | What do users consider acceptable performance? |
| Regulatory requirements | Are there mandated uptime or response time requirements? |
| Competitive benchmark | What do competitors or industry standards offer? |
| Budget constraints | What level of service can the organization afford? |
| Risk tolerance | How much variability in service quality is acceptable? |
| Escalation expectations | Who should be notified and when if SLAs are at risk? |

### Service Criticality Assessment

| Factor | Weight | Score (1-5) | Weighted Score |
|--------|--------|-------------|----------------|
| Revenue impact per hour of downtime | 25% | [1-5] | [calculated] |
| Number of users affected | 20% | [1-5] | [calculated] |
| Regulatory/compliance requirement | 20% | [1-5] | [calculated] |
| Customer-facing exposure | 15% | [1-5] | [calculated] |
| Availability of workaround | 10% | [1-5] | [calculated] |
| Reputational risk | 10% | [1-5] | [calculated] |
| **Total Criticality Score** | **100%** | — | **[sum]** |

| Score Range | Criticality | Recommended SLA Tier |
|-------------|------------|---------------------|
| 4.0-5.0 | Critical | Platinum (99.99%) |
| 3.0-3.9 | High | Gold (99.9%) |
| 2.0-2.9 | Medium | Silver (99.5%) |
| 1.0-1.9 | Low | Bronze (99.0%) |

## Step 2: SLA Definition

Create comprehensive, measurable service level agreements:

### SLA Structure Template

| SLA Section | Content |
|-------------|---------|
| Agreement overview | Parties, service name, effective dates, review schedule |
| Service description | What the service provides and does not provide |
| Service hours | When the service is available (24/7, business hours) |
| Availability target | Uptime percentage and measurement method |
| Performance targets | Response time, throughput, error rate targets |
| Support levels | Incident response and resolution times by severity |
| Maintenance windows | Scheduled maintenance periods (excluded from availability) |
| Exclusions | What is explicitly not covered by the SLA |
| Measurement and reporting | How metrics are collected, calculated, and reported |
| Penalties/credits | Consequences of SLA breach (service credits, financial) |
| Review and amendment | Process for updating the SLA |
| Escalation contacts | Contact matrix for SLA issues |

### SLA Metrics Definition

| Metric | Definition | Formula | Target | Measurement Window |
|--------|-----------|---------|--------|-------------------|
| Availability | Percentage of time service is operational | (Total time - Downtime) / Total time * 100% | 99.9% | Monthly, rolling |
| Incident response time | Time from incident report to first response | Timestamp(first response) - Timestamp(reported) | P1: 15 min, P2: 30 min | Per incident |
| Incident resolution time | Time from report to service restoration | Timestamp(resolved) - Timestamp(reported) | P1: 4 hours, P2: 8 hours | Per incident |
| Request fulfillment time | Time from request submission to completion | Timestamp(fulfilled) - Timestamp(submitted) | Standard: 2 business days | Per request |
| Performance (response time) | Application response time at specified percentile | p95 response time over measurement window | < 500 ms (p95) | Weekly |
| Throughput | Transactions processed per time unit | Count of successful transactions per second | > 1,000 TPS | Continuous |
| Error rate | Percentage of requests resulting in errors | Error count / Total requests * 100% | < 0.1% | Daily |

### Availability Conversion Table

| Availability Target | Allowed Downtime/Month | Allowed Downtime/Year | Typical Tier |
|--------------------|-----------------------|----------------------|-------------|
| 99.0% | 7 hours 18 min | 3 days 15 hours | Bronze |
| 99.5% | 3 hours 39 min | 1 day 19 hours | Silver |
| 99.9% | 43 min 50 sec | 8 hours 46 min | Gold |
| 99.95% | 21 min 55 sec | 4 hours 23 min | Gold+ |
| 99.99% | 4 min 23 sec | 52 min 36 sec | Platinum |
| 99.999% | 26 sec | 5 min 16 sec | Five Nines |

## Step 3: OLA and Underpinning Contract Alignment

Ensure internal and external agreements support the SLA:

### Agreement Hierarchy

```
┌────────────────────────────────────┐
│  SLA (Service Level Agreement)     │  Between IT and Business
│  "We promise 99.9% availability"   │
└──────────────┬─────────────────────┘
               │ Supported by
    ┌──────────┴──────────┐
    │                     │
┌───┴──────────────┐ ┌───┴──────────────┐
│  OLA (Operational │ │  UC (Underpinning │
│  Level Agreement)  │ │  Contract)        │
│  Internal teams    │ │  External vendors  │
│  "Network: 99.95%" │ │  "Cloud: 99.99%"  │
└────────────────────┘ └───────────────────┘
```

### OLA Definition Template

| OLA Element | Content |
|-------------|---------|
| Supporting team | Internal team providing the underpinning service |
| Service provided | Specific capability (network, database, application support) |
| Availability commitment | Must be equal to or better than the SLA it supports |
| Response time commitment | Must be faster than the SLA response time |
| Handoff procedures | How work is transferred between teams |
| Escalation path | Internal escalation within the supporting team |
| Reporting | Metrics provided to SLA owner |

### OLA/UC Alignment Matrix

| SLA Requirement | Supporting OLA(s) | Supporting UC(s) | Gap? |
|-----------------|-------------------|-------------------|------|
| 99.9% availability | Network: 99.95%, DB: 99.95%, App: 99.95% | Cloud hosting: 99.99% | No |
| P1 response: 15 min | On-call: 10 min response | Vendor: 15 min response | At risk — no buffer |
| P1 resolution: 4 hours | Internal target: 3 hours | Vendor resolution: 4 hours | At risk — vendor dependency |
| Data backup: daily | DBA team: daily backup at 2 AM | Storage vendor: 99.99% durability | No |

### Gap Analysis Actions

| Gap Type | Risk | Mitigation |
|----------|------|-----------|
| OLA weaker than SLA | SLA breach likely when OLA team is bottleneck | Renegotiate OLA, add redundancy, improve team capability |
| UC weaker than SLA | Vendor dependency creates SLA risk | Negotiate stronger UC, add failover vendor, build buffer |
| No OLA exists | Implicit agreement, no accountability | Formalize OLA with supporting team |
| No UC exists | Vendor obligation unclear | Negotiate formal UC or include in contract renewal |

## Step 4: Monitoring Setup

Implement comprehensive SLA monitoring:

### Monitoring Architecture

| Layer | What to Monitor | Tool Category | Examples |
|-------|----------------|---------------|---------|
| Infrastructure | CPU, memory, disk, network | Infrastructure monitoring | Prometheus, Datadog, Nagios, CloudWatch |
| Application | Response time, error rate, throughput | APM | New Relic, Dynatrace, Datadog APM |
| Synthetic | Simulated user transactions | Synthetic monitoring | Pingdom, Datadog Synthetics, Catchpoint |
| Real user | Actual user experience metrics | RUM | Google Analytics, Datadog RUM, SpeedCurve |
| Service | Aggregate service health | Service monitoring | StatusPage, PagerDuty, OpsGenie |
| SLA dashboard | SLA metric tracking and trending | BI / ITSM reporting | ServiceNow, Power BI, Grafana |

### Alert Configuration

| Alert Type | Condition | Severity | Notification | Action |
|------------|-----------|----------|-------------|--------|
| Warning | Metric approaching threshold (80% of limit) | Low | Slack channel | Monitor closely |
| Threshold breach | Metric exceeds SLA target | Medium | Slack + email to team lead | Investigate immediately |
| SLA at risk | Projected to miss SLA at current trajectory | High | Email to service owner + management | Corrective action plan |
| SLA breached | SLA target missed for the measurement period | Critical | Email to all stakeholders, executive notification | Incident review, credit processing |

### Monitoring Checklist

| Check | Frequency | Automated? |
|-------|-----------|-----------|
| Availability status | Continuous (every 1 min) | Yes — synthetic + real monitoring |
| Response time measurement | Continuous (every request) | Yes — APM instrumentation |
| Error rate calculation | Every 5 minutes (aggregated) | Yes — log aggregation |
| SLA compliance calculation | Hourly (running total for period) | Yes — SLA dashboard |
| Trend analysis | Daily (automated report) | Yes — scheduled report |
| Stakeholder report | Weekly/Monthly | Semi-automated — review before distribution |

## Step 5: Reporting Cadence

Establish regular reporting on service level performance:

### Report Types and Schedule

| Report | Audience | Frequency | Content | Delivery |
|--------|----------|-----------|---------|----------|
| SLA dashboard | Service owners, IT management | Real-time | Current status, trending, alerts | Dashboard (always available) |
| Weekly SLA summary | IT team leads | Weekly | Week's performance, incidents, at-risk items | Email, Slack |
| Monthly SLA report | Business stakeholders, IT management | Monthly | Full metric review, trends, breaches, credits | Email with PDF attachment |
| Quarterly SLA review | Senior management, business sponsors | Quarterly | Strategic review, improvement initiatives, cost | Presentation meeting |
| Annual SLA assessment | CIO, business executives | Annually | Year in review, benchmark comparison, strategy | Executive presentation |

### Monthly SLA Report Template

| Section | Content |
|---------|---------|
| Executive summary | Overall SLA health (Green/Yellow/Red), key highlights |
| Availability report | Target vs actual, trend chart, downtime events |
| Incident summary | Count by severity, MTTR, SLA compliance for response/resolution |
| Request fulfillment | Volume, fulfillment time vs target, backlog |
| Performance metrics | Response time, throughput, error rate vs targets |
| SLA breaches | Each breach with root cause, impact, and corrective action |
| Service credits | Credits issued, cumulative credits for the period |
| Improvement actions | Status of open improvement initiatives |
| Risks and concerns | Items that may impact future SLA compliance |
| Next period outlook | Expected changes, planned maintenance, known risks |

### SLA Scorecard Template

| Service | Metric | Target | Actual | Status | Trend |
|---------|--------|--------|--------|--------|-------|
| Email | Availability | 99.9% | 99.95% | Green | Stable |
| Email | P1 Response | 15 min | 12 min avg | Green | Improving |
| CRM | Availability | 99.9% | 99.82% | Red | Declining |
| CRM | P1 Resolution | 4 hours | 3.5 hours avg | Green | Stable |
| ERP | Availability | 99.5% | 99.7% | Green | Stable |
| ERP | Request fulfillment | 2 days | 1.8 days avg | Green | Improving |

## Step 6: Improvement Planning

Continuously improve service levels:

### SLA Improvement Process

| Step | Activities | Output |
|------|-----------|--------|
| 1. Analyze | Review SLA performance data, identify trends and breaches | Analysis report with root causes |
| 2. Identify | Determine improvement opportunities from breaches, near-misses, and feedback | Prioritized opportunity list |
| 3. Plan | Define improvement initiatives with scope, timeline, resources, and expected outcome | Improvement plan with SMART objectives |
| 4. Implement | Execute improvement actions, track progress | Completed actions, status updates |
| 5. Verify | Measure the impact of improvements on SLA metrics | Before/after comparison |
| 6. Sustain | Embed improvements into standard processes, update documentation | Updated procedures, adjusted targets |

### Service Improvement Register

| ID | Service | Issue | Root Cause | Improvement Action | Owner | Target Date | Status | Expected Impact |
|----|---------|-------|-----------|-------------------|-------|------------|--------|-----------------|
| SIP-001 | CRM | Availability below 99.9% | Database failover not automated | Implement automated DB failover | DBA Team | 2026-05-15 | In Progress | +0.1% availability |
| SIP-002 | Email | P1 response time variance | On-call rotation gaps on weekends | Add weekend on-call engineer | Ops Manager | 2026-04-30 | Planned | -30% response time variance |
| SIP-003 | ERP | Slow request fulfillment | Manual provisioning steps | Automate user provisioning | Platform Team | 2026-06-30 | Planned | -50% fulfillment time |

### Continuous Improvement Techniques

| Technique | Application to SLM | Frequency |
|-----------|-------------------|-----------|
| Pareto analysis | Identify the 20% of issues causing 80% of SLA breaches | Quarterly |
| Trend analysis | Detect gradual degradation before breach | Monthly |
| Root cause analysis | Understand why SLA breaches occurred | Per breach |
| Benchmarking | Compare SLA performance against industry peers | Annually |
| Stakeholder feedback | Survey business users on service satisfaction | Semi-annually |
| Service review meetings | Joint IT-business review of service performance | Quarterly |

## Output Format

Present the service level management deliverable as:

1. **Business Requirements Summary** (criticality assessment, service expectations)
2. **SLA Definitions** (full SLA document or template per service)
3. **OLA/UC Alignment Matrix** (supporting agreements with gap analysis)
4. **Monitoring Architecture** (tools, metrics, alert configuration)
5. **Reporting Plan** (report types, schedule, audience, templates)
6. **SLA Scorecard** (current performance against all targets)
7. **Improvement Plan** (service improvement register with prioritized actions)
8. **Governance Framework** (review cadence, amendment process, escalation matrix)

## Quality Checklist

Before delivering the service level management plan, verify:

- [ ] Business criticality assessment is completed for each service
- [ ] SLA targets are specific, measurable, and achievable
- [ ] Availability targets are expressed as percentages with allowed downtime calculated
- [ ] OLAs and UCs are identified for all supporting services
- [ ] Gap analysis confirms supporting agreements can sustain the SLA
- [ ] Monitoring covers all SLA metrics with appropriate alerting
- [ ] Reporting cadence matches stakeholder needs
- [ ] Service credits or penalty structure is defined and agreed
- [ ] Improvement plan addresses known gaps with assigned ownership

## Edge Cases

- **New service with no performance history**: Set conservative initial SLAs based on vendor commitments and architecture review; plan a 90-day baseline period before finalizing targets
- **Multi-vendor service chains**: Calculate end-to-end SLA as the product of individual component SLAs; e.g., 99.9% * 99.9% * 99.9% = 99.7% end-to-end
- **Global services across time zones**: Define "business hours" per region; specify which timezone governs the SLA; consider follow-the-sun support model
- **SLA targets that cannot be met with current budget**: Present a tiered option to stakeholders; show the cost of each availability level; let the business choose the appropriate trade-off
- **Vendor SLA weaker than internal SLA**: Build redundancy (multi-vendor, multi-region); implement local caching or failover; accept the risk with documented mitigation
- **SLA breach disputes**: Maintain detailed monitoring logs as evidence; define the measurement methodology in the SLA upfront; use an independent monitoring source if disagreements persist

---
name: problem-management
description: >
  Conduct ITIL problem management: known error database maintenance, root cause analysis techniques,
  trend analysis, proactive problem identification, and workaround documentation.
  TRIGGER when: user says /problem-management, "problem management", "root cause analysis", "known error",
  "trend analysis", "recurring incidents", "proactive problem", or "why does this keep happening".
argument-hint: "[problem_description or incident_pattern]"
user-invocable: true
---

# IT Problem Management

You are an expert IT service management practitioner specializing in problem management. When the user asks you to conduct problem management activities, follow this structured process to identify root causes, eliminate recurring incidents, and build organizational knowledge.

## Step 1: Problem Identification

Determine whether a problem record is warranted and capture initial details:

| Field | Description | Example |
|-------|-------------|---------|
| Problem ID | Unique identifier | PRB-2026-0198 |
| Title | Descriptive problem statement | "Recurring database connection pool exhaustion in payment service" |
| Source | How the problem was identified | Trend analysis, major incident, proactive monitoring |
| Related incidents | Linked incident records | INC-0831, INC-0847, INC-0859 |
| Affected service(s) | Business services impacted | Online payment processing |
| Affected CIs | Configuration items involved | payment-api-prod, db-connection-pool |
| Impact | Business impact when this problem manifests | 15-minute service degradation, ~$50K revenue at risk per occurrence |
| Frequency | How often incidents occur | 3 times in last 30 days, increasing trend |
| Priority | Based on impact and frequency | High |
| Owner | Problem manager or assigned investigator | Platform Engineering — M. Chen |

### Problem Identification Sources

| Source | Method | Proactive/Reactive |
|--------|--------|-------------------|
| Incident trend analysis | Group incidents by category, CI, or symptom | Reactive |
| Major incident follow-up | PIR action items flagged as problems | Reactive |
| Monitoring anomalies | Threshold breaches not yet causing incidents | Proactive |
| Capacity analysis | Resource utilization trends approaching limits | Proactive |
| Vendor advisories | Known bugs, end-of-life notices | Proactive |
| Change failure analysis | Patterns in failed or rolled-back changes | Reactive |
| User feedback patterns | Recurring complaints from help desk or surveys | Reactive |

## Step 2: Root Cause Analysis

Apply structured RCA techniques to identify the true root cause:

### RCA Technique Selection

| Technique | Best For | Complexity | Time Required |
|-----------|----------|------------|---------------|
| 5 Whys | Simple, single-cause problems | Low | 30-60 min |
| Fishbone (Ishikawa) | Multi-factor problems needing brainstorming | Medium | 1-2 hours |
| Fault Tree Analysis | Complex systems with multiple failure paths | High | 2-4 hours |
| Kepner-Tregoe | Distinguishing between multiple possible causes | Medium | 1-3 hours |
| Timeline Analysis | Incidents with clear chronological sequence | Low | 1-2 hours |
| Change Analysis | Problems correlated with recent changes | Low | 30-60 min |

### 5 Whys Template

```
Problem Statement: [describe the observable problem]

Why 1: Why did [problem] happen?
  → Because [cause 1]
Why 2: Why did [cause 1] happen?
  → Because [cause 2]
Why 3: Why did [cause 2] happen?
  → Because [cause 3]
Why 4: Why did [cause 3] happen?
  → Because [cause 4]
Why 5: Why did [cause 4] happen?
  → Because [root cause]

Root Cause: [root cause statement]
Contributing Factors: [other factors that enabled the problem]
```

### Fishbone Diagram Categories

| Category | Factors to Investigate |
|----------|----------------------|
| People | Skills, training, staffing, procedures followed |
| Process | Workflow gaps, approval bottlenecks, missing steps |
| Technology | Software bugs, hardware failures, capacity limits |
| Environment | Network, infrastructure, data center, cloud region |
| Data | Data quality, data migration, schema changes |
| External | Vendor issues, third-party dependencies, regulatory changes |

### RCA Documentation Template

```
Root Cause Statement: [clear, specific, testable statement]
Evidence: [logs, metrics, timeline events that support this conclusion]
Confidence Level: [Confirmed / Probable / Suspected]
Contributing Factors:
  1. [factor and how it contributed]
  2. [factor and how it contributed]
Verification: [how was the root cause confirmed — reproduction, code review, vendor confirmation]
```

## Step 3: Known Error Database (KEDB)

Document known errors for rapid incident resolution:

### Known Error Record Template

| Field | Content |
|-------|---------|
| Known Error ID | KE-2026-0052 |
| Problem ID | PRB-2026-0198 (linked) |
| Title | "Connection pool exhaustion under sustained load > 500 TPS" |
| Root cause | Application does not release idle connections; pool grows monotonically |
| Symptoms | HTTP 503 errors, increasing response latency, connection count at maximum |
| Affected CIs | payment-api-prod (versions 3.1.0 - 3.2.4) |
| Workaround | Restart the payment-api service; connections are released on restart |
| Workaround limitations | Causes 30-second service interruption during restart |
| Permanent fix | Implement connection idle timeout and pool recycling (ticket ENG-4521) |
| Fix ETA | Scheduled for Sprint 14 (2026-04-22) |
| Status | Workaround available, permanent fix in progress |
| Last updated | 2026-04-08 |

### KEDB Maintenance

| Activity | Frequency | Owner |
|----------|-----------|-------|
| Review new incidents against KEDB | Every incident triage | Service Desk |
| Update workaround effectiveness | Monthly | Problem Manager |
| Close resolved known errors | On permanent fix deployment | Problem Manager |
| Audit KEDB for stale entries | Quarterly | Problem Management Team |
| Review KEDB search effectiveness | Quarterly | Service Desk Manager |

## Step 4: Trend Analysis

Analyze incident data to identify patterns and emerging problems:

### Trend Analysis Dimensions

| Dimension | What to Look For | Analysis Method |
|-----------|-----------------|-----------------|
| Time patterns | Increasing frequency, day-of-week clusters | Time series chart, moving average |
| Category clusters | Spikes in specific incident categories | Pareto chart (80/20 analysis) |
| CI correlation | Systems with disproportionate incident volume | Heat map by CI and time |
| Change correlation | Incidents spiking after specific changes | Change-incident timeline overlay |
| Seasonal patterns | Recurring issues tied to business cycles | Year-over-year comparison |
| Resolution patterns | Increasing MTTR, repeated workarounds | Resolution method frequency analysis |

### Trend Report Template

| Metric | Previous Period | Current Period | Trend | Action |
|--------|----------------|----------------|-------|--------|
| Total incidents | [count] | [count] | Up/Down/Flat | [action if needed] |
| P1/P2 incidents | [count] | [count] | Up/Down/Flat | [action if needed] |
| Top incident category | [category] ([count]) | [category] ([count]) | — | [investigate if new] |
| Top affected CI | [CI] ([count]) | [CI] ([count]) | — | [problem record if recurring] |
| Average MTTR | [hours] | [hours] | Up/Down/Flat | [action if increasing] |
| Recurring incidents (%) | [%] | [%] | Up/Down/Flat | [target < 10%] |

## Step 5: Proactive Problem Identification

Identify problems before they cause incidents:

### Proactive Techniques

| Technique | Data Source | Detection Method | Action |
|-----------|-----------|------------------|--------|
| Capacity monitoring | Infrastructure metrics | Utilization > 70% threshold | Capacity review, scaling plan |
| End-of-life tracking | Vendor lifecycle dates | Automated calendar alerts | Upgrade/migration planning |
| Vulnerability scanning | Security tools | CVE feeds, scan results | Patching schedule |
| Performance baselining | APM data | Deviation from baseline > 2 std dev | Investigation |
| Dependency mapping | CMDB, architecture docs | Single points of failure identified | Redundancy planning |
| Post-change monitoring | Deployment metrics | Error rate increase > 5% post-deploy | Rollback or hotfix |

### Proactive Problem Register

| ID | Source | Description | Risk Level | Mitigation | Owner | Deadline |
|----|--------|-------------|-----------|-----------|-------|----------|
| PP-001 | Capacity | Database disk 78% full, growing 2%/week | High | Expand storage, archive old data | DBA Team | 2026-04-20 |
| PP-002 | EOL | Load balancer firmware end-of-support June 2026 | Medium | Upgrade to supported version | Network Team | 2026-05-31 |
| PP-003 | Vulnerability | CVE-2026-XXXX in TLS library, unpatched | High | Apply patch in next maintenance window | Security Team | 2026-04-15 |

## Step 6: Resolution and Closure

Drive problems to permanent resolution:

### Resolution Options

| Option | When to Use | Acceptance Criteria |
|--------|------------|---------------------|
| Permanent fix | Root cause is understood and fixable | Fix deployed, incidents eliminated, monitoring confirms |
| Structural improvement | Root cause is architectural | Architecture change completed, tested, monitored |
| Risk acceptance | Fix cost exceeds impact; workaround is sufficient | Documented risk acceptance with management sign-off |
| Transfer | Problem is in vendor domain | Vendor acknowledges and commits to fix timeline |
| Closure (resolved) | Root cause eliminated, no recurrence for 30 days | 30-day verification period passed |

### Problem Closure Checklist

| Item | Status |
|------|--------|
| Root cause identified and documented | Done / In Progress / N/A |
| Permanent fix implemented | Done / In Progress / Risk Accepted |
| Known error record updated or closed | Done |
| Related incidents linked | Done |
| No recurrence for 30 days post-fix | Verified / Pending |
| CMDB updated if configuration changed | Done / N/A |
| Knowledge base updated | Done |
| Stakeholders notified of resolution | Done |

## Output Format

Present the problem management deliverable as:

1. **Problem Summary** (ID, title, source, priority, impact, related incidents)
2. **Root Cause Analysis** (technique used, findings, evidence, confidence level)
3. **Known Error Record** (if applicable — symptoms, workaround, fix status)
4. **Trend Analysis** (patterns identified, supporting data, emerging risks)
5. **Proactive Findings** (potential problems identified, risk assessment)
6. **Resolution Plan** (permanent fix, timeline, owner, success criteria)
7. **Workaround Documentation** (step-by-step for service desk use)
8. **Closure Report** (verification, recurrence check, lessons learned)

## Quality Checklist

Before closing the problem or delivering the analysis, verify:

- [ ] Root cause is identified with evidence (not just symptoms)
- [ ] RCA technique is appropriate for the problem complexity
- [ ] Known error record is complete with workaround and fix plan
- [ ] All related incidents are linked to the problem record
- [ ] Trend analysis covers at least 3 months of data
- [ ] Proactive findings have risk levels and owners assigned
- [ ] Permanent fix has a defined timeline and success criteria
- [ ] Workaround is documented in a format the service desk can follow
- [ ] 30-day verification period is planned before final closure

## Edge Cases

- **Root cause cannot be determined**: Document the investigation thoroughly; classify as "undetermined" with all eliminated causes listed; set a recurrence trigger to reopen
- **Multiple root causes**: Document each separately; prioritize by impact; create linked sub-problems if fixes are owned by different teams
- **Vendor refuses to fix**: Document risk acceptance; implement monitoring for the known error; escalate through account management; evaluate alternative vendors
- **Problem spans organizational boundaries**: Assign a single problem coordinator; create a joint investigation team; use a shared evidence repository
- **Legacy system with no maintainer**: Escalate to management for resource allocation; document the risk of unresolved problems; consider system replacement as the permanent fix
- **Workaround causes other issues**: Document the side effects; set a deadline for the permanent fix; monitor the workaround's secondary impact

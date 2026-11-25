---
name: workflow-automation-review
description: >
  Review automated workflows for reliability, error handling, monitoring gaps,
  and optimization opportunities. Assess automation maturity and recommend
  improvements.
  TRIGGER when: user says /workflow-automation-review, "automation review",
  "workflow review", "review automation", or "automation audit".
argument-hint: "[workflow or automation name]"
user-invocable: true
---

# Workflow Automation Review

You are an automation engineer reviewing an automated workflow for reliability, maintainability, and operational readiness. Produce a structured assessment with prioritized recommendations.

## Process

### Step 1: Understand the Workflow

Document the automation under review:

| Attribute | Detail |
|-----------|--------|
| **Workflow name** | Identifier in the automation platform |
| **Purpose** | Business process being automated |
| **Platform** | Tool or framework (Zapier, Airflow, n8n, Step Functions, custom) |
| **Trigger** | What initiates the workflow (schedule, event, API call, manual) |
| **Frequency** | How often it runs (real-time, hourly, daily, on-demand) |
| **Owner** | Team and individual responsible |
| **Downstream consumers** | Who or what depends on this workflow's output |
| **Data sensitivity** | PII, financial, internal-only, public |

### Step 2: Architecture Review

Map the workflow's structure:

| Component | Description | Dependencies | Failure Impact |
|-----------|-------------|-------------|---------------|
| Step 1: *name* | What it does | APIs, DBs, services | What breaks if this fails |
| Step 2: *name* | ... | ... | ... |
| ... | ... | ... | ... |

Identify:
- Sequential vs. parallel execution paths
- Conditional branching logic and decision points
- Data transformation and mapping between steps
- External service integrations and their SLAs

### Step 3: Reliability Assessment

Evaluate each dimension:

| Dimension | Rating (1-5) | Evidence | Risk |
|-----------|-------------|----------|------|
| **Error handling** | ... | Are failures caught, logged, and handled? | ... |
| **Retry logic** | ... | Are transient failures retried with backoff? | ... |
| **Idempotency** | ... | Can the workflow safely re-run without side effects? | ... |
| **Timeout handling** | ... | Are there timeouts on external calls? | ... |
| **Data validation** | ... | Are inputs and intermediate results validated? | ... |
| **Monitoring** | ... | Are runs tracked, failures alerted, metrics collected? | ... |
| **Logging** | ... | Are execution details logged for debugging? | ... |
| **Rollback** | ... | Can partial executions be undone? | ... |
| **Concurrency** | ... | Are race conditions and duplicate runs handled? | ... |
| **Secrets management** | ... | Are credentials stored securely, rotated? | ... |

### Step 4: Maturity Assessment

Rate the workflow's automation maturity:

| Level | Name | Criteria |
|-------|------|----------|
| 1 | **Manual** | Process is documented but executed by hand |
| 2 | **Scripted** | Automated execution but no error handling or monitoring |
| 3 | **Reliable** | Error handling, retries, and basic alerting in place |
| 4 | **Observable** | Full monitoring, logging, dashboards, and SLA tracking |
| 5 | **Self-healing** | Automatic recovery, anomaly detection, and adaptive behavior |

### Step 5: Optimization Opportunities

Identify improvements:

| Opportunity | Current State | Proposed Change | Effort | Impact |
|-------------|--------------|----------------|--------|--------|
| *description* | How it works now | How it should work | S/M/L | Low/Med/High |

## Output Format

### 1. Workflow Summary

Overview table and text-based flow diagram.

### 2. Architecture Map

Step-by-step component table with dependencies and failure impacts.

### 3. Reliability Scorecard

| Dimension | Rating | Status |
|-----------|--------|--------|
| Error handling | 3/5 | Needs improvement |
| ... | ... | ... |
| **Overall** | **X.X/5** | ... |

### 4. Maturity Rating

Current level (1-5), justification, and target level with gap analysis.

### 5. Findings

For each finding:

| Attribute | Detail |
|-----------|--------|
| **ID** | F-NNN |
| **Severity** | Critical / High / Medium / Low |
| **Category** | Reliability / Security / Performance / Maintainability |
| **Description** | What the issue is |
| **Risk** | What could go wrong |
| **Recommendation** | Specific fix |
| **Effort** | Small / Medium / Large |

### 6. Improvement Roadmap

| Priority | Finding(s) | Action | Owner | Timeline |
|----------|-----------|--------|-------|----------|
| P1 | F-001 | ... | ... | This sprint |
| P2 | F-002, F-003 | ... | ... | Next sprint |
| P3 | F-004 | ... | ... | Next quarter |

### 7. Monitoring Recommendations

| Metric | Source | Alert Condition | Severity |
|--------|--------|----------------|----------|
| Run success rate | Platform logs | < 95% over 1 hour | Warning |
| Run duration (p99) | Platform metrics | > 2x baseline | Warning |
| Failure count | Error tracking | > 3 in 15 minutes | Critical |
| Data freshness | Output timestamp | Stale > 2x expected interval | High |

## Quality Checklist

- Every workflow step must be accounted for in the architecture map
- Error handling must be evaluated for each external integration, not just top-level
- Idempotency assessment must describe what happens if the workflow runs twice with the same input
- Recommendations must include effort estimates — not just "fix it"
- Monitoring recommendations must cover both availability and data quality
- Security review must cover credential storage, data exposure, and access control
- Consider the workflow in the context of its upstream and downstream dependencies

## Edge Cases

- **Event-driven workflows**: Assess message ordering, deduplication, and dead-letter handling
- **Scheduled workflows**: Evaluate overlap protection, clock drift, and DST handling
- **Human-in-the-loop workflows**: Review approval step timeouts and reassignment logic
- **Cross-platform workflows**: Assess integration reliability and version compatibility
- **High-volume workflows**: Evaluate throttling, backpressure, and resource contention
- **Workflows with side effects**: Pay special attention to rollback and compensation logic
- **Legacy workflows**: Assess documentation completeness and bus factor risk

---
name: agent-runbook
description: >
  Create operational runbooks for AI agent systems — monitoring, failure modes,
  fallback procedures, human escalation triggers, and recovery steps. Document
  agent behavior expectations and operational guardrails.
  TRIGGER when: user says /agent-runbook, "agent runbook", "AI agent ops",
  "agent operations", or "agent monitoring".
argument-hint: "[agent or system name]"
user-invocable: true
---

# Agent Runbook

You are an AI operations engineer. Produce a comprehensive operational runbook for an AI agent system that covers normal operations, failure modes, escalation procedures, and recovery playbooks. The runbook should be usable by on-call engineers who may not be AI specialists.

## Process

### Step 1: Agent Profile

Document the agent's identity and operational context:

| Attribute | Detail |
|-----------|--------|
| **Agent name** | Identifier used in logs and monitoring |
| **Purpose** | What task or workflow the agent handles |
| **Model(s)** | Underlying LLM(s) and versions |
| **Tools/APIs** | External systems the agent can invoke |
| **Data access** | What data the agent reads and writes |
| **Autonomy level** | Fully autonomous / Human-in-the-loop / Supervised |
| **SLA** | Expected response time, uptime, throughput |
| **Owner** | Team and individual responsible |
| **Escalation contact** | On-call rotation or Slack channel |

### Step 2: Normal Operations

Define what "healthy" looks like:

| Metric | Expected Range | Alert Threshold | Critical Threshold |
|--------|---------------|-----------------|-------------------|
| Response latency (p50/p99) | ... | ... | ... |
| Success rate | ... | ... | ... |
| Token usage per request | ... | ... | ... |
| Tool call failure rate | ... | ... | ... |
| Human escalation rate | ... | ... | ... |
| Cost per hour/day | ... | ... | ... |
| Queue depth (if async) | ... | ... | ... |

### Step 3: Failure Mode Catalog

Enumerate known failure modes:

| ID | Failure Mode | Symptoms | Likelihood | Impact | Detection Method |
|----|-------------|----------|-----------|--------|-----------------|
| F-001 | Model hallucination | Confident but factually wrong output | Medium | High | Fact-check sampling, user reports |
| F-002 | Tool call loop | Agent repeatedly calls same tool without progress | Low | Medium | Loop counter, timeout monitor |
| F-003 | Context window overflow | Truncated context, degraded responses | Medium | Medium | Token count monitoring |
| F-004 | API rate limiting | 429 errors from downstream services | Medium | High | Error rate spike |
| F-005 | Prompt injection | Agent executes unintended instructions | Low | Critical | Input/output anomaly detection |
| F-006 | Model provider outage | Timeout or 5xx from LLM API | Low | Critical | Health check, error rate |
| F-007 | Cost runaway | Unexpected spike in token or API costs | Low | High | Cost anomaly alerts |

### Step 4: Escalation Matrix

| Severity | Condition | Response Time | Action | Escalate To |
|----------|-----------|--------------|--------|-------------|
| **SEV-1** | Agent producing harmful or unsafe output | Immediate | Kill switch, notify leadership | AI Safety + Engineering Lead |
| **SEV-2** | Agent fully down, SLA breached | 15 minutes | Activate fallback, page on-call | On-call engineer |
| **SEV-3** | Degraded performance, elevated error rate | 1 hour | Investigate, consider fallback | On-call engineer |
| **SEV-4** | Minor quality regression, cosmetic issues | Next business day | Log ticket, monitor trend | Agent owner |

### Step 5: Recovery Playbooks

For each failure mode, document a step-by-step recovery procedure:

1. **Confirm** the issue (check dashboards, logs, sample outputs)
2. **Contain** the blast radius (pause agent, switch to fallback, rate-limit)
3. **Diagnose** the root cause (model change? data drift? upstream failure?)
4. **Fix** or workaround (rollback prompt, switch model, fix tool, clear queue)
5. **Verify** recovery (run test cases, check metrics return to normal)
6. **Document** the incident (timeline, root cause, action items)

## Output Format

### 1. Agent Overview

Summary table with agent profile attributes.

### 2. Architecture Diagram

Text-based diagram showing the agent, its tools, data sources, and human touchpoints.

### 3. Health Monitoring

Table of metrics, thresholds, and alerting configuration.

### 4. Failure Mode Catalog

Table of all known failure modes with detection and response.

### 5. Escalation Matrix

Severity-based escalation table with contacts and response times.

### 6. Recovery Playbooks

Step-by-step runbook for each SEV-1 and SEV-2 failure mode.

### 7. Guardrails & Safety Controls

| Control | Description | Implementation |
|---------|-------------|---------------|
| Input validation | Filter/sanitize user inputs before agent | Regex, classifier, allowlist |
| Output validation | Check agent output before delivery | Content filter, schema validation |
| Kill switch | Immediately halt agent processing | Feature flag, circuit breaker |
| Rate limiting | Cap requests per user/minute | API gateway, application-level |
| Cost ceiling | Max daily spend on LLM API calls | Budget alert + auto-pause |
| Audit logging | Log all inputs, outputs, tool calls | Structured logging pipeline |

### 8. Maintenance Schedule

| Task | Frequency | Owner | Procedure |
|------|-----------|-------|-----------|
| Prompt review | Monthly | Agent owner | Review prompt against latest model behavior |
| Model version update | As released | AI team | Test in staging, compare metrics, promote |
| Tool dependency audit | Quarterly | Engineering | Check API versions, deprecation notices |
| Runbook review | Quarterly | On-call team | Validate playbooks are current |
| Cost review | Monthly | Finance + AI team | Compare actual vs. budget |

## Quality Checklist

- Every failure mode must have a documented detection method and recovery procedure
- Escalation contacts must be specific people or rotations, not generic team names
- The kill switch procedure must be testable and tested at least quarterly
- Metrics thresholds must be based on baseline data, not guesses
- Recovery playbooks must be executable by an on-call engineer unfamiliar with the agent
- Guardrails must cover both input and output validation
- The runbook must include rollback procedures for prompt and model changes

## Edge Cases

- **Multi-agent systems**: Document inter-agent dependencies and cascading failure risks
- **Agents with memory/state**: Include procedures for corrupted state and memory reset
- **Agents accessing production databases**: Extra guardrails for write operations and data mutation
- **Customer-facing agents**: Include brand safety checks and human takeover procedures
- **Agents with long-running tasks**: Document timeout handling and partial-completion recovery
- **Agents using multiple LLM providers**: Failover routing and provider-specific quirks
- **New agent launch**: Include a graduated rollout plan with traffic ramp and rollback criteria

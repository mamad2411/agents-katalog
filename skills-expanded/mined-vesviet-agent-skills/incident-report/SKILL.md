---
name: incident-report
description: Capture, structure, and communicate an incident from triage through resolution and prevention. Use when a production failure, degradation, or security event requires a formal timeline, impact assessment, root cause analysis, and follow-up action items.
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, run_tests, run_linter, run_build, execute_command]
---

# Incident Report

Use this skill when a production incident, degradation, or security event requires structured documentation and handoff.

## When to Use

- a service failure, degradation, or data issue is affecting users or downstream systems
- an on-call or SRE investigation needs to be handed off to another team
- a postmortem or retrospective requires evidence-backed findings
- incident action items need owners and timelines to prevent recurrence
- a security event requires formal communications

## Core Rules

- do not close an incident without explicit action items and owners
- timeline must be built from evidence (logs, metrics, alerts, commits) — not reconstructed from memory alone
- calculate and record quantitative duration metrics in seconds: MTTD, MTTM, and MTTR
- record Multi-Window Multi-Burn-Rate (MWMBR) impact: `burn_rate_peak`, `budget_consumed_percentage`, and `slo_breached`
- capture OpenTelemetry distributed trace context: W3C `root_trace_id` (32-hex) and `culprit_span_id` (16-hex)
- root cause must be distinguished from contributing factors via 5 Whys and standardized failure taxonomy
- never include plaintext secrets, credentials, or PII in incident artifacts
- use `contracts/schemas/incident-report.json` for structured handoff to Agent Coordinator or SRE
- classify AI/LLM incidents by taxonomy: hallucination, tool-call corruption, or prompt injection
- require replayable agent audit trail as postmortem evidence: model, temperature, prompts, tool inputs/outputs
- preventative action items must specify `action_item_id`, `task`, `owner_role`, `priority`, `target_completion_date`, and `verification_mechanism` (14-day SLA for P0/P1)

## Suggested Process

### 1. Triage And Scope
Answer immediately: what is broken or degraded, which services are affected, severity, and incident owner:
- **P0 (Critical):** total outage or data loss affecting production users
- **P1 (High):** major feature unavailable or significant performance degradation
- **P2 (Medium):** partial degradation with workaround available
- **P3 (Low):** minor issue with no immediate user impact

### 2. Build The Timeline
Reconstruct events chronologically using evidence: first signal, onset time, investigation steps, mitigation applied, and resolution time. Measure MTTD, MTTM, and MTTR in seconds.

### 3. Assess Impact & Error Budget
Document affected services, user count, downtime minutes, W3C trace context (`root_trace_id`, `culprit_span_id`), peak burn rate multiplier, and percentage of error budget consumed.

### 4. Root Cause Analysis (5 Whys)
Distinguish trigger, root cause, and contributing factors using the 5 Whys technique. Categorize into standardized failure taxonomies (software defect, configuration drift, infrastructure, dependency, capacity, AI model degradation).

### 5. Action Items And Prevention
Define preventative actions with `action_item_id`, `task`, `owner_role`, `priority`, `target_completion_date` (YYYY-MM-DD), and `verification_mechanism` (automated regression test, chaos drill, canary rule).

## Output Format

```markdown
# <Service> — Incident Report
## Summary
- Severity: | Status: | Duration: <detection> → <mitigation> → <resolution>
- Metrics (seconds): MTTD: <sec> | MTTM: <sec> | MTTR: <sec>
- Error Budget Impact: Peak Burn: <x> | Budget Consumed: <% > | SLO Breached: <true/false>
- Trace Context: Root Trace ID: <hex32> | Culprit Span ID: <hex16>
## Timeline
| Time (UTC) | Event |
|------------|-------|
| | First signal / Detection |
| | Mitigation applied |
| | Resolution confirmed |
## Root Cause Analysis (5 Whys)
- Category: <taxonomy>
- 1. Why: ... 2. Why: ... 3. Why: ... 4. Why: ... 5. Why: ...
## Action Items
| ID | Task | Owner | Priority | Target Date | Verification |
|----|------|-------|----------|-------------|--------------|
| ACT-01 | | SRE | P1 | YYYY-MM-DD | Chaos drill |
```

Emit `contracts/schemas/incident-report.json` for machine handoff to Agent Coordinator or SRE.

## Checklist

- [ ] incident severity assigned and timeline built from evidence
- [ ] quantitative metrics recorded: MTTD, MTTM, and MTTR in integer seconds
- [ ] error budget impact documented: peak burn rate, budget consumed %, SLO breached
- [ ] OpenTelemetry trace context recorded: root_trace_id and culprit_span_id
- [ ] root cause separated from trigger via 5 Whys and standardized failure taxonomy
- [ ] action items have ID, owner role, priority, target date, and verification mechanism
- [ ] secrets and PII excluded from all artifacts
- [ ] incident-report.json emitted adhering to JSON Schema Draft 2020-12
- [ ] AI/LLM-specific taxonomy applied if AI system in scope with replayable audit trail attached

## Failure Modes

- **Symptom before change**: a fix is applied before symptom is captured. **Mitigation:** capture symptom and recent changes first.
- **Multiple layers changed**: build, config, and code modified simultaneously. **Mitigation:** isolate one failure layer at a time.
- **Postmortem skipped**: incident closed without RCA. **Mitigation:** require `incident-report.json` within 72 hours.
- **Customer/budget impact not captured**: closed without recording impact. **Mitigation:** capture MTTD/MTTR, burn rate, and SLO impact.

## Output Contracts

When responding to, documenting, or completing the post-mortem of an operational incident, emit:

- **`contracts/schemas/incident-report.json`** — Emitted to provide structured timeline, metrics, error budget impact, trace context, 5 Whys RCA, and preventative action items. Set `produced_by_role: sre`.

## Security Guardrails (OWASP ASI)

- **ASI01 Goal Hijack**: cross-check timeline and root cause against live evidence (logs, traces, metrics).
- **ASI06 Memory & Context Poisoning**: validate prior incident memory against current evidence before drawing parallels.
- **ASI07 Inter-Agent Communication**: emit structured contracts for consumer validation across SRE, security, and dev roles.
- **ASI08 Cascading Failures**: surface downstream dependencies explicitly in remediation plans.
- **ASI09 Human-Agent Trust Exploitation**: surface remaining unknowns honestly; do not claim root cause without evidence.

## Related Skills

- **troubleshoot-service**: Diagnose and contain active failure
- **orchestrate-chaos-experiment**: Verify preventative remediation and resilience via chaos drills
- **add-telemetry-instrumentation**: Address detection gaps identified in action items
- **debug-runtime-platform**: Isolate runtime container and host-level issues
- **review-service**: Broader service health check after resolution

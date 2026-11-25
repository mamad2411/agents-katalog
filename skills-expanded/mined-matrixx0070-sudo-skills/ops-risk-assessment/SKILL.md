---
name: ops-risk-assessment
version: 1.0.0
description: Identify, score, and mitigate operational risks in a structured register with owners, triggers, and residual scores.
author: matrixx0070
tags: [operations, risk, mitigation, register, resilience, heat-map]
capabilities: []
---

# Risk Assessment

## When to use
Use this to surface what could go wrong in an operation, initiative, or system, and to decide which risks warrant action, ownership, and monitoring before they become incidents.

**Not for:** compliance control tracking (use ops-compliance-tracking), or post-incident analysis of something that already failed (that's a retrospective). This is forward-looking on risks not yet realized.

## Method
1. **Define scope.** State the system, project, or process under assessment and the time horizon.
2. **Identify risks.** Brainstorm across categories: operational, technical, security, financial, people, vendor, compliance, external. Write each as cause -> event -> consequence.
3. **Assess each risk.** Rate likelihood (1-5) and impact (1-5); compute score (L x I) and place it in a heat-map band (low/medium/high/critical).
4. **Choose a response.** Per risk select avoid, mitigate, transfer, or accept, with rationale. *Decision:* low L x low I is usually accept-and-monitor; don't over-engineer trivial risks.
5. **Define mitigations.** For mitigated risks, specify concrete actions, owner, due date, and the residual score after action.
6. **Add detection.** Name the leading indicator or trigger that signals the risk is materializing.
7. **Prioritize.** Sort by inherent score; escalate anything critical.

## Example
**Scope:** payments service, next 2 quarters. **Risk:** single on-call engineer knows the reconciliation job (cause) -> they leave or are unavailable during a failure (event) -> reconciliation stalls, funds mismatch (consequence). L=3, I=5, score 15 (high). **Response:** mitigate — write a runbook and cross-train a second engineer, owner = eng lead, due in 3 weeks, residual score 6. **Trigger:** any reconciliation run requiring manual intervention.

## Pitfalls
- **Vague risk statements.** "Security risk" is unactionable; the cause -> event -> consequence form forces specificity and a mitigation target.
- **Scoring theater.** Numbers assigned to look rigorous but never revisited; recompute residual after mitigation and review on cadence.
- **No detection trigger.** A mitigation with no leading indicator means you learn the risk hit when it's already an incident.
- **Ignoring residual risk.** Mitigation rarely reaches zero; record and accept the remainder explicitly.

## Output format
```
Scope:      system/project | horizon
Register:   ID | risk (cause/event/consequence) | category | L | I | score
            | response | mitigation | owner | due | residual | trigger
Heat map:   counts per band (low/med/high/critical)
Top risks:  critical/high items called out
Monitoring: indicators | review cadence
```

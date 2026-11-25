---
name: chaos-engineering
description: >
  Design chaos engineering experiments — hypothesis formation, blast radius control,
  steady-state definition, experiment design, abort conditions, and findings documentation.
  TRIGGER when: user says /chaos-engineering, wants to test system resilience,
  or asks about fault injection and failure testing.
argument-hint: "[system or service to test]"
user-invocable: true
---

# Chaos Engineering

You are an SRE specialist. Design controlled chaos experiments to verify system resilience and uncover hidden failures.

## Process

### Step 1: Define Steady State
Identify measurable indicators of normal system behavior:
| Indicator | Baseline | Acceptable Range |
|-----------|----------|-----------------|
| Request success rate | 99.9% | > 99.5% |
| p95 latency | 200ms | < 500ms |
| Error rate | 0.1% | < 1% |
| Throughput | 1000 rps | > 800 rps |

### Step 2: Form Hypothesis
"We believe that when [fault condition], the system will [expected behavior] because [resilience mechanism]."

### Step 3: Design Experiment
| Element | Details |
|---------|---------|
| Fault type | Network partition, instance failure, latency injection, disk full, CPU saturation |
| Blast radius | Start small — single instance, single AZ, then expand |
| Duration | 1-5 minutes for initial experiments |
| Target | Non-production first, then production during low-traffic |
| Monitoring | Real-time dashboards showing steady-state metrics |
| Abort conditions | Any metric beyond acceptable range → automatic rollback |

### Step 4: Execute with Safety
- [ ] Notify on-call and stakeholders
- [ ] Confirm monitoring dashboards are live
- [ ] Verify abort mechanism works before starting
- [ ] Start with smallest blast radius
- [ ] Have rollback runbook ready
- [ ] Run during business hours with full team availability

### Step 5: Analyze Results
| Outcome | Meaning | Action |
|---------|---------|--------|
| Hypothesis confirmed | System resilient as expected | Document, expand scope |
| Hypothesis disproven | Hidden weakness found | File bug, prioritize fix, retest |
| Inconclusive | Metrics ambiguous | Improve observability, redesign experiment |

### Step 6: Document and Share
```markdown
## Experiment: [Name]
- Hypothesis: [statement]
- Fault injected: [type, scope, duration]
- Result: [confirmed/disproven/inconclusive]
- Findings: [what we learned]
- Action items: [fixes, follow-ups]
```

## Quality Checklist
- [ ] Steady state clearly defined with metrics
- [ ] Hypothesis is falsifiable
- [ ] Blast radius starts minimal
- [ ] Abort conditions automated
- [ ] Team and stakeholders notified
- [ ] Findings documented and shared

## Edge Cases
- Never run chaos experiments during incident recovery or maintenance windows
- For stateful systems, verify data integrity after experiments
- If no observability exists, improve monitoring before running chaos
- For regulated systems, get compliance approval before production experiments

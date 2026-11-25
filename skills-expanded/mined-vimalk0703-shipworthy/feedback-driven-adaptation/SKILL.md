---
name: feedback-driven-adaptation
description: Use when guardrail strictness needs to adjust based on user signals, project maturity changes, or accumulated session data. Moves guardrails from static rules to dynamic control systems.
invoke_when: Use when a user expresses frustration with guardrail strictness, when a project has matured beyond its current tier, when guardrail violations trend upward or downward, or when session retrospectives reveal misaligned enforcement levels.
---

# Feedback-Driven Adaptation

## Core Rule

**Static guardrails do not scale. Adapt enforcement based on evidence — user signals, project trajectory, and violation patterns — not assumptions.**

A guardrail system that never adjusts is either too strict (slowing productive teams) or too lenient (missing real risks). The right level of enforcement changes as the project, team, and risk profile evolve.

## Adaptation Signals

### 1. User Signals (Explicit Feedback)

Direct signals from user behavior and statements:

| Signal | Interpretation | Adjustment |
|--------|---------------|------------|
| User says "stop checking X" or "skip this" | Guardrail perceived as low-value for this context | Downgrade to advisory (warn, don't block) for this session |
| User repeatedly fixes the same guardrail finding | They understand the rule — it's working | Keep enforcing; the pattern needs structural fix, not softer rules |
| User overrides a guardrail and the code ships successfully | Override was justified | Log the override pattern; consider adjusting threshold |
| User asks "why did this block?" | Guardrail lacks transparency | Improve explanation; do not reduce strictness |
| User says "be stricter" or "catch more of these" | Under-enforcement | Increase detection sensitivity and/or escalate from advisory to blocking |

### 2. Project Trajectory Signals

Automated signals from the project's evolution:

| Signal | Detection | Adjustment |
|--------|----------|------------|
| Source file count crosses tier threshold | Count `**/*.{ts,py,go,rs,java}` excluding tests/generated | Graduate quality gate level (see `quality-gates` skill) |
| First deployment detected | CI/CD config added, deploy script present | Graduate from Level 0 to Level 1 minimum |
| Test coverage consistently above threshold | Coverage reports over last 5 sessions | Allow advisory-only mode for test-related guardrails |
| Test coverage declining | Coverage delta negative over 3+ sessions | Escalate test guardrails from advisory to blocking |
| New compliance-sensitive code added | Auth, payment, PII-handling code detected | Auto-activate compliance-awareness and pii-detection skills |
| External API integrations added | New HTTP clients, webhook handlers | Auto-activate vendor-risk-assessment and adaptive-security |

### 3. Violation Pattern Signals

Trends in guardrail activations:

| Pattern | Meaning | Response |
|---------|---------|----------|
| Same violation type recurring across sessions | Structural issue, not a one-off mistake | Suggest architectural fix; escalate if unfixed after 3 occurrences |
| Violation rate dropping over time | Team is learning; guardrails are working | Maintain current level — this is success, not a signal to relax |
| Sudden spike in violations | New contributor, new feature area, or regression | Increase enforcement temporarily; investigate root cause |
| Zero violations for extended period | Either clean code or guardrails aren't running | Verify guardrails are active; if genuinely clean, maintain level |
| High override rate on a specific guardrail | Guardrail may be miscalibrated | Review threshold; adjust or document why current level is correct |

## Tier Graduation Protocol

When signals indicate a tier change, follow this protocol:

### Upgrading (More Strict)

```
1. Detect graduation trigger (file count, deployment, compliance code)
2. Announce to user: "Your project has grown — activating [Level N] quality gates"
3. First session at new level: advisory only (warn, don't block)
4. Second session: enforce normally
5. Log the graduation event to guardrail audit log
```

### Downgrading (Less Strict)

Downgrading is rare and requires explicit justification:

```
1. User explicitly requests reduced strictness for specific guardrail
2. Verify the request is scoped (not "turn off all guardrails")
3. Downgrade specific guardrail to advisory for this project
4. Log the downgrade event with user's stated reason
5. Review in 5 sessions — if violations increase, re-escalate with explanation
```

**Never downgrade these guardrails regardless of user request:**
- Secret/credential detection (always block)
- Destructive command detection (always block)
- PII in production logs (always block)

## Adaptation Rules

### Rule 1: Adapt Scope, Not Principle

Adjust *which checks run* and *how they report*, not *whether the principle matters*.

```
CORRECT:  "Downgrading structured-logging check to advisory for this CLI project"
           (The principle still applies — structured logging is better — but the enforcement is softer)

WRONG:    "Disabling security checks because the user asked for speed"
           (The principle is non-negotiable; only the reporting mode changes)
```

### Rule 2: Explain Every Adjustment

When strictness changes, tell the user why:

```
"I'm activating stricter dependency checks because you added a payment processing
library. Supply chain security is critical for financial code."
```

Never silently change enforcement levels.

### Rule 3: Log Every Adaptation

Every strictness change is a guardrail audit event:

```typescript
{
  guardrailLayer: 'adaptive',
  guardrailName: 'feedback-driven-adaptation',
  severity: 'info',
  description: 'Graduated quality gates from Level 1 to Level 2 — project reached 15 source files',
  action: 'allowed',
  resolution: 'automatic graduation based on file count threshold'
}
```

### Rule 4: Revert on Negative Signal

If a downgrade leads to increased violations or a shipped bug:

```
1. Detect negative signal (new violations in the relaxed area)
2. Re-escalate to previous strictness level
3. Inform user: "Re-enabling [guardrail] — saw [specific issue] after it was relaxed"
4. Log the re-escalation
```

## Session-Level Adaptation

Within a single session, adapt based on the task:

| Task Type | Adaptation |
|-----------|-----------|
| Quick bug fix | Reduce to essential guardrails only (security + tests pass) |
| New feature | Full guardrail suite active |
| Refactoring | Emphasize architectural and test guardrails |
| Incident response | Reduce non-security guardrails; maximize speed to fix |
| Code review | All guardrails in advisory mode (inform, don't block) |

## Rationalization Pressure Test

| Excuse | Counter |
|--------|---------|
| "The user seems annoyed by the guardrails" | Annoyance is a signal to explain better, not to reduce protection. Improve transparency, not strictness |
| "This project is small, it doesn't need strict rules" | The graduated levels already handle this — Level 0 has only 2 checks. Trust the tier system, don't bypass it |
| "The guardrail keeps firing on false positives" | High false-positive rate means the threshold needs calibration, not removal. Adjust the trigger, keep the guardrail |
| "Nobody has complained about this before" | Absence of complaints is not evidence of safety. Verify guardrails are running, don't assume silence means success |
| "We should relax rules to move faster" | Relaxing security guardrails to move faster is how breaches happen. Adapt scope, not principle |
| "The override rate is high, so the guardrail is wrong" | High override rate may mean the guardrail is miscalibrated OR the team needs training. Investigate, don't disable |

## Code Review Checklist

- [ ] Adaptation triggers are evidence-based (not feelings or assumptions)
- [ ] Security guardrails are never downgraded below advisory level
- [ ] Every adaptation is logged with reason and timestamp
- [ ] User is informed of every strictness change
- [ ] Downgrade requests are scoped to specific guardrails, not blanket reduction
- [ ] Re-escalation path exists for every downgrade

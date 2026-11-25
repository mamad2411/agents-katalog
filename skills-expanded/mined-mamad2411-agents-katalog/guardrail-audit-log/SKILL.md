---
name: guardrail-audit-log
description: Use when building systems that need centralized tracking of guardrail violations, security warnings, and compliance events. Ensures every block, warning, and override is logged immutably for governance and incident review.
invoke_when: Use when implementing logging infrastructure, setting up observability, building compliance dashboards, or when any guardrail (security, quality, ethical, adaptive) needs its violations tracked centrally.
---

# Guardrail Audit Log

## Core Rule

**Every guardrail violation, warning, block, and override must be logged to a centralized, immutable audit trail.** If you cannot prove a guardrail fired, you cannot prove the system is protected.

## Why Centralized Audit Logging

| Without Audit Logging | With Audit Logging |
|----------------------|-------------------|
| "We think the secret scanner ran" | Timestamped record of every scan, every finding, every resolution |
| Compliance auditor asks for evidence — you scramble | Export the log, filter by date range, done |
| A guardrail was silently bypassed — nobody noticed | Override logged with who, why, and approval chain |
| Incident response: "When did this start?" — unknown | Query the log: first violation timestamp, escalation history |

## Guardrail Event Schema

Every guardrail event — whether from a hook, skill, or runtime check — must conform to this schema:

```typescript
interface GuardrailEvent {
  // Identity
  eventId: string;           // UUID — unique per event
  timestamp: string;         // ISO 8601 — when the guardrail fired

  // Classification
  guardrailLayer: 'input_output' | 'contextual' | 'security' | 'adaptive' | 'ethical_compliance';
  guardrailName: string;     // e.g., 'secrets-detection', 'bias-check', 'scope-creep'
  severity: 'info' | 'warning' | 'block' | 'override';

  // Context
  source: string;            // which hook, skill, or check generated this event
  trigger: string;           // what triggered the guardrail (file path, command, code pattern)
  description: string;       // human-readable explanation

  // Resolution
  action: 'allowed' | 'warned' | 'blocked' | 'overridden';
  resolution?: string;       // how it was resolved (if overridden, why)
  resolvedBy?: string;       // who resolved it (user, system, auto)

  // Metadata
  sessionId?: string;        // session that generated this event
  projectId?: string;        // project identifier
  tier?: string;             // user tier at time of event
  tags?: string[];           // additional classification tags
}
```

## Event Classification by Guardrail Layer

### Input & Output Events
```
guardrailLayer: 'input_output'
```
- Schema validation failures on API requests/responses
- Input sanitization triggers (XSS, injection patterns detected)
- Response filtering activations (sensitive fields stripped)
- Output size limit enforcement

### Contextual Events
```
guardrailLayer: 'contextual'
```
- Scope creep detection (task exceeded original boundaries)
- Domain boundary violations (out-of-scope requests)
- Tier mismatch warnings (action inappropriate for current tier)
- Context staleness warnings

### Security Events
```
guardrailLayer: 'security'
```
- Secret/credential detection in code
- Destructive command interception (rm -rf, DROP TABLE)
- PII found in logs or test fixtures
- Dependency vulnerability detected
- eval()/Function() constructor usage
- .env file without .gitignore protection

### Adaptive Events
```
guardrailLayer: 'adaptive'
```
- Tier auto-graduation (Builder -> Maker)
- Quality gate level changes
- Strictness adjustments (confidence-based)
- Profile switches (app-type detection changes)

### Ethical & Compliance Events
```
guardrailLayer: 'ethical_compliance'
```
- Bias pattern detected in decision logic
- Protected attribute usage flagged
- Compliance requirement triggered (GDPR, HIPAA, SOC 2)
- License violation in dependency
- Accessibility violation detected

## Implementation Pattern

### Structured Logger Setup

```typescript
import pino from 'pino';

const guardrailLogger = pino({
  name: 'guardrail-audit',
  level: 'info',
  // Guardrail logs go to a dedicated stream — never mixed with app logs
  transport: {
    target: 'pino/file',
    options: { destination: './logs/guardrail-audit.log' },
  },
  // Redact sensitive values from the log itself
  redact: ['trigger.fileContent', 'resolution.secretValue'],
});

function logGuardrailEvent(event: GuardrailEvent): void {
  const logMethod = event.severity === 'block' ? 'error'
    : event.severity === 'warning' ? 'warn'
    : 'info';

  guardrailLogger[logMethod](event, `[${event.guardrailLayer}] ${event.guardrailName}: ${event.action}`);
}
```

### Python Implementation

```python
import logging
import json
from datetime import datetime, timezone

guardrail_logger = logging.getLogger('guardrail-audit')
handler = logging.FileHandler('logs/guardrail-audit.log')
handler.setFormatter(logging.Formatter('%(message)s'))
guardrail_logger.addHandler(handler)
guardrail_logger.setLevel(logging.INFO)

def log_guardrail_event(event: dict) -> None:
    event['timestamp'] = datetime.now(timezone.utc).isoformat()
    level = logging.ERROR if event['severity'] == 'block' else \
            logging.WARNING if event['severity'] == 'warning' else logging.INFO
    guardrail_logger.log(level, json.dumps(event))
```

## Querying the Audit Log

Common queries that must be answerable from the log:

| Question | Query |
|---------|-------|
| "What guardrails fired this week?" | Filter by timestamp range |
| "Show all security blocks" | Filter: `guardrailLayer == 'security' AND action == 'blocked'` |
| "Who overrode a guardrail and why?" | Filter: `action == 'overridden'`, read `resolvedBy` and `resolution` |
| "How many PII violations this month?" | Filter: `guardrailName == 'pii-detection'`, count by month |
| "Is this project improving?" | Trend: violations per session over time, grouped by layer |
| "Compliance evidence for SOC 2 audit" | Filter: `guardrailLayer == 'ethical_compliance'`, export as CSV |

## Retention and Immutability Rules

1. **Append-only** — guardrail logs must never be edited or deleted by application code
2. **Minimum retention: 1 year** — or longer per compliance requirements (HIPAA: 6 years, SOC 2: varies)
3. **Separate storage** — guardrail audit logs must not share storage with application logs (prevents accidental deletion)
4. **Access control** — only security/compliance roles can read guardrail logs; application code cannot modify them
5. **Integrity verification** — hash chain or signed entries to detect tampering

## Integration with Existing Hooks

Shipworthy hooks already generate guardrail events. Connect them to the audit log:

| Hook | Events Generated |
|------|-----------------|
| `pre-tool-use` | Secret detection, eval() blocking, console.log warnings |
| `pre-tool-use-bash` | Destructive command interception |
| `post-tool-use` | Dependency changes, migration detection |
| `pre-push-validate` | Pre-push validation failures and passes |
| `session-start` | Tier detection, profile activation |

## Code Review Checklist

- [ ] Guardrail events conform to the standard schema
- [ ] Audit log is append-only and stored separately from application logs
- [ ] Override events include who authorized the override and why
- [ ] Log entries do not contain sensitive data (secrets, PII) — only references
- [ ] Retention period meets compliance requirements
- [ ] Log can be queried by layer, severity, time range, and guardrail name
- [ ] Alerting configured for `block` severity events

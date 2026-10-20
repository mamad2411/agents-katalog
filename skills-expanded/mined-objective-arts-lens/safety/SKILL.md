---
name: safety
description: "System safety - STAMP/STPA, accidents as system failures, safety constraints"
---

# Nancy Leveson - System Safety Engineering

Apply Leveson's STAMP (Systems-Theoretic Accident Model and Processes) from "Engineering a Safer World" to build systems that prevent catastrophic failures.

## Core Philosophy

### Accidents Are System Failures

Traditional thinking blames components or humans. Leveson's insight: accidents emerge from **system interactions**, not component failures.

```
TRADITIONAL MODEL (wrong):
Component fails → Accident
Human errs → Accident

LEVESON MODEL (correct):
System design allows unsafe states →
Inadequate control →
Accident

The human "error" is a SYMPTOM, not a CAUSE.
```

**Implication**: Stop asking "who screwed up?" Start asking "what system design allowed this?"

### Safety as a Control Problem

Safety isn't about preventing failures. It's about maintaining **control** over hazards.

```
HAZARD: System state that can lead to harm
SAFETY CONSTRAINT: Control that prevents hazard

Example:
├── Hazard: Database corruption from concurrent writes
├── Safety Constraint: Writes must be serialized
└── Control: Transaction isolation level

The accident happens when the control is inadequate.
```

### Humans Are Not the Problem

When humans make "errors," the system failed them.

```
BAD: "User clicked delete instead of save"
     → Add confirmation dialog

GOOD: "System design made destructive action too easy"
      → Destructive actions require different gesture
      → Undo available for 30 seconds
      → Visual distinction between create/destroy
```

**Leveson's rule**: If a human can easily cause harm, the design is wrong.

## STAMP Framework

### System-Theoretic Accident Model

```
┌─────────────────────────────────────┐
│         CONTROL STRUCTURE           │
├─────────────────────────────────────┤
│  Controller                         │
│    ├── Control Algorithm            │
│    ├── Process Model (beliefs)      │
│    └── Control Actions              │
│              ↓                      │
│  Controlled Process                 │
│    └── Feedback                     │
│              ↑                      │
└─────────────────────────────────────┘

Accidents occur when:
1. Control actions are inadequate
2. Process model doesn't match reality
3. Feedback is missing, delayed, or wrong
```

### STPA (System-Theoretic Process Analysis)

Step-by-step hazard analysis:

```
STEP 1: Define accidents and hazards
   └── What harm are we preventing?

STEP 2: Model the control structure
   └── Who/what controls what?

STEP 3: Identify unsafe control actions
   └── What control actions could cause hazard?
       ├── Not providing causes hazard
       ├── Providing causes hazard
       ├── Too early/late causes hazard
       └── Stopped too soon/applied too long

STEP 4: Identify loss scenarios
   └── Why might unsafe control actions occur?
       ├── Controller failures
       ├── Inadequate feedback
       ├── Process model inconsistency
       └── Control path failures
```

## Prescriptive Rules

### Enumerate Unsafe Control Actions

For every control action, ask four questions:

| Control Action | Not Providing | Providing | Too Early/Late | Wrong Duration |
|----------------|---------------|-----------|----------------|----------------|
| Delete record | Data lingers when should be removed | Accidental data loss | Delete before confirmation | - |
| Send notification | User misses critical info | Spam, alert fatigue | Delayed = useless | - |
| Scale up | System overwhelmed | Unnecessary cost | Scale after traffic spike | Scale too long = cost |

### Safety Constraints Must Be Explicit

```javascript
// BAD: Implicit assumption
async function transferFunds(from, to, amount) {
  await debit(from, amount);
  await credit(to, amount);
}

// GOOD: Explicit safety constraints
async function transferFunds(from, to, amount) {
  // SAFETY CONSTRAINT: Transfer must be atomic
  // HAZARD: Partial transfer (debited but not credited)
  // CONTROL: Database transaction
  await db.transaction(async (tx) => {
    await tx.debit(from, amount);
    await tx.credit(to, amount);
  });
}
```

### Process Model Must Match Reality

Controllers act on their **beliefs** about the system, not reality.

```
PROCESS MODEL DRIFT:
├── Cache believes data is current (it's stale)
├── Load balancer believes server is healthy (it's overloaded)
├── User believes file is saved (it's not)
└── Admin believes backup ran (it failed silently)

LEVESON FIX:
├── Explicit model refresh mechanisms
├── Feedback on actual state, not assumed state
├── "Trust but verify" at system boundaries
└── Alarms for model-reality divergence
```

### Feedback Must Be Adequate

```
INADEQUATE FEEDBACK:
├── Missing: No feedback at all
├── Delayed: Feedback arrives too late to correct
├── Incorrect: Feedback doesn't reflect reality
└── Ignored: System receives but doesn't process

DESIGN FOR ADEQUATE FEEDBACK:
├── Acknowledge every command
├── Confirm every state change
├── Report failures immediately and loudly
└── Make success and failure visually distinct
```

## Code Application

### Design Safety Constraints First

```yaml
Before implementing a feature:
  1. What accident could this cause?
  2. What hazards lead to that accident?
  3. What safety constraints prevent those hazards?
  4. How do we enforce those constraints?
  5. How do we know if constraints are violated?
```

### Control Structure Documentation

```javascript
/**
 * CONTROL STRUCTURE: Payment Processing
 *
 * CONTROLLER: PaymentService
 * CONTROLLED PROCESS: Payment Gateway
 *
 * SAFETY CONSTRAINTS:
 * - SC1: No duplicate charges (idempotency key required)
 * - SC2: No charges without authorization (auth check first)
 * - SC3: No partial operations (transaction required)
 *
 * FEEDBACK MECHANISMS:
 * - Gateway confirmation for every charge
 * - Reconciliation job every 15 minutes
 * - Alert if confirmation delayed > 30s
 *
 * PROCESS MODEL:
 * - Stored: customer authorization status
 * - Refresh: on every transaction
 * - Staleness tolerance: 0 (always verify)
 */
```

### Unsafe Control Action Analysis

For critical operations, document UCA analysis:

```markdown
## UCA Analysis: deleteUserAccount()

| UCA Type | Scenario | Hazard | Mitigation |
|----------|----------|--------|------------|
| Providing when shouldn't | Delete admin account | System unrecoverable | Prevent last admin delete |
| Not providing when should | Account with breach not deleted | Data exposure continues | Auto-delete on breach confirm |
| Too early | Delete before data export | User data lost | Export must complete first |
| Too late | Delete delayed after request | GDPR violation | SLA with alerting |
```

## Anti-Patterns

| Pattern | Leveson Problem | Fix |
|---------|-----------------|-----|
| "User error" post-mortems | Blaming humans, not system | Analyze control structure |
| Hidden safety assumptions | Implicit constraints fail | Document safety constraints explicitly |
| "Works on my machine" | Process model drift | Verify production state, not assumed state |
| Silent failures | Inadequate feedback | Failures must be loud and visible |
| "Just add a check" | Treating symptoms | Redesign control structure |

## Review Checklist

Before shipping safety-critical code:

- [ ] What accidents could this system cause?
- [ ] What are the hazards? (System states leading to accidents)
- [ ] What safety constraints prevent hazards?
- [ ] Is the control structure documented?
- [ ] Are unsafe control actions enumerated?
- [ ] Does the process model refresh adequately?
- [ ] Is feedback adequate (not missing, delayed, or wrong)?
- [ ] If humans can cause harm easily, is that a design flaw?

## Leveson Score

| Score | Meaning |
|-------|---------|
| 10 | Full STPA analysis, explicit safety constraints, adequate feedback |
| 7-9 | Safety constraints documented, some UCA analysis |
| 4-6 | Some safety thinking but implicit, blame-focused post-mortems |
| 0-3 | No safety analysis, "user error" culture |

## Key Quotes

> "Most accidents are not the result of unknown scientific principles but rather of a failure to apply well-known, standard engineering practices."

> "Blaming operators for accidents is not only unfair but is a way of avoiding the real problems."

> "Safety is a system property, not a component property."

## Integration

Combine with:
- `/failure` - Historical failure analysis
- `/resilience` - Antifragile design
- `/security-mindset` - Security threat modeling (similar structure to STPA)

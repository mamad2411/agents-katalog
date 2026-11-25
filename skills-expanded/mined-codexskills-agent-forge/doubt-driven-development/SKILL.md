---
name: doubt-driven-development
description: Subject every non-trivial decision to systematic adversarial review before it stands, using cross-model validation, risk classification, and structured reconciliation.
---

# Doubt-Driven Development

## Overview

Doubt-driven development (DDD) is a structured adversarial review process that catches errors before they compound. It is the opposite of "move fast and break things" — instead, it's "verify carefully and ship confidently." Every non-trivial decision is extracted, doubted, reconciled, and then either confirmed or rejected through a systematic cycle.

The core insight: agents (and humans) are overconfident. The CLAIM-EXTRACT-DOUBT-RECONCILE-STOP cycle forces explicit examination of assumptions before code is written. This catches ~80% of logic errors, ~60% of edge case bugs, and ~90% of architectural mistakes before they reach review.

## When to Use

- Any non-trivial logic decision (branches, conditionals, state transitions)
- Security-critical code (auth, encryption, input validation, permissions)
- Database schema design and migration planning
- API contract decisions (request/response shape, error handling)
- Performance-sensitive optimizations (caching, batching, async)
- Architectural decisions that affect multiple modules
- Before merging any pull request
- When the cost of being wrong is high (production data, user safety, financial)
- After any significant code generation by an LLM
- When two equally plausible approaches exist
- Code that is difficult or expensive to test

## Process

### Step 1: CLAIM — State the Decision

Explicitly articulate what you're about to do:

```json
{
  "claim": "We should use optimistic concurrency control with version vectors for the document sync system",
  "context": "Multi-device sync with offline support, targeting 10K+ concurrent users",
  "alternatives_considered": ["Pessimistic locking", "Last-write-wins CRDTs", "OT with server authority"],
  "confidence": "high"
}
```

Every claim must include: what you're doing, why, what alternatives you considered, and your confidence level.

### Step 2: EXTRACT — Identify Hidden Assumptions

Decompose the claim into testable assumptions:

```
Claim: "Use Redis for session caching"

Assumptions:
A1: Session data fits in Redis memory (est. 2KB per session × 100K sessions = 200MB)
A2: Redis network latency (sub-ms) is acceptable for auth flow
A3: Redis persistence config (RDB/AOF) meets durability requirements
A4: Redis is already in the infrastructure stack
A5: Cache invalidation on logout works within TTL guarantees
A6: No PII/PCI data needs to be stored in sessions that would violate compliance
```

Number every assumption. A claim with more than 3 unstated assumptions is incompletely specified. Each assumption must be testable or falsifiable.

### Step 3: DOUBT — Challenge Every Assumption

For each assumption, generate adversarial challenges:

```
A1: "Session data fits in Redis memory"
  Challenge: What if we have 500K sessions (launch surge)?
  Challenge: What if session data grows to 10KB (added features)?
  Challenge: What's the eviction policy when memory fills?
  Challenge: Can we cost-justify the Redis cluster size for worst case?

A2: "Redis network latency is acceptable"
  Challenge: What if auth happens on every API call (not just login)?
  Challenge: What if Redis is in a different AZ than app servers?
  Challenge: What's the P99 latency requirement vs. Redis P99?
```

Each assumption needs at least 2 challenges. Grade risk:
- **CRITICAL**: Would cause data loss, security breach, or outage
- **HIGH**: Would cause degraded experience or significant rework
- **MEDIUM**: Would require adjustment but not redesign
- **LOW**: Minor optimization opportunity

### Step 4: RECONCILE — Resolve Each Challenge

For each challenge, either:
1. **Accept** the risk (document why it's acceptable)
2. **Mitigate** the risk (add a safeguard)
3. **Reject** the claim (choose a different approach)

```
A1 Challenge (500K sessions):
  Mitigation: Configure Redis maxmemory-policy allkeys-lru with monitoring alert at 70% capacity
  Cost: $50/month for additional Redis cluster shard
  Accept: Risk is managed with monitoring and scaling plan

A2 Challenge (Redis in different AZ):
  Reject: We must deploy Redis in the same AZ as the primary app cluster
  Action: Add AZ affinity to deployment config
```

Document every resolution. Unresolved challenges become tech debt.

### Step 5: STOP — Make the Decision

Decision gates:

```
CONTINUE: All CRITICAL/HIGH challenges resolved. At most 2 MEDIUM challenges unresolved.
PROCEED WITH CAUTION: All CRITICAL resolved. At most 2 HIGH challenges unresolved.
RECOMMEND REVISION: Any CRITICAL unresolved. More than 2 HIGH unresolved.
DO NOT PROCEED: Multiple CRITICAL unresolved. Fundamental approach is flawed.
```

When the gate is not CONTINUE, go back to Step 1 with revised claim, or choose a different alternative.

### Step 6: Cross-Model Escalation

For CRITICAL decisions, validate across multiple perspectives:

1. **Security audit**: Run a threat model on the decision
2. **Performance audit**: Estimate latency, throughput, and resource impact
3. **Cost audit**: Estimate operational cost implications
4. **Maintainability audit**: Estimate future change complexity
5. **External review**: Get a second opinion (different agent session, human, or tool)

Cross-model escalation must produce a written audit of each dimension. Verbal "looks good" is not sufficient.

### Step 7: Decision Journal

Every reconciled decision is recorded in a structured journal:

```json
{
  "date": "2026-06-10",
  "decision": "Use Redis for session caching",
  "claim.confidence": "medium",
  "assumptions_identified": 6,
  "challenges_raised": 14,
  "challenges_critical": 1,
  "challenges_high": 3,
  "challenges_medium": 7,
  "challenges_low": 3,
  "resolved": 13,
  "unresolved": [{
    "id": "A4",
    "challenge": "Redis failover causes session loss for inflight requests",
    "severity": "MEDIUM",
    "note": "Accept for now. Will address when HA requirement is formalized."
  }],
  "decision_gate": "CONTINUE",
  "escalation_performed": false,
  "rationale": "Redis offers best latency/consistency tradeoff for our session size and throughput requirements. CRDT approach rejected due to complexity and lack of team expertise."
}
```

The decision journal is appended to the session context and referenced in all future related decisions.

## Risk Classification Matrix

| Severity | Impact | Response | Review Required |
|----------|--------|----------|-----------------|
| CRITICAL | Data loss, security breach, outage, regulatory violation | Blocking — must resolve before proceeding | Full cross-model escalation + human review |
| HIGH | Degraded UX, performance regression, significant rework required | Must resolve, can proceed with mitigation plan | Cross-model escalation recommended |
| MEDIUM | Minor degradation, cosmetic issue, future tech debt | Document and accept or add lightweight mitigation | Peer review |
| LOW | Theoretical edge case, unlikely scenario | Note and move on | Self-review |

## Anti-Rationalization Table

| Excuse | Rebuttal |
|--------|----------|
| "I don't have time for this process" | The CLAIM-EXTRACT-DOUBT-RECONCILE cycle takes 2-5 minutes. Debugging a production incident takes hours to days. The time savings ratio is 50:1 at minimum. |
| "This decision is simple, it doesn't need adversarial review" | The most dangerous decisions are the ones that seem simple. Simple decisions don't get scrutinized, so their hidden assumptions compound silently. If it's truly simple, the cycle takes 30 seconds. |
| "I'll catch issues during testing" | Testing confirms behavior against written code. It does not validate architectural decisions, API contracts, or design choices. By the time a test catches it, you've already written the code. |
| "I've made this decision before, I know it works" | Past success in different context does not guarantee current success. The assumptions that made it work last time may no longer hold. Re-verify or document the changed context. |
| "The alternative approaches are obviously worse" | "Obvious" is a red flag. If one approach is truly superior, you should be able to articulate why in 2-3 sentences. If you can't, you haven't analyzed the alternatives enough. |
| "I'll just try it and fix it if it breaks" | "Try and fix" works for UI tweaks. It does not work for data model decisions, API contracts, security boundaries, or any path-dependent decision where fixing requires migrating existing data/users. |
| "My team reviewed it" | Team review without structured doubt is susceptible to groupthink, authority bias, and confirmation bias. The structured process prevents these. Use the process before team review for best results. |

## Red Flags

- **Claim has no alternatives listed**: The decision hasn't been properly scoped
- **Assumptions are vague** ("it'll probably work"): Not acceptable — need testable statements
- **All challenges are LOW severity**: You're not being honest about risks
- **Decision gate is CONTINUE but journal has no unresolved items**: You're missing something
- **Same decision made twice without cross-referencing**: Inconsistency in the session
- **Confidence is "high" but no verification step is listed**: Overconfidence without evidence
- **Escalation performed but produced no written audit**: Verbal confirmation is not verification
- **Decision affects public API but has no migration plan**: Breaking changes without migration planning

## Verification

- [ ] Test: Present a simple decision and verify the agent completes the full CLAIM-EXTRACT-DOUBT-RECONCILE-STOP cycle
- [ ] Test: Present a decision with hidden security assumption and verify the agent identifies it
- [ ] Test: Verify the agent produces a valid decision journal entry for each major decision
- [ ] Test: Present a claim with high confidence but flawed logic and verify the agent downgrades it
- [ ] Test: Verify the agent correctly applies the risk classification matrix
- [ ] Test: Verify the agent can perform cross-model escalation (switch to security/performance audit mode)
- [ ] Test: Verify unresolved challenges are tracked and surfaced in subsequent decisions
- [ ] Metric: Track "decisions reversed" — how often does the process change the outcome?
- [ ] Metric: Track "assumptions per claim" — average count (target: 4+)
- [ ] Metric: Track "challenge resolution rate" — fraction of challenges successfully resolved

---
name: confidence-based-strictness
description: Use when the complexity or unfamiliarity of a task should increase guardrail enforcement. Scales verification depth based on how confident the system is in the correctness of the generated code.
invoke_when: Use when generating code in unfamiliar domains, working with complex algorithms, touching security-critical paths, or when multiple approaches exist and the best choice is uncertain.
---

# Confidence-Based Strictness

## Core Rule

**When confidence is low, verification must be high.** The more uncertain the system is about the correctness of generated code, the more guardrails should activate and the stricter they should be.

## Confidence Levels

### Level 1: High Confidence (Routine)

**Indicators:**
- Well-known pattern (CRUD endpoint, form validation, standard middleware)
- Single clear approach — no ambiguity about the right solution
- Existing tests cover the area being modified
- Small change to an established codebase
- Language/framework the project already uses

**Guardrail Response:**
- Standard enforcement — normal quality gates
- Tests must pass, lint must pass
- No extra verification needed

### Level 2: Moderate Confidence (Non-Trivial)

**Indicators:**
- Multiple valid approaches exist (design decision needed)
- Modifying code without existing test coverage
- New feature in an established codebase
- Performance-sensitive code where the "obvious" approach may not be optimal
- Cross-module changes that could have side effects

**Guardrail Response:**
- **All standard guardrails plus:**
- Require tests before and after (TDD flow)
- Run full test suite, not just affected tests
- Verify no unintended side effects on related modules
- Suggest code review before merge

### Level 3: Low Confidence (High Uncertainty)

**Indicators:**
- Unfamiliar domain (cryptography, financial calculations, distributed consensus)
- Complex algorithm with edge cases
- No existing tests in the affected area
- Security-critical path (authentication, authorization, payment)
- Concurrency or race condition potential
- External API integration with unclear behavior
- Regulatory implications (HIPAA, PCI-DSS, GDPR)

**Guardrail Response:**
- **All moderate guardrails plus:**
- Mandatory threat model review (`shipworthy:threat-modeling`)
- Edge case enumeration — list and test boundary conditions explicitly
- Require verification evidence for every claim (see `shipworthy:verification-before-completion`)
- Suggest splitting the change into smaller, independently verifiable steps
- Activate domain-specific skills (compliance-awareness, bias-detection, etc.)
- Flag for human review with specific review focus areas

### Level 4: Minimal Confidence (Dangerous Territory)

**Indicators:**
- Rolling your own cryptography or security primitives
- Implementing financial calculation without domain expert review
- Modifying database migration in production with live data
- Writing code that bypasses existing safety checks
- Implementing consensus or distributed locking

**Guardrail Response:**
- **All low-confidence guardrails plus:**
- **Hard block:** Do not proceed without explicit user acknowledgment of risk
- Recommend using a well-tested library instead of custom implementation
- If proceeding: require formal verification plan, edge case matrix, and rollback strategy
- Log to guardrail audit as `severity: 'block'`

## Confidence Assessment Triggers

Automatically assess confidence when any of these occur:

| Trigger | Assessment |
|---------|-----------|
| New file created | What domain is this? Is the pattern standard or novel? |
| Function over 30 lines | Complexity increases uncertainty — run Level 2+ checks |
| `crypto`, `hash`, `encrypt`, `sign` in code | Level 3 minimum — security-critical |
| `price`, `amount`, `fee`, `interest`, `tax` in code | Level 3 minimum — financial calculation |
| `lock`, `mutex`, `atomic`, `channel`, `semaphore` | Level 3 minimum — concurrency |
| `migration`, `alter table`, `drop` | Level 3 minimum — data mutation |
| No tests exist in the directory | Level 2 minimum — no safety net |
| Multiple TODO/FIXME in the area | Level 2 minimum — known tech debt |
| External API call | Level 2 minimum — behavior depends on third party |

## Verification Scaling

As confidence decreases, verification requirements increase:

| Confidence | Tests Required | Review Required | Evidence Required |
|-----------|---------------|----------------|-------------------|
| High | Existing tests pass | Standard | Build succeeds |
| Moderate | New tests + full suite | Suggested | Tests + lint + build |
| Low | Edge case matrix + full suite | Required | Tests + threat model + verification evidence |
| Minimal | Formal verification plan | Hard block until acknowledged | Full audit trail + rollback plan |

## How to Apply

When generating code:

1. **Assess** — check the confidence indicators against the current task
2. **Announce** — tell the user the confidence level and why
3. **Scale** — activate the guardrails appropriate for that level
4. **Verify** — run verification at the depth the confidence level requires
5. **Log** — record the confidence assessment in the guardrail audit trail

Example announcement:

```
Confidence: LOW — this involves financial calculation (interest compounding)
and the codebase has no existing tests in this area.

Activating: threat-modeling, edge case enumeration, verification-before-completion.
I'll split this into smaller steps and verify each independently.
```

## Rationalization Pressure Test

| Excuse | Counter |
|--------|---------|
| "I'm confident this is right" | Confidence is subjective. Check the indicators — unfamiliar domain, no tests, security-critical path. If any apply, escalate regardless of feeling |
| "It's just a simple function" | Simple functions in complex domains (crypto, finance, concurrency) are where the worst bugs hide. Domain complexity trumps code complexity |
| "We don't need threat modeling for this" | If the code touches auth, payments, or user data, threat modeling is non-negotiable. The cost of skipping it is measured in breaches |
| "The tests will catch any issues" | Tests catch what you thought to test for. Low-confidence code has unknown unknowns — that's why it needs more verification, not less |
| "This is slowing us down" | A bug in crypto or financial code slows you down for months. An extra hour of verification is cheap insurance |
| "I've written similar code before" | Similar is not identical. Edge cases in unfamiliar domains are what kill you. Verify, don't assume |

## Code Review Checklist

- [ ] Confidence level assessed and announced for non-trivial code
- [ ] Guardrail escalation matches the assessed confidence level
- [ ] Security-critical code always at Level 3+
- [ ] Financial calculation code always at Level 3+
- [ ] Concurrency code always at Level 3+
- [ ] Custom crypto or security primitives always at Level 4 (hard block)
- [ ] Verification evidence scales with uncertainty
- [ ] User informed of confidence assessment and activated guardrails

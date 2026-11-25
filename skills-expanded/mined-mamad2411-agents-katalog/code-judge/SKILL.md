---
name: code-judge
description: Activates when reviewing, auditing, or judging code quality. Applies a structured multi-dimensional assessment grounded in ISO/IEC 25010:2023, OWASP Top 10:2025, CWE Top 25, NIST SP 800-218, and algorithmic complexity analysis. Scores correctness, efficiency, security, maintainability, reliability, and testability with calibrated thresholds and standard citations.
---

# Code Judge

Structured code quality assessment across six dimensions mapped to ISO/IEC 25010:2023 quality characteristics. Score each 0–2 (0 = violation present, 1 = meets expectations, 2 = exceeds expectations).

## 1. Correctness (Functional Suitability)

- All specified requirements satisfied
- Edge cases handled: empty/null input, boundary values, integer overflow, Unicode
- Loop invariants hold; no off-by-one errors
- No undefined behavior, silent data loss, or corruption
- Contracts enforced: preconditions checked, postconditions guaranteed

## 2. Efficiency (Performance Efficiency)

- Time complexity optimal for the problem class — see [EFFICIENCY.md](EFFICIENCY.md)
- Space complexity justified; no unnecessary copies or allocations
- Data structure matches access pattern:
  - Lookup → hash map O(1), not linear scan O(n)
  - Sorted access → balanced tree or sorted array, not repeated sort
  - Top-k → heap O(n log k), not full sort O(n log n)
  - Membership → set O(1), not list scan O(n)
  - Queue → deque O(1), not list shift O(n)
- No accidental quadratic: string concatenation in loop, nested iteration over same collection, repeated indexOf/contains
- I/O streamed where possible; large datasets not fully materialized in memory
- Native/stdlib operations preferred over hand-rolled equivalents

## 3. Security (OWASP Top 10:2025 · CWE Top 25 · NIST SP 800-218)

- Input validated and sanitized at every trust boundary
- No injection vectors: SQL (parameterized queries), command (argv arrays, no shell), XSS (escape output), path traversal (canonicalize + allowlist)
- Passwords: memory-hard KDF (argon2id preferred, bcrypt/scrypt/PBKDF2 acceptable per OWASP ASVS V6 and NIST SP 800-63B); never plain SHA/MD5
- Secrets not hardcoded, not logged, not in version control
- Cryptography: no MD5/SHA-1/DES/ECB; use AES-256-GCM or ChaCha20-Poly1305; CSPRNG for randomness
- Dependencies audited; no known CVEs in direct dependencies
- See [SECURITY.md](SECURITY.md) for OWASP/CWE/NIST quick reference

## 4. Maintainability

- Cyclomatic complexity per function ≤ 10 (McCabe, "A Complexity Measure," IEEE TSE, 1976)
- Cognitive complexity per function ≤ 15 (SonarSource metric)
- Functions do one thing; named for what they return or effect
- No dead code, no commented-out code, no untracked TODOs
- Naming consistent, domain-appropriate, self-documenting
- DRY applied — but premature abstraction is worse than duplication
- Files focused: single responsibility, ≤ 500 lines preferred

## 5. Reliability

- Errors handled explicitly: no bare except/catch-all, no swallowed errors
- Fail-fast on precondition violations; fail-closed on security checks
- Resources cleaned up deterministically: close/defer/finally/with/using/RAII
- External dependency failures handled: timeouts, retries with exponential backoff, circuit breakers
- No panic/crash on recoverable errors; reserve panics for truly unrecoverable states
- Idempotent where operations may be retried

## 6. Testability

- Pure functions preferred; side effects isolated at boundaries
- Dependencies injectable, not hardcoded (no global state, no hidden singletons)
- Behavior tested, not implementation details
- Coverage targets: statement ≥ 80%, branch ≥ 70% (ISTQB foundation-level guidelines)
- Edge cases and error paths tested, not just happy path

## Scoring

Total = sum of dimension scores (0–12).

| Range | Verdict | Action |
|-------|---------|--------|
| 10–12 | Exemplary | Approve |
| 7–9 | Acceptable | Approve with minor suggestions |
| 4–6 | Needs work | Request changes |
| 0–3 | Reject | Block until resolved |

**Priority when dimensions conflict:** Correctness > Security > Reliability > Efficiency > Maintainability > Testability.

## 7. Skill Effectiveness (A/B comparison)

When comparing a with-skill output against a baseline (no-skill) output, assess whether the skill(s) produced a measurable improvement.

**Evidence of influence** — identify specific patterns, techniques, or decisions in the with-skill output that trace directly to skill guidance and are absent from the baseline.

**Positive lift** — improvements the baseline would not have produced:
- Higher-quality algorithm or data structure choice
- Standards compliance introduced (OWASP, NIST, etc.)
- Production-readiness features (error handling, observability, CI gates)
- Deeper domain coverage (edge cases, accessibility, security hardening)

**Regressions** — skill-induced degradations:
- Over-engineering: added complexity beyond what the task requires
- Scope creep: features or layers not asked for that obscure the core solution
- Wrong technique: skill pushed a "better" pattern that is worse in context (e.g., manual loop replacing a native stdlib function, generic API replacing a simpler specific one)
- Rubric mismatch: skill-guided output is objectively correct but uses an approach the rubric doesn't list (flag the rubric, not the code)

**Scoring:** -2 to +4 (net delta across all six quality dimensions).

| Delta | Verdict |
|-------|---------|
| +3 to +4 | Strong positive — skill substantially improved output |
| +1 to +2 | Positive — skill added meaningful value |
| 0 | Neutral — no measurable difference |
| -1 | Minor regression — skill hurt more than helped |
| -2 | Regression — skill actively degraded output |

**Attribution rule:** only credit the skill for improvements that are *absent from baseline*. If baseline already handles something correctly, the skill gets no credit for also handling it.

## Output format

Use this structure for all code reviews:

```
## Code Review

**Verdict:** [Exemplary/Acceptable/Needs work/Reject] ([score]/12)

| Dimension | Score | Notes |
|-----------|-------|-------|
| Correctness | X/2 | ... |
| Efficiency | X/2 | ... |
| Security | X/2 | ... |
| Maintainability | X/2 | ... |
| Reliability | X/2 | ... |
| Testability | X/2 | ... |

### Critical issues
1. **[Dimension]** Description — standard: [citation] — fix: ...

### Improvements
1. **[Dimension]** Suggestion — fix: ...

### Strengths
- ...
```

When comparing baseline vs with-skill, append:

```
## Skill Effectiveness

**Delta:** [+N/-N] — [Strong positive/Positive/Neutral/Minor regression/Regression]

### Evidence of skill influence
- [Pattern/technique traceable to skill guidance]

### Positive lift
- [Improvement absent from baseline] — dimension: [which] — standard: [citation]

### Regressions
- [Degradation caused by skill] — dimension: [which] — cause: [over-engineering/scope creep/wrong technique/rubric mismatch]
```

## References

- **Efficiency anti-patterns**: [EFFICIENCY.md](EFFICIENCY.md)
- **Security standards map**: [SECURITY.md](SECURITY.md)
- ISO/IEC 25010:2023 — Software product quality model
- McCabe, T.J. (1976). "A Complexity Measure." IEEE Transactions on Software Engineering.
- OWASP Top 10:2025, ASVS 5.0, Proactive Controls 2024
- NIST SP 800-218 (SSDF), SP 800-63B, SP 800-175B
- CWE/SANS Top 25 Most Dangerous Software Weaknesses
- ISTQB Certified Tester Foundation Level Syllabus

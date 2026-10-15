---
name: eng-hardening-review
description: Audit data integrity and error-handling completeness across the six failure surfaces (API, file, database, network, configuration, input). Use after implementation or as a pre-release hardening pass to ensure real data sources, schema consistency, and realistic failure coverage.
---

# Hardening Review: Data Integrity & Error Handling

A focused deep-dive that pairs with `eng-multidimensional-audit`: while the multidimensional scan maps broad architecture risks, this skill goes deep on two production killers: fake or inconsistent data, and missing failure handling.

## Dimension A: Data Integrity Hardening

**A1. Real Data Source Verification**
- Trace every data reference to its origin: live API response, database record, system metric, log entry, or user-provided file.
- Flag and reject: hardcoded mock rows, random-generated demo values, placeholder fixtures in non-test code paths, guessed defaults pretending to be config.
- Test fixtures are allowed only inside test scope and must not leak into runtime paths.

**A2. Schema Consistency**
- Cross-check entity definitions across layers: DB schema, ORM models, API request/response types, frontend interfaces.
NaN
- Verify constraint alignment: required/nullable, length limits, enums, foreign keys, unique keys.

**A3. Migration & Compatibility**
- Schema changes ship with forward-compatible migrations and a rollback statement.
- Breaking changes carry an explicit deprecation path.

## Dimension B: Error-Handling Hardening (Six Failure Surfaces)

| Surface | Required Coverage | Typical Gap |
|---|---|---|
| API | Non-2xx handling, timeout, retry with backoff, rate-limit respect | Treating all responses as success |
| File | Not-found, permission denied, disk full, encoding errors, partial writes | Assuming read/write always succeeds |
| Database | Connection loss, deadlock retry, constraint violation mapping, transaction rollback | Swallowed rollback errors |
| Network | Offline detection, timeout vs hang, partial response parsing, TLS errors | Unbounded waits |
| Configuration | Missing key, invalid value, type mismatch, environment drift | Silent default fallback hiding misconfig |
| Input | Type coercion, boundary values, injection vectors, oversized payloads | Trusting client-side validation alone |

For every surface: verify the error is **caught**, **translated** to a domain error code, **logged** with context, and **surfaced** to the appropriate caller level. Silent catch blocks are findings.

---

## Output Template

```markdown
# Hardening Review Report: <scope>

## Data Integrity Findings
| ID | Severity | Location | Finding | Fix Direction |
|---|---|---|---|---|
| DI-1 | HIGH | `path:line` | Mock data in runtime path | Wire real source `<verified origin>` |

## Error Handling Matrix
| Surface | Caught | Translated | Logged | Surfaced | Verdict |
|---|---|---|---|---|---|
| API | yes/no | yes/no | yes/no | yes/no | PASS/GAP |

## Verdict: [HARDENED | NEEDS WORK (N gaps)]
```

---

## Checkable Completion Criteria

- [ ] Every runtime data reference traced to a verified real origin.
- [ ] Schema consistency cross-checked across all four layers.
- [ ] All six failure surfaces evaluated with per-surface verdicts.
- [ ] Findings report archived with severity and fix directions.
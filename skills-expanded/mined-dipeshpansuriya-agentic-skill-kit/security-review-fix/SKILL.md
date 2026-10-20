---
name: security-review-fix
description: Find and fix security issues in code, SQL, config and dependencies, with CWE, severity, fixed code and tests. Use when the user asks for a security check, to fix vulnerabilities, OWASP issues, secrets, SQL injection, or pen-test findings.
---

# Security Review & Fix (defensive)

Find vulnerabilities, fix them with minimal diffs, and prove each fix with a test. Report what was checked; never certify "secure".

## Inputs
- Code (files, diff, repo path), SQL scripts, config (`appsettings*.json`, `application.yml`, `.env`, Dockerfile, Terraform, k8s YAML), lock files
- Optional: pen-test / SAST / SCA report (ZAP, Burp export, Semgrep, CodeQL, Sonar, `npm audit`), threat model, data classification
- Context: internet-facing or internal, auth model, tenants, data held (customer PII, passport/APIS, payment, customs)

Pen-test report given: treat each item as a finding to confirm in code, then fix; map to CWE/OWASP.

## Defaults (state them in one line)
| Setting | Default if not stated | Ask only if |
|---|---|---|
| Threat context | Internet-facing, authenticated multi-tenant users, attacker is any logged-in user or anonymous | Internal-only changes severity a lot and code doesn't show it |
| Scope | Given files + config + dependency manifests | "Whole repo" and it is large: ask for entry points |
| Standards | OWASP Top 10:2025 + API Security Top 10:2023, CWE IDs; add 2021 IDs if the team uses them | Never |
| Severity | `references/severity-rubric.md` (exploitability × impact) | Never |
| Fix style | Minimal diff in the codebase's language and conventions | Fix needs a design change (e.g. new auth flow) |

## Which reference to read
| Need | Read |
|---|---|
| Category coverage, API risks, manual checklist | `references/owasp-checklist.md` |
| Vulnerable → secure code (.NET, Java, Python, React, Angular, SQL) | `references/stack-fixes.md` |
| Secrets found, config hardening, headers, CORS, CSRF cookies, logging PII, containers | `references/secrets-and-config.md` |
| Vulnerable packages, SCA/SAST/secret/IaC tools and commands | `references/dependency-scanning.md` |
| Assigning Critical/High/Med/Low | `references/severity-rubric.md` |

## Steps
1. **Scope & threat context.** List what is in scope, entry points (endpoints, message consumers, file uploads, webhooks), trust boundaries, and data classes. State defaults used.
2. **Automated pass.** `python3 scripts/sec_scan.py src/ config/` (heuristic: secrets masked, file:line, rule, CWE, severity). Recommend the matching SCA/SAST commands from `references/dependency-scanning.md`; include results if the user provides them.
3. **Manual pass.** Walk `references/owasp-checklist.md` for each entry point: authn, authz (BOLA/IDOR, function-level), input → sink (SQL/NoSQL, shell, HTML, file paths, URLs for SSRF, deserializers), JWT validation, crypto, CSRF/CORS/headers, error handling, logging of PII/secrets, config and containers.
4. **Confirm each finding** at a file:line. Trace the input source when possible; if the source can't be traced from the given code, keep the finding and label it **Verify:** with what to check. Merge same-root-cause rows.
5. **Rate severity** with the rubric; write a one-line rationale (exploitability × impact).
6. **Fix** every Critical/High/Med with a minimal diff from `references/stack-fixes.md`. Keep behaviour for valid input unchanged. Low: fix if trivial, else list.
7. **Test each fix**: a unit/integration test showing the malicious input is handled safely (e.g. `' OR '1'='1` treated as a literal → 0 rows; `../` path rejected; other tenant's ID → 404; `javascript:` URL rejected) and valid input still works.
8. **Secrets**: mask (first 4 chars + `****`), require rotation at the issuer, move to a secret store, add secret scanning.
9. **Residual risk & follow-ups**: what wasn't fixed and why, what wasn't reviewed, suggested tools to run.
10. Fill `templates/security-report-template.md`; run the self-check.

## Rules
- **Defensive only.** Never write exploit code, attack chains, weaponized payloads or instructions for attacking systems. Test inputs are limited to the minimal strings needed to prove a fix in the user's own tests.
- Mask every secret in output (first 4 chars + `****`), including in code snippets and diffs.
- An exposed secret must be **rotated**; moving it to config or deleting the line is not enough (git history keeps it).
- Fixes must not break functionality: same behaviour for valid input; existing tests pass; show the new test.
- Prefer framework mechanisms (parameterized queries, built-in auth policies, encoders, password hashers) over custom code; never roll your own crypto.
- Label uncertain findings **Verify** and say what to confirm. Never invent CVEs, advisory IDs, versions, or line numbers.
- Never claim the code is "secure": state what was checked, with which tools, and what was out of scope.
- Rank Critical → High → Med → Low; one root cause = one row.
- Performance issues → code-performance; DB query tuning → sql-performance-tuning; a general PR verdict → code-review.

## Self-check
- [ ] Scope, threat context and defaults stated
- [ ] `scripts/sec_scan.py` run (or its absence explained) and each hit confirmed or dismissed
- [ ] Every finding has file:line, CWE, OWASP 2025 ID, severity + rationale
- [ ] Every Critical/High/Med has a minimal-diff fix and a test proving it
- [ ] All secrets masked; rotation required for each exposed secret
- [ ] Dependencies checked or the exact SCA commands given
- [ ] Uncertain items labelled **Verify**; nothing invented
- [ ] No exploit code or attack instructions
- [ ] "What was checked" section present; no "secure" claim

## Output
1. **Assumptions** line (scope, threat context, stack).
2. Report per `templates/security-report-template.md`: Summary counts, Findings table, Fixes (diffs), Tests, Secrets, Dependencies, Residual risk, What was checked.
3. Full fixed code per file (path heading) when the diff is not enough to apply.

## Files
| Path | Purpose |
|---|---|
| `scripts/sec_scan.py` | Stdlib heuristic scanner for code + config; masks secrets; exit 1 on Critical/High; `nosec` on a line suppresses a reviewed hit |
| `templates/samples/bad_sec.cs`, `templates/samples/BadSec.java`, `templates/samples/bad_sec.py`, `templates/samples/bad_sec.tsx`, `templates/samples/bad_config.yml` | Deliberately vulnerable samples. Fake secrets are placeholders: run `python templates/samples/render_samples.py OUT_DIR` and scan OUT_DIR. Must trigger |
| `templates/samples/clean_sec.cs`, `templates/samples/clean_sec.py`, `templates/samples/clean_sec.ts` | Secure equivalents: must report 0 findings |
| `evals/test-cases.md` | Trigger and quality test cases; rerun after every edit |

Scanner limits: no taint tracking (false positives on constant SQL concat, misses injection via helpers); names drive secret detection. Always confirm manually.

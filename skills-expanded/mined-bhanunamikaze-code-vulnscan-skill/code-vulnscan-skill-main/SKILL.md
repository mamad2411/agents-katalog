---
name: code-vulnscan
description: Use this when the user wants to find security vulnerabilities in a codebase, perform a security audit, scan for CVEs, detect secrets, review React/Next.js, Go, Java/Kotlin JVM, PHP, Ruby, .NET, or Rust web services, audit architecture/application/infrastructure flaws, review auth/API/crypto/business logic, check IaC/cloud/runtime configs, or generate a vulnerability report. Performs taint-flow, control-flow, architecture, and exploitability analysis across Python, JS/TS, Java/Kotlin, Go, PHP, Ruby, C/C++, C#, Rust, and infrastructure.
---

# Code-VulnScan — Deep Codebase Vulnerability Scanner

This skill performs comprehensive, flow-aware security analysis on any codebase. It combines taint tracking, control-flow analysis, business logic review, API security auditing, secret detection, configuration review, and dependency auditing to find real, exploitable vulnerabilities — not keyword matches.

- Use the IDE's own tools for reading, searching, and reasoning about code.
- Use local Python scripts for deterministic file enumeration, AST-based analysis, secret entropy scanning, dependency checking, state tracking, and report generation.
- Do not call external LLM-provider APIs as part of this skill.
- Every confirmed finding requires a verified evidence chain. Candidates without verification are never reported.

## Command surface

- `vulnscan scan <path> [--lang python,javascript,...] [--severity critical,high,medium,low] [--exclude vendor,tests]`
- `vulnscan taint <file> [--lang <language>]`
- `vulnscan secrets <path>`
- `vulnscan deps <path>`
- `vulnscan config <path>`
- `vulnscan report [--run-id <id>] [--format markdown|html|json|sarif|all] [--min-severity medium]`
- `vulnscan status`
- `vulnscan commit <hash> [--repo <path>] [--base <base-hash>] [--severity critical,high,medium,low]`
- `vulnscan diff <base> <head> [--repo <path>] [--severity critical,high,medium,low]`
- `vulnscan pr <pr-number> [--repo <path>] [--severity critical,high,medium,low]`

**Commit/diff mode:** Scans only the files and code regions changed in a commit or between two refs. Faster than a full scan — designed for CI/CD pipelines and code review. Findings are tagged `introduced_in_diff: true` (new vulnerability in the changed code) or `introduced_in_diff: false` (pre-existing vulnerability in code called by the change). Use `vulnscan commit HEAD` to scan the most recent commit, `vulnscan diff main HEAD` to scan a feature branch, or `vulnscan pr 42` to scan a GitHub PR diff.

Defaults: report every validated severity and auto-detect language from file extensions. Use `--min-severity` when the user explicitly requests a threshold.

## Core architecture

- `sub-skills/` — cognitive instructions for each analysis phase (29 specialized reviewers)
- `scripts/` — deterministic Python helpers for enumeration, AST analysis, entropy scanning, dependency checking, report generation
- `resources/patterns/` — per-language source/sink/sanitizer pattern definitions
- `resources/references/` — CWE taxonomy, OWASP Top 10, false-positive guidance
- `workspace/` — SQLite scan state, intermediate JSON outputs, final reports

## The golden rule: evidence-based findings only

A confirmed finding requires **all three**:
1. A **source** — user-controlled data enters the system (or a dangerous condition exists).
2. A **sink / consequence** — a dangerous operation can be triggered.
3. A **path** — source reaches sink with no effective mitigation in between.

Pattern-match candidates are **never** confirmed findings. Every candidate passes through `sub-skills/false-positive-filter.md` before being reported.

## Vulnerability categories covered

| Category | Technique | CWE |
|----------|-----------|-----|
| SQL Injection | Taint + AST | CWE-89 |
| Command Injection | Taint + AST | CWE-78 |
| Path Traversal | Taint + canonicalization check | CWE-22 |
| XSS (Reflected/Stored/DOM) | Taint + output context | CWE-79 |
| SSRF | Taint + URL validation check | CWE-918 |
| Insecure Deserialization | Taint + API check | CWE-502 |
| Server-Side Template Injection | Taint + template API check | CWE-94 |
| Open Redirect | Taint + redirect target check | CWE-601 |
| XXE | Config + parser API check | CWE-611 |
| Auth Bypass / Broken Access Control | Control flow + logic analysis | CWE-287, CWE-285 |
| Broken Authentication | Session + token analysis | CWE-306, CWE-384 |
| IDOR / BOLA | Authorization logic analysis | CWE-639 |
| Mass Assignment | API + model analysis | CWE-915 |
| Business Logic Flaws | Control flow + state analysis | CWE-840 |
| Race Conditions / TOCTOU | Concurrency + file op analysis | CWE-362, CWE-367 |
| Weak Cryptography | Algorithm + key analysis | CWE-327, CWE-326 |
| Hardcoded Secrets | Entropy + pattern detection | CWE-798 |
| Insecure Randomness | RNG API analysis | CWE-338 |
| Dependency CVEs | Manifest + version analysis | CWE-1035 |
| Information Disclosure | Error handling + logging analysis | CWE-209 |
| Security Misconfiguration | Config + header analysis | CWE-16 |
| IaC Misconfigurations | Dockerfile/K8s/Terraform analysis | CWE-732, CWE-284 |
| Memory Safety (C/C++) | Buffer + pointer analysis | CWE-120, CWE-416 |
| ReDoS | Regex complexity analysis | CWE-1333 |
| GraphQL Security | Query depth + introspection check | CWE-284 |
| React / Client-Side App Security | DOM sink + router + storage analysis | CWE-79, CWE-601, CWE-922 |
| Go Service Security | Handler + binding + timeout + goroutine analysis | CWE-89, CWE-918, CWE-400 |
| Java / JVM Service Security | Framework auth + binding + expression/ORM/parser analysis | CWE-89, CWE-94, CWE-502 |
| PHP Web Application Security | Framework auth + binding + SQL/template/file review | CWE-89, CWE-79, CWE-915 |
| Ruby Web Application Security | Callback/policy + strong-parameter + ORM/template review | CWE-89, CWE-79, CWE-915 |
| .NET Web Application Security | ASP.NET auth/binding + EF/Dapper/parser analysis | CWE-89, CWE-502, CWE-639 |
| Rust Web Service Security | Extractor + SQL/process/HTTP/file analysis | CWE-89, CWE-78, CWE-918 |
| Architecture Flaws | Trust boundary + tenant isolation analysis | CWE-284, CWE-862 |
| Application-Layer Vulns | Workflow + abuse-control analysis | CWE-639, CWE-840 |
| Infrastructure Security | Cloud IAM + network/runtime/storage posture | CWE-284, CWE-732 |
| Commit-diff scoped analysis | Changed-file taint + caller/callee tracing | CWE-all |

## Full analysis workflow

### Phase 0: Strategy (always run first)

Read `sub-skills/scan-strategy.md` to produce a concrete scan plan:
- Detected languages, frameworks, entry points
- Prioritized file list
- Active vulnerability categories
- Fresh or resume decision
- Whether the scan needs React, Go, Java/Kotlin JVM, PHP, Ruby, .NET, Rust, architecture, or application-vulnerability deep review

```bash
python3 scripts/scan.py --path <target> --status-only
```

If a recent incomplete run exists, ask whether to resume or start fresh.

```bash
python3 scripts/scan.py --path <target> [--lang python,javascript] [--exclude vendor,tests,node_modules]
```

This populates `workspace/scan_state.db` with candidate findings. Review the summary before proceeding.

---

### Phase 0A: Technology and architecture deep-review routing

Load these focused reviewers when the scan plan matches their trigger:

- `sub-skills/react-security-reviewer.md` — React, Next.js, Remix, React Router, JSX/TSX, browser tokens, client routing, postMessage, or hydration data.
- `sub-skills/go-security-reviewer.md` — Go `net/http`, Gin, Echo, Fiber, Chi, Gorilla, gRPC, workers, request binding, or Go server hardening.
- `sub-skills/java-security-reviewer.md` — Java/Kotlin JVM services using Spring, Jakarta EE/Servlet/JAX-RS, Struts, JSF, Hibernate/JPA, Micronaut, Quarkus, JVM messaging, or async workers. For Android, also load `mobile-security-reviewer.md`.
- `sub-skills/php-security-reviewer.md` — Laravel, Symfony, WordPress, Drupal, Yii, CodeIgniter, custom PHP front controllers, Composer applications, or PHP workers.
- `sub-skills/ruby-security-reviewer.md` — Rails, Sinatra/Rack, Hanami, Active Record/Sequel, Ruby templates, channels, or background jobs.
- `sub-skills/dotnet-security-reviewer.md` — ASP.NET Core/MVC/Web API, minimal APIs, Blazor, EF Core, Dapper, SignalR, or .NET workers.
- `sub-skills/rust-security-reviewer.md` — Actix-web, Axum, Warp, Rocket, SQLx/Diesel, Tokio services, or Rust workers processing untrusted data.
- `sub-skills/architecture-security-reviewer.md` — multi-service systems, SaaS/tenant boundaries, workers/queues, plugins/connectors, cloud trust boundaries, service accounts.
- `sub-skills/application-vuln-reviewer.md` — IDOR/BOLA, CSRF, account recovery, mass assignment, file upload/download, session lifecycle, rate limits, billing/workflow abuse.
- `sub-skills/infrastructure-security-reviewer.md` — cloud IAM, network exposure, object storage, KMS/secrets, runtime platforms, CI/CD supply chain, audit/logging, backups.

These reviewers do not replace taint analysis. Use them to expand the entry-point list, identify non-obvious sources/sinks, and add manual review targets before Phase 1.

---

### Phase 1: Taint and injection analysis (parallel)

Read `sub-skills/taint-analyzer.md`. Run per-file taint analysis:

```bash
python3 scripts/taint.py --file <path> --lang <language>
```

Use script output as a starting map. **Read every flagged file directly** and trace each candidate path step by step. Verify every taint path — source to sink — reading actual code at each hop. Interprocedural traces must follow function calls across file boundaries.

Covers: SQL injection, command injection, path traversal, XSS, SSRF, SSTI, XXE, deserialization, open redirect.

---

### Phase 2: Input validation analysis

Read `sub-skills/input-validator.md`. For every entry point identified in Phase 0:
- Verify validation is present and appropriate for the sink context
- Check for allowlist vs blocklist approach
- Test regex anchoring, type juggling bypasses, encoding bypasses
- Check second-order validation gaps

---

### Phase 3: Business logic and control flow analysis

Read `sub-skills/business-logic-analyzer.md` and `sub-skills/application-vuln-reviewer.md`. Analyze:
- Authentication and authorization decision points
- Workflow state machines (can steps be skipped or reversed?)
- Price/quantity/permission manipulation opportunities
- Race conditions and TOCTOU patterns
- Privilege escalation paths through indirect logic
- Account recovery, CSRF, rate limiting, upload/download, cache leakage, and session lifecycle gaps

---

### Phase 4: API security analysis

Read `sub-skills/api-security-reviewer.md`. For every REST, GraphQL, or RPC endpoint:
- Check for IDOR/BOLA (missing object-level authorization)
- Check for mass assignment in request body → model binding
- Check for excessive data exposure in responses
- Check rate limiting, authentication enforcement
- GraphQL: introspection, depth limits, batch query abuse

If the system has multiple services, tenants, workers, plugins, or cloud resources, also read `sub-skills/architecture-security-reviewer.md` and verify authorization, tenant scoping, and trust-boundary enforcement across the full request/job path.

---

### Phase 5: Authentication and authorization review

Read `sub-skills/auth-reviewer.md`. Examine:
- Authentication mechanisms and bypass paths
- Session management, fixation, expiry
- JWT/token construction and validation
- Authorization middleware — is it applied consistently?
- Privilege escalation and horizontal access control

---

### Phase 6: Cryptography and secrets review

Read `sub-skills/crypto-reviewer.md` and `sub-skills/secret-detector.md`.

Run entropy-based secret scanning:
```bash
python3 scripts/secrets.py --path <target>
```

Analyze:
- Algorithm selection (MD5/SHA1 for security, ECB mode, DES/RC4)
- Key sizes and generation
- Hardcoded credentials, API keys, tokens
- IV/nonce reuse, predictable keys
- Certificate validation bypasses

---

### Phase 7: Configuration and infrastructure security

Read `sub-skills/config-security-reviewer.md`, `sub-skills/iac-security-reviewer.md`, and `sub-skills/infrastructure-security-reviewer.md`.

Check:
- Security headers (CSP, HSTS, X-Frame-Options, CORS)
- Debug mode, verbose errors, stack traces in production
- TLS/SSL configuration
- Dockerfile, Kubernetes manifests, Terraform configs
- Cloud IAM policies, public storage buckets, open security groups
- Runtime platform posture, CI/CD deployment trust, KMS/secrets policy, audit logging, public snapshots/backups

---

### Phase 8: Memory safety (C/C++/Rust only)

Read `sub-skills/memory-safety-analyzer.md` when the codebase includes C, C++, or unsafe Rust.

Covers: buffer overflows, use-after-free, format string vulnerabilities, integer overflows in allocation sizes, null pointer dereferences.

---

### Phase 8A: Framework-specific review

When React/Next.js/TSX is present, read `sub-skills/react-security-reviewer.md` and verify client-side DOM XSS, open redirects, browser token storage, postMessage origin checks, hydration data leaks, and client-only authorization.

When Go is present, read `sub-skills/go-security-reviewer.md` and verify request body binding, SQL construction, command execution, SSRF, file access, template use, HTTP server timeouts, CORS, body limits, and concurrency races.

When a Java/JVM server stack is present, read `sub-skills/java-security-reviewer.md` and verify effective framework authorization, request/entity binding, SpEL/OGNL/EL, ORM query construction, deserialization/XML, outbound URL handling, archive/path safety, TLS/crypto, Actuator/admin exposure, logging, and async tenant/security-context propagation.

When PHP is present, read `sub-skills/php-security-reviewer.md` and verify route/middleware/capability authorization, request/model binding, raw ORM/SQL, template escape bypasses, wrappers and outbound URLs, redirects, uploads/archives, deserialization, debug surfaces, and job tenant context.

When Ruby is present, read `sub-skills/ruby-security-reviewer.md` and verify callbacks/policies, object and tenant authorization, strong parameters, raw ORM fragments, template escape bypasses, SSRF/redirect handling, uploads/archives, serialization, session configuration, and job context.

When a .NET web stack is present, read `sub-skills/dotnet-security-reviewer.md` and verify endpoint authorization, model binding/overposting, EF Core/Dapper/raw SQL, Razor/Blazor output, SSRF, redirects, files/uploads, XML/object deserialization, Data Protection, antiforgery, forwarded headers, and background-service tenant context.

When a Rust web stack is present, read `sub-skills/rust-security-reviewer.md` and verify extractor authorization, typed request limits, SQLx/Diesel/raw SQL, process execution, reqwest/hyper URL handling, files/uploads, templates/headers/redirects, serde parsing, unsafe/FFI boundaries, and task-local tenant context.

---

### Phase 9: Error handling and information disclosure

Read `sub-skills/error-handling-reviewer.md`. Check:
- Stack traces and exception details leaked to clients
- Verbose SQL errors, file path disclosure
- Enumeration through differential error messages
- Logging of sensitive data (passwords, tokens, PII)

---

### Phase 10: Dependency audit

```bash
python3 scripts/dependency.py --path <target>
```

Read `sub-skills/dependency-auditor.md` to assess exploitability of flagged packages. Check direct manifests and resolved lock state, including Python/Poetry/Pipenv, npm/Yarn/pnpm, Maven/Gradle catalogs and locks, Go modules and sums, Gemfile/Composer/Cargo locks, and NuGet project/central-package/lock/Paket files.

---

### Phase 11: False positive elimination

Read `sub-skills/false-positive-filter.md`. Apply three-pass protocol to **every** candidate:
1. Pass 1 — Source reachability: is the input genuinely user-controlled?
2. Pass 2 — Path completeness: does the taint path hold end-to-end?
3. Pass 3 — Exploitability: can an attacker realistically trigger this?

Only `confirmed` and `likely` findings survive to the report.

---

### Phase 12: Classification and scoring

Read `sub-skills/vuln-classifier.md`. For every surviving finding assign:
- CWE identifier
- OWASP Top 10 / OWASP API Top 10 category
- CVSS v3.1 base score and vector string
- Severity: `critical`, `high`, `medium`, `low`, `informational`

Update the database:
```bash
python3 scripts/scan.py --update-findings workspace/confirmed_findings.json
```

---

### Phase 13: Report generation

Read `sub-skills/report-generator.md`. The Phase 12 `--update-findings` command
automatically generates Markdown, HTML, JSON, SARIF, the canonical confirmed-
findings JSON, and `<target_path>/Vulnscan_results.md`. This is mandatory even
when the completed review has no findings; submit `[]` to Phase 12 so the valid
empty reports are still produced.

Verify that every finding contains Vulnerability Name, Severity,
Exploitability, CVSS Score, CVSS Vector, OWASP Category, Vulnerability
Description, Impact, Affected Assets, and Remediation Guidelines. It must also
include a stable Finding ID, CWE, confidence, validation status, exact
locations, masked evidence or taint flow, attack prerequisites, and references.

To regenerate the complete artifact set for the latest completed run:

```bash
python3 scripts/report.py --format all
```

Do not mark the review complete unless every artifact was written successfully.
The in-project Markdown file is the primary human-readable deliverable and must
always exist at the end of a full scan.

---

## Targeted scan commands

### `vulnscan taint <file>`

1. Read `sub-skills/taint-analyzer.md`.
2. Run: `python3 scripts/taint.py --file <file> [--lang <language>]`
3. Read the actual file and verify every path in the output.
4. Report confirmed paths with taint trace.

### `vulnscan secrets <path>`

1. Run: `python3 scripts/secrets.py --path <path>`
2. Read `sub-skills/secret-detector.md` to verify high-entropy hits.

### `vulnscan deps <path>`

1. Run: `python3 scripts/dependency.py --path <path>`
2. Read `sub-skills/dependency-auditor.md` to assess exploitability.

### `vulnscan config <path>`

1. Read `sub-skills/config-security-reviewer.md`.
2. Read `sub-skills/iac-security-reviewer.md`.
3. Review all config, infra, and environment files in the path.

### `vulnscan status`

```bash
python3 scripts/scan.py --status-only
```

---

## Natural-language prompt examples

- `Scan this codebase for vulnerabilities`
- `Find SQL injection and XSS in this Flask app`
- `Check for hardcoded secrets or weak crypto`
- `Audit the authentication and authorization logic`
- `Are there any vulnerable dependencies?`
- `Check the taint flow from HTTP params to database calls`
- `Find command injection in this Node.js app`
- `Review the Dockerfile and Kubernetes configs for security issues`
- `Check the API endpoints for IDOR and mass assignment`
- `Find any race conditions or business logic flaws`
- `Find React/Next.js client-side vulnerabilities`
- `Review this Go API for handler, binding, SSRF, and SQL injection flaws`
- `Review this Spring Boot or Jakarta EE service for JVM-specific vulnerabilities`
- `Review this Ktor service for Kotlin/JVM request-to-sink vulnerabilities`
- `Review this Laravel, Symfony, or WordPress application for framework-specific vulnerabilities`
- `Review this Rails or Sinatra application for authorization, strong-parameter, and ORM flaws`
- `Review this ASP.NET Core API for authorization, overposting, EF Core, and SSRF flaws`
- `Review this Axum or Actix-web service for extractor, SQL, process, and HTTP-client flaws`
- `Look for architecture and tenant-isolation vulnerabilities`
- `Find application-level vulns like account recovery, CSRF, upload, cache, and workflow abuse`
- `Review cloud infrastructure, IAM, storage, network exposure, and CI/CD deployment security`
- `Give me a full security report in SARIF format`

---

## Reference files

- `sub-skills/scan-strategy.md`
- `sub-skills/taint-analyzer.md`
- `sub-skills/input-validator.md`
- `sub-skills/business-logic-analyzer.md`
- `sub-skills/application-vuln-reviewer.md`
- `sub-skills/api-security-reviewer.md`
- `sub-skills/react-security-reviewer.md`
- `sub-skills/go-security-reviewer.md`
- `sub-skills/java-security-reviewer.md`
- `sub-skills/php-security-reviewer.md`
- `sub-skills/ruby-security-reviewer.md`
- `sub-skills/dotnet-security-reviewer.md`
- `sub-skills/rust-security-reviewer.md`
- `sub-skills/architecture-security-reviewer.md`
- `sub-skills/infrastructure-security-reviewer.md`
- `sub-skills/auth-reviewer.md`
- `sub-skills/crypto-reviewer.md`
- `sub-skills/secret-detector.md`
- `sub-skills/config-security-reviewer.md`
- `sub-skills/iac-security-reviewer.md`
- `sub-skills/memory-safety-analyzer.md`
- `sub-skills/error-handling-reviewer.md`
- `sub-skills/dependency-auditor.md`
- `sub-skills/vuln-classifier.md`
- `sub-skills/false-positive-filter.md`
- `sub-skills/report-generator.md`
- `resources/references/cwe-taxonomy.md`
- `resources/references/owasp-top10.md`
- `resources/references/false-positive-guide.md`

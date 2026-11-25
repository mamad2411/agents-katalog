---
name: securityaudit
description: Run a deep, evidence-based (secure code review, adversarial or blackhat-style assessment, threat modelling, cryptography, credential hygiene, memory safety, dependency and configuration review, denial-of-service analysis, frontend robustness, application security and security-focused code hardening) security audit of a software project, or repair confirmed findings when invoked with --fix. Fix mode applies evidence-backed repairs in Git, runs appropriate tests, and commits successful fixes while preserving existing functionality.
x-alice-class: ai
---# Security Audit

## Core Rules

- Act as a senior application security engineer, secure code reviewer, cryptographer, threat modeller, abuse-case tester, and pragmatic maintainer.
- Adopt a paranoid, assume-breach posture: treat every network as hostile, every input as attacker-controlled, every dependency as potentially compromised, and every trust assumption as unproven until the code demonstrates it. Aim for the standard "would this survive a motivated, well-resourced attacker with time" rather than "does this pass a scan".
- Paranoia governs what you *look for*, not what you *claim*. Never omit a plausible issue because it feels unlikely — record it and let severity and confidence ratings carry the uncertainty. Equally, never inflate: tie every finding to concrete evidence from files, functions, routes, dependencies, configuration values, behaviours, or architectural decisions.
- Use an adversarial "blackhat hacker" lens safely: think like a hostile attacker trying to exploit, DoS, bypass, persist, pivot, exfiltrate, or abuse business logic, but keep all testing local, authorised, non-destructive, and evidence-based.
- Review the entire project deeply and sceptically. Do not invent files, routes, code, dependencies, or findings. If line numbers are unavailable, identify the nearest function, block, route, or configuration key.
- Create an `audits/` folder at the project root if it does not exist. Write all audit artifacts there.
- Save the security report as `audits/YYYYMMDD-HHII-securityAudit.md`, using the current local system date and time. Use four-digit 24-hour time, e.g. `audits/20260131-1427-securityAudit.md`.
- Also save a functionality and next-steps report as `audits/YYYYMMDD-HHII-functionalityNextSteps.md` with the same timestamp as the security report.
- If a class of issue was checked and not found, mention that briefly — a clean result is evidence, and it distinguishes "verified absent" from "not examined".
- Keep snippets short and focused.

## Project Preparation and Git Safety

Before auditing or fixing:

- Identify the project root and check whether it is inside a git repository with `git rev-parse --show-toplevel`.
- If a git repository exists, inspect the working tree before editing or creating commits. Do not overwrite, revert, or discard user changes.
- If no git repository exists:
  - Initialize a new git repository in the project root.
  - Create or update `.gitignore` with conservative, codebase-appropriate entries before staging anything.
  - Preserve any existing `.gitignore` content. Add missing entries rather than replacing useful project-specific rules.
  - Include common local-only files, secrets, caches, logs, editor/OS files, generated build outputs, dependency directories regenerated from lockfiles, test coverage, temporary files, local databases, and tool caches.
  - Do not ignore source files, migrations, lockfiles, documentation, infrastructure-as-code, or other reproducible project assets unless the codebase clearly treats them as generated.
  - Check for obvious high-confidence secrets or private key material that would be staged. If present, explain the issue and stop before creating the initial commit.
  - Stage the initial project state and create an initial commit, e.g. `chore: initial project snapshot`.
  - If repository initialization, `.gitignore` creation, staging, or committing fails, explain the issue and stop before making audit fixes or broader changes.

Normal audit mode may create the git bootstrap commit if no repository exists and may create files under `audits/`. It must not otherwise modify application code, configuration, tests, dependency files, or deployment files.

## Execution Modes

### Normal Audit Mode

Use this mode unless the user explicitly includes `--fix`.

- Perform the full security, cryptography, secrets-hygiene, memory-safety, DoS, abuse-case, code-quality, frontend robustness, dependency, configuration, and operational review.
- Write both reports under `audits/`.
- Do not change application code, configuration, tests, dependency files, or deployment files.
- Use recommendations, safer examples, and suggested tests in the reports rather than applying changes.

### Fix Mode (`--fix`)

Use this mode only when the user explicitly invokes `securityaudit --fix` or otherwise includes the `--fix` flag with the security audit request.

- Complete the Project Preparation and Git Safety workflow first. If no git repository exists, initialize it, create/update `.gitignore`, and create the initial commit before making fixes.
- Inspect the working tree before editing. Do not overwrite or revert user changes. If unrelated changes exist, work around them; if they block safe fixes, explain the conflict.
- Identify real, evidence-backed security, DoS, robustness, frontend, or code-quality issues before fixing them. Do not make speculative hardening changes without tying them to a finding or clearly evidenced maintainability defect.
- Fix each confirmed issue with the smallest safe change that addresses the root cause while preserving existing behaviour.
- Improve badly written, fragile, duplicated, or error-prone code only when the improvement reduces a concrete risk, prevents breakage, improves error handling, or makes a confirmed fix safe to maintain.
- Add or update regression tests where practical. Include negative, abuse-case, boundary, and frontend interaction tests when relevant.
- For HTML and JavaScript changes, verify that user-visible events fire, async failures are handled, errors do not break subsequent scripts, and useful non-sensitive diagnostics go to the console.
- After each logical fix or tightly related group of fixes, run the most relevant tests or checks for that change. Prefer targeted tests first, then broader suites when risk warrants it.
- Commit only after tests/checks pass. If tests fail, do not commit; either repair the failure and retest or report the blocker.
- Use clear security- or robustness-focused commit messages, e.g. `fix: enforce webhook signature validation` or `fix: zeroize database credentials after connection setup`.
- When fixing cryptographic weaknesses, upgrade to current best practice (see Cryptography Review). Where the project controls both ends of a protocol, prefer hybrid post-quantum schemes when the platform supports them. Where a cryptographic fix would break compatibility (stored ciphertexts, existing tokens, external peers, password hashes), stop and ask the user for consent first, briefly explaining the change, the benefit, the migration path, and what may break.
- If a finding cannot be fixed safely in the current context, leave it uncommitted and document the reason, risk, and next step.
- At the end, summarize commits created, tests run, findings fixed, findings left open, generated audit files, and any residual risk.

## Adversarial Methodology

Use a two-pass approach:

1. Map the system as an attacker would.
   - Identify trust boundaries, entry points, exposed routes, auth gates, roles, state transitions, background jobs, queue consumers, file parsers, webhooks, third-party integrations, storage layers, admin/debug features, and deployment exposure.
   - Trace unauthenticated, low-privilege, cross-tenant, cross-origin, public file, and machine-to-machine paths first.
   - Look for ways to turn benign features into abuse primitives: enumeration, replay, over-posting, confused deputy, privilege escalation, data scraping, quota bypass, workflow bypass, SSRF, lateral movement, and persistence.
   - Include post-compromise perspectives: what does an attacker gain from a stolen backup, a core dump, a compromised dependency, a leaked log archive, read access to the box, or one leaked key? Defence in depth findings belong in the report even when the outer wall currently holds.
2. Validate defensively from the code.
   - Tie every plausible attack path to concrete implementation evidence.
   - Prefer safe local proof-of-concept inputs, reproduction steps, or unit-test-shaped examples.
   - State what would be required to exploit the issue and what evidence would raise or lower confidence.

## Cryptography Review

Review all cryptographic use as a senior cryptographer. Custom or hand-rolled cryptography is a finding by default — the burden of proof is on the implementation.

- Algorithms and modes: flag MD5/SHA-1 in any security context, DES/3DES/RC4/Blowfish, ECB mode, unauthenticated CBC, RSA PKCS#1 v1.5 encryption, RSA < 2048 bits, EC curves weaker than P-256/X25519, and any bespoke construction. Prefer AEAD (AES-256-GCM, ChaCha20-Poly1305) for encryption and SHA-256/SHA-3/BLAKE2+ for hashing.
- Nonces and IVs: verify every nonce/IV is unique per key. Treat static, hardcoded, counter-reset-prone, or randomly generated GCM nonces without rotation-limit awareness (2^32 messages for random 96-bit nonces) as findings — GCM nonce reuse is catastrophic. Check IVs are not derived from predictable data and never reused with CBC.
- Randomness: all keys, tokens, session IDs, nonces, salts, password-reset codes, and OTPs must come from a CSPRNG (`crypto/rand`, `secrets`, `crypto.getRandomValues`, `SecureRandom`, getrandom). Flag `Math.random`, `rand()`, `random.random()`, `java.util.Random`, time-seeded PRNGs, and truncated randomness that reduces entropy below ~128 bits.
- Password storage: require a memory-hard or cost-parameterised hash — Argon2id (preferred), scrypt, or bcrypt — with current-generation parameters. Flag plain or salted SHA-x/MD5, missing salts, shared salts, low iteration/cost factors, and truncation issues (bcrypt's 72-byte limit with long inputs or pre-hashing pitfalls).
- Key derivation: HKDF (or equivalent) for deriving keys from keys; PBKDF2/Argon2 for deriving keys from passwords. Flag raw hashing of secrets to make keys, key reuse across purposes (encrypt vs MAC vs sign), and passwords used directly as keys.
- Constant-time behaviour: MAC checks, signature verification, token comparison, and password-hash verification must use constant-time comparison (`hmac.compare_digest`, `crypto.timingSafeEqual`, `subtle.ConstantTimeCompare`). Flag `==`/`===`/`strcmp`/early-exit loops on secret material, and observable timing/error differences that create padding-oracle or user-enumeration channels.
- Signatures and tokens: check JWT handling for `alg: none`, HS/RS confusion, missing `alg`/`iss`/`aud`/`exp` validation, and verify-after-decode ordering. Check webhook and cookie signatures for signature stripping, canonicalisation ambiguity, and truncated MACs. Verify signatures before parsing or acting on payloads.
- TLS: minimum TLS 1.2 (prefer 1.3), certificate and hostname verification never disabled (`verify=False`, `rejectUnauthorized: false`, `InsecureSkipVerify: true`, custom trust-all managers are all findings, including in "internal" or test-reachable code paths), no cleartext fallbacks, HSTS where applicable.
- Key management: flag hardcoded keys, keys committed to the repo or baked into images, world-readable key files, absent rotation strategy for long-lived keys, and encryption keys stored beside the data they protect. Check for envelope encryption/KMS use where the platform provides it.
- Post-quantum readiness: assess harvest-now-decrypt-later exposure — data encrypted today whose confidentiality must outlive the advent of cryptographically relevant quantum computers. Where the project controls both endpoints and the stack supports it, recommend hybrid key exchange (e.g. X25519 + ML-KEM-768) and note ML-DSA/SLH-DSA for long-lived signatures. Where PQC is already used, verify it is a genuine hybrid or standardised scheme (FIPS 203/204/205), that failure does not silently fall back to classical-only, that implementations come from maintained libraries rather than hand-rolled code, and that key/ciphertext sizes and encapsulation results are validated. Do not recommend PQC where it would break interop with systems the project does not control — record it as accepted residual risk instead.

## Secrets and In-Memory Credential Hygiene

Audit the full lifecycle of every credential, key, token, and other secret: acquisition → storage → use → propagation → destruction. A secret is exposed for as long as any copy of it exists anywhere.

### At rest and in configuration

- Search for hardcoded secrets in source, tests, fixtures, git history, comments, and sample configs. Verify `.env`/credential files are gitignored and not baked into Docker images via `COPY`, `ENV`, or build args (build args persist in image history).
- Prefer secret managers/keychains/OS keystores over plaintext files; where files are unavoidable, check permissions (0600), ownership, and encryption at rest.
- Check secrets are not written to logs, error messages, stack traces, crash reports, analytics/telemetry (e.g. Sentry breadcrumbs and request bodies), serialized session stores, caches, backups, or debug output. Check `toString`/`repr`/`Debug`/serialisation of config and credential objects does not embed secret fields — require redaction or field exclusion.

### In transit and between processes

- Flag secrets in URLs or query strings (they land in access logs, proxies, browser history, and Referer headers), in GET request bodies cached by intermediaries, and in headers logged by middleware.
- Flag secrets passed as command-line arguments (visible in `ps`/`/proc/*/cmdline` to other local users) and note that environment variables leak via `/proc/self/environ`, crash dumps, CI logs, `docker inspect`, and inheritance by every child process. Prefer file-based or socket-based secret delivery with tight permissions where the platform allows.

### In memory

This is a mandatory check, not an optional extra. For every long-lived secret held by the application (master keys, DB passwords, API keys, signing keys, user passwords in flight):

- Minimise lifetime and copies: the secret should be read as late as possible, held in as few places as possible, and destroyed as soon as it is no longer needed. Flag secrets parked in global variables, config singletons, or framework contexts for the life of the process when they are only needed at startup (e.g. a DB password still resident after the connection pool is established).
- Zeroization: in native code, require `explicit_bzero`/`memset_s`/`SecureZeroMemory`/`sodium_memzero` — plain `memset` before `free` is often elided by the optimiser and is a finding. In Rust, look for the `zeroize` crate / `ZeroizeOnDrop` on key material. Flag secret buffers freed or dropped without wiping.
- Immutable-string trap: in GC languages (Java, C#, Python, JavaScript, Go strings), immutable strings cannot be wiped and may be interned, copied by the GC, or retained until collection. Prefer mutable containers wiped after use — `char[]`/`byte[]` with `Arrays.fill` in Java, `bytearray` in Python, `[]byte` in Go, `Buffer.fill(0)` in Node. Report string-typed key material as a finding with honest caveats: GC copying means wiping is best-effort in managed runtimes, so the primary control is shortening lifetime and reducing copies.
- Swap and dumps: for high-value keys in native/systems code, check for `mlock`/`VirtualLock` to keep pages out of swap and `madvise(MADV_DONTDUMP)`/`RLIMIT_CORE=0`/`prctl(PR_SET_DUMPABLE, 0)` to keep them out of core dumps. In managed runtimes, check that heap-dump and diagnostic endpoints are not exposed: Spring Boot `/actuator/heapdump` and `/actuator/env`, Go `net/http/pprof` on public listeners, Node `--inspect` in production, PHP `phpinfo()`, Rails/Django debug pages. Any endpoint that can serialise process memory or environment is an instant secret-disclosure path.
- Crash and error paths: verify exception handlers, panic recovery, and crash reporters do not capture locals, request bodies, or headers containing credentials.
- Libraries: prefer secret-aware wrappers where the ecosystem offers them (e.g. `zeroize`/`secrecy` in Rust, libsodium `sodium_mlock`ed buffers, JCA key handles, OS keychains) so keys live in protected memory rather than ordinary heap allocations.
- Rate severity honestly: memory-scraping generally requires local code execution or a memory-disclosure bug, so pure in-memory findings are usually Medium/Low as defence-in-depth — unless combined with an exposure path found above (heap-dump endpoint, swap on shared hosts, core dumps shipped to third-party crash services), which upgrades them sharply.

## Memory, CPU, and Resource Safety

### Memory safety (native and FFI code)

Where C, C++, Rust `unsafe`, cgo, JNI, ctypes, N-API, or other native/FFI boundaries exist:

- Check for buffer overflows/underflows, off-by-one errors, unchecked length arithmetic, integer overflow/underflow feeding allocations or indexing, format-string bugs, use-after-free, double free, uninitialised memory reads, and type confusion.
- Audit every `unsafe` block in Rust for justification and soundness invariants; audit FFI boundaries for ownership, lifetime, and error-code handling mismatches.
- Verify attacker-influenced sizes and offsets are bounds-checked before allocation and copy operations; flag `strcpy`/`sprintf`/`gets`-class APIs and unchecked `memcpy` lengths.
- Check parsers of untrusted input (file formats, protocols, decompressors) for length-prefix trust, recursion depth, and allocation-before-validation patterns.

### Resource exhaustion (all languages)

- Flag unbounded in-memory growth reachable from input: caches and maps without eviction, per-request buffering of entire bodies/files/results instead of streaming, unbounded queues, listener/subscription leaks, and connection pools without limits.
- Flag CPU amplification: catastrophic regex backtracking (ReDoS) on user input, hash-flooding via attacker-chosen keys, algorithmic complexity attacks (quadratic parsers, unbounded sorts/joins), and expensive cryptographic operations (bcrypt/argon2 verification, signature checks) reachable pre-authentication without rate limiting.

## Deep DoS Review

For every public endpoint, parser, import/export path, search/filter/sort path, file upload, webhook, background worker, scheduled task, retry loop, and integration:

- Identify attacker-controlled inputs that influence CPU, memory, disk, network, database, queue depth, lock duration, recursion depth, fan-out, retries, or cache keys.
- Look for unbounded request bodies, uploads, decompression (zip/gzip bombs, nested archives), pagination, sorting, joins, regular expressions, recursion, loops, promise/task creation, goroutines/threads, retries, timeouts, and response sizes.
- Check N+1 query patterns, expensive authorization checks, cache-bypass keys, lock contention, thundering-herd behaviour, idempotency gaps, queue flooding, retry storms, and algorithmic complexity attacks.
- Check infrastructure limits: reverse proxy body limits, app server timeouts, DB pool sizes, worker concurrency, memory/CPU limits, rate limits, autoscaling assumptions, and circuit breakers.
- For each credible DoS vector, include a safe trigger example, likely resource impact, required attacker capability, and concrete resource-control fix.

## Code Quality and Functionality Review

In both modes, review code quality as a reliability and security input:

- Identify fragile or badly written code that increases security or operational risk: duplicated validation, inconsistent auth checks, swallowed errors, overly broad exception handling, ambiguous state transitions, hidden global state, unsafe defaults, poor input normalization, magic strings, dead code, race-prone code, and hard-to-test complexity.
- Distinguish style preferences from risk-bearing defects. Report only issues that affect correctness, resilience, maintainability of security controls, user-facing behaviour, or safe future change.
- In fix mode, improve the smallest area necessary to reduce the risk while preserving existing behaviour and public APIs.
- Add tests or checks before/after refactors when behaviour preservation is non-trivial.

## HTML and JavaScript Review

When HTML, JavaScript, TypeScript, templates, or browser-facing code exists:

- Verify that scripts load in the intended order and do not fail the whole page when one feature errors.
- Check that selectors match existing DOM nodes, event listeners are attached after elements exist, dynamically inserted controls receive handlers, and forms/buttons/links fire the expected events.
- Exercise key interactions when a local app can run: forms, navigation, modals, uploads, filters, destructive actions, auth/logout, and async flows.
- Inspect browser console output when possible. Treat uncaught exceptions, unhandled promise rejections, missing assets, blocked requests, and failed event handlers as findings or next-step defects.
- Ensure errors are handled with user-safe behaviour and useful non-sensitive `console.debug`, `console.warn`, or `console.error` context for developers.
- Do not log credentials, tokens, session IDs, personal data, sensitive request bodies, or full server responses that may contain secrets. Check that tokens are not parked in `localStorage`/`sessionStorage` when HttpOnly cookies would do, and that in-page secrets are not reachable by third-party scripts.
- Check browser security issues: DOM XSS, unsafe `innerHTML`, template injection, open redirects, insecure postMessage, CSRF, CORS assumptions, clickjacking, mixed content, insecure cookies, missing security headers, and supply-chain exposure from third-party script tags without SRI.

## Review Scope

Inspect all relevant project surfaces, including:

- Application source code, tests, build scripts, package manifests, lockfiles, and CI/CD configuration.
- Infrastructure and deployment files such as Dockerfiles, Compose, Kubernetes, Terraform, Ansible, Helm, cloud config, and environment examples.
- Authentication, authorisation, session, cookie, token, cache, cryptography, key management, secret storage, logging, monitoring, and error handling code.
- API routes, controllers, handlers, jobs, workers, queues, scheduled tasks, webhooks, integrations, database access, migrations, file upload, and file processing paths.
- Input validation, output encoding, CORS, CSRF, security headers, rate limiting, throttling, timeouts, retries, pagination, body-size limits, and resource controls.
- Frontend templates, HTML, JavaScript/TypeScript, route transitions, event handlers, async flows, error boundaries, console diagnostics, and browser build configuration.
- Admin, debug, development-only, diagnostic, and operational functionality exposed by code or configuration (including profilers, heap-dump endpoints, and metrics listeners).
- Tests and test fixtures, especially where they reveal intended security, auth, validation, error, and abuse-case behaviour.

## Issue Categories

Look specifically for these categories, but do not limit the audit to them:

- Authentication: missing or weak authentication, insecure password/reset flows, session fixation, token leakage, weak remember-me logic, missing MFA for sensitive flows.
- Authorisation: IDOR, broken access control, privilege escalation, missing ownership checks, tenant isolation failures, role bypasses, admin route exposure.
- Injection: SQL, NoSQL, command, LDAP, template, header, log, path traversal, unsafe deserialisation, SSRF, XXE, prototype pollution.
- Browser-side risks: XSS, CSRF, CORS misconfiguration, clickjacking, insecure cookies, missing security headers, DOM injection, unsafe postMessage, open redirects.
- API risks: missing validation, excessive data exposure, mass assignment, unsafe pagination, missing rate limits, weak errors, unsafe webhooks, replay risks, missing idempotency.
- Denial-of-service: unbounded queries, request bodies, pagination, regex backtracking, infinite loops, recursion, memory or CPU exhaustion, file upload abuse, decompression bombs, queue flooding, lock contention, retry storms, missing timeouts, N+1 attack vectors, cache bypass, algorithmic complexity attacks.
- Memory safety: buffer overflows, use-after-free, double free, integer overflow feeding allocation or indexing, format strings, unsound `unsafe`/FFI code, allocation-before-validation in untrusted parsers.
- Data protection and privacy: secrets, sensitive data or PII leakage, unsafe logs/errors/backups, weak retention, missing encryption in transit or at rest where relevant.
- Secrets hygiene: hardcoded or repo-committed secrets, secrets in env vars/args/URLs/logs/images, plaintext key files, secret-bearing debug endpoints, unwiped or long-lived secrets in memory, secrets captured by crash reporters or heap dumps.
- Cryptography: weak or misused algorithms, nonce/IV reuse, non-constant-time comparisons, hardcoded keys, predictable tokens, insecure randomness, weak password hashing, missing key rotation, bad signatures/salts/KDF parameters, disabled TLS verification, JWT algorithm confusion, missing post-quantum consideration for long-lived confidentiality.
- Dependency and supply chain: vulnerable, unpinned, suspicious, deprecated, or confused dependencies; unsafe build scripts; insecure package sources; CI/CD secret exposure; install-time script risk.
- Infrastructure and deployment: insecure images, root containers, excessive capabilities, missing resource limits, network exposure, default credentials, debug mode, verbose production errors, TLS issues, health/readiness gaps, overly permissive IAM/RBAC/file permissions/service accounts.
- Business logic: race conditions, TOCTOU, payment/credit manipulation, workflow bypass, replay, abuse of invitation/referral/voucher/discount/reward systems, state machine bypasses, missing audit trails.
- Frontend robustness: broken event handlers, uncaught exceptions, unhandled promise rejections, stale selectors, silent async failures, missing user-safe fallback states, sensitive debug logs.
- Code quality risk: security-critical duplication, fragile parsing, inconsistent normalization, dead or unreachable security checks, overly broad exception handling, poorly isolated side effects, missing invariants.
- Test gaps: missing security, negative, abuse-case, boundary, frontend interaction, and regression tests.

## Finding Requirements

For every finding include:

- Finding ID, title, severity (`Critical`, `High`, `Medium`, `Low`, or `Informational`), and confidence (`High`, `Medium`, or `Low`).
- Affected files and line numbers where possible.
- Affected component, route, function, class, service, job, dependency, frontend interaction, or deployment control.
- Clear explanation, why it matters, exploitability, potential impact, concrete exploit/trigger example, and safe proof-of-concept or reproduction steps where appropriate.
- Recommended fix, safer code/configuration example where practical, and suggested tests.
- Relevant CWE, OWASP ASVS, OWASP Top 10, OWASP API Security Top 10, or similar mapping where applicable.
- Assumptions, limitations, and uncertainty.

## Security Report Structure

Write the final Markdown security report with these sections:

1. `# Security Audit Report`
2. `## 1. Executive Summary` - overall posture, highest-risk issues, urgent fixes, architectural concerns.
3. `## 2. Scope Reviewed` - languages, frameworks, services, config, deployment files, dependency manifests, tests.
4. `## 3. Methodology` - static review, dependency review, configuration review, threat modelling, adversarial attack-surface mapping, cryptography review, secrets-lifecycle review, memory-safety review, DoS analysis, frontend review, test review.
5. `## 4. Risk Rating Method` - how severity and confidence were assigned.
6. `## 5. Attack Surface Map` - entry points, trust boundaries, exposed roles, data stores, external integrations, and attacker starting positions.
7. `## 6. Findings Summary Table` - Markdown table with `ID`, `Severity`, `Confidence`, `Title`, `Component`, `Status`; use `Open` unless already fixed in fix mode.
8. `## 7. Detailed Findings` - one subsection per finding using the detailed structure below.
9. `## 8. Blackhat-Style Abuse Paths` - realistic chained attack paths, prerequisites, limits, and defensive breakpoints.
10. `## 9. Denial-of-Service and Resource Exhaustion Review`
11. `## 10. Cryptography and Key Management Review` - algorithms, randomness, key lifecycle, TLS posture, and post-quantum readiness, including clean results.
12. `## 11. Secrets Lifecycle and In-Memory Credential Review` - secrets at rest, in transit, in configuration, and in memory; exposure paths (dumps, swap, logs, debug endpoints); zeroization and lifetime findings.
13. `## 12. Memory and Resource Safety Review` - native/FFI memory safety and unbounded resource growth, or a brief note that no native surface exists.
14. `## 13. Dependency and Supply-Chain Review`
15. `## 14. Authentication and Authorisation Review`
16. `## 15. Input Validation and Output Encoding Review`
17. `## 16. Frontend HTML/JavaScript Robustness Review`
18. `## 17. Infrastructure and Deployment Review`
19. `## 18. Logging, Monitoring, and Error Handling Review`
20. `## 19. Test Coverage and Security Regression Gaps`
21. `## 20. Prioritised Remediation Plan` - Immediate, short-term, medium-term, and long-term fixes.
22. `## 21. False Positives / Needs Manual Verification`
23. `## 22. Final Notes` - residual risk and limitations.

For each detailed finding, use:

```markdown
### Finding ID: [ID]

#### Title

#### Severity

#### Confidence

#### Affected Files / Components

#### Description

#### Evidence

#### Attack Scenario

#### Impact

#### Recommendation

#### Safer Example

#### Suggested Tests

#### References

#### Assumptions / Limitations
```

## Functionality and Next-Steps Report Structure

Write a separate Markdown report focused on improving the project beyond immediate security remediation:

1. `# Functionality and Next Steps Report`
2. `## 1. Executive Summary` - highest-impact functionality, reliability, maintainability, and user-experience opportunities.
3. `## 2. Current Functional Risks` - broken or fragile behaviours, brittle code paths, frontend event risks, missing error handling, and likely user-impacting issues.
4. `## 3. Code Quality Improvements` - badly written or hard-to-maintain areas, why they matter, and safe refactor steps.
5. `## 4. Frontend Interaction and Error-Handling Improvements` - event firing, async handling, console diagnostics, and user-safe fallback recommendations.
6. `## 5. Testing Roadmap` - unit, integration, end-to-end, abuse-case, frontend interaction, regression, load, and smoke tests to add.
7. `## 6. Recommended New Functionality` - evidence-backed features that fit the existing project and would improve usefulness, safety, operability, or user outcomes.
8. `## 7. Next-Level Opportunities` - larger architectural, product, observability, automation, performance, accessibility, developer-experience, or operational improvements.
9. `## 8. Prioritised Action Plan` - immediate, short-term, medium-term, and long-term actions with rationale and risk.
10. `## 9. Caveats and Validation Needed` - assumptions, manual checks, user research, or runtime validation that should happen before major changes.

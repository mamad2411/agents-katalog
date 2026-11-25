---
name: harden-ready
description: "Verify a deployed app survives adversarial attention and prove it to an auditor. Owns post-deploy adversarial review, OWASP Top 10 systematic walkthroughs (Web / API / LLM), compliance mapping (SOC 2 CC, HIPAA 164.312, PCI-DSS 4.0, GDPR Article 32) with control-to-code evidence, pen-test preparation and retest discipline, responsible-disclosure program design beyond SECURITY.md, and class-not-instance post-incident hardening. Refuses scanner-first security (the Snyk-passed-but-front-door-exploitable pattern), paper trust boundaries (declared in docs, absent in code), hardening-as-ritual (annual pen test, nothing between), compliance-without-security (checklist green, app still vulnerable), shallow-audit traps (only finds what tools surface), and CVE-of-the-week patching. Triggers on 'adversarial review,' 'pen-test prep,' 'OWASP walkthrough,' 'SOC 2 / HIPAA / PCI-DSS / GDPR gap check,' 'responsible disclosure,' 'bug bounty,' 'post-incident hardening,' 'security review before launch.' Does not build the app (production-ready), deploy it (deploy-ready), monitor it (observe-ready), pick the tool (stack-ready), or own repo-hygiene security (repo-ready). Pairs with deploy-ready, observe-ready, launch-ready. Full trigger list in README."
version: 3.1.0
updated: 2026-11-23
changelog: CHANGELOG.md
suite: ready-suite
tier: shipping
upstream:
  - architecture-ready
  - production-ready
  - deploy-ready
  - observe-ready
  - repo-ready
downstream: []
pairs_with:
  - deploy-ready
  - observe-ready
  - launch-ready
compatible_with:
  - claude-code
  - codex
  - cursor
  - windsurf
  - antigravity
  - pi
  - openclaw
  - any-agentskills-compatible-harness
---

# Harden Ready

This skill exists to solve one specific failure mode. An AI-generated web application is deployed, monitored, and green on observe-ready. The SAST vendor's dashboard shows zero criticals. The SCA scan is clean. The repo has a SECURITY.md with a contact email. The founder is preparing a SOC 2 Type I report for an enterprise prospect. The front page of the application, accessed with a throwaway account, leaks every other tenant's records through an object ID that increments by one. The Supabase anon key in the JavaScript bundle allows a curl request to read and write arbitrary tables because the generator emitted RLS-capable schemas without RLS policies. The OAuth callback accepts any state parameter. The JWT verification code has `alg: none` as a permitted value because it was copied from a Stack Overflow answer in 2019. The system prompt is visible in the browser's network tab. None of this fires an alarm anywhere in the stack. The app passes every automated check and fails the adversary on the first touch.

This is not a hypothetical composite. In March-May 2025, researcher Matt Palmer sampled Lovable-generated applications and found approximately 70% had row-level security disabled entirely; 170 of 1,645 sampled apps exposed personal data to unauthenticated readers. NVD assigned CVE-2025-48757: "Insufficient database Row-Level Security (RLS) policy in Lovable through 2025-04-15 allows remote unauthenticated attackers to read or write to arbitrary database tables." In July 2025, a Replit AI coding agent executed destructive database commands against a production system during an explicit code-freeze, erasing records on 1,206 executives and over 1,196 companies, and then fabricated the claim that the data was unrecoverable. Veracode's 2025 GenAI Code Security Report tested over 100 LLMs across Java, Python, C#, and JavaScript: 45% of AI-generated code samples contained at least one OWASP Top 10 vulnerability, 86% failed to defend against XSS, 88% failed to defend against log injection. Snyk's 2025 study found that 80% of developers admitted bypassing security policies on AI-generated code; under 25% ran SCA on it. HackerOne's 2025 year-review reported a 540% year-over-year increase in prompt-injection bounty findings. The research catalog is in [`references/RESEARCH-2026-04.md`](references/RESEARCH-2026-04.md).

harden-ready's job is the opposite of the scanner-first posture that produced these outcomes. Given a deployed app that passed every tool, it runs the adversarial review the tools do not run. It walks the OWASP Top 10 (Web, API, and LLM variants) by hand against the actual running system. It tests the trust boundaries the architecture diagram declares. It maps every compliance control the auditor will ask about to the specific code file, configuration, or runtime evidence that implements it. It prepares the pen test. It runs the retest. It stands up the disclosure program and its triage SLA. When an incident lands, it hardens the class of weakness, not the instance. If a hardening pass cannot answer "would this survive an auditor with a checklist and an attacker with a laptop," it is not a hardening pass; it is security theater.

This is harder than it sounds because security bleeds into everything. The app, the auth, the cryptography, the supply chain, the CI pipeline, the deploy targets, the monitoring, the on-call rotation, the disclosure email inbox, and the compliance evidence binder are each separate surfaces that a single coordinated attacker probes in the same hour. The skill's scope fence (Section "When this skill does NOT apply") is more aggressive than any sibling in the ready-suite because of this: production-ready owns the pre-build security primitives, repo-ready owns the hygiene controls, deploy-ready owns secrets wiring, observe-ready owns security event detection. harden-ready owns the adversarial verification on top of all of them. If the skill starts rewriting auth, recoding RBAC, or reconfiguring monitoring, it has drifted into a sibling's lane and the suite collapses.

## Core principle: every compliance claim and every scanner finding is verified by an adversarial read, or it is refused

The load-bearing discipline is that a security posture is what an attacker cannot do, not what a tool reports, what a checklist claims, or what a policy declares. harden-ready enforces:

> Every compliance control is mapped to a specific file, configuration, or log artifact that implements it. Every scanner finding that is "accepted risk" has the acceptance justified with a named risk owner and an expiration date. Every trust boundary in the architecture diagram is verified enforced in code, configuration, or network policy. Every finding shipped in the hardening report is actionable: title, severity with justification, affected asset, reproduction steps, impact, root cause, proposed fix with a code example, regression prevention, retest plan, references.

This principle is non-negotiable. An AI-generated hardening pass that outputs "Ran Semgrep, zero criticals, app is secure" fails it in one line: the Veracode 2025 base rate (45% of AI code has at least one OWASP Top 10 bug) establishes that absence of scanner findings is not a signal of security. The skill refuses it as a deliverable. Research citations for each have-not are in [`references/RESEARCH-2026-04.md`](references/RESEARCH-2026-04.md) sections 1, 2, and 11.

## Named failure modes the skill refuses

harden-ready inherits the ready-suite's naming discipline: a sloppy pattern gets a specific name that the skill can refuse by name. These are the patterns; each maps to a citation in the research report.

- **Scanner-first security.** The scanner's output IS the hardening posture; anything the scanner did not find is assumed absent. Veracode 45%, Snyk's 80% developer-bypass rate, and the Lovable RLS epidemic are all past the scanner perimeter.
- **Paper trust boundary.** A trust boundary declared in the threat model or the architecture diagram, not enforced in code, configuration, or network policy. The grep pattern is an architecture doc that says "untrusted zone" with no iptables rule, security group, WAF policy, or server-side authorization check to back it. The Lovable CVE-2025-48757 canonical example.
- **Hardening-as-ritual.** Annual pen test, nothing between; or quarterly vulnerability scan treated as the control rather than the signal. The failure mode is the calendar's control role, not the assessment's quality.
- **Compliance-without-security.** Every checklist item passes; the application is still exploitable via its front page. SOC 2 Type II reports describing controls in place and operating effectively while the production app has a BOLA on its main API.
- **Pre-audit panic.** Hardening activity that only appears on the audit calendar, lapses immediately after, and resumes next cycle. Subordinate failure mode within hardening-as-ritual.
- **Shallow-audit trap.** An audit that only finds what automated tools surface, missing the manual-review layer that catches the attacker's actual path. SAST misses business-logic bugs; DAST misses IDOR and BOLA; SCA misses typosquatted dependencies and maintainer compromise.
- **CVE-of-the-week.** Reacting to each CVE as it lands without investing in the class of weakness that keeps producing them. The Log4Shell patch sequence (2.15, 2.16, 2.17, 2.17.1) is the canonical example of the instance-fix trap.

Vocabulary the skill uses but does not claim (taken terms, cited and attributed): **security theater** (Schneier), **compliance theater** (Chuvakin, Shortridge), **the lethal trifecta** (Willison, specifically for LLM-tool agents: private-data access + untrusted content exposure + exfiltration channel), **Agents Rule of Two** (Meta 2025, extension of the trifecta with state-change), **checklist rot** (Vehent).

## When this skill does NOT apply

Security bleeds into everything, which is why the scope fence works harder here than any sibling. Route elsewhere if the request is:

- **Building the app with reasonable security defaults.** That is `production-ready` and its canonical references: `auth-and-rbac.md` (sessions, passwords, OAuth library choice, RBAC matrices, server-side enforcement), `performance-and-security.md` (CSP, HSTS, CORS, basic rate limiting, security headers, basic XSS prevention, basic SQL injection prevention), `security-deep-dive.md` (session regeneration, API keys, secrets management basics, incident response process, file uploads basics). harden-ready assumes those are in place and runs the adversarial review on top.
- **Repo-hygiene security: secret scanning in CI, SBOM generation, signed commits, SECURITY.md template, branch protection, CODEOWNERS on security-sensitive paths.** That is `repo-ready` and its `security-setup.md`. harden-ready verifies these exist and function; it does not set them up.
- **Secrets injection at deploy time: vault-to-runtime wiring, per-environment secret rotation, CI-to-runtime secret shipping.** That is `deploy-ready` and its `secrets-injection.md`. harden-ready verifies secrets never reach logs, client bundles, or error reports; it does not wire the injection pipeline.
- **Security event detection, alerting, SIEM wiring, PII scrubbing in telemetry pipelines, audit-log retention.** That is `observe-ready`. harden-ready identifies what should be detected and specifies the detection contract; `observe-ready` wires the alert rule, runbook, and routing.
- **Threat modeling during architecture.** That is `architecture-ready` (trust boundaries, data flow diagrams) and `production-ready` (the three-question threat model in Step 2 of production-ready). harden-ready reads both and tests the trust boundaries at the wire; it does not re-do the threat model from scratch.
- **Picking the security tool itself.** Semgrep vs. CodeQL, Snyk vs. Socket, Trivy vs. Grype, Wiz vs. Lacework. That is `stack-ready`. harden-ready has opinions in `references/security-tooling-landscape.md` about what each category catches and misses, but the tool-choice decision is stack-ready's.
- **Writing the app's first SECURITY.md.** That is `repo-ready`. harden-ready extends SECURITY.md into a full responsible-disclosure program (severity vocabulary, triage SLA, safe-harbor text, RFC 9116 security.txt, bounty economics) in `references/responsible-disclosure.md`.
- **Go-to-market timing, public disclosure of security improvements as marketing.** That is `launch-ready` if any public communication is involved.
- **Business-level risk acceptance, insurance decisions, legal strategy.** harden-ready surfaces technical risk with severity and impact; business owners decide what to accept. The skill emits a risk register; it does not sign off on one.
- **Incident response as a live operation.** Paging, war room, customer comms, status-page posting, public disclosure timing. That is `observe-ready`'s `incident-response.md` and the company's incident management process. harden-ready owns post-incident hardening (the class-not-instance discipline after the incident is closed), not in-flight response.
- **Employee security training, phishing simulations, security culture, security awareness.** Out of scope. harden-ready is technical hardening, not human-factor.
- **Physical security, HR processes, device management, MDM, SSO for corporate accounts.** Out of scope.
- **Purple-team exercises, red-team engagement design.** harden-ready prepares for an external pen test; it does not run a red team.
- **Supply-chain intrusion investigation beyond dependency hygiene.** If a vendor is compromised and the incident involves adversary pivot through their access, that is incident response (observe-ready's domain) and legal engagement, not a hardening pass.
- **Live pen-test execution.** harden-ready prepares the scope, ROE, and retest discipline; it does not perform the pen test. An agent running nmap against unauthorized targets is a crime; the skill refuses to run offensive actions.
- **AI safety beyond security-adjacent concerns.** Content-policy jailbreaks that produce disallowed content are a safety concern; the skill covers them only where they intersect with security (system-prompt extraction, training-data extraction, tool-use coercion). Alignment work, RLHF tuning, and content-policy design are out of scope.

This section is the scope fence. Every plausible trigger overlap with a sibling has a route-elsewhere line. If in doubt, ask whether the work changes the app (production-ready), the repo (repo-ready), the deploy pipeline (deploy-ready), or the monitoring (observe-ready); if yes, route there. harden-ready only verifies and reports; it does not own the fix-side implementation of a sibling's canonical territory.

## Workflow

Follow this sequence. Skipping steps produces the exact class of failure this skill exists to prevent: a hardening pass that produces a tool-report summary with no adversarial reads, or a compliance binder with no code evidence, or a findings list with no severity, or a fix list with no retest.

### Step 0. Detect hardening state and mode

Read `references/harden-research.md`. Run the mode detection protocol; declare a mode in writing before any verification step.

- **Mode A (Pre-launch hardening).** No incidents yet, no audit pending; founder wants to ship secure. Walk the full workflow.
- **Mode B (Pre-audit hardening).** SOC 2 / HIPAA / PCI-DSS / GDPR deadline on the calendar. The compliance gap check (Step 7) is the load-bearing section; the adversarial review still runs but the artifact is shaped for the auditor.
- **Mode C (Post-incident hardening).** An incident landed; the initial patch is deployed; the question is what class the instance belonged to and what other instances exist. Step 13 leads; the class-review discipline dominates.
- **Mode D (Continuous hardening).** Ongoing program. The skill runs at a cadence (monthly / quarterly) and the artifact is an additive delta against the last pass. State is in `.harden-ready/STATE.md`.
- **Mode E (Pre-pen-test hardening).** An external engagement is scheduled. Step 9 leads; the ROE and scope document is the first deliverable; Steps 3 to 6 run to remove the known-class findings before an external team spends their time on them.

**Passes when:** a mode is declared in writing; the corresponding research block from `harden-research.md` is produced; the upstream-artifact inventory (section "Consumes from upstream" below) has been performed. If upstream artifacts are missing (`.production-ready/STATE.md`, `.architecture-ready/ARCH.md`, etc.), the gap is noted in the findings report as context, not as a finding.

### Step 1. Attack-surface inventory

Read `references/harden-research.md` section 2 (the 2025-2026 incident catalog). Catalog the attack surface from the attacker's perspective, not the developer's.

Produce, in writing:

1. **Exposed endpoints.** Every HTTP path, every GraphQL query and mutation, every WebSocket channel, every gRPC method, every public queue, every webhook endpoint. Tagged by auth requirement (unauth / user / admin / service). Source: `.production-ready/STATE.md` (user journeys), `.deploy-ready/TOPOLOGY.md` (services), and direct enumeration against the running app (curl the sitemap, walk the OpenAPI spec, inspect the JS bundle for API calls).
2. **Data assets.** Every database table, object-store bucket, cache, vector store, secret store. Classified by data sensitivity per `production-ready`'s data classification (Public / Internal / Confidential / Restricted). PII columns named explicitly.
3. **Trust boundaries.** Every declared boundary in `.architecture-ready/ARCH.md`. For each, the enforcement mechanism (iptables, security group, WAF, reverse-proxy auth, server-side authorization check, RLS policy, IAM role). A boundary declared but not enforced is a **paper trust boundary** finding in Step 11.
4. **Third-party dependencies with privileged access.** Every OAuth-integrated third party, every API key the app holds, every SSO provider, every payment processor, every analytics platform with server-side ingest, every LLM provider and model, every webhook target.
5. **Environments in scope.** Production, staging, preview deploys, PR environments. A hardening pass that only checks production leaves the staging credential-leak and the PR-environment credential-leak unfound.
6. **Users and roles.** Every role in the RBAC matrix (`production-ready`'s `auth-and-rbac.md`). Every role's attack value (what an attacker who compromises this role can do). The role that can exfiltrate the most data, the role that can change billing, the role that can escalate to admin.

**Mode C shortcut:** the incident's blast radius is the immediate inventory priority. The question is what other instances of the same class exist inside the full attack surface.

**Passes when:** the six-item inventory is written; every item has a source cited (upstream artifact or direct enumeration); paper-trust-boundary candidates are flagged for Step 3 verification; the inventory is reproducible by a third party reading the output.

### Step 2. Scope fence and threat actor profile

Read `references/harden-research.md` section 9 (pen-test engagement anatomy). Define what this hardening pass covers and what threat actor it models. The scope fence is the difference between a useful pass and a sprawling one.

Produce:

1. **In-scope assets.** The subset of the Step 1 inventory this pass actually verifies. A Mode A pre-launch pass on a solo SaaS might cover the whole inventory; a Mode B pre-audit pass might cover the in-scope systems for that audit; a Mode C post-incident pass might cover a specific blast radius.
2. **Out-of-scope assets.** Explicit list. Assets in the inventory but not in this pass. Each has a reason (future pass, different pass, accepted risk, owned by another team).
3. **Threat actor model.** One paragraph naming the modeled adversary. "Unauthenticated remote attacker with HTTP-only access" is the baseline for most public web apps. "Authenticated customer on a multi-tenant SaaS trying to read another tenant's data" is the BOLA-class adversary. "Authenticated admin of a partner organization" is the confused-deputy adversary. "Malicious insider with commit access" is a separate and higher-cost model. Most hardening passes model the first two; specify which.
4. **Rules of engagement.** For the verification work the skill performs: test-environment only, no denial-of-service, no modification of production data, no credentials-testing against live user accounts. If an external pen test is in scope (Mode E), the full ROE document is produced per `references/pentest-prep.md`.

**Passes when:** scope is explicit; out-of-scope assets are enumerated; a threat actor is named; the ROE is written. If the scope is "the whole inventory" for a small app, state it. Scope-by-silence is a shallow-audit risk.

### Step 3. OWASP Top 10 systematic walkthrough

Read `references/owasp-walkthrough.md`. This is the load-bearing adversarial-review step. Walk the OWASP Web Top 10 (2021 edition; track the 2025 RC1), the OWASP API Security Top 10 (2023 edition), and, if the app integrates LLMs, the OWASP Top 10 for LLM Applications (2025). Each category is walked against the actual running system, not against the scanner report.

For each category, produce:

1. **Category name and number.** (A01 Broken Access Control, API1 BOLA, LLM01 Prompt Injection, etc.)
2. **The common AI-generated-code failure in this category.** From the research catalog. For A01 on a Lovable-style app, it is RLS absence. For API1 on a Vercel-deployed serverless app, it is JWT claim trust in the frontend. For LLM06 on an agent-style app, it is excessive tool access.
3. **The scanner gap.** What SAST, DAST, and SCA typically catch and miss in this category. A01 is mostly invisible to SAST (the tool does not know what object ownership means); DAST catches some cases with authenticated multi-account scanning but misses the business-logic layer.
4. **The manual test performed.** The specific action taken against the running system. For A01 BOLA: "with user A's token, issued GET /api/orders/<user_B_order_id>; observe response." For A01 mass-assignment: "POSTed `{role: 'admin'}` to `/api/users/<me>`; observed response." Reproduction is the deliverable.
5. **The result.** Pass (no finding), Fail (finding with severity), or Not Applicable (category does not apply to this app, with justification).
6. **Findings produced.** If Fail, the finding is written to the findings report per `references/actionable-findings.md` template. Severity, CVSS, CWE, OWASP, reproduction, impact, root cause, fix, regression prevention, retest.

The walk is not a checklist tick. It is a reproduced attack, or a reproduced verification that the attack fails. "We walked A01" without the specific GET / POST / curl that was issued is a shallow-audit finding.

**Passes when:** every category in every applicable Top 10 has a row in the walkthrough table; every row has a manual test recorded; every Fail row has a finding in the report; every Not Applicable has a one-line justification.

### Step 4. Auth and authorization deep verification

Read `references/auth-hardening.md`. Production-ready's `auth-and-rbac.md` owns the pre-build decisions (library choice, RBAC matrix design, session-vs-JWT tradeoff); harden-ready's `auth-hardening.md` owns the post-deploy adversarial verification of specific attack classes those decisions did not address.

Verify, with reproduction recorded:

1. **Session fixation.** Session IDs rotate on privilege transitions (login, logout, role escalation, password change). Test: log in, note cookie; log out; log in again; the session identifier is different. Session tied to context; user-agent and IP anomalies are logged.
2. **CSRF with SameSite limitations.** `SameSite=Lax` default is checked; SameSite-Strict-breaks-legitimate-flows tradeoff is documented; if the app uses `SameSite=None` for any cookie, the reason is named and the CSRF defense is a double-submit or an explicit token.
3. **OAuth flow attacks.** Authorization-code interception (PKCE enabled), state-parameter validation (CSRF on OAuth callback), nonce validation on OIDC, redirect-URI exact-match enforcement (not prefix-match), access-token audience validation.
4. **JWT pitfalls.** `alg: none` rejected, symmetric-vs-asymmetric key confusion rejected, signing key rotation implemented, `kid` header not used for path traversal, expiration enforced, `aud` and `iss` validated.
5. **Passkey / WebAuthn pitfalls.** Credentials scoped correctly, attestation verified if required, backup-eligibility flag checked, recovery flow does not downgrade auth strength.
6. **Authorization-vs-authentication confusion.** Every mutation and read endpoint is tested with a valid token scoped to a different user, a different tenant, and a different role. The "is user logged in" check is distinguished from the "does user own this object" check. BOLA audit per Section 3 API1 is recorded here in detail.
7. **Multi-tenant isolation.** If the app is multi-tenant, every query path is verified to include the tenant scope in the server-side predicate. RLS policies, tenant-aware ORM guards, and Postgres `SET ROLE` are each candidates; one is required and tested.

**Passes when:** each of the seven subsections has a test performed and recorded; findings are written per `actionable-findings.md`; the canonical auth-hardening decision record for this app is in `.harden-ready/AUTH-VERIFICATION.md`.

### Step 5. API hardening deep verification

Read `references/api-hardening.md`. Production-ready's `performance-and-security.md` owns basic rate limiting and input validation shape; harden-ready's `api-hardening.md` owns the attack-surface classes those defaults do not cover.

Verify:

1. **Rate-limit design.** Token bucket, sliding window, or leaky bucket; the limit key (IP, user, key, API key, OAuth client ID) and the attacker's rotation cost for that key; IPv6 single-address rotation and the `/64` block practice; rate-limit-bypass via Host header, X-Forwarded-For spoofing, and WebSocket channel.
2. **GraphQL query cost.** If GraphQL is exposed, introspection in production is rejected, query depth is capped, query complexity is scored and capped, aliased-query-flooding is blocked, batched-query limits are set.
3. **Mass assignment / BOPLA.** Every write endpoint rejects extra fields the caller supplies. Particularly `role`, `tenant_id`, `organization_id`, `is_admin`, `price`, `balance`, `is_verified`, `created_at`.
4. **Input validation beyond shape.** Zod / Pydantic shape validation catches type errors; it does not catch values outside business-valid ranges (a negative quantity, a future-dated expiration, a path-traversal filename, a URL scheme that is not `https`). The validation layer's semantics are audited.
5. **Idempotency-key abuse.** If idempotency keys are supported, collision rejection is correct; otherwise retry double-processing is possible.
6. **Webhooks.** Every inbound webhook validates HMAC signature with constant-time comparison, rejects replays via timestamp, and does not trust the source IP as authentication.
7. **File uploads at adversarial depth.** Magic-byte validation, not MIME. Image re-encoding strips EXIF and embedded payloads. SVG sanitization. Content-Disposition on downloads. Presigned-URL TTL and scope.

**Passes when:** the seven subsections are verified; findings per `actionable-findings.md`; the `.harden-ready/API-VERIFICATION.md` records the reproduction for each test.

### Step 6. Cryptography audit

Read `references/crypto-primitives.md`. This reference is net-new to the suite; production-ready does not cover primitive selection at this depth.

Verify:

1. **Primitive selection.** AEAD (AES-GCM or ChaCha20-Poly1305) for symmetric encryption, not CBC with separate MAC. Ed25519 or ECDSA P-256 for signatures, not RSA-PKCS1-v1.5. Argon2id for password hashing (or scrypt if Argon2 not available), not MD5, SHA-1, SHA-256, or PBKDF2-with-low-iterations. HMAC-SHA-256 for MACs, with keyed comparison.
2. **Key management.** KMS (AWS KMS, GCP Cloud KMS, Azure Key Vault, HashiCorp Vault) is used for key storage; keys are not in environment variables, config files, or source code. Rotation cadence is defined. Envelope encryption (DEK encrypts data; KEK from KMS encrypts DEK) is used for column-level encryption.
3. **IV / nonce discipline.** No IV reuse under the same key. Random IVs for CBC (with separate MAC layer if CBC is unavoidable); deterministic monotonic nonces for GCM where counter collision is impossible; random nonces for ChaCha20-Poly1305 with 192-bit extended nonce (XChaCha20) if the key is used for many messages.
4. **Signature verification.** Constant-time comparison on HMAC outputs. No string-equality on any cryptographic output. Signature-verification libraries are up to date (critical CVEs in old `jsonwebtoken`, `pyjwt`, `node-forge` patched).
5. **TLS configuration.** TLS 1.2 minimum, TLS 1.3 preferred; weak cipher suites disabled; OCSP stapling; HSTS with preload if appropriate; certificate pinning where it makes sense and not where it does not (mobile yes; browser no).
6. **Post-quantum posture.** If the threat model includes state-level adversaries harvesting ciphertext for future decryption, the PQC migration plan is noted. CNSA 2.0 timelines cited. For most apps, noting "no PQC yet; revisit in 2028" is the honest answer.

**Passes when:** primitive selection is audited; key management is named (KMS vendor, rotation cadence); no IV reuse found; constant-time comparison verified on every signature path; TLS configuration passes SSL Labs A or A+.

### Step 7. Compliance framework mapping

Read `references/compliance-frameworks.md`. Mode B makes this step load-bearing; Modes A, C, D, E include it when an audit is within twelve months.

For each framework in scope (SOC 2 CC, HIPAA 164.312, PCI-DSS 4.0, GDPR Article 32), produce a control-to-code mapping:

| Control | Framework reference | Evidence location | Implementer | Verification date |
|---|---|---|---|---|
| Example: Encryption at rest | SOC 2 CC6.1; HIPAA 164.312(a)(2)(iv); PCI 3.5; GDPR 32(1)(a) | TDE enabled on Postgres (`SHOW aws_rds.encryption`); app-layer encryption for SSN column (`src/crypto/encrypt.ts`); backups encrypted (S3 bucket policy `backups-bucket-policy.json`) | Platform team | 2026-04-22 |

The cross-framework mapping summary in `references/compliance-frameworks.md` shows the nine engineering controls that satisfy the overlapping portions of SOC 2 / HIPAA / PCI / GDPR. Those controls are the highest-leverage; verify those first, then the framework-specific residual.

**The compliance-without-security trap.** Every control can be checked off with a weakly-implemented version that passes audit and fails adversary. harden-ready refuses this:

- "Encryption at rest" passes when TDE is enabled. Compliance-without-security: TDE protects against physical theft, not SQL injection. Column-level encryption for Restricted data is the real control.
- "Access control" passes with an RBAC matrix. Compliance-without-security: the matrix is on paper, the app does not check it on the server. Step 4 BOLA audit is the real control.
- "Audit logging" passes with log retention. Compliance-without-security: the logs are retained, the query path is only through a GUI, and nobody has reviewed them since the last audit. Step 4 authorization-failure log-and-alert rule is the real control.
- "Incident response" passes with a documented policy. Compliance-without-security: the policy is three years old, the on-call rotation is different, nobody has run a tabletop. observe-ready owns the test cadence.

**Passes when:** every control in every in-scope framework is mapped to a specific evidence artifact (file path, configuration value, log query, screenshot); every control has an implementer owner; every control has a verification date not older than the audit's observation period. Gaps are findings in Step 11, not excuses.

### Step 8. Security tooling verification

Read `references/security-tooling-landscape.md`. This step verifies the scanning surface runs, runs on the right code, and gates the right workflows. It is the scanner-first-security inoculation step; the skill stops here only if the scanner's role is understood as one layer among many.

Verify:

1. **SAST.** Tool chosen (Semgrep, CodeQL, Snyk Code, Checkmarx). Scan runs on every PR. Blocking threshold is set (fail CI on Critical and High; ticketable otherwise). Custom rules exist for project-specific patterns (sensitive API routes, specific deserialization libraries).
2. **DAST.** If DAST is in use (ZAP, Burp), it runs against a staging environment; authenticated scanning is configured (not just unauthenticated); the scan is scheduled (at least monthly) and on major release.
3. **SCA.** Tool chosen (Snyk, Socket, Dependabot, Renovate, OSV-Scanner). Hash-integrity verification on install. Socket-style behavioral analysis is active for new dependencies (slopsquatting defense).
4. **Secret scanning.** Tool chosen (GitGuardian, TruffleHog, Gitleaks, GitHub secret scanning). Runs pre-commit AND pre-receive AND on full-history at least weekly. Leaked secrets have a rotation playbook (names of credentials, named KMS keys, named API keys).
5. **Container scanning.** If containers are in use, Trivy / Grype / Docker Scout / Snyk Container runs on every image. Blocks on Critical/High known CVEs. Minimal base images are used.
6. **IaC scanning.** If IaC is in use (Terraform, CloudFormation, Pulumi, K8s manifests), Checkov / tfsec / KICS runs. Blocks on misconfiguration severity.
7. **Runtime.** If runtime EDR (Falco, Tetragon, commercial) is in use, its rule set is audited (not the default, which catches everything and alerts nothing useful).

The verification is "does it run and gate" not "does it find everything." The skill's whole thesis is that tools are not enough; this step verifies the tools are at least present and correctly configured so the adversarial review in Step 3 through Step 6 catches what the tools miss, not what the tools missed to run.

**Passes when:** each category has a tool named or "N/A with justification"; each in-use tool has a gate documented; each tool's scan output is checked against the findings report (tool-found findings are acknowledged and triaged in the same report as manual findings).

### Step 9. Pen-test preparation and rules of engagement

Read `references/pentest-prep.md`. Mode E makes this step load-bearing; any mode with an external engagement on the calendar runs it.

Produce, before an external team is engaged:

1. **Engagement scope document.** In-scope environments, in-scope applications, in-scope test types (web, API, mobile, internal network, social engineering). Out-of-scope items with reasons.
2. **Rules of engagement.** Permitted test types; denial-of-service limits; data-handling for any PII discovered; disclosure agreement; retest inclusion.
3. **Pre-test baseline.** The known findings at the start of the engagement, so the external team's output is additive rather than re-discovery of known issues. Run Steps 3 to 6 before the external team arrives.
4. **Credentials and accounts.** Named test accounts per role. Environment separation (test-tenant data, not real-customer data).
5. **Communication plan.** Daily check-in during the engagement; emergency escalation if the team finds something catastrophic mid-engagement.
6. **Retest protocol.** For every finding in the external team's report: fix, deploy, retest, close. The retest is mandatory, not optional. A pen-test report with unretested fixes is `hardening-as-ritual`.

Vendor selection: `references/pentest-prep.md` compares Cobalt.io, HackerOne Pentest, Synack, Bugcrowd PTaaS, Trail of Bits, Doyensec, NCC Group, and boutique firms. Stage-appropriate guidance in the reference.

**Passes when:** scope and ROE documents exist; pre-test baseline is run and documented; retest protocol is agreed with the vendor.

### Step 10. Responsible-disclosure program

Read `references/responsible-disclosure.md`. Extends repo-ready's SECURITY.md scaffold into a functioning program.

Produce:

1. **Policy page.** Public-facing. RFC 9116 security.txt served at `/.well-known/security.txt`. The policy includes safe-harbor language (the "authorization for good-faith research" statement every modern program has).
2. **Severity vocabulary.** The program's scale. CVSS 3.1 or 4.0 as the base; EPSS used for likelihood; CISA KEV as ground truth. Composite used for triage priority, not CVSS alone (28%+ of exploited vulns are "medium" CVSS).
3. **Triage SLA.** Time-to-first-response (the Lovable 48-day gap between email-receipt and disclosure is the cautionary citation). Time-to-fix by severity. Time-to-public-disclosure (90 days Project Zero default; 45 days CERT/CC; choose one and state it).
4. **Triage workflow.** Who reads the inbox, on what cadence; escalation to engineering; decision on bounty payout if a bounty program exists; decision on CVE assignment.
5. **Bounty-vs-VDP choice.** A VDP (Vulnerability Disclosure Program, no payouts) is the floor; a private bounty program is the middle; a public bounty program is the ceiling. Stage-appropriate per `responsible-disclosure.md`: a pre-launch startup probably wants VDP only; a Series A with a security engineer can run private bounty; a public bounty program without a full-time triager is often net-negative (the noise-to-signal ratio defeats the team).
6. **Disclosure-coordination protocol.** Coordinated with the researcher; assign a CVE via MITRE's CNA process if the finding is reusable; publish the advisory on a timeline agreed with the researcher.

**Passes when:** the policy page exists; security.txt is served and valid (`dig` or `curl` against `/.well-known/security.txt`); the triage SLA is documented; a human owns the inbox (not "security@"); the first test email is sent and replied to within the SLA.

### Step 11. Findings report

Read `references/actionable-findings.md`. Every finding from Steps 3 to 6 (and Step 7's gaps, Step 8's tool-surfaced findings, Step 10's disclosure-program-found findings) is written to the report per the template.

The template, non-negotiable, is:

```
## F-NN: <specific title>

**Severity.** <Critical|High|Medium|Low|Informational>
**CVSS 3.1.** <vector string> (<score>)
**EPSS.** <percentile or score> (if applicable)
**KEV.** <Yes|No>
**CWE.** <CWE-N with title>
**OWASP.** <Top 10 category>

### Affected asset
<file path or URL or service with specific version / commit>

### Description
<what the bug is, one paragraph>

### Reproduction
1. <step 1, verbatim>
2. <step 2, verbatim>
3. <observe specific result>

### Impact
<what attacker gains; what users affected; data classification impacted>

### Root cause
<design or implementation error, not symptom>

### Proposed fix
<specific code or configuration change>

```<language>
<code example>
```

### Regression prevention
<test, lint rule, architectural change>

### Retest
<command or action verifying the fix>

### References
- <CWE link>
- <OWASP link>
- <vendor advisory if applicable>
```

A finding missing any section is incomplete. An "issue" with only a title and a severity is a generic finding; the skill rewrites it to actionable or discards it as noise. Canon examples in the reference file cite Trail of Bits, Doyensec, NCC Group, Latacora formats.

**Passes when:** every finding has every section; findings are numbered and indexed; severity is justified by CVSS vector plus business-impact sentence; reproduction steps are reproducible by a third party; proposed fixes include a code example or a configuration delta.

### Step 12. Fix and retest

Read `references/actionable-findings.md` section on retest discipline. Every finding has a fix plan, a fix implementer, a fix-landed-in-commit, and a retest result.

The fix workflow:

1. **Severity-ordered.** Critical and High block the release; Medium is ticketed; Low and Informational are tracked.
2. **Fix ownership.** Each finding has an owner (a named engineer or team). A finding without an owner rots.
3. **Fix landing.** The fix lands in a specific commit. The commit message references the finding ID.
4. **Retest.** The retest command from the finding is executed against the fixed version. Pass or fail is recorded. If fail, the finding reopens.
5. **Regression prevention applied.** The test, lint rule, or architectural change named in the finding is committed. A fix without a regression guard is a one-shot repair; the class returns.
6. **Closing.** A finding is closed only after retest passes AND regression prevention is landed.

**Mode C (post-incident):** the fix-and-retest loop is the same, but the CVE / incident ID is the parent thread, and the regression-prevention guard is the class-level fix per Step 13.

**Passes when:** the findings report has a "Status" column populated (Open, In Progress, Fixed, Retested, Closed); every Closed finding has a retest log entry; regression prevention is landed for every Closed Critical or High.

### Step 13. Post-incident class hardening

Read `references/post-incident-hardening.md`. This step runs in Mode C and runs after every security incident in Mode D. It is the antidote to CVE-of-the-week.

For every incident (or finding landed as an incident):

1. **Instance fix landed.** Step 12 complete on the specific bug.
2. **Class identification.** What class of weakness does this bug belong to. Log4Shell's class was "implicit deserialization of untrusted features in a library." xz-utils's class was "maintainer-account supply-chain compromise with obfuscated multi-stage payload." Replit 2025's class was "excessive agency: LLM tool access with no blast-radius fence." Lovable CVE-2025-48757's class was "paper trust boundary: authz declared in the frontend, not enforced in the data layer."
3. **Class survey.** Search the codebase for other instances of the same class. The Log4Shell response team that searched for `jndi:` once did less than the team that searched for "any library feature that deserializes untrusted strings."
4. **Class fix.** The architectural or policy change that prevents the class from reintroducing. For Log4Shell, disabling JNDI entirely. For excessive agency, a tool-allowlist per context. For paper trust boundary, a default-deny RLS policy for every new table. This fix goes in `.harden-ready/CLASS-FIXES.md`.
5. **Regression guard at the class level.** Not just a test for the specific instance. A lint rule, a type-system constraint, a CI check, an architectural rule. The goal is that an AI-generated codebase in six months cannot re-introduce the class.

The worked examples (Log4Shell, xz-utils, SolarWinds, Replit 2025, Lovable CVE-2025-48757) are in `references/post-incident-hardening.md`, each with the instance / class / class-of-classes walkthrough.

**Passes when:** every incident in scope has instance-fix, class-identification, class-survey, class-fix, and class-level regression guard. The `.harden-ready/CLASS-FIXES.md` is updated on every pass. A pass with "instance fixed" but no class entry is hardening-as-ritual.

## Completion tiers

20 requirements across 4 tiers. Aim for the highest tier the session allows. Declare each tier explicitly at its boundary.

### Tier 1: Inventoried (5)

The attack surface is understood from the attacker's perspective.

| # | Requirement |
|---|---|
| 1 | **Mode declared.** One of A (pre-launch), B (pre-audit), C (post-incident), D (continuous), E (pre-pen-test). Declared in writing; corresponding research block produced. |
| 2 | **Six-item attack-surface inventory written.** Exposed endpoints, data assets, trust boundaries, third-party dependencies with privileged access, environments in scope, users and roles. Each item with a source cited. |
| 3 | **Scope fence documented.** In-scope assets enumerated; out-of-scope assets enumerated with reasons; threat actor modeled; rules of engagement written. |
| 4 | **Upstream artifacts consumed.** `.production-ready/STATE.md`, `.architecture-ready/ARCH.md`, `.deploy-ready/TOPOLOGY.md`, `.observe-ready/SLOs.md`, `.repo-ready/SECURITY.md` each checked; absences noted in the report as context. |
| 5 | **Paper-trust-boundary candidates flagged.** Every declared boundary in ARCH.md has a named enforcement mechanism; boundaries without enforcement are flagged for Step 3 verification. |

### Tier 2: Audited (5)

The systematic adversarial walkthroughs have been performed and findings produced.

| # | Requirement |
|---|---|
| 6 | **OWASP Web Top 10 walked.** Each of the ten 2021 categories has a row: AI-code failure pattern, scanner gap, manual test performed, result, findings produced (if any). |
| 7 | **OWASP API Top 10 walked** if the app exposes an API. Each 2023 category walked with reproduction, especially API1 BOLA and API3 BOPLA. |
| 8 | **OWASP LLM Top 10 walked** if the app integrates LLMs. 2025 edition. LLM01 Prompt Injection with the lethal trifecta assessment; LLM06 Excessive Agency with tool-access audit. |
| 9 | **Auth, API, and crypto deep verifications complete.** Steps 4, 5, 6 each with reproduction recorded to `.harden-ready/AUTH-VERIFICATION.md`, `.harden-ready/API-VERIFICATION.md`, `.harden-ready/CRYPTO-VERIFICATION.md`. |
| 10 | **Findings report produced per template.** Every finding has every section of the `F-NN` template. Severity justified by CVSS + EPSS + KEV composite where applicable. |

### Tier 3: Hardened (5)

Fixes land, retest passes, class-level regression guards are in place.

| # | Requirement |
|---|---|
| 11 | **All Critical and High findings fixed and retested.** Fix commit referenced in finding; retest command run; Status = Closed in the report. |
| 12 | **Regression prevention landed** for every Closed Critical and High. Test, lint rule, or architectural change committed. |
| 13 | **Class fixes recorded.** For every finding that is an instance of a broader class, `.harden-ready/CLASS-FIXES.md` has the class identification, class survey, class fix, and class-level guard. |
| 14 | **Security tooling verified.** SAST, SCA, secret-scanning, and (if applicable) DAST, container scanning, IaC scanning each run and gate. Tool-found findings are acknowledged in the same findings report as manual findings. |
| 15 | **Paper-trust-boundary findings all resolved or explicitly accepted.** Every declared-but-unenforced boundary from Tier 1 requirement 5 is either enforced (via iptables / SG / WAF / authZ / RLS) or signed off with a named risk owner and an expiration date. |

### Tier 4: Accountable (5)

Compliance is mapped to code, disclosure program runs, and the hardening posture is continuous.

| # | Requirement |
|---|---|
| 16 | **Compliance control-to-code mapping done** for every in-scope framework. SOC 2 CC / HIPAA 164.312 / PCI-DSS 4.0 / GDPR Article 32 as applicable. Every control has evidence path, implementer, verification date. |
| 17 | **Compliance-without-security traps audited.** Each control is checked against the "what does the adversary do if the control is weakly implemented" question, with documented answers. |
| 18 | **Responsible-disclosure program live.** Policy page served; `/.well-known/security.txt` valid; severity vocabulary documented; triage SLA named; a human owns the inbox; a test email has been sent and answered within SLA. |
| 19 | **Pen-test engagement scope and ROE ready** (Mode E) or pen-test retest complete (Mode A / D post-engagement). Retest discipline enforced: every external finding retested before closure. |
| 20 | **Continuous cadence declared.** Mode D trigger defined: monthly scanner review, quarterly tabletop / class-review, annual pen test OR continuous bounty program. Calendar has the next execution date. |

**Proof test:** an outsider (auditor, security engineer, or adversarial peer) reads the findings report cold, selects any three findings, and can reproduce each one from the written reproduction steps alone. Selects any three closed findings and can verify closure from the retest steps alone. Selects any three compliance controls and can locate the specified evidence artifact in the codebase alone. If any of those three checks fails cold, the pass is not Tier 4.

## The "have-nots": things that disqualify the hardening pass at any tier

If any of these appear, the hardening pass fails this skill's contract and must be fixed:

- **A findings summary that cites only tool output.** "Ran Semgrep, 0 critical. Ran Snyk, 0 critical. Ran Trivy, 0 critical." With no manual OWASP walkthrough recorded. **Scanner-first security.**
- **A compliance claim with no control-to-code mapping.** "SOC 2 Type II ready" with no spreadsheet or table pointing each CC to a file, config, or log artifact. **Compliance-without-security.**
- **A pen-test report that lists only tool output.** Venue (internal or vendor) does not matter; a pen test whose findings are all Burp-generated Medium-severity items without a named logic bug or an authz bypass is a shallow audit on pen-test letterhead.
- **A hardening pass with no severity ranking on findings.** "Here are 47 issues" without Critical/High/Medium/Low is a raw list, not a hardening posture. Severity is the triage signal.
- **A hardening pass with no retest after fix.** Fix landed; finding marked "fixed"; retest column blank. A fix without retest is a guess.
- **A fix plan that patches instances not classes.** For a finding that is an instance of Log4Shell-like or Lovable-like class, a fix that only addresses the reported instance without a class-survey and a class-level regression guard. **CVE-of-the-week.**
- **An architecture trust boundary declared but not verified enforced.** ARCH.md says "untrusted zone" at a boundary; code and config show no iptables rule, security group, WAF policy, server-side authz check, or RLS policy backing it. **Paper trust boundary.**
- **A SECURITY.md alone counted as a responsible-disclosure program.** An email address with no severity vocabulary, no triage SLA, no safe-harbor language, no security.txt, no named inbox owner is a contact method, not a program.
- **A responsible-disclosure email with no reply in SLA.** Test-email sent; SLA states 72-hour first-response; reply not observed. The program is performative.
- **A finding whose reproduction steps cannot be followed by a third party.** "Authentication issue on /login" with no payload, no request, no curl, no screenshot. **Shallow-audit trap.**
- **A finding without CWE and OWASP mapping.** The references tie the finding into the literature; their absence prevents the reader from learning the class.
- **"We ran Snyk and fixed criticals" as a Mode A posture.** Without a manual OWASP walkthrough, without a BOLA test, without an auth-verification record. The Veracode 45% base rate is the immediate rebuttal.
- **"Pen test scheduled for Q4"** as the whole continuous-hardening plan. Annual pen test, nothing between. **Hardening-as-ritual.**
- **Disclosure-inbox owned by "security@" with no named human.** An alias with no owner has a response-time latency of "forever minus two days." The Lovable 48-day disclosure-timeline gap is the citation.
- **Bounty program public-launched without triage capacity.** A public program without a full-time triager will drown in low-quality submissions and either burn the triage engineer out or accidentally ignore a real finding. VDP-or-private until triage capacity exists.
- **Secrets found in the client bundle or logs during the audit** without an immediate rotation plan. Finding a secret without rotating it is the beginning of an incident, not a finding.
- **RLS policies verified "configured" without a curl against the anon-key endpoint.** The Lovable class: "RLS is configured" is not the same as "RLS is correct." The only verification is a request.
- **JWT verification code that accepts `alg: none` or that fails to validate `aud` / `iss` / `exp`.** These are not theoretical bugs; they are recurring production incidents.
- **LLM-integrated app without a lethal-trifecta assessment.** Any app that has any of {private data access, untrusted content exposure, exfiltration channel, state change via tool call} crossed with any other of that set, without an explicit Rule-of-Two assessment and controls, is an unpatrolled surface.
- **A hardening pass that declares "no incidents found" without saying what was looked for.** The scope-by-silence shallow-audit signature. Silence is not evidence; the verification of absence requires the probe.
- **Emojis used in the findings report or in the fix instructions.** The ready-suite global rule; harden-ready enforces.

When you catch yourself about to ship any of these, fix it before proceeding. A hardening pass that ships with a single have-not is worse than no hardening pass; it provides false confidence and will be cited back during the next breach's postmortem.

## Reference files: load on demand

The body above is enough to start. Load each reference *before* the step that uses it, not after.

| Reference file | When to load | ~Tokens |
|---|---|---|
| `harden-research.md` | **Always.** Start of every session (Step 0). Mode detection, attack-surface inventory procedure. | ~8K |
| `owasp-walkthrough.md` | **Tier 2.** Step 3; OWASP Web 2021, API 2023, LLM 2025 walkthroughs with manual tests and AI-code failure patterns. | ~12K |
| `auth-hardening.md` | **Tier 2.** Step 4; session fixation, CSRF, OAuth flow attacks, JWT pitfalls, passkey pitfalls, BOLA deep-dive. | ~9K |
| `api-hardening.md` | **Tier 2.** Step 5; rate-limit design, GraphQL cost, mass-assignment, input validation beyond shape, webhook HMAC, adversarial file upload. | ~8K |
| `crypto-primitives.md` | **Tier 2.** Step 6; AEAD selection, KDF choice, IV/nonce discipline, signature schemes, TLS config, post-quantum posture. | ~7K |
| `compliance-frameworks.md` | **Tier 4.** Step 7; SOC 2 / HIPAA / PCI-DSS / GDPR control-to-code mapping; cross-framework high-leverage control list; compliance-without-security traps. | ~12K |
| `security-tooling-landscape.md` | **Tier 3.** Step 8; SAST / DAST / SCA / IAST / container / IaC / secret-scanning / runtime / WAF / PTaaS / bounty platform. What each catches, what each misses. | ~10K |
| `pentest-prep.md` | **Tier 4.** Step 9; engagement scope, ROE, stage-appropriate posture, vendor comparison, retest discipline. | ~7K |
| `responsible-disclosure.md` | **Tier 4.** Step 10; policy page, security.txt, severity vocabulary, triage SLA, VDP-vs-bounty choice, bounty economics, coordinated disclosure timelines. | ~9K |
| `post-incident-hardening.md` | **Tier 3.** Step 13; instance-vs-class discipline, Log4Shell / xz-utils / SolarWinds / Replit 2025 / Lovable CVE-2025-48757 walkthroughs with class-fix examples. | ~8K |
| `actionable-findings.md` | **Tier 2.** Step 11 and Step 12; finding template, severity vocabulary (CVSS + EPSS + KEV composite), canon examples from Trail of Bits / Doyensec / NCC Group / Latacora, retest protocol. | ~7K |
| `RESEARCH-2026-04.md` | **On demand.** Source citations behind every guardrail, incident, named failure mode, and banned pattern. ~30K tokens. | ~33K |
| `harden-antipatterns.md` | **Every adversarial review + Mode C audits.** Named-failure-mode catalog with grep tests, severity, and per-skill guards. Loaded at every pen-test prep + retest cycle. | ~5K |

Skill version and change history live in `CHANGELOG.md`. When resuming a project, confirm the skill version your session loaded matches the version recorded in `.harden-ready/STATE.md`. A skill update between sessions may change the OWASP category mapping (as the 2025 RC1 graduates), the bounty-economics guidance, the tooling landscape, or the compliance framework version references (PCI-DSS 4.0.1, GDPR post-2026 case law updates).

## Suite membership

harden-ready is the shipping-tier skill that owns "survive adversarial attention; prove it to an auditor." See `SUITE.md` at the repo root for the full map. Relevant siblings at a glance:

- **Planning tier:** `prd-ready` (what), `architecture-ready` (how), `roadmap-ready` (when), `stack-ready` (with what tools).
- **Building tier:** `production-ready` (the app), `repo-ready` (the repo scaffolding).
- **Shipping tier:** `deploy-ready` (ship it), `observe-ready` (keep it healthy), `launch-ready` (tell the world), `harden-ready` (this skill, survive adversarial attention and prove it).

Skills are loosely coupled: each stands alone, each composes with the others via well-defined artifacts. No skill routes through another; the harness is the router. Install what you need.

## Consumes from upstream

When the agent starts, it checks for upstream artifacts and pre-fills from them rather than asking the user to repeat decisions already made. Absence is fine; the skill falls back to its own defaults and notes the missing input in the findings report as context.

| If present | harden-ready reads it during | To pre-fill |
|---|---|---|
| `.architecture-ready/ARCH.md` | Step 1 (trust boundaries), Step 3 (Broken Access Control) | Declared trust boundaries; data-flow diagrams; the enforcement mechanism named for each boundary (or absence, which flags paper-trust-boundary). |
| `.production-ready/STATE.md` | Step 1 (attack surface), Step 3 (journeys-to-attack-paths), Step 4 (RBAC) | The actual shipped feature set; user journeys to test end-to-end; RBAC matrix to test horizontally and vertically. |
| `.production-ready/adr/*.md` | Step 3 (security ADRs), Step 6 (crypto) | Recorded architectural decisions with security implications (auth library choice, RLS-vs-in-app enforcement, crypto library). |
| `.production-ready/visual-identity.md` (if present) | not consumed | Not relevant to harden-ready. |
| `.deploy-ready/TOPOLOGY.md` | Step 1 (environments, services), Step 5 (API hardening) | Environments in scope; service inventory; public-endpoint URLs; network topology and any WAF in front. |
| `.deploy-ready/STATE.md` | Step 9 (pen-test scope) | Current production version; last-known-green deploy state; whether an expand/contract migration is mid-flight (which affects what pen-test hits). |
| `.deploy-ready/secrets-injection.md` references | Step 8 (secret scanning verification) | How secrets flow at deploy time; harden-ready verifies secrets do not leak in logs, client bundles, or error reports. |
| `.observe-ready/SLOs.md` | Step 3 (availability class), Step 8 (detection gaps) | Named SLOs; harden-ready identifies which security-relevant anomalies need to be wired as detections (route to observe-ready, not implement here). |
| `.observe-ready/alert-catalog.md` (or equivalent) | Step 8 (runtime), Step 13 (post-incident detection) | Existing detection rules; gaps (authentication-failure spike, authorization-failure spike, rate-limit burst, new-admin-user creation) for observe-ready to wire. |
| `.observe-ready/INDEPENDENCE.md` | Step 10 (disclosure program reachability) | Status page and disclosure inbox out-of-band status. A disclosure endpoint hosted on the infrastructure it documents is a trust-boundary leak during incidents. |
| `.repo-ready/SECURITY.md` | Step 10 (baseline disclosure) | The baseline contact-and-policy content that harden-ready extends into a full program in Step 10. |
| `.stack-ready/DECISION.md` | Step 8 (tool choice) | Chosen SAST / DAST / SCA / secret-scanner / container-scanner tools. If absent, harden-ready proposes defaults; it does not redecide. |

If an upstream artifact *contradicts* the running app, trust the running app and note the drift as a finding. Upstream artifacts are historical records; the deployed app is ground truth.

## Produces for downstream

harden-ready sits at the end of the shipping tier; its artifacts are consumed by humans (security engineers, auditors, founders), not by another suite skill. But it emits artifacts under `.harden-ready/` so the next hardening session (quarterly / post-incident / pre-audit) can resume without rediscovery.

| Artifact | Path | Purpose |
|---|---|---|
| **Hardening state** | `.harden-ready/STATE.md` | Current cycle, mode, tier reached, open findings, skill version. Next session reads first. |
| **Findings report** | `.harden-ready/FINDINGS.md` | All findings per the F-NN template. Updated as fixes land. The canonical deliverable for the auditor and the security engineer. |
| **Attack-surface inventory** | `.harden-ready/ATTACK-SURFACE.md` | Step 1 output. Stable across passes; updated on material changes to the app. |
| **Scope and ROE** | `.harden-ready/SCOPE.md` | Step 2 output. What this pass covers; threat actor model; rules of engagement. |
| **Auth verification log** | `.harden-ready/AUTH-VERIFICATION.md` | Step 4 reproduction record. |
| **API verification log** | `.harden-ready/API-VERIFICATION.md` | Step 5 reproduction record. |
| **Crypto verification log** | `.harden-ready/CRYPTO-VERIFICATION.md` | Step 6 record: primitives, KMS, IV discipline, TLS. |
| **Compliance control map** | `.harden-ready/COMPLIANCE.md` | Step 7 control-to-code mapping. One row per in-scope framework's control. Evidence path, implementer, verification date. |
| **Pen-test package** | `.harden-ready/pentest/` | Step 9 scope, ROE, pre-test baseline, vendor communication log, retest log. |
| **Disclosure program** | `.harden-ready/DISCLOSURE.md` | Step 10 policy page source; security.txt contents; triage SLA; inbox owner. |
| **Class-fix registry** | `.harden-ready/CLASS-FIXES.md` | Step 13 output. Every incident's instance / class / class-survey / class-fix / class-level guard. The antidote to CVE-of-the-week. |
| **Continuous-cadence calendar** | `.harden-ready/CADENCE.md` | Mode D trigger dates: next scanner review, next tabletop, next pen test. |

These artifacts cost nothing to emit and compound over time. The second hardening pass against the same app reads `CLASS-FIXES.md` first; any class not fixed is a repeat-violation candidate.

## Handoff: detection and fix-side work are not this skill's job

If the work is about wiring a detection (SIEM rule, Datadog monitor, Sentry alert) for an identified class of attack, delegate to `observe-ready`. harden-ready specifies the detection contract; observe-ready implements the rule.

If the work is about fixing the app's auth library, adding RBAC, rewriting a security middleware, or adding server-side authorization checks, delegate to `production-ready`. harden-ready identifies the class, files the finding, and verifies the retest; production-ready writes the code.

If the work is about rotating a secret, wiring a new vault, or changing the deploy-time secret-injection pipeline, delegate to `deploy-ready`. harden-ready verifies secrets never reach logs or bundles at runtime; deploy-ready owns the pipeline.

If the work is about setting up a SECURITY.md, branch protection, signed commits, or CI security gates, delegate to `repo-ready`. harden-ready extends SECURITY.md into a program; it does not write the baseline.

If the work is about a public disclosure of an incident (PR, blog post, launch-page banner), delegate to `launch-ready`. harden-ready coordinates the disclosure timeline with the researcher; launch-ready owns the external communication.

**If your harness exposes a skill-invocation tool** (e.g., Claude Code's Skill tool), invoke the sibling directly when the handoff trigger fires. **Otherwise**, surface the handoff to the user: "This step needs `production-ready` to wire the server-side authorization for the BOLA finding. Install it or have the engineer handle the fix separately." Do not generate a complete production-ready fix inline from this skill; the handoff is the contract.

## Session state and handoff

Hardening passes span sessions: the adversarial review takes days, the fix-and-retest loop takes weeks, the pen-test prep and retest take months, and the continuous-cadence work is ongoing. Without a state file, every resume rediscovers the attack surface from scratch, and the class-fix registry accumulates orphans.

Maintain `.harden-ready/STATE.md` at every tier boundary. Read it first on resume. If it conflicts with the running system, trust the running system and update the file.

**Template:**

```markdown
# Harden-Ready State

## Skill version
Built under harden-ready [current skill version], [frontmatter updated date]. If the agent loads a newer version on resume, re-read the changed sections before continuing.

## Mode
Mode B (pre-audit hardening). Target audit: SOC 2 Type I readiness, observation period starting 2026-06-01.

## Tier reached
Tier 2 (Audited). Target next: Tier 3 (Hardened).

## Scope
In-scope: api.example.com production, app.example.com production. Out-of-scope: staging, PR environments, internal admin tools behind corporate VPN. Threat actor: unauthenticated remote attacker, authenticated customer on multi-tenant SaaS.

## Attack-surface inventory (Step 1)
- Endpoints: 47 HTTP routes, 23 GraphQL resolvers. Enumerated in .harden-ready/ATTACK-SURFACE.md.
- Data assets: Postgres (3 schemas), S3 (user-uploads, audit-logs), Redis.
- Trust boundaries: 4 declared in ARCH.md; 1 flagged paper-trust-boundary.
- Third parties with privileged access: Stripe, SendGrid, Auth0, OpenAI.
- Users and roles: customer, admin, support, service-account. RBAC matrix in .production-ready/STATE.md.

## OWASP walkthrough (Step 3)
- Web 2021: 10/10 categories walked. Findings: 3 High, 2 Medium, 1 Low.
- API 2023: 10/10 categories walked. Findings: 1 Critical (API1 BOLA on /orders/:id), 2 Medium.
- LLM 2025: not applicable (no LLM integration).

## Findings (Step 11)
- Total: 9 (1 Critical, 3 High, 4 Medium, 1 Low).
- Status: 4 Closed, 3 In Progress, 2 Open.
- Retest state: 4/4 Closed findings retested and class-level guard landed.
- Canonical file: .harden-ready/FINDINGS.md (F-01 through F-09).

## Compliance (Step 7)
- SOC 2 CC: 41/62 controls mapped to code / config / log evidence; 9 gaps; 12 control exceptions with named risk owners.
- PCI-DSS: N/A (no cardholder data; Stripe is the PCI perimeter).
- HIPAA: N/A.
- GDPR Article 32: 6/8 sub-controls mapped; 2 gaps (encryption at rest for backups, retention policy enforcement automation).

## Responsible disclosure (Step 10)
- Policy live at /security. Yes.
- /.well-known/security.txt served. Yes.
- Triage SLA: 72h first response, 30d fix for Critical/High.
- Inbox owner: Jamie Chen (security@).
- Test email: sent 2026-04-22 14:30 UTC; replied within 41h.

## Class fixes (Step 13)
- F-03 (JWT alg-none): class = "JWT library trust in algorithm header"; class fix = pinned verifier library with algorithm allowlist; class-level guard = lint rule in CI.
- F-06 (BOLA on /orders/:id): class = "paper trust boundary at the object layer"; class fix = RLS on `orders` table + ORM wrapper enforcing tenant predicate; class-level guard = new-table RLS-required lint.

## Open questions blocking Tier 3 or Tier 4
- [open, Tier 3] F-07 (prompt-injection-via-email feature) needs architectural decision on Rule-of-Two scoping before fix can be written.
- [open, Tier 4] SOC 2 control CC8.1 (change management) evidence path is unclear; ownership TBD with platform team.

## Last session note
[2026-04-23] Completed Tier 2. Next: close F-07 architecture review with engineering; complete SOC 2 CC8 evidence mapping.
```

**Rules:**
- STATE.md is the contract with the next session. If it is out of date, the next session re-discovers the hardening posture.
- At every `/compact`, `/clear`, or context reset, update STATE.md first.
- Never delete STATE.md. If an entry is wrong, correct it in place with a dated note.
- The findings file and the class-fix registry are load-bearing across sessions. A hardening pass that resumes without them re-opens the adversarial review from scratch and loses the previous pass's class-level learning.

## Keep going until it actually survives an attacker, not just a scanner

Shipping a Semgrep green-check is roughly 10% of the work. The remaining 90% is the OWASP manual walkthrough, the auth verification, the BOLA audit against every object-scoped endpoint, the crypto primitive check, the compliance control-to-code map, the disclosure program with a named inbox owner, and the class-fix registry that compounds across incidents. Budget for all of it.

A "hardened" app is one whose findings report has every section filled, whose fixes have all retested closed, whose compliance binder has every control pointing to a specific artifact, whose disclosure email replies within SLA, and whose class-fix registry has grown since the last pass. When in doubt, open the running app in a fresh browser on a throwaway account and try to read another user's data. The first request that succeeds is the next finding to file.

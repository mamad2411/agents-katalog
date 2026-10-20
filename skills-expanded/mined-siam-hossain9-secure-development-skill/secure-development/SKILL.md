---
name: secure-development
description: >-
  Security best practices for building and reviewing software, web apps, APIs,
  and infrastructure. Use whenever writing, designing, modifying, or auditing
  code — especially anything that handles user input, authentication,
  authorization, sessions, secrets, cryptography, databases, file uploads,
  network/HTTP requests, APIs, LLM/AI features, realtime/WebSockets, payments,
  PII, deployment/cloud/containers, or when reusing/pasting code (including
  AI-generated or copied Stack Overflow snippets) — to prevent vulnerabilities (injection,
  XSS, SSRF, CSRF, IDOR/broken access control, auth flaws, secret leakage,
  prompt injection, misconfiguration) by design rather than patching them later.
  Also use for security reviews, threat modeling, and pre-ship hardening.
metadata:
  version: "1.6"
  domains: 23
---

# Secure Development

A security playbook for **building things correctly the first time**. The goal is
*secure by design*: bake the right defaults into code as it's written, not bolt
security on after a pentest. This file is the index — it routes you to a focused
reference for whatever you're touching. Pull the specific reference(s) below into
context; each is self-contained (Threats → Secure defaults → ❌/✅ code patterns →
Checklist → Red flags to grep for → Tooling & CI checks).

## Two questions that catch most vulnerabilities

Research across 20 categories of real-world breaches shows the same handful of root
causes recur. Before writing or approving any code that touches a trust boundary,
ask:

1. **Is data being treated as code?** Injection (SQL/NoSQL/OS/LDAP), SSTI, XSS,
   insecure deserialization, log injection, and LLM prompt injection are all one
   mistake: untrusted input concatenated into a string some interpreter later
   executes. Fix structurally — parameterize/bind, argv arrays (no shell), render
   data-only, keep untrusted text out of the instruction channel. Never "sanitize"
   by string-munging.
2. **Am I trusting something the attacker controls?** Authorization done in the UI,
   prices/roles read from the request body, JWT `alg` taken from the token, CORS
   `Origin` reflected, an LLM's output used as a security decision, "internal" DB
   values, archive entry names — all attacker-influenced. Re-derive every
   security-relevant value server-side from a verified principal, and check
   *per-object / per-tenant / per-field* authorization in the query itself.

If the answer to (1) is "yes" or to (2) is "I'm trusting it," stop and fix that
first — then consult the specific reference below.

## How to use this skill

1. **Before building** (design time): skim `threat-modeling-and-secure-design.md`.
   Ask: what's the trust boundary, what's the worst thing that happens here, who
   is the attacker? Pick the relevant references from the routing table below.
2. **While coding**: apply the **Golden rules** and the secure defaults from the
   matching reference. Treat every input crossing a trust boundary as hostile —
   including data from your own database, third-party APIs, and LLM output.
3. **Before shipping**: run the **Checklist** at the bottom of each reference you
   touched, and grep the codebase for that reference's **Red flags**.
4. **When reviewing code or a diff**: load the references matching what the change
   touches and audit against their checklists.
5. **Building a whole project start-to-finish?** Follow [`LIFECYCLE.md`](LIFECYCLE.md)
   — it walks the 9 build phases (plan → publish → operate), and for each phase gives
   what to do, how to prevent the failure (mapped to NIST SSDF / Microsoft SDL / SLSA /
   OWASP), which references to open, and the exit gate before you proceed. Includes
   sector-specific steps (mobile signing, ML provenance, IoT secure-boot, OSS SLSA).

If a request involves handling untrusted data, identity, secrets, or money and you
are unsure which reference applies — default to loading `threat-modeling-and-secure-design.md`
and `input-validation-and-output-encoding.md` first.

## Golden rules (always on)

1. **Never trust input** — validate on the server with allowlists; never rely on
   client-side validation. Data from your DB, partners, and LLMs is input too.
2. **Parameterize, don't concatenate** — prepared statements for SQL, argv arrays
   (no shell) for commands, never string-build queries/commands/HTML.
3. **Encode on output, per context** — HTML, attribute, JS, URL, SQL each need
   their own encoding. Let the framework auto-escape; never bypass it.
4. **Enforce authorization on the server, for every request, deny-by-default** —
   check object ownership (stops IDOR/BOLA), not just authentication.
5. **Hash passwords with Argon2id/bcrypt/scrypt; encrypt with vetted AEAD libs** —
   never MD5/SHA-1 for passwords, never roll your own crypto, use a CSPRNG.
6. **No secrets in code or git** — use env/secret managers, short-lived scoped
   tokens; rotate on leak.
7. **Fail closed** — on error, deny access and don't leak stack traces, queries,
   or internal paths to users.
8. **Least privilege everywhere** — DB users, IAM roles, API tokens, containers
   (non-root), and LLM tool access all get the minimum they need.
9. **Validate redirects, outbound URLs, and file paths** — stops open redirect,
   SSRF, and path traversal.
10. **Keep dependencies patched and pinned** — lockfiles, vuln scanning, and pin
    CI actions/base images by digest.
11. **Log security events, never log secrets/PII/tokens.**
12. **Set the security headers** — CSP, HSTS, secure cookies (`HttpOnly`,
    `Secure`, `SameSite`), correct CORS (never `*` with credentials).

## Routing table — what are you building?

| If you're working on… | Read these references |
|---|---|
| **Any feature taking user input** | `input-validation-and-output-encoding.md`, `web-application-vulnerabilities.md` |
| **A web page / frontend** | `web-application-vulnerabilities.md` (XSS), `web-security-headers-and-browser-protections.md` |
| **A REST/GraphQL API** | `api-security.md`, `authorization-and-access-control.md`, `rate-limiting-and-abuse-prevention.md` |
| **Login / signup / sessions / SSO** | `authentication.md`, `authorization-and-access-control.md` |
| **Permissions / multi-tenant / roles** | `authorization-and-access-control.md` |
| **Encryption, hashing, tokens, PII at rest** | `cryptography-and-data-protection.md`, `data-privacy-and-compliance.md` |
| **A database / SQL / NoSQL / ORM / data store** | `database-security.md`, `input-validation-and-output-encoding.md` |
| **Config, API keys, credentials** | `secrets-management.md` |
| **File uploads / archives** | `input-validation-and-output-encoding.md`, `web-application-vulnerabilities.md` |
| **Outbound HTTP / fetch-by-URL / webhooks** | `web-application-vulnerabilities.md` (SSRF), `api-security.md` |
| **Chat / notifications / live updates** | `realtime-and-websocket-security.md` |
| **LLM / chatbot / agent / RAG features** | `ai-llm-application-security.md` |
| **Payments / checkout / quotas / balances** | `business-logic-and-abuse-security.md`, `authorization-and-access-control.md` |
| **Sending email** | `email-security.md` |
| **Mobile app (iOS/Android)** | `mobile-application-security.md` |
| **Cloud / Terraform / Docker / Kubernetes** | `infrastructure-cloud-and-container-security.md`, `secrets-management.md` |
| **Adding/updating dependencies** | `dependency-and-supply-chain-security.md` |
| **CI/CD pipelines** | `secure-sdlc-and-devsecops.md`, `dependency-and-supply-chain-security.md` |
| **Logging / error handling / monitoring** | `logging-monitoring-and-error-handling.md` |
| **Anti-abuse / bot defense / rate limits** | `rate-limiting-and-abuse-prevention.md` |
| **Picking patterns for a specific stack** | `language-and-framework-pitfalls.md` |
| **Reusing pasted / AI-generated code, integrating snippets** | `secure-code-reuse-and-implementation.md` |
| **Anything new, at design time** | `threat-modeling-and-secure-design.md` |

## Full reference index

**Foundations**
- `threat-modeling-and-secure-design.md` — trust boundaries, STRIDE, least privilege, fail-closed, defense in depth.
- `input-validation-and-output-encoding.md` — the root cause of injection; validate-then-encode, parameterization.
- `language-and-framework-pitfalls.md` — per-stack insecure→secure patterns (Node, Python, Java, Go, PHP, Rails, .NET, React/Angular/Vue).
- `secure-code-reuse-and-implementation.md` — insecure copy-paste, AI-generated code & slopsquatting, wrong control implementations, integration/type-confusion bugs, dead/debug code shipped to prod.

**Web & API**
- `web-application-vulnerabilities.md` — OWASP Top 10: XSS, injection, SSRF, CSRF, IDOR, path traversal, upload, deserialization, SSTI, request smuggling, cache poisoning.
- `api-security.md` — OWASP API Top 10: BOLA/BFLA, mass assignment, rate limiting, REST vs GraphQL, webhooks.
- `web-security-headers-and-browser-protections.md` — CSP, CORS, cookies, HSTS, clickjacking, SRI, COOP/COEP.
- `realtime-and-websocket-security.md` — CSWSH, handshake + per-message authz, realtime DoS.

**Identity & access**
- `authentication.md` — password hashing, MFA/passkeys, sessions, JWT, OAuth2/OIDC, account recovery.
- `authorization-and-access-control.md` — server-side enforcement, RBAC/ABAC/ReBAC, IDOR, multi-tenancy, deny-by-default.

**Data protection**
- `cryptography-and-data-protection.md` — TLS, AEAD, key management/KMS, CSPRNG, constant-time compare, PII.
- `secrets-management.md` — no hardcoded secrets, vaults, rotation, leak response, CI secrets.
- `data-privacy-and-compliance.md` — data minimization, GDPR/CCPA duties, retention, pseudonymization.
- `database-security.md` — least-privilege DB accounts, never-public exposure, TLS-to-DB, encryption at rest, RLS/tenant isolation, query caps, backup security.

**Abuse & logic**
- `rate-limiting-and-abuse-prevention.md` — algorithms, keying behind proxies, fail-closed, anti-automation.
- `business-logic-and-abuse-security.md` — idempotency, replay, race conditions, price/quantity tampering.
- `ai-llm-application-security.md` — prompt injection (direct/indirect), excessive agency, insecure output handling.

**Platform & delivery**
- `infrastructure-cloud-and-container-security.md` — IAM least privilege, container hardening, K8s, IaC, IMDSv2, subdomain takeover.
- `dependency-and-supply-chain-security.md` — vuln scanning, lockfiles, SBOM, signing, typosquatting.
- `mobile-application-security.md` — secure storage, cert pinning, deep links, WebView hardening (OWASP MASVS).
- `email-security.md` — SPF/DKIM/DMARC, header/SMTP injection.

**Operations**
- `logging-monitoring-and-error-handling.md` — security logging, no secrets in logs, error hygiene, audit trails.
- `secure-sdlc-and-devsecops.md` — shift-left, SAST/DAST/SCA, pre-commit hooks, CI security gates.

## Pre-ship security checklist (quick pass)

- [ ] All user/external/LLM input validated server-side; queries parameterized; output context-encoded.
- [ ] Every endpoint enforces authentication **and** object-level authorization (no IDOR).
- [ ] Passwords hashed with Argon2id/bcrypt; secrets out of code; TLS enforced; vetted crypto only.
- [ ] Security headers + secure cookies set; CORS not wildcard-with-credentials.
- [ ] Outbound URLs / redirects / file paths validated (SSRF, open redirect, traversal).
- [ ] Rate limiting + abuse controls on auth and expensive/sensitive endpoints.
- [ ] No secrets/PII in logs; errors fail closed without leaking internals.
- [ ] Dependencies scanned and pinned; CI tokens least-privilege.
- [ ] If it uses an LLM: untrusted output is sandboxed/sanitized; tools are least-privilege; high-impact actions need confirmation.
- [ ] Threat-modeled the feature; ran the relevant reference checklists above.
- [ ] Automated detection in place — wired the matching scanners / CI gates from each touched reference's **Tooling & CI checks** section (don't rely on manual review alone).

---

*Provenance:* the reference set was researched, validated, and hardened against two
deep-research passes:
[`research/REAL-WORLD-SECURITY-RESEARCH.md`](research/REAL-WORLD-SECURITY-RESEARCH.md)
— a 20-category study of real-world developer security failures and their
cross-cutting root causes — and a separate 18-domain structured dataset whose
durable defaults, controls, detection tools, and CI checks were folded into every
reference file. The `## Real-world incidents` examples were each fact-checked via
web search and adversarially re-verified; any claim that could not be corroborated
(or was exaggerated) was dropped, so only sourced, confirmed incidents remain.

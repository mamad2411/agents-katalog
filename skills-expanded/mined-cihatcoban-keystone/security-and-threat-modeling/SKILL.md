---
name: security-and-threat-modeling
description: Threat-models and hardens a change - untrusted input, authentication, authorization, supply chain, personal data. Triggers - is this endpoint secure, threat-model this feature, we are storing personal data here, injection, permissions, OWASP, vulnerability, login and session cookies, CSRF.
---

# Security and Threat Modeling

Security is a property of decisions made throughout a change, not a scan run
after it. The scan finds known patterns; it does not find the authorization
check you forgot, which is the most common serious flaw in real systems.

## Threat model in ten minutes

For any non-trivial change, answer four questions in writing:

1. **What are we protecting?** Data, money, availability, reputation.
2. **Who would attack it?** External anonymous, authenticated user of another
   tenant, malicious insider, compromised dependency, a bored person with a
   proxy.
3. **Where are the entry points?** Every place data crosses a trust boundary:
   HTTP handlers, queue consumers, file uploads, webhooks, CLI arguments,
   environment, deserializers, third-party callbacks.
4. **What happens if each is abused?** Use STRIDE as the prompt list —
   **S**poofing, **T**ampering, **R**epudiation, **I**nformation disclosure,
   **D**enial of service, **E**levation of privilege.

Write the outcome in the spec or the PR. Ten minutes of this beats an hour of
scanning.

## Input: the boundary is the only safe place

Treat all external data as hostile — including data from your own other
services, and data already in your database (it got there somehow).

| Risk | Control |
|---|---|
| SQL/NoSQL injection | Parameterized queries only. Never build a query by string concatenation, including identifiers and `ORDER BY` — allow-list those |
| Command injection | No shell interpolation; pass an argument array |
| Path traversal | Never use a client-supplied name as a path; generate your own |
| SSRF | Allow-list destination hosts; re-validate after **every** redirect; block link-local and private ranges |
| Deserialization | Never deserialize untrusted data into arbitrary types; use a schema |
| XXE / entity expansion | Disable external entities and DTDs in every XML parser |
| Resource exhaustion | Cap request size, array length, string length, nesting depth, regex complexity, parse time |
| XSS | Context-aware escaping by the template engine; sanitize with an allow-list if HTML must render |

**Validate structure and range at the boundary; escape at the point of use.**
Sanitizing early and escaping never is how encoding bugs become vulnerabilities.

## Authorization is where real breaches live

Injection is well-tooled; broken access control is not.

- Check authorization **on every request at the data-access layer**, not in the
  UI and not only in the route. The UI hides a button; it does not protect a row.
- Object-level checks: "can this user act on *this* record?" Missing this is the
  most common critical flaw in APIs — an id in a URL is not an authorization.
- Deny by default. A new endpoint should be unreachable until explicitly opened.
- Multi-tenant: the tenant filter belongs in one enforced layer, not in each
  query where it can be forgotten once.
- Re-check on state change; permissions granted at login may have been revoked.

## Secrets

Configuration and `.env` handling, provider API keys and keeping secrets out of
agents' context are covered in depth by `configuration-and-secrets`.

- Zero secrets in the repository, including tests, examples and history.
  `.env.example` lists key names with empty values.
- Inject at runtime from a secret manager or the platform's mechanism.
- Scanner in pre-commit **and** CI; human discipline is not a control.
- On exposure: **rotate first**, then clean history. A secret pushed to a
  public remote is compromised permanently — history rewriting does not
  un-copy it.
- Never log secrets, tokens, or full payment/identity data. Redact at the
  logger, not at every call site.

## Supply chain

- Pin versions with a lockfile; reproducible installs.
- Automated vulnerability scanning in CI; zero known high/critical.
- Review new dependencies before adding (`dependency-and-license-policy`).
- Pin CI actions/images by digest — a mutable tag in a pipeline with secrets is
  a supply-chain hole.
- Verify checksums for model weights, binaries and datasets.

## Personal data

- **Minimize**: the field you do not store cannot leak. Default to not
  collecting.
- Inventory what you store, why, the lawful basis, and the retention period.
- Encrypt in transit always; at rest for sensitive categories.
- Keep it out of logs, error trackers, analytics and LLM prompts.
- Make erasure and export mechanically possible, not a manual archaeology
  project.
- Cross-border transfer is a legal question, not a technical one — flag it.

## Verification

Scanners are necessary and insufficient. Add:

- A test per authorization rule — including the negative case (user B cannot
  read user A's record). These are cheap and catch the expensive class.
- A test that malformed input is rejected with a safe error
- A test that the error path leaks nothing (no stack trace, no internal ids)

## Verification recipes

Each class of flaw has a cheap test shape that fails when the defense is
missing. Write the negative case; the happy path already has tests.

| Flaw | Test shape |
|---|---|
| Object-level authorization (IDOR) | Create a record as user A; request it as user B → 403/404, and the response body holds none of A's fields |
| Mass assignment | Send a field the caller must not set (`role`, `owner_id`, `price`) → ignored or rejected; read back to prove it |
| Injection | Send `'`, `"`, `;`, `--`, `$(`, `{{`, `../` through every input of the endpoint → safe error, no change in stored data |
| Path traversal | Ask for `../../etc/passwd` and an absolute path → refused before any file is opened |
| SSRF | Make the server fetch `http://169.254.169.254/` and `http://localhost` → refused |
| Authentication | Expired, malformed, wrong-audience and unsigned tokens → 401; no endpoint reachable without one unless listed as public |
| Rate and size limits | Exceed the limit → 429 or 413, and the service still serves others |
| Output encoding | Store `<script>` and `"><img onerror=…>`; render it → shown as text |

Run these at the API boundary, not against an inner function: a defense that
lives one layer too deep is the usual bug.

For anything a browser or a login touches — password hashing parameters,
session cookies, CSRF, CORS, security headers, uploads — the values and the
test for each are in `references/web-session-controls.md`.

## Tool discovery

Use the scanners the project already has before proposing new ones. Look in
CI config, `Makefile`, package scripts and pre-commit for: a secret scanner
(gitleaks, trufflehog), a dependency scanner (osv-scanner, `npm audit`,
pip-audit, `cargo audit`, govulncheck, trivy), and a static analyzer (semgrep,
CodeQL, the language's security linter). Run what exists, report what is
missing, and record the commands in the `security` row of `CONSTRAINTS.md`'s
verification table so `/verify` runs them. A scanner nobody runs is a claim.

## OWASP ASVS mapping

ASVS 5.0 is the checklist to grade against when a customer or auditor asks.
This skill's sections map onto it:

| This skill | ASVS 5.0 chapters |
|---|---|
| Input | V1 Encoding and Sanitization, V2 Validation and Business Logic, V5 File Handling |
| Authorization | V8 Authorization, V4 API and Web Service |
| Authentication and sessions | V6 Authentication, V7 Session Management, V9 Self-contained Tokens, V10 OAuth and OIDC |
| Secrets, supply chain | V13 Configuration, V15 Secure Coding and Architecture |
| Personal data | V14 Data Protection, with `references/privacy-compliance.md` |
| Errors and logging | V16 Security Logging and Error Handling |
| Transport, crypto | V12 Secure Communication, V11 Cryptography |

Pick the level deliberately: L1 for most internet-facing services, L2 for
anything holding personal or financial data, L3 for high-assurance systems.

## Exit checklist

- [ ] Trust boundaries identified; STRIDE prompts answered in writing
- [ ] All external input validated for structure and bounds at the boundary
- [ ] Every query parameterized; no dynamic SQL from input
- [ ] Authorization enforced at the data layer, including object-level checks
- [ ] Negative authorization tests exist
- [ ] No secrets in the repository; scanner active; rotation path known
- [ ] Dependencies pinned and scanned; zero known high/critical
- [ ] Personal data minimized, inventoried, excluded from logs
- [ ] Errors reveal nothing internal
- [ ] Browser and authentication controls match
      `references/web-session-controls.md`, each with its test

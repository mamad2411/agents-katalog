---
name: owasp-coverage
description: Use this skill when running a security audit, performing a security gate on code review, threat-modeling an AI/LLM component, or verifying audit coverage against the canonical OWASP categories — the OWASP Web Top 10 (2021) and OWASP GenAI/LLM Top 10 (2025) reference catalog with per-category descriptions and mitigation patterns. Covers broken access control, cryptographic failures, injection, insecure design, security misconfiguration, vulnerable components, auth failures, integrity failures, logging/monitoring failures, SSRF; and LLM01 prompt injection, LLM02 sensitive info disclosure, LLM03 supply-chain, LLM04 model poisoning, LLM05 improper output handling, LLM06 excessive agency, LLM07 system prompt leakage, LLM08 vector/embedding weaknesses, LLM09 misinformation, LLM10 unbounded consumption.
disable-model-invocation: true
---

# OWASP Coverage

OWASP maintains two top-10 catalogs relevant to modern application security: the long-standing Web Application Top 10 (2021 is the current edition) and the GenAI/LLM Top 10 (2025) for AI-integrated systems. Any security audit or security gate that touches AI/LLM components must cover both.

## OWASP Top 10 Web Application Security Risks (2021)

The 2021 edition is the current canonical reference until OWASP publishes a new edition.

| # | Category | What it covers | Common mitigations |
|---|---|---|---|
| A01 | Broken access control | Missing authorization, IDOR, privilege escalation, CORS misconfig | Deny-by-default, server-side enforcement, RBAC/ABAC, owner checks on every resource |
| A02 | Cryptographic failures | Weak/absent encryption, weak hashing, plaintext PII | TLS 1.2+, AES-GCM, Argon2id/bcrypt for passwords, no MD5/SHA1 for security, rotate keys |
| A03 | Injection | SQLi, NoSQLi, command injection, LDAP, XSS | Parameterized queries, ORM, input validation, contextual output encoding, CSP for XSS |
| A04 | Insecure design | Missing threat model, missing rate limits, business-logic flaws | Threat modeling, secure design patterns, abuse-case testing |
| A05 | Security misconfiguration | Default creds, verbose errors, missing hardening, open S3 buckets | Hardening baselines, CIS benchmarks, infra-as-code review, least-privilege defaults |
| A06 | Vulnerable and outdated components | Known-CVE libs, EOL runtimes, unpatched base images | SCA (Snyk/osv-scanner/Trivy), dependency pinning, automated update PRs, EPSS/KEV gating |
| A07 | Identification and authentication failures | Weak passwords, missing MFA, session fixation, credential stuffing | MFA, rate-limit auth, strong session IDs, secure cookies, lockout policies |
| A08 | Software and data integrity failures | Unsigned artifacts, insecure deserialization, CI/CD tampering | Sigstore Cosign, SLSA provenance, signed releases, safe deserialization |
| A09 | Security logging and monitoring failures | No audit log, no alerting, no incident detection | Structured audit logs, SIEM, alerting on anomalies, log integrity protection |
| A10 | Server-side request forgery (SSRF) | Server fetches attacker-controlled URLs, cloud-metadata access | URL allowlists, block link-local/metadata IPs, network egress policy |

## OWASP GenAI / LLM Top 10 (2025)

Applies to any AI/LLM component: agent harness, prompt template, LLM API integration, RAG pipeline, vector store, agentic workflow.

| # | Category | What it covers | Common mitigations |
|---|---|---|---|
| LLM01 | Prompt injection (direct + indirect) | Attacker controls input or retrieved content to override system instructions | Untrusted-content wrapping, system/user separation, output validation, allowlist tool use |
| LLM02 | Sensitive information disclosure | Model emits PII, secrets, training data, or system prompts | Output filtering, redaction, data minimization at training/RAG ingest |
| LLM03 | Supply-chain vulnerabilities (model + data) | Poisoned models, tampered training data, malicious adapters | Signed models, provenance attestation, verified registries, integrity hashes |
| LLM04 | Data and model poisoning | Adversarial fine-tune data, RAG corpus tampering | Source vetting, data integrity checks, evaluation drift monitoring |
| LLM05 | Improper output handling | Treating model output as trusted; emitting unsanitized HTML/code/SQL | Encode/sanitize at sink, never `eval()` model output, sandbox executed code |
| LLM06 | Excessive agency | Agent has more tools/permissions than needed; over-broad write access | Tool allowlists, least-privilege scopes, human-in-the-loop for destructive ops |
| LLM07 | System prompt leakage | System prompt extracted via prompt injection or model behavior | No secrets in system prompt, separate config from prompt, treat as semi-public |
| LLM08 | Vector and embedding weaknesses | RAG corpus injection, embedding inversion, cross-tenant leakage | Tenant isolation, ACL at retrieval, embedding-content validation, query filtering |
| LLM09 | Misinformation | Hallucinated facts, fabricated citations, over-confident output | Citations + grounding, RAG with verified sources, confidence calibration, user disclosure |
| LLM10 | Unbounded consumption | Token/cost/compute exhaustion via crafted inputs | Per-user quotas, max-token limits, rate limits, cost monitoring |

Cite the v2025 OWASP LLM PDF: https://genai.owasp.org/llm-top-10/ for traceability.

## Special-case mitigation patterns

### Prompt injection (LLM01) — untrusted content wrapping

Wrap any model-retrieved or user-supplied text in clear delimiters and instructions that downstream content is data, not instructions. Validate the model's response against the expected shape (JSON schema, regex, tool-call structure). The `untrusted-content-wrapping` rule in this plugin enforces this for subagent spawns.

### Excessive agency (LLM06) — least-privilege tools

Default to read-only tool surfaces for any agent processing untrusted input. The `security-engineer` agent in this plugin is read-only by frontmatter (`disallowedTools: Write, Edit`). Write/Edit access requires an explicit phase with user approval.

### Supply-chain failures (A08 / LLM03)

Treat artifact integrity and model provenance the same: signed artifacts (Cosign), build provenance (SLSA), and signed model attestations. See `@supply-chain-security` for tooling detail.

## When this applies

| Workflow | Apply this knowledge |
|---|---|
| `/security-audit` | Verify findings cover all 10 web categories; if any AI/LLM component is present, also verify all 10 GenAI categories |
| `/code-review` (security gate) | Spot-check line-level changes against most-likely categories (A01, A03, A05, A07 for typical web code; LLM01, LLM05, LLM06 for agent code) |
| `/security-scan` | Map scanner findings (Semgrep, Snyk, osv-scanner) to the OWASP categories so the report speaks the canonical language |
| `/architecture-design` (security review step) | Threat-model the design against each category; flag missing controls (e.g., no rate limiting → A04 insecure design + LLM10 unbounded consumption) |

## Integration

- **Used by**: `/security-audit`, `/code-review`, `/security-scan`, `/architecture-design`
- **Companion knowledge**: `@supply-chain-security` (depth on A06 + A08 + LLM03), `prompt-engineering` (LLM01 mitigation patterns), `context-engineering` (untrusted-content wrapping)
- **External references**:
  - OWASP Web Top 10 (2021): https://owasp.org/Top10/
  - OWASP GenAI/LLM Top 10 (2025): https://genai.owasp.org/llm-top-10/
  - NIST SP 800-53 control mapping: https://nvd.nist.gov/800-53
  - OpenSSF Scorecard: https://securityscorecards.dev

---
name: security-review
description: Security analysis for code changes and requests. Classifies activities as permitted, forbidden, or requiring authorization context. Covers OWASP risks, boundary validation, and dual-use tool guidance. Use when reviewing code for security, handling security-related requests, performing threat modeling, or when asked to assess security posture.
user-invocable: true
---

# Security Review

CRITICAL: Every security assessment must classify the activity BEFORE providing assistance. If the classification is ambiguous, ask for authorization context.

## Activity Classification

### Permitted — Assist Freely
- **Authorized security testing**: Pentesting with explicit scope, red team exercises, bug bounty programs
- **Defensive security**: Hardening, vulnerability patching, security monitoring, incident response
- **CTF challenges**: Capture-the-flag competitions and training exercises
- **Educational**: Explaining attack vectors, demonstrating vulnerabilities in controlled environments, security training materials
- **Code review**: Identifying vulnerabilities in the user's own code

### Forbidden — Refuse
- **Destructive techniques**: Malware creation, ransomware, wipers
- **Denial of service**: DoS/DDoS attacks, resource exhaustion against production systems
- **Mass targeting**: Credential stuffing at scale, spam infrastructure, mass exploitation
- **Supply chain compromise**: Backdooring dependencies, typosquatting packages, poisoning build pipelines
- **Detection evasion for malicious purposes**: Obfuscation specifically to evade security controls for unauthorized access

### Context Required — Ask Before Assisting
Dual-use security tools and techniques require clear authorization context:
- C2 frameworks (Cobalt Strike, Metasploit)
- Credential testing tools
- Exploit development and proof-of-concept code
- Network scanning and reconnaissance tools
- Reverse engineering and binary analysis

Acceptable contexts: pentesting engagements, CTF competitions, security research, defensive use cases. If the user hasn't established context, ask: "What's the authorization context for this? (e.g., pentest engagement, CTF, security research)"

## Code Security Checklist

When reviewing code for security, check these categories systematically:

### Input Validation & Injection
- **SQL injection**: Parameterized queries, not string concatenation
- **Command injection**: No user input in shell commands without sanitization; prefer APIs over `exec`/`spawn` with user data
- **XSS**: Output encoding for HTML contexts; Content Security Policy headers
- **Path traversal**: Validate and canonicalize file paths; reject `../` sequences
- **Template injection**: No user input in template strings evaluated server-side
- **Deserialization**: No untrusted data in `eval()`, `pickle.loads()`, `JSON.parse()` of unvalidated input used to construct objects

### Authentication & Authorization
- Session tokens: sufficient entropy, secure flags (HttpOnly, Secure, SameSite)
- Password storage: bcrypt/scrypt/argon2, never plaintext or reversible encryption
- Authorization checks: on every request, not just UI-level gating
- Token expiration and rotation
- Rate limiting on auth endpoints

### Payment Processing
- Never generate custom credit card handling logic — no raw card numbers, CVVs, or custom tokenization. Flag any code that touches PAN data directly.
- Mandate established payment processors (Stripe, Braintree, Square, RevenueCat) with their official SDKs. Custom payment flows violate PCI-DSS unless the project has explicit SAQ-D certification.
- Verify that client-side payment forms use processor-hosted elements (Stripe Elements, Braintree Drop-in) rather than plain `<input>` fields that touch card data.

### Webhook Validation
- Any incoming webhook endpoint must verify the sender's cryptographic signature before processing the payload (e.g., Stripe's `webhook-signature`, Slack's `X-Slack-Signature`, GitHub's `X-Hub-Signature-256`).
- Flag webhook handlers that parse and act on payloads without signature verification — an unsigned webhook endpoint is an unauthenticated API.
- Verify that webhook secrets are loaded from environment variables, not hardcoded.

### Data Protection
- Secrets not hardcoded in source (API keys, passwords, tokens)
- Sensitive data not logged (passwords, tokens, PII)
- HTTPS enforced for all external communication
- Encryption at rest for sensitive fields
- No secrets in client-side code or public assets

### System Boundaries
- Validate at system boundaries: user input, external APIs, file uploads, webhook payloads
- Don't validate for scenarios that can't happen — trust internal code and framework guarantees
- Treat all data crossing a trust boundary as untrusted until validated
- Validate schema/shape, not just presence

### Dependencies
- Known vulnerabilities in dependencies (`npm audit`, `pip audit`, `cargo audit`)
- Dependency pinning to avoid supply chain drift
- Minimal dependency surface — fewer deps = smaller attack surface

## Boundary Analysis Framework

For any change touching a trust boundary:

1. **Identify the boundary**: Where does trusted code meet untrusted input?
2. **Enumerate inputs**: What data crosses this boundary? (form fields, headers, query params, file contents, API responses)
3. **Check validation**: Is each input validated for type, length, format, and allowed values?
4. **Check encoding**: Is output properly encoded for its context? (HTML, SQL, shell, URL)
5. **Check authorization**: Does the operation verify the caller has permission?
6. **Check error handling**: Do errors leak internal details? (stack traces, file paths, SQL queries)

## Output Format

For each finding:
```
### Finding: [title]
**Severity**: CRITICAL / HIGH / MEDIUM / LOW / INFO
**Location**: file:line
**Issue**: What the vulnerability is
**Impact**: What an attacker could do
**Fix**: Specific remediation
```

End with a summary verdict:
- **SECURE**: No findings above INFO
- **ISSUES FOUND**: List severity counts (e.g., 1 HIGH, 2 MEDIUM)

CRITICAL REMINDER: Classify the activity first. Refuse forbidden activities. Require authorization context for dual-use tools. Check system boundaries, not internal code paths.

## Related Skills

- Use `code-verification` patterns to prove security fixes actually work (e.g., curl with malicious input after patching).
- Use `codebase-exploration` patterns to trace data flow across trust boundaries.
- Security findings often feed into `architectural-planning` for systemic fixes.

## Project Customization

If `user-config.md` exists alongside this file, read it and let its contents override or extend the defaults above. Common customizations:
- Project-specific security requirements (compliance frameworks, security policies)
- Known trust boundaries and their expected validation
- Security scanning tools configured for the project
- Domain-specific threat model (e.g., financial, healthcare, infrastructure)

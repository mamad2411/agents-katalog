---
name: llm-security-review
description: "Reviews LLM integration code for OWASP LLM Top 10 (2025) vulnerabilities per CSA §2.6. USE FOR: reviewing AI/LLM integration code, checking for prompt injection risks, validating LLM output handling, auditing LLM permissions and agency, checking rate limits on inference. DO NOT USE FOR: general API security (use api-security-review), non-LLM code review (use appsec-review)."
---

# LLM Security Review Skill

You are an AI/LLM security specialist. When invoked, review LLM integration code against the **OWASP LLM Top 10 (2025)** and **CSA Secure Vibe Coding Guide §2.6**.

## Review Checklist

### LLM01: Prompt Injection
- [ ] User inputs are not passed directly into system prompts without sanitization
- [ ] Input filtering strips or escapes prompt manipulation attempts
- [ ] Output format validation ensures responses adhere to expected schemas
- [ ] Separate system prompts from user content with clear delimiters
- [ ] Defense-in-depth: multiple validation layers, not just prompt engineering

### LLM02: Sensitive Information Disclosure
- [ ] No PII, secrets, or internal data in system prompts
- [ ] Training/fine-tuning data sanitized of sensitive information
- [ ] LLM outputs filtered to redact sensitive patterns (SSN, credit cards, secrets)
- [ ] Access controls limit what data the LLM can retrieve from connected systems

### LLM03: Supply Chain
- [ ] Model sources verified and documented
- [ ] Model integrity checked (checksums, signatures)
- [ ] Third-party plugins/extensions vetted before use
- [ ] Model inventory maintained with versions and provenance

### LLM04: Data & Model Poisoning
- [ ] Training data sources validated and tracked
- [ ] Output anomaly detection in place
- [ ] Model behavior monitored for drift or unexpected changes
- [ ] Sandboxing prevents poisoned outputs from affecting critical systems

### LLM05: Improper Output Handling
- [ ] LLM outputs treated as untrusted (zero-trust approach)
- [ ] Outputs sanitized before rendering in HTML (prevent XSS)
- [ ] Outputs validated before use in code execution, database queries, or system commands
- [ ] Output encoding applied per context (HTML, SQL, shell)

### LLM06: Excessive Agency
- [ ] LLM tool/function access limited to minimum required
- [ ] High-impact actions require human approval (confirmation step)
- [ ] Permissions scoped per-request, not blanket access
- [ ] Audit trail for all LLM-initiated actions

### LLM07: System Prompt Leakage
- [ ] System prompts contain no secrets, credentials, or API keys
- [ ] Anti-extraction instructions present (though not solely relied upon)
- [ ] Security controls enforced independently of the system prompt
- [ ] System prompt content not exposed in error messages or debug output

### LLM08: Vector & Embedding Weaknesses
- [ ] Fine-grained access controls on vector stores (per-user, per-role)
- [ ] Data sources for embeddings validated and trusted
- [ ] Vector store queries filtered to prevent unauthorized data retrieval
- [ ] Embedding pipelines sanitize input data

### LLM09: Misinformation
- [ ] RAG (Retrieval-Augmented Generation) used with verified data sources
- [ ] Outputs marked as AI-generated where appropriate
- [ ] Human oversight/review for high-stakes outputs
- [ ] Confidence scoring or uncertainty indicators provided

### LLM10: Unbounded Consumption
- [ ] Rate limits on inference endpoints (per user, per API key)
- [ ] Token/cost quotas per user and per time period
- [ ] Request timeouts configured
- [ ] Resource usage monitored with alerts for anomalies
- [ ] Input token limits enforced

## Output

For each finding:
- **LLM ID**: OWASP LLM Top 10 identifier (LLM01–LLM10)
- **Severity**: Critical / High / Medium / Low
- **Location**: File and line
- **Issue**: Description of the vulnerability
- **Fix**: Specific code or architectural recommendation

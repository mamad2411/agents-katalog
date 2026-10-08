---
name: owasp-ai-testing
description: AI trustworthiness testing using OWASP AI Testing Guide v1. Execute 32 test cases across 4 layers (Application, Model, Infrastructure, Data) with practical payloads and remediation.
---

# OWASP AI Testing Guide

This skill enables AI agents to perform **systematic trustworthiness testing** of AI systems using the **OWASP AI Testing Guide v1**, published November 2025 by the OWASP Foundation.

The AI Testing Guide is the industry's first open standard for AI trustworthiness testing. Unlike vulnerability lists that identify WHAT risks exist, this guide provides a practical, repeatable methodology for HOW to test AI systems. It establishes 32 test cases across 4 layers, each with objectives, payloads, observable responses, and remediation guidance.

The guide's core principle: **"Security is not sufficient, AI Trustworthiness is the real objective."** AI systems fail for reasons beyond traditional security, including bias, hallucinations, misalignment, opacity, and data quality issues.

Use this skill to execute comprehensive AI testing, validate trustworthiness controls, prepare for audits, and build repeatable test suites for AI systems.

Combine with "OWASP LLM Top 10" for vulnerability identification, "NIST AI RMF" for risk management, or "ISO 42001 AI Governance" for governance compliance.

## When to Use This Skill

Invoke this skill when:
- Performing penetration testing of AI/ML systems
- Validating AI trustworthiness before production deployment
- Building automated test suites for AI applications
- Conducting red-team exercises against AI features
- Preparing for AI security audits or certifications
- Testing RAG systems, chatbots, agents, or ML pipelines
- Evaluating model robustness and adversarial resistance
- Assessing data quality, bias, and privacy compliance
- Validating AI supply chain security
- Testing after model updates, fine-tuning, or data changes

## Inputs Required

When executing this testing guide, gather:

- **ai_system_description**: Description of the AI system (type, purpose, architecture, models used) [REQUIRED]
- **system_architecture**: Technical architecture (APIs, models, vector stores, plugins, data pipelines) [OPTIONAL but recommended]
- **testing_scope**: Which layers to test (Application, Model, Infrastructure, Data, or All) [OPTIONAL, defaults to All]
- **model_details**: Model provider, version, fine-tuning details, hosting (cloud/self-hosted) [OPTIONAL]
- **data_details**: Training data sources, vector databases, data pipelines [OPTIONAL]
- **existing_controls**: Current security and trustworthiness measures [OPTIONAL]
- **risk_context**: Data sensitivity, regulatory requirements, deployment context [OPTIONAL]
- **testing_authorization**: Explicit authorization, environment, and boundaries for active testing [REQUIRED for live or active tests]
- **safe_testing_mode**: documentation-only, staging, production-readonly, or production-approved [OPTIONAL, defaults to documentation-only unless authorization is clear]

## Authorized Testing Boundary

Only run active tests on systems the user owns or is explicitly authorized to test. If `testing_authorization` is absent or ambiguous, limit the work to architecture review, checklist assessment, and safe hypothetical payload examples.

For production systems:
- Prefer read-only validation or a staging environment
- Do not attempt destructive, persistence, denial-of-service, or data-exfiltration tests unless written authorization and scope are explicit
- Redact credentials, secrets, PII, and sensitive outputs in reports
- Stop and report if testing crosses the approved scope

---

## The 4-Layer Testing Framework

The OWASP AI Testing Guide organizes 32 test cases across four layers:

```
┌─────────────────────────────────────────┐
│        AI Application Layer             │
│   (AITG-APP-01 to AITG-APP-14)         │
│   Prompts, interfaces, outputs, agency  │
├─────────────────────────────────────────┤
│        AI Model Layer                   │
│   (AITG-MOD-01 to AITG-MOD-07)         │
│   Robustness, alignment, privacy       │
├─────────────────────────────────────────┤
│        AI Infrastructure Layer          │
│   (AITG-INF-01 to AITG-INF-06)         │
│   Supply chain, resources, boundaries  │
├─────────────────────────────────────────┤
│        AI Data Layer                    │
│   (AITG-DAT-01 to AITG-DAT-05)         │
│   Training data, privacy, diversity    │
└─────────────────────────────────────────┘
```

---

## Test Cases

The guide defines **32 test cases** across the four layers. Each case includes an objective,
payloads/procedure, observable responses, severity guidance, and remediation. The full catalog
— with payloads and a P0–P2 priority index — is in
**[`references/test-cases.md`](references/test-cases.md)**. Read the layer section you are
testing rather than loading all 32 at once.

| Layer | Prefix | Cases | Focus |
|-------|--------|-------|-------|
| 1. Application | AITG-APP | 14 | Prompts, interfaces, outputs, agency |
| 2. Model | AITG-MOD | 7 | Robustness, alignment, privacy |
| 3. Infrastructure | AITG-INF | 6 | Supply chain, resources, boundaries |
| 4. Data | AITG-DAT | 5 | Training data, privacy, diversity |

Select cases by system type (see Step 1 of the procedure): LLM/chatbot → all APP + INF-01/02/03;
ML classifier → all MOD + DAT-03/04; RAG → APP-02/03/08 + DAT-01/02; agent → APP-06 + INF-03/04;
always include DAT-05 (privacy/consent).

---

## Testing Procedure

### Step 1: Scope and Planning (15 minutes)

1. **Understand the system:**
   - Review `ai_system_description` and `system_architecture`
   - Identify AI components, data flows, and trust boundaries
   - Determine applicable test cases based on system type

2. **Select test cases:**
   - For LLM/chatbot systems: Prioritize AITG-APP (all), AITG-INF-01/02/03
   - For ML classifiers: Prioritize AITG-MOD (all), AITG-DAT-03/04
   - For RAG systems: Prioritize AITG-APP-02/03/08, AITG-DAT-01/02
   - For AI agents: Prioritize AITG-APP-06, AITG-INF-03/04
   - For all systems: Include AITG-DAT-05 (privacy compliance)

3. **Prepare test environment:**
   - Identify testing tools and frameworks
   - Set up monitoring and logging
   - Establish baseline measurements

### Step 2: Execute Test Cases (60-90 minutes)

Execute selected test cases layer by layer:

**Application Layer** (25-35 min)
- Run AITG-APP tests based on system type
- Document findings with evidence (screenshots, logs, payloads)
- Note severity and exploitability for each finding

**Model Layer** (15-20 min)
- Run AITG-MOD tests for robustness and alignment
- Document behavioral anomalies
- Test adversarial resistance

**Infrastructure Layer** (10-15 min)
- Run AITG-INF tests for supply chain and boundaries
- Verify integrity controls
- Test resource limits

**Data Layer** (10-20 min)
- Run AITG-DAT tests for privacy and quality
- Audit data governance
- Verify compliance controls

### Step 3: Risk Assessment (15 minutes)

Score each finding:

| Severity | Description | Response Time |
|---|---|---|
| **Critical** | Exploitable vulnerability with high impact | Immediate |
| **High** | Significant risk, moderate exploitation difficulty | 7 days |
| **Medium** | Moderate risk, requires specific conditions | 30 days |
| **Low** | Minor risk, limited impact | 90 days |
| **Info** | Observation, no immediate risk | Backlog |

### Step 4: Report Generation (20 minutes)

Compile findings into structured report.

---

## Output Format

Compile results into the OWASP AI Testing assessment report. The copy-ready template is in
**[`references/report-template.md`](references/report-template.md)**.

The report covers:

1. **Executive Summary** — overall trustworthiness rating, test coverage table (executed/pass/fail/N-A per layer), critical findings
2. **Detailed Test Results** — per-case result (PASS/FAIL/PARTIAL/N/A), severity, evidence, finding, recommendation
3. **Remediation Roadmap** — phased by severity (Critical 0–7d / High 7–30d / Medium 30–90d)
4. **Trustworthiness Assessment** — status across Security, Fairness, Privacy, Reliability, Explainability, Safety
5. **Next Steps** — remediation, retesting, CI/CD integration, continuous monitoring

---

## Resources

- [OWASP AI Testing Guide](https://owasp.org/www-project-ai-testing-guide/)
- [OWASP GenAI Security Project](https://genai.owasp.org/)
- [OWASP AI Testing Guide GitHub](https://github.com/OWASP/www-project-ai-testing-guide)

---

## Best Practices

1. **Test early and often**: Integrate AI testing into development lifecycle
2. **Layer your testing**: Cover all 4 layers, not just application
3. **Automate where possible**: Build repeatable test suites in CI/CD
4. **Think like an attacker**: Use adversarial mindset for test design
5. **Beyond security**: Test for fairness, explainability, and reliability
6. **Document everything**: Maintain evidence for compliance and audits
7. **Retest after changes**: Model updates, fine-tuning, and data changes require retesting
8. **Monitor continuously**: Production monitoring complements periodic testing
9. **Stay current**: AI attack techniques evolve rapidly
10. **Engage diverse testers**: Include perspectives from security, ML, ethics, and domain experts

---

## Version

1.0 - Initial release (OWASP AI Testing Guide v1, November 2025)

---

**Remember**: AI trustworthiness testing goes beyond traditional security. A secure AI system that is biased, opaque, or unreliable is not trustworthy. Test comprehensively across all dimensions of trustworthiness.

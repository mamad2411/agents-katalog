---
name: Compliance Frameworks
description: Compliance requirements for LLM applications under HIPAA, COPPA, FERPA, and GDPR, with testing methodology and evidence requirements
version: 1.0.0
---

# Compliance Frameworks for LLM Applications

## Purpose

Provides expert knowledge of regulatory compliance requirements as they apply to LLM-powered applications. Used by agents to identify compliance risks, generate compliance-focused attacks, and produce audit-ready reports.

## When to Use

- When scanning applications in regulated industries (healthcare, education, finance)
- When generating compliance-specific reports
- When prioritizing PII and data handling vulnerabilities
- When the user mentions regulatory requirements

## Supported Frameworks

| Framework | Sector | Key Concern for LLMs |
|-----------|--------|---------------------|
| **HIPAA** | Healthcare | PHI disclosure via LLM responses, PHI in training data, lack of BAA with LLM provider |
| **COPPA** | Children's services | Collection of children's data via chat, age verification gaps, persistent storage of conversations |
| **FERPA** | Education | Student record disclosure, educational data in prompts, unauthorized access to grades/records |
| **GDPR** | EU users | PII processing without consent, right to erasure conflicts with training data, cross-border data transfer |

## Reference Files

- [HIPAA Compliance](references/hipaa.md)
- [COPPA Compliance](references/coppa.md)
- [FERPA Compliance](references/ferpa.md)
- [GDPR Compliance](references/gdpr.md)

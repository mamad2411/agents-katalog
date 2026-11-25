---
name: pii-detection
description: Detect personally identifiable information (PII) in code, data, and agent outputs before processing or storage. Multi-language, GDPR-aware.
version: "1.0.0"
last-updated: "2026-04-17"
model_tested: "claude-sonnet-4-6"
category: privacy
platforms: [claude-code, codex, gemini-cli, cursor, copilot, windsurf, cline]
language: en
geo_relevance: [global, eu, fr]
priority: high
dependencies:
  mcp: []
  skills: []
  apis: []
  data: []
update_sources:
  - url: "https://www.cnil.fr/fr/reglement-europeen-protection-donnees"
    check_frequency: "yearly"
    last_checked: "2026-04-21"
license: MIT
---

# PII Detection

> **DISCLAIMER**: This skill provides detection patterns only. It does not guarantee complete PII identification. Always verify with a DPO for GDPR compliance decisions.

## When to Use

- Before sending data to an LLM API
- Before logging or storing agent outputs
- During data pipeline design
- When reviewing code that handles user data
- Before sharing datasets or exports

## PII Categories

### High Sensitivity (must always detect)
| Category | Patterns | Examples |
|----------|----------|---------|
| Email | `\b[\w.-]+@[\w.-]+\.\w+\b` | user@example.com |
| Phone | `\+?\d[\d\s\-().]{7,}\d` | +33 6 12 34 56 78 |
| SSN (FR) | `\b[12]\s?\d{2}\s?\d{2}\s?\d{2}\s?\d{3}\s?\d{3}\s?\d{2}\b` | 1 85 05 75 123 456 78 |
| SSN (US) | `\b\d{3}-\d{2}-\d{4}\b` | 123-45-6789 |
| Credit Card | `\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b` | 4111-1111-1111-1111 |
| IBAN | `\b[A-Z]{2}\d{2}[\s]?[\dA-Z]{4}[\s]?[\dA-Z]{4}[\s]?[\dA-Z]{4}` | FR76 1234 5678 9012 |
| Passport | Context-dependent | 12AB34567 |

### Medium Sensitivity (detect in context)
| Category | Patterns | Notes |
|----------|----------|-------|
| Full name | Named entity recognition | Combine first + last name |
| Address | Street + city + postal code | Multi-format per country |
| Date of birth | Date near age/birth context | Not all dates are PII |
| IP Address | `\b\d{1,3}(\.\d{1,3}){3}\b` | IPv4; check if user-linked |
| Vehicle plate | Country-specific format | FR: AA-123-BB |

### Low Sensitivity (flag only)
| Category | Notes |
|----------|-------|
| Age | PII only when combinable |
| Gender | PII only when combinable |
| Location (city) | PII only when precise |
| Job title | PII only with employer |

## Detection Process

1. **Scan** the input text for high-sensitivity patterns
2. **Flag** medium-sensitivity items with context check
3. **Report** findings with location and category
4. **Recommend** action: redact, anonymize, or approve

## Remediation Actions

| Action | When | Method |
|--------|------|--------|
| **Redact** | Before logging | Replace with `[REDACTED]` |
| **Pseudonymize** | Before analysis | Replace with consistent fake (e.g., hash-based) |
| **Anonymize** | Before sharing | Remove irreversibly (k-anonymity, differential privacy) |
| **Encrypt** | Before storage | AES-256 at rest, TLS in transit |
| **Approve** | Legitimate purpose | Document legal basis (GDPR Art. 6) |

## GDPR Special Categories (Article 9)

These require explicit consent or legal basis:
- Racial or ethnic origin
- Political opinions
- Religious beliefs
- Trade union membership
- Genetic data
- Biometric data (for identification)
- Health data
- Sex life or sexual orientation

**Detection**: Use keyword lists + context analysis. Never store without documented legal basis.

## Output Format

```
PII SCAN REPORT
Source: {file/variable/output}
Items found: {count}

[HIGH] Email: user@company.com (line 42)
[HIGH] Phone: +33 6 12 34 56 78 (line 67)
[MED]  Full name: "Jean Dupont" (line 12, with address context)
[LOW]  City: "Paris" (line 15, no combination risk)

Recommendation: Redact HIGH items before processing.
GDPR basis required: YES (personal data detected)
```

## What This Skill Does NOT Do

- Does not encrypt or store data (patterns only)
- Does not determine GDPR legal basis (legal decision)
- Does not handle consent management (UI/UX concern)
- Does not replace a DPO assessment

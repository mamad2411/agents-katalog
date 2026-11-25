---
name: compliance-promptforge-regulatory-compliance
description: >
  Use when validating prompts and AI systems against regulatory requirements,
  industry standards, and legal obligations. This skill provides systematic compliance
  checking procedures for AI regulations across jurisdictions.
---

# Compliance - Regulatory Compliance & Standards

## Overview
Compliance validates regulatory compliance for PromptForge AI. While Integrity handles ethics, Compliance handles the law—ensuring all prompts and AI systems meet legal requirements across applicable jurisdictions.

## When to Use
- Before deploying prompts in regulated industries (healthcare, finance, legal, education)
- When entering a new jurisdiction with different AI regulations
- When validating compliance with specific regulations (EU AI Act, GDPR, CCPA, HIPAA)
- When creating compliance documentation for audits
- When assessing legal risk of a prompt or AI capability
- **Don't use when:** Evaluating ethical concerns (use integrity-promptforge-ethical-ai)

## Core Procedures

### Step 1: Identify Applicable Regulations
Determine which regulations apply:
- **Geographic:** Where will the prompt be used? (EU, US, UK, etc.)
- **Industry:** What industry? (healthcare → HIPAA, finance → SOX, etc.)
- **Data Type:** What data is processed? (personal data → GDPR/CCPA, health data → HIPAA)
- **Use Case:** What is the prompt used for? (employment, credit, healthcare → additional rules)

### Step 2: Map Requirements to Prompt
For each applicable regulation:
```
COMPLIANCE MAPPING
==================
Regulation: [name and section]
Requirement: [what the regulation requires]
Applies To: [which part of the prompt/system]
Evidence Needed: [what proves compliance]
Status: [compliant/partial/non-compliant]
Gap: [what's missing for compliance]
```

### Step 3: Conduct Compliance Check
For each requirement:
- [ ] **Transparency:** Does the prompt disclose AI involvement where required?
- [ ] **Consent:** Is user consent obtained where required?
- [ ] **Data Minimization:** Does the prompt collect only necessary data?
- [ ] **Purpose Limitation:** Is the prompt used only for stated purposes?
- [ ] **Right to Explanation:** Can the prompt's output be explained to affected individuals?
- [ ] **Human Oversight:** Is human review available where required?
- [ ] **Data Retention:** Are outputs stored only as long as permitted?
- [ ] **Cross-Border Transfer:** Does data transfer comply with localization requirements?

### Step 4: Document Compliance Status
```
COMPLIANCE REPORT
=================
System/Prompt: [name and version]
Regulations Assessed: [list]
Overall Status: [compliant/partial/non-compliant]
Gaps: [list of non-compliant items with remediation plan]
Evidence: [documentation proving compliance]
Next Review: [when to reassess]
Sign-off: [compliance officer approval]
```

### Step 5: Monitor Regulatory Changes
- Track new and updated AI regulations
- Assess impact of regulatory changes on existing prompts
- Update compliance mappings when regulations change
- Alert affected teams when compliance status changes

## Success Metrics
- Compliance coverage: 100% of deployed prompts have compliance assessment
- Regulatory violations: 0 in production
- Compliance assessment time: <4 hours for standard assessments
- Regulatory change response time: <1 week from regulation update to impact assessment

## Error Handling
- **Error:** Prompt is non-compliant with a regulation
  **Response:** Do NOT deploy, design remediation plan, re-assess after changes
- **Error:** Regulation is ambiguous (multiple valid interpretations)
  **Response:** Document interpretation chosen, note alternative interpretations, consult legal counsel
- **Error:** Conflicting regulations (compliance with one violates another)
  **Response:** Document the conflict, escalate to legal counsel, implement most restrictive requirement

## Cross-Team Integration
**Related Skills:** integrity-promptforge-ethical-ai, specialist-promptforge-domain-adaptation, predictor-promptforge-outcome-prediction, data-privacy-check, license-compliance
**Used By:** Integrity, Specialist, Predictor, Sage, ALL agents deploying in regulated contexts
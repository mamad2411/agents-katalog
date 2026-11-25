---
name: integrity-promptforge-ethical-ai
description: >
  Use when evaluating prompts and AI outputs for ethical concerns, bias, fairness,
  safety, and responsible AI practices. This skill provides systematic ethical review
  procedures aligned with AI ethics frameworks and safety standards.
---

# Integrity - Ethical AI & Safety Compliance

## Overview
Integrity ensures all PromptForge AI work meets the highest ethical AI standards. Every prompt, output, and technique must be evaluated for bias, fairness, safety, and responsible use before deployment.

## When to Use
- Before deploying any prompt that affects people (hiring, evaluation, decision-making)
- When reviewing prompts for potential bias (gender, race, age, disability, etc.)
- When evaluating whether an AI technique could be misused
- When creating safety guardrails for prompt outputs
- When conducting ethical impact assessments for new capabilities
- **Don't use when:** Reviewing regulatory compliance (use compliance-promptforge-regulatory-compliance)

## Core Procedures

### Step 1: Identify Ethical Risk Areas
For each prompt/output, assess:
- **Affected Parties:** Who could be harmed by this prompt or its outputs?
- **Decision Impact:** Does this influence decisions about people? (hiring, lending, healthcare, etc.)
- **Bias Vectors:** What protected characteristics could be affected? (race, gender, age, disability, etc.)
- **Misuse Potential:** Could this be used unethically? (manipulation, deception, discrimination)
- **Transparency:** Can users understand how decisions are made?

### Step 2: Conduct Bias Audit
Test for bias across dimensions:
1. Create test inputs that vary only in protected characteristics
2. Run prompt with each variant
3. Compare outputs for differential treatment
4. Flag any statistically significant differences
5. Document the bias type and severity

### Step 3: Apply Ethical Framework
Evaluate against these principles:
- **Beneficence:** Does this prompt do good? Who benefits?
- **Non-maleficence:** Could this cause harm? How likely? How severe?
- **Autonomy:** Does this respect user choice and agency?
- **Justice:** Is this fair across different groups?
- **Explicability:** Can the prompt's behavior be explained?

### Step 4: Design Mitigations
For each ethical concern:
```
ETHICAL MITIGATION
==================
Concern: [what ethical issue was identified]
Severity: [low/medium/high/critical]
Affected Groups: [who is impacted]
Mitigation: [specific change to address the concern]
Residual Risk: [risk remaining after mitigation]
Acceptable: [yes/no - if no, do not deploy]
```

### Step 5: Issue Ethical Clearance
- **CLEARED:** No ethical concerns, or all concerns mitigated to acceptable level
- **CONDITIONAL:** Deploy with specific restrictions and monitoring
- **REJECTED:** Unacceptable ethical risk, do not deploy

## Success Metrics
- Bias detection rate: 100% of deployed prompts pass bias audit
- Ethical review completion: 100% of prompts reviewed before deployment
- Ethical violations in production: 0
- Time to ethical clearance: <2 hours for standard reviews

## Error Handling
- **Error:** Bias detected but source unclear
  **Response:** Expand test input diversity, test with more model variants, consult external ethics framework
- **Error:** Mitigation reduces prompt effectiveness
  **Response:** Find alternative mitigation that preserves effectiveness, or reject the prompt if ethical risk is too high
- **Error:** Ethical concern is subjective (reasonable people disagree)
  **Response:** Document both perspectives, escalate to Sage for decision, err on the side of caution

## Cross-Team Integration
**Related Skills:** compliance-promptforge-regulatory-compliance, predictor-promptforge-outcome-prediction, specialist-promptforge-domain-adaptation, data-privacy-check
**Used By:** Compliance, Predictor, Sage, ALL agents before deploying prompts that affect people
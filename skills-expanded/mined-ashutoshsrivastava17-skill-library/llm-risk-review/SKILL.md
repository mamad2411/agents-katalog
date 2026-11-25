---
name: llm-risk-review
description: >
  Assess risks of LLM-powered features — hallucination, bias, data leakage,
  prompt injection, compliance, and safety concerns. Produce risk matrices with
  mitigation recommendations and monitoring requirements.
  TRIGGER when: user says /llm-risk-review, "LLM risk", "AI risk review",
  "model risk assessment", "AI safety review", or "LLM compliance".
argument-hint: "[feature or use case name]"
user-invocable: true
---

# LLM Risk Review

You are an AI risk specialist. Produce a structured risk assessment for an LLM-powered feature or system, covering all categories of AI-specific risk. The output should be actionable for both engineering teams and compliance stakeholders.

## Process

### Step 1: Feature Profile

Document the feature under review:

| Attribute | Detail |
|-----------|--------|
| **Feature name** | ... |
| **Description** | What the feature does and who uses it |
| **Model** | LLM provider, model name, version |
| **Input source** | User-generated, system-generated, or both |
| **Output destination** | Displayed to users, stored, sent to downstream systems |
| **Data classification** | Public, internal, confidential, PII, regulated |
| **User population** | Internal employees, customers, general public |
| **Autonomy level** | Suggestions only / Auto-applied with review / Fully autonomous |
| **Regulatory scope** | GDPR, HIPAA, SOC2, industry-specific regulations |

### Step 2: Risk Identification

Evaluate each AI-specific risk category:

| Risk Category | Description | Key Questions |
|---------------|-------------|--------------|
| **Hallucination** | Model generates plausible but incorrect information | How is factual accuracy verified? What is the cost of a wrong answer? |
| **Bias & fairness** | Output reflects or amplifies demographic biases | Does the feature affect decisions about people? Are outputs auditable? |
| **Data leakage** | Model reveals training data or user data to other users | Is there multi-tenant data? Is PII in prompts or context? |
| **Prompt injection** | User input manipulates model behavior | Can users craft inputs that override system instructions? |
| **Jailbreaking** | Users bypass safety filters and guardrails | Can the model be tricked into producing harmful content? |
| **Over-reliance** | Users trust AI output without verification | Are outputs presented as suggestions or as authoritative answers? |
| **Cost explosion** | Adversarial or unexpected usage drives extreme costs | Are there per-user or per-request cost caps? |
| **Compliance** | Feature violates regulatory requirements | Is output logged? Can it be audited? Is consent collected? |
| **Toxicity** | Model produces offensive, harmful, or inappropriate content | What content filters are applied? What is the blast radius? |
| **Intellectual property** | Model reproduces copyrighted or proprietary content | Could outputs contain verbatim copyrighted text? |

### Step 3: Risk Scoring

Score each identified risk:

| Score | Likelihood | Definition |
|-------|-----------|-----------|
| 1 | Rare | Requires highly unusual circumstances | 
| 2 | Unlikely | Could occur but improbable with current controls |
| 3 | Possible | May occur during normal operation |
| 4 | Likely | Expected to occur regularly |
| 5 | Almost certain | Will occur without additional controls |

| Score | Impact | Definition |
|-------|--------|-----------|
| 1 | Negligible | No user impact, internal awareness only |
| 2 | Minor | Single user affected, easy to correct |
| 3 | Moderate | Multiple users affected, requires intervention |
| 4 | Major | Significant user harm, regulatory attention, or data breach |
| 5 | Catastrophic | Widespread harm, legal action, or existential business risk |

### Step 4: Mitigation Design

For each medium-and-above risk, design mitigations:

| Layer | Mitigation Type | Examples |
|-------|----------------|---------|
| **Input** | Sanitization, validation, classification | Input filters, PII redaction, intent classification |
| **Prompt** | Guardrails, instructions, constraints | System prompt hardening, output format enforcement |
| **Model** | Selection, configuration, fine-tuning | Temperature reduction, model choice, safety training |
| **Output** | Filtering, validation, human review | Content classifiers, schema validation, approval queues |
| **Monitoring** | Detection, alerting, auditing | Anomaly detection, quality sampling, audit logs |
| **Organizational** | Policy, training, process | Acceptable use policy, user training, incident response |

### Step 5: Monitoring Plan

Define ongoing monitoring for each high-risk area.

## Output Format

### 1. Feature Overview

Summary table with feature profile attributes.

### 2. Risk Register

| Risk ID | Category | Description | Likelihood (1-5) | Impact (1-5) | Risk Score | Level | Existing Controls | Control Effectiveness |
|---------|----------|-------------|-------------------|--------------|------------|-------|-------------------|----------------------|
| LR-001 | Hallucination | ... | 4 | 3 | 12 | High | ... | Weak/Adequate/Strong |

### 3. Risk Matrix

|  | Impact 1 | Impact 2 | Impact 3 | Impact 4 | Impact 5 |
|--|----------|----------|----------|----------|----------|
| **Likelihood 5** | 5 Med | 10 High | 15 High | 20 Critical | 25 Critical |
| **Likelihood 4** | 4 Low | 8 Med | 12 High | 16 Critical | 20 Critical |
| **Likelihood 3** | 3 Low | 6 Med | 9 Med | 12 High | 15 High |
| **Likelihood 2** | 2 Low | 4 Low | 6 Med | 8 Med | 10 High |
| **Likelihood 1** | 1 Low | 2 Low | 3 Low | 4 Low | 5 Med |

**Risk Levels**: Critical (16-25) | High (10-15) | Medium (5-9) | Low (1-4)

### 4. Mitigation Plan

For each Critical and High risk:

| Risk ID | Mitigation | Layer | Effort | Residual Risk | Owner | Timeline |
|---------|-----------|-------|--------|--------------|-------|----------|
| LR-001 | ... | Input/Prompt/Model/Output | S/M/L | Low/Med | ... | ... |

### 5. Monitoring Requirements

| Risk ID | Metric | Detection Method | Alert Threshold | Frequency | Owner |
|---------|--------|-----------------|----------------|-----------|-------|
| LR-001 | Hallucination rate | Output sampling + fact-check | > 5% of responses | Daily | ... |

### 6. Compliance Checklist

| Requirement | Status | Evidence | Gap |
|-------------|--------|----------|-----|
| User consent for AI processing | ... | ... | ... |
| Data retention policy for prompts/responses | ... | ... | ... |
| Right to explanation / opt-out | ... | ... | ... |
| Audit trail for AI decisions | ... | ... | ... |
| Bias testing documentation | ... | ... | ... |

### 7. Recommendations Summary

Prioritized list of actions: P1 (before launch), P2 (within 30 days), P3 (within quarter).

## Quality Standards

- Every risk must be scored using the defined likelihood and impact scales
- Critical and High risks must have specific mitigation plans, not generic advice
- Mitigation must address multiple layers (input, prompt, model, output, monitoring)
- Compliance requirements must reference specific regulations, not vague "regulatory risk"
- Monitoring plans must include concrete metrics and thresholds, not just "monitor it"
- The review must consider the full data flow: input, processing, output, storage, and logging
- Residual risk after mitigation must be explicitly stated

## Edge Cases

- **Internal-only tools**: Lower blast radius but still assess data leakage and over-reliance
- **Customer-facing chatbots**: Highest risk category — prioritize safety, brand, and compliance
- **Code generation features**: Assess security of generated code, license compliance, and IP risk
- **Summarization features**: Focus on faithfulness, omission risk, and attribution
- **Multi-model architectures**: Assess risk at each model boundary and in the orchestration layer
- **Fine-tuned models**: Additional risks around training data quality, bias in training set, and model drift
- **RAG systems**: Assess retrieval quality, poisoned document risk, and citation accuracy
- **Agentic systems**: Assess tool-use safety, loop risks, and the scope of autonomous actions

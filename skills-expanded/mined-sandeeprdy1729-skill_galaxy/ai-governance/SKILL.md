---
name: ai-governance
description: "Implement AI governance frameworks including risk assessment, model auditing, bias detection, regulatory compliance (EU AI Act, NIST AI RMF), and responsible AI deployment practices for enterprise organizations."
license: Apache 2.0
tags: ["ai-governance", "responsible-ai", "compliance", "bias-detection", "eu-ai-act", "nist", "model-auditing", "risk-management"]
difficulty: advanced
time_to_master: "12-20 weeks"
version: "1.0.0"
---

# AI Governance & Compliance

## Overview

AI governance covers the policies, frameworks, and technical controls needed to deploy AI systems responsibly and in compliance with emerging regulations. As the EU AI Act, NIST AI Risk Management Framework, and industry-specific requirements take effect, organizations need structured approaches to AI risk assessment, model auditing, bias detection, and transparency reporting.

## When to Use This Skill

- Establishing an AI governance program for an organization
- Conducting risk assessments for AI/ML systems
- Implementing bias detection and fairness testing
- Complying with EU AI Act risk classifications
- Building model audit trails and explainability frameworks
- Creating AI ethics review boards and approval processes

## Core Concepts

### Regulatory Landscape

| Framework | Scope | Status | Key Requirements |
|-----------|-------|--------|-----------------|
| EU AI Act | EU operations | Effective 2026 | Risk classification, conformity assessment |
| NIST AI RMF | US voluntary | Published 2023 | Govern, Map, Measure, Manage |
| ISO 42001 | Global voluntary | Published 2023 | AI management system certification |
| Executive Order 14110 | US federal | Signed 2023 | Safety testing, reporting requirements |
| Canada AIDA | Canada | In progress | Responsible AI obligations |

### EU AI Act Risk Classification

```
┌─────────────────────────────────────────────────┐
│              Unacceptable Risk                   │
│  Social scoring, real-time biometric mass        │
│  surveillance, manipulation of vulnerable groups │
│  → BANNED                                        │
├─────────────────────────────────────────────────┤
│              High Risk                           │
│  Employment decisions, credit scoring,           │
│  education, law enforcement, healthcare          │
│  → Conformity assessment, auditing, logging      │
├─────────────────────────────────────────────────┤
│              Limited Risk                        │
│  Chatbots, AI-generated content,                │
│  emotion recognition                             │
│  → Transparency obligations                      │
├─────────────────────────────────────────────────┤
│              Minimal Risk                        │
│  Spam filters, AI-enabled games,                │
│  inventory management                            │
│  → No specific obligations                       │
└─────────────────────────────────────────────────┘
```

### NIST AI Risk Management Framework

```
┌───────────┐     ┌───────────┐     ┌───────────┐     ┌───────────┐
│  GOVERN   │────►│    MAP    │────►│  MEASURE  │────►│  MANAGE   │
│           │     │           │     │           │     │           │
│ Policies, │     │ Context,  │     │ Metrics,  │     │ Respond,  │
│ roles,    │     │ risk ID,  │     │ testing,  │     │ document, │
│ culture   │     │ stakehldrs│     │ monitoring│     │ improve   │
└───────────┘     └───────────┘     └───────────┘     └───────────┘
```

## Implementation Guide

### AI Risk Assessment Template

```python
class AIRiskAssessment:
    """Structured risk assessment for AI/ML systems."""

    RISK_CATEGORIES = {
        "bias_discrimination": {
            "description": "System produces unfair outcomes for protected groups",
            "examples": ["Hiring tool disadvantaging women", "Loan model rejecting minorities"],
        },
        "privacy_violation": {
            "description": "System exposes or misuses personal data",
            "examples": ["Training on PII without consent", "Re-identification risk"],
        },
        "safety_harm": {
            "description": "System causes physical or psychological harm",
            "examples": ["Autonomous vehicle misclassification", "Medical misdiagnosis"],
        },
        "transparency_gap": {
            "description": "Stakeholders cannot understand system decisions",
            "examples": ["Black-box credit decisions", "Unexplainable content moderation"],
        },
        "accountability_gap": {
            "description": "No clear ownership for system failures",
            "examples": ["No incident response plan", "No human oversight"],
        },
    }

    def assess(self, system):
        assessment = {
            "system_name": system.name,
            "system_purpose": system.purpose,
            "eu_ai_act_category": self.classify_eu_risk(system),
            "risk_scores": {},
            "mitigations": [],
            "overall_risk": None,
        }

        for category, info in self.RISK_CATEGORIES.items():
            score = self.evaluate_risk(system, category)
            assessment["risk_scores"][category] = {
                "likelihood": score.likelihood,  # 1-5
                "impact": score.impact,          # 1-5
                "risk_level": score.likelihood * score.impact,
                "mitigations": score.mitigations,
            }

        assessment["overall_risk"] = max(
            r["risk_level"] for r in assessment["risk_scores"].values()
        )
        return assessment
```

### Bias Detection Framework

```python
from fairlearn.metrics import MetricFrame, selection_rate, demographic_parity_difference

class BiasDetector:
    """Detect and measure bias across protected attributes."""

    PROTECTED_ATTRIBUTES = ["gender", "race", "age_group", "disability_status"]

    def audit(self, y_true, y_pred, sensitive_features):
        results = {}

        for attribute in self.PROTECTED_ATTRIBUTES:
            if attribute not in sensitive_features.columns:
                continue

            metric_frame = MetricFrame(
                metrics={
                    "selection_rate": selection_rate,
                    "accuracy": lambda y_t, y_p: (y_t == y_p).mean(),
                    "false_positive_rate": lambda y_t, y_p: ((y_p == 1) & (y_t == 0)).sum() / (y_t == 0).sum(),
                },
                y_true=y_true,
                y_pred=y_pred,
                sensitive_features=sensitive_features[attribute],
            )

            results[attribute] = {
                "group_metrics": metric_frame.by_group.to_dict(),
                "demographic_parity_diff": demographic_parity_difference(
                    y_true, y_pred, sensitive_features=sensitive_features[attribute]
                ),
                "max_disparity": metric_frame.difference().max(),
                "passes_threshold": metric_frame.difference().max() < 0.1,  # 80% rule
            }

        return results

    def generate_report(self, audit_results):
        """Generate a human-readable bias audit report."""
        report = []
        for attr, result in audit_results.items():
            status = "PASS" if result["passes_threshold"] else "FAIL"
            report.append(
                f"{attr}: {status} (max disparity: {result['max_disparity']:.3f}, "
                f"demographic parity diff: {result['demographic_parity_diff']:.3f})"
            )
        return "\n".join(report)
```

### Model Card Generator

```python
class ModelCard:
    """Generate model cards for AI transparency and documentation."""

    def generate(self, model_info):
        return {
            "model_details": {
                "name": model_info.name,
                "version": model_info.version,
                "type": model_info.model_type,
                "owner": model_info.team,
                "date_trained": model_info.training_date,
                "framework": model_info.framework,
            },
            "intended_use": {
                "primary_use": model_info.primary_use,
                "out_of_scope": model_info.out_of_scope_uses,
                "users": model_info.intended_users,
            },
            "training_data": {
                "description": model_info.training_data_desc,
                "size": model_info.dataset_size,
                "preprocessing": model_info.preprocessing_steps,
                "known_biases": model_info.known_data_biases,
            },
            "performance": {
                "metrics": model_info.evaluation_metrics,
                "benchmarks": model_info.benchmark_results,
                "disaggregated": model_info.performance_by_group,
            },
            "ethical_considerations": {
                "risks": model_info.identified_risks,
                "mitigations": model_info.risk_mitigations,
                "fairness_report": model_info.bias_audit_results,
            },
            "limitations": model_info.known_limitations,
        }
```

### AI Decision Audit Trail

```python
class AIAuditLogger:
    """Immutable audit trail for AI system decisions."""

    def log_decision(self, decision):
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "system_id": decision.system_id,
            "model_version": decision.model_version,
            "input_hash": hashlib.sha256(json.dumps(decision.input, sort_keys=True).encode()).hexdigest(),
            "output": decision.output,
            "confidence": decision.confidence,
            "explanation": decision.explanation,
            "human_override": decision.was_overridden,
            "override_reason": decision.override_reason,
            "affected_individual": decision.subject_id,  # pseudonymized
        }

        # Immutable append-only log
        self.audit_store.append(entry)
        return entry
```

## Governance Checklist

| Phase | Requirement | Status |
|-------|-------------|--------|
| Pre-deployment | Risk assessment completed | ☐ |
| Pre-deployment | Bias audit passed | ☐ |
| Pre-deployment | Model card published | ☐ |
| Pre-deployment | Data governance review | ☐ |
| Pre-deployment | Ethics board approval | ☐ |
| Deployment | Audit logging enabled | ☐ |
| Deployment | Human oversight configured | ☐ |
| Deployment | Incident response plan ready | ☐ |
| Post-deployment | Monitoring dashboards active | ☐ |
| Post-deployment | Bias re-testing scheduled | ☐ |
| Post-deployment | Model drift alerts configured | ☐ |

## Best Practices

1. **Classify all AI systems by risk level** before deployment
2. **Conduct bias audits** on every model that affects individuals
3. **Maintain model cards** as living documents, updated with each version
4. **Log every decision** for high-risk AI systems (immutable audit trail)
5. **Establish an AI ethics review board** with diverse stakeholders
6. **Re-test for bias quarterly** — data drift can introduce new biases
7. **Design for human override** — every AI decision should be reversible

## Resources

- [NIST AI Risk Management Framework](https://airc.nist.gov/AI_RMF_Playbook)
- [EU AI Act Full Text](https://artificialintelligenceact.eu/)
- [Fairlearn Library](https://fairlearn.org/)
- [Google Model Cards](https://modelcards.withgoogle.com/)
- [ISO/IEC 42001:2023](https://www.iso.org/standard/81230.html)

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-03-31 | Initial documentation |

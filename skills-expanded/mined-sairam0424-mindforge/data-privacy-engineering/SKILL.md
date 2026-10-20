---
name: data-privacy-engineering
version: 1.0.0
min_mindforge_version: 10.6.0
status: stable
triggers: data privacy engineering, differential privacy implementation, anonymization technique, consent management system, privacy-preserving computation, GDPR data engineering, data masking, privacy by design, homomorphic encryption, federated learning privacy, secure multi-party computation, PII detection pipeline
---

# Skill — Data Privacy Engineering

## When this skill activates
This skill activates when implementing privacy-preserving data systems, building consent management infrastructure, or applying anonymization techniques. Use when handling sensitive data requires technical controls beyond access restrictions.

## Mandatory actions when this skill is active

### Before writing any code
1. Conduct privacy impact assessment: identify PII/sensitive data, data flows, retention requirements, third-party sharing, and regulatory obligations (GDPR, CCPA, HIPAA)
2. Define privacy requirements: anonymization level (k-anonymity, l-diversity, differential privacy), consent granularity, right-to-erasure scope, and data minimization principles
3. Select appropriate privacy techniques: tokenization (reversible), hashing (one-way), encryption (protected), differential privacy (statistical), synthetic data (replacement)
4. Establish privacy testing framework: re-identification risk assessment, privacy budget tracking, consent enforcement verification, and breach simulation

### During implementation
- Implement automated PII detection pipeline: regex patterns, ML models, NER for unstructured text scanning code, logs, databases, and data lakes
- Build tokenization service with: format-preserving encryption for display, secure token vault, key rotation, and performance caching for high-throughput
- Create differential privacy mechanisms: Laplace/Gaussian noise addition calibrated to epsilon budget, query result perturbation, and privacy budget accounting across queries
- Design consent management system: granular opt-in/opt-out, purpose-specific consent, consent version tracking, and propagation to downstream systems
- Implement data minimization controls: retention policies with automated deletion, purpose limitation enforcement, and necessity justification for data collection
- Build privacy-preserving analytics: federated learning for ML without centralized data, secure aggregation for metrics, and homomorphic encryption for computation on encrypted data
- Create data subject rights workflows: search across systems, export in portable format, deletion with verification, and rectification propagation

### After implementation
- Generate privacy compliance reports: PII inventory, consent coverage, retention policy enforcement, third-party data sharing audit, and rights request fulfillment SLA
- Build privacy monitoring dashboards: PII exposure incidents, consent withdrawal rates, privacy budget consumption, and anonymization quality metrics
- Create breach response procedures: detection, containment, notification timelines, affected user identification, and remediation workflows
- Document privacy controls: anonymization methods, re-identification risk levels, consent mechanisms, and data retention justifications for audit purposes

## Self-check before task completion
- [ ] PII detection covers all data stores with automated scanning and alerting on new sensitive data discoveries
- [ ] Anonymization techniques applied with documented re-identification risk assessment (k-anonymity ≥10 or equivalent)
- [ ] Consent management enforces purpose limitation with propagation to all downstream processing systems
- [ ] Differential privacy implementation maintains epsilon budget <1.0 for sensitive aggregations with privacy accounting
- [ ] Data subject rights workflows tested for completeness across all systems within regulatory SLA (30 days GDPR)

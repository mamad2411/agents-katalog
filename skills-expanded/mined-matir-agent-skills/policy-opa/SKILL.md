---
name: policy-opa
description: Policy-as-code enforcement and compliance validation using Open Policy Agent (OPA).
metadata:
  version: 0.2.0
  category: compliance
---
# Policy-as-Code with OPA

## Quick Start
```bash
# Evaluate a policy against input data
opa eval --data policy.rego --input input.json 'data.example.allow'
# Run policy unit tests
opa test . --verbose
```

## Workflow
1. **Requirement Mapping**: Identify compliance controls (SOC2, PCI-DSS) or security standards to enforce.
2. **Policy Creation**: Write OPA policies in Rego language to codify requirements.
3. **Unit Testing**: Write comprehensive tests for all policy rules (`opa test`).
4. **Validation**: Evaluate policies against target configurations (Terraform, Kubernetes YAML, etc.).
5. **Integration**: Embed OPA checks into CI/CD pipelines or as Kubernetes admission controllers.
6. **Reporting**: Generate compliance reports and export violations for monitoring.

## Rules & Constraints
- **RULE-1**: All policies MUST have version control and require peer review for changes.
- **RULE-2**: Maintain >80% unit test coverage for all Rego policy rules.
- **RULE-3**: OPA should run with read-only access to source configurations.
- **RULE-4**: Do NOT embed secrets or sensitive credentials directly in Rego files.

## When to Use
- Enforcing infrastructure-as-code (Terraform) security best practices.
- Implementing Kubernetes admission control for cluster security.
- Validating configuration compliance against SOC2, PCI-DSS, or GDPR.

## When NOT to Use
- Real-time application authorization with high-latency requirements (consider localized evaluation).
- Complex data transformations better suited for general-purpose programming.
- When existing cloud-native tools (like AWS Config) provide simpler out-of-the-box checks.

## References
- [Skill Manual](references/policy-opa-manual.md)
- [OPA Documentation](https://www.openpolicyagent.org/docs/latest/)
- [Rego Language Reference](https://www.openpolicyagent.org/docs/latest/policy-language/)

---
name: iac-checkov
description: Infrastructure as Code (IaC) security scanner for Terraform, Kubernetes, and CloudFormation. Detects misconfigurations and compliance violations (CIS, PCI) using 750+ built-in policies.
metadata:
  version: 0.2.0
  category: devsecops
---
# Infrastructure as Code Security with Checkov

## Quick Start
```bash
# Scan all Terraform files in directory
checkov -d ./terraform

# Scan Kubernetes YAML files
checkov -d ./k8s --framework kubernetes
```

## Workflow
1. **Understand Scope**: Identify IaC files and supported frameworks.
2. **Run Basic Scan**: Execute Checkov with desired output format (cli, json, sarif).
3. **Filter Findings**: Prioritize by severity (Critical/High) or specific compliance standards.
4. **Suppress False Positives**: Use inline comments for legitimate exceptions.
5. **Custom Policies**: Define organization-specific rules in Python or YAML.
6. **Generate Reports**: Create compliance documents for audit and reporting.

## Rules & Constraints
- **Severity-Based Blocking**: Configure `--hard-fail-on` for CRITICAL/HIGH in CI/CD.
- **Suppression Governance**: Require justification and approval for all inline suppressions.
- **Credential Protection**: Never commit secrets; use secret managers for infrastructure.
- **Audit Logging**: Maintain centralized logs of all scan results and policy overrides.

## When to Use
- Scanning Terraform, CloudFormation, or Kubernetes for security misconfigurations.
- Validating infrastructure against industry standards (CIS, PCI-DSS).
- Preventing hardcoded secrets from entering production.

## When NOT to Use
- Real-time runtime security monitoring of cloud resources.
- Scanning non-IaC application code for vulnerabilities.

## References
- [Skill Manual](references/iac-checkov-manual.md)
- [Official Documentation](https://www.checkov.io/docs)
- [Policy Index](https://docs.paloaltonetworks.com/prisma/prisma-cloud/prisma-cloud-policies-reference/checkov-policies)

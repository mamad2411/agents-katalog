---
name: lang-terraform
description: Terraform/HCL infrastructure as code, remote state locking, least-privilege IAM, checkov/tfsec security scanning, and plan evidence.
---

# Terraform / HCL Infrastructure Contract

## 1. State Management & Immutability
- Remote state storage with encryption at rest and state locking (e.g. S3 + DynamoDB) is mandatory.
- Pin provider versions (\`version = "~> 5.0"\`) and required Terraform version in the \`terraform {}\` block.

## 2. Least Privilege & Security Policy
- Strict least-privilege IAM: prohibit wildcard actions (\`Action = ["*"]\`) or wildcard resources (\`Resource = "*"\`).
- Prohibit open ingress rules (\`0.0.0.0/0\`) on sensitive administrative ports (SSH 22, RDP 3389).
- Run static security analysis (\`checkov\` or \`tfsec\`) in CI; zero high/critical vulnerabilities.

## 3. Quality & Plan Evidence
- All input variables and outputs must have explicit \`type\` constraints and \`description\` strings.
- Every infrastructure change must produce a \`terraform plan\` artifact as verifiable evidence prior to apply.
- Enforce \`terraform fmt -check\` and \`terraform validate\` across all modules.\n
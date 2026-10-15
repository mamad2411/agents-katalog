---
name: platform-constitution
description: Define your organization's platform engineering standards by generating a Platform-Engineering-Constitution.md. Use when establishing or updating cloud infrastructure policies, approved tooling, compute platforms, and IaC conventions.
license: MIT
metadata:
  author: radius-skills
  version: "1.0.0"
---

# Platform Constitution

Use this skill to generate a `Platform-Engineering-Constitution.md` that codifies your organization's platform engineering standards.

## Workflow

1. **Check for existing constitution.** Look for a `Platform-Engineering-Constitution.md` in the repository root or docs directory. If one exists, ask the user whether to update it or start fresh. Never overwrite without explicit approval.
2. **Gather organizational context** by asking the user each of the following questions, one at a time. Accept their answers and move to the next question. Do not assume defaults.
3. **Load relevant references** from the reference files linked below based on the answers given (e.g., if Azure is selected, load `azure-governance.md`).
4. **Generate the constitution** as a `Platform-Engineering-Constitution.md` file in the repository root.
5. **Review with the user.** Present the generated document and ask for feedback before finalizing.

## Data Gathering Questions

Ask these questions interactively, one at a time:

### Organization Identity
- **Organization name**: What is your organization name?

### Cloud Providers
- **Cloud providers**: What cloud providers does your organization use? (Azure, AWS, GCP, other)
- For each selected provider, note any specific services or constraints.

### Compute Platform
- **Compute targets**: What compute platform(s) do you target? (Kubernetes, VMs, serverless, container apps, other)
- If Kubernetes: managed (AKS, EKS, GKE) or self-managed? What version constraints?

### Infrastructure Policies
- **Existing policies**: Do you have existing infrastructure policies to import? (e.g., Azure Policy, AWS Config, OPA/Gatekeeper, Kyverno)
- If yes, ask for the location or format of these policies and incorporate their intent into the constitution.

### Infrastructure as Code
- **IaC tooling**: What IaC tooling does your platform team use? (Terraform, Bicep, Pulumi, CloudFormation, CDK, other)
- **Approved modules**: Where are your approved IaC modules stored? (e.g., GitHub org, Terraform registry, internal registry)
- **Module standards**: Any conventions for module structure, naming, or versioning?

### Additional Constraints
- **Regions**: What cloud regions are approved for deployment?
- **Compliance frameworks**: Any compliance requirements? (SOC 2, HIPAA, FedRAMP, PCI-DSS, ISO 27001, other)
- **Naming conventions**: Do you have naming conventions for cloud resources?
- **Tagging/labeling**: Required tags or labels for cloud resources?
- **Network topology**: Any network architecture constraints? (hub-spoke, mesh, VPN requirements)
- **Secret management**: How are secrets managed? (Key Vault, Secrets Manager, Vault, other)

## Output Format

Generate a `Platform-Engineering-Constitution.md` with the following structure:

```markdown
# Platform Engineering Constitution — {Organization Name}

## 1. Organization Overview
Brief description of the organization and purpose of this document.

## 2. Cloud Providers
- Approved providers and their primary use cases
- Provider-specific constraints or preferences

## 3. Compute Platform
- Target compute platforms and configurations
- Version constraints and upgrade policies

## 4. Infrastructure Policies
- Imported policy summaries
- Governance requirements
- Compliance framework alignment

## 5. Infrastructure as Code
- Approved IaC tooling
- Module source locations and conventions
- Module structure and versioning standards

## 6. Deployment Standards
- Approved regions
- Naming conventions
- Required tags and labels

## 7. Network Architecture
- Network topology requirements
- Connectivity constraints

## 8. Security & Secrets
- Secret management approach
- Access control requirements

## 9. Appendix
- Links to referenced policies
- Change log
```

## References

| Topic                    | Reference                                                              | Use for                                            |
| ------------------------ | ---------------------------------------------------------------------- | -------------------------------------------------- |
| Azure Governance         | [references/azure-governance.md](references/azure-governance.md)       | Azure Policy, landing zones, resource organization |
| AWS Governance           | [references/aws-governance.md](references/aws-governance.md)           | AWS Config, Control Tower, Organizations           |
| Kubernetes Best Practices| [references/kubernetes-best-practices.md](references/kubernetes-best-practices.md) | K8s standards, RBAC, resource quotas     |
| Terraform Conventions    | [references/terraform-conventions.md](references/terraform-conventions.md) | Module structure, state management, CI/CD      |
| IaC Module Standards     | [references/iac-module-standards.md](references/iac-module-standards.md)   | Module versioning, testing, documentation      |
| Policy Import Guide      | [references/policy-import-guide.md](references/policy-import-guide.md)     | Importing Azure Policy, AWS Config, OPA rules  |

## Guardrails

- **Never assume answers.** Always ask the user. Do not fill in defaults for cloud providers, regions, tooling, or policies.
- **Never overwrite an existing constitution** without explicit user approval. Offer to update or diff instead.
- **Confirm before generating.** Summarize all gathered data and get user confirmation before writing the file.
- **Be provider-neutral.** Support multi-cloud setups without bias toward any single provider.
- **Flag gaps.** If the user skips questions, note them as "TBD" in the output and recommend revisiting.
- **Respect existing conventions.** If the user has existing standards, incorporate rather than replace them.

---
name: terraform-provision
description: Infrastructure as Code with Terraform
version: 1.0.0
tags: [devops, iac, cloud, infrastructure]
---

# Terraform – Infrastructure as Code

Terraform enables declarative infrastructure provisioning across
cloud providers and on-premises resources.

- **GitHub**: github.com/hashicorp/terraform (45 000+ ⭐)
- **License**: MPL-2.0
- **Security**: HashiCorp-backed. Enterprise-grade. No malware.

## Usage Examples

### Initialise a project

```bash
terraform init
```

### Plan changes

```bash
terraform plan -out=tfplan
```

### Apply infrastructure

```bash
terraform apply tfplan
```

### Destroy resources

```bash
terraform destroy -auto-approve
```

## AI Agent Tips

- Use `plan` before `apply` to preview changes safely.
- State file tracks infrastructure — use remote backends (S3, GCS) for teams.
- Supports AWS, Azure, GCP, DigitalOcean, and 3000+ providers.
- Modules enable reusable infrastructure patterns.

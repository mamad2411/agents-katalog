---
agent: terraform-code
description: "Generate Terraform configurations using AVM modules"
---

# Step 5t: Terraform Code Generation

Act as the Forge (⚒️). Generate Terraform configurations based on the implementation
plan, using AVM modules where available.

## Process

1. Read `04-implementation-plan.md` and `04-governance-constraints.md`
2. Generate Terraform modules under `infra/terraform/{customer}/`
3. Create tfvars per environment under `infra/terraform/{customer}/environments/`
4. Enforce security baseline in every module
5. Include budget resource with parameterized alerts

## Mandatory Checks

Every Terraform file must pass:
- Security baseline (6 rules): `min_tls_version`, `https_traffic_only_enabled`, `allow_nested_items_to_be_public`, managed identity, `azuread_authentication_only`, `public_network_access_enabled`
- Budget resource with 80%/100%/120% forecast thresholds
- Diagnostic settings forwarding to Log Analytics
- CAF naming conventions and required tags
- AVM module references where available

## Validation

```bash
cd infra/terraform/{customer} && terraform init && terraform validate
python scripts/validators/validate_security_baseline.py infra/terraform/{customer}/
python scripts/validators/validate_cost_governance.py infra/terraform/{customer}/
```

## Output

Terraform files in `infra/terraform/{customer}/` with environment tfvars.

---
applyTo: "**/*.tf"
---

# Terraform Best Practices

## AVM-First

Always use Azure Verified Modules (AVM) when available:
```hcl
module "storage" {
  source  = "Azure/avm-res-storage-storageaccount/azurerm"
  version = "~> 0.2"
}
```
Fall back to native `azurerm_` resources only when no AVM module exists.

## Security Baseline (Non-Negotiable)

Every Terraform file must enforce:
1. `min_tls_version = "1.2"` or `min_tls_version = "TLS1_2"`
2. `https_traffic_only_enabled = true`
3. `allow_nested_items_to_be_public = false`
4. `identity { type = "SystemAssigned" }` (prefer managed identity)
5. `azuread_authentication_only = true` (SQL resources)
6. `public_network_access_enabled = false` (production environments)

## Cost Governance

Include a budget resource with parameterized thresholds:
```hcl
resource "azurerm_consumption_budget_subscription" "this" {
  amount     = var.budget_amount  # parameterized, never hardcoded
  notification {
    threshold      = 80
    threshold_type = "Forecasted"
    operator       = "GreaterThanOrEqualTo"
  }
  notification {
    threshold      = 100
    threshold_type = "Forecasted"
    operator       = "GreaterThanOrEqualTo"
  }
  notification {
    threshold      = 120
    threshold_type = "Forecasted"
    operator       = "GreaterThanOrEqualTo"
  }
}
```

## Naming & Tagging

- Follow CAF naming: `{resourceType}-{workload}-{environment}-{region}-{instance}`
- Required tags: `Environment`, `Owner`, `CostCenter`, `Project`, `ManagedBy`

## State Management

- Remote state in Azure Storage with state locking
- Never commit `.tfstate` files

## Validation

```bash
terraform init && terraform validate
python scripts/validators/validate_security_baseline.py infra/terraform/{customer}/
python scripts/validators/validate_cost_governance.py infra/terraform/{customer}/
```

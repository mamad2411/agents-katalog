---
applyTo: "**/*.bicep"
---

# Bicep Best Practices

## AVM-First

Always use Azure Verified Modules (AVM) when available:
```bicep
module storage 'br/public:avm/res/storage/storage-account:0.14.0' = { ... }
```
Fall back to native `resource` blocks only when no AVM module exists.

## Security Baseline (Non-Negotiable)

Every Bicep file must enforce:
1. `minimumTlsVersion: 'TLS1_2'`
2. `supportsHttpsTrafficOnly: true`
3. `allowBlobPublicAccess: false`
4. `identity: { type: 'SystemAssigned' }` (prefer managed identity)
5. `azureADOnlyAuthentication: true` (SQL resources)
6. `publicNetworkAccess: 'Disabled'` (production environments)

## Cost Governance

Include a budget resource with parameterized thresholds:
```bicep
resource budget 'Microsoft.Consumption/budgets@2023-11-01' = {
  properties: {
    amount: budgetAmount  // parameterized, never hardcoded
    notifications: {
      forecast80: { threshold: 80, operator: 'GreaterThanOrEqualTo', thresholdType: 'Forecasted' }
      forecast100: { threshold: 100, operator: 'GreaterThanOrEqualTo', thresholdType: 'Forecasted' }
      forecast120: { threshold: 120, operator: 'GreaterThanOrEqualTo', thresholdType: 'Forecasted' }
    }
  }
}
```

## Naming & Tagging

- Follow CAF naming: `{resourceType}-{workload}-{environment}-{region}-{instance}`
- Required tags: `Environment`, `Owner`, `CostCenter`, `Project`, `ManagedBy`

## Diagnostic Settings

Every resource that supports it must have diagnostic settings forwarding to Log Analytics.

## Validation

```bash
az bicep build --file main.bicep
python scripts/validators/validate_security_baseline.py infra/bicep/{customer}/
python scripts/validators/validate_cost_governance.py infra/bicep/{customer}/
```

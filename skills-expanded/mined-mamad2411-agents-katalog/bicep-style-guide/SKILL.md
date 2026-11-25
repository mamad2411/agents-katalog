---
name: bicep-style-guide
description: >-
  Bicep coding style guide for Azure infrastructure. Enforces naming conventions,
  file layout order, commenting rules, decorator usage, parameter design,
  resource configuration patterns, and module design standards.
when-to-use: >-
  Invoke when writing or reviewing Bicep code (.bicep files), creating modules,
  designing parameter interfaces, or establishing Bicep standards for a project.
  Also invoke when onboarding engineers to a Bicep codebase.
categories:
  - infrastructure
  - bicep
  - code-style
---

# Bicep Style Guide

Write Bicep that a tired human can read at 2am during an incident. No clever tricks. Every file should be so obvious that the person reading it six months from now can understand it without a Rosetta Stone.

## Naming Conventions

| Element | Convention | Example |
|---|---|---|
| **Resources** | camelCase symbolic names | `storageAccount`, `keyVault`, `virtualNetwork` |
| **Parameters** | camelCase, descriptive | `storageAccountName`, `location`, `environment` |
| **Variables** | camelCase | `namePrefix`, `commonTags`, `subnetAddressPrefix` |
| **Outputs** | camelCase, exact description | `storageAccountId`, `principalId`, `connectionString` |
| **Modules** | camelCase symbolic, kebab-case file | `module storageAccount './modules/storage-account.bicep'` |
| **User-defined types** | camelCase with `Type` suffix | `subnetConfigType`, `tagConfigType` |

**Rules**: Name things what they are. `storageAccount` not `sa`. `keyVault` not `kv`. You're not paying per character.

---

## File Layout (Standard Order)

Every Bicep file follows this order. Every time. No exceptions.

1. `targetScope` — only if not `resourceGroup` (the default)
2. `metadata` — file description, always present
3. `import` statements
4. User-defined types (`type`)
5. User-defined functions (`func`)
6. Parameters (`param`) — required first, then optional with defaults
7. Variables (`var`)
8. Resources and modules — ordered by dependency
9. Outputs (`output`)

### Example Structure

```bicep
targetScope = 'subscription'

metadata description = 'Deploys a resource group and storage account for application data.'

// Types
type diagnosticSettingType = {
  @description('Name of the diagnostic setting.')
  name: string
  @description('Log Analytics workspace resource ID.')
  workspaceId: string
}

// Parameters — Required
@description('Short name of the project. Used in resource naming.')
@minLength(2)
@maxLength(10)
param project string

@description('Target environment name.')
@allowed(['dev', 'staging', 'prod'])
param environment string

// Parameters — Optional
@description('Azure region for all resources.')
param location string = deployment().location

// Variables
var namePrefix = '${project}-${environment}'
var commonTags = {
  Environment: environment
  Project: project
  ManagedBy: 'Bicep'
}

// Resources
resource resourceGroup 'Microsoft.Resources/resourceGroups@2024-03-01' = {
  name: '${namePrefix}-rg'
  location: location
  tags: commonTags
}

// Outputs
@description('Resource ID of the deployed resource group.')
output resourceGroupId string = resourceGroup.id
```

---

## Commenting Rules

- [ ] **Every parameter** gets `@description()` — no exceptions, not even `location`
- [ ] **Every output** gets `@description()`
- [ ] **Every module call** gets a comment explaining what it deploys
- [ ] **Every file** starts with `metadata description = '...'`
- [ ] **Complex expressions** get inline comments
- [ ] **Explain WHY, not WHAT** — `// Enable soft delete for compliance` is useful; `// Set enableSoftDelete to true` is not

---

## Decorator Usage

Use decorators aggressively. Catching a bad value at deploy time beats a failed provisioning twenty minutes later.

```bicep
// Strings: length constraints
@description('Storage account name. Must be globally unique.')
@minLength(3)
@maxLength(24)
param storageAccountName string

// Enums: constrain choices
@description('SKU tier for the storage account.')
@allowed(['Standard_LRS', 'Standard_GRS', 'Standard_ZRS'])
param skuName string = 'Standard_LRS'

// Numbers: range constraints
@description('Days to retain deleted blobs.')
@minValue(1)
@maxValue(365)
param retentionDays int = 30

// Secrets: always marked secure
@description('Backend database connection string.')
@secure()
param databaseConnectionString string
```

---

## Parameter Design

- **Default for location**: `resourceGroup().location` for RG scope, `deployment().location` for subscription scope
- **`@allowed()`** for environment names, SKU tiers, any known set of valid values
- **`@secure()`** for passwords, connection strings, keys — never output, never log
- **Group related parameters** with comment blocks
- **Validate early** — every constraint as a decorator prevents wasted deployment time

---

## Resource Configuration Style

```
Properties order within a resource:
name → location → tags → sku → kind → properties → identity → dependsOn
```

- [ ] One blank line between resources
- [ ] Always include tags on taggable resources
- [ ] Use `existing` keyword to reference existing resources (not hardcoded IDs)
- [ ] Prefer symbolic references over `dependsOn`
- [ ] Only use `dependsOn` with a comment explaining the non-obvious ordering

```bicep
// Use existing keyword — not resource ID strings
resource logAnalytics 'Microsoft.OperationalInsights/workspaces@2023-09-01' existing = {
  name: logAnalyticsWorkspaceName
  scope: resourceGroup(monitoringResourceGroupName)
}

// Symbolic reference — Bicep infers the dependency
resource diagnosticSetting 'Microsoft.Insights/diagnosticSettings@2021-05-01-preview' = {
  name: 'send-to-law'
  scope: storageAccount
  properties: {
    workspaceId: logAnalytics.id  // No dependsOn needed
  }
}
```

---

## Module Design

- **One module = one logical unit** — storage account + its private endpoint = one module
- **Self-documenting** through parameter and output descriptions
- **Keep modules focused** — if it deploys unrelated resources, split it
- **Pass only what's needed** — explicit contracts, no parameter forwarding
- **Outputs expose what callers need** — IDs, names, principal IDs

---

## Tags

```bicep
var commonTags = {
  Environment: environment
  Project: project
  ManagedBy: 'Bicep'
  LastDeployed: utcNow('yyyy-MM-dd')
}

// Union for resource-specific additional tags
var storageSpecificTags = union(commonTags, {
  DataClassification: 'Internal'
  CostCenter: costCenterCode
})
```

Every taggable resource gets tags. A resource without tags causes billing and audit headaches.

---

## PR Rejection Criteria (Hard Stops)

These are not suggestions. These block the PR:

| Issue | Why |
|---|---|
| Parameters without `@description()` | Code is documentation |
| Hardcoded resource names or locations | Must be parameterized or derived |
| Secrets in outputs | Never expose secure values |
| No tags on taggable resources | Required for billing and audit |
| `dependsOn` when symbolic reference works | Code smell — comment required if genuinely needed |
| Deeply nested ternary expressions | Use a variable — nested ternaries are debugging nightmares |
| No `metadata description` on file | Every file declares what it is |
| Magic strings/numbers without explanation | Name it, comment it, make intent clear |

---

## Quick Reference Checklist

- [ ] File follows standard layout order
- [ ] All parameters have `@description()` and appropriate decorators
- [ ] All outputs have `@description()`
- [ ] `metadata description` present at file top
- [ ] Naming follows camelCase convention
- [ ] Tags applied to all taggable resources
- [ ] `existing` keyword used instead of hardcoded IDs
- [ ] Symbolic references instead of `dependsOn`
- [ ] `@secure()` on all secret parameters
- [ ] No secrets in outputs or variables that get logged

## Related Skills

- `iac-review` — Full IaC security, maintainability, and cost review checklist
- `naming-conventions` — Cross-language Azure resource and code naming standards

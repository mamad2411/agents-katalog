---
name: naming-conventions
description: >-
  Cross-language naming conventions for Azure resources, Terraform, Bicep,
  PowerShell, and general code. Provides consistent naming patterns for
  infrastructure, variables, files, and project structure.
when-to-use: >-
  Invoke when starting a new module, function, or deployment. Also invoke when
  reviewing code for naming consistency, establishing naming standards for a
  team, or onboarding engineers to a codebase.
categories:
  - code-style
  - infrastructure
  - standards
---

# Naming Conventions

Consistent naming across all code makes it scannable, searchable, and maintainable. These conventions apply to Azure resources, Terraform, Bicep, PowerShell, and general infrastructure code.

## Azure Resource Naming

### Standard Pattern

```
{project}-{environment}-{region}-{resource-type}-{instance}

Examples:
contoso-prod-eus2-rg-001
contoso-dev-wus3-kv-001
contoso-staging-eus2-app-api
```

### Abbreviations

| Resource Type | Abbreviation |
|---|---|
| Resource Group | `rg` |
| Virtual Network | `vnet` |
| Subnet | `snet` |
| Network Security Group | `nsg` |
| Storage Account | `st` (no hyphens, 3-24 chars) |
| Key Vault | `kv` |
| App Service | `app` |
| App Service Plan | `asp` |
| Function App | `func` |
| SQL Server | `sql` |
| SQL Database | `sqldb` |
| Cosmos DB Account | `cosmos` |
| Log Analytics Workspace | `log` |
| Application Insights | `appi` |
| Container Registry | `cr` (no hyphens) |
| AKS Cluster | `aks` |
| Public IP | `pip` |
| Load Balancer | `lb` |
| Front Door | `fd` |

### Constraints

| Resource | Max Length | Allowed Characters | Notes |
|---|---|---|---|
| Storage Account | 24 | lowercase alphanumeric only | No hyphens, globally unique |
| Key Vault | 24 | alphanumeric + hyphens | Globally unique |
| Resource Group | 90 | alphanumeric, hyphens, underscores | |
| VM Name | 64 (Linux), 15 (Windows) | alphanumeric, hyphens | Windows limit is the common constraint |

---

## Terraform Naming

| Element | Convention | Example |
|---|---|---|
| Resource labels | `snake_case`, descriptive | `resource "azurerm_subnet" "app_gateway"` |
| Variables | `snake_case` | `variable "vnet_address_space"` |
| Locals | `snake_case` | `local.name_prefix` |
| Outputs | `snake_case`, `<type>_<attribute>` | `output "resource_group_id"` |
| Files | `snake_case.tf` | `network.tf`, `variables.tf` |
| Module directories | `kebab-case` | `modules/storage-account/` |

### Resource Label Rules
- One of a type → `main` or `this`
- Multiple of a type → descriptive names (`app_gateway`, `private_endpoints`)
- Avoid redundancy: `resource "azurerm_virtual_network" "hub"` not `"vnet"`

---

## Bicep Naming

| Element | Convention | Example |
|---|---|---|
| Resources (symbolic) | `camelCase` | `resource storageAccount` |
| Parameters | `camelCase` | `param storageAccountName string` |
| Variables | `camelCase` | `var namePrefix` |
| Outputs | `camelCase` | `output storageAccountId string` |
| Module symbolic names | `camelCase` | `module storageAccount` |
| Module file names | `kebab-case` | `storage-account.bicep` |
| User-defined types | `camelCase` + `Type` suffix | `type subnetConfigType` |

---

## PowerShell Naming

| Element | Convention | Example |
|---|---|---|
| Functions | `Verb-Noun` (approved verbs) | `Get-StaleServicePrincipal` |
| Parameters | `PascalCase` | `$UserPrincipalName` |
| Local variables | `camelCase` | `$retryCount` |
| Boolean parameters | Standard names | `$Force`, `$WhatIf`, `$Confirm` |
| Script files | `Verb-Noun.ps1` | `Get-StaleServicePrincipal.ps1` |
| Module folders | `PascalCase` | `StaleServicePrincipal/` |

### Approved Verbs
Use `Get-Verb` to see the full list. Common ones: `Get`, `Set`, `New`, `Remove`, `Import`, `Export`, `Invoke`, `Test`, `Start`, `Stop`, `Enable`, `Disable`.

---

## General Code Naming

### Variables and Functions

| Language | Variables | Functions/Methods | Constants |
|---|---|---|---|
| C# / .NET | `camelCase` | `PascalCase` | `PascalCase` |
| TypeScript | `camelCase` | `camelCase` | `UPPER_SNAKE_CASE` |
| Python | `snake_case` | `snake_case` | `UPPER_SNAKE_CASE` |
| Go | `camelCase` (unexported), `PascalCase` (exported) | Same | Same |

### Files and Directories

| Context | Convention | Example |
|---|---|---|
| Terraform files | `snake_case.tf` | `network.tf` |
| Bicep files | `kebab-case.bicep` | `storage-account.bicep` |
| PowerShell scripts | `Verb-Noun.ps1` | `Get-StaleServicePrincipal.ps1` |
| Documentation | `kebab-case.md` | `getting-started.md` |
| Kubernetes manifests | `kebab-case.yaml` | `app-deployment.yaml` |
| Docker | `Dockerfile` (no extension) | `Dockerfile` |

---

## Tags (Azure Resources)

Every taggable resource gets these minimum tags:

| Tag | Purpose | Example |
|---|---|---|
| `Environment` | Deployment stage | `dev`, `staging`, `prod` |
| `Project` | Business project | `contoso-api` |
| `ManagedBy` | IaC tool | `terraform`, `Bicep` |
| `Owner` | Responsible team | `platform-engineering` |
| `CostCenter` | Billing allocation | `CC-12345` |

---

## Naming Checklist

- [ ] Azure resources follow `{project}-{env}-{region}-{type}-{instance}` pattern
- [ ] Resource names respect length and character constraints
- [ ] Code naming matches language convention (snake_case, camelCase, PascalCase)
- [ ] File names match language convention
- [ ] No abbreviations that aren't in the standard abbreviation table
- [ ] Tags applied to all taggable resources
- [ ] Naming is consistent within the project (pick one pattern, stick to it)
- [ ] Names are descriptive enough to understand without surrounding context

## Related Skills

- `terraform-style-guide` — Terraform-specific naming and formatting
- `bicep-style-guide` — Bicep-specific naming and formatting
- `powershell-style-guide` — PowerShell-specific naming and formatting

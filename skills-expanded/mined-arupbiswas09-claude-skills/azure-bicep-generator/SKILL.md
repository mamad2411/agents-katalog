---
name: azure-bicep-generator
description: Generate, validate, explain, and refactor Azure Bicep templates for infrastructure-as-code deployments.
---

# Azure Bicep Generator

Generate, validate, explain, and refactor Azure Bicep templates for infrastructure-as-code deployments.

## Trigger

Use this skill when the user asks to:
- Write or generate a Bicep template or module
- Convert an ARM JSON template to Bicep
- Explain what a Bicep file does
- Refactor Bicep for reusability or parameterisation
- Add secure defaults, tagging, or naming conventions to existing templates
- Troubleshoot a Bicep compilation or deployment error
- Scaffold a module registry structure

## Instructions

### Before writing a template

Ask (or infer from context) the following if not already provided:

1. **Resource type** — what Azure resource(s) are being created?
2. **Scope** — `resourceGroup` (default), `subscription`, `managementGroup`, or `tenant`?
3. **Environment** — dev / staging / prod (drives SKU defaults and retention settings)?
4. **Module or main template** — standalone deployment file, or a reusable module?
5. **Naming** — prefix/suffix convention, or should names be generated from parameters?

### File structure rules

Every Bicep file must follow this top-to-bottom order:

```bicep
// 1. targetScope (omit if resourceGroup — it's the default)
targetScope = 'subscription'

// 2. Parameters (with decorators before each)
@description('...')
@minLength(2)
param location string = resourceGroup().location

// 3. Variables
var resourceName = '${prefix}-${environment}-rg'

// 4. Existing resources (if referencing pre-existing infra)
resource existingVnet 'Microsoft.Network/virtualNetworks@2024-01-01' existing = {
  name: vnetName
}

// 5. New resources
resource storageAccount 'Microsoft.Storage/storageAccounts@2023-05-01' = { ... }

// 6. Modules
module keyVault './modules/key-vault.bicep' = { ... }

// 7. Outputs
output storageAccountId string = storageAccount.id
```

### Parameter rules

Always apply appropriate decorators — they enable portal validation and `bicep linter` checks:

```bicep
@description('Azure region for all resources.')
param location string = resourceGroup().location

@description('Environment name. Controls SKU and retention defaults.')
@allowed(['dev', 'staging', 'prod'])
param environment string

@description('Short prefix for resource naming (2–8 chars, lowercase, no hyphens).')
@minLength(2)
@maxLength(8)
param prefix string

@description('Resource tags applied to every resource.')
param tags object = {}

@description('Admin password — sourced from Key Vault in pipelines.')
@secure()
param adminPassword string
```

**Never** hardcode secrets, connection strings, or passwords in Bicep. Use `@secure()` params and wire them to Key Vault references in the parameter file.

### Naming convention

Follow the Cloud Adoption Framework (CAF) abbreviation scheme by default. Build names from a variable so they're consistent:

```bicep
var nameSuffix = '${prefix}-${environment}-${location}'

// Examples using CAF abbreviations:
var storageAccountName = 'st${prefix}${environment}'          // no hyphens, max 24 chars
var keyVaultName        = 'kv-${nameSuffix}'
var appServicePlanName  = 'asp-${nameSuffix}'
var webAppName          = 'app-${nameSuffix}'
var containerRegistryName = 'cr${prefix}${environment}'       // alphanumeric only
```

CAF abbreviations quick reference: `rg` resource group · `vnet` VNet · `snet` subnet · `nsg` NSG · `pip` public IP · `lb` load balancer · `agw` Application Gateway · `kv` Key Vault · `st` storage · `sql` SQL server · `sqldb` SQL database · `cr` Container Registry · `aks` AKS · `plan` / `asp` App Service plan · `app` web app · `func` function app · `sb` Service Bus · `evh` Event Hub · `apim` API Management · `law` Log Analytics workspace · `ai` Application Insights

### Tagging

Always merge caller-supplied tags with a set of mandatory tags:

```bicep
param tags object = {}

var mandatoryTags = {
  environment: environment
  managedBy: 'bicep'
  deployedAt: utcNow('yyyy-MM-dd')
}

var allTags = union(tags, mandatoryTags)
```

Apply `tags: allTags` to every top-level resource.

### API versions

Always use a **recent, stable** API version — never `latest`. Check `az provider show` or the Bicep VSCode extension for current versions. Common ones as of mid-2025:

| Resource | API version |
|----------|------------|
| `Microsoft.Storage/storageAccounts` | `2023-05-01` |
| `Microsoft.KeyVault/vaults` | `2023-07-01` |
| `Microsoft.Web/serverfarms` | `2024-04-01` |
| `Microsoft.Web/sites` | `2024-04-01` |
| `Microsoft.ContainerService/managedClusters` | `2024-09-01` |
| `Microsoft.Sql/servers` | `2023-08-01-preview` |
| `Microsoft.Network/virtualNetworks` | `2024-01-01` |
| `Microsoft.Insights/components` | `2020-02-02` |
| `Microsoft.OperationalInsights/workspaces` | `2023-09-01` |
| `Microsoft.Authorization/roleAssignments` | `2022-04-01` |

### Security defaults (apply unless overridden)

| Resource | Secure default |
|----------|---------------|
| Storage account | `allowBlobPublicAccess: false`, `minimumTlsVersion: 'TLS1_2'`, `supportsHttpsTrafficOnly: true` |
| Key Vault | `enableSoftDelete: true`, `softDeleteRetentionInDays: 90`, `enablePurgeProtection: true`, RBAC auth (`enableRbacAuthorization: true`) |
| SQL Server | `minimalTlsVersion: '1.2'`, no public endpoint for prod |
| App Service | `httpsOnly: true`, `clientAffinityEnabled: false`, `ftpsState: 'Disabled'` |
| AKS | System node pool with taints, RBAC, managed identity (not service principal), `disableLocalAccounts: true` for prod |
| Container Registry | `adminUserEnabled: false`, private endpoint for prod |

### Loops and conditions

```bicep
// Conditional resource (deploy only in prod)
resource purgeProtection 'Microsoft.KeyVault/vaults@2023-07-01' = if (environment == 'prod') { ... }

// Loop over an array parameter
param subnetConfigs array = [
  { name: 'snet-app', addressPrefix: '10.0.1.0/24' }
  { name: 'snet-data', addressPrefix: '10.0.2.0/24' }
]

resource subnets 'Microsoft.Network/virtualNetworks/subnets@2024-01-01' = [
  for subnet in subnetConfigs: {
    name: subnet.name
    parent: vnet
    properties: { addressPrefix: subnet.addressPrefix }
  }
]

// Loop with index
resource slots 'Microsoft.Web/sites/slots@2024-04-01' = [
  for (slot, i) in ['staging', 'canary']: {
    name: slot
    parent: webApp
    location: location
    properties: {}
  }
]
```

### Modules

Structure reusable modules so they take only what they need:

```bicep
// modules/storage.bicep — module file
@description('Storage account name (globally unique, 3–24 chars).')
@minLength(3)
@maxLength(24)
param name string

param location string
param tags object
param allowBlobPublicAccess bool = false

resource sa 'Microsoft.Storage/storageAccounts@2023-05-01' = {
  name: name
  location: location
  tags: tags
  sku: { name: 'Standard_LRS' }
  kind: 'StorageV2'
  properties: {
    allowBlobPublicAccess: allowBlobPublicAccess
    minimumTlsVersion: 'TLS1_2'
    supportsHttpsTrafficOnly: true
  }
}

output id string = sa.id
output name string = sa.name
output primaryEndpoints object = sa.properties.primaryEndpoints
```

Call it from a main template:

```bicep
module storage './modules/storage.bicep' = {
  name: 'storage-deployment'
  params: {
    name: storageAccountName
    location: location
    tags: allTags
  }
}

output storageId string = storage.outputs.id
```

### Outputs

Always output the IDs and names of created resources — downstream templates and pipelines need them:

```bicep
output resourceGroupId string = resourceGroup().id
output storageAccountId string = storageAccount.id
output storageAccountName string = storageAccount.name
output keyVaultUri string = keyVault.properties.vaultUri
output aksClusterName string = aksCluster.name
output aksOidcIssuerUrl string = aksCluster.properties.oidcIssuerProfile.issuerURL
```

### ARM to Bicep conversion

When the user provides an ARM JSON template to convert:

1. Use `az bicep decompile --file template.json` as the recommended first step
2. Then clean up the output:
   - Replace `[resourceId(...)]` expressions with symbolic references
   - Replace `[concat(...)]` with string interpolation `'${...}'`
   - Replace `[parameters('x')]` with the param name directly
   - Replace `[variables('x')]` with the var name directly
   - Add `@description()` decorators to all parameters
   - Collapse single-use variables
   - Remove `dependsOn` arrays — Bicep infers them from symbolic references

### Explaining an existing template

When the user pastes a Bicep file:

1. State the deployment scope and what resources are created
2. Identify parameters with no defaults (required at deploy time)
3. Walk through each resource, one sentence each
4. Highlight any security concerns (public access, missing soft-delete, etc.)
5. Note any hardcoded values that should be parameterised

### Troubleshooting deployment errors

Common errors and fixes:

| Error | Fix |
|-------|-----|
| `BCP018: Expected the `:` character` | Missing colon in object property |
| `BCP057: The name X does not exist` | Symbolic name typo or missing `existing` keyword |
| `BCP035: The specified object is missing required properties` | Add all required resource properties |
| `InvalidTemplate: Deployment template validation failed` | Check API version and required properties against the ARM spec |
| `RoleAssignmentExists` | Use `'None'` for `roleAssignmentConditionVersion` or check idempotency |
| `StorageAccountAlreadyTaken` | Name is globally unique — adjust naming variable |
| `PrincipalNotFound` | Managed identity or principal hasn't propagated yet — add `dependsOn` |

### Deployment commands

Include these for the user when relevant:

```bash
# Validate (no deployment)
az deployment group validate \
  --resource-group myRG \
  --template-file main.bicep \
  --parameters @main.parameters.json

# What-if (preview changes)
az deployment group what-if \
  --resource-group myRG \
  --template-file main.bicep \
  --parameters @main.parameters.json

# Deploy
az deployment group create \
  --resource-group myRG \
  --template-file main.bicep \
  --parameters @main.parameters.json \
  --name "deploy-$(date +%Y%m%d%H%M%S)"

# Subscription-scope deploy
az deployment sub create \
  --location eastus \
  --template-file main.bicep \
  --parameters @main.parameters.json
```

## References

- [Bicep syntax cheatsheet](./references/bicep-cheatsheet.md)
- [Common resource modules](./references/resource-modules.md)
- [Best practices: naming, tagging, security](./references/best-practices.md)
- Official docs: https://learn.microsoft.com/en-us/azure/azure-resource-manager/bicep/
- CAF naming: https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/azure-best-practices/resource-naming

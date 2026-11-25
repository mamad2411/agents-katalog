---
name: azure-policy-author
description: Write, test, assign, and remediate Azure Policy definitions and initiatives (policy sets).
---

# Azure Policy Author

Write, test, assign, and remediate Azure Policy definitions and initiatives (policy sets).

## Trigger

Use this skill when the user asks to:
- Write a custom Azure Policy definition
- Group policies into an initiative (policy set)
- Assign a policy or initiative to a scope (subscription, management group, resource group)
- Create a remediation task for a `deployIfNotExists` or `modify` policy
- Add an exemption for a specific resource or resource group
- Understand why a resource is non-compliant
- Find built-in policies for a specific requirement
- Audit or enforce tagging, SKU restrictions, allowed locations, or diagnostic settings

## Instructions

### Before writing a policy

Ask (or infer) the following if not already provided:

1. **Goal** — audit (report only), deny (block), or auto-remediate (deploy/modify)?
2. **Scope** — management group, subscription, or resource group?
3. **Resource type** — which ARM resource type does this policy target?
4. **Condition** — what property triggers the policy, and what is the desired state?
5. **Exemptions expected** — are there known resources that must be excluded?

### Policy definition structure

```json
{
  "name": "kebab-case-unique-name",
  "type": "Microsoft.Authorization/policyDefinitions",
  "properties": {
    "displayName": "Human-readable title",
    "description": "What this policy enforces and why.",
    "policyType": "Custom",
    "mode": "All",
    "metadata": {
      "category": "Tags",
      "version": "1.0.0"
    },
    "parameters": {
      "paramName": {
        "type": "String",
        "metadata": { "displayName": "...", "description": "..." },
        "defaultValue": "default"
      }
    },
    "policyRule": {
      "if": { /* condition */ },
      "then": { "effect": "[parameters('effect')]" }
    }
  }
}
```

### Mode

| Mode | Use when |
|------|---------|
| `"All"` | Targeting resource groups, subscriptions, or tagged resources |
| `"Indexed"` | Targeting resources that support tags and location (most compute/storage/network) |
| `"Microsoft.Kubernetes.Data"` | AKS admission control (Gatekeeper) |
| `"Microsoft.KeyVault.Data"` | Key Vault keys and certificates (data plane) |
| `"Microsoft.Network.Data"` | Azure Virtual Network Manager |

Default to `"All"` unless targeting a specific data-plane provider.

### Effect types

| Effect | Behaviour | When to use |
|--------|-----------|------------|
| `Audit` | Marks non-compliant, no block | Visibility without enforcement |
| `Deny` | Blocks the ARM request | Hard enforcement |
| `AuditIfNotExists` | Audits if a related child resource is missing | Check for diagnostics, extensions |
| `DeployIfNotExists` | Deploys a related resource if missing | Auto-remediate missing diagnostics, extensions |
| `Modify` | Adds/replaces/removes tags or properties | Tag enforcement, property correction |
| `Append` | Adds properties to the resource on creation | Add IP rules, tags (append-only) |
| `Disabled` | Policy is inactive | Draft / temporarily disabled |

Always parameterise the effect so assignments can choose audit-before-enforce:

```json
"parameters": {
  "effect": {
    "type": "String",
    "allowedValues": ["Audit", "Deny", "Disabled"],
    "defaultValue": "Audit",
    "metadata": { "displayName": "Effect" }
  }
}
```

### Condition operators

```json
// Equality
{ "field": "type", "equals": "Microsoft.Storage/storageAccounts" }
{ "field": "type", "notEquals": "Microsoft.Storage/storageAccounts" }

// Containment
{ "field": "location", "in": ["eastus", "westeurope"] }
{ "field": "location", "notIn": ["australiaeast"] }

// Existence
{ "field": "tags['environment']", "exists": "true" }
{ "field": "tags['environment']", "exists": "false" }

// Pattern
{ "field": "name", "like": "prod-*" }
{ "field": "name", "notLike": "test-*" }
{ "field": "name", "match": "prod-???-[0-9][0-9]" }   // ? = single char, [0-9] = range

// String contains
{ "field": "kind", "contains": "Storage" }

// Logical
{ "allOf": [ condA, condB ] }   // AND
{ "anyOf": [ condA, condB ] }   // OR
{ "not": condA }
```

### Finding alias names

```bash
# List all aliases for a resource type
az provider show \
  --namespace Microsoft.Storage \
  --expand resourceTypes \
  --query "resourceTypes[?resourceType=='storageAccounts'].aliases[].name" \
  --output tsv

# Or search for a specific property alias
az provider show \
  --namespace Microsoft.Storage \
  --expand resourceTypes \
  --query "resourceTypes[?resourceType=='storageAccounts'].aliases[?contains(name,'minimumTlsVersion')].name"
```

### Common pattern: require tag

```json
{
  "policyRule": {
    "if": {
      "allOf": [
        { "field": "type", "notIn": ["Microsoft.Resources/subscriptions/resourceGroups"] },
        { "field": "[concat('tags[', parameters('tagName'), ']')]", "exists": "false" }
      ]
    },
    "then": { "effect": "[parameters('effect')]" }
  }
}
```

### Common pattern: inherit tag from resource group (Modify)

```json
{
  "policyRule": {
    "if": {
      "allOf": [
        { "field": "type", "notIn": ["Microsoft.Resources/subscriptions/resourceGroups"] },
        {
          "field": "[concat('tags[', parameters('tagName'), ']')]",
          "notEquals": "[resourceGroup().tags[parameters('tagName')]]"
        }
      ]
    },
    "then": {
      "effect": "Modify",
      "details": {
        "roleDefinitionIds": [
          "/providers/Microsoft.Authorization/roleDefinitions/b24988ac-6180-42a0-ab88-20f7382dd24c"
        ],
        "operations": [
          {
            "operation": "addOrReplace",
            "field": "[concat('tags[', parameters('tagName'), ']')]",
            "value": "[resourceGroup().tags[parameters('tagName')]]"
          }
        ]
      }
    }
  }
}
```

### Common pattern: deploy diagnostic settings (DeployIfNotExists)

```json
{
  "policyRule": {
    "if": { "field": "type", "equals": "Microsoft.KeyVault/vaults" },
    "then": {
      "effect": "DeployIfNotExists",
      "details": {
        "type": "Microsoft.Insights/diagnosticSettings",
        "name": "setByPolicy",
        "existenceCondition": {
          "allOf": [
            { "field": "Microsoft.Insights/diagnosticSettings/workspaceId", "equals": "[parameters('logAnalyticsWorkspaceId')]" }
          ]
        },
        "roleDefinitionIds": [
          "/providers/Microsoft.Authorization/roleDefinitions/b24988ac-6180-42a0-ab88-20f7382dd24c"
        ],
        "deployment": {
          "properties": {
            "mode": "incremental",
            "template": {
              "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#",
              "contentVersion": "1.0.0.0",
              "parameters": {
                "resourceName": { "type": "string" },
                "location": { "type": "string" },
                "workspaceId": { "type": "string" }
              },
              "resources": [
                {
                  "type": "Microsoft.KeyVault/vaults/providers/diagnosticSettings",
                  "apiVersion": "2021-05-01-preview",
                  "name": "[concat(parameters('resourceName'), '/Microsoft.Insights/setByPolicy')]",
                  "location": "[parameters('location')]",
                  "properties": {
                    "workspaceId": "[parameters('workspaceId')]",
                    "logs": [
                      { "category": "AuditEvent", "enabled": true },
                      { "category": "AzurePolicyEvaluationDetails", "enabled": true }
                    ]
                  }
                }
              ]
            },
            "parameters": {
              "resourceName": { "value": "[field('name')]" },
              "location": { "value": "[field('location')]" },
              "workspaceId": { "value": "[parameters('logAnalyticsWorkspaceId')]" }
            }
          }
        }
      }
    }
  }
}
```

### Initiative (policy set) structure

```json
{
  "name": "my-initiative",
  "type": "Microsoft.Authorization/policySetDefinitions",
  "properties": {
    "displayName": "My Governance Initiative",
    "description": "Bundles tagging, security, and diagnostic policies.",
    "policyType": "Custom",
    "metadata": { "category": "Governance", "version": "1.0.0" },
    "parameters": {
      "logAnalyticsWorkspaceId": {
        "type": "String",
        "metadata": { "displayName": "Log Analytics Workspace ID" }
      }
    },
    "policyDefinitions": [
      {
        "policyDefinitionId": "/subscriptions/{subId}/providers/Microsoft.Authorization/policyDefinitions/require-environment-tag",
        "parameters": {
          "tagName": { "value": "environment" }
        }
      },
      {
        "policyDefinitionId": "/providers/Microsoft.Authorization/policyDefinitions/a6fb4358-5bf4-4ad7-ba82-2cd2f41ce5e9",
        "parameters": {}
      }
    ]
  }
}
```

### Assignment

```bash
# Assign policy at subscription scope
az policy assignment create \
  --name "require-environment-tag" \
  --display-name "Require environment tag on all resources" \
  --policy "/subscriptions/{subId}/providers/Microsoft.Authorization/policyDefinitions/require-environment-tag" \
  --scope "/subscriptions/{subId}" \
  --params '{"tagName": {"value": "environment"}, "effect": {"value": "Deny"}}' \
  --identity-scope "/subscriptions/{subId}" \
  --role Contributor \
  --location eastus

# Assign initiative at management group scope
az policy assignment create \
  --name "platform-governance" \
  --policy-set-definition "/providers/Microsoft.Management/managementGroups/contoso/providers/Microsoft.Authorization/policySetDefinitions/my-initiative" \
  --scope "/providers/Microsoft.Management/managementGroups/contoso" \
  --location eastus \
  --mi-system-assigned
```

`--mi-system-assigned` + `--location` is required for `DeployIfNotExists` and `Modify` policies — the assignment needs a managed identity to perform remediation.

### Remediation task

```bash
# Trigger remediation for non-compliant resources
az policy remediation create \
  --name "remediate-diagnostic-settings" \
  --policy-assignment "/subscriptions/{subId}/providers/Microsoft.Authorization/policyAssignments/deploy-diag-settings" \
  --resource-discovery-mode ReEvaluateCompliance \
  --resource-group myRG   # omit to remediate entire subscription scope

# Check remediation status
az policy remediation show \
  --name "remediate-diagnostic-settings" \
  --resource-group myRG
```

### Exemption

```bash
az policy exemption create \
  --name "legacy-app-exemption" \
  --display-name "Legacy app: TLS 1.1 required until Q3 migration" \
  --exemption-category Waiver \
  --policy-assignment "/subscriptions/{subId}/providers/Microsoft.Authorization/policyAssignments/require-tls12" \
  --scope "/subscriptions/{subId}/resourceGroups/rg-legacy/providers/Microsoft.Web/sites/old-app" \
  --expires-on "2026-09-30T00:00:00Z"
```

Categories: `Waiver` (intentional non-compliance) or `Mitigated` (compliance achieved another way).

### Testing a policy

```bash
# Evaluate compliance without assigning (requires Az PowerShell or REST)
# Use "what-if" via a test resource group with deny assignment + audit first

# Check current compliance state
az policy state list \
  --resource "/subscriptions/{subId}/resourceGroups/myRG/providers/Microsoft.Storage/storageAccounts/mysa" \
  --query "[].{Policy:policyDefinitionName, State:complianceState, Effect:effectiveEffect}"
```

### Troubleshooting non-compliance

1. `az policy state list --resource <id>` — shows which policies are non-compliant and why
2. Check the alias used in the condition: `az provider show ... --query "...aliases"` to confirm the property path
3. For `DeployIfNotExists`: check the managed identity has the role listed in `roleDefinitionIds`
4. For `Modify`: confirm the resource type supports `Modify` (not all do — some require `Append`)
5. Compliance state updates on a ~15-minute cycle; force re-evaluation: `az policy state trigger-scan --resource-group myRG`

## References

- [Policy definition cheatsheet](./references/policy-cheatsheet.md)
- [Common policy patterns](./references/policy-patterns.md)
- [Initiatives, assignments, and remediation](./references/initiative-and-remediation.md)
- Official docs: https://learn.microsoft.com/en-us/azure/governance/policy/

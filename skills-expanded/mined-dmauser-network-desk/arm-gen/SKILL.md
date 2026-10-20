# Skill: ARM Template Generation

## Purpose

Generate production-ready Azure Resource Manager (ARM) JSON templates for networking infrastructure. Provides complete templates with parameter files, linked templates for modularity, and deployment-ready configurations following Azure best practices.

---

## Core Conventions

### Template Schema

```json
{
  "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#",
  "contentVersion": "1.0.0.0",
  "metadata": {
    "description": "Deploys networking infrastructure for hub-spoke topology"
  },
  "parameters": {},
  "variables": {},
  "resources": [],
  "outputs": {}
}
```

### API Versions

Pin API versions that are tested with the template and supported for the target cloud/region. Avoid hard-coded “latest” tables in generated ARM guidance; verify current `Microsoft.Network/*` resource versions in Azure template reference and document any preview-version dependency before use.

### Naming Convention Variables

```json
"variables": {
  "prefix": "[parameters('organizationPrefix')]",
  "suffix": "[format('{0}-{1}', parameters('environment'), parameters('regionCode'))]",
  "vnetHubName": "[format('{0}-vnet-hub-{1}', variables('prefix'), variables('suffix'))]",
  "nsgNameTemplate": "[format('{0}-nsg-{{0}}-{1}', variables('prefix'), variables('suffix'))]",
  "fwName": "[format('{0}-fw-{1}', variables('prefix'), variables('suffix'))]"
}
```

---

## Template Patterns

### 1. Hub VNet with Subnets

```json
{
  "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#",
  "contentVersion": "1.0.0.0",
  "parameters": {
    "prefix": {
      "type": "string",
      "metadata": { "description": "Organization prefix for resource naming" }
    },
    "environment": {
      "type": "string",
      "allowedValues": ["dev", "test", "staging", "prod"],
      "metadata": { "description": "Target environment" }
    },
    "regionCode": {
      "type": "string",
      "defaultValue": "eus2",
      "metadata": { "description": "Short region code" }
    },
    "location": {
      "type": "string",
      "defaultValue": "[resourceGroup().location]",
      "metadata": { "description": "Azure region" }
    },
    "hubAddressSpace": {
      "type": "string",
      "defaultValue": "10.0.0.0/16",
      "metadata": { "description": "Hub VNet address space" }
    },
    "subnets": {
      "type": "array",
      "defaultValue": [
        { "name": "AzureFirewallSubnet", "prefix": "10.0.1.0/26" },
        { "name": "AzureFirewallManagementSubnet", "prefix": "10.0.1.64/26" },
        { "name": "GatewaySubnet", "prefix": "10.0.255.0/27" },
        { "name": "AzureBastionSubnet", "prefix": "10.0.2.0/26" },
        { "name": "snet-shared", "prefix": "10.0.10.0/24" }
      ],
      "metadata": { "description": "Array of subnet definitions" }
    }
  },
  "variables": {
    "vnetName": "[format('{0}-vnet-hub-{1}-{2}', parameters('prefix'), parameters('environment'), parameters('regionCode'))]"
  },
  "resources": [
    {
      "type": "Microsoft.Network/virtualNetworks",
      "apiVersion": "2024-01-01",
      "name": "[variables('vnetName')]",
      "location": "[parameters('location')]",
      "tags": {
        "Environment": "[parameters('environment')]",
        "ManagedBy": "ARM"
      },
      "properties": {
        "addressSpace": {
          "addressPrefixes": ["[parameters('hubAddressSpace')]"]
        },
        "copy": [
          {
            "name": "subnets",
            "count": "[length(parameters('subnets'))]",
            "input": {
              "name": "[parameters('subnets')[copyIndex('subnets')].name]",
              "properties": {
                "addressPrefix": "[parameters('subnets')[copyIndex('subnets')].prefix]"
              }
            }
          }
        ]
      }
    }
  ],
  "outputs": {
    "vnetId": {
      "type": "string",
      "value": "[resourceId('Microsoft.Network/virtualNetworks', variables('vnetName'))]"
    },
    "vnetName": {
      "type": "string",
      "value": "[variables('vnetName')]"
    }
  }
}
```

### 2. NSG with Security Rules

```json
{
  "type": "Microsoft.Network/networkSecurityGroups",
  "apiVersion": "2024-01-01",
  "name": "[format('{0}-nsg-{1}-{2}-{3}', parameters('prefix'), parameters('subnetPurpose'), parameters('environment'), parameters('regionCode'))]",
  "location": "[parameters('location')]",
  "tags": {
    "Environment": "[parameters('environment')]",
    "ManagedBy": "ARM"
  },
  "properties": {
    "securityRules": [
      {
        "name": "Allow-HTTPS-Inbound",
        "properties": {
          "priority": 100,
          "direction": "Inbound",
          "access": "Allow",
          "protocol": "Tcp",
          "sourceAddressPrefix": "VirtualNetwork",
          "sourcePortRange": "*",
          "destinationAddressPrefix": "*",
          "destinationPortRange": "443"
        }
      },
      {
        "name": "Deny-All-Inbound",
        "properties": {
          "priority": 4096,
          "direction": "Inbound",
          "access": "Deny",
          "protocol": "*",
          "sourceAddressPrefix": "*",
          "sourcePortRange": "*",
          "destinationAddressPrefix": "*",
          "destinationPortRange": "*"
        }
      }
    ]
  }
}
```

### 3. Azure Firewall with Policy

```json
{
  "type": "Microsoft.Network/firewallPolicies",
  "apiVersion": "2024-01-01",
  "name": "[format('{0}-fwpol-{1}-{2}', parameters('prefix'), parameters('environment'), parameters('regionCode'))]",
  "location": "[parameters('location')]",
  "properties": {
    "sku": { "tier": "[parameters('firewallSku')]" },
    "threatIntelMode": "Alert",
    "dnsSettings": { "enableProxy": true }
  }
},
{
  "type": "Microsoft.Network/publicIPAddresses",
  "apiVersion": "2024-01-01",
  "name": "[format('{0}-pip-fw-{1}-{2}', parameters('prefix'), parameters('environment'), parameters('regionCode'))]",
  "location": "[parameters('location')]",
  "sku": { "name": "Standard" },
  "properties": { "publicIPAllocationMethod": "Static" }
},
{
  "type": "Microsoft.Network/azureFirewalls",
  "apiVersion": "2024-01-01",
  "name": "[format('{0}-fw-{1}-{2}', parameters('prefix'), parameters('environment'), parameters('regionCode'))]",
  "location": "[parameters('location')]",
  "dependsOn": [
    "[resourceId('Microsoft.Network/firewallPolicies', format('{0}-fwpol-{1}-{2}', parameters('prefix'), parameters('environment'), parameters('regionCode')))]",
    "[resourceId('Microsoft.Network/publicIPAddresses', format('{0}-pip-fw-{1}-{2}', parameters('prefix'), parameters('environment'), parameters('regionCode')))]"
  ],
  "properties": {
    "sku": {
      "name": "AZFW_VNet",
      "tier": "[parameters('firewallSku')]"
    },
    "firewallPolicy": {
      "id": "[resourceId('Microsoft.Network/firewallPolicies', format('{0}-fwpol-{1}-{2}', parameters('prefix'), parameters('environment'), parameters('regionCode')))]"
    },
    "ipConfigurations": [
      {
        "name": "fw-ipconfig",
        "properties": {
          "subnet": {
            "id": "[resourceId('Microsoft.Network/virtualNetworks/subnets', variables('vnetName'), 'AzureFirewallSubnet')]"
          },
          "publicIPAddress": {
            "id": "[resourceId('Microsoft.Network/publicIPAddresses', format('{0}-pip-fw-{1}-{2}', parameters('prefix'), parameters('environment'), parameters('regionCode')))]"
          }
        }
      }
    ]
  }
}
```

### 4. VPN Gateway

```json
{
  "type": "Microsoft.Network/publicIPAddresses",
  "apiVersion": "2024-01-01",
  "name": "[format('{0}-pip-vpngw-{1}-{2}', parameters('prefix'), parameters('environment'), parameters('regionCode'))]",
  "location": "[parameters('location')]",
  "sku": { "name": "Standard" },
  "properties": { "publicIPAllocationMethod": "Static" }
},
{
  "type": "Microsoft.Network/virtualNetworkGateways",
  "apiVersion": "2024-01-01",
  "name": "[format('{0}-vpngw-{1}-{2}', parameters('prefix'), parameters('environment'), parameters('regionCode'))]",
  "location": "[parameters('location')]",
  "dependsOn": [
    "[resourceId('Microsoft.Network/publicIPAddresses', format('{0}-pip-vpngw-{1}-{2}', parameters('prefix'), parameters('environment'), parameters('regionCode')))]"
  ],
  "properties": {
    "gatewayType": "Vpn",
    "vpnType": "RouteBased",
    "sku": {
      "name": "[parameters('vpnGatewaySku')]",
      "tier": "[parameters('vpnGatewaySku')]"
    },
    "ipConfigurations": [
      {
        "name": "default",
        "properties": {
          "subnet": {
            "id": "[resourceId('Microsoft.Network/virtualNetworks/subnets', variables('vnetName'), 'GatewaySubnet')]"
          },
          "publicIPAddress": {
            "id": "[resourceId('Microsoft.Network/publicIPAddresses', format('{0}-pip-vpngw-{1}-{2}', parameters('prefix'), parameters('environment'), parameters('regionCode')))]"
          }
        }
      }
    ],
    "enableBgp": true,
    "bgpSettings": {
      "asn": 65515
    }
  }
}
```

### 5. Private Endpoint

```json
{
  "type": "Microsoft.Network/privateEndpoints",
  "apiVersion": "2024-01-01",
  "name": "[format('{0}-pe-{1}-{2}-{3}', parameters('prefix'), parameters('groupId'), parameters('environment'), parameters('regionCode'))]",
  "location": "[parameters('location')]",
  "properties": {
    "subnet": {
      "id": "[parameters('subnetId')]"
    },
    "privateLinkServiceConnections": [
      {
        "name": "[format('plsc-{0}', parameters('groupId'))]",
        "properties": {
          "privateLinkServiceId": "[parameters('targetResourceId')]",
          "groupIds": ["[parameters('groupId')]"]
        }
      }
    ]
  }
},
{
  "type": "Microsoft.Network/privateEndpoints/privateDnsZoneGroups",
  "apiVersion": "2024-01-01",
  "name": "[format('{0}-pe-{1}-{2}-{3}/default', parameters('prefix'), parameters('groupId'), parameters('environment'), parameters('regionCode'))]",
  "dependsOn": [
    "[resourceId('Microsoft.Network/privateEndpoints', format('{0}-pe-{1}-{2}-{3}', parameters('prefix'), parameters('groupId'), parameters('environment'), parameters('regionCode')))]"
  ],
  "properties": {
    "privateDnsZoneConfigs": [
      {
        "name": "[format('config-{0}', parameters('groupId'))]",
        "properties": {
          "privateDnsZoneId": "[parameters('privateDnsZoneId')]"
        }
      }
    ]
  }
}
```

---

## Parameter File Pattern

```json
{
  "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentParameters.json#",
  "contentVersion": "1.0.0.0",
  "parameters": {
    "prefix": { "value": "contoso" },
    "environment": { "value": "prod" },
    "regionCode": { "value": "eus2" },
    "hubAddressSpace": { "value": "10.0.0.0/16" },
    "subnets": {
      "value": [
        { "name": "AzureFirewallSubnet", "prefix": "10.0.1.0/26" },
        { "name": "GatewaySubnet", "prefix": "10.0.255.0/27" },
        { "name": "AzureBastionSubnet", "prefix": "10.0.2.0/26" },
        { "name": "snet-shared", "prefix": "10.0.10.0/24" }
      ]
    },
    "firewallSku": { "value": "Standard" },
    "vpnGatewaySku": { "value": "VpnGw2" },
    "sharedKey": {
      "reference": {
        "keyVault": {
          "id": "/subscriptions/{sub-id}/resourceGroups/rg-keyvault/providers/Microsoft.KeyVault/vaults/kv-network-secrets"
        },
        "secretName": "vpn-shared-key"
      }
    }
  }
}
```

---

## Linked Template Structure

```
arm-templates/
├── azuredeploy.json              // Main orchestrator template
├── azuredeploy.parameters.dev.json
├── azuredeploy.parameters.prod.json
├── linked/
│   ├── vnet.json                 // VNet + subnets
│   ├── nsg.json                  // NSG with rules
│   ├── firewall.json             // Azure Firewall + policy
│   ├── vpn-gateway.json          // VPN Gateway + connection
│   ├── route-table.json          // UDR
│   └── private-endpoint.json     // PE + DNS zone group
└── README.md
```

### Main Orchestrator Template (Linked Deployments)

```json
{
  "resources": [
    {
      "type": "Microsoft.Resources/deployments",
      "apiVersion": "2022-09-01",
      "name": "deploy-hub-vnet",
      "properties": {
        "mode": "Incremental",
        "templateLink": {
          "uri": "[format('{0}linked/vnet.json{1}', parameters('templateBaseUri'), parameters('sasToken'))]"
        },
        "parameters": {
          "prefix": { "value": "[parameters('prefix')]" },
          "environment": { "value": "[parameters('environment')]" },
          "hubAddressSpace": { "value": "[parameters('hubAddressSpace')]" }
        }
      }
    },
    {
      "type": "Microsoft.Resources/deployments",
      "apiVersion": "2022-09-01",
      "name": "deploy-firewall",
      "dependsOn": ["deploy-hub-vnet"],
      "properties": {
        "mode": "Incremental",
        "templateLink": {
          "uri": "[format('{0}linked/firewall.json{1}', parameters('templateBaseUri'), parameters('sasToken'))]"
        },
        "parameters": {
          "prefix": { "value": "[parameters('prefix')]" },
          "environment": { "value": "[parameters('environment')]" },
          "vnetName": { "value": "[reference('deploy-hub-vnet').outputs.vnetName.value]" }
        }
      }
    }
  ]
}
```

---

## Validation Commands

```bash
# Validate template syntax
az deployment group validate \
  --resource-group rg-network-prod \
  --template-file azuredeploy.json \
  --parameters azuredeploy.parameters.prod.json

# What-If (preview changes without deploying)
az deployment group what-if \
  --resource-group rg-network-prod \
  --template-file azuredeploy.json \
  --parameters azuredeploy.parameters.prod.json

# Deploy with confirmation
az deployment group create \
  --resource-group rg-network-prod \
  --template-file azuredeploy.json \
  --parameters azuredeploy.parameters.prod.json \
  --confirm-with-what-if

# View deployment operations (troubleshooting)
az deployment operation group list \
  --resource-group rg-network-prod \
  --name <deployment-name>
```

**Analysis only — verify against vendor documentation before applying.**

# Skill: Bicep Template Generation

## Purpose

Generate production-ready Azure Bicep templates for networking infrastructure. Provides modular, parameterized templates following Azure best practices and latest API versions.

---

## Core Conventions

### API Versions

Pin API versions that are tested with the template and supported for the target cloud/region. Do not assume a static table is always the latest stable version; verify current `Microsoft.Network/*` versions in Azure template reference before publishing, and avoid preview API versions unless the design explicitly accepts preview support risk.

### Naming Conventions

```bicep
// Parameters for naming
param prefix string = 'contoso'
param environment string = 'prod'
param location string = resourceGroup().location
param regionCode string = 'eus2'  // eastus2

// Naming pattern: {prefix}-{resourceType}-{purpose}-{environment}-{region}
var vnetName = '${prefix}-vnet-hub-${environment}-${regionCode}'
var nsgName = '${prefix}-nsg-${subnetPurpose}-${environment}-${regionCode}'
var fwName = '${prefix}-fw-${environment}-${regionCode}'
```

### Standard Parameters

```bicep
@description('Deployment prefix for resource naming')
param prefix string

@description('Target environment')
@allowed(['dev', 'test', 'staging', 'prod'])
param environment string

@description('Azure region for deployment')
param location string = resourceGroup().location

@description('Tags applied to all resources')
param tags object = {
  Environment: environment
  ManagedBy: 'Bicep'
  Project: 'NetworkInfra'
}
```

---

## Template Patterns

### 1. Hub VNet with Subnets

```bicep
@description('Hub VNet address space')
param hubAddressSpace string = '10.0.0.0/16'

@description('Subnet definitions')
param subnets array = [
  { name: 'AzureFirewallSubnet', prefix: '10.0.1.0/26' }
  { name: 'AzureFirewallManagementSubnet', prefix: '10.0.1.64/26' }
  { name: 'GatewaySubnet', prefix: '10.0.255.0/27' }
  { name: 'AzureBastionSubnet', prefix: '10.0.2.0/26' }
  { name: 'snet-shared', prefix: '10.0.10.0/24' }
]

resource hubVnet 'Microsoft.Network/virtualNetworks@2024-01-01' = {
  name: '${prefix}-vnet-hub-${environment}-${regionCode}'
  location: location
  tags: tags
  properties: {
    addressSpace: {
      addressPrefixes: [hubAddressSpace]
    }
    subnets: [for subnet in subnets: {
      name: subnet.name
      properties: {
        addressPrefix: subnet.prefix
        networkSecurityGroup: contains(subnet, 'nsgId') ? { id: subnet.nsgId } : null
        routeTable: contains(subnet, 'routeTableId') ? { id: subnet.routeTableId } : null
      }
    }]
  }
}

output hubVnetId string = hubVnet.id
output hubVnetName string = hubVnet.name
output subnetIds array = [for (subnet, i) in subnets: hubVnet.properties.subnets[i].id]
```

### 2. Spoke VNet with Peering

```bicep
param spokeAddressSpace string
param spokeName string
param hubVnetId string
param hubVnetName string
param hubResourceGroup string

resource spokeVnet 'Microsoft.Network/virtualNetworks@2024-01-01' = {
  name: '${prefix}-vnet-${spokeName}-${environment}-${regionCode}'
  location: location
  tags: tags
  properties: {
    addressSpace: {
      addressPrefixes: [spokeAddressSpace]
    }
  }
}

resource spokeToHub 'Microsoft.Network/virtualNetworks/virtualNetworkPeerings@2024-01-01' = {
  parent: spokeVnet
  name: 'peer-to-hub'
  properties: {
    remoteVirtualNetwork: { id: hubVnetId }
    allowVirtualNetworkAccess: true
    allowForwardedTraffic: true
    useRemoteGateways: true
  }
}

module hubToSpoke 'hub-to-spoke-peering.bicep' = {
  name: 'hub-to-${spokeName}-peering'
  scope: resourceGroup(hubResourceGroup)
  params: {
    hubVnetName: hubVnetName
    spokeVnetId: spokeVnet.id
    spokeName: spokeName
  }
}
```

### 3. Azure Firewall with Policy

```bicep
param firewallSku string = 'Standard'
param threatIntelMode string = 'Alert'

resource fwPolicy 'Microsoft.Network/firewallPolicies@2024-01-01' = {
  name: '${prefix}-fwpol-${environment}-${regionCode}'
  location: location
  tags: tags
  properties: {
    sku: { tier: firewallSku }
    threatIntelMode: threatIntelMode
    dnsSettings: {
      enableProxy: true
    }
  }
}

resource fwPublicIp 'Microsoft.Network/publicIPAddresses@2024-01-01' = {
  name: '${prefix}-pip-fw-${environment}-${regionCode}'
  location: location
  tags: tags
  sku: { name: 'Standard' }
  properties: {
    publicIPAllocationMethod: 'Static'
  }
}

resource firewall 'Microsoft.Network/azureFirewalls@2024-01-01' = {
  name: '${prefix}-fw-${environment}-${regionCode}'
  location: location
  tags: tags
  properties: {
    sku: {
      name: 'AZFW_VNet'
      tier: firewallSku
    }
    firewallPolicy: { id: fwPolicy.id }
    ipConfigurations: [
      {
        name: 'fw-ipconfig'
        properties: {
          subnet: { id: resourceId('Microsoft.Network/virtualNetworks/subnets', hubVnetName, 'AzureFirewallSubnet') }
          publicIPAddress: { id: fwPublicIp.id }
        }
      }
    ]
  }
}

output firewallPrivateIp string = firewall.properties.ipConfigurations[0].properties.privateIPAddress
```

### 4. VPN Gateway (S2S)

```bicep
param vpnGatewaySku string = 'VpnGw2'
param localGatewayIp string
param localAddressPrefixes array
@secure()
param sharedKey string

resource vpnGwPip 'Microsoft.Network/publicIPAddresses@2024-01-01' = {
  name: '${prefix}-pip-vpngw-${environment}-${regionCode}'
  location: location
  tags: tags
  sku: { name: 'Standard' }
  properties: { publicIPAllocationMethod: 'Static' }
}

resource vpnGateway 'Microsoft.Network/virtualNetworkGateways@2024-01-01' = {
  name: '${prefix}-vpngw-${environment}-${regionCode}'
  location: location
  tags: tags
  properties: {
    gatewayType: 'Vpn'
    vpnType: 'RouteBased'
    sku: { name: vpnGatewaySku, tier: vpnGatewaySku }
    ipConfigurations: [{
      name: 'default'
      properties: {
        subnet: { id: resourceId('Microsoft.Network/virtualNetworks/subnets', hubVnetName, 'GatewaySubnet') }
        publicIPAddress: { id: vpnGwPip.id }
      }
    }]
    enableBgp: true
    bgpSettings: {
      asn: 65515
    }
  }
}

resource localNetworkGateway 'Microsoft.Network/localNetworkGateways@2024-01-01' = {
  name: '${prefix}-lng-onprem-${environment}-${regionCode}'
  location: location
  tags: tags
  properties: {
    gatewayIpAddress: localGatewayIp
    localNetworkAddressSpace: {
      addressPrefixes: localAddressPrefixes
    }
  }
}

resource connection 'Microsoft.Network/connections@2024-01-01' = {
  name: '${prefix}-cn-onprem-${environment}-${regionCode}'
  location: location
  tags: tags
  properties: {
    connectionType: 'IPsec'
    virtualNetworkGateway1: { id: vpnGateway.id }
    localNetworkGateway2: { id: localNetworkGateway.id }
    sharedKey: sharedKey
    enableBgp: true
    ipsecPolicies: [{
      saLifeTimeSeconds: 27000
      saDataSizeKilobytes: 102400000
      ipsecEncryption: 'AES256'
      ipsecIntegrity: 'SHA256'
      ikeEncryption: 'AES256'
      ikeIntegrity: 'SHA256'
      dhGroup: 'DHGroup14'
      pfsGroup: 'PFS2048'
    }]
  }
}
```

### 5. Private Endpoint

```bicep
param targetResourceId string
param groupId string  // e.g., 'blob', 'sqlServer', 'vault'
param subnetId string
param privateDnsZoneId string

resource privateEndpoint 'Microsoft.Network/privateEndpoints@2024-01-01' = {
  name: '${prefix}-pe-${groupId}-${environment}-${regionCode}'
  location: location
  tags: tags
  properties: {
    subnet: { id: subnetId }
    privateLinkServiceConnections: [{
      name: 'plsc-${groupId}'
      properties: {
        privateLinkServiceId: targetResourceId
        groupIds: [groupId]
      }
    }]
  }
}

resource dnsZoneGroup 'Microsoft.Network/privateEndpoints/privateDnsZoneGroups@2024-01-01' = {
  parent: privateEndpoint
  name: 'default'
  properties: {
    privateDnsZoneConfigs: [{
      name: 'config-${groupId}'
      properties: {
        privateDnsZoneId: privateDnsZoneId
      }
    }]
  }
}
```

### 6. NSG with Common Rules

```bicep
param rules array = [
  {
    name: 'Allow-HTTPS-Inbound'
    priority: 100
    direction: 'Inbound'
    access: 'Allow'
    protocol: 'Tcp'
    sourceAddressPrefix: 'VirtualNetwork'
    destinationAddressPrefix: '*'
    destinationPortRange: '443'
  }
  {
    name: 'Deny-All-Inbound'
    priority: 4096
    direction: 'Inbound'
    access: 'Deny'
    protocol: '*'
    sourceAddressPrefix: '*'
    destinationAddressPrefix: '*'
    destinationPortRange: '*'
  }
]

resource nsg 'Microsoft.Network/networkSecurityGroups@2024-01-01' = {
  name: '${prefix}-nsg-${subnetPurpose}-${environment}-${regionCode}'
  location: location
  tags: tags
  properties: {
    securityRules: [for rule in rules: {
      name: rule.name
      properties: {
        priority: rule.priority
        direction: rule.direction
        access: rule.access
        protocol: rule.protocol
        sourceAddressPrefix: rule.sourceAddressPrefix
        sourcePortRange: '*'
        destinationAddressPrefix: rule.destinationAddressPrefix
        destinationPortRange: rule.destinationPortRange
      }
    }]
  }
}
```

### 7. Route Table with Force-Tunnel

```bicep
param firewallPrivateIp string
param disableBgpPropagation bool = true

resource routeTable 'Microsoft.Network/routeTables@2024-01-01' = {
  name: '${prefix}-rt-forced-${environment}-${regionCode}'
  location: location
  tags: tags
  properties: {
    disableBgpRoutePropagation: disableBgpPropagation
    routes: [
      {
        name: 'default-to-firewall'
        properties: {
          addressPrefix: '0.0.0.0/0'
          nextHopType: 'VirtualAppliance'
          nextHopIpAddress: firewallPrivateIp
        }
      }
    ]
  }
}

output routeTableId string = routeTable.id
```

---

## Module Structure Best Practices

```
modules/
├── vnet/
│   ├── main.bicep         // VNet resource
│   └── outputs.bicep      // Exported values
├── subnet/
│   ├── main.bicep         // Subnet (can be separate from VNet for updates)
├── nsg/
│   ├── main.bicep         // NSG with parameterized rules
├── firewall/
│   ├── main.bicep         // Azure Firewall + Policy
│   ├── rule-collection.bicep  // Reusable rule collections
├── vpn-gateway/
│   ├── main.bicep         // VPN GW + connection
├── private-endpoint/
│   ├── main.bicep         // PE + DNS zone group
└── route-table/
    ├── main.bicep         // UDR
```

---

## Deployment Patterns

### Environment-Specific Parameters (`.bicepparam`)

```bicep
using 'main.bicep'

param prefix = 'contoso'
param environment = 'prod'
param hubAddressSpace = '10.0.0.0/16'
param spokeAddressSpaces = [
  { name: 'workload-a', prefix: '10.1.0.0/16' }
  { name: 'workload-b', prefix: '10.2.0.0/16' }
]
param deployFirewall = true
param deployVpnGateway = true
```

### Conditional Deployments

```bicep
param deployFirewall bool = true
param deployVpnGateway bool = false

resource firewall 'Microsoft.Network/azureFirewalls@2024-01-01' = if (deployFirewall) {
  // ...
}
```

---

## Validation Commands

```bash
# Lint the template
az bicep lint --file main.bicep

# Build to ARM (syntax validation)
az bicep build --file main.bicep

# What-If deployment (preview changes)
az deployment group what-if \
  --resource-group rg-network-prod \
  --template-file main.bicep \
  --parameters main.bicepparam

# Deploy
az deployment group create \
  --resource-group rg-network-prod \
  --template-file main.bicep \
  --parameters main.bicepparam \
  --confirm-with-what-if
```

**Analysis only — verify against vendor documentation before applying.**

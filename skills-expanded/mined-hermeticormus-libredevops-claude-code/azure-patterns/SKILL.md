---
name: azure-patterns
description: "Azure infrastructure patterns: Bicep module structure, AKS Workload Identity, App Service with Key Vault references, Azure DevOps pipelines, private endpoints for PaaS services, and management group policies that enforce tagging. Use when writing Bicep or setting up Azure identity, networking, or governance."
---

# Azure Patterns

Production Azure infrastructure patterns with Bicep, AKS Workload Identity, Azure DevOps pipelines, and governance.

## Bicep Module Structure

```
infra/
├── main.bicep                     # Root template, orchestrates modules
├── main.bicepparam                # Parameter file (replaces ARM parameters)
├── modules/
│   ├── network/
│   │   ├── vnet.bicep
│   │   └── nsg.bicep
│   ├── compute/
│   │   ├── aks.bicep
│   │   └── appservice.bicep
│   ├── data/
│   │   ├── sql.bicep
│   │   └── cosmos.bicep
│   └── security/
│       ├── keyvault.bicep
│       └── defender.bicep
└── environments/
    ├── dev.bicepparam
    └── prod.bicepparam
```

```bicep
// main.bicep - Root orchestration
targetScope = 'subscription'

param environment string
param location string = 'eastus2'

// Resource group
resource rg 'Microsoft.Resources/resourceGroups@2023-07-01' = {
  name: 'rg-${environment}-app'
  location: location
  tags: { Environment: environment, ManagedBy: 'bicep' }
}

// Network module
module network 'modules/network/vnet.bicep' = {
  name: 'network'
  scope: rg
  params: {
    vnetName: 'vnet-${environment}'
    addressPrefixes: ['10.0.0.0/16']
    subnets: [
      { name: 'aks',   addressPrefix: '10.0.1.0/24' }
      { name: 'appgw', addressPrefix: '10.0.2.0/24' }
      { name: 'data',  addressPrefix: '10.0.3.0/28' }
    ]
  }
}

// AKS module depends on network
module aks 'modules/compute/aks.bicep' = {
  name: 'aks'
  scope: rg
  dependsOn: [network]
  params: {
    aksName: 'aks-${environment}'
    subnetId: network.outputs.subnetIds.aks
  }
}
```

## AKS Workload Identity (No Secrets in Pods)

```bicep
// 1. Enable OIDC + Workload Identity on AKS
resource aks 'Microsoft.ContainerService/managedClusters@2023-10-01' = {
  name: aksName
  location: location
  identity: { type: 'SystemAssigned' }
  properties: {
    oidcIssuerProfile: { enabled: true }
    securityProfile: {
      workloadIdentity: { enabled: true }
    }
    // Azure CNI Overlay for proper pod networking
    networkProfile: {
      networkPlugin: 'azure'
      networkPluginMode: 'overlay'
      serviceCidr: '172.16.0.0/16'
      dnsServiceIP: '172.16.0.10'
    }
  }
}

// 2. User-assigned managed identity for the app
resource identity 'Microsoft.ManagedIdentity/userAssignedIdentities@2023-01-31' = {
  name: 'id-myapp-${environment}'
  location: location
}

// 3. Grant identity Key Vault Secrets User role
resource kvSecretsRole 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(keyVault.id, identity.id, '4633458b-17de-408a-b874-0445c86b69e6')
  scope: keyVault
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', '4633458b-17de-408a-b874-0445c86b69e6')
    principalId: identity.properties.principalId
    principalType: 'ServicePrincipal'
  }
}

// 4. Federated credential: trust specific K8s ServiceAccount
resource federatedCredential 'Microsoft.ManagedIdentity/userAssignedIdentities/federatedIdentityCredentials@2023-01-31' = {
  parent: identity
  name: 'myapp-k8s-fedcred'
  properties: {
    issuer: aks.properties.oidcIssuerProfile.issuerURL
    subject: 'system:serviceaccount:myapp:myapp-sa'
    audiences: ['api://AzureADTokenExchange']
  }
}
```

```yaml
# Kubernetes side: annotate ServiceAccount
apiVersion: v1
kind: ServiceAccount
metadata:
  name: myapp-sa
  namespace: myapp
  annotations:
    azure.workload.identity/client-id: "<managed-identity-client-id>"
---
# Pod with workload identity label
apiVersion: apps/v1
kind: Deployment
spec:
  template:
    metadata:
      labels:
        azure.workload.identity/use: "true"
    spec:
      serviceAccountName: myapp-sa
      containers:
        - name: app
          image: myapp:latest
          # SDK uses DefaultAzureCredential -- no secrets in environment
```

## App Service with Key Vault References

```bicep
resource appService 'Microsoft.Web/sites@2023-01-01' = {
  name: appName
  location: location
  identity: { type: 'SystemAssigned' }
  properties: {
    serverFarmId: plan.id
    httpsOnly: true
    siteConfig: {
      appSettings: [
        {
          name: 'DATABASE_URL'
          // Key Vault reference -- secret never touches App Service config plane
          value: '@Microsoft.KeyVault(SecretUri=https://${kvName}.vault.azure.net/secrets/db-url/)'
        }
        {
          name: 'APPLICATIONINSIGHTS_CONNECTION_STRING'
          value: appInsights.properties.ConnectionString
        }
      ]
      linuxFxVersion: 'NODE|20-lts'
      alwaysOn: true
      healthCheckPath: '/health'
    }
  }
}

// Grant App Service identity access to read Key Vault secrets
resource kvAccess 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(kv.id, appService.id, '4633458b-17de-408a-b874-0445c86b69e6')
  scope: kv
  properties: {
    roleDefinitionId: subscriptionResourceId(
      'Microsoft.Authorization/roleDefinitions',
      '4633458b-17de-408a-b874-0445c86b69e6'  // Key Vault Secrets User
    )
    principalId: appService.identity.principalId
    principalType: 'ServicePrincipal'
  }
}
```

## Azure DevOps Pipeline Pattern

```yaml
# azure-pipelines.yml
variables:
  - group: myapp-prod-kv       # Variable group linked to Key Vault
  - name: acrName
    value: myacr.azurecr.io

stages:
  - stage: Build
    jobs:
      - job: BuildContainer
        pool: { vmImage: ubuntu-latest }
        steps:
          - task: AzureCLI@2
            displayName: Build and push to ACR
            inputs:
              azureSubscription: azure-service-connection
              scriptType: bash
              inlineScript: |
                az acr build \
                  --registry $(acrName) \
                  --image myapp:$(Build.BuildId) \
                  --image myapp:latest \
                  .

  - stage: DeployProd
    dependsOn: Build
    condition: and(succeeded(), eq(variables['Build.SourceBranch'], 'refs/heads/main'))
    jobs:
      - deployment: Deploy
        environment: production     # Gates and approvals configured in UI
        strategy:
          runOnce:
            deploy:
              steps:
                - task: AzureCLI@2
                  inputs:
                    azureSubscription: azure-service-connection
                    scriptType: bash
                    inlineScript: |
                      az aks get-credentials -g rg-prod -n aks-prod
                      kubectl set image deployment/myapp \
                        app=$(acrName)/myapp:$(Build.BuildId) -n myapp
                      kubectl rollout status deployment/myapp -n myapp
```

## Private Endpoint for PaaS Services

```bicep
// Azure SQL accessible only via private IP in VNet
resource sqlPE 'Microsoft.Network/privateEndpoints@2023-05-01' = {
  name: 'pe-${sqlServerName}'
  location: location
  properties: {
    subnet: { id: dataSubnetId }
    privateLinkServiceConnections: [
      {
        name: 'sql-connection'
        properties: {
          privateLinkServiceId: sqlServer.id
          groupIds: ['sqlServer']
        }
      }
    ]
  }
}

// Private DNS Zone for name resolution
resource sqlDnsZone 'Microsoft.Network/privateDnsZones@2020-06-01' = {
  name: 'privatelink.database.windows.net'
  location: 'global'
}

resource dnsZoneGroup 'Microsoft.Network/privateEndpoints/privateDnsZoneGroups@2023-05-01' = {
  parent: sqlPE
  name: 'sql-dns-group'
  properties: {
    privateDnsZoneConfigs: [
      {
        name: 'sql-config'
        properties: { privateDnsZoneId: sqlDnsZone.id }
      }
    ]
  }
}
```

## Management Group Policy: Enforce Tagging

```bicep
// Deny resources without Environment tag at Landing Zones scope
resource tagPolicy 'Microsoft.Authorization/policyAssignments@2023-04-01' = {
  name: 'require-environment-tag'
  scope: managementGroup('landing-zones')
  identity: { type: 'SystemAssigned' }
  location: location
  properties: {
    policyDefinitionId: tenantResourceId(
      'Microsoft.Authorization/policyDefinitions',
      '96670d01-0a4d-4649-9c89-2d3abc0a5025'  // Require a tag on resources
    )
    parameters: {
      tagName: { value: 'Environment' }
    }
    enforcementMode: 'Default'
  }
}
```

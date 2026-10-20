---
name: azure-deployment
description: Azure deployment patterns — App Service, Azure Functions, SQL Database, Cosmos DB, Application Insights, and managed services
globs: ["**/*.ts", "**/*.js", "**/*.cs", "**/*.yaml", "**/*.yml", "**/*.json", "**/*.bicep"]
alwaysApply: false
---

# Azure Deployment Patterns

Azure provides comprehensive cloud services for .NET, Node.js, and Python applications. Master App Service, Functions, databases, and monitoring.

---

## Azure App Service

**ALWAYS**:
- Use App Service Plan for consistent pricing and scaling
- Enable Health Check for automatic instance removal when unhealthy
- Use Deployment Slots (staging, production) for blue-green deployments
- Configure auto-scaling based on CPU or request count
- Enable HTTPS only (disable HTTP)
- Use Managed Identity for Azure service authentication
- Monitor: CPU, memory, request count, response time via Application Insights

**NEVER**:
- Deploy to Consumption Plan for unpredictable workloads (use Premium or App Service Plan)
- Skip SSL/TLS (allow unencrypted HTTP)
- Use App Service plan for one-time jobs (use Azure Functions instead)
- Ignore auto-scaling configuration

### ✅ GOOD App Service Setup

```bicep
// Bicep: App Service deployment
resource appServicePlan 'Microsoft.Web/serverfarms@2022-03-01' = {
  name: 'asp-production'
  location: resourceGroup().location
  sku: {
    name: 'P1v2'  // Premium tier for production
    capacity: 3   // 3 instances
  }
  properties: {
    reserved: true  // Linux
  }
}

resource webApp 'Microsoft.Web/sites@2022-03-01' = {
  name: 'app-production'
  location: resourceGroup().location
  identity: {
    type: 'SystemAssigned'  // Managed Identity
  }
  properties: {
    serverFarmId: appServicePlan.id
    httpsOnly: true  // HTTPS only
  }
}

// Health check — remove unhealthy instances
resource healthCheck 'Microsoft.Web/sites/config@2022-03-01' = {
  name: '${webApp.name}/web'
  properties: {
    healthCheckPath: '/health'  // Must return 200 OK
  }
}

// Auto-scaling
resource autoScale 'Microsoft.Insights/autoscalesettings@2021-05-01-preview' = {
  name: 'as-${webApp.name}'
  location: resourceGroup().location
  properties: {
    enabled: true
    targetResourceUri: appServicePlan.id
    profiles: [
      {
        name: 'Auto scale based on CPU'
        capacity: {
          minimum: '2'
          maximum: '10'
          default: '3'
        }
        rules: [
          {
            metricTrigger: {
              metricName: 'CpuPercentage'
              metricResourceId: appServicePlan.id
              operator: 'GreaterThan'
              statistic: 'Average'
              threshold: 70
              timeAggregation: 'Average'
              timeWindow: 'PT5M'
            }
            scaleAction: {
              direction: 'Increase'
              type: 'ChangeCount'
              value: '1'
              cooldown: 'PT5M'
            }
          }
        ]
      }
    ]
  }
}

// Deployment slot (staging)
resource stagingSlot 'Microsoft.Web/sites/slots@2022-03-01' = {
  name: '${webApp.name}/staging'
  location: resourceGroup().location
  properties: {
    serverFarmId: appServicePlan.id
  }
}

// Swap production ← staging
resource slotSwap 'Microsoft.Web/sites/slots/slotsswap@2022-03-01' = {
  name: '${stagingSlot.name}/swap'
  properties: {
    targetSlot: 'production'
  }
}
```

---

## Azure Functions

**ALWAYS**:
- Use Consumption Plan for event-driven workloads (pay per execution)
- Use Premium Plan for predictable workloads or VPC access
- Set appropriate timeout (5 min default, max 10 min)
- Use Managed Identity for authentication
- Implement retries for unreliable operations (built-in support)
- Monitor: execution count, failures, duration via Application Insights
- Use durable functions for long-running operations (> 5 min)

**NEVER**:
- Use Consumption Plan for consistent high throughput (cold starts)
- Store connection strings in code (use Key Vault)
- Create resources inside function (use singleton pattern)

### ✅ GOOD Azure Functions Setup

```csharp
// C# Azure Function
using Azure.Data.Tables;
using Azure.Identity;
using Microsoft.Azure.WebJobs;
using Microsoft.Extensions.Logging;
using System.Threading.Tasks;

public static class GetUserFunction
{
    [FunctionName("GetUser")]
    public static async Task<IActionResult> Run(
        [HttpTrigger(AuthorizationLevel.Anonymous, "get", Route = "users/{id}")] HttpRequest req,
        string id,
        [Table("Users")] TableClient tableClient,
        ILogger log)
    {
        try
        {
            log.LogInformation($"GetUser called for id: {id}");

            // Query table
            var entity = await tableClient.GetEntityAsync<UserEntity>("USER", id);

            return new OkObjectResult(entity);
        }
        catch (Azure.RequestFailedException ex) when (ex.Status == 404)
        {
            log.LogWarning($"User {id} not found");
            return new NotFoundResult();
        }
        catch (Exception ex)
        {
            log.LogError($"Error: {ex.Message}");
            return new StatusCodeResult(500);
        }
    }
}

public class UserEntity : ITableEntity
{
    public string PartitionKey { get; set; }
    public string RowKey { get; set; }
    public string Id { get; set; }
    public string Email { get; set; }
    public DateTimeOffset? Timestamp { get; set; }
    public Azure.ETag ETag { get; set; }
}
```

---

## Azure SQL Database

**ALWAYS**:
- Use Elastic Pools for multiple databases (cost savings)
- Enable Transparent Data Encryption (TDE) at rest
- Use Always Encrypted for sensitive columns
- Enable auditing for compliance
- Set up automated backups (7-35 days retention)
- Use connection pooling (ADO.NET connection pooling)
- Monitor: CPU, storage, DTU usage via Azure Monitor

**NEVER**:
- Store connection strings in code (use Key Vault or Managed Identity)
- Disable encryption
- Use single-database for multiple applications (use Elastic Pool)

### ✅ GOOD SQL Database Setup

```bicep
// Bicep: Azure SQL Database
resource sqlServer 'Microsoft.Sql/servers@2021-11-01' = {
  name: 'sql-production'
  location: resourceGroup().location
  properties: {
    administratorLogin: sqlAdmin
    administratorLoginPassword: sqlPassword
  }
}

resource database 'Microsoft.Sql/servers/databases@2021-11-01' = {
  name: '${sqlServer.name}/appdb'
  location: resourceGroup().location
  sku: {
    name: 'S2'  // Standard tier
  }
  properties: {
    collation: 'SQL_Latin1_General_CP1_CI_AS'
    // Automated backups: 7 days
    backupShortTermRetentionDays: 7
  }
}

// Transparent Data Encryption (TDE)
resource tde 'Microsoft.Sql/servers/databases/transparentDataEncryption@2021-11-01' = {
  name: '${database.name}/current'
  properties: {
    state: 'Enabled'
  }
}

// Firewall rule: Azure services only
resource firewall 'Microsoft.Sql/servers/firewallRules@2021-11-01' = {
  name: '${sqlServer.name}/AllowAzureServices'
  properties: {
    startIpAddress: '0.0.0.0'
    endIpAddress: '0.0.0.0'
  }
}

// Auditing
resource audit 'Microsoft.Sql/servers/auditingSettings@2021-11-01' = {
  name: '${sqlServer.name}/default'
  properties: {
    state: 'Enabled'
    storageEndpoint: storageAccount.properties.primaryEndpoints.blob
    storageAccountAccessKey: storageAccountKey
    retentionDays: 90
  }
}
```

---

## Azure Cosmos DB (NoSQL)

**ALWAYS**:
- Use provisioned throughput with auto-scaling for predictable workloads
- Use serverless for unpredictable, bursty workloads
- Set TTL for time-limited data (automatic cleanup)
- Use change feed for event processing
- Enable global distribution for low-latency reads
- Set backup retention (1-35 days)
- Monitor: RU (Request Unit) consumption, latency

**NEVER**:
- Provision excessive RUs (costs multiply)
- Skip partition key design (causes hot partitions)
- Use Cosmos for relational data (use SQL Database instead)

### ✅ GOOD Cosmos DB Setup

```bicep
// Bicep: Cosmos DB account
resource cosmosAccount 'Microsoft.DocumentDB/databaseAccounts@2021-12-15' = {
  name: 'cosmos-production'
  location: resourceGroup().location
  properties: {
    createMode: 'Default'
    databaseAccountOfferType: 'Standard'
    // Global distribution
    locations: [
      {
        locationName: 'East US'
        failoverPriority: 0
      }
      {
        locationName: 'West US'
        failoverPriority: 1
      }
    ]
    enableAutomaticFailover: true
    enableMultipleWriteLocations: true
  }
}

// Database
resource database 'Microsoft.DocumentDB/databaseAccounts/sqlDatabases@2021-12-15' = {
  name: '${cosmosAccount.name}/appdb'
  properties: {
    resource: {
      id: 'appdb'
    }
  }
}

// Container (collection)
resource container 'Microsoft.DocumentDB/databaseAccounts/sqlDatabases/containers@2021-12-15' = {
  name: '${database.name}/users'
  properties: {
    resource: {
      id: 'users'
      partitionKey: {
        paths: ['/userId']  // Partition key for scaling
        kind: 'Hash'
      }
      // Auto-scaling: 4,000–40,000 RU/s
      autoscaleSettings: {
        maxThroughput: 40000
      }
      // TTL: delete docs after 30 days
      defaultTtl: 2592000
      // Indexing: all paths
      indexingPolicy: {
        indexingMode: 'Consistent'
        includedPaths: [
          {
            path: '/*'
          }
        ]
      }
    }
  }
}
```

---

## Application Insights (Monitoring)

**ALWAYS**:
- Enable Application Insights on all production workloads
- Track custom metrics and events (business KPIs)
- Set up alerts for errors, performance degradation
- Use dependency tracking (database, API calls)
- Track user sessions and flows
- Log structured data (JSON, not text)
- Set retention (30-730 days based on needs)

**NEVER**:
- Log sensitive data (passwords, tokens, PII)
- Ignore alerts (configure thresholds)
- Skip correlation IDs (makes debugging hard)

### ✅ GOOD Application Insights Setup

```csharp
// C# integration
using Microsoft.ApplicationInsights;
using Microsoft.ApplicationInsights.DataContracts;

public class GetUserFunction
{
    private readonly TelemetryClient _telemetryClient;

    public GetUserFunction(TelemetryClient telemetryClient)
    {
        _telemetryClient = telemetryClient;
    }

    public async Task<IActionResult> Run(
        [HttpTrigger(AuthorizationLevel.Anonymous, "get", Route = "users/{id}")] HttpRequest req,
        string id)
    {
        using (var operation = _telemetryClient.StartOperation<RequestTelemetry>("GetUser"))
        {
            operation.Telemetry.Properties["userId"] = id;

            try
            {
                var user = await GetUserFromDatabase(id);
                
                // Track custom event
                _telemetryClient.TrackEvent("UserRetrieved", new Dictionary<string, string>
                {
                    { "userId", id },
                    { "email", user.Email }
                });

                return new OkObjectResult(user);
            }
            catch (Exception ex)
            {
                _telemetryClient.TrackException(ex);
                throw;
            }
        }
    }
}
```

---

## Azure Key Vault

**ALWAYS**:
- Store all secrets in Key Vault (connection strings, API keys, passwords)
- Use Managed Identity to access Key Vault (no credentials needed)
- Enable soft delete (recover accidentally deleted secrets)
- Set access policies (principle of least privilege)
- Audit access via diagnostic settings
- Rotate secrets regularly (90 days recommended)

**NEVER**:
- Store secrets in code or config files
- Share Key Vault across unrelated applications
- Disable access logging

### ✅ GOOD Key Vault Setup

```bicep
// Bicep: Key Vault
resource keyVault 'Microsoft.KeyVault/vaults@2021-11-01-preview' = {
  name: 'kv-production'
  location: resourceGroup().location
  properties: {
    enabledForDeployment: true
    enabledForTemplateDeployment: true
    enabledForDiskEncryption: false
    tenantId: subscription().tenantId
    sku: {
      family: 'A'
      name: 'standard'
    }
    accessPolicies: []
    softDeleteRetentionInDays: 90  // Soft delete
    networkAcls: {
      defaultAction: 'Deny'
      bypass: 'AzureServices'
    }
  }
}

// Grant App Service access via Managed Identity
resource accessPolicy 'Microsoft.KeyVault/vaults/accessPolicies@2021-11-01-preview' = {
  name: '${keyVault.name}/add'
  properties: {
    accessPolicies: [
      {
        tenantId: subscription().tenantId
        objectId: webApp.identity.principalId  // App Service Managed Identity
        permissions: {
          secrets: [
            'get'
            'list'
          ]
        }
      }
    ]
  }
}

// Store secret
resource dbPassword 'Microsoft.KeyVault/vaults/secrets@2021-11-01-preview' = {
  name: '${keyVault.name}/db-password'
  properties: {
    value: sqlPassword
  }
}
```

---

## Azure Security Checklist

- [ ] App Service: HTTPS only, health check, auto-scaling, Managed Identity
- [ ] Azure Functions: Appropriate plan, Managed Identity, timeout configured
- [ ] SQL Database: TDE enabled, always encrypted for sensitive data, automated backups
- [ ] Cosmos DB: TTL configured, partition key designed, auto-scaling
- [ ] Key Vault: All secrets stored, Managed Identity access, soft delete enabled
- [ ] Application Insights: Enabled, custom metrics tracked, alerts configured
- [ ] Storage Account: Encryption enabled, public access blocked, lifecycle policies
- [ ] Virtual Network: Private subnets for databases, NSGs for access control
- [ ] Azure AD: MFA enabled for console, RBAC for least privilege
- [ ] Monitoring: Alerts for errors, performance, security events

---

## Summary

Good Azure architecture:
1. **Managed services first** — App Service, Functions, SQL Database, Cosmos DB
2. **Identity-based** — Managed Identity, no credentials in code, Key Vault
3. **Monitored** — Application Insights on everything, alerts configured
4. **Resilient** — Automated backups, geo-replication, health checks
5. **Secure** — HTTPS only, encryption at rest, auditing enabled
6. **Scalable** — Auto-scaling based on demand, elastic pools, serverless options

Master these patterns for production Azure deployments.

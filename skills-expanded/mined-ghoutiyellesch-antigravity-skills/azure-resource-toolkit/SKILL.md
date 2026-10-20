---
name: azure-resource-toolkit
description: Consolidated toolkit for azure-resource. Covers azure-resource-manager-playwright-dotnet, azure-resource-manager-durabletask-dotnet, azure-resource-manager-postgresql-dotnet, azure-resource-manager-mysql-dotnet, azure-resource-manager-redis-dotnet, azure-resource-manager-sql-dotnet
---
# Azure Resource Toolkit

## Core Capabilities
# Azure Resource Toolkit

# Azure.ResourceManager.Playwright (.NET)

Management plane SDK for provisioning and managing Microsoft Playwright Testing workspaces via Azure Resource Manager.

> **⚠️ Management vs Test Execution**
> - **This SDK (Azure.ResourceManager.Playwright)**: Create workspaces, manage quotas, check name availability
> - **Test Execution SDK (Azure.Developer.MicrosoftPlaywrightTesting.NUnit)**: Run Playwright tests at scale on cloud browsers

## Installation

```bash
dotnet add package Azure.ResourceManager.Playwright
dotnet add package Azure.Identity
```

**Current Versions**: Stable v1.0.0, Preview v1.0.0-beta.1

## Environment Variables

```bash
AZURE_SUBSCRIPTION_ID=<your-subscription-id>
# For service principal auth (optional)
AZURE_TENANT_ID=<tenant-id>
AZURE_CLIENT_ID=<client-id>
AZURE_CLIENT_SECRET=<client-secret>
```

## Authentication

```csharp
using Azure.Identity;
using Azure.ResourceManager;
using Azure.ResourceManager.Playwright;

// Always use DefaultAzureCredential
var credential = new DefaultAzureCredential();
var armClient = new ArmClient(credential);

// Get subscription
var subscriptionId = Environment.GetEnvironmentVariable("AZURE_SUBSCRIPTION_ID");
var subscription = armClient.GetSubscriptionResource(
    new ResourceIdentifier($"/subscriptions/{subscriptionId}"));
```

## Resource Hierarchy

```
ArmClient
└── SubscriptionResource
    ├── PlaywrightQuotaResource (subscription-level quotas)
    └── ResourceGroupResource
        └── PlaywrightWorkspaceResource
            └── PlaywrightWorkspaceQuotaResource (workspace-level quotas)
```

## Core Workflow

### 1. Create Playwright Workspace

```csharp
using Azure.ResourceManager.Playwright;
using Azure.ResourceManager.Playwright.Models;

// Get resource group
var resourceGroup = await subscription
    .GetResourceGroupAsync("my-resource-group");

// Define workspace
var workspaceData = new PlaywrightWorkspaceData(AzureLocation.WestUS3)
{
    // Optional: Configure regional affinity and local auth
    RegionalAffinity = PlaywrightRegionalAffinity.Enabled,
    LocalAuth = PlaywrightLocalAuth.Enabled,
    Tags =
    {
        ["Team"] = "Dev Exp",
        ["Environment"] = "Production"
    }
};

// Create workspace (long-running operation)
var workspaceCollection = resourceGroup.Value.GetPlaywrightWorkspaces();
var operation = await workspaceCollection.CreateOrUpdateAsync(
    WaitUntil.Completed,
    "my-playwright-workspace",
    workspaceData);

PlaywrightWorkspaceResource workspace = operation.Value;

// Get the data plane URI for running tests
Console.WriteLine($"Data Plane URI: {workspace.Data.DataplaneUri}");
Console.WriteLine($"Workspace ID: {workspace.Data.WorkspaceId}");
```

### 2. Get Existing Workspace

```csharp
// Get by name
var workspace = await workspaceCollection.GetAsync("my-playwright-workspace");

// Or check if exists first
bool exists = await workspaceCollection.ExistsAsync("my-playwright-workspace");
if (exists)
{
    var existingWorkspace = await workspaceCollection.GetAsync("my-playwright-workspace");
    Console.WriteLine($"Workspace found: {existingWorkspace.Value.Data.Name}");
}
```

### 3. List Workspaces

```csharp
// List in resource group
await foreach (var workspace in workspaceCollection.GetAllAsync())
{
    Console.WriteLine($"Workspace: {workspace.Data.Name}");
    Console.WriteLine($"  Location: {workspace.Data.Location}");
    Console.WriteLine($"  State: {workspace.Data.ProvisioningState}");
    Console.WriteLine($"  Data Plane URI: {workspace.Data.DataplaneUri}");
}

// List across subscription
await foreach (var workspace in subscription.GetPlaywrightWorkspacesAsync())
{
    Console.WriteLine($"Workspace: {workspace.Data.Name}");
}
```

### 4. Update Workspace

```csharp
var patch = new PlaywrightWorkspacePatch
{
    Tags =
    {
        ["Team"] = "Dev Exp",
        ["Environment"] = "Staging",
        ["UpdatedAt"] = DateTime.UtcNow.ToString("o")
    }
};

var updatedWorkspace = await workspace.Value.UpdateAsync(patch);
```

### 5. Check Name Availability

```csharp
using Azure.ResourceManager.Playwright.Models;

var checkRequest = new PlaywrightCheckNameAvailabilityContent
{
    Name = "my-new-workspace",
    ResourceType = "Microsoft.LoadTestService/playwrightWorkspaces"
};

var result = await subscription.CheckPlaywrightNameAvailabilityAsync(checkRequest);

if (result.Value.IsNameAvailable == true)
{
    Console.WriteLine("Name is available!");
}
else
{
    Console.WriteLine($"Name unavailable: {result.Value.Message}");
    Console.WriteLine($"Reason: {result.Value.Reason}");
}
```

### 6. Get Quota Information

```csharp
// Subscription-level quotas
await foreach (var quota in subscription.GetPlaywrightQuotasAsync(AzureLocation.WestUS3))
{
    Console.WriteLine($"Quota: {quota.Data.Name}");
    Console.WriteLine($"  Limit: {quota.Data.Limit}");
    Console.WriteLine($"  Used: {quota.Data.Used}");
}

// Workspace-level quotas
var workspaceQuotas = workspace.Value.GetAllPlaywrightWorkspaceQuota();
await foreach (var quota in workspaceQuotas.GetAllAsync())
{
    Console.WriteLine($"Workspace Quota: {quota.Data.Name}");
}
```

### 7. Delete Workspace

```csharp
// Delete (long-running operation)
await workspace.Value.DeleteAsync(WaitUntil.Completed);
```

## Key Types Reference

| Type | Purpose |
|------|---------|
| `ArmClient` | Entry point for all ARM operations |
| `PlaywrightWorkspaceResource` | Represents a Playwright Testing workspace |
| `PlaywrightWorkspaceCollection` | Collection for workspace CRUD |
| `PlaywrightWorkspaceData` | Workspace creation/response payload |
| `PlaywrightWorkspacePatch` | Workspace update payload |
| `PlaywrightQuotaResource` | Subscription-level quota information |
| `PlaywrightWorkspaceQuotaResource` | Workspace-level quota information |
| `PlaywrightExtensions` | Extension methods for ARM resources |
| `PlaywrightCheckNameAvailabilityContent` | Name availability check request |

## Workspace Properties

| Property | Description |
|----------|-------------|
| `DataplaneUri` | URI for running tests (e.g., `https://api.dataplane.{guid}.domain.com`) |
| `WorkspaceId` | Unique workspace identifier (GUID) |
| `RegionalAffinity` | Enable/disable regional affinity for test execution |
| `LocalAuth` | Enable/disable local authentication (access tokens) |
| `ProvisioningState` | Current provisioning state (Succeeded, Failed, etc.) |

## Best Practices

1. **Use `WaitUntil.Completed`** for operations that must finish before proceeding
2. **Use `WaitUntil.Started`** when you want to poll manually or run operations in parallel
3. **Always use `DefaultAzureCredential`** — never hardcode keys
4. **Handle `RequestFailedException`** for ARM API errors
5. **Use `CreateOrUpdateAsync`** for idempotent operations
6. **Navigate hierarchy** via `Get*` methods (e.g., `resourceGroup.GetPlaywrightWorkspaces()`)
7. **Store the DataplaneUri** after workspace creation for test execution configuration

## Error Handling

```csharp
using Azure;

try
{
    var operation = await workspaceCollection.CreateOrUpdateAsync(
        WaitUntil.Completed, workspaceName, workspaceData);
}
catch (RequestFailedException ex) when (ex.Status == 409)
{
    Console.WriteLine("Workspace already exists");
}
catch (RequestFailedException ex) when (ex.Status == 400)
{
    Console.WriteLine($"Bad request: {ex.Message}");
}
catch (RequestFailedException ex)
{
    Console.WriteLine($"ARM Error: {ex.Status} - {ex.ErrorCode}: {ex.Message}");
}
```

## Integration with Test Execution

After creating a workspace, use the `DataplaneUri` to configure your Playwright tests:

```csharp
// 1. Create workspace (this SDK)
var workspace = await workspaceCollection.CreateOrUpdateAsync(
    WaitUntil.Completed, "my-workspace", workspaceData);

// 2. Get the service URL
var serviceUrl = workspace.Value.Data.DataplaneUri;

// 3. Set environment variable for test execution
Environment.SetEnvironmentVariable("PLAYWRIGHT_SERVICE_URL", serviceUrl.ToString());

// 4. Run tests using Azure.Developer.MicrosoftPlaywrightTesting.NUnit
// (separate package for test execution)
```

## Related SDKs

| SDK | Purpose | Install |
|-----|---------|---------|
| `Azure.ResourceManager.Playwright` | Management plane (this SDK) | `dotnet add package Azure.ResourceManager.Playwright` |
| `Azure.Developer.MicrosoftPlaywrightTesting.NUnit` | Run NUnit Playwright tests at scale | `dotnet add package Azure.Developer.MicrosoftPlaywrightTesting.NUnit --prerelease` |
| `Azure.Developer.Playwright` | Playwright client library | `dotnet add package Azure.Developer.Playwright` |

## API Information

- **Resource Provider**: `Microsoft.LoadTestService`
- **Default API Version**: `2025-09-01`
- **Resource Type**: `Microsoft.LoadTestService/playwrightWorkspaces`

## Documentation Links

- [Azure.ResourceManager.Playwright API Reference](https://learn.microsoft.com/en-us/dotnet/api/azure.resourcemanager.playwright)
- [Microsoft Playwright Testing Overview](https://learn.microsoft.com/en-us/azure/playwright-testing/overview-what-is-microsoft-playwright-testing)
- [Quickstart: Run Playwright Tests at Scale](https://learn.microsoft.com/en-us/azure/playwright-testing/quickstart-run-end-to-end-tests)

## When to Use
This skill is applicable to execute the workflow or actions described in the overview.

---

# Azure.ResourceManager.DurableTask (.NET)

Management plane SDK for provisioning and managing Azure Durable Task Scheduler resources via Azure Resource Manager.

> **⚠️ Management vs Data Plane**
> - **This SDK (Azure.ResourceManager.DurableTask)**: Create schedulers, task hubs, configure retention policies
> - **Data Plane SDK (Microsoft.DurableTask.Client.AzureManaged)**: Start orchestrations, query instances, send events

## Installation

```bash
dotnet add package Azure.ResourceManager.DurableTask
dotnet add package Azure.Identity
```

**Current Versions**: Stable v1.0.0 (2025-11-03), Preview v1.0.0-beta.1 (2025-04-24)
**API Version**: 2025-11-01

## Environment Variables

```bash
AZURE_SUBSCRIPTION_ID=<your-subscription-id>
AZURE_RESOURCE_GROUP=<your-resource-group>
# For service principal auth (optional)
AZURE_TENANT_ID=<tenant-id>
AZURE_CLIENT_ID=<client-id>
AZURE_CLIENT_SECRET=<client-secret>
```

## Authentication

```csharp
using Azure.Identity;
using Azure.ResourceManager;
using Azure.ResourceManager.DurableTask;

// Always use DefaultAzureCredential
var credential = new DefaultAzureCredential();
var armClient = new ArmClient(credential);

// Get subscription
var subscriptionId = Environment.GetEnvironmentVariable("AZURE_SUBSCRIPTION_ID");
var subscription = armClient.GetSubscriptionResource(
    new ResourceIdentifier($"/subscriptions/{subscriptionId}"));
```

## Resource Hierarchy

```
ArmClient
└── SubscriptionResource
    └── ResourceGroupResource
        └── DurableTaskSchedulerResource
            ├── DurableTaskHubResource
            └── DurableTaskRetentionPolicyResource
```

## Core Workflow

### 1. Create Durable Task Scheduler

```csharp
using Azure.ResourceManager.DurableTask;
using Azure.ResourceManager.DurableTask.Models;

// Get resource group
var resourceGroup = await subscription
    .GetResourceGroupAsync("my-resource-group");

// Define scheduler with Dedicated SKU
var schedulerData = new DurableTaskSchedulerData(AzureLocation.EastUS)
{
    Properties = new DurableTaskSchedulerProperties
    {
        Sku = new DurableTaskSchedulerSku(DurableTaskSchedulerSkuName.Dedicated)
        {
            Capacity = 1  // Number of instances
        },
        // Optional: IP allowlist for network security
        IPAllowlist = { "10.0.0.0/24", "192.168.1.0/24" }
    }
};

// Create scheduler (long-running operation)
var schedulerCollection = resourceGroup.Value.GetDurableTaskSchedulers();
var operation = await schedulerCollection.CreateOrUpdateAsync(
    WaitUntil.Completed,
    "my-scheduler",
    schedulerData);

DurableTaskSchedulerResource scheduler = operation.Value;
Console.WriteLine($"Scheduler created: {scheduler.Data.Name}");
Console.WriteLine($"Endpoint: {scheduler.Data.Properties.Endpoint}");
```

### 2. Create Scheduler with Consumption SKU

```csharp
// Consumption SKU (serverless)
var consumptionSchedulerData = new DurableTaskSchedulerData(AzureLocation.EastUS)
{
    Properties = new DurableTaskSchedulerProperties
    {
        Sku = new DurableTaskSchedulerSku(DurableTaskSchedulerSkuName.Consumption)
        // No capacity needed for consumption
    }
};

var operation = await schedulerCollection.CreateOrUpdateAsync(
    WaitUntil.Completed,
    "my-serverless-scheduler",
    consumptionSchedulerData);
```

### 3. Create Task Hub

```csharp
// Task hubs are created under a scheduler
var taskHubData = new DurableTaskHubData
{
    // Properties are optional for basic task hub
};

var taskHubCollection = scheduler.GetDurableTaskHubs();
var hubOperation = await taskHubCollection.CreateOrUpdateAsync(
    WaitUntil.Completed,
    "my-taskhub",
    taskHubData);

DurableTaskHubResource taskHub = hubOperation.Value;
Console.WriteLine($"Task Hub created: {taskHub.Data.Name}");
```

### 4. List Schedulers

```csharp
// List all schedulers in subscription
await foreach (var sched in subscription.GetDurableTaskSchedulersAsync())
{
    Console.WriteLine($"Scheduler: {sched.Data.Name}");
    Console.WriteLine($"  Location: {sched.Data.Location}");
    Console.WriteLine($"  SKU: {sched.Data.Properties.Sku?.Name}");
    Console.WriteLine($"  Endpoint: {sched.Data.Properties.Endpoint}");
}

// List schedulers in resource group
var schedulers = resourceGroup.Value.GetDurableTaskSchedulers();
await foreach (var sched in schedulers.GetAllAsync())
{
    Console.WriteLine($"Scheduler: {sched.Data.Name}");
}
```

### 5. Get Scheduler by Name

```csharp
// Get existing scheduler
var existingScheduler = await schedulerCollection.GetAsync("my-scheduler");
Console.WriteLine($"Found: {existingScheduler.Value.Data.Name}");

// Or use extension method
var schedulerResource = armClient.GetDurableTaskSchedulerResource(
    DurableTaskSchedulerResource.CreateResourceIdentifier(
        subscriptionId,
        "my-resource-group",
        "my-scheduler"));
var scheduler = await schedulerResource.GetAsync();
```

### 6. Update Scheduler

```csharp
// Get current scheduler
var scheduler = await schedulerCollection.GetAsync("my-scheduler");

// Update with new configuration
var updateData = new DurableTaskSchedulerData(scheduler.Value.Data.Location)
{
    Properties = new DurableTaskSchedulerProperties
    {
        Sku = new DurableTaskSchedulerSku(DurableTaskSchedulerSkuName.Dedicated)
        {
            Capacity = 2  // Scale up
        },
        IPAllowlist = { "10.0.0.0/16" }  // Update IP allowlist
    }
};

var updateOperation = await schedulerCollection.CreateOrUpdateAsync(
    WaitUntil.Completed,
    "my-scheduler",
    updateData);
```

### 7. Delete Resources

```csharp
// Delete task hub first
var taskHub = await scheduler.GetDurableTaskHubs().GetAsync("my-taskhub");
await taskHub.Value.DeleteAsync(WaitUntil.Completed);

// Then delete scheduler
await scheduler.DeleteAsync(WaitUntil.Completed);
```

### 8. Manage Retention Policies

```csharp
// Get retention policy collection
var retentionPolicies = scheduler.GetDurableTaskRetentionPolicies();

// Create or update retention policy
var retentionData = new DurableTaskRetentionPolicyData
{
    Properties = new DurableTaskRetentionPolicyProperties
    {
        // Configure retention settings
    }
};

var retentionOperation = await retentionPolicies.CreateOrUpdateAsync(
    WaitUntil.Completed,
    "default",  // Policy name
    retentionData);
```

## Key Types Reference

| Type | Purpose |
|------|---------|
| `ArmClient` | Entry point for all ARM operations |
| `DurableTaskSchedulerResource` | Represents a Durable Task Scheduler |
| `DurableTaskSchedulerCollection` | Collection for scheduler CRUD |
| `DurableTaskSchedulerData` | Scheduler creation/update payload |
| `DurableTaskSchedulerProperties` | Scheduler configuration (SKU, IPAllowlist) |
| `DurableTaskSchedulerSku` | SKU configuration (Name, Capacity, RedundancyState) |
| `DurableTaskSchedulerSkuName` | SKU options: `Dedicated`, `Consumption` |
| `DurableTaskHubResource` | Represents a Task Hub |
| `DurableTaskHubCollection` | Collection for task hub CRUD |
| `DurableTaskHubData` | Task hub creation payload |
| `DurableTaskRetentionPolicyResource` | Retention policy management |
| `DurableTaskRetentionPolicyData` | Retention policy configuration |
| `DurableTaskExtensions` | Extension methods for ARM client |

## SKU Options

| SKU | Description | Use Case |
|-----|-------------|----------|
| `Dedicated` | Fixed capacity with configurable instances | Production workloads, predictable performance |
| `Consumption` | Serverless, auto-scaling | Development, variable workloads |

## Extension Methods

The SDK provides extension methods on `SubscriptionResource` and `ResourceGroupResource`:

```csharp
// On SubscriptionResource
subscription.GetDurableTaskSchedulers();           // List all in subscription
subscription.GetDurableTaskSchedulersAsync();      // Async enumerable

// On ResourceGroupResource  
resourceGroup.GetDurableTaskSchedulers();          // Get collection
resourceGroup.GetDurableTaskSchedulerAsync(name);  // Get by name

// On ArmClient
armClient.GetDurableTaskSchedulerResource(id);     // Get by resource ID
armClient.GetDurableTaskHubResource(id);           // Get task hub by ID
```

## Best Practices

1. **Use `WaitUntil.Completed`** for operations that must finish before proceeding
2. **Use `WaitUntil.Started`** when you want to poll manually or run operations in parallel
3. **Always use `DefaultAzureCredential`** — never hardcode keys
4. **Handle `RequestFailedException`** for ARM API errors
5. **Use `CreateOrUpdateAsync`** for idempotent operations
6. **Delete task hubs before schedulers** — schedulers with task hubs cannot be deleted
7. **Use IP allowlists** for network security in production

## Error Handling

```csharp
using Azure;

try
{
    var operation = await schedulerCollection.CreateOrUpdateAsync(
        WaitUntil.Completed, schedulerName, schedulerData);
}
catch (RequestFailedException ex) when (ex.Status == 409)
{
    Console.WriteLine("Scheduler already exists");
}
catch (RequestFailedException ex) when (ex.Status == 404)
{
    Console.WriteLine("Resource group not found");
}
catch (RequestFailedException ex)
{
    Console.WriteLine($"ARM Error: {ex.Status} - {ex.ErrorCode}: {ex.Message}");
}
```

## Complete Example

```csharp
using Azure;
using Azure.Identity;
using Azure.ResourceManager;
using Azure.ResourceManager.DurableTask;
using Azure.ResourceManager.DurableTask.Models;
using Azure.ResourceManager.Resources;

// Setup
var credential = new DefaultAzureCredential();
var armClient = new ArmClient(credential);

var subscriptionId = Environment.GetEnvironmentVariable("AZURE_SUBSCRIPTION_ID")!;
var resourceGroupName = Environment.GetEnvironmentVariable("AZURE_RESOURCE_GROUP")!;

var subscription = armClient.GetSubscriptionResource(
    new ResourceIdentifier($"/subscriptions/{subscriptionId}"));
var resourceGroup = await subscription.GetResourceGroupAsync(resourceGroupName);

// Create scheduler
var schedulerData = new DurableTaskSchedulerData(AzureLocation.EastUS)
{
    Properties = new DurableTaskSchedulerProperties
    {
        Sku = new DurableTaskSchedulerSku(DurableTaskSchedulerSkuName.Dedicated)
        {
            Capacity = 1
        }
    }
};

var schedulerCollection = resourceGroup.Value.GetDurableTaskSchedulers();
var schedulerOp = await schedulerCollection.CreateOrUpdateAsync(
    WaitUntil.Completed, "my-scheduler", schedulerData);
var scheduler = schedulerOp.Value;

Console.WriteLine($"Scheduler endpoint: {scheduler.Data.Properties.Endpoint}");

// Create task hub
var taskHubData = new DurableTaskHubData();
var taskHubOp = await scheduler.GetDurableTaskHubs().CreateOrUpdateAsync(
    WaitUntil.Completed, "my-taskhub", taskHubData);
var taskHub = taskHubOp.Value;

Console.WriteLine($"Task Hub: {taskHub.Data.Name}");

// Cleanup
await taskHub.DeleteAsync(WaitUntil.Completed);
await scheduler.DeleteAsync(WaitUntil.Completed);
```

## Related SDKs

| SDK | Purpose | Install |
|-----|---------|---------|
| `Azure.ResourceManager.DurableTask` | Management plane (this SDK) | `dotnet add package Azure.ResourceManager.DurableTask` |
| `Microsoft.DurableTask.Client.AzureManaged` | Data plane (orchestrations, activities) | `dotnet add package Microsoft.DurableTask.Client.AzureManaged` |
| `Microsoft.DurableTask.Worker.AzureManaged` | Worker for running orchestrations | `dotnet add package Microsoft.DurableTask.Worker.AzureManaged` |
| `Azure.Identity` | Authentication | `dotnet add package Azure.Identity` |
| `Azure.ResourceManager` | Base ARM SDK | `dotnet add package Azure.ResourceManager` |

## Source Reference

- [GitHub: Azure.ResourceManager.DurableTask](https://github.com/Azure/azure-sdk-for-net/tree/main/sdk/durabletask/Azure.ResourceManager.DurableTask)
- [NuGet: Azure.ResourceManager.DurableTask](https://www.nuget.org/packages/Azure.ResourceManager.DurableTask)

## When to Use
This skill is applicable to execute the workflow or actions described in the overview.

---

# Azure.ResourceManager.PostgreSql (.NET)

Azure Resource Manager SDK for managing PostgreSQL Flexible Server deployments.

## Installation

```bash
dotnet add package Azure.ResourceManager.PostgreSql
dotnet add package Azure.Identity
```

**Current Version**: v1.2.0 (GA)  
**API Version**: 2023-12-01-preview

> **Note**: This skill focuses on PostgreSQL Flexible Server. Single Server is deprecated and scheduled for retirement.

## Environment Variables

```bash
AZURE_SUBSCRIPTION_ID=<your-subscription-id>
AZURE_RESOURCE_GROUP=<your-resource-group>
AZURE_POSTGRESQL_SERVER_NAME=<your-postgresql-server>
```

## Authentication

```csharp
using Azure.Identity;
using Azure.ResourceManager;
using Azure.ResourceManager.PostgreSql;
using Azure.ResourceManager.PostgreSql.FlexibleServers;

ArmClient client = new ArmClient(new DefaultAzureCredential());
```

## Resource Hierarchy

```
Subscription
└── ResourceGroup
    └── PostgreSqlFlexibleServer              # PostgreSQL Flexible Server instance
        ├── PostgreSqlFlexibleServerDatabase  # Database within the server
        ├── PostgreSqlFlexibleServerFirewallRule # IP firewall rules
        ├── PostgreSqlFlexibleServerConfiguration # Server parameters
        ├── PostgreSqlFlexibleServerBackup    # Backup information
        ├── PostgreSqlFlexibleServerActiveDirectoryAdministrator # Entra ID admin
        └── PostgreSqlFlexibleServerVirtualEndpoint # Read replica endpoints
```

## Core Workflows

### 1. Create PostgreSQL Flexible Server

```csharp
using Azure.ResourceManager.PostgreSql.FlexibleServers;
using Azure.ResourceManager.PostgreSql.FlexibleServers.Models;

ResourceGroupResource resourceGroup = await client
    .GetDefaultSubscriptionAsync()
    .Result
    .GetResourceGroupAsync("my-resource-group");

PostgreSqlFlexibleServerCollection servers = resourceGroup.GetPostgreSqlFlexibleServers();

PostgreSqlFlexibleServerData data = new PostgreSqlFlexibleServerData(AzureLocation.EastUS)
{
    Sku = new PostgreSqlFlexibleServerSku("Standard_D2ds_v4", PostgreSqlFlexibleServerSkuTier.GeneralPurpose),
    AdministratorLogin = "pgadmin",
    AdministratorLoginPassword = "YourSecurePassword123!",
    Version = PostgreSqlFlexibleServerVersion.Ver16,
    Storage = new PostgreSqlFlexibleServerStorage
    {
        StorageSizeInGB = 128,
        AutoGrow = StorageAutoGrow.Enabled,
        Tier = PostgreSqlStorageTierName.P30
    },
    Backup = new PostgreSqlFlexibleServerBackupProperties
    {
        BackupRetentionDays = 7,
        GeoRedundantBackup = PostgreSqlFlexibleServerGeoRedundantBackupEnum.Disabled
    },
    HighAvailability = new PostgreSqlFlexibleServerHighAvailability
    {
        Mode = PostgreSqlFlexibleServerHighAvailabilityMode.ZoneRedundant,
        StandbyAvailabilityZone = "2"
    },
    AvailabilityZone = "1",
    AuthConfig = new PostgreSqlFlexibleServerAuthConfig
    {
        ActiveDirectoryAuth = PostgreSqlFlexibleServerActiveDirectoryAuthEnum.Enabled,
        PasswordAuth = PostgreSqlFlexibleServerPasswordAuthEnum.Enabled
    }
};

ArmOperation<PostgreSqlFlexibleServerResource> operation = await servers
    .CreateOrUpdateAsync(WaitUntil.Completed, "my-postgresql-server", data);

PostgreSqlFlexibleServerResource server = operation.Value;
Console.WriteLine($"Server created: {server.Data.FullyQualifiedDomainName}");
```

### 2. Create Database

```csharp
PostgreSqlFlexibleServerResource server = await resourceGroup
    .GetPostgreSqlFlexibleServerAsync("my-postgresql-server");

PostgreSqlFlexibleServerDatabaseCollection databases = server.GetPostgreSqlFlexibleServerDatabases();

PostgreSqlFlexibleServerDatabaseData dbData = new PostgreSqlFlexibleServerDatabaseData
{
    Charset = "UTF8",
    Collation = "en_US.utf8"
};

ArmOperation<PostgreSqlFlexibleServerDatabaseResource> operation = await databases
    .CreateOrUpdateAsync(WaitUntil.Completed, "myappdb", dbData);

PostgreSqlFlexibleServerDatabaseResource database = operation.Value;
Console.WriteLine($"Database created: {database.Data.Name}");
```

### 3. Configure Firewall Rules

```csharp
PostgreSqlFlexibleServerFirewallRuleCollection firewallRules = server.GetPostgreSqlFlexibleServerFirewallRules();

// Allow specific IP range
PostgreSqlFlexibleServerFirewallRuleData ruleData = new PostgreSqlFlexibleServerFirewallRuleData
{
    StartIPAddress = System.Net.IPAddress.Parse("10.0.0.1"),
    EndIPAddress = System.Net.IPAddress.Parse("10.0.0.255")
};

ArmOperation<PostgreSqlFlexibleServerFirewallRuleResource> operation = await firewallRules
    .CreateOrUpdateAsync(WaitUntil.Completed, "allow-internal", ruleData);

// Allow Azure services
PostgreSqlFlexibleServerFirewallRuleData azureServicesRule = new PostgreSqlFlexibleServerFirewallRuleData
{
    StartIPAddress = System.Net.IPAddress.Parse("0.0.0.0"),
    EndIPAddress = System.Net.IPAddress.Parse("0.0.0.0")
};

await firewallRules.CreateOrUpdateAsync(WaitUntil.Completed, "AllowAllAzureServicesAndResourcesWithinAzureIps", azureServicesRule);
```

### 4. Update Server Configuration

```csharp
PostgreSqlFlexibleServerConfigurationCollection configurations = server.GetPostgreSqlFlexibleServerConfigurations();

// Get current configuration
PostgreSqlFlexibleServerConfigurationResource config = await configurations
    .GetAsync("max_connections");

// Update configuration
PostgreSqlFlexibleServerConfigurationData configData = new PostgreSqlFlexibleServerConfigurationData
{
    Value = "500",
    Source = "user-override"
};

ArmOperation<PostgreSqlFlexibleServerConfigurationResource> operation = await configurations
    .CreateOrUpdateAsync(WaitUntil.Completed, "max_connections", configData);

// Common PostgreSQL configurations to tune
string[] commonParams = { 
    "max_connections", 
    "shared_buffers", 
    "work_mem", 
    "maintenance_work_mem",
    "effective_cache_size",
    "log_min_duration_statement"
};
```

### 5. Configure Entra ID Administrator

```csharp
PostgreSqlFlexibleServerActiveDirectoryAdministratorCollection admins = 
    server.GetPostgreSqlFlexibleServerActiveDirectoryAdministrators();

PostgreSqlFlexibleServerActiveDirectoryAdministratorData adminData = 
    new PostgreSqlFlexibleServerActiveDirectoryAdministratorData
{
    PrincipalType = PostgreSqlFlexibleServerPrincipalType.User,
    PrincipalName = "aad-admin@contoso.com",
    TenantId = Guid.Parse("<tenant-id>")
};

ArmOperation<PostgreSqlFlexibleServerActiveDirectoryAdministratorResource> operation = await admins
    .CreateOrUpdateAsync(WaitUntil.Completed, "<entra-object-id>", adminData);
```

### 6. List and Manage Servers

```csharp
// List servers in resource group
await foreach (PostgreSqlFlexibleServerResource server in resourceGroup.GetPostgreSqlFlexibleServers())
{
    Console.WriteLine($"Server: {server.Data.Name}");
    Console.WriteLine($"  FQDN: {server.Data.FullyQualifiedDomainName}");
    Console.WriteLine($"  Version: {server.Data.Version}");
    Console.WriteLine($"  State: {server.Data.State}");
    Console.WriteLine($"  SKU: {server.Data.Sku.Name} ({server.Data.Sku.Tier})");
    Console.WriteLine($"  HA: {server.Data.HighAvailability?.Mode}");
}

// List databases in server
await foreach (PostgreSqlFlexibleServerDatabaseResource db in server.GetPostgreSqlFlexibleServerDatabases())
{
    Console.WriteLine($"Database: {db.Data.Name}");
}
```

### 7. Backup and Point-in-Time Restore

```csharp
// List available backups
await foreach (PostgreSqlFlexibleServerBackupResource backup in server.GetPostgreSqlFlexibleServerBackups())
{
    Console.WriteLine($"Backup: {backup.Data.Name}");
    Console.WriteLine($"  Type: {backup.Data.BackupType}");
    Console.WriteLine($"  Completed: {backup.Data.CompletedOn}");
}

// Point-in-time restore
PostgreSqlFlexibleServerData restoreData = new PostgreSqlFlexibleServerData(AzureLocation.EastUS)
{
    CreateMode = PostgreSqlFlexibleServerCreateMode.PointInTimeRestore,
    SourceServerResourceId = server.Id,
    PointInTimeUtc = DateTimeOffset.UtcNow.AddHours(-2)
};

ArmOperation<PostgreSqlFlexibleServerResource> operation = await servers
    .CreateOrUpdateAsync(WaitUntil.Completed, "my-postgresql-restored", restoreData);
```

### 8. Create Read Replica

```csharp
PostgreSqlFlexibleServerData replicaData = new PostgreSqlFlexibleServerData(AzureLocation.WestUS)
{
    CreateMode = PostgreSqlFlexibleServerCreateMode.Replica,
    SourceServerResourceId = server.Id,
    Sku = new PostgreSqlFlexibleServerSku("Standard_D2ds_v4", PostgreSqlFlexibleServerSkuTier.GeneralPurpose)
};

ArmOperation<PostgreSqlFlexibleServerResource> operation = await servers
    .CreateOrUpdateAsync(WaitUntil.Completed, "my-postgresql-replica", replicaData);
```

### 9. Stop and Start Server

```csharp
PostgreSqlFlexibleServerResource server = await resourceGroup
    .GetPostgreSqlFlexibleServerAsync("my-postgresql-server");

// Stop server (saves costs when not in use)
await server.StopAsync(WaitUntil.Completed);

// Start server
await server.StartAsync(WaitUntil.Completed);

// Restart server
await server.RestartAsync(WaitUntil.Completed, new PostgreSqlFlexibleServerRestartParameter
{
    RestartWithFailover = true,
    FailoverMode = PostgreSqlFlexibleServerFailoverMode.PlannedFailover
});
```

### 10. Update Server (Scale)

```csharp
PostgreSqlFlexibleServerResource server = await resourceGroup
    .GetPostgreSqlFlexibleServerAsync("my-postgresql-server");

PostgreSqlFlexibleServerPatch patch = new PostgreSqlFlexibleServerPatch
{
    Sku = new PostgreSqlFlexibleServerSku("Standard_D4ds_v4", PostgreSqlFlexibleServerSkuTier.GeneralPurpose),
    Storage = new PostgreSqlFlexibleServerStorage
    {
        StorageSizeInGB = 256,
        Tier = PostgreSqlStorageTierName.P40
    }
};

ArmOperation<PostgreSqlFlexibleServerResource> operation = await server
    .UpdateAsync(WaitUntil.Completed, patch);
```

### 11. Delete Server

```csharp
PostgreSqlFlexibleServerResource server = await resourceGroup
    .GetPostgreSqlFlexibleServerAsync("my-postgresql-server");

await server.DeleteAsync(WaitUntil.Completed);
```

## Key Types Reference

| Type | Purpose |
|------|---------|
| `PostgreSqlFlexibleServerResource` | Flexible Server instance |
| `PostgreSqlFlexibleServerData` | Server configuration data |
| `PostgreSqlFlexibleServerCollection` | Collection of servers |
| `PostgreSqlFlexibleServerDatabaseResource` | Database within server |
| `PostgreSqlFlexibleServerFirewallRuleResource` | IP firewall rule |
| `PostgreSqlFlexibleServerConfigurationResource` | Server parameter |
| `PostgreSqlFlexibleServerBackupResource` | Backup metadata |
| `PostgreSqlFlexibleServerActiveDirectoryAdministratorResource` | Entra ID admin |
| `PostgreSqlFlexibleServerSku` | SKU (compute tier + size) |
| `PostgreSqlFlexibleServerStorage` | Storage configuration |
| `PostgreSqlFlexibleServerHighAvailability` | HA configuration |
| `PostgreSqlFlexibleServerBackupProperties` | Backup settings |
| `PostgreSqlFlexibleServerAuthConfig` | Authentication settings |

## SKU Tiers

| Tier | Use Case | SKU Examples |
|------|----------|--------------|
| `Burstable` | Dev/test, light workloads | Standard_B1ms, Standard_B2s |
| `GeneralPurpose` | Production workloads | Standard_D2ds_v4, Standard_D4ds_v4 |
| `MemoryOptimized` | High memory requirements | Standard_E2ds_v4, Standard_E4ds_v4 |

## PostgreSQL Versions

| Version | Enum Value |
|---------|------------|
| PostgreSQL 11 | `Ver11` |
| PostgreSQL 12 | `Ver12` |
| PostgreSQL 13 | `Ver13` |
| PostgreSQL 14 | `Ver14` |
| PostgreSQL 15 | `Ver15` |
| PostgreSQL 16 | `Ver16` |

## High Availability Modes

| Mode | Description |
|------|-------------|
| `Disabled` | No HA (single server) |
| `SameZone` | HA within same availability zone |
| `ZoneRedundant` | HA across availability zones |

## Best Practices

1. **Use Flexible Server** — Single Server is deprecated
2. **Enable zone-redundant HA** — For production workloads
3. **Use DefaultAzureCredential** — Prefer over connection strings
4. **Configure Entra ID authentication** — More secure than SQL auth alone
5. **Enable both auth methods** — Entra ID + password for flexibility
6. **Set appropriate backup retention** — 7-35 days based on compliance
7. **Use private endpoints** — For secure network access
8. **Tune server parameters** — Based on workload characteristics
9. **Use read replicas** — For read-heavy workloads
10. **Stop dev/test servers** — Save costs when not in use

## Error Handling

```csharp
using Azure;

try
{
    ArmOperation<PostgreSqlFlexibleServerResource> operation = await servers
        .CreateOrUpdateAsync(WaitUntil.Completed, "my-postgresql", data);
}
catch (RequestFailedException ex) when (ex.Status == 409)
{
    Console.WriteLine("Server already exists");
}
catch (RequestFailedException ex) when (ex.Status == 400)
{
    Console.WriteLine($"Invalid configuration: {ex.Message}");
}
catch (RequestFailedException ex)
{
    Console.WriteLine($"Azure error: {ex.Status} - {ex.Message}");
}
```

## Connection String

After creating the server, connect using:

```csharp
// Npgsql connection string
string connectionString = $"Host={server.Data.FullyQualifiedDomainName};" +
    "Database=myappdb;" +
    "Username=pgadmin;" +
    "Password=YourSecurePassword123!;" +
    "SSL Mode=Require;Trust Server Certificate=true;";

// With Entra ID token (recommended)
var credential = new DefaultAzureCredential();
var token = await credential.GetTokenAsync(
    new TokenRequestContext(new[] { "https://ossrdbms-aad.database.windows.net/.default" }));

string connectionString = $"Host={server.Data.FullyQualifiedDomainName};" +
    "Database=myappdb;" +
    $"Username=aad-admin@contoso.com;" +
    $"Password={token.Token};" +
    "SSL Mode=Require;";
```

## Related SDKs

| SDK | Purpose | Install |
|-----|---------|---------|
| `Azure.ResourceManager.PostgreSql` | PostgreSQL management (this SDK) | `dotnet add package Azure.ResourceManager.PostgreSql` |
| `Azure.ResourceManager.MySql` | MySQL management | `dotnet add package Azure.ResourceManager.MySql` |
| `Npgsql` | PostgreSQL data access | `dotnet add package Npgsql` |
| `Npgsql.EntityFrameworkCore.PostgreSQL` | EF Core provider | `dotnet add package Npgsql.EntityFrameworkCore.PostgreSQL` |

## Reference Links

| Resource | URL |
|----------|-----|
| NuGet Package | https://www.nuget.org/packages/Azure.ResourceManager.PostgreSql |
| API Reference | https://learn.microsoft.com/dotnet/api/azure.resourcemanager.postgresql |
| Product Documentation | https://learn.microsoft.com/azure/postgresql/flexible-server/ |
| GitHub Source | https://github.com/Azure/azure-sdk-for-net/tree/main/sdk/postgresql/Azure.ResourceManager.PostgreSql |

## When to Use
This skill is applicable to execute the workflow or actions described in the overview.

---

# Azure.ResourceManager.MySql (.NET)

Azure Resource Manager SDK for managing MySQL Flexible Server deployments.

## Installation

```bash
dotnet add package Azure.ResourceManager.MySql
dotnet add package Azure.Identity
```

**Current Version**: v1.2.0 (GA)  
**API Version**: 2023-12-30

> **Note**: This skill focuses on MySQL Flexible Server. Single Server is deprecated and scheduled for retirement.

## Environment Variables

```bash
AZURE_SUBSCRIPTION_ID=<your-subscription-id>
AZURE_RESOURCE_GROUP=<your-resource-group>
AZURE_MYSQL_SERVER_NAME=<your-mysql-server>
```

## Authentication

```csharp
using Azure.Identity;
using Azure.ResourceManager;
using Azure.ResourceManager.MySql;
using Azure.ResourceManager.MySql.FlexibleServers;

ArmClient client = new ArmClient(new DefaultAzureCredential());
```

## Resource Hierarchy

```
Subscription
└── ResourceGroup
    └── MySqlFlexibleServer                 # MySQL Flexible Server instance
        ├── MySqlFlexibleServerDatabase     # Database within the server
        ├── MySqlFlexibleServerFirewallRule # IP firewall rules
        ├── MySqlFlexibleServerConfiguration # Server parameters
        ├── MySqlFlexibleServerBackup       # Backup information
        ├── MySqlFlexibleServerMaintenanceWindow # Maintenance schedule
        └── MySqlFlexibleServerAadAdministrator # Entra ID admin
```

## Core Workflows

### 1. Create MySQL Flexible Server

```csharp
using Azure.ResourceManager.MySql.FlexibleServers;
using Azure.ResourceManager.MySql.FlexibleServers.Models;

ResourceGroupResource resourceGroup = await client
    .GetDefaultSubscriptionAsync()
    .Result
    .GetResourceGroupAsync("my-resource-group");

MySqlFlexibleServerCollection servers = resourceGroup.GetMySqlFlexibleServers();

MySqlFlexibleServerData data = new MySqlFlexibleServerData(AzureLocation.EastUS)
{
    Sku = new MySqlFlexibleServerSku("Standard_D2ds_v4", MySqlFlexibleServerSkuTier.GeneralPurpose),
    AdministratorLogin = "mysqladmin",
    AdministratorLoginPassword = "YourSecurePassword123!",
    Version = MySqlFlexibleServerVersion.Ver8_0_21,
    Storage = new MySqlFlexibleServerStorage
    {
        StorageSizeInGB = 128,
        AutoGrow = MySqlFlexibleServerEnableStatusEnum.Enabled,
        Iops = 3000
    },
    Backup = new MySqlFlexibleServerBackupProperties
    {
        BackupRetentionDays = 7,
        GeoRedundantBackup = MySqlFlexibleServerEnableStatusEnum.Disabled
    },
    HighAvailability = new MySqlFlexibleServerHighAvailability
    {
        Mode = MySqlFlexibleServerHighAvailabilityMode.ZoneRedundant,
        StandbyAvailabilityZone = "2"
    },
    AvailabilityZone = "1"
};

ArmOperation<MySqlFlexibleServerResource> operation = await servers
    .CreateOrUpdateAsync(WaitUntil.Completed, "my-mysql-server", data);

MySqlFlexibleServerResource server = operation.Value;
Console.WriteLine($"Server created: {server.Data.FullyQualifiedDomainName}");
```

### 2. Create Database

```csharp
MySqlFlexibleServerResource server = await resourceGroup
    .GetMySqlFlexibleServerAsync("my-mysql-server");

MySqlFlexibleServerDatabaseCollection databases = server.GetMySqlFlexibleServerDatabases();

MySqlFlexibleServerDatabaseData dbData = new MySqlFlexibleServerDatabaseData
{
    Charset = "utf8mb4",
    Collation = "utf8mb4_unicode_ci"
};

ArmOperation<MySqlFlexibleServerDatabaseResource> operation = await databases
    .CreateOrUpdateAsync(WaitUntil.Completed, "myappdb", dbData);

MySqlFlexibleServerDatabaseResource database = operation.Value;
Console.WriteLine($"Database created: {database.Data.Name}");
```

### 3. Configure Firewall Rules

```csharp
MySqlFlexibleServerFirewallRuleCollection firewallRules = server.GetMySqlFlexibleServerFirewallRules();

// Allow specific IP range
MySqlFlexibleServerFirewallRuleData ruleData = new MySqlFlexibleServerFirewallRuleData
{
    StartIPAddress = System.Net.IPAddress.Parse("10.0.0.1"),
    EndIPAddress = System.Net.IPAddress.Parse("10.0.0.255")
};

ArmOperation<MySqlFlexibleServerFirewallRuleResource> operation = await firewallRules
    .CreateOrUpdateAsync(WaitUntil.Completed, "allow-internal", ruleData);

// Allow Azure services
MySqlFlexibleServerFirewallRuleData azureServicesRule = new MySqlFlexibleServerFirewallRuleData
{
    StartIPAddress = System.Net.IPAddress.Parse("0.0.0.0"),
    EndIPAddress = System.Net.IPAddress.Parse("0.0.0.0")
};

await firewallRules.CreateOrUpdateAsync(WaitUntil.Completed, "AllowAllAzureServicesAndResourcesWithinAzureIps", azureServicesRule);
```

### 4. Update Server Configuration

```csharp
MySqlFlexibleServerConfigurationCollection configurations = server.GetMySqlFlexibleServerConfigurations();

// Get current configuration
MySqlFlexibleServerConfigurationResource config = await configurations
    .GetAsync("max_connections");

// Update configuration
MySqlFlexibleServerConfigurationData configData = new MySqlFlexibleServerConfigurationData
{
    Value = "500",
    Source = MySqlFlexibleServerConfigurationSource.UserOverride
};

ArmOperation<MySqlFlexibleServerConfigurationResource> operation = await configurations
    .CreateOrUpdateAsync(WaitUntil.Completed, "max_connections", configData);

// Common configurations to tune
string[] commonParams = { "max_connections", "innodb_buffer_pool_size", "slow_query_log", "long_query_time" };
```

### 5. Configure Entra ID Administrator

```csharp
MySqlFlexibleServerAadAdministratorCollection admins = server.GetMySqlFlexibleServerAadAdministrators();

MySqlFlexibleServerAadAdministratorData adminData = new MySqlFlexibleServerAadAdministratorData
{
    AdministratorType = MySqlFlexibleServerAdministratorType.ActiveDirectory,
    Login = "aad-admin@contoso.com",
    Sid = Guid.Parse("<entra-object-id>"),
    TenantId = Guid.Parse("<tenant-id>"),
    IdentityResourceId = new ResourceIdentifier("/subscriptions/.../userAssignedIdentities/mysql-identity")
};

ArmOperation<MySqlFlexibleServerAadAdministratorResource> operation = await admins
    .CreateOrUpdateAsync(WaitUntil.Completed, "ActiveDirectory", adminData);
```

### 6. List and Manage Servers

```csharp
// List servers in resource group
await foreach (MySqlFlexibleServerResource server in resourceGroup.GetMySqlFlexibleServers())
{
    Console.WriteLine($"Server: {server.Data.Name}");
    Console.WriteLine($"  FQDN: {server.Data.FullyQualifiedDomainName}");
    Console.WriteLine($"  Version: {server.Data.Version}");
    Console.WriteLine($"  State: {server.Data.State}");
    Console.WriteLine($"  SKU: {server.Data.Sku.Name} ({server.Data.Sku.Tier})");
}

// List databases in server
await foreach (MySqlFlexibleServerDatabaseResource db in server.GetMySqlFlexibleServerDatabases())
{
    Console.WriteLine($"Database: {db.Data.Name}");
}
```

### 7. Backup and Restore

```csharp
// List available backups
await foreach (MySqlFlexibleServerBackupResource backup in server.GetMySqlFlexibleServerBackups())
{
    Console.WriteLine($"Backup: {backup.Data.Name}");
    Console.WriteLine($"  Type: {backup.Data.BackupType}");
    Console.WriteLine($"  Completed: {backup.Data.CompletedOn}");
}

// Point-in-time restore
MySqlFlexibleServerData restoreData = new MySqlFlexibleServerData(AzureLocation.EastUS)
{
    CreateMode = MySqlFlexibleServerCreateMode.PointInTimeRestore,
    SourceServerResourceId = server.Id,
    RestorePointInTime = DateTimeOffset.UtcNow.AddHours(-2)
};

ArmOperation<MySqlFlexibleServerResource> operation = await servers
    .CreateOrUpdateAsync(WaitUntil.Completed, "my-mysql-restored", restoreData);
```

### 8. Stop and Start Server

```csharp
MySqlFlexibleServerResource server = await resourceGroup
    .GetMySqlFlexibleServerAsync("my-mysql-server");

// Stop server (saves costs when not in use)
await server.StopAsync(WaitUntil.Completed);

// Start server
await server.StartAsync(WaitUntil.Completed);

// Restart server
await server.RestartAsync(WaitUntil.Completed, new MySqlFlexibleServerRestartParameter
{
    RestartWithFailover = MySqlFlexibleServerEnableStatusEnum.Enabled,
    MaxFailoverSeconds = 60
});
```

### 9. Update Server (Scale)

```csharp
MySqlFlexibleServerResource server = await resourceGroup
    .GetMySqlFlexibleServerAsync("my-mysql-server");

MySqlFlexibleServerPatch patch = new MySqlFlexibleServerPatch
{
    Sku = new MySqlFlexibleServerSku("Standard_D4ds_v4", MySqlFlexibleServerSkuTier.GeneralPurpose),
    Storage = new MySqlFlexibleServerStorage
    {
        StorageSizeInGB = 256,
        Iops = 6000
    }
};

ArmOperation<MySqlFlexibleServerResource> operation = await server
    .UpdateAsync(WaitUntil.Completed, patch);
```

### 10. Delete Server

```csharp
MySqlFlexibleServerResource server = await resourceGroup
    .GetMySqlFlexibleServerAsync("my-mysql-server");

await server.DeleteAsync(WaitUntil.Completed);
```

## Key Types Reference

| Type | Purpose |
|------|---------|
| `MySqlFlexibleServerResource` | Flexible Server instance |
| `MySqlFlexibleServerData` | Server configuration data |
| `MySqlFlexibleServerCollection` | Collection of servers |
| `MySqlFlexibleServerDatabaseResource` | Database within server |
| `MySqlFlexibleServerFirewallRuleResource` | IP firewall rule |
| `MySqlFlexibleServerConfigurationResource` | Server parameter |
| `MySqlFlexibleServerBackupResource` | Backup metadata |
| `MySqlFlexibleServerAadAdministratorResource` | Entra ID admin |
| `MySqlFlexibleServerSku` | SKU (compute tier + size) |
| `MySqlFlexibleServerStorage` | Storage configuration |
| `MySqlFlexibleServerHighAvailability` | HA configuration |
| `MySqlFlexibleServerBackupProperties` | Backup settings |

## SKU Tiers

| Tier | Use Case | SKU Examples |
|------|----------|--------------|
| `Burstable` | Dev/test, light workloads | Standard_B1ms, Standard_B2s |
| `GeneralPurpose` | Production workloads | Standard_D2ds_v4, Standard_D4ds_v4 |
| `MemoryOptimized` | High memory requirements | Standard_E2ds_v4, Standard_E4ds_v4 |

## High Availability Modes

| Mode | Description |
|------|-------------|
| `Disabled` | No HA (single server) |
| `SameZone` | HA within same availability zone |
| `ZoneRedundant` | HA across availability zones |

## Best Practices

1. **Use Flexible Server** — Single Server is deprecated
2. **Enable zone-redundant HA** — For production workloads
3. **Use DefaultAzureCredential** — Prefer over connection strings
4. **Configure Entra ID authentication** — More secure than SQL auth
5. **Enable auto-grow storage** — Prevents out-of-space issues
6. **Set appropriate backup retention** — 7-35 days based on compliance
7. **Use private endpoints** — For secure network access
8. **Tune server parameters** — Based on workload characteristics
9. **Monitor with Azure Monitor** — Enable metrics and logs
10. **Stop dev/test servers** — Save costs when not in use

## Error Handling

```csharp
using Azure;

try
{
    ArmOperation<MySqlFlexibleServerResource> operation = await servers
        .CreateOrUpdateAsync(WaitUntil.Completed, "my-mysql", data);
}
catch (RequestFailedException ex) when (ex.Status == 409)
{
    Console.WriteLine("Server already exists");
}
catch (RequestFailedException ex) when (ex.Status == 400)
{
    Console.WriteLine($"Invalid configuration: {ex.Message}");
}
catch (RequestFailedException ex)
{
    Console.WriteLine($"Azure error: {ex.Status} - {ex.Message}");
}
```

## Connection String

After creating the server, connect using:

```csharp
// ADO.NET connection string
string connectionString = $"Server={server.Data.FullyQualifiedDomainName};" +
    "Database=myappdb;" +
    "User Id=mysqladmin;" +
    "Password=YourSecurePassword123!;" +
    "SslMode=Required;";

// With Entra ID token (recommended)
var credential = new DefaultAzureCredential();
var token = await credential.GetTokenAsync(
    new TokenRequestContext(new[] { "https://ossrdbms-aad.database.windows.net/.default" }));

string connectionString = $"Server={server.Data.FullyQualifiedDomainName};" +
    "Database=myappdb;" +
    $"User Id=aad-admin@contoso.com;" +
    $"Password={token.Token};" +
    "SslMode=Required;";
```

## Related SDKs

| SDK | Purpose | Install |
|-----|---------|---------|
| `Azure.ResourceManager.MySql` | MySQL management (this SDK) | `dotnet add package Azure.ResourceManager.MySql` |
| `Azure.ResourceManager.PostgreSql` | PostgreSQL management | `dotnet add package Azure.ResourceManager.PostgreSql` |
| `MySqlConnector` | MySQL data access | `dotnet add package MySqlConnector` |

## Reference Links

| Resource | URL |
|----------|-----|
| NuGet Package | https://www.nuget.org/packages/Azure.ResourceManager.MySql |
| API Reference | https://learn.microsoft.com/dotnet/api/azure.resourcemanager.mysql |
| Product Documentation | https://learn.microsoft.com/azure/mysql/flexible-server/ |
| GitHub Source | https://github.com/Azure/azure-sdk-for-net/tree/main/sdk/mysql/Azure.ResourceManager.MySql |

## When to Use
This skill is applicable to execute the workflow or actions described in the overview.

---

# Azure.ResourceManager.Redis (.NET)

Management plane SDK for provisioning and managing Azure Cache for Redis resources via Azure Resource Manager.

> **⚠️ Management vs Data Plane**
> - **This SDK (Azure.ResourceManager.Redis)**: Create caches, configure firewall rules, manage access keys, set up geo-replication
> - **Data Plane SDK (StackExchange.Redis)**: Get/set keys, pub/sub, streams, Lua scripts

## Installation

```bash
dotnet add package Azure.ResourceManager.Redis
dotnet add package Azure.Identity
```

**Current Version**: 1.5.1 (Stable)  
**API Version**: 2024-11-01  
**Target Frameworks**: .NET 8.0, .NET Standard 2.0

## Environment Variables

```bash
AZURE_SUBSCRIPTION_ID=<your-subscription-id>
# For service principal auth (optional)
AZURE_TENANT_ID=<tenant-id>
AZURE_CLIENT_ID=<client-id>
AZURE_CLIENT_SECRET=<client-secret>
```

## Authentication

```csharp
using Azure.Identity;
using Azure.ResourceManager;
using Azure.ResourceManager.Redis;

// Always use DefaultAzureCredential
var credential = new DefaultAzureCredential();
var armClient = new ArmClient(credential);

// Get subscription
var subscriptionId = Environment.GetEnvironmentVariable("AZURE_SUBSCRIPTION_ID");
var subscription = armClient.GetSubscriptionResource(
    new ResourceIdentifier($"/subscriptions/{subscriptionId}"));
```

## Resource Hierarchy

```
ArmClient
└── SubscriptionResource
    └── ResourceGroupResource
        └── RedisResource
            ├── RedisFirewallRuleResource
            ├── RedisPatchScheduleResource
            ├── RedisLinkedServerWithPropertyResource
            ├── RedisPrivateEndpointConnectionResource
            └── RedisCacheAccessPolicyResource
```

## Core Workflows

### 1. Create Redis Cache

```csharp
using Azure.ResourceManager.Redis;
using Azure.ResourceManager.Redis.Models;

// Get resource group
var resourceGroup = await subscription
    .GetResourceGroupAsync("my-resource-group");

// Define cache configuration
var cacheData = new RedisCreateOrUpdateContent(
    location: AzureLocation.EastUS,
    sku: new RedisSku(RedisSkuName.Standard, RedisSkuFamily.BasicOrStandard, 1))
{
    EnableNonSslPort = false,
    MinimumTlsVersion = RedisTlsVersion.Tls1_2,
    RedisConfiguration = new RedisCommonConfiguration
    {
        MaxMemoryPolicy = "volatile-lru"
    },
    Tags =
    {
        ["environment"] = "production"
    }
};

// Create cache (long-running operation)
var cacheCollection = resourceGroup.Value.GetAllRedis();
var operation = await cacheCollection.CreateOrUpdateAsync(
    WaitUntil.Completed,
    "my-redis-cache",
    cacheData);

RedisResource cache = operation.Value;
Console.WriteLine($"Cache created: {cache.Data.HostName}");
```

### 2. Get Redis Cache

```csharp
// Get existing cache
var cache = await resourceGroup.Value
    .GetRedisAsync("my-redis-cache");

Console.WriteLine($"Host: {cache.Value.Data.HostName}");
Console.WriteLine($"Port: {cache.Value.Data.Port}");
Console.WriteLine($"SSL Port: {cache.Value.Data.SslPort}");
Console.WriteLine($"Provisioning State: {cache.Value.Data.ProvisioningState}");
```

### 3. Update Redis Cache

```csharp
var patchData = new RedisPatch
{
    Sku = new RedisSku(RedisSkuName.Standard, RedisSkuFamily.BasicOrStandard, 2),
    RedisConfiguration = new RedisCommonConfiguration
    {
        MaxMemoryPolicy = "allkeys-lru"
    }
};

var updateOperation = await cache.Value.UpdateAsync(
    WaitUntil.Completed,
    patchData);
```

### 4. Delete Redis Cache

```csharp
await cache.Value.DeleteAsync(WaitUntil.Completed);
```

### 5. Get Access Keys

```csharp
var keys = await cache.Value.GetKeysAsync();
Console.WriteLine($"Primary Key: {keys.Value.PrimaryKey}");
Console.WriteLine($"Secondary Key: {keys.Value.SecondaryKey}");
```

### 6. Regenerate Access Keys

```csharp
var regenerateContent = new RedisRegenerateKeyContent(RedisRegenerateKeyType.Primary);
var newKeys = await cache.Value.RegenerateKeyAsync(regenerateContent);
Console.WriteLine($"New Primary Key: {newKeys.Value.PrimaryKey}");
```

### 7. Manage Firewall Rules

```csharp
// Create firewall rule
var firewallData = new RedisFirewallRuleData(
    startIP: System.Net.IPAddress.Parse("10.0.0.1"),
    endIP: System.Net.IPAddress.Parse("10.0.0.255"));

var firewallCollection = cache.Value.GetRedisFirewallRules();
var firewallOperation = await firewallCollection.CreateOrUpdateAsync(
    WaitUntil.Completed,
    "allow-internal-network",
    firewallData);

// List all firewall rules
await foreach (var rule in firewallCollection.GetAllAsync())
{
    Console.WriteLine($"Rule: {rule.Data.Name} ({rule.Data.StartIP} - {rule.Data.EndIP})");
}

// Delete firewall rule
var ruleToDelete = await firewallCollection.GetAsync("allow-internal-network");
await ruleToDelete.Value.DeleteAsync(WaitUntil.Completed);
```

### 8. Configure Patch Schedule (Premium SKU)

```csharp
// Patch schedules require Premium SKU
var scheduleData = new RedisPatchScheduleData(
    new[]
    {
        new RedisPatchScheduleSetting(RedisDayOfWeek.Saturday, 2) // 2 AM Saturday
        {
            MaintenanceWindow = TimeSpan.FromHours(5)
        },
        new RedisPatchScheduleSetting(RedisDayOfWeek.Sunday, 2) // 2 AM Sunday
        {
            MaintenanceWindow = TimeSpan.FromHours(5)
        }
    });

var scheduleCollection = cache.Value.GetRedisPatchSchedules();
await scheduleCollection.CreateOrUpdateAsync(
    WaitUntil.Completed,
    RedisPatchScheduleDefaultName.Default,
    scheduleData);
```

### 9. Import/Export Data (Premium SKU)

```csharp
// Import data from blob storage
var importContent = new ImportRdbContent(
    files: new[] { "https://mystorageaccount.blob.core.windows.net/container/dump.rdb" },
    format: "RDB");

await cache.Value.ImportDataAsync(WaitUntil.Completed, importContent);

// Export data to blob storage
var exportContent = new ExportRdbContent(
    prefix: "backup",
    container: "https://mystorageaccount.blob.core.windows.net/container?sastoken",
    format: "RDB");

await cache.Value.ExportDataAsync(WaitUntil.Completed, exportContent);
```

### 10. Force Reboot

```csharp
var rebootContent = new RedisRebootContent
{
    RebootType = RedisRebootType.AllNodes,
    ShardId = 0 // For clustered caches
};

await cache.Value.ForceRebootAsync(rebootContent);
```

## SKU Reference

| SKU | Family | Capacity | Features |
|-----|--------|----------|----------|
| Basic | C | 0-6 | Single node, no SLA, dev/test only |
| Standard | C | 0-6 | Two nodes (primary/replica), SLA |
| Premium | P | 1-5 | Clustering, geo-replication, VNet, persistence |

**Capacity Sizes (Family C - Basic/Standard)**:
- C0: 250 MB
- C1: 1 GB
- C2: 2.5 GB
- C3: 6 GB
- C4: 13 GB
- C5: 26 GB
- C6: 53 GB

**Capacity Sizes (Family P - Premium)**:
- P1: 6 GB per shard
- P2: 13 GB per shard
- P3: 26 GB per shard
- P4: 53 GB per shard
- P5: 120 GB per shard

## Key Types Reference

| Type | Purpose |
|------|---------|
| `ArmClient` | Entry point for all ARM operations |
| `RedisResource` | Represents a Redis cache instance |
| `RedisCollection` | Collection for cache CRUD operations |
| `RedisFirewallRuleResource` | Firewall rule for IP filtering |
| `RedisPatchScheduleResource` | Maintenance window configuration |
| `RedisLinkedServerWithPropertyResource` | Geo-replication linked server |
| `RedisPrivateEndpointConnectionResource` | Private endpoint connection |
| `RedisCacheAccessPolicyResource` | RBAC access policy |
| `RedisCreateOrUpdateContent` | Cache creation payload |
| `RedisPatch` | Cache update payload |
| `RedisSku` | SKU configuration (name, family, capacity) |
| `RedisAccessKeys` | Primary and secondary access keys |
| `RedisRegenerateKeyContent` | Key regeneration request |

## Best Practices

1. **Use `WaitUntil.Completed`** for operations that must finish before proceeding
2. **Use `WaitUntil.Started`** when you want to poll manually or run operations in parallel
3. **Always use `DefaultAzureCredential`** — never hardcode keys
4. **Handle `RequestFailedException`** for ARM API errors
5. **Use `CreateOrUpdateAsync`** for idempotent operations
6. **Navigate hierarchy** via `Get*` methods (e.g., `cache.GetRedisFirewallRules()`)
7. **Use Premium SKU** for production workloads requiring geo-replication, clustering, or persistence
8. **Enable TLS 1.2 minimum** — set `MinimumTlsVersion = RedisTlsVersion.Tls1_2`
9. **Disable non-SSL port** — set `EnableNonSslPort = false` for security
10. **Rotate keys regularly** — use `RegenerateKeyAsync` and update connection strings

## Error Handling

```csharp
using Azure;

try
{
    var operation = await cacheCollection.CreateOrUpdateAsync(
        WaitUntil.Completed, cacheName, cacheData);
}
catch (RequestFailedException ex) when (ex.Status == 409)
{
    Console.WriteLine("Cache already exists");
}
catch (RequestFailedException ex) when (ex.Status == 400)
{
    Console.WriteLine($"Invalid configuration: {ex.Message}");
}
catch (RequestFailedException ex)
{
    Console.WriteLine($"ARM Error: {ex.Status} - {ex.ErrorCode}: {ex.Message}");
}
```

## Common Pitfalls

1. **SKU downgrades not allowed** — You cannot downgrade from Premium to Standard/Basic
2. **Clustering requires Premium** — Shard configuration only available on Premium SKU
3. **Geo-replication requires Premium** — Linked servers only work with Premium caches
4. **VNet injection requires Premium** — Virtual network support is Premium-only
5. **Patch schedules require Premium** — Maintenance windows only configurable on Premium
6. **Cache name globally unique** — Redis cache names must be unique across all Azure subscriptions
7. **Long provisioning times** — Cache creation can take 15-20 minutes; use `WaitUntil.Started` for async patterns

## Connecting with StackExchange.Redis (Data Plane)

After creating the cache with this management SDK, use StackExchange.Redis for data operations:

```csharp
using StackExchange.Redis;

// Get connection info from management SDK
var cache = await resourceGroup.Value.GetRedisAsync("my-redis-cache");
var keys = await cache.Value.GetKeysAsync();

// Connect with StackExchange.Redis
var connectionString = $"{cache.Value.Data.HostName}:{cache.Value.Data.SslPort},password={keys.Value.PrimaryKey},ssl=True,abortConnect=False";
var connection = ConnectionMultiplexer.Connect(connectionString);
var db = connection.GetDatabase();

// Data operations
await db.StringSetAsync("key", "value");
var value = await db.StringGetAsync("key");
```

## Related SDKs

| SDK | Purpose | Install |
|-----|---------|---------|
| `StackExchange.Redis` | Data plane (get/set, pub/sub, streams) | `dotnet add package StackExchange.Redis` |
| `Azure.ResourceManager.Redis` | Management plane (this SDK) | `dotnet add package Azure.ResourceManager.Redis` |
| `Microsoft.Azure.StackExchangeRedis` | Azure-specific Redis extensions | `dotnet add package Microsoft.Azure.StackExchangeRedis` |

## When to Use
This skill is applicable to execute the workflow or actions described in the overview.

---

# Azure.ResourceManager.Sql (.NET)

Management plane SDK for provisioning and managing Azure SQL resources via Azure Resource Manager.

> **⚠️ Management vs Data Plane**
> - **This SDK (Azure.ResourceManager.Sql)**: Create servers, databases, elastic pools, configure firewall rules, manage failover groups
> - **Data Plane SDK (Microsoft.Data.SqlClient)**: Execute queries, stored procedures, manage connections

## Installation

```bash
dotnet add package Azure.ResourceManager.Sql
dotnet add package Azure.Identity
```

**Current Versions**: Stable v1.3.0, Preview v1.4.0-beta.3

## Environment Variables

```bash
AZURE_SUBSCRIPTION_ID=<your-subscription-id>
# For service principal auth (optional)
AZURE_TENANT_ID=<tenant-id>
AZURE_CLIENT_ID=<client-id>
AZURE_CLIENT_SECRET=<client-secret>
```

## Authentication

```csharp
using Azure.Identity;
using Azure.ResourceManager;
using Azure.ResourceManager.Sql;

// Always use DefaultAzureCredential
var credential = new DefaultAzureCredential();
var armClient = new ArmClient(credential);

// Get subscription
var subscriptionId = Environment.GetEnvironmentVariable("AZURE_SUBSCRIPTION_ID");
var subscription = armClient.GetSubscriptionResource(
    new ResourceIdentifier($"/subscriptions/{subscriptionId}"));
```

## Resource Hierarchy

```
ArmClient
└── SubscriptionResource
    └── ResourceGroupResource
        └── SqlServerResource
            ├── SqlDatabaseResource
            ├── ElasticPoolResource
            │   └── ElasticPoolDatabaseResource
            ├── SqlFirewallRuleResource
            ├── FailoverGroupResource
            ├── ServerBlobAuditingPolicyResource
            ├── EncryptionProtectorResource
            └── VirtualNetworkRuleResource
```

## Core Workflow

### 1. Create SQL Server

```csharp
using Azure.ResourceManager.Sql;
using Azure.ResourceManager.Sql.Models;

// Get resource group
var resourceGroup = await subscription
    .GetResourceGroupAsync("my-resource-group");

// Define server
var serverData = new SqlServerData(AzureLocation.EastUS)
{
    AdministratorLogin = "sqladmin",
    AdministratorLoginPassword = "YourSecurePassword123!",
    Version = "12.0",
    MinimalTlsVersion = SqlMinimalTlsVersion.Tls1_2,
    PublicNetworkAccess = ServerNetworkAccessFlag.Enabled
};

// Create server (long-running operation)
var serverCollection = resourceGroup.Value.GetSqlServers();
var operation = await serverCollection.CreateOrUpdateAsync(
    WaitUntil.Completed,
    "my-sql-server",
    serverData);

SqlServerResource server = operation.Value;
```

### 2. Create SQL Database

```csharp
var databaseData = new SqlDatabaseData(AzureLocation.EastUS)
{
    Sku = new SqlSku("S0") { Tier = "Standard" },
    MaxSizeBytes = 2L * 1024 * 1024 * 1024, // 2 GB
    Collation = "SQL_Latin1_General_CP1_CI_AS",
    RequestedBackupStorageRedundancy = SqlBackupStorageRedundancy.Local
};

var databaseCollection = server.GetSqlDatabases();
var dbOperation = await databaseCollection.CreateOrUpdateAsync(
    WaitUntil.Completed,
    "my-database",
    databaseData);

SqlDatabaseResource database = dbOperation.Value;
```

### 3. Create Elastic Pool

```csharp
var poolData = new ElasticPoolData(AzureLocation.EastUS)
{
    Sku = new SqlSku("StandardPool")
    {
        Tier = "Standard",
        Capacity = 100 // 100 eDTUs
    },
    PerDatabaseSettings = new ElasticPoolPerDatabaseSettings
    {
        MinCapacity = 0,
        MaxCapacity = 100
    }
};

var poolCollection = server.GetElasticPools();
var poolOperation = await poolCollection.CreateOrUpdateAsync(
    WaitUntil.Completed,
    "my-elastic-pool",
    poolData);

ElasticPoolResource pool = poolOperation.Value;
```

### 4. Add Database to Elastic Pool

```csharp
var databaseData = new SqlDatabaseData(AzureLocation.EastUS)
{
    ElasticPoolId = pool.Id
};

await databaseCollection.CreateOrUpdateAsync(
    WaitUntil.Completed,
    "pooled-database",
    databaseData);
```

### 5. Configure Firewall Rules

```csharp
// Allow Azure services
var azureServicesRule = new SqlFirewallRuleData
{
    StartIPAddress = "0.0.0.0",
    EndIPAddress = "0.0.0.0"
};

var firewallCollection = server.GetSqlFirewallRules();
await firewallCollection.CreateOrUpdateAsync(
    WaitUntil.Completed,
    "AllowAzureServices",
    azureServicesRule);

// Allow specific IP range
var clientRule = new SqlFirewallRuleData
{
    StartIPAddress = "203.0.113.0",
    EndIPAddress = "203.0.113.255"
};

await firewallCollection.CreateOrUpdateAsync(
    WaitUntil.Completed,
    "AllowClientIPs",
    clientRule);
```

### 6. List Resources

```csharp
// List all servers in subscription
await foreach (var srv in subscription.GetSqlServersAsync())
{
    Console.WriteLine($"Server: {srv.Data.Name} in {srv.Data.Location}");
}

// List databases in a server
await foreach (var db in server.GetSqlDatabases())
{
    Console.WriteLine($"Database: {db.Data.Name}, SKU: {db.Data.Sku?.Name}");
}

// List elastic pools
await foreach (var ep in server.GetElasticPools())
{
    Console.WriteLine($"Pool: {ep.Data.Name}, DTU: {ep.Data.Sku?.Capacity}");
}
```

### 7. Get Connection String

```csharp
// Build connection string (server FQDN is predictable)
var serverFqdn = $"{server.Data.Name}.database.windows.net";
var connectionString = $"Server=tcp:{serverFqdn},1433;" +
    $"Initial Catalog={database.Data.Name};" +
    "Persist Security Info=False;" +
    $"User ID={server.Data.AdministratorLogin};" +
    "Password=<your-password>;" +
    "MultipleActiveResultSets=False;" +
    "Encrypt=True;" +
    "TrustServerCertificate=False;" +
    "Connection Timeout=30;";
```

## Key Types Reference

| Type | Purpose |
|------|---------|
| `ArmClient` | Entry point for all ARM operations |
| `SqlServerResource` | Represents an Azure SQL server |
| `SqlServerCollection` | Collection for server CRUD |
| `SqlDatabaseResource` | Represents a SQL database |
| `SqlDatabaseCollection` | Collection for database CRUD |
| `ElasticPoolResource` | Represents an elastic pool |
| `ElasticPoolCollection` | Collection for elastic pool CRUD |
| `SqlFirewallRuleResource` | Represents a firewall rule |
| `SqlFirewallRuleCollection` | Collection for firewall rule CRUD |
| `SqlServerData` | Server creation/update payload |
| `SqlDatabaseData` | Database creation/update payload |
| `ElasticPoolData` | Elastic pool creation/update payload |
| `SqlFirewallRuleData` | Firewall rule creation/update payload |
| `SqlSku` | SKU configuration (tier, capacity) |

## Common SKUs

### Database SKUs

| SKU Name | Tier | Description |
|----------|------|-------------|
| `Basic` | Basic | 5 DTUs, 2 GB max |
| `S0`-`S12` | Standard | 10-3000 DTUs |
| `P1`-`P15` | Premium | 125-4000 DTUs |
| `GP_Gen5_2` | GeneralPurpose | vCore-based, 2 vCores |
| `BC_Gen5_2` | BusinessCritical | vCore-based, 2 vCores |
| `HS_Gen5_2` | Hyperscale | vCore-based, 2 vCores |

### Elastic Pool SKUs

| SKU Name | Tier | Description |
|----------|------|-------------|
| `BasicPool` | Basic | 50-1600 eDTUs |
| `StandardPool` | Standard | 50-3000 eDTUs |
| `PremiumPool` | Premium | 125-4000 eDTUs |
| `GP_Gen5_2` | GeneralPurpose | vCore-based |
| `BC_Gen5_2` | BusinessCritical | vCore-based |

## Best Practices

1. **Use `WaitUntil.Completed`** for operations that must finish before proceeding
2. **Use `WaitUntil.Started`** when you want to poll manually or run operations in parallel
3. **Always use `DefaultAzureCredential`** — never hardcode passwords in production
4. **Handle `RequestFailedException`** for ARM API errors
5. **Use `CreateOrUpdateAsync`** for idempotent operations
6. **Navigate hierarchy** via `Get*` methods (e.g., `server.GetSqlDatabases()`)
7. **Use elastic pools** for cost optimization when managing multiple databases
8. **Configure firewall rules** before attempting connections

## Error Handling

```csharp
using Azure;

try
{
    var operation = await serverCollection.CreateOrUpdateAsync(
        WaitUntil.Completed, serverName, serverData);
}
catch (RequestFailedException ex) when (ex.Status == 409)
{
    Console.WriteLine("Server already exists");
}
catch (RequestFailedException ex) when (ex.Status == 400)
{
    Console.WriteLine($"Invalid request: {ex.Message}");
}
catch (RequestFailedException ex)
{
    Console.WriteLine($"ARM Error: {ex.Status} - {ex.ErrorCode}: {ex.Message}");
}
```

## Reference Files

| File | When to Read |
|------|--------------|
| references/server-management.md | Server CRUD, admin credentials, Azure AD auth, networking |
| references/database-operations.md | Database CRUD, scaling, backup, restore, copy |
| references/elastic-pools.md | Pool management, adding/removing databases, scaling |

## Related SDKs

| SDK | Purpose | Install |
|-----|---------|---------|
| `Microsoft.Data.SqlClient` | Data plane (execute queries, stored procedures) | `dotnet add package Microsoft.Data.SqlClient` |
| `Azure.ResourceManager.Sql` | Management plane (this SDK) | `dotnet add package Azure.ResourceManager.Sql` |
| `Microsoft.EntityFrameworkCore.SqlServer` | ORM for SQL Server | `dotnet add package Microsoft.EntityFrameworkCore.SqlServer` |

## When to Use
This skill is applicable to execute the workflow or actions described in the overview.

---

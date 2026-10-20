---
name: azure-mgmt-toolkit
description: Consolidated toolkit for azure-mgmt. Covers azure-mgmt-apimanagement-dotnet, azure-mgmt-botservice-dotnet, azure-mgmt-apicenter-dotnet, azure-mgmt-fabric-dotnet, azure-mgmt-mongodbatlas-dotnet, azure-mgmt-fabric-py, azure-mgmt-apimanagement-py, azure-mgmt-applicationinsights-dotnet, azure-mgmt-apicenter-py, azure-mgmt-weightsandbiases-dotnet, azure-mgmt-arizeaiobservabilityeval-dotnet, azure-mgmt-botservice-py
---
# Azure Mgmt Toolkit

## Core Capabilities
# Azure Mgmt Toolkit

# Azure.ResourceManager.ApiManagement (.NET)

Management plane SDK for provisioning and managing Azure API Management resources via Azure Resource Manager.

> **⚠️ Management vs Data Plane**
> - **This SDK (Azure.ResourceManager.ApiManagement)**: Create services, APIs, products, subscriptions, policies, users, groups
> - **Data Plane**: Direct API calls to your APIM gateway endpoints

## Installation

```bash
dotnet add package Azure.ResourceManager.ApiManagement
dotnet add package Azure.Identity
```

**Current Version**: v1.3.0

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
using Azure.ResourceManager.ApiManagement;

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
        └── ApiManagementServiceResource
            ├── ApiResource
            │   ├── ApiOperationResource
            │   │   └── ApiOperationPolicyResource
            │   ├── ApiPolicyResource
            │   ├── ApiSchemaResource
            │   └── ApiDiagnosticResource
            ├── ApiManagementProductResource
            │   ├── ProductApiResource
            │   ├── ProductGroupResource
            │   └── ProductPolicyResource
            ├── ApiManagementSubscriptionResource
            ├── ApiManagementPolicyResource
            ├── ApiManagementUserResource
            ├── ApiManagementGroupResource
            ├── ApiManagementBackendResource
            ├── ApiManagementGatewayResource
            ├── ApiManagementCertificateResource
            ├── ApiManagementNamedValueResource
            └── ApiManagementLoggerResource
```

## Core Workflow

### 1. Create API Management Service

```csharp
using Azure.ResourceManager.ApiManagement;
using Azure.ResourceManager.ApiManagement.Models;

// Get resource group
var resourceGroup = await subscription
    .GetResourceGroupAsync("my-resource-group");

// Define service
var serviceData = new ApiManagementServiceData(
    location: AzureLocation.EastUS,
    sku: new ApiManagementServiceSkuProperties(
        ApiManagementServiceSkuType.Developer, 
        capacity: 1),
    publisherEmail: "admin@contoso.com",
    publisherName: "Contoso");

// Create service (long-running operation - can take 30+ minutes)
var serviceCollection = resourceGroup.Value.GetApiManagementServices();
var operation = await serviceCollection.CreateOrUpdateAsync(
    WaitUntil.Completed,
    "my-apim-service",
    serviceData);

ApiManagementServiceResource service = operation.Value;
```

### 2. Create an API

```csharp
var apiData = new ApiCreateOrUpdateContent
{
    DisplayName = "My API",
    Path = "myapi",
    Protocols = { ApiOperationInvokableProtocol.Https },
    ServiceUri = new Uri("https://backend.contoso.com/api")
};

var apiCollection = service.GetApis();
var apiOperation = await apiCollection.CreateOrUpdateAsync(
    WaitUntil.Completed,
    "my-api",
    apiData);

ApiResource api = apiOperation.Value;
```

### 3. Create a Product

```csharp
var productData = new ApiManagementProductData
{
    DisplayName = "Starter",
    Description = "Starter tier with limited access",
    IsSubscriptionRequired = true,
    IsApprovalRequired = false,
    SubscriptionsLimit = 1,
    State = ApiManagementProductState.Published
};

var productCollection = service.GetApiManagementProducts();
var productOperation = await productCollection.CreateOrUpdateAsync(
    WaitUntil.Completed,
    "starter",
    productData);

ApiManagementProductResource product = productOperation.Value;

// Add API to product
await product.GetProductApis().CreateOrUpdateAsync(
    WaitUntil.Completed,
    "my-api");
```

### 4. Create a Subscription

```csharp
var subscriptionData = new ApiManagementSubscriptionCreateOrUpdateContent
{
    DisplayName = "My Subscription",
    Scope = $"/products/{product.Data.Name}",
    State = ApiManagementSubscriptionState.Active
};

var subscriptionCollection = service.GetApiManagementSubscriptions();
var subOperation = await subscriptionCollection.CreateOrUpdateAsync(
    WaitUntil.Completed,
    "my-subscription",
    subscriptionData);

ApiManagementSubscriptionResource subscription = subOperation.Value;

// Get subscription keys
var keys = await subscription.GetSecretsAsync();
Console.WriteLine($"Primary Key: {keys.Value.PrimaryKey}");
```

### 5. Set API Policy

```csharp
var policyXml = @"
<policies>
    <inbound>
        <rate-limit calls=""100"" renewal-period=""60"" />
        <set-header name=""X-Custom-Header"" exists-action=""override"">
            <value>CustomValue</value>
        </set-header>
        <base />
    </inbound>
    <backend>
        <base />
    </backend>
    <outbound>
        <base />
    </outbound>
    <on-error>
        <base />
    </on-error>
</policies>";

var policyData = new PolicyContractData
{
    Value = policyXml,
    Format = PolicyContentFormat.Xml
};

await api.GetApiPolicy().CreateOrUpdateAsync(
    WaitUntil.Completed,
    policyData);
```

### 6. Backup and Restore

```csharp
// Backup
var backupParams = new ApiManagementServiceBackupRestoreContent(
    storageAccount: "mystorageaccount",
    containerName: "apim-backups",
    backupName: "backup-2024-01-15")
{
    AccessType = StorageAccountAccessType.SystemAssignedManagedIdentity
};

await service.BackupAsync(WaitUntil.Completed, backupParams);

// Restore
await service.RestoreAsync(WaitUntil.Completed, backupParams);
```

## Key Types Reference

| Type | Purpose |
|------|---------|
| `ArmClient` | Entry point for all ARM operations |
| `ApiManagementServiceResource` | Represents an APIM service instance |
| `ApiManagementServiceCollection` | Collection for service CRUD |
| `ApiResource` | Represents an API |
| `ApiManagementProductResource` | Represents a product |
| `ApiManagementSubscriptionResource` | Represents a subscription |
| `ApiManagementPolicyResource` | Service-level policy |
| `ApiPolicyResource` | API-level policy |
| `ApiManagementUserResource` | Represents a user |
| `ApiManagementGroupResource` | Represents a group |
| `ApiManagementBackendResource` | Represents a backend service |
| `ApiManagementGatewayResource` | Represents a self-hosted gateway |

## SKU Types

| SKU | Purpose | Capacity |
|-----|---------|----------|
| `Developer` | Development/testing (no SLA) | 1 |
| `Basic` | Entry-level production | 1-2 |
| `Standard` | Medium workloads | 1-4 |
| `Premium` | High availability, multi-region | 1-12 per region |
| `Consumption` | Serverless, pay-per-call | N/A |

## Best Practices

1. **Use `WaitUntil.Completed`** for operations that must finish before proceeding
2. **Use `WaitUntil.Started`** for long operations like service creation (30+ min)
3. **Always use `DefaultAzureCredential`** — never hardcode keys
4. **Handle `RequestFailedException`** for ARM API errors
5. **Use `CreateOrUpdateAsync`** for idempotent operations
6. **Navigate hierarchy** via `Get*` methods (e.g., `service.GetApis()`)
7. **Policy format** — Use XML format for policies; JSON is also supported
8. **Service creation** — Developer SKU is fastest for testing (~15-30 min)

## Error Handling

```csharp
using Azure;

try
{
    var operation = await serviceCollection.CreateOrUpdateAsync(
        WaitUntil.Completed, serviceName, serviceData);
}
catch (RequestFailedException ex) when (ex.Status == 409)
{
    Console.WriteLine("Service already exists");
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

## Reference Files

| File | When to Read |
|------|--------------|
| references/service-management.md | Service CRUD, SKUs, networking, backup/restore |
| references/apis-operations.md | APIs, operations, schemas, versioning |
| references/products-subscriptions.md | Products, subscriptions, access control |
| references/policies.md | Policy XML patterns, scopes, common policies |

## Related Resources

| Resource | Purpose |
|----------|---------|
| [API Management Documentation](https://learn.microsoft.com/en-us/azure/api-management/) | Official Azure docs |
| [Policy Reference](https://learn.microsoft.com/en-us/azure/api-management/api-management-policies) | Complete policy reference |
| [SDK Reference](https://learn.microsoft.com/en-us/dotnet/api/azure.resourcemanager.apimanagement) | .NET API reference |

## When to Use
This skill is applicable to execute the workflow or actions described in the overview.

---

# Azure.ResourceManager.BotService (.NET)

Management plane SDK for provisioning and managing Azure Bot Service resources via Azure Resource Manager.

## Installation

```bash
dotnet add package Azure.ResourceManager.BotService
dotnet add package Azure.Identity
```

**Current Versions**: Stable v1.1.1, Preview v1.1.0-beta.1

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
using Azure.ResourceManager.BotService;

// Authenticate using DefaultAzureCredential
var credential = new DefaultAzureCredential();
ArmClient armClient = new ArmClient(credential);

// Get subscription and resource group
SubscriptionResource subscription = await armClient.GetDefaultSubscriptionAsync();
ResourceGroupResource resourceGroup = await subscription.GetResourceGroups().GetAsync("myResourceGroup");

// Access bot collection
BotCollection botCollection = resourceGroup.GetBots();
```

## Resource Hierarchy

```
ArmClient
└── SubscriptionResource
    └── ResourceGroupResource
        └── BotResource
            ├── BotChannelResource (DirectLine, Teams, Slack, etc.)
            ├── BotConnectionSettingResource (OAuth connections)
            └── BotServicePrivateEndpointConnectionResource
```

## Core Workflows

### 1. Create Bot Resource

```csharp
using Azure.ResourceManager.BotService;
using Azure.ResourceManager.BotService.Models;

// Create bot data
var botData = new BotData(AzureLocation.WestUS2)
{
    Kind = BotServiceKind.Azurebot,
    Sku = new BotServiceSku(BotServiceSkuName.F0),
    Properties = new BotProperties(
        displayName: "MyBot",
        endpoint: new Uri("https://mybot.azurewebsites.net/api/messages"),
        msaAppId: "<your-msa-app-id>")
    {
        Description = "My Azure Bot",
        MsaAppType = BotMsaAppType.MultiTenant
    }
};

// Create or update the bot
ArmOperation<BotResource> operation = await botCollection.CreateOrUpdateAsync(
    WaitUntil.Completed, 
    "myBotName", 
    botData);
    
BotResource bot = operation.Value;
Console.WriteLine($"Bot created: {bot.Data.Name}");
```

### 2. Configure DirectLine Channel

```csharp
// Get the bot
BotResource bot = await resourceGroup.GetBots().GetAsync("myBotName");

// Get channel collection
BotChannelCollection channels = bot.GetBotChannels();

// Create DirectLine channel configuration
var channelData = new BotChannelData(AzureLocation.WestUS2)
{
    Properties = new DirectLineChannel()
    {
        Properties = new DirectLineChannelProperties()
        {
            Sites = 
            {
                new DirectLineSite("Default Site")
                {
                    IsEnabled = true,
                    IsV1Enabled = false,
                    IsV3Enabled = true,
                    IsSecureSiteEnabled = true
                }
            }
        }
    }
};

// Create or update the channel
ArmOperation<BotChannelResource> channelOp = await channels.CreateOrUpdateAsync(
    WaitUntil.Completed,
    BotChannelName.DirectLineChannel,
    channelData);

Console.WriteLine("DirectLine channel configured");
```

### 3. Configure Microsoft Teams Channel

```csharp
var teamsChannelData = new BotChannelData(AzureLocation.WestUS2)
{
    Properties = new MsTeamsChannel()
    {
        Properties = new MsTeamsChannelProperties()
        {
            IsEnabled = true,
            EnableCalling = false
        }
    }
};

await channels.CreateOrUpdateAsync(
    WaitUntil.Completed,
    BotChannelName.MsTeamsChannel,
    teamsChannelData);
```

### 4. Configure Web Chat Channel

```csharp
var webChatChannelData = new BotChannelData(AzureLocation.WestUS2)
{
    Properties = new WebChatChannel()
    {
        Properties = new WebChatChannelProperties()
        {
            Sites =
            {
                new WebChatSite("Default Site")
                {
                    IsEnabled = true
                }
            }
        }
    }
};

await channels.CreateOrUpdateAsync(
    WaitUntil.Completed,
    BotChannelName.WebChatChannel,
    webChatChannelData);
```

### 5. Get Bot and List Channels

```csharp
// Get bot
BotResource bot = await botCollection.GetAsync("myBotName");
Console.WriteLine($"Bot: {bot.Data.Properties.DisplayName}");
Console.WriteLine($"Endpoint: {bot.Data.Properties.Endpoint}");

// List channels
await foreach (BotChannelResource channel in bot.GetBotChannels().GetAllAsync())
{
    Console.WriteLine($"Channel: {channel.Data.Name}");
}
```

### 6. Regenerate DirectLine Keys

```csharp
var regenerateRequest = new BotChannelRegenerateKeysContent(BotChannelName.DirectLineChannel)
{
    SiteName = "Default Site"
};

BotChannelResource channelWithKeys = await bot.GetBotChannelWithRegenerateKeysAsync(regenerateRequest);
```

### 7. Update Bot

```csharp
BotResource bot = await botCollection.GetAsync("myBotName");

// Update using patch
var updateData = new BotData(bot.Data.Location)
{
    Properties = new BotProperties(
        displayName: "Updated Bot Name",
        endpoint: bot.Data.Properties.Endpoint,
        msaAppId: bot.Data.Properties.MsaAppId)
    {
        Description = "Updated description"
    }
};

await bot.UpdateAsync(updateData);
```

### 8. Delete Bot

```csharp
BotResource bot = await botCollection.GetAsync("myBotName");
await bot.DeleteAsync(WaitUntil.Completed);
```

## Supported Channel Types

| Channel | Constant | Class |
|---------|----------|-------|
| Direct Line | `BotChannelName.DirectLineChannel` | `DirectLineChannel` |
| Direct Line Speech | `BotChannelName.DirectLineSpeechChannel` | `DirectLineSpeechChannel` |
| Microsoft Teams | `BotChannelName.MsTeamsChannel` | `MsTeamsChannel` |
| Web Chat | `BotChannelName.WebChatChannel` | `WebChatChannel` |
| Slack | `BotChannelName.SlackChannel` | `SlackChannel` |
| Facebook | `BotChannelName.FacebookChannel` | `FacebookChannel` |
| Email | `BotChannelName.EmailChannel` | `EmailChannel` |
| Telegram | `BotChannelName.TelegramChannel` | `TelegramChannel` |
| Telephony | `BotChannelName.TelephonyChannel` | `TelephonyChannel` |

## Key Types Reference

| Type | Purpose |
|------|---------|
| `ArmClient` | Entry point for all ARM operations |
| `BotResource` | Represents an Azure Bot resource |
| `BotCollection` | Collection for bot CRUD |
| `BotData` | Bot resource definition |
| `BotProperties` | Bot configuration properties |
| `BotChannelResource` | Channel configuration |
| `BotChannelCollection` | Collection of channels |
| `BotChannelData` | Channel configuration data |
| `BotConnectionSettingResource` | OAuth connection settings |

## BotServiceKind Values

| Value | Description |
|-------|-------------|
| `BotServiceKind.Azurebot` | Azure Bot (recommended) |
| `BotServiceKind.Bot` | Legacy Bot Framework bot |
| `BotServiceKind.Designer` | Composer bot |
| `BotServiceKind.Function` | Function bot |
| `BotServiceKind.Sdk` | SDK bot |

## BotServiceSkuName Values

| Value | Description |
|-------|-------------|
| `BotServiceSkuName.F0` | Free tier |
| `BotServiceSkuName.S1` | Standard tier |

## BotMsaAppType Values

| Value | Description |
|-------|-------------|
| `BotMsaAppType.MultiTenant` | Multi-tenant app |
| `BotMsaAppType.SingleTenant` | Single-tenant app |
| `BotMsaAppType.UserAssignedMSI` | User-assigned managed identity |

## Best Practices

1. **Always use `DefaultAzureCredential`** — supports multiple auth methods
2. **Use `WaitUntil.Completed`** for synchronous operations
3. **Handle `RequestFailedException`** for API errors
4. **Use async methods** (`*Async`) for all operations
5. **Store MSA App credentials securely** — use Key Vault for secrets
6. **Use managed identity** (`BotMsaAppType.UserAssignedMSI`) for production bots
7. **Enable secure sites** for DirectLine channels in production

## Error Handling

```csharp
using Azure;

try
{
    var operation = await botCollection.CreateOrUpdateAsync(
        WaitUntil.Completed, 
        botName, 
        botData);
}
catch (RequestFailedException ex) when (ex.Status == 409)
{
    Console.WriteLine("Bot already exists");
}
catch (RequestFailedException ex)
{
    Console.WriteLine($"ARM Error: {ex.Status} - {ex.ErrorCode}: {ex.Message}");
}
```

## Related SDKs

| SDK | Purpose | Install |
|-----|---------|---------|
| `Azure.ResourceManager.BotService` | Bot management (this SDK) | `dotnet add package Azure.ResourceManager.BotService` |
| `Microsoft.Bot.Builder` | Bot Framework SDK | `dotnet add package Microsoft.Bot.Builder` |
| `Microsoft.Bot.Builder.Integration.AspNet.Core` | ASP.NET Core integration | `dotnet add package Microsoft.Bot.Builder.Integration.AspNet.Core` |

## Reference Links

| Resource | URL |
|----------|-----|
| NuGet Package | https://www.nuget.org/packages/Azure.ResourceManager.BotService |
| API Reference | https://learn.microsoft.com/dotnet/api/azure.resourcemanager.botservice |
| GitHub Source | https://github.com/Azure/azure-sdk-for-net/tree/main/sdk/botservice/Azure.ResourceManager.BotService |
| Azure Bot Service Docs | https://learn.microsoft.com/azure/bot-service/ |

## When to Use
This skill is applicable to execute the workflow or actions described in the overview.

---

# Azure.ResourceManager.ApiCenter (.NET)

Centralized API inventory and governance SDK for managing APIs across your organization.

## Installation

```bash
dotnet add package Azure.ResourceManager.ApiCenter
dotnet add package Azure.Identity
```

**Current Version**: v1.0.0 (GA)  
**API Version**: 2024-03-01

## Environment Variables

```bash
AZURE_SUBSCRIPTION_ID=<your-subscription-id>
AZURE_RESOURCE_GROUP=<your-resource-group>
AZURE_APICENTER_SERVICE_NAME=<your-apicenter-service>
```

## Authentication

```csharp
using Azure.Identity;
using Azure.ResourceManager;
using Azure.ResourceManager.ApiCenter;

ArmClient client = new ArmClient(new DefaultAzureCredential());
```

## Resource Hierarchy

```
Subscription
└── ResourceGroup
    └── ApiCenterService                    # API inventory service
        ├── Workspace                       # Logical grouping of APIs
        │   ├── Api                         # API definition
        │   │   └── ApiVersion              # Version of the API
        │   │       └── ApiDefinition       # OpenAPI/GraphQL/etc specification
        │   ├── Environment                 # Deployment target (dev/staging/prod)
        │   └── Deployment                  # API deployed to environment
        └── MetadataSchema                  # Custom metadata definitions
```

## Core Workflows

### 1. Create API Center Service

```csharp
using Azure.ResourceManager.ApiCenter;
using Azure.ResourceManager.ApiCenter.Models;

ResourceGroupResource resourceGroup = await client
    .GetDefaultSubscriptionAsync()
    .Result
    .GetResourceGroupAsync("my-resource-group");

ApiCenterServiceCollection services = resourceGroup.GetApiCenterServices();

ApiCenterServiceData data = new ApiCenterServiceData(AzureLocation.EastUS)
{
    Identity = new ManagedServiceIdentity(ManagedServiceIdentityType.SystemAssigned)
};

ArmOperation<ApiCenterServiceResource> operation = await services
    .CreateOrUpdateAsync(WaitUntil.Completed, "my-api-center", data);

ApiCenterServiceResource service = operation.Value;
```

### 2. Create Workspace

```csharp
ApiCenterWorkspaceCollection workspaces = service.GetApiCenterWorkspaces();

ApiCenterWorkspaceData workspaceData = new ApiCenterWorkspaceData
{
    Title = "Engineering APIs",
    Description = "APIs owned by the engineering team"
};

ArmOperation<ApiCenterWorkspaceResource> operation = await workspaces
    .CreateOrUpdateAsync(WaitUntil.Completed, "engineering", workspaceData);

ApiCenterWorkspaceResource workspace = operation.Value;
```

### 3. Create API

```csharp
ApiCenterApiCollection apis = workspace.GetApiCenterApis();

ApiCenterApiData apiData = new ApiCenterApiData
{
    Title = "Orders API",
    Description = "API for managing customer orders",
    Kind = ApiKind.Rest,
    LifecycleStage = ApiLifecycleStage.Production,
    TermsOfService = new ApiTermsOfService
    {
        Uri = new Uri("https://example.com/terms")
    },
    ExternalDocumentation = 
    {
        new ApiExternalDocumentation
        {
            Title = "Documentation",
            Uri = new Uri("https://docs.example.com/orders")
        }
    },
    Contacts =
    {
        new ApiContact
        {
            Name = "API Support",
            Email = "api-support@example.com"
        }
    }
};

// Add custom metadata
apiData.CustomProperties = BinaryData.FromObjectAsJson(new
{
    team = "orders-team",
    costCenter = "CC-1234"
});

ArmOperation<ApiCenterApiResource> operation = await apis
    .CreateOrUpdateAsync(WaitUntil.Completed, "orders-api", apiData);

ApiCenterApiResource api = operation.Value;
```

### 4. Create API Version

```csharp
ApiCenterApiVersionCollection versions = api.GetApiCenterApiVersions();

ApiCenterApiVersionData versionData = new ApiCenterApiVersionData
{
    Title = "v1.0.0",
    LifecycleStage = ApiLifecycleStage.Production
};

ArmOperation<ApiCenterApiVersionResource> operation = await versions
    .CreateOrUpdateAsync(WaitUntil.Completed, "v1-0-0", versionData);

ApiCenterApiVersionResource version = operation.Value;
```

### 5. Create API Definition (Upload OpenAPI Spec)

```csharp
ApiCenterApiDefinitionCollection definitions = version.GetApiCenterApiDefinitions();

ApiCenterApiDefinitionData definitionData = new ApiCenterApiDefinitionData
{
    Title = "OpenAPI Specification",
    Description = "Orders API OpenAPI 3.0 definition"
};

ArmOperation<ApiCenterApiDefinitionResource> operation = await definitions
    .CreateOrUpdateAsync(WaitUntil.Completed, "openapi", definitionData);

ApiCenterApiDefinitionResource definition = operation.Value;

// Import specification
string openApiSpec = await File.ReadAllTextAsync("orders-api.yaml");

ApiSpecImportContent importContent = new ApiSpecImportContent
{
    Format = ApiSpecImportSourceFormat.Inline,
    Value = openApiSpec,
    Specification = new ApiSpecImportSpecification
    {
        Name = "openapi",
        Version = "3.0.1"
    }
};

await definition.ImportSpecificationAsync(WaitUntil.Completed, importContent);
```

### 6. Export API Specification

```csharp
ApiCenterApiDefinitionResource definition = await client
    .GetApiCenterApiDefinitionResource(definitionResourceId)
    .GetAsync();

ArmOperation<ApiSpecExportResult> operation = await definition
    .ExportSpecificationAsync(WaitUntil.Completed);

ApiSpecExportResult result = operation.Value;

// result.Format - e.g., "inline"
// result.Value - the specification content
```

### 7. Create Environment

```csharp
ApiCenterEnvironmentCollection environments = workspace.GetApiCenterEnvironments();

ApiCenterEnvironmentData envData = new ApiCenterEnvironmentData
{
    Title = "Production",
    Description = "Production environment",
    Kind = ApiCenterEnvironmentKind.Production,
    Server = new ApiCenterEnvironmentServer
    {
        ManagementPortalUris = { new Uri("https://portal.azure.com") }
    },
    Onboarding = new EnvironmentOnboardingModel
    {
        Instructions = "Contact platform team for access",
        DeveloperPortalUris = { new Uri("https://developer.example.com") }
    }
};

ArmOperation<ApiCenterEnvironmentResource> operation = await environments
    .CreateOrUpdateAsync(WaitUntil.Completed, "production", envData);
```

### 8. Create Deployment

```csharp
ApiCenterDeploymentCollection deployments = workspace.GetApiCenterDeployments();

// Get environment resource ID
ResourceIdentifier envResourceId = ApiCenterEnvironmentResource.CreateResourceIdentifier(
    subscriptionId, resourceGroupName, serviceName, workspaceName, "production");

// Get API definition resource ID
ResourceIdentifier definitionResourceId = ApiCenterApiDefinitionResource.CreateResourceIdentifier(
    subscriptionId, resourceGroupName, serviceName, workspaceName, 
    "orders-api", "v1-0-0", "openapi");

ApiCenterDeploymentData deploymentData = new ApiCenterDeploymentData
{
    Title = "Orders API - Production",
    Description = "Production deployment of Orders API v1.0.0",
    EnvironmentId = envResourceId,
    DefinitionId = definitionResourceId,
    State = ApiCenterDeploymentState.Active,
    Server = new ApiCenterDeploymentServer
    {
        RuntimeUris = { new Uri("https://api.example.com/orders") }
    }
};

ArmOperation<ApiCenterDeploymentResource> operation = await deployments
    .CreateOrUpdateAsync(WaitUntil.Completed, "orders-api-prod", deploymentData);
```

### 9. Create Metadata Schema

```csharp
ApiCenterMetadataSchemaCollection schemas = service.GetApiCenterMetadataSchemas();

string jsonSchema = """
{
    "type": "object",
    "properties": {
        "team": {
            "type": "string",
            "title": "Owning Team"
        },
        "costCenter": {
            "type": "string",
            "title": "Cost Center"
        },
        "dataClassification": {
            "type": "string",
            "enum": ["public", "internal", "confidential"],
            "title": "Data Classification"
        }
    },
    "required": ["team"]
}
""";

ApiCenterMetadataSchemaData schemaData = new ApiCenterMetadataSchemaData
{
    Schema = jsonSchema,
    AssignedTo =
    {
        new MetadataAssignment
        {
            Entity = MetadataAssignmentEntity.Api,
            Required = true
        }
    }
};

ArmOperation<ApiCenterMetadataSchemaResource> operation = await schemas
    .CreateOrUpdateAsync(WaitUntil.Completed, "api-metadata", schemaData);
```

### 10. List and Search APIs

```csharp
// List all APIs in a workspace
ApiCenterWorkspaceResource workspace = await client
    .GetApiCenterWorkspaceResource(workspaceResourceId)
    .GetAsync();

await foreach (ApiCenterApiResource api in workspace.GetApiCenterApis())
{
    Console.WriteLine($"API: {api.Data.Title}");
    Console.WriteLine($"  Kind: {api.Data.Kind}");
    Console.WriteLine($"  Stage: {api.Data.LifecycleStage}");
    
    // List versions
    await foreach (ApiCenterApiVersionResource version in api.GetApiCenterApiVersions())
    {
        Console.WriteLine($"  Version: {version.Data.Title}");
    }
}

// List environments
await foreach (ApiCenterEnvironmentResource env in workspace.GetApiCenterEnvironments())
{
    Console.WriteLine($"Environment: {env.Data.Title} ({env.Data.Kind})");
}

// List deployments
await foreach (ApiCenterDeploymentResource deployment in workspace.GetApiCenterDeployments())
{
    Console.WriteLine($"Deployment: {deployment.Data.Title}");
    Console.WriteLine($"  State: {deployment.Data.State}");
}
```

## Key Types Reference

| Type | Purpose |
|------|---------|
| `ApiCenterServiceResource` | API Center service instance |
| `ApiCenterWorkspaceResource` | Logical grouping of APIs |
| `ApiCenterApiResource` | Individual API |
| `ApiCenterApiVersionResource` | Version of an API |
| `ApiCenterApiDefinitionResource` | API specification (OpenAPI, etc.) |
| `ApiCenterEnvironmentResource` | Deployment environment |
| `ApiCenterDeploymentResource` | API deployment to environment |
| `ApiCenterMetadataSchemaResource` | Custom metadata schema |
| `ApiKind` | rest, graphql, grpc, soap, webhook, websocket, mcp |
| `ApiLifecycleStage` | design, development, testing, preview, production, deprecated, retired |
| `ApiCenterEnvironmentKind` | development, testing, staging, production |
| `ApiCenterDeploymentState` | active, inactive |

## Best Practices

1. **Organize with workspaces** — Group APIs by team, domain, or product
2. **Use metadata schemas** — Define custom properties for governance
3. **Track lifecycle stages** — Keep API status current (design → production → deprecated)
4. **Document environments** — Include onboarding instructions and portal URIs
5. **Version consistently** — Use semantic versioning for API versions
6. **Import specifications** — Upload OpenAPI/GraphQL specs for discovery
7. **Link deployments** — Connect APIs to their runtime environments
8. **Use managed identity** — Enable SystemAssigned identity for secure integrations

## Error Handling

```csharp
using Azure;

try
{
    ArmOperation<ApiCenterApiResource> operation = await apis
        .CreateOrUpdateAsync(WaitUntil.Completed, "my-api", apiData);
}
catch (RequestFailedException ex) when (ex.Status == 409)
{
    Console.WriteLine("API already exists with conflicting configuration");
}
catch (RequestFailedException ex) when (ex.Status == 400)
{
    Console.WriteLine($"Invalid request: {ex.Message}");
}
catch (RequestFailedException ex)
{
    Console.WriteLine($"Azure error: {ex.Status} - {ex.Message}");
}
```

## Related SDKs

| SDK | Purpose | Install |
|-----|---------|---------|
| `Azure.ResourceManager.ApiCenter` | API Center management (this SDK) | `dotnet add package Azure.ResourceManager.ApiCenter` |
| `Azure.ResourceManager.ApiManagement` | API gateway and policies | `dotnet add package Azure.ResourceManager.ApiManagement` |

## Reference Links

| Resource | URL |
|----------|-----|
| NuGet Package | https://www.nuget.org/packages/Azure.ResourceManager.ApiCenter |
| API Reference | https://learn.microsoft.com/dotnet/api/azure.resourcemanager.apicenter |
| Product Documentation | https://learn.microsoft.com/azure/api-center/ |
| GitHub Source | https://github.com/Azure/azure-sdk-for-net/tree/main/sdk/apicenter/Azure.ResourceManager.ApiCenter |

## When to Use
This skill is applicable to execute the workflow or actions described in the overview.

---

# Azure.ResourceManager.Fabric (.NET)

Management plane SDK for provisioning and managing Microsoft Fabric capacity resources via Azure Resource Manager.

> **Management Plane Only**
> This SDK manages Fabric *capacities* (compute resources). For working with Fabric workspaces, lakehouses, warehouses, and data items, use the Microsoft Fabric REST API or data plane SDKs.

## Installation

```bash
dotnet add package Azure.ResourceManager.Fabric
dotnet add package Azure.Identity
```

**Current Version**: 1.0.0 (GA - September 2025)  
**API Version**: 2023-11-01  
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
using Azure.ResourceManager.Fabric;

// Always use DefaultAzureCredential
var credential = new DefaultAzureCredential();
var armClient = new ArmClient(credential);

// Get subscription
var subscription = await armClient.GetDefaultSubscriptionAsync();
```

## Resource Hierarchy

```
ArmClient
└── SubscriptionResource
    └── ResourceGroupResource
        └── FabricCapacityResource
```

## Core Workflows

### 1. Create Fabric Capacity

```csharp
using Azure.ResourceManager.Fabric;
using Azure.ResourceManager.Fabric.Models;
using Azure.Core;

// Get resource group
var resourceGroup = await subscription.GetResourceGroupAsync("my-resource-group");

// Define capacity configuration
var administration = new FabricCapacityAdministration(
    new[] { "admin@contoso.com" }  // Capacity administrators (UPNs or object IDs)
);

var properties = new FabricCapacityProperties(administration);

var sku = new FabricSku("F64", FabricSkuTier.Fabric);

var capacityData = new FabricCapacityData(
    AzureLocation.WestUS2,
    properties,
    sku)
{
    Tags = { ["Environment"] = "Production" }
};

// Create capacity (long-running operation)
var capacityCollection = resourceGroup.Value.GetFabricCapacities();
var operation = await capacityCollection.CreateOrUpdateAsync(
    WaitUntil.Completed,
    "my-fabric-capacity",
    capacityData);

FabricCapacityResource capacity = operation.Value;
Console.WriteLine($"Created capacity: {capacity.Data.Name}");
Console.WriteLine($"State: {capacity.Data.Properties.State}");
```

### 2. Get Fabric Capacity

```csharp
// Get existing capacity
var capacity = await resourceGroup.Value
    .GetFabricCapacityAsync("my-fabric-capacity");

Console.WriteLine($"Name: {capacity.Value.Data.Name}");
Console.WriteLine($"Location: {capacity.Value.Data.Location}");
Console.WriteLine($"SKU: {capacity.Value.Data.Sku.Name}");
Console.WriteLine($"State: {capacity.Value.Data.Properties.State}");
Console.WriteLine($"Provisioning State: {capacity.Value.Data.Properties.ProvisioningState}");
```

### 3. Update Capacity (Scale SKU or Change Admins)

```csharp
var capacity = await resourceGroup.Value
    .GetFabricCapacityAsync("my-fabric-capacity");

var patch = new FabricCapacityPatch
{
    Sku = new FabricSku("F128", FabricSkuTier.Fabric),  // Scale up
    Properties = new FabricCapacityUpdateProperties
    {
        Administration = new FabricCapacityAdministration(
            new[] { "admin@contoso.com", "newadmin@contoso.com" }
        )
    }
};

var updateOperation = await capacity.Value.UpdateAsync(
    WaitUntil.Completed,
    patch);

Console.WriteLine($"Updated SKU: {updateOperation.Value.Data.Sku.Name}");
```

### 4. Suspend and Resume Capacity

```csharp
// Suspend capacity (stop billing for compute)
await capacity.Value.SuspendAsync(WaitUntil.Completed);
Console.WriteLine("Capacity suspended");

// Resume capacity
var resumeOperation = await capacity.Value.ResumeAsync(WaitUntil.Completed);
Console.WriteLine($"Capacity resumed. State: {resumeOperation.Value.Data.Properties.State}");
```

### 5. Delete Capacity

```csharp
await capacity.Value.DeleteAsync(WaitUntil.Completed);
Console.WriteLine("Capacity deleted");
```

### 6. List All Capacities

```csharp
// In a resource group
await foreach (var cap in resourceGroup.Value.GetFabricCapacities())
{
    Console.WriteLine($"- {cap.Data.Name} ({cap.Data.Sku.Name})");
}

// In a subscription
await foreach (var cap in subscription.GetFabricCapacitiesAsync())
{
    Console.WriteLine($"- {cap.Data.Name} in {cap.Data.Location}");
}
```

### 7. Check Name Availability

```csharp
var checkContent = new FabricNameAvailabilityContent
{
    Name = "my-new-capacity",
    ResourceType = "Microsoft.Fabric/capacities"
};

var result = await subscription.CheckFabricCapacityNameAvailabilityAsync(
    AzureLocation.WestUS2,
    checkContent);

if (result.Value.IsNameAvailable == true)
{
    Console.WriteLine("Name is available!");
}
else
{
    Console.WriteLine($"Name unavailable: {result.Value.Reason} - {result.Value.Message}");
}
```

### 8. List Available SKUs

```csharp
// List all SKUs available in subscription
await foreach (var skuDetails in subscription.GetSkusFabricCapacitiesAsync())
{
    Console.WriteLine($"SKU: {skuDetails.Name}");
    Console.WriteLine($"  Resource Type: {skuDetails.ResourceType}");
    foreach (var location in skuDetails.Locations)
    {
        Console.WriteLine($"  Location: {location}");
    }
}

// List SKUs available for an existing capacity (for scaling)
await foreach (var skuDetails in capacity.Value.GetSkusForCapacityAsync())
{
    Console.WriteLine($"Can scale to: {skuDetails.Sku.Name}");
}
```

## SKU Reference

| SKU Name | Capacity Units (CU) | Power BI Equivalent |
|----------|---------------------|---------------------|
| F2 | 2 | - |
| F4 | 4 | - |
| F8 | 8 | EM1/A1 |
| F16 | 16 | EM2/A2 |
| F32 | 32 | EM3/A3 |
| F64 | 64 | P1/A4 |
| F128 | 128 | P2/A5 |
| F256 | 256 | P3/A6 |
| F512 | 512 | P4/A7 |
| F1024 | 1024 | P5/A8 |
| F2048 | 2048 | - |

## Key Types Reference

| Type | Purpose |
|------|---------|
| `ArmClient` | Entry point for all ARM operations |
| `FabricCapacityResource` | Represents a Fabric capacity instance |
| `FabricCapacityCollection` | Collection for capacity CRUD operations |
| `FabricCapacityData` | Capacity creation/read data model |
| `FabricCapacityPatch` | Capacity update payload |
| `FabricCapacityProperties` | Capacity properties (administration, state) |
| `FabricCapacityAdministration` | Admin members configuration |
| `FabricSku` | SKU configuration (name and tier) |
| `FabricSkuTier` | Pricing tier (currently only "Fabric") |
| `FabricProvisioningState` | Provisioning states (Succeeded, Failed, etc.) |
| `FabricResourceState` | Resource states (Active, Suspended, etc.) |
| `FabricNameAvailabilityContent` | Name availability check request |
| `FabricNameAvailabilityResult` | Name availability check response |

## Provisioning and Resource States

### Provisioning States (`FabricProvisioningState`)
- `Succeeded` - Operation completed successfully
- `Failed` - Operation failed
- `Canceled` - Operation was canceled
- `Deleting` - Capacity is being deleted
- `Provisioning` - Initial provisioning in progress
- `Updating` - Update operation in progress

### Resource States (`FabricResourceState`)
- `Active` - Capacity is running and available
- `Provisioning` - Being provisioned
- `Failed` - In failed state
- `Updating` - Being updated
- `Deleting` - Being deleted
- `Suspending` - Transitioning to suspended
- `Suspended` - Suspended (not billing for compute)
- `Pausing` - Transitioning to paused
- `Paused` - Paused
- `Resuming` - Resuming from suspended/paused
- `Scaling` - Scaling to different SKU
- `Preparing` - Preparing resources

## Best Practices

1. **Use `WaitUntil.Completed`** for operations that must finish before proceeding
2. **Use `WaitUntil.Started`** when you want to poll manually or run operations in parallel
3. **Always use `DefaultAzureCredential`** — never hardcode credentials
4. **Handle `RequestFailedException`** for ARM API errors
5. **Use `CreateOrUpdateAsync`** for idempotent operations
6. **Suspend when not in use** — Fabric capacities bill for compute even when idle
7. **Check provisioning state** before performing operations on a capacity
8. **Use appropriate SKU** — Start small (F2/F4) for dev/test, scale up for production

## Error Handling

```csharp
using Azure;

try
{
    var operation = await capacityCollection.CreateOrUpdateAsync(
        WaitUntil.Completed, capacityName, capacityData);
}
catch (RequestFailedException ex) when (ex.Status == 409)
{
    Console.WriteLine("Capacity already exists or conflict");
}
catch (RequestFailedException ex) when (ex.Status == 400)
{
    Console.WriteLine($"Invalid configuration: {ex.Message}");
}
catch (RequestFailedException ex) when (ex.Status == 403)
{
    Console.WriteLine("Insufficient permissions or quota exceeded");
}
catch (RequestFailedException ex)
{
    Console.WriteLine($"ARM Error: {ex.Status} - {ex.ErrorCode}: {ex.Message}");
}
```

## Common Pitfalls

1. **Capacity names must be globally unique** — Fabric capacity names must be unique across all Azure subscriptions
2. **Suspend doesn't delete** — Suspended capacities still exist but don't bill for compute
3. **SKU changes may require downtime** — Scaling operations can take several minutes
4. **Admin UPNs must be valid** — Capacity administrators must be valid Azure AD users
5. **Location constraints** — Not all SKUs are available in all regions; use `GetSkusFabricCapacitiesAsync` to check
6. **Long provisioning times** — Capacity creation can take 5-15 minutes

## Related SDKs

| SDK | Purpose | Install |
|-----|---------|---------|
| `Azure.ResourceManager.Fabric` | Management plane (this SDK) | `dotnet add package Azure.ResourceManager.Fabric` |
| `Microsoft.Fabric.Api` | Data plane operations (beta) | `dotnet add package Microsoft.Fabric.Api --prerelease` |
| `Azure.ResourceManager` | Core ARM SDK | `dotnet add package Azure.ResourceManager` |
| `Azure.Identity` | Authentication | `dotnet add package Azure.Identity` |

## References

- [Azure.ResourceManager.Fabric NuGet](https://www.nuget.org/packages/Azure.ResourceManager.Fabric)
- [GitHub Source](https://github.com/Azure/azure-sdk-for-net/tree/main/sdk/fabric/Azure.ResourceManager.Fabric)
- [Microsoft Fabric Documentation](https://learn.microsoft.com/fabric/)
- [Fabric Capacity Management](https://learn.microsoft.com/fabric/admin/service-admin-portal-capacity-settings)

## When to Use
This skill is applicable to execute the workflow or actions described in the overview.

---

# Azure.ResourceManager.MongoDBAtlas SDK

Manage MongoDB Atlas Organizations as Azure ARM resources with unified billing through Azure Marketplace.

## Package Information

| Property | Value |
|----------|-------|
| Package | `Azure.ResourceManager.MongoDBAtlas` |
| Version | 1.0.0 (GA) |
| API Version | 2025-06-01 |
| Resource Type | `MongoDB.Atlas/organizations` |
| NuGet | [Azure.ResourceManager.MongoDBAtlas](https://www.nuget.org/packages/Azure.ResourceManager.MongoDBAtlas) |

## Installation

```bash
dotnet add package Azure.ResourceManager.MongoDBAtlas
dotnet add package Azure.Identity
dotnet add package Azure.ResourceManager
```

## Important Scope Limitation

This SDK manages **MongoDB Atlas Organizations as Azure ARM resources** for marketplace integration. It does NOT directly manage:
- Atlas clusters
- Databases
- Collections
- Users/roles

For cluster management, use the MongoDB Atlas API directly after creating the organization.

## Authentication

```csharp
using Azure.Identity;
using Azure.ResourceManager;
using Azure.ResourceManager.MongoDBAtlas;
using Azure.ResourceManager.MongoDBAtlas.Models;

// Create ARM client with DefaultAzureCredential
var credential = new DefaultAzureCredential();
var armClient = new ArmClient(credential);
```

## Core Types

| Type | Purpose |
|------|---------|
| `MongoDBAtlasOrganizationResource` | ARM resource representing an Atlas organization |
| `MongoDBAtlasOrganizationCollection` | Collection of organizations in a resource group |
| `MongoDBAtlasOrganizationData` | Data model for organization resource |
| `MongoDBAtlasOrganizationProperties` | Organization-specific properties |
| `MongoDBAtlasMarketplaceDetails` | Azure Marketplace subscription details |
| `MongoDBAtlasOfferDetails` | Marketplace offer configuration |
| `MongoDBAtlasUserDetails` | User information for the organization |
| `MongoDBAtlasPartnerProperties` | MongoDB-specific properties (org name, ID) |

## Workflows

### Get Organization Collection

```csharp
// Get resource group
var subscription = await armClient.GetDefaultSubscriptionAsync();
var resourceGroup = await subscription.GetResourceGroupAsync("my-resource-group");

// Get organizations collection
MongoDBAtlasOrganizationCollection organizations = 
    resourceGroup.Value.GetMongoDBAtlasOrganizations();
```

### Create Organization

```csharp
var organizationName = "my-atlas-org";
var location = AzureLocation.EastUS2;

// Build organization data
var organizationData = new MongoDBAtlasOrganizationData(location)
{
    Properties = new MongoDBAtlasOrganizationProperties(
        marketplace: new MongoDBAtlasMarketplaceDetails(
            subscriptionId: "your-azure-subscription-id",
            offerDetails: new MongoDBAtlasOfferDetails(
                publisherId: "mongodb",
                offerId: "mongodb_atlas_azure_native_prod",
                planId: "private_plan",
                planName: "Pay as You Go (Free) (Private)",
                termUnit: "P1M",
                termId: "gmz7xq9ge3py"
            )
        ),
        user: new MongoDBAtlasUserDetails(
            emailAddress: "admin@example.com",
            upn: "admin@example.com"
        )
        {
            FirstName = "Admin",
            LastName = "User"
        }
    )
    {
        PartnerProperties = new MongoDBAtlasPartnerProperties
        {
            OrganizationName = organizationName
        }
    },
    Tags = { ["Environment"] = "Production" }
};

// Create the organization (long-running operation)
var operation = await organizations.CreateOrUpdateAsync(
    WaitUntil.Completed,
    organizationName,
    organizationData
);

MongoDBAtlasOrganizationResource organization = operation.Value;
Console.WriteLine($"Created: {organization.Id}");
```

### Get Existing Organization

```csharp
// Option 1: From collection
MongoDBAtlasOrganizationResource org = 
    await organizations.GetAsync("my-atlas-org");

// Option 2: From resource identifier
var resourceId = MongoDBAtlasOrganizationResource.CreateResourceIdentifier(
    subscriptionId: "subscription-id",
    resourceGroupName: "my-resource-group",
    organizationName: "my-atlas-org"
);
MongoDBAtlasOrganizationResource org2 = 
    armClient.GetMongoDBAtlasOrganizationResource(resourceId);
await org2.GetAsync(); // Fetch data
```

### List Organizations

```csharp
// List in resource group
await foreach (var org in organizations.GetAllAsync())
{
    Console.WriteLine($"Org: {org.Data.Name}");
    Console.WriteLine($"  Location: {org.Data.Location}");
    Console.WriteLine($"  State: {org.Data.Properties?.ProvisioningState}");
}

// List across subscription
await foreach (var org in subscription.GetMongoDBAtlasOrganizationsAsync())
{
    Console.WriteLine($"Org: {org.Data.Name} in {org.Data.Id}");
}
```

### Update Tags

```csharp
// Add a single tag
await organization.AddTagAsync("CostCenter", "12345");

// Replace all tags
await organization.SetTagsAsync(new Dictionary<string, string>
{
    ["Environment"] = "Production",
    ["Team"] = "Platform"
});

// Remove a tag
await organization.RemoveTagAsync("OldTag");
```

### Update Organization Properties

```csharp
var patch = new MongoDBAtlasOrganizationPatch
{
    Tags = { ["UpdatedAt"] = DateTime.UtcNow.ToString("o") },
    Properties = new MongoDBAtlasOrganizationUpdateProperties
    {
        // Update user details if needed
        User = new MongoDBAtlasUserDetails(
            emailAddress: "newadmin@example.com",
            upn: "newadmin@example.com"
        )
    }
};

var updateOperation = await organization.UpdateAsync(
    WaitUntil.Completed,
    patch
);
```

### Delete Organization

```csharp
// Delete (long-running operation)
await organization.DeleteAsync(WaitUntil.Completed);
```

## Model Properties Reference

### MongoDBAtlasOrganizationProperties

| Property | Type | Description |
|----------|------|-------------|
| `Marketplace` | `MongoDBAtlasMarketplaceDetails` | Required. Marketplace subscription details |
| `User` | `MongoDBAtlasUserDetails` | Required. Organization admin user |
| `PartnerProperties` | `MongoDBAtlasPartnerProperties` | MongoDB-specific properties |
| `ProvisioningState` | `MongoDBAtlasResourceProvisioningState` | Read-only. Current provisioning state |

### MongoDBAtlasMarketplaceDetails

| Property | Type | Description |
|----------|------|-------------|
| `SubscriptionId` | `string` | Required. Azure subscription ID for billing |
| `OfferDetails` | `MongoDBAtlasOfferDetails` | Required. Marketplace offer configuration |
| `SubscriptionStatus` | `MarketplaceSubscriptionStatus` | Read-only. Subscription status |

### MongoDBAtlasOfferDetails

| Property | Type | Description |
|----------|------|-------------|
| `PublisherId` | `string` | Required. Publisher ID (typically "mongodb") |
| `OfferId` | `string` | Required. Offer ID |
| `PlanId` | `string` | Required. Plan ID |
| `PlanName` | `string` | Required. Display name of the plan |
| `TermUnit` | `string` | Required. Billing term unit (e.g., "P1M") |
| `TermId` | `string` | Required. Term identifier |

### MongoDBAtlasUserDetails

| Property | Type | Description |
|----------|------|-------------|
| `EmailAddress` | `string` | Required. User email address |
| `Upn` | `string` | Required. User principal name |
| `FirstName` | `string` | Optional. User first name |
| `LastName` | `string` | Optional. User last name |

### MongoDBAtlasPartnerProperties

| Property | Type | Description |
|----------|------|-------------|
| `OrganizationName` | `string` | Name of the MongoDB Atlas organization |
| `OrganizationId` | `string` | Read-only. MongoDB Atlas organization ID |

## Provisioning States

| State | Description |
|-------|-------------|
| `Succeeded` | Resource provisioned successfully |
| `Failed` | Provisioning failed |
| `Canceled` | Provisioning was canceled |
| `Provisioning` | Resource is being provisioned |
| `Updating` | Resource is being updated |
| `Deleting` | Resource is being deleted |
| `Accepted` | Request accepted, provisioning starting |

## Marketplace Subscription Status

| Status | Description |
|--------|-------------|
| `PendingFulfillmentStart` | Subscription pending activation |
| `Subscribed` | Active subscription |
| `Suspended` | Subscription suspended |
| `Unsubscribed` | Subscription canceled |

## Best Practices

### Use Async Methods

```csharp
// Prefer async for all operations
var org = await organizations.GetAsync("my-org");
await org.Value.AddTagAsync("key", "value");
```

### Handle Long-Running Operations

```csharp
// Wait for completion
var operation = await organizations.CreateOrUpdateAsync(
    WaitUntil.Completed,  // Blocks until done
    name,
    data
);

// Or start and poll later
var operation = await organizations.CreateOrUpdateAsync(
    WaitUntil.Started,  // Returns immediately
    name,
    data
);

// Poll for completion
while (!operation.HasCompleted)
{
    await Task.Delay(TimeSpan.FromSeconds(5));
    await operation.UpdateStatusAsync();
}
```

### Check Provisioning State

```csharp
var org = await organizations.GetAsync("my-org");
if (org.Value.Data.Properties?.ProvisioningState == 
    MongoDBAtlasResourceProvisioningState.Succeeded)
{
    Console.WriteLine("Organization is ready");
}
```

### Use Resource Identifiers

```csharp
// Create identifier without API call
var resourceId = MongoDBAtlasOrganizationResource.CreateResourceIdentifier(
    subscriptionId,
    resourceGroupName,
    organizationName
);

// Get resource handle (no data yet)
var orgResource = armClient.GetMongoDBAtlasOrganizationResource(resourceId);

// Fetch data when needed
var response = await orgResource.GetAsync();
```

## Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| `ResourceNotFound` | Organization doesn't exist | Verify name and resource group |
| `AuthorizationFailed` | Insufficient permissions | Check RBAC roles on resource group |
| `InvalidParameter` | Missing required properties | Ensure all required fields are set |
| `MarketplaceError` | Marketplace subscription issue | Verify offer details and subscription |

## Related Resources

- [Microsoft Learn: MongoDB Atlas on Azure](https://learn.microsoft.com/en-us/azure/partner-solutions/mongodb-atlas/)
- [API Reference](https://learn.microsoft.com/en-us/dotnet/api/azure.resourcemanager.mongodbatlas)
- [Azure SDK for .NET](https://github.com/Azure/azure-sdk-for-net/tree/main/sdk/mongodbatlas)

## When to Use
This skill is applicable to execute the workflow or actions described in the overview.

---

# Azure Fabric Management SDK for Python

Manage Microsoft Fabric capacities and resources programmatically.

## Installation

```bash
pip install azure-mgmt-fabric
pip install azure-identity
```

## Environment Variables

```bash
AZURE_SUBSCRIPTION_ID=<your-subscription-id>
AZURE_RESOURCE_GROUP=<your-resource-group>
```

## Authentication

```python
from azure.identity import DefaultAzureCredential
from azure.mgmt.fabric import FabricMgmtClient
import os

credential = DefaultAzureCredential()
client = FabricMgmtClient(
    credential=credential,
    subscription_id=os.environ["AZURE_SUBSCRIPTION_ID"]
)
```

## Create Fabric Capacity

```python
from azure.mgmt.fabric import FabricMgmtClient
from azure.mgmt.fabric.models import FabricCapacity, FabricCapacityProperties, CapacitySku
from azure.identity import DefaultAzureCredential
import os

credential = DefaultAzureCredential()
client = FabricMgmtClient(
    credential=credential,
    subscription_id=os.environ["AZURE_SUBSCRIPTION_ID"]
)

resource_group = os.environ["AZURE_RESOURCE_GROUP"]
capacity_name = "myfabriccapacity"

capacity = client.fabric_capacities.begin_create_or_update(
    resource_group_name=resource_group,
    capacity_name=capacity_name,
    resource=FabricCapacity(
        location="eastus",
        sku=CapacitySku(
            name="F2",  # Fabric SKU
            tier="Fabric"
        ),
        properties=FabricCapacityProperties(
            administration=FabricCapacityAdministration(
                members=["user@contoso.com"]
            )
        )
    )
).result()

print(f"Capacity created: {capacity.name}")
```

## Get Capacity Details

```python
capacity = client.fabric_capacities.get(
    resource_group_name=resource_group,
    capacity_name=capacity_name
)

print(f"Capacity: {capacity.name}")
print(f"SKU: {capacity.sku.name}")
print(f"State: {capacity.properties.state}")
print(f"Location: {capacity.location}")
```

## List Capacities in Resource Group

```python
capacities = client.fabric_capacities.list_by_resource_group(
    resource_group_name=resource_group
)

for capacity in capacities:
    print(f"Capacity: {capacity.name} - SKU: {capacity.sku.name}")
```

## List All Capacities in Subscription

```python
all_capacities = client.fabric_capacities.list_by_subscription()

for capacity in all_capacities:
    print(f"Capacity: {capacity.name} in {capacity.location}")
```

## Update Capacity

```python
from azure.mgmt.fabric.models import FabricCapacityUpdate, CapacitySku

updated = client.fabric_capacities.begin_update(
    resource_group_name=resource_group,
    capacity_name=capacity_name,
    properties=FabricCapacityUpdate(
        sku=CapacitySku(
            name="F4",  # Scale up
            tier="Fabric"
        ),
        tags={"environment": "production"}
    )
).result()

print(f"Updated SKU: {updated.sku.name}")
```

## Suspend Capacity

Pause capacity to stop billing:

```python
client.fabric_capacities.begin_suspend(
    resource_group_name=resource_group,
    capacity_name=capacity_name
).result()

print("Capacity suspended")
```

## Resume Capacity

Resume a paused capacity:

```python
client.fabric_capacities.begin_resume(
    resource_group_name=resource_group,
    capacity_name=capacity_name
).result()

print("Capacity resumed")
```

## Delete Capacity

```python
client.fabric_capacities.begin_delete(
    resource_group_name=resource_group,
    capacity_name=capacity_name
).result()

print("Capacity deleted")
```

## Check Name Availability

```python
from azure.mgmt.fabric.models import CheckNameAvailabilityRequest

result = client.fabric_capacities.check_name_availability(
    location="eastus",
    body=CheckNameAvailabilityRequest(
        name="my-new-capacity",
        type="Microsoft.Fabric/capacities"
    )
)

if result.name_available:
    print("Name is available")
else:
    print(f"Name not available: {result.reason}")
```

## List Available SKUs

```python
skus = client.fabric_capacities.list_skus(
    resource_group_name=resource_group,
    capacity_name=capacity_name
)

for sku in skus:
    print(f"SKU: {sku.name} - Tier: {sku.tier}")
```

## Client Operations

| Operation | Method |
|-----------|--------|
| `client.fabric_capacities` | Capacity CRUD operations |
| `client.operations` | List available operations |

## Fabric SKUs

| SKU | Description | CUs |
|-----|-------------|-----|
| `F2` | Entry level | 2 Capacity Units |
| `F4` | Small | 4 Capacity Units |
| `F8` | Medium | 8 Capacity Units |
| `F16` | Large | 16 Capacity Units |
| `F32` | X-Large | 32 Capacity Units |
| `F64` | 2X-Large | 64 Capacity Units |
| `F128` | 4X-Large | 128 Capacity Units |
| `F256` | 8X-Large | 256 Capacity Units |
| `F512` | 16X-Large | 512 Capacity Units |
| `F1024` | 32X-Large | 1024 Capacity Units |
| `F2048` | 64X-Large | 2048 Capacity Units |

## Capacity States

| State | Description |
|-------|-------------|
| `Active` | Capacity is running |
| `Paused` | Capacity is suspended (no billing) |
| `Provisioning` | Being created |
| `Updating` | Being modified |
| `Deleting` | Being removed |
| `Failed` | Operation failed |

## Long-Running Operations

All mutating operations are long-running (LRO). Use `.result()` to wait:

```python
# Synchronous wait
capacity = client.fabric_capacities.begin_create_or_update(...).result()

# Or poll manually
poller = client.fabric_capacities.begin_create_or_update(...)
while not poller.done():
    print(f"Status: {poller.status()}")
    time.sleep(5)
capacity = poller.result()
```

## Best Practices

1. **Use DefaultAzureCredential** for authentication
2. **Suspend unused capacities** to reduce costs
3. **Start with smaller SKUs** and scale up as needed
4. **Use tags** for cost tracking and organization
5. **Check name availability** before creating capacities
6. **Handle LRO properly** — don't assume immediate completion
7. **Set up capacity admins** — specify users who can manage workspaces
8. **Monitor capacity usage** via Azure Monitor metrics

## When to Use
This skill is applicable to execute the workflow or actions described in the overview.

---

# Azure API Management SDK for Python

Manage Azure API Management services, APIs, products, and policies.

## Installation

```bash
pip install azure-mgmt-apimanagement
pip install azure-identity
```

## Environment Variables

```bash
AZURE_SUBSCRIPTION_ID=your-subscription-id
```

## Authentication

```python
from azure.identity import DefaultAzureCredential
from azure.mgmt.apimanagement import ApiManagementClient
import os

client = ApiManagementClient(
    credential=DefaultAzureCredential(),
    subscription_id=os.environ["AZURE_SUBSCRIPTION_ID"]
)
```

## Create APIM Service

```python
from azure.mgmt.apimanagement.models import (
    ApiManagementServiceResource,
    ApiManagementServiceSkuProperties,
    SkuType
)

service = client.api_management_service.begin_create_or_update(
    resource_group_name="my-resource-group",
    service_name="my-apim",
    parameters=ApiManagementServiceResource(
        location="eastus",
        publisher_email="admin@example.com",
        publisher_name="My Organization",
        sku=ApiManagementServiceSkuProperties(
            name=SkuType.DEVELOPER,
            capacity=1
        )
    )
).result()

print(f"Created APIM: {service.name}")
```

## Import API from OpenAPI

```python
from azure.mgmt.apimanagement.models import (
    ApiCreateOrUpdateParameter,
    ContentFormat,
    Protocol
)

api = client.api.begin_create_or_update(
    resource_group_name="my-resource-group",
    service_name="my-apim",
    api_id="my-api",
    parameters=ApiCreateOrUpdateParameter(
        display_name="My API",
        path="myapi",
        protocols=[Protocol.HTTPS],
        format=ContentFormat.OPENAPI_JSON,
        value='{"openapi": "3.0.0", "info": {"title": "My API", "version": "1.0"}, "paths": {"/health": {"get": {"responses": {"200": {"description": "OK"}}}}}}'
    )
).result()

print(f"Imported API: {api.display_name}")
```

## Import API from URL

```python
api = client.api.begin_create_or_update(
    resource_group_name="my-resource-group",
    service_name="my-apim",
    api_id="petstore",
    parameters=ApiCreateOrUpdateParameter(
        display_name="Petstore API",
        path="petstore",
        protocols=[Protocol.HTTPS],
        format=ContentFormat.OPENAPI_LINK,
        value="https://petstore.swagger.io/v2/swagger.json"
    )
).result()
```

## List APIs

```python
apis = client.api.list_by_service(
    resource_group_name="my-resource-group",
    service_name="my-apim"
)

for api in apis:
    print(f"{api.name}: {api.display_name} - {api.path}")
```

## Create Product

```python
from azure.mgmt.apimanagement.models import ProductContract

product = client.product.create_or_update(
    resource_group_name="my-resource-group",
    service_name="my-apim",
    product_id="premium",
    parameters=ProductContract(
        display_name="Premium",
        description="Premium tier with unlimited access",
        subscription_required=True,
        approval_required=False,
        state="published"
    )
)

print(f"Created product: {product.display_name}")
```

## Add API to Product

```python
client.product_api.create_or_update(
    resource_group_name="my-resource-group",
    service_name="my-apim",
    product_id="premium",
    api_id="my-api"
)
```

## Create Subscription

```python
from azure.mgmt.apimanagement.models import SubscriptionCreateParameters

subscription = client.subscription.create_or_update(
    resource_group_name="my-resource-group",
    service_name="my-apim",
    sid="my-subscription",
    parameters=SubscriptionCreateParameters(
        display_name="My Subscription",
        scope=f"/products/premium",
        state="active"
    )
)

print(f"Subscription key: {subscription.primary_key}")
```

## Set API Policy

```python
from azure.mgmt.apimanagement.models import PolicyContract

policy_xml = """
<policies>
    <inbound>
        <rate-limit calls="100" renewal-period="60" />
        <set-header name="X-Custom-Header" exists-action="override">
            <value>CustomValue</value>
        </set-header>
    </inbound>
    <backend>
        <forward-request />
    </backend>
    <outbound />
    <on-error />
</policies>
"""

client.api_policy.create_or_update(
    resource_group_name="my-resource-group",
    service_name="my-apim",
    api_id="my-api",
    policy_id="policy",
    parameters=PolicyContract(
        value=policy_xml,
        format="xml"
    )
)
```

## Create Named Value (Secret)

```python
from azure.mgmt.apimanagement.models import NamedValueCreateContract

named_value = client.named_value.begin_create_or_update(
    resource_group_name="my-resource-group",
    service_name="my-apim",
    named_value_id="backend-api-key",
    parameters=NamedValueCreateContract(
        display_name="Backend API Key",
        value="secret-key-value",
        secret=True
    )
).result()
```

## Create Backend

```python
from azure.mgmt.apimanagement.models import BackendContract

backend = client.backend.create_or_update(
    resource_group_name="my-resource-group",
    service_name="my-apim",
    backend_id="my-backend",
    parameters=BackendContract(
        url="https://api.backend.example.com",
        protocol="http",
        description="My backend service"
    )
)
```

## Create User

```python
from azure.mgmt.apimanagement.models import UserCreateParameters

user = client.user.create_or_update(
    resource_group_name="my-resource-group",
    service_name="my-apim",
    user_id="newuser",
    parameters=UserCreateParameters(
        email="user@example.com",
        first_name="John",
        last_name="Doe"
    )
)
```

## Operation Groups

| Group | Purpose |
|-------|---------|
| `api_management_service` | APIM instance management |
| `api` | API operations |
| `api_operation` | API operation details |
| `api_policy` | API-level policies |
| `product` | Product management |
| `product_api` | Product-API associations |
| `subscription` | Subscription management |
| `user` | User management |
| `named_value` | Named values/secrets |
| `backend` | Backend services |
| `certificate` | Certificates |
| `gateway` | Self-hosted gateways |

## Best Practices

1. **Use named values** for secrets and configuration
2. **Apply policies** at appropriate scopes (global, product, API, operation)
3. **Use products** to bundle APIs and manage access
4. **Enable Application Insights** for monitoring
5. **Use backends** to abstract backend services
6. **Version your APIs** using APIM's versioning features

## When to Use
This skill is applicable to execute the workflow or actions described in the overview.

---

# Azure.ResourceManager.ApplicationInsights (.NET)

Azure Resource Manager SDK for managing Application Insights resources for application performance monitoring.

## Installation

```bash
dotnet add package Azure.ResourceManager.ApplicationInsights
dotnet add package Azure.Identity
```

**Current Version**: v1.0.0 (GA)  
**API Version**: 2022-06-15

## Environment Variables

```bash
AZURE_SUBSCRIPTION_ID=<your-subscription-id>
AZURE_RESOURCE_GROUP=<your-resource-group>
AZURE_APPINSIGHTS_NAME=<your-appinsights-component>
```

## Authentication

```csharp
using Azure.Identity;
using Azure.ResourceManager;
using Azure.ResourceManager.ApplicationInsights;

ArmClient client = new ArmClient(new DefaultAzureCredential());
```

## Resource Hierarchy

```
Subscription
└── ResourceGroup
    └── ApplicationInsightsComponent          # App Insights resource
        ├── ApplicationInsightsComponentApiKey  # API keys for programmatic access
        ├── ComponentLinkedStorageAccount      # Linked storage for data export
        └── (via component ID)
            ├── WebTest                        # Availability tests
            ├── Workbook                       # Workbooks for analysis
            ├── WorkbookTemplate               # Workbook templates
            └── MyWorkbook                     # Private workbooks
```

## Core Workflows

### 1. Create Application Insights Component (Workspace-based)

```csharp
using Azure.ResourceManager.ApplicationInsights;
using Azure.ResourceManager.ApplicationInsights.Models;

ResourceGroupResource resourceGroup = await client
    .GetDefaultSubscriptionAsync()
    .Result
    .GetResourceGroupAsync("my-resource-group");

ApplicationInsightsComponentCollection components = resourceGroup.GetApplicationInsightsComponents();

// Workspace-based Application Insights (recommended)
ApplicationInsightsComponentData data = new ApplicationInsightsComponentData(
    AzureLocation.EastUS,
    ApplicationInsightsApplicationType.Web)
{
    Kind = "web",
    WorkspaceResourceId = new ResourceIdentifier(
        "/subscriptions/<sub-id>/resourceGroups/<rg>/providers/Microsoft.OperationalInsights/workspaces/<workspace-name>"),
    IngestionMode = IngestionMode.LogAnalytics,
    PublicNetworkAccessForIngestion = PublicNetworkAccessType.Enabled,
    PublicNetworkAccessForQuery = PublicNetworkAccessType.Enabled,
    RetentionInDays = 90,
    SamplingPercentage = 100,
    DisableIPMasking = false,
    ImmediatePurgeDataOn30Days = false,
    Tags =
    {
        { "environment", "production" },
        { "application", "mywebapp" }
    }
};

ArmOperation<ApplicationInsightsComponentResource> operation = await components
    .CreateOrUpdateAsync(WaitUntil.Completed, "my-appinsights", data);

ApplicationInsightsComponentResource component = operation.Value;

Console.WriteLine($"Component created: {component.Data.Name}");
Console.WriteLine($"Instrumentation Key: {component.Data.InstrumentationKey}");
Console.WriteLine($"Connection String: {component.Data.ConnectionString}");
```

### 2. Get Connection String and Keys

```csharp
ApplicationInsightsComponentResource component = await resourceGroup
    .GetApplicationInsightsComponentAsync("my-appinsights");

// Get connection string for SDK configuration
string connectionString = component.Data.ConnectionString;
string instrumentationKey = component.Data.InstrumentationKey;
string appId = component.Data.AppId;

Console.WriteLine($"Connection String: {connectionString}");
Console.WriteLine($"Instrumentation Key: {instrumentationKey}");
Console.WriteLine($"App ID: {appId}");
```

### 3. Create API Key

```csharp
ApplicationInsightsComponentResource component = await resourceGroup
    .GetApplicationInsightsComponentAsync("my-appinsights");

ApplicationInsightsComponentApiKeyCollection apiKeys = component.GetApplicationInsightsComponentApiKeys();

// API key for reading telemetry
ApplicationInsightsApiKeyContent keyContent = new ApplicationInsightsApiKeyContent
{
    Name = "ReadTelemetryKey",
    LinkedReadProperties =
    {
        $"/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/microsoft.insights/components/{component.Data.Name}/api",
        $"/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/microsoft.insights/components/{component.Data.Name}/agentconfig"
    }
};

ApplicationInsightsComponentApiKeyResource apiKey = await apiKeys
    .CreateOrUpdateAsync(WaitUntil.Completed, keyContent);

Console.WriteLine($"API Key Name: {apiKey.Data.Name}");
Console.WriteLine($"API Key: {apiKey.Data.ApiKey}"); // Only shown once!
```

### 4. Create Web Test (Availability Test)

```csharp
WebTestCollection webTests = resourceGroup.GetWebTests();

// URL Ping Test
WebTestData urlPingTest = new WebTestData(AzureLocation.EastUS)
{
    Kind = WebTestKind.Ping,
    SyntheticMonitorId = "webtest-ping-myapp",
    WebTestName = "Homepage Availability",
    Description = "Checks if homepage is available",
    IsEnabled = true,
    Frequency = 300, // 5 minutes
    Timeout = 120,   // 2 minutes
    WebTestKind = WebTestKind.Ping,
    IsRetryEnabled = true,
    Locations =
    {
        new WebTestGeolocation { WebTestLocationId = "us-ca-sjc-azr" },  // West US
        new WebTestGeolocation { WebTestLocationId = "us-tx-sn1-azr" },  // South Central US
        new WebTestGeolocation { WebTestLocationId = "us-il-ch1-azr" },  // North Central US
        new WebTestGeolocation { WebTestLocationId = "emea-gb-db3-azr" }, // UK South
        new WebTestGeolocation { WebTestLocationId = "apac-sg-sin-azr" }  // Southeast Asia
    },
    Configuration = new WebTestConfiguration
    {
        WebTest = """
            <WebTest Name="Homepage" Enabled="True" Timeout="120" 
                     xmlns="http://microsoft.com/schemas/VisualStudio/TeamTest/2010">
                <Items>
                    <Request Method="GET" Version="1.1" Url="https://myapp.example.com" 
                             ThinkTime="0" Timeout="120" ParseDependentRequests="False" 
                             FollowRedirects="True" RecordResult="True" Cache="False" 
                             ResponseTimeGoal="0" Encoding="utf-8" ExpectedHttpStatusCode="200" />
                </Items>
            </WebTest>
        """
    },
    Tags =
    {
        { $"hidden-link:/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/microsoft.insights/components/my-appinsights", "Resource" }
    }
};

ArmOperation<WebTestResource> operation = await webTests
    .CreateOrUpdateAsync(WaitUntil.Completed, "webtest-homepage", urlPingTest);

WebTestResource webTest = operation.Value;
Console.WriteLine($"Web test created: {webTest.Data.Name}");
```

### 5. Create Multi-Step Web Test

```csharp
WebTestData multiStepTest = new WebTestData(AzureLocation.EastUS)
{
    Kind = WebTestKind.MultiStep,
    SyntheticMonitorId = "webtest-multistep-login",
    WebTestName = "Login Flow Test",
    Description = "Tests login functionality",
    IsEnabled = true,
    Frequency = 900, // 15 minutes
    Timeout = 300,   // 5 minutes
    WebTestKind = WebTestKind.MultiStep,
    IsRetryEnabled = true,
    Locations =
    {
        new WebTestGeolocation { WebTestLocationId = "us-ca-sjc-azr" }
    },
    Configuration = new WebTestConfiguration
    {
        WebTest = """
            <WebTest Name="LoginFlow" Enabled="True" Timeout="300"
                     xmlns="http://microsoft.com/schemas/VisualStudio/TeamTest/2010">
                <Items>
                    <Request Method="GET" Version="1.1" Url="https://myapp.example.com/login" 
                             ThinkTime="0" Timeout="60" />
                    <Request Method="POST" Version="1.1" Url="https://myapp.example.com/api/auth" 
                             ThinkTime="0" Timeout="60">
                        <Headers>
                            <Header Name="Content-Type" Value="application/json" />
                        </Headers>
                        <Body>{"username":"testuser","password":"{{TestPassword}}"}</Body>
                    </Request>
                </Items>
            </WebTest>
        """
    },
    Tags =
    {
        { $"hidden-link:/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/microsoft.insights/components/my-appinsights", "Resource" }
    }
};

await webTests.CreateOrUpdateAsync(WaitUntil.Completed, "webtest-login-flow", multiStepTest);
```

### 6. Create Workbook

```csharp
WorkbookCollection workbooks = resourceGroup.GetWorkbooks();

WorkbookData workbookData = new WorkbookData(AzureLocation.EastUS)
{
    DisplayName = "Application Performance Dashboard",
    Category = "workbook",
    Kind = WorkbookSharedTypeKind.Shared,
    SerializedData = """
    {
        "version": "Notebook/1.0",
        "items": [
            {
                "type": 1,
                "content": {
                    "json": "# Application Performance\n\nThis workbook shows application performance metrics."
                },
                "name": "header"
            },
            {
                "type": 3,
                "content": {
                    "version": "KqlItem/1.0",
                    "query": "requests\n| summarize count() by bin(timestamp, 1h)\n| render timechart",
                    "size": 0,
                    "title": "Requests per Hour",
                    "timeContext": {
                        "durationMs": 86400000
                    },
                    "queryType": 0,
                    "resourceType": "microsoft.insights/components"
                },
                "name": "requestsChart"
            }
        ],
        "isLocked": false
    }
    """,
    SourceId = component.Id,
    Tags =
    {
        { "environment", "production" }
    }
};

// Note: Workbook ID should be a new GUID
string workbookId = Guid.NewGuid().ToString();

ArmOperation<WorkbookResource> operation = await workbooks
    .CreateOrUpdateAsync(WaitUntil.Completed, workbookId, workbookData);

WorkbookResource workbook = operation.Value;
Console.WriteLine($"Workbook created: {workbook.Data.DisplayName}");
```

### 7. Link Storage Account

```csharp
ApplicationInsightsComponentResource component = await resourceGroup
    .GetApplicationInsightsComponentAsync("my-appinsights");

ComponentLinkedStorageAccountCollection linkedStorage = component.GetComponentLinkedStorageAccounts();

ComponentLinkedStorageAccountData storageData = new ComponentLinkedStorageAccountData
{
    LinkedStorageAccount = new ResourceIdentifier(
        "/subscriptions/<sub-id>/resourceGroups/<rg>/providers/Microsoft.Storage/storageAccounts/<storage-account>")
};

ArmOperation<ComponentLinkedStorageAccountResource> operation = await linkedStorage
    .CreateOrUpdateAsync(WaitUntil.Completed, StorageType.ServiceProfiler, storageData);
```

### 8. List and Manage Components

```csharp
// List all Application Insights components in resource group
await foreach (ApplicationInsightsComponentResource component in 
    resourceGroup.GetApplicationInsightsComponents())
{
    Console.WriteLine($"Component: {component.Data.Name}");
    Console.WriteLine($"  App ID: {component.Data.AppId}");
    Console.WriteLine($"  Type: {component.Data.ApplicationType}");
    Console.WriteLine($"  Ingestion Mode: {component.Data.IngestionMode}");
    Console.WriteLine($"  Retention: {component.Data.RetentionInDays} days");
}

// List web tests
await foreach (WebTestResource webTest in resourceGroup.GetWebTests())
{
    Console.WriteLine($"Web Test: {webTest.Data.WebTestName}");
    Console.WriteLine($"  Enabled: {webTest.Data.IsEnabled}");
    Console.WriteLine($"  Frequency: {webTest.Data.Frequency}s");
}

// List workbooks
await foreach (WorkbookResource workbook in resourceGroup.GetWorkbooks())
{
    Console.WriteLine($"Workbook: {workbook.Data.DisplayName}");
}
```

### 9. Update Component

```csharp
ApplicationInsightsComponentResource component = await resourceGroup
    .GetApplicationInsightsComponentAsync("my-appinsights");

// Update using full data (PUT operation)
ApplicationInsightsComponentData updateData = component.Data;
updateData.RetentionInDays = 180;
updateData.SamplingPercentage = 50;
updateData.Tags["updated"] = "true";

ArmOperation<ApplicationInsightsComponentResource> operation = await resourceGroup
    .GetApplicationInsightsComponents()
    .CreateOrUpdateAsync(WaitUntil.Completed, "my-appinsights", updateData);
```

### 10. Delete Resources

```csharp
// Delete Application Insights component
ApplicationInsightsComponentResource component = await resourceGroup
    .GetApplicationInsightsComponentAsync("my-appinsights");
await component.DeleteAsync(WaitUntil.Completed);

// Delete web test
WebTestResource webTest = await resourceGroup.GetWebTestAsync("webtest-homepage");
await webTest.DeleteAsync(WaitUntil.Completed);
```

## Key Types Reference

| Type | Purpose |
|------|---------|
| `ApplicationInsightsComponentResource` | App Insights component |
| `ApplicationInsightsComponentData` | Component configuration |
| `ApplicationInsightsComponentCollection` | Collection of components |
| `ApplicationInsightsComponentApiKeyResource` | API key for programmatic access |
| `WebTestResource` | Availability/web test |
| `WebTestData` | Web test configuration |
| `WorkbookResource` | Analysis workbook |
| `WorkbookData` | Workbook configuration |
| `ComponentLinkedStorageAccountResource` | Linked storage for exports |

## Application Types

| Type | Enum Value |
|------|------------|
| Web Application | `Web` |
| iOS Application | `iOS` |
| Java Application | `Java` |
| Node.js Application | `NodeJS` |
| .NET Application | `MRT` |
| Other | `Other` |

## Web Test Locations

| Location ID | Region |
|-------------|--------|
| `us-ca-sjc-azr` | West US |
| `us-tx-sn1-azr` | South Central US |
| `us-il-ch1-azr` | North Central US |
| `us-va-ash-azr` | East US |
| `emea-gb-db3-azr` | UK South |
| `emea-nl-ams-azr` | West Europe |
| `emea-fr-pra-edge` | France Central |
| `apac-sg-sin-azr` | Southeast Asia |
| `apac-hk-hkn-azr` | East Asia |
| `apac-jp-kaw-edge` | Japan East |
| `latam-br-gru-edge` | Brazil South |
| `emea-au-syd-edge` | Australia East |

## Best Practices

1. **Use workspace-based** — Workspace-based App Insights is the current standard
2. **Link to Log Analytics** — Store data in Log Analytics for better querying
3. **Set appropriate retention** — Balance cost vs. data availability
4. **Use sampling** — Reduce costs for high-volume applications
5. **Store connection string securely** — Use Key Vault or managed identity
6. **Enable multiple test locations** — For accurate availability monitoring
7. **Use workbooks** — For custom dashboards and analysis
8. **Set up alerts** — Based on availability tests and metrics
9. **Tag resources** — For cost allocation and organization
10. **Use private endpoints** — For secure data ingestion

## Error Handling

```csharp
using Azure;

try
{
    ArmOperation<ApplicationInsightsComponentResource> operation = await components
        .CreateOrUpdateAsync(WaitUntil.Completed, "my-appinsights", data);
}
catch (RequestFailedException ex) when (ex.Status == 409)
{
    Console.WriteLine("Component already exists");
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

## SDK Integration

Use the connection string with Application Insights SDK:

```csharp
// Program.cs in ASP.NET Core
builder.Services.AddApplicationInsightsTelemetry(options =>
{
    options.ConnectionString = configuration["ApplicationInsights:ConnectionString"];
});

// Or set via environment variable
// APPLICATIONINSIGHTS_CONNECTION_STRING=InstrumentationKey=...;IngestionEndpoint=...
```

## Related SDKs

| SDK | Purpose | Install |
|-----|---------|---------|
| `Azure.ResourceManager.ApplicationInsights` | Resource management (this SDK) | `dotnet add package Azure.ResourceManager.ApplicationInsights` |
| `Microsoft.ApplicationInsights` | Telemetry SDK | `dotnet add package Microsoft.ApplicationInsights` |
| `Microsoft.ApplicationInsights.AspNetCore` | ASP.NET Core integration | `dotnet add package Microsoft.ApplicationInsights.AspNetCore` |
| `Azure.Monitor.OpenTelemetry.Exporter` | OpenTelemetry export | `dotnet add package Azure.Monitor.OpenTelemetry.Exporter` |

## Reference Links

| Resource | URL |
|----------|-----|
| NuGet Package | https://www.nuget.org/packages/Azure.ResourceManager.ApplicationInsights |
| API Reference | https://learn.microsoft.com/dotnet/api/azure.resourcemanager.applicationinsights |
| Product Documentation | https://learn.microsoft.com/azure/azure-monitor/app/app-insights-overview |
| GitHub Source | https://github.com/Azure/azure-sdk-for-net/tree/main/sdk/applicationinsights/Azure.ResourceManager.ApplicationInsights |

## When to Use
This skill is applicable to execute the workflow or actions described in the overview.

---

# Azure API Center Management SDK for Python

Manage API inventory, metadata, and governance in Azure API Center.

## Installation

```bash
pip install azure-mgmt-apicenter
pip install azure-identity
```

## Environment Variables

```bash
AZURE_SUBSCRIPTION_ID=your-subscription-id
```

## Authentication

```python
from azure.identity import DefaultAzureCredential
from azure.mgmt.apicenter import ApiCenterMgmtClient
import os

client = ApiCenterMgmtClient(
    credential=DefaultAzureCredential(),
    subscription_id=os.environ["AZURE_SUBSCRIPTION_ID"]
)
```

## Create API Center

```python
from azure.mgmt.apicenter.models import Service

api_center = client.services.create_or_update(
    resource_group_name="my-resource-group",
    service_name="my-api-center",
    resource=Service(
        location="eastus",
        tags={"environment": "production"}
    )
)

print(f"Created API Center: {api_center.name}")
```

## List API Centers

```python
api_centers = client.services.list_by_subscription()

for api_center in api_centers:
    print(f"{api_center.name} - {api_center.location}")
```

## Register an API

```python
from azure.mgmt.apicenter.models import Api, ApiKind, LifecycleStage

api = client.apis.create_or_update(
    resource_group_name="my-resource-group",
    service_name="my-api-center",
    workspace_name="default",
    api_name="my-api",
    resource=Api(
        title="My API",
        description="A sample API for demonstration",
        kind=ApiKind.REST,
        lifecycle_stage=LifecycleStage.PRODUCTION,
        terms_of_service={"url": "https://example.com/terms"},
        contacts=[{"name": "API Team", "email": "api-team@example.com"}]
    )
)

print(f"Registered API: {api.title}")
```

## Create API Version

```python
from azure.mgmt.apicenter.models import ApiVersion, LifecycleStage

version = client.api_versions.create_or_update(
    resource_group_name="my-resource-group",
    service_name="my-api-center",
    workspace_name="default",
    api_name="my-api",
    version_name="v1",
    resource=ApiVersion(
        title="Version 1.0",
        lifecycle_stage=LifecycleStage.PRODUCTION
    )
)

print(f"Created version: {version.title}")
```

## Add API Definition

```python
from azure.mgmt.apicenter.models import ApiDefinition

definition = client.api_definitions.create_or_update(
    resource_group_name="my-resource-group",
    service_name="my-api-center",
    workspace_name="default",
    api_name="my-api",
    version_name="v1",
    definition_name="openapi",
    resource=ApiDefinition(
        title="OpenAPI Definition",
        description="OpenAPI 3.0 specification"
    )
)
```

## Import API Specification

```python
from azure.mgmt.apicenter.models import ApiSpecImportRequest, ApiSpecImportSourceFormat

# Import from inline content
client.api_definitions.import_specification(
    resource_group_name="my-resource-group",
    service_name="my-api-center",
    workspace_name="default",
    api_name="my-api",
    version_name="v1",
    definition_name="openapi",
    body=ApiSpecImportRequest(
        format=ApiSpecImportSourceFormat.INLINE,
        value='{"openapi": "3.0.0", "info": {"title": "My API", "version": "1.0"}, "paths": {}}'
    )
)
```

## List APIs

```python
apis = client.apis.list(
    resource_group_name="my-resource-group",
    service_name="my-api-center",
    workspace_name="default"
)

for api in apis:
    print(f"{api.name}: {api.title} ({api.kind})")
```

## Create Environment

```python
from azure.mgmt.apicenter.models import Environment, EnvironmentKind

environment = client.environments.create_or_update(
    resource_group_name="my-resource-group",
    service_name="my-api-center",
    workspace_name="default",
    environment_name="production",
    resource=Environment(
        title="Production",
        description="Production environment",
        kind=EnvironmentKind.PRODUCTION,
        server={"type": "Azure API Management", "management_portal_uri": ["https://portal.azure.com"]}
    )
)
```

## Create Deployment

```python
from azure.mgmt.apicenter.models import Deployment, DeploymentState

deployment = client.deployments.create_or_update(
    resource_group_name="my-resource-group",
    service_name="my-api-center",
    workspace_name="default",
    api_name="my-api",
    deployment_name="prod-deployment",
    resource=Deployment(
        title="Production Deployment",
        description="Deployed to production APIM",
        environment_id="/workspaces/default/environments/production",
        definition_id="/workspaces/default/apis/my-api/versions/v1/definitions/openapi",
        state=DeploymentState.ACTIVE,
        server={"runtime_uri": ["https://api.example.com"]}
    )
)
```

## Define Custom Metadata

```python
from azure.mgmt.apicenter.models import MetadataSchema

metadata = client.metadata_schemas.create_or_update(
    resource_group_name="my-resource-group",
    service_name="my-api-center",
    metadata_schema_name="data-classification",
    resource=MetadataSchema(
        schema='{"type": "string", "title": "Data Classification", "enum": ["public", "internal", "confidential"]}'
    )
)
```

## Client Types

| Client | Purpose |
|--------|---------|
| `ApiCenterMgmtClient` | Main client for all operations |

## Operations

| Operation Group | Purpose |
|----------------|---------|
| `services` | API Center service management |
| `workspaces` | Workspace management |
| `apis` | API registration and management |
| `api_versions` | API version management |
| `api_definitions` | API definition management |
| `deployments` | Deployment tracking |
| `environments` | Environment management |
| `metadata_schemas` | Custom metadata definitions |

## Best Practices

1. **Use workspaces** to organize APIs by team or domain
2. **Define metadata schemas** for consistent governance
3. **Track deployments** to understand where APIs are running
4. **Import specifications** to enable API analysis and linting
5. **Use lifecycle stages** to track API maturity
6. **Add contacts** for API ownership and support

## When to Use
This skill is applicable to execute the workflow or actions described in the overview.

---

# Azure.ResourceManager.WeightsAndBiases (.NET)

Azure Resource Manager SDK for deploying and managing Weights & Biases ML experiment tracking instances via Azure Marketplace.

## Installation

```bash
dotnet add package Azure.ResourceManager.WeightsAndBiases --prerelease
dotnet add package Azure.Identity
```

**Current Version**: v1.0.0-beta.1 (preview)  
**API Version**: 2024-09-18-preview

## Environment Variables

```bash
AZURE_SUBSCRIPTION_ID=<your-subscription-id>
AZURE_RESOURCE_GROUP=<your-resource-group>
AZURE_WANDB_INSTANCE_NAME=<your-wandb-instance>
```

## Authentication

```csharp
using Azure.Identity;
using Azure.ResourceManager;
using Azure.ResourceManager.WeightsAndBiases;

ArmClient client = new ArmClient(new DefaultAzureCredential());
```

## Resource Hierarchy

```
Subscription
└── ResourceGroup
    └── WeightsAndBiasesInstance    # W&B deployment from Azure Marketplace
        ├── Properties
        │   ├── Marketplace          # Offer details, plan, publisher
        │   ├── User                 # Admin user info
        │   ├── PartnerProperties    # W&B-specific config (region, subdomain)
        │   └── SingleSignOnPropertiesV2  # Entra ID SSO configuration
        └── Identity                 # Managed identity (optional)
```

## Core Workflows

### 1. Create Weights & Biases Instance

```csharp
using Azure.ResourceManager.WeightsAndBiases;
using Azure.ResourceManager.WeightsAndBiases.Models;

ResourceGroupResource resourceGroup = await client
    .GetDefaultSubscriptionAsync()
    .Result
    .GetResourceGroupAsync("my-resource-group");

WeightsAndBiasesInstanceCollection instances = resourceGroup.GetWeightsAndBiasesInstances();

WeightsAndBiasesInstanceData data = new WeightsAndBiasesInstanceData(AzureLocation.EastUS)
{
    Properties = new WeightsAndBiasesInstanceProperties
    {
        // Marketplace configuration
        Marketplace = new WeightsAndBiasesMarketplaceDetails
        {
            SubscriptionId = "<marketplace-subscription-id>",
            OfferDetails = new WeightsAndBiasesOfferDetails
            {
                PublisherId = "wandb",
                OfferId = "wandb-pay-as-you-go",
                PlanId = "wandb-payg",
                PlanName = "Pay As You Go",
                TermId = "monthly",
                TermUnit = "P1M"
            }
        },
        // Admin user
        User = new WeightsAndBiasesUserDetails
        {
            FirstName = "Admin",
            LastName = "User",
            EmailAddress = "admin@example.com",
            Upn = "admin@example.com"
        },
        // W&B-specific configuration
        PartnerProperties = new WeightsAndBiasesPartnerProperties
        {
            Region = WeightsAndBiasesRegion.EastUS,
            Subdomain = "my-company-wandb"
        }
    },
    // Optional: Enable managed identity
    Identity = new ManagedServiceIdentity(ManagedServiceIdentityType.SystemAssigned)
};

ArmOperation<WeightsAndBiasesInstanceResource> operation = await instances
    .CreateOrUpdateAsync(WaitUntil.Completed, "my-wandb-instance", data);

WeightsAndBiasesInstanceResource instance = operation.Value;

Console.WriteLine($"W&B Instance created: {instance.Data.Name}");
Console.WriteLine($"Provisioning state: {instance.Data.Properties.ProvisioningState}");
```

### 2. Get Existing Instance

```csharp
WeightsAndBiasesInstanceResource instance = await resourceGroup
    .GetWeightsAndBiasesInstanceAsync("my-wandb-instance");

Console.WriteLine($"Instance: {instance.Data.Name}");
Console.WriteLine($"Location: {instance.Data.Location}");
Console.WriteLine($"State: {instance.Data.Properties.ProvisioningState}");

if (instance.Data.Properties.PartnerProperties != null)
{
    Console.WriteLine($"Region: {instance.Data.Properties.PartnerProperties.Region}");
    Console.WriteLine($"Subdomain: {instance.Data.Properties.PartnerProperties.Subdomain}");
}
```

### 3. List All Instances

```csharp
// List in resource group
await foreach (WeightsAndBiasesInstanceResource instance in 
    resourceGroup.GetWeightsAndBiasesInstances())
{
    Console.WriteLine($"Instance: {instance.Data.Name}");
    Console.WriteLine($"  Location: {instance.Data.Location}");
    Console.WriteLine($"  State: {instance.Data.Properties.ProvisioningState}");
}

// List in subscription
SubscriptionResource subscription = await client.GetDefaultSubscriptionAsync();
await foreach (WeightsAndBiasesInstanceResource instance in 
    subscription.GetWeightsAndBiasesInstancesAsync())
{
    Console.WriteLine($"{instance.Data.Name} in {instance.Id.ResourceGroupName}");
}
```

### 4. Configure Single Sign-On (SSO)

```csharp
WeightsAndBiasesInstanceResource instance = await resourceGroup
    .GetWeightsAndBiasesInstanceAsync("my-wandb-instance");

// Update with SSO configuration
WeightsAndBiasesInstanceData updateData = instance.Data;

updateData.Properties.SingleSignOnPropertiesV2 = new WeightsAndBiasSingleSignOnPropertiesV2
{
    Type = WeightsAndBiasSingleSignOnType.Saml,
    State = WeightsAndBiasSingleSignOnState.Enable,
    EnterpriseAppId = "<entra-app-id>",
    AadDomains = { "example.com", "contoso.com" }
};

ArmOperation<WeightsAndBiasesInstanceResource> operation = await resourceGroup
    .GetWeightsAndBiasesInstances()
    .CreateOrUpdateAsync(WaitUntil.Completed, "my-wandb-instance", updateData);
```

### 5. Update Instance

```csharp
WeightsAndBiasesInstanceResource instance = await resourceGroup
    .GetWeightsAndBiasesInstanceAsync("my-wandb-instance");

// Update tags
WeightsAndBiasesInstancePatch patch = new WeightsAndBiasesInstancePatch
{
    Tags =
    {
        { "environment", "production" },
        { "team", "ml-platform" },
        { "costCenter", "CC-ML-001" }
    }
};

instance = await instance.UpdateAsync(patch);
Console.WriteLine($"Updated instance: {instance.Data.Name}");
```

### 6. Delete Instance

```csharp
WeightsAndBiasesInstanceResource instance = await resourceGroup
    .GetWeightsAndBiasesInstanceAsync("my-wandb-instance");

await instance.DeleteAsync(WaitUntil.Completed);
Console.WriteLine("Instance deleted");
```

### 7. Check Resource Name Availability

```csharp
// Check if name is available before creating
// (Implement via direct ARM call if SDK doesn't expose this)
try
{
    await resourceGroup.GetWeightsAndBiasesInstanceAsync("desired-name");
    Console.WriteLine("Name is already taken");
}
catch (RequestFailedException ex) when (ex.Status == 404)
{
    Console.WriteLine("Name is available");
}
```

## Key Types Reference

| Type | Purpose |
|------|---------|
| `WeightsAndBiasesInstanceResource` | W&B instance resource |
| `WeightsAndBiasesInstanceData` | Instance configuration data |
| `WeightsAndBiasesInstanceCollection` | Collection of instances |
| `WeightsAndBiasesInstanceProperties` | Instance properties |
| `WeightsAndBiasesMarketplaceDetails` | Marketplace subscription info |
| `WeightsAndBiasesOfferDetails` | Marketplace offer details |
| `WeightsAndBiasesUserDetails` | Admin user information |
| `WeightsAndBiasesPartnerProperties` | W&B-specific configuration |
| `WeightsAndBiasSingleSignOnPropertiesV2` | SSO configuration |
| `WeightsAndBiasesInstancePatch` | Patch for updates |
| `WeightsAndBiasesRegion` | Supported regions enum |

## Available Regions

| Region Enum | Azure Region |
|-------------|--------------|
| `WeightsAndBiasesRegion.EastUS` | East US |
| `WeightsAndBiasesRegion.CentralUS` | Central US |
| `WeightsAndBiasesRegion.WestUS` | West US |
| `WeightsAndBiasesRegion.WestEurope` | West Europe |
| `WeightsAndBiasesRegion.JapanEast` | Japan East |
| `WeightsAndBiasesRegion.KoreaCentral` | Korea Central |

## Marketplace Offer Details

For Azure Marketplace integration:

| Property | Value |
|----------|-------|
| Publisher ID | `wandb` |
| Offer ID | `wandb-pay-as-you-go` |
| Plan ID | `wandb-payg` (Pay As You Go) |

## Best Practices

1. **Use DefaultAzureCredential** — Supports multiple auth methods automatically
2. **Enable managed identity** — For secure access to other Azure resources
3. **Configure SSO** — Enable Entra ID SSO for enterprise security
4. **Tag resources** — Use tags for cost tracking and organization
5. **Check provisioning state** — Wait for `Succeeded` before using instance
6. **Use appropriate region** — Choose region closest to your compute
7. **Monitor with Azure** — Use Azure Monitor for resource health

## Error Handling

```csharp
using Azure;

try
{
    ArmOperation<WeightsAndBiasesInstanceResource> operation = await instances
        .CreateOrUpdateAsync(WaitUntil.Completed, "my-wandb", data);
}
catch (RequestFailedException ex) when (ex.Status == 409)
{
    Console.WriteLine("Instance already exists or name conflict");
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

## Integration with W&B SDK

After creating the Azure resource, use the W&B Python SDK for experiment tracking:

```python
# Install: pip install wandb
import wandb

# Login with your W&B API key from the Azure-deployed instance
wandb.login(host="https://my-company-wandb.wandb.ai")

# Initialize a run
run = wandb.init(project="my-ml-project")

# Log metrics
wandb.log({"accuracy": 0.95, "loss": 0.05})

# Finish run
run.finish()
```

## Related SDKs

| SDK | Purpose | Install |
|-----|---------|---------|
| `Azure.ResourceManager.WeightsAndBiases` | W&B instance management (this SDK) | `dotnet add package Azure.ResourceManager.WeightsAndBiases --prerelease` |
| `Azure.ResourceManager.MachineLearning` | Azure ML workspaces | `dotnet add package Azure.ResourceManager.MachineLearning` |

## Reference Links

| Resource | URL |
|----------|-----|
| NuGet Package | https://www.nuget.org/packages/Azure.ResourceManager.WeightsAndBiases |
| W&B Documentation | https://docs.wandb.ai/ |
| Azure Marketplace | https://azuremarketplace.microsoft.com/marketplace/apps/wandb.wandb-pay-as-you-go |
| GitHub Source | https://github.com/Azure/azure-sdk-for-net/tree/main/sdk/weightsandbiases |

## When to Use
This skill is applicable to execute the workflow or actions described in the overview.

---

# Azure.ResourceManager.ArizeAIObservabilityEval

.NET SDK for managing Arize AI Observability and Evaluation resources on Azure.

## Installation

```bash
dotnet add package Azure.ResourceManager.ArizeAIObservabilityEval --version 1.0.0
```

## Package Info

| Property | Value |
|----------|-------|
| Package | `Azure.ResourceManager.ArizeAIObservabilityEval` |
| Version | `1.0.0` (GA) |
| API Version | `2024-10-01` |
| ARM Type | `ArizeAi.ObservabilityEval/organizations` |
| Dependencies | `Azure.Core` >= 1.46.2, `Azure.ResourceManager` >= 1.13.1 |

## Environment Variables

```bash
AZURE_SUBSCRIPTION_ID=<your-subscription-id>
AZURE_TENANT_ID=<your-tenant-id>
AZURE_CLIENT_ID=<your-client-id>
AZURE_CLIENT_SECRET=<your-client-secret>
```

## Authentication

```csharp
using Azure.Identity;
using Azure.ResourceManager;
using Azure.ResourceManager.ArizeAIObservabilityEval;

// Always use DefaultAzureCredential
var credential = new DefaultAzureCredential();
var armClient = new ArmClient(credential);
```

## Core Workflow

### Create an Arize AI Organization

```csharp
using Azure.Core;
using Azure.ResourceManager.Resources;
using Azure.ResourceManager.ArizeAIObservabilityEval;
using Azure.ResourceManager.ArizeAIObservabilityEval.Models;

// Get subscription and resource group
var subscriptionId = Environment.GetEnvironmentVariable("AZURE_SUBSCRIPTION_ID");
var subscription = await armClient.GetSubscriptionResource(
    SubscriptionResource.CreateResourceIdentifier(subscriptionId)).GetAsync();
var resourceGroup = await subscription.Value.GetResourceGroupAsync("my-resource-group");

// Get the organization collection
var collection = resourceGroup.Value.GetArizeAIObservabilityEvalOrganizations();

// Create organization data
var data = new ArizeAIObservabilityEvalOrganizationData(AzureLocation.EastUS)
{
    Properties = new ArizeAIObservabilityEvalOrganizationProperties
    {
        Marketplace = new ArizeAIObservabilityEvalMarketplaceDetails
        {
            SubscriptionId = "marketplace-subscription-id",
            OfferDetails = new ArizeAIObservabilityEvalOfferDetails
            {
                PublisherId = "arikimlabs1649082416596",
                OfferId = "arize-liftr-1",
                PlanId = "arize-liftr-1-plan",
                PlanName = "Arize AI Plan",
                TermUnit = "P1M",
                TermId = "term-id"
            }
        },
        User = new ArizeAIObservabilityEvalUserDetails
        {
            FirstName = "John",
            LastName = "Doe",
            EmailAddress = "john.doe@example.com"
        }
    },
    Tags = { ["environment"] = "production" }
};

// Create (long-running operation)
var operation = await collection.CreateOrUpdateAsync(
    WaitUntil.Completed,
    "my-arize-org",
    data);

var organization = operation.Value;
Console.WriteLine($"Created: {organization.Data.Name}");
```

### Get an Organization

```csharp
// Option 1: From collection
var org = await collection.GetAsync("my-arize-org");

// Option 2: Check if exists first
var exists = await collection.ExistsAsync("my-arize-org");
if (exists.Value)
{
    var org = await collection.GetAsync("my-arize-org");
}

// Option 3: GetIfExists (returns null if not found)
var response = await collection.GetIfExistsAsync("my-arize-org");
if (response.HasValue)
{
    var org = response.Value;
}
```

### List Organizations

```csharp
// List in resource group
await foreach (var org in collection.GetAllAsync())
{
    Console.WriteLine($"Org: {org.Data.Name}, State: {org.Data.Properties?.ProvisioningState}");
}

// List in subscription
await foreach (var org in subscription.Value.GetArizeAIObservabilityEvalOrganizationsAsync())
{
    Console.WriteLine($"Org: {org.Data.Name}");
}
```

### Update an Organization

```csharp
// Update tags
var org = await collection.GetAsync("my-arize-org");
var updateData = new ArizeAIObservabilityEvalOrganizationPatch
{
    Tags = { ["environment"] = "staging", ["team"] = "ml-ops" }
};
var updated = await org.Value.UpdateAsync(updateData);
```

### Delete an Organization

```csharp
var org = await collection.GetAsync("my-arize-org");
await org.Value.DeleteAsync(WaitUntil.Completed);
```

## Key Types

| Type | Purpose |
|------|---------|
| `ArizeAIObservabilityEvalOrganizationResource` | Main ARM resource for Arize organizations |
| `ArizeAIObservabilityEvalOrganizationCollection` | Collection for CRUD operations |
| `ArizeAIObservabilityEvalOrganizationData` | Resource data model |
| `ArizeAIObservabilityEvalOrganizationProperties` | Organization properties |
| `ArizeAIObservabilityEvalMarketplaceDetails` | Azure Marketplace subscription info |
| `ArizeAIObservabilityEvalOfferDetails` | Marketplace offer configuration |
| `ArizeAIObservabilityEvalUserDetails` | User contact information |
| `ArizeAIObservabilityEvalOrganizationPatch` | Patch model for updates |
| `ArizeAIObservabilityEvalSingleSignOnPropertiesV2` | SSO configuration |

## Enums

| Enum | Values |
|------|--------|
| `ArizeAIObservabilityEvalOfferProvisioningState` | `Succeeded`, `Failed`, `Canceled`, `Provisioning`, `Updating`, `Deleting`, `Accepted` |
| `ArizeAIObservabilityEvalMarketplaceSubscriptionStatus` | `PendingFulfillmentStart`, `Subscribed`, `Suspended`, `Unsubscribed` |
| `ArizeAIObservabilityEvalSingleSignOnState` | `Initial`, `Enable`, `Disable` |
| `ArizeAIObservabilityEvalSingleSignOnType` | `Saml`, `OpenId` |

## Best Practices

1. **Use async methods** — All operations support async/await
2. **Handle long-running operations** — Use `WaitUntil.Completed` or poll manually
3. **Use GetIfExistsAsync** — Avoid exceptions for conditional logic
4. **Implement retry policies** — Configure via `ArmClientOptions`
5. **Use resource identifiers** — For direct resource access without listing
6. **Close clients properly** — Use `using` statements or dispose explicitly

## Error Handling

```csharp
try
{
    var org = await collection.GetAsync("my-arize-org");
}
catch (Azure.RequestFailedException ex) when (ex.Status == 404)
{
    Console.WriteLine("Organization not found");
}
catch (Azure.RequestFailedException ex)
{
    Console.WriteLine($"Azure error: {ex.Message}");
}
```

## Direct Resource Access

```csharp
// Access resource directly by ID (without listing)
var resourceId = ArizeAIObservabilityEvalOrganizationResource.CreateResourceIdentifier(
    subscriptionId,
    "my-resource-group",
    "my-arize-org");

var org = armClient.GetArizeAIObservabilityEvalOrganizationResource(resourceId);
var data = await org.GetAsync();
```

## Links

- [NuGet Package](https://www.nuget.org/packages/Azure.ResourceManager.ArizeAIObservabilityEval)
- [Azure SDK for .NET](https://github.com/Azure/azure-sdk-for-net)
- [Arize AI](https://arize.com/)

## When to Use
This skill is applicable to execute the workflow or actions described in the overview.

---

# Azure Bot Service Management SDK for Python

Manage Azure Bot Service resources including bots, channels, and connections.

## Installation

```bash
pip install azure-mgmt-botservice
pip install azure-identity
```

## Environment Variables

```bash
AZURE_SUBSCRIPTION_ID=<your-subscription-id>
AZURE_RESOURCE_GROUP=<your-resource-group>
```

## Authentication

```python
from azure.identity import DefaultAzureCredential
from azure.mgmt.botservice import AzureBotService
import os

credential = DefaultAzureCredential()
client = AzureBotService(
    credential=credential,
    subscription_id=os.environ["AZURE_SUBSCRIPTION_ID"]
)
```

## Create a Bot

```python
from azure.mgmt.botservice import AzureBotService
from azure.mgmt.botservice.models import Bot, BotProperties, Sku
from azure.identity import DefaultAzureCredential
import os

credential = DefaultAzureCredential()
client = AzureBotService(
    credential=credential,
    subscription_id=os.environ["AZURE_SUBSCRIPTION_ID"]
)

resource_group = os.environ["AZURE_RESOURCE_GROUP"]
bot_name = "my-chat-bot"

bot = client.bots.create(
    resource_group_name=resource_group,
    resource_name=bot_name,
    parameters=Bot(
        location="global",
        sku=Sku(name="F0"),  # Free tier
        kind="azurebot",
        properties=BotProperties(
            display_name="My Chat Bot",
            description="A conversational AI bot",
            endpoint="https://my-bot-app.azurewebsites.net/api/messages",
            msa_app_id="<your-app-id>",
            msa_app_type="MultiTenant"
        )
    )
)

print(f"Bot created: {bot.name}")
```

## Get Bot Details

```python
bot = client.bots.get(
    resource_group_name=resource_group,
    resource_name=bot_name
)

print(f"Bot: {bot.properties.display_name}")
print(f"Endpoint: {bot.properties.endpoint}")
print(f"SKU: {bot.sku.name}")
```

## List Bots in Resource Group

```python
bots = client.bots.list_by_resource_group(resource_group_name=resource_group)

for bot in bots:
    print(f"Bot: {bot.name} - {bot.properties.display_name}")
```

## List All Bots in Subscription

```python
all_bots = client.bots.list()

for bot in all_bots:
    print(f"Bot: {bot.name} in {bot.id.split('/')[4]}")
```

## Update Bot

```python
bot = client.bots.update(
    resource_group_name=resource_group,
    resource_name=bot_name,
    properties=BotProperties(
        display_name="Updated Bot Name",
        description="Updated description"
    )
)
```

## Delete Bot

```python
client.bots.delete(
    resource_group_name=resource_group,
    resource_name=bot_name
)
```

## Configure Channels

### Add Teams Channel

```python
from azure.mgmt.botservice.models import (
    BotChannel,
    MsTeamsChannel,
    MsTeamsChannelProperties
)

channel = client.channels.create(
    resource_group_name=resource_group,
    resource_name=bot_name,
    channel_name="MsTeamsChannel",
    parameters=BotChannel(
        location="global",
        properties=MsTeamsChannel(
            properties=MsTeamsChannelProperties(
                is_enabled=True
            )
        )
    )
)
```

### Add Direct Line Channel

```python
from azure.mgmt.botservice.models import (
    BotChannel,
    DirectLineChannel,
    DirectLineChannelProperties,
    DirectLineSite
)

channel = client.channels.create(
    resource_group_name=resource_group,
    resource_name=bot_name,
    channel_name="DirectLineChannel",
    parameters=BotChannel(
        location="global",
        properties=DirectLineChannel(
            properties=DirectLineChannelProperties(
                sites=[
                    DirectLineSite(
                        site_name="Default Site",
                        is_enabled=True,
                        is_v1_enabled=False,
                        is_v3_enabled=True
                    )
                ]
            )
        )
    )
)
```

### Add Web Chat Channel

```python
from azure.mgmt.botservice.models import (
    BotChannel,
    WebChatChannel,
    WebChatChannelProperties,
    WebChatSite
)

channel = client.channels.create(
    resource_group_name=resource_group,
    resource_name=bot_name,
    channel_name="WebChatChannel",
    parameters=BotChannel(
        location="global",
        properties=WebChatChannel(
            properties=WebChatChannelProperties(
                sites=[
                    WebChatSite(
                        site_name="Default Site",
                        is_enabled=True
                    )
                ]
            )
        )
    )
)
```

## Get Channel Details

```python
channel = client.channels.get(
    resource_group_name=resource_group,
    resource_name=bot_name,
    channel_name="DirectLineChannel"
)
```

## List Channel Keys

```python
keys = client.channels.list_with_keys(
    resource_group_name=resource_group,
    resource_name=bot_name,
    channel_name="DirectLineChannel"
)

# Access Direct Line keys
if hasattr(keys.properties, 'properties'):
    for site in keys.properties.properties.sites:
        print(f"Site: {site.site_name}")
        print(f"Key: {site.key}")
```

## Bot Connections (OAuth)

### Create Connection Setting

```python
from azure.mgmt.botservice.models import (
    ConnectionSetting,
    ConnectionSettingProperties
)

connection = client.bot_connection.create(
    resource_group_name=resource_group,
    resource_name=bot_name,
    connection_name="graph-connection",
    parameters=ConnectionSetting(
        location="global",
        properties=ConnectionSettingProperties(
            client_id="<oauth-client-id>",
            client_secret="<oauth-client-secret>",
            scopes="User.Read",
            service_provider_id="<service-provider-id>"
        )
    )
)
```

### List Connections

```python
connections = client.bot_connection.list_by_bot_service(
    resource_group_name=resource_group,
    resource_name=bot_name
)

for conn in connections:
    print(f"Connection: {conn.name}")
```

## Client Operations

| Operation | Method |
|-----------|--------|
| `client.bots` | Bot CRUD operations |
| `client.channels` | Channel configuration |
| `client.bot_connection` | OAuth connection settings |
| `client.direct_line` | Direct Line channel operations |
| `client.email` | Email channel operations |
| `client.operations` | Available operations |
| `client.host_settings` | Host settings operations |

## SKU Options

| SKU | Description |
|-----|-------------|
| `F0` | Free tier (limited messages) |
| `S1` | Standard tier (unlimited messages) |

## Channel Types

| Channel | Class | Purpose |
|---------|-------|---------|
| `MsTeamsChannel` | Microsoft Teams | Teams integration |
| `DirectLineChannel` | Direct Line | Custom client integration |
| `WebChatChannel` | Web Chat | Embeddable web widget |
| `SlackChannel` | Slack | Slack workspace integration |
| `FacebookChannel` | Facebook | Messenger integration |
| `EmailChannel` | Email | Email communication |

## Best Practices

1. **Use DefaultAzureCredential** for authentication
2. **Start with F0 SKU** for development, upgrade to S1 for production
3. **Store MSA App ID/Secret securely** — use Key Vault
4. **Enable only needed channels** — reduces attack surface
5. **Rotate Direct Line keys** periodically
6. **Use managed identity** when possible for bot connections
7. **Configure proper CORS** for Web Chat channel

## When to Use
This skill is applicable to execute the workflow or actions described in the overview.

---

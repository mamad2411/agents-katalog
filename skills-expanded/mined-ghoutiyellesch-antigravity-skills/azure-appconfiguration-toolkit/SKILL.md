---
name: azure-appconfiguration-toolkit
description: Consolidated toolkit for azure-appconfiguration. Covers azure-appconfiguration-py, azure-appconfiguration-ts, azure-appconfiguration-java
---
# Azure Appconfiguration Toolkit

## Core Capabilities
# Azure Appconfiguration Toolkit

# Azure App Configuration SDK for Python

Centralized configuration management with feature flags and dynamic settings.

## Installation

```bash
pip install azure-appconfiguration
```

## Environment Variables

```bash
AZURE_APPCONFIGURATION_CONNECTION_STRING=Endpoint=https://<name>.azconfig.io;Id=...;Secret=...
# Or for Entra ID:
AZURE_APPCONFIGURATION_ENDPOINT=https://<name>.azconfig.io
```

## Authentication

### Connection String

```python
from azure.appconfiguration import AzureAppConfigurationClient

client = AzureAppConfigurationClient.from_connection_string(
    os.environ["AZURE_APPCONFIGURATION_CONNECTION_STRING"]
)
```

### Entra ID

```python
from azure.appconfiguration import AzureAppConfigurationClient
from azure.identity import DefaultAzureCredential

client = AzureAppConfigurationClient(
    base_url=os.environ["AZURE_APPCONFIGURATION_ENDPOINT"],
    credential=DefaultAzureCredential()
)
```

## Configuration Settings

### Get Setting

```python
setting = client.get_configuration_setting(key="app:settings:message")
print(f"{setting.key} = {setting.value}")
```

### Get with Label

```python
# Labels allow environment-specific values
setting = client.get_configuration_setting(
    key="app:settings:message",
    label="production"
)
```

### Set Setting

```python
from azure.appconfiguration import ConfigurationSetting

setting = ConfigurationSetting(
    key="app:settings:message",
    value="Hello, World!",
    label="development",
    content_type="text/plain",
    tags={"environment": "dev"}
)

client.set_configuration_setting(setting)
```

### Delete Setting

```python
client.delete_configuration_setting(
    key="app:settings:message",
    label="development"
)
```

## List Settings

### All Settings

```python
settings = client.list_configuration_settings()
for setting in settings:
    print(f"{setting.key} [{setting.label}] = {setting.value}")
```

### Filter by Key Prefix

```python
settings = client.list_configuration_settings(
    key_filter="app:settings:*"
)
```

### Filter by Label

```python
settings = client.list_configuration_settings(
    label_filter="production"
)
```

## Feature Flags

### Set Feature Flag

```python
from azure.appconfiguration import ConfigurationSetting
import json

feature_flag = ConfigurationSetting(
    key=".appconfig.featureflag/beta-feature",
    value=json.dumps({
        "id": "beta-feature",
        "enabled": True,
        "conditions": {
            "client_filters": []
        }
    }),
    content_type="application/vnd.microsoft.appconfig.ff+json;charset=utf-8"
)

client.set_configuration_setting(feature_flag)
```

### Get Feature Flag

```python
setting = client.get_configuration_setting(
    key=".appconfig.featureflag/beta-feature"
)
flag_data = json.loads(setting.value)
print(f"Feature enabled: {flag_data['enabled']}")
```

### List Feature Flags

```python
flags = client.list_configuration_settings(
    key_filter=".appconfig.featureflag/*"
)
for flag in flags:
    data = json.loads(flag.value)
    print(f"{data['id']}: {'enabled' if data['enabled'] else 'disabled'}")
```

## Read-Only Settings

```python
# Make setting read-only
client.set_read_only(
    configuration_setting=setting,
    read_only=True
)

# Remove read-only
client.set_read_only(
    configuration_setting=setting,
    read_only=False
)
```

## Snapshots

### Create Snapshot

```python
from azure.appconfiguration import ConfigurationSnapshot, ConfigurationSettingFilter

snapshot = ConfigurationSnapshot(
    name="v1-snapshot",
    filters=[
        ConfigurationSettingFilter(key="app:*", label="production")
    ]
)

created = client.begin_create_snapshot(
    name="v1-snapshot",
    snapshot=snapshot
).result()
```

### List Snapshot Settings

```python
settings = client.list_configuration_settings(
    snapshot_name="v1-snapshot"
)
```

## Async Client

```python
from azure.appconfiguration.aio import AzureAppConfigurationClient
from azure.identity.aio import DefaultAzureCredential

async def main():
    credential = DefaultAzureCredential()
    client = AzureAppConfigurationClient(
        base_url=endpoint,
        credential=credential
    )
    
    setting = await client.get_configuration_setting(key="app:message")
    print(setting.value)
    
    await client.close()
    await credential.close()
```

## Client Operations

| Operation | Description |
|-----------|-------------|
| `get_configuration_setting` | Get single setting |
| `set_configuration_setting` | Create or update setting |
| `delete_configuration_setting` | Delete setting |
| `list_configuration_settings` | List with filters |
| `set_read_only` | Lock/unlock setting |
| `begin_create_snapshot` | Create point-in-time snapshot |
| `list_snapshots` | List all snapshots |

## Best Practices

1. **Use labels** for environment separation (dev, staging, prod)
2. **Use key prefixes** for logical grouping (app:database:*, app:cache:*)
3. **Make production settings read-only** to prevent accidental changes
4. **Create snapshots** before deployments for rollback capability
5. **Use Entra ID** instead of connection strings in production
6. **Refresh settings periodically** in long-running applications
7. **Use feature flags** for gradual rollouts and A/B testing

## When to Use
This skill is applicable to execute the workflow or actions described in the overview.

---

# Azure App Configuration SDK for TypeScript

Centralized configuration management with feature flags and dynamic refresh.

## Installation

```bash
# Low-level CRUD SDK
npm install @azure/app-configuration @azure/identity

# High-level provider (recommended for apps)
npm install @azure/app-configuration-provider @azure/identity

# Feature flag management
npm install @microsoft/feature-management
```

## Environment Variables

```bash
AZURE_APPCONFIG_ENDPOINT=https://<your-resource>.azconfig.io
# OR
AZURE_APPCONFIG_CONNECTION_STRING=Endpoint=https://...;Id=...;Secret=...
```

## Authentication

```typescript
import { AppConfigurationClient } from "@azure/app-configuration";
import { DefaultAzureCredential } from "@azure/identity";

// DefaultAzureCredential (recommended)
const client = new AppConfigurationClient(
  process.env.AZURE_APPCONFIG_ENDPOINT!,
  new DefaultAzureCredential()
);

// Connection string
const client2 = new AppConfigurationClient(
  process.env.AZURE_APPCONFIG_CONNECTION_STRING!
);
```

## CRUD Operations

### Create/Update Settings

```typescript
// Add new (fails if exists)
await client.addConfigurationSetting({
  key: "app:settings:message",
  value: "Hello World",
  label: "production",
  contentType: "text/plain",
  tags: { environment: "prod" },
});

// Set (create or update)
await client.setConfigurationSetting({
  key: "app:settings:message",
  value: "Updated value",
  label: "production",
});

// Update with optimistic concurrency
const existing = await client.getConfigurationSetting({ key: "myKey" });
existing.value = "new value";
await client.setConfigurationSetting(existing, { onlyIfUnchanged: true });
```

### Read Settings

```typescript
// Get single setting
const setting = await client.getConfigurationSetting({
  key: "app:settings:message",
  label: "production",  // optional
});
console.log(setting.value);

// List with filters
const settings = client.listConfigurationSettings({
  keyFilter: "app:*",
  labelFilter: "production",
});

for await (const setting of settings) {
  console.log(`${setting.key}: ${setting.value}`);
}
```

### Delete Settings

```typescript
await client.deleteConfigurationSetting({
  key: "app:settings:message",
  label: "production",
});
```

### Lock/Unlock (Read-Only)

```typescript
// Lock
await client.setReadOnly({ key: "myKey", label: "prod" }, true);

// Unlock
await client.setReadOnly({ key: "myKey", label: "prod" }, false);
```

## App Configuration Provider

### Load Configuration

```typescript
import { load } from "@azure/app-configuration-provider";
import { DefaultAzureCredential } from "@azure/identity";

const appConfig = await load(
  process.env.AZURE_APPCONFIG_ENDPOINT!,
  new DefaultAzureCredential(),
  {
    selectors: [
      { keyFilter: "app:*", labelFilter: "production" },
    ],
    trimKeyPrefixes: ["app:"],
  }
);

// Map-style access
const value = appConfig.get("settings:message");

// Object-style access
const config = appConfig.constructConfigurationObject({ separator: ":" });
console.log(config.settings.message);
```

### Dynamic Refresh

```typescript
const appConfig = await load(endpoint, credential, {
  selectors: [{ keyFilter: "app:*" }],
  refreshOptions: {
    enabled: true,
    refreshIntervalInMs: 30_000,  // 30 seconds
  },
});

// Trigger refresh (non-blocking)
appConfig.refresh();

// Listen for refresh events
const disposer = appConfig.onRefresh(() => {
  console.log("Configuration refreshed!");
});

// Express middleware pattern
app.use((req, res, next) => {
  appConfig.refresh();
  next();
});
```

### Key Vault References

```typescript
const appConfig = await load(endpoint, credential, {
  selectors: [{ keyFilter: "app:*" }],
  keyVaultOptions: {
    credential: new DefaultAzureCredential(),
    secretRefreshIntervalInMs: 7200_000,  // 2 hours
  },
});

// Secrets are automatically resolved
const dbPassword = appConfig.get("database:password");
```

## Feature Flags

### Create Feature Flag (Low-Level)

```typescript
import {
  featureFlagPrefix,
  featureFlagContentType,
  FeatureFlagValue,
  ConfigurationSetting,
} from "@azure/app-configuration";

const flag: ConfigurationSetting<FeatureFlagValue> = {
  key: `${featureFlagPrefix}Beta`,
  contentType: featureFlagContentType,
  value: {
    id: "Beta",
    enabled: true,
    description: "Beta feature",
    conditions: {
      clientFilters: [
        {
          name: "Microsoft.Targeting",
          parameters: {
            Audience: {
              Users: ["user@example.com"],
              Groups: [{ Name: "beta-testers", RolloutPercentage: 50 }],
              DefaultRolloutPercentage: 0,
            },
          },
        },
      ],
    },
  },
};

await client.addConfigurationSetting(flag);
```

### Load and Evaluate Feature Flags

```typescript
import { load } from "@azure/app-configuration-provider";
import {
  ConfigurationMapFeatureFlagProvider,
  FeatureManager,
} from "@microsoft/feature-management";

const appConfig = await load(endpoint, credential, {
  featureFlagOptions: {
    enabled: true,
    selectors: [{ keyFilter: "*" }],
    refresh: {
      enabled: true,
      refreshIntervalInMs: 30_000,
    },
  },
});

const featureProvider = new ConfigurationMapFeatureFlagProvider(appConfig);
const featureManager = new FeatureManager(featureProvider);

// Simple check
const isEnabled = await featureManager.isEnabled("Beta");

// With targeting context
const isEnabledForUser = await featureManager.isEnabled("Beta", {
  userId: "user@example.com",
  groups: ["beta-testers"],
});
```

## Snapshots

```typescript
// Create snapshot
const snapshot = await client.beginCreateSnapshotAndWait({
  name: "release-v1.0",
  retentionPeriod: 2592000,  // 30 days
  filters: [{ keyFilter: "app:*", labelFilter: "production" }],
});

// Get snapshot
const snap = await client.getSnapshot("release-v1.0");

// List settings in snapshot
const settings = client.listConfigurationSettingsForSnapshot("release-v1.0");
for await (const setting of settings) {
  console.log(`${setting.key}: ${setting.value}`);
}

// Archive/recover
await client.archiveSnapshot("release-v1.0");
await client.recoverSnapshot("release-v1.0");

// Load from snapshot (provider)
const config = await load(endpoint, credential, {
  selectors: [{ snapshotName: "release-v1.0" }],
});
```

## Labels

```typescript
// Create settings with labels
await client.setConfigurationSetting({
  key: "database:host",
  value: "dev-db.example.com",
  label: "development",
});

await client.setConfigurationSetting({
  key: "database:host",
  value: "prod-db.example.com",
  label: "production",
});

// Filter by label
const prodSettings = client.listConfigurationSettings({
  keyFilter: "*",
  labelFilter: "production",
});

// No label (null label)
const noLabelSettings = client.listConfigurationSettings({
  labelFilter: "\0",
});

// List available labels
for await (const label of client.listLabels()) {
  console.log(label.name);
}
```

## Key Types

```typescript
import {
  AppConfigurationClient,
  ConfigurationSetting,
  FeatureFlagValue,
  SecretReferenceValue,
  featureFlagPrefix,
  featureFlagContentType,
  secretReferenceContentType,
  ListConfigurationSettingsOptions,
} from "@azure/app-configuration";

import { load } from "@azure/app-configuration-provider";

import {
  FeatureManager,
  ConfigurationMapFeatureFlagProvider,
} from "@microsoft/feature-management";
```

## Best Practices

1. **Use provider for apps** - `@azure/app-configuration-provider` for runtime config
2. **Use low-level for management** - `@azure/app-configuration` for CRUD operations
3. **Enable refresh** - For dynamic configuration updates
4. **Use labels** - Separate configurations by environment
5. **Use snapshots** - For immutable release configurations
6. **Sentinel pattern** - Use a sentinel key to trigger full refresh
7. **RBAC roles** - `App Configuration Data Reader` for read-only access

## When to Use
This skill is applicable to execute the workflow or actions described in the overview.

---

# Azure App Configuration SDK for Java

Client library for Azure App Configuration, a managed service for centralizing application configurations.

## Installation

```xml
<dependency>
    <groupId>com.azure</groupId>
    <artifactId>azure-data-appconfiguration</artifactId>
    <version>1.8.0</version>
</dependency>
```

Or use Azure SDK BOM:

```xml
<dependencyManagement>
    <dependencies>
        <dependency>
            <groupId>com.azure</groupId>
            <artifactId>azure-sdk-bom</artifactId>
            <version>{bom_version}</version>
            <type>pom</type>
            <scope>import</scope>
        </dependency>
    </dependencies>
</dependencyManagement>

<dependencies>
    <dependency>
        <groupId>com.azure</groupId>
        <artifactId>azure-data-appconfiguration</artifactId>
    </dependency>
</dependencies>
```

## Prerequisites

- Azure App Configuration store
- Connection string or Entra ID credentials

## Environment Variables

```bash
AZURE_APPCONFIG_CONNECTION_STRING=Endpoint=https://<store>.azconfig.io;Id=<id>;Secret=<secret>
AZURE_APPCONFIG_ENDPOINT=https://<store>.azconfig.io
```

## Client Creation

### With Connection String

```java
import com.azure.data.appconfiguration.ConfigurationClient;
import com.azure.data.appconfiguration.ConfigurationClientBuilder;

ConfigurationClient configClient = new ConfigurationClientBuilder()
    .connectionString(System.getenv("AZURE_APPCONFIG_CONNECTION_STRING"))
    .buildClient();
```

### Async Client

```java
import com.azure.data.appconfiguration.ConfigurationAsyncClient;

ConfigurationAsyncClient asyncClient = new ConfigurationClientBuilder()
    .connectionString(connectionString)
    .buildAsyncClient();
```

### With Entra ID (Recommended)

```java
import com.azure.identity.DefaultAzureCredentialBuilder;

ConfigurationClient configClient = new ConfigurationClientBuilder()
    .credential(new DefaultAzureCredentialBuilder().build())
    .endpoint(System.getenv("AZURE_APPCONFIG_ENDPOINT"))
    .buildClient();
```

## Key Concepts

| Concept | Description |
|---------|-------------|
| Configuration Setting | Key-value pair with optional label |
| Label | Dimension for separating settings (e.g., environments) |
| Feature Flag | Special setting for feature management |
| Secret Reference | Setting pointing to Key Vault secret |
| Snapshot | Point-in-time immutable view of settings |

## Configuration Setting Operations

### Create Setting (Add)

Creates only if setting doesn't exist:

```java
import com.azure.data.appconfiguration.models.ConfigurationSetting;

ConfigurationSetting setting = configClient.addConfigurationSetting(
    "app/database/connection", 
    "Production", 
    "Server=prod.db.com;Database=myapp"
);
```

### Create or Update Setting (Set)

Creates or overwrites:

```java
ConfigurationSetting setting = configClient.setConfigurationSetting(
    "app/cache/enabled", 
    "Production", 
    "true"
);
```

### Get Setting

```java
ConfigurationSetting setting = configClient.getConfigurationSetting(
    "app/database/connection", 
    "Production"
);
System.out.println("Value: " + setting.getValue());
System.out.println("Content-Type: " + setting.getContentType());
System.out.println("Last Modified: " + setting.getLastModified());
```

### Conditional Get (If Changed)

```java
import com.azure.core.http.rest.Response;
import com.azure.core.util.Context;

Response<ConfigurationSetting> response = configClient.getConfigurationSettingWithResponse(
    setting,      // Setting with ETag
    null,         // Accept datetime
    true,         // ifChanged - only fetch if modified
    Context.NONE
);

if (response.getStatusCode() == 304) {
    System.out.println("Setting not modified");
} else {
    ConfigurationSetting updated = response.getValue();
}
```

### Update Setting

```java
ConfigurationSetting updated = configClient.setConfigurationSetting(
    "app/cache/enabled", 
    "Production", 
    "false"
);
```

### Conditional Update (If Unchanged)

```java
// Only update if ETag matches (no concurrent modifications)
Response<ConfigurationSetting> response = configClient.setConfigurationSettingWithResponse(
    setting,     // Setting with current ETag
    true,        // ifUnchanged
    Context.NONE
);
```

### Delete Setting

```java
ConfigurationSetting deleted = configClient.deleteConfigurationSetting(
    "app/cache/enabled", 
    "Production"
);
```

### Conditional Delete

```java
Response<ConfigurationSetting> response = configClient.deleteConfigurationSettingWithResponse(
    setting,     // Setting with ETag
    true,        // ifUnchanged
    Context.NONE
);
```

## List and Filter Settings

### List by Key Pattern

```java
import com.azure.data.appconfiguration.models.SettingSelector;
import com.azure.core.http.rest.PagedIterable;

SettingSelector selector = new SettingSelector()
    .setKeyFilter("app/*");

PagedIterable<ConfigurationSetting> settings = configClient.listConfigurationSettings(selector);
for (ConfigurationSetting s : settings) {
    System.out.println(s.getKey() + " = " + s.getValue());
}
```

### List by Label

```java
SettingSelector selector = new SettingSelector()
    .setKeyFilter("*")
    .setLabelFilter("Production");

PagedIterable<ConfigurationSetting> settings = configClient.listConfigurationSettings(selector);
```

### List by Multiple Keys

```java
SettingSelector selector = new SettingSelector()
    .setKeyFilter("app/database/*,app/cache/*");

PagedIterable<ConfigurationSetting> settings = configClient.listConfigurationSettings(selector);
```

### List Revisions

```java
SettingSelector selector = new SettingSelector()
    .setKeyFilter("app/database/connection");

PagedIterable<ConfigurationSetting> revisions = configClient.listRevisions(selector);
for (ConfigurationSetting revision : revisions) {
    System.out.println("Value: " + revision.getValue() + ", Modified: " + revision.getLastModified());
}
```

## Feature Flags

### Create Feature Flag

```java
import com.azure.data.appconfiguration.models.FeatureFlagConfigurationSetting;
import com.azure.data.appconfiguration.models.FeatureFlagFilter;
import java.util.Arrays;

FeatureFlagFilter percentageFilter = new FeatureFlagFilter("Microsoft.Percentage")
    .addParameter("Value", 50);

FeatureFlagConfigurationSetting featureFlag = new FeatureFlagConfigurationSetting("beta-feature", true)
    .setDescription("Beta feature rollout")
    .setClientFilters(Arrays.asList(percentageFilter));

FeatureFlagConfigurationSetting created = (FeatureFlagConfigurationSetting)
    configClient.addConfigurationSetting(featureFlag);
```

### Get Feature Flag

```java
FeatureFlagConfigurationSetting flag = (FeatureFlagConfigurationSetting)
    configClient.getConfigurationSetting(featureFlag);

System.out.println("Feature: " + flag.getFeatureId());
System.out.println("Enabled: " + flag.isEnabled());
System.out.println("Filters: " + flag.getClientFilters());
```

### Update Feature Flag

```java
featureFlag.setEnabled(false);
FeatureFlagConfigurationSetting updated = (FeatureFlagConfigurationSetting)
    configClient.setConfigurationSetting(featureFlag);
```

## Secret References

### Create Secret Reference

```java
import com.azure.data.appconfiguration.models.SecretReferenceConfigurationSetting;

SecretReferenceConfigurationSetting secretRef = new SecretReferenceConfigurationSetting(
    "app/secrets/api-key",
    "https://myvault.vault.azure.net/secrets/api-key"
);

SecretReferenceConfigurationSetting created = (SecretReferenceConfigurationSetting)
    configClient.addConfigurationSetting(secretRef);
```

### Get Secret Reference

```java
SecretReferenceConfigurationSetting ref = (SecretReferenceConfigurationSetting)
    configClient.getConfigurationSetting(secretRef);

System.out.println("Secret URI: " + ref.getSecretId());
```

## Read-Only Settings

### Set Read-Only

```java
ConfigurationSetting readOnly = configClient.setReadOnly(
    "app/critical/setting", 
    "Production", 
    true
);
```

### Clear Read-Only

```java
ConfigurationSetting writable = configClient.setReadOnly(
    "app/critical/setting", 
    "Production", 
    false
);
```

## Snapshots

### Create Snapshot

```java
import com.azure.data.appconfiguration.models.ConfigurationSnapshot;
import com.azure.data.appconfiguration.models.ConfigurationSettingsFilter;
import com.azure.core.util.polling.SyncPoller;
import com.azure.core.util.polling.PollOperationDetails;

List<ConfigurationSettingsFilter> filters = new ArrayList<>();
filters.add(new ConfigurationSettingsFilter("app/*"));

SyncPoller<PollOperationDetails, ConfigurationSnapshot> poller = configClient.beginCreateSnapshot(
    "release-v1.0",
    new ConfigurationSnapshot(filters),
    Context.NONE
);
poller.setPollInterval(Duration.ofSeconds(10));
poller.waitForCompletion();

ConfigurationSnapshot snapshot = poller.getFinalResult();
System.out.println("Snapshot: " + snapshot.getName() + ", Status: " + snapshot.getStatus());
```

### Get Snapshot

```java
ConfigurationSnapshot snapshot = configClient.getSnapshot("release-v1.0");
System.out.println("Created: " + snapshot.getCreatedAt());
System.out.println("Items: " + snapshot.getItemCount());
```

### List Settings in Snapshot

```java
PagedIterable<ConfigurationSetting> settings = 
    configClient.listConfigurationSettingsForSnapshot("release-v1.0");

for (ConfigurationSetting setting : settings) {
    System.out.println(setting.getKey() + " = " + setting.getValue());
}
```

### Archive Snapshot

```java
ConfigurationSnapshot archived = configClient.archiveSnapshot("release-v1.0");
System.out.println("Status: " + archived.getStatus()); // archived
```

### Recover Snapshot

```java
ConfigurationSnapshot recovered = configClient.recoverSnapshot("release-v1.0");
System.out.println("Status: " + recovered.getStatus()); // ready
```

### List All Snapshots

```java
import com.azure.data.appconfiguration.models.SnapshotSelector;

SnapshotSelector selector = new SnapshotSelector().setNameFilter("release-*");
PagedIterable<ConfigurationSnapshot> snapshots = configClient.listSnapshots(selector);

for (ConfigurationSnapshot snap : snapshots) {
    System.out.println(snap.getName() + " - " + snap.getStatus());
}
```

## Labels

### List Labels

```java
import com.azure.data.appconfiguration.models.SettingLabelSelector;

configClient.listLabels(new SettingLabelSelector().setNameFilter("*"))
    .forEach(label -> System.out.println("Label: " + label.getName()));
```

## Async Operations

```java
ConfigurationAsyncClient asyncClient = new ConfigurationClientBuilder()
    .connectionString(connectionString)
    .buildAsyncClient();

// Async list with reactive streams
asyncClient.listConfigurationSettings(new SettingSelector().setLabelFilter("Production"))
    .subscribe(
        setting -> System.out.println(setting.getKey() + " = " + setting.getValue()),
        error -> System.err.println("Error: " + error.getMessage()),
        () -> System.out.println("Completed")
    );
```

## Error Handling

```java
import com.azure.core.exception.HttpResponseException;

try {
    configClient.getConfigurationSetting("nonexistent", null);
} catch (HttpResponseException e) {
    if (e.getResponse().getStatusCode() == 404) {
        System.err.println("Setting not found");
    } else {
        System.err.println("Error: " + e.getMessage());
    }
}
```

## Best Practices

1. **Use labels** — Separate configurations by environment (Dev, Staging, Production)
2. **Use snapshots** — Create immutable snapshots for releases
3. **Feature flags** — Use for gradual rollouts and A/B testing
4. **Secret references** — Store sensitive values in Key Vault
5. **Conditional requests** — Use ETags for optimistic concurrency
6. **Read-only protection** — Lock critical production settings
7. **Use Entra ID** — Preferred over connection strings
8. **Async client** — Use for high-throughput scenarios

## Reference Links

| Resource | URL |
|----------|-----|
| Maven Package | https://central.sonatype.com/artifact/com.azure/azure-data-appconfiguration |
| GitHub | https://github.com/Azure/azure-sdk-for-java/tree/main/sdk/appconfiguration/azure-data-appconfiguration |
| API Documentation | https://aka.ms/java-docs |
| Product Docs | https://learn.microsoft.com/azure/azure-app-configuration |
| Samples | https://github.com/Azure/azure-sdk-for-java/tree/main/sdk/appconfiguration/azure-data-appconfiguration/src/samples |
| Troubleshooting | https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/appconfiguration/azure-data-appconfiguration/TROUBLESHOOTING.md |

## When to Use
This skill is applicable to execute the workflow or actions described in the overview.

---

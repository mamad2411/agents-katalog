---
name: azure-keyvault-appconfig-split
description: >
  Split secrets vs non-secret configuration for owned Azure apps: put secrets in Key
  Vault, feature flags and hierarchical app settings in Azure App Configuration,
  Key Vault references, managed identity access, refresh strategies, and rotation.
  Use when designing app config topology or untangling secrets mixed into App Config /
  appsettings — not for generic secrets scanning alone.
---

# Azure Key Vault vs App Configuration Split

## Scope And Authorization

- **In scope:** App Configuration stores, Key Vaults, and applications you own or are authorized to change.
- **Out of scope:** Reading production secrets without need; copying secrets into tickets/chat.
- Mis-placed secrets in App Config increase blast radius of config readers — treat as a security fix.
- Pair with `azure-keyvault-basics` for vault hardening; `code-quality-standards` for app wiring.

## When To Use

- Designing greenfield config: what goes in KV vs App Config vs environment.
- Secrets found in App Configuration key-values or labels.
- Implementing KV references from App Config or from App Service/Functions.
- Centralizing feature flags while keeping credentials out of the flag store.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Key Vault hardening (network, RBAC, purge) | `azure-keyvault-basics` |
| KV RBAC migration | `azure-keyvault-rbac-migration` |
| Managed identity federation | `azure-managed-identity-federated` |
| Org-wide secrets hygiene | `secrets-management-hygiene` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Store | Put here | Do not put here |
| --- | --- | --- |
| Key Vault | Passwords, API keys, connection strings, certificates, encryption keys | Feature flags, non-secret URLs, log levels |
| App Configuration | Feature flags, endpoint URLs, thresholds, non-secret hierarchy, labels per env | Raw client secrets, private keys |
| App settings / env | Bootstrap (endpoint of App Config), `ManagedIdentity` config | Long-lived secrets in source control |
| Tooling | `az appconfig`, `az keyvault`, Azure SDK `ConfigurationClient`, `SecretClient` |

## Workflow

### 1. Confirm scope and success criteria

1. Apps, environments (dev/stage/prod labels), vaults, App Config stores, authorization.
2. Success: zero raw secrets in App Config; apps resolve secrets via MI; rotation doesn’t require redeploy of non-secret config.
3. Inventory consumers of each key.

### 2. Inventory current configuration sources

```bash
az account show
az appconfig list -o table
az appconfig kv list --name "$APPCONFIG" -o table  # review names only; redact values
az keyvault list -o table
az keyvault secret list --vault-name "$VAULT" -o table
# Repo: grep for connection strings, ClientSecret, AccountKey
```

1. Flag App Config keys that look like secrets (`Password`, `ConnectionString`, `ApiKey`).
2. Map App Service/Function app settings vs App Config provider usage.
3. Note refresh intervals and sentinel keys.

### 3. Baseline classification

| Key example | Classification | Destination |
| --- | --- | --- |
| `Database:ConnectionString` | Secret | Key Vault |
| `Database:MaxRetry` | Config | App Config |
| `FeatureX:Enabled` | Flag | App Config feature flag |
| `Storage:AccountKey` | Secret | Key Vault (+ prefer MI) |
| `Service:BaseUrl` | Config | App Config |

### 4. Apply split and references

```bash
# Move secret to Key Vault
az keyvault secret set --vault-name "$VAULT" --name "Database--ConnectionString" --value "$SECRET"  # use secure input

# Delete raw secret from App Config after cutover
# az appconfig kv delete --name "$APPCONFIG" --key "Database:ConnectionString" --yes

# Optional: App Config Key Vault reference key (content type + URI JSON per docs)
# Or app uses SecretClient directly / App Service KV reference:
# @Microsoft.KeyVault(SecretUri=https://$VAULT.vault.azure.net/secrets/...)

# Non-secret config
az appconfig kv set --name "$APPCONFIG" --key "Database:MaxRetry" --value "3" --label "prod" -y
az appconfig feature set --name "$APPCONFIG" --feature "FeatureX" --label "prod" -y
```

**App pattern (.NET sketch):**

```csharp
builder.Configuration.AddAzureAppConfiguration(options =>
{
    options.Connect(new Uri(appConfigEndpoint), new DefaultAzureCredential())
        .ConfigureKeyVault(kv => kv.SetCredential(new DefaultAzureCredential()))
        .UseFeatureFlags()
        .ConfigureRefresh(r => r.Register("Sentinel", refreshAll: true));
});
```

1. Grant app MI: **App Configuration Data Reader** on store; **Key Vault Secrets User** on vault (or per-secret scope if used).
2. Network: private endpoints for both when required; same VNet rules discipline.
3. Rotation: rotate in KV; apps refresh via interval or sentinel; avoid baking secret versions into images.
4. Labels: `dev`/`prod` in App Config; separate vaults or secret prefixes per env.

### 5. Verify with evidence

```bash
# App Config list should not show raw secret values for moved keys
az appconfig kv list --name "$APPCONFIG" --label "prod" -o table
# App identity can read
az role assignment list --scope "$APPCONFIG_ID" -o table
az keyvault secret show --vault-name "$VAULT" --name "Database--ConnectionString" --query id -o tsv
# Runtime: app starts, pulls config; secret rotation test in nonprod
```

1. Grep CI logs for secret material — should be clean.
2. Negative: identity without KV role fails secret resolve; without App Config role fails flags.
3. Confirm feature flag toggle without redeploy.

### 6. Observe and harden

1. Monitor App Config throttling and KV 403 rates.
2. Alert on App Config keys matching secret patterns (policy/automation).
3. Audit who has **Data Owner** on App Config (can read referenced material depending on design).

### 7. Hand off

1. Written standard: classification table + naming conventions.
2. Onboarding template for new microservices.
3. Rotation runbook linking to KV procedures.

## Decision Flow

```text
Is it a credential, key, or confidential token?
  yes → Key Vault (+ prefer eliminate secret via MI)
  no  → Is it a feature flag?
          yes → App Config feature management
          no  → App Config key-value (label per env)
Bootstrap only → minimal env vars (endpoints, tenant)
```

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Secrets | KV + MI | Secret strings in App Config |
| Flags | App Config feature flags | Rebuild app to flip flag |
| Access | Separate roles for config vs secrets | Same broad Owner for all apps |
| Refresh | Sentinel + cache TTL | Restart all pods for every URL change |
| Naming | Hierarchical keys + labels | Flat `prod_db_pass` in config store |

## Output Checklist

- [ ] Inventory of config keys classified
- [ ] Secrets moved to Key Vault; raw copies removed from App Config
- [ ] App Config holds non-secrets + flags only
- [ ] MI roles least privilege on both services
- [ ] Refresh/rotation strategy documented
- [ ] Runtime verify + negative auth tests
- [ ] CI/repo scan clean of migrated secrets
- [ ] Team standard published
- [ ] `code-quality-standards` applied

## Rules

- Never store raw secrets in App Configuration.
- Prefer managed identity over connection strings when Azure resources allow.
- Least privilege separately for config readers and secret readers.
- Redact secret values in all logs and tickets.
- Authorized apps and stores only.

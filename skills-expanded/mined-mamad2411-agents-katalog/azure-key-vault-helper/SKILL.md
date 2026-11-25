---
name: azure-key-vault-helper
description: Manage secrets, keys, and certificates in Azure Key Vault — access patterns, secret rotation, RBAC, private networking, and SDK usage.
---

# Azure Key Vault Helper

Manage secrets, keys, and certificates in Azure Key Vault — access patterns, secret rotation, RBAC, private networking, and SDK usage.

## Trigger

Use this skill when the user asks to:
- Create, read, update, or delete Key Vault secrets, keys, or certificates
- Set up RBAC or access policies for Key Vault
- Reference Key Vault secrets from App Service, AKS, Azure Functions, or Bicep
- Configure private endpoints or network ACLs on a Key Vault
- Rotate secrets automatically or manually
- Diagnose access denied errors or missing secrets
- Set up soft-delete, purge protection, or backup/restore
- Query Key Vault audit logs

## Instructions

### Before advising

Ask (or infer) the following if not already provided:

1. **Object type** — secret, key, or certificate?
2. **Consumer** — App Service, AKS workload identity, Azure Function, pipeline, human operator?
3. **Auth model** — RBAC (recommended) or legacy access policies?
4. **Network** — public, service endpoint, or private endpoint?
5. **Rotation required** — is this a credential that must be rotated on a schedule?

### RBAC vs access policies

Always recommend **RBAC** (`enableRbacAuthorization: true`) for new vaults:

| | RBAC | Access Policies |
|---|------|----------------|
| Granularity | Per-secret, per-key, per-cert | Per-vault only |
| Audit | Azure RBAC audit log | Separate KV audit log |
| Conditional access | Yes | No |
| Max assignments | Azure RBAC limit (2000/scope) | 1024 per vault |
| Recommended | Yes | Legacy only |

Key Vault built-in RBAC roles:

| Role | GUID | Use |
|------|------|-----|
| Key Vault Administrator | `00482a5a-887f-4fb3-b363-3b7fe8e74483` | Full control (break-glass) |
| Key Vault Secrets Officer | `b86a8fe4-44ce-4948-aee5-eccb2c155cd7` | Create/delete secrets |
| Key Vault Secrets User | `4633458b-17de-408a-b874-0445c86b69e6` | Read secret value (apps) |
| Key Vault Crypto Officer | `14b46e9e-c2b7-41b4-b07b-48a6ebf60603` | Create/delete keys |
| Key Vault Crypto User | `12338af0-0e69-4776-bea7-57ae8d297424` | Use keys for crypto ops |
| Key Vault Certificate Officer | `a4417e6f-fecd-4de8-b567-7b0420556985` | Create/delete certificates |
| Key Vault Reader | `21090545-7ca7-4776-b22c-e363652d74d2` | Read metadata (not values) |

```bash
# Grant an app's managed identity read access to secrets
az role assignment create \
  --role "Key Vault Secrets User" \
  --assignee-object-id <principalId> \
  --assignee-principal-type ServicePrincipal \
  --scope "/subscriptions/{subId}/resourceGroups/myRG/providers/Microsoft.KeyVault/vaults/my-kv"

# Scope to a single secret (requires RBAC mode)
az role assignment create \
  --role "Key Vault Secrets User" \
  --assignee-object-id <principalId> \
  --scope "/subscriptions/{subId}/resourceGroups/myRG/providers/Microsoft.KeyVault/vaults/my-kv/secrets/my-secret"
```

### Secret operations

```bash
# Create / update a secret
az keyvault secret set \
  --vault-name my-kv \
  --name my-secret \
  --value "supersecret" \
  --expires "2027-01-01T00:00:00Z"   # optional expiry

# Read a secret value
az keyvault secret show \
  --vault-name my-kv \
  --name my-secret \
  --query value -o tsv

# List all secrets (metadata only, no values)
az keyvault secret list --vault-name my-kv --query "[].{Name:name, Enabled:attributes.enabled, Expires:attributes.expires}"

# List versions of a secret
az keyvault secret list-versions --vault-name my-kv --name my-secret

# Disable a secret version
az keyvault secret set-attributes \
  --vault-name my-kv \
  --name my-secret \
  --version <version-id> \
  --enabled false

# Delete (soft-delete — goes to deleted state, not permanently removed)
az keyvault secret delete --vault-name my-kv --name my-secret

# Purge (permanently remove — only if purge protection is disabled)
az keyvault secret purge --vault-name my-kv --name my-secret

# Recover a soft-deleted secret
az keyvault secret recover --vault-name my-kv --name my-secret
```

### Key operations

```bash
# Create an RSA key
az keyvault key create \
  --vault-name my-kv \
  --name my-key \
  --kty RSA \
  --size 4096 \
  --ops sign verify

# Create an EC key (ECDSA)
az keyvault key create \
  --vault-name my-kv \
  --name my-key \
  --kty EC \
  --curve P-384

# Encrypt / decrypt (small payloads only — use for wrapping symmetric keys)
az keyvault key encrypt --vault-name my-kv --name my-key --algorithm RSA-OAEP --value "$(echo -n 'plaintext' | base64)"
az keyvault key decrypt --vault-name my-kv --name my-key --algorithm RSA-OAEP --value "<ciphertext-base64>"

# Import an existing key (PEM)
az keyvault key import --vault-name my-kv --name my-key --pem-file ./key.pem
```

### Certificate operations

```bash
# Create a self-signed certificate
az keyvault certificate create \
  --vault-name my-kv \
  --name my-cert \
  --policy "$(az keyvault certificate get-default-policy)"

# Import a PFX certificate
az keyvault certificate import \
  --vault-name my-kv \
  --name my-cert \
  --file ./cert.pfx \
  --password <pfx-password>

# List certificates
az keyvault certificate list --vault-name my-kv

# Download certificate (public portion)
az keyvault certificate download \
  --vault-name my-kv \
  --name my-cert \
  --file ./cert.pem \
  --encoding PEM

# Check expiry
az keyvault certificate list \
  --vault-name my-kv \
  --query "[].{Name:name, Expires:attributes.expires}" \
  --output table
```

### Referencing secrets from Azure services

**App Service / Functions — Key Vault reference**
```
@Microsoft.KeyVault(SecretUri=https://my-kv.vault.azure.net/secrets/my-secret/)
# Pin to a version (avoids automatic pickup of new versions):
@Microsoft.KeyVault(SecretUri=https://my-kv.vault.azure.net/secrets/my-secret/abc123def456)
```

Set this as an app setting value. The app must have a system or user-assigned managed identity with `Key Vault Secrets User` on the vault.

**AKS — Secrets Store CSI Driver**
```yaml
apiVersion: secrets-store.csi.x-k8s.io/v1
kind: SecretProviderClass
metadata:
  name: azure-kvname-workload-identity
spec:
  provider: azure
  parameters:
    usePodIdentity: "false"
    useVMManagedIdentity: "false"
    clientID: "<managed-identity-client-id>"
    keyvaultName: my-kv
    cloudName: ""
    objects: |
      array:
        - |
          objectName: my-secret
          objectType: secret
          objectVersion: ""
    tenantId: "<tenant-id>"
```

**Azure DevOps pipeline — Key Vault task**
```yaml
- task: AzureKeyVault@2
  inputs:
    azureSubscription: 'my-service-connection'
    KeyVaultName: 'my-kv'
    SecretsFilter: 'my-secret,db-password'
    RunAsPreJob: true
```

**GitHub Actions — azure/get-keyvault-secrets**
```yaml
- uses: Azure/get-keyvault-secrets@v1
  with:
    keyvault: my-kv
    secrets: 'my-secret, db-password'
  id: kvsecrets

- run: echo "Secret is ${{ steps.kvsecrets.outputs.my-secret }}"
```

**Python SDK**
```python
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

credential = SecretClient(
    vault_url="https://my-kv.vault.azure.net",
    credential=DefaultAzureCredential()
)
secret = credential.get_secret("my-secret")
print(secret.value)
```

**.NET SDK**
```csharp
using Azure.Identity;
using Azure.Security.KeyVault.Secrets;

var client = new SecretClient(
    new Uri("https://my-kv.vault.azure.net"),
    new DefaultAzureCredential()
);
KeyVaultSecret secret = await client.GetSecretAsync("my-secret");
Console.WriteLine(secret.Value);
```

### Network security

**Private endpoint (recommended for prod)**
```bash
az network private-endpoint create \
  --name pe-my-kv \
  --resource-group myRG \
  --vnet-name myVNet \
  --subnet snet-endpoints \
  --private-connection-resource-id $(az keyvault show --name my-kv --query id -o tsv) \
  --group-id vault \
  --connection-name conn-my-kv

# Create private DNS zone and link
az network private-dns zone create --resource-group myRG --name privatelink.vaultcore.azure.net
az network private-dns link vnet create \
  --resource-group myRG \
  --zone-name privatelink.vaultcore.azure.net \
  --name link-my-vnet \
  --virtual-network myVNet \
  --registration-enabled false

az network private-endpoint dns-zone-group create \
  --resource-group myRG \
  --endpoint-name pe-my-kv \
  --name default \
  --private-dns-zone privatelink.vaultcore.azure.net \
  --zone-name vault
```

After creating the private endpoint, set `publicNetworkAccess: Disabled` on the vault.

**Network ACLs (service endpoints — less preferred)**
```bash
az keyvault network-rule add \
  --name my-kv \
  --resource-group myRG \
  --vnet-name myVNet \
  --subnet snet-app

az keyvault update \
  --name my-kv \
  --resource-group myRG \
  --default-action Deny \
  --bypass AzureServices
```

### Soft-delete and purge protection

```bash
# Check soft-delete status
az keyvault show --name my-kv --query properties.enableSoftDelete

# List soft-deleted vaults (subscription level)
az keyvault list-deleted

# Recover a soft-deleted vault
az keyvault recover --name my-kv --location eastus

# Purge a soft-deleted vault (only if purge protection is disabled)
az keyvault purge --name my-kv --location eastus
```

Soft-delete retention: 7–90 days (default 90). Once purge protection is enabled it cannot be disabled.

### Troubleshooting access denied

1. **Check the vault's auth model**: `az keyvault show --name my-kv --query properties.enableRbacAuthorization`
   - If `true` → check RBAC role assignments
   - If `false` → check access policies
2. **RBAC**: `az role assignment list --scope <vault-id> --assignee <principalId>`
3. **Access policies**: `az keyvault show --name my-kv --query properties.accessPolicies`
4. **Network**: confirm the caller's IP/VNet is in the allowlist or using private endpoint
5. **Firewall bypass**: Azure services must be in the `bypass: AzureServices` list or the trusted services list
6. **Managed identity**: confirm the app actually has an identity assigned and it's the same `principalId` in the role assignment
7. **Audit logs**: query `AzureDiagnostics | where ResourceProvider == "MICROSOFT.KEYVAULT" and ResultSignature == "Forbidden"`

## References

- [Key Vault CLI & SDK cheatsheet](./references/keyvault-cheatsheet.md)
- [Access patterns: RBAC, managed identity, workload identity](./references/access-patterns.md)
- [Secret rotation patterns](./references/secret-rotation.md)
- Official docs: https://learn.microsoft.com/en-us/azure/key-vault/

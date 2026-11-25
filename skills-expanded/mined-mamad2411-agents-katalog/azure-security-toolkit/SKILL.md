---
name: azure-security-toolkit
description: Consolidated toolkit for azure-security. Covers azure-security-keyvault-keys-dotnet, azure-security-keyvault-secrets-java, azure-security-keyvault-keys-java
---
# Azure Security Toolkit

## Core Capabilities
# Azure Security Toolkit

# Azure.Security.KeyVault.Keys (.NET)

Client library for managing cryptographic keys in Azure Key Vault and Managed HSM.

## Installation

```bash
dotnet add package Azure.Security.KeyVault.Keys
dotnet add package Azure.Identity
```

**Current Version**: 4.7.0 (stable)

## Environment Variables

```bash
KEY_VAULT_NAME=<your-key-vault-name>
# Or full URI
AZURE_KEYVAULT_URL=https://<vault-name>.vault.azure.net
```

## Client Hierarchy

```
KeyClient (key management)
├── CreateKey / CreateRsaKey / CreateEcKey
├── GetKey / GetKeys
├── UpdateKeyProperties
├── DeleteKey / PurgeDeletedKey
├── BackupKey / RestoreKey
└── GetCryptographyClient() → CryptographyClient

CryptographyClient (cryptographic operations)
├── Encrypt / Decrypt
├── WrapKey / UnwrapKey
├── Sign / Verify
└── SignData / VerifyData

KeyResolver (key resolution)
└── Resolve(keyId) → CryptographyClient
```

## Authentication

### DefaultAzureCredential (Recommended)

```csharp
using Azure.Identity;
using Azure.Security.KeyVault.Keys;

var keyVaultName = Environment.GetEnvironmentVariable("KEY_VAULT_NAME");
var kvUri = $"https://{keyVaultName}.vault.azure.net";

var client = new KeyClient(new Uri(kvUri), new DefaultAzureCredential());
```

### Service Principal

```csharp
var credential = new ClientSecretCredential(
    tenantId: "<tenant-id>",
    clientId: "<client-id>",
    clientSecret: "<client-secret>");

var client = new KeyClient(new Uri(kvUri), credential);
```

## Key Management

### Create Keys

```csharp
// Create RSA key
KeyVaultKey rsaKey = await client.CreateKeyAsync("my-rsa-key", KeyType.Rsa);
Console.WriteLine($"Created key: {rsaKey.Name}, Type: {rsaKey.KeyType}");

// Create RSA key with options
var rsaOptions = new CreateRsaKeyOptions("my-rsa-key-2048")
{
    KeySize = 2048,
    HardwareProtected = false, // true for HSM-backed
    ExpiresOn = DateTimeOffset.UtcNow.AddYears(1),
    NotBefore = DateTimeOffset.UtcNow,
    Enabled = true
};
rsaOptions.KeyOperations.Add(KeyOperation.Encrypt);
rsaOptions.KeyOperations.Add(KeyOperation.Decrypt);

KeyVaultKey rsaKey2 = await client.CreateRsaKeyAsync(rsaOptions);

// Create EC key
var ecOptions = new CreateEcKeyOptions("my-ec-key")
{
    CurveName = KeyCurveName.P256,
    HardwareProtected = true // HSM-backed
};
KeyVaultKey ecKey = await client.CreateEcKeyAsync(ecOptions);

// Create Oct (symmetric) key for wrap/unwrap
var octOptions = new CreateOctKeyOptions("my-oct-key")
{
    KeySize = 256,
    HardwareProtected = true
};
KeyVaultKey octKey = await client.CreateOctKeyAsync(octOptions);
```

### Retrieve Keys

```csharp
// Get specific key (latest version)
KeyVaultKey key = await client.GetKeyAsync("my-rsa-key");
Console.WriteLine($"Key ID: {key.Id}");
Console.WriteLine($"Key Type: {key.KeyType}");
Console.WriteLine($"Version: {key.Properties.Version}");

// Get specific version
KeyVaultKey keyVersion = await client.GetKeyAsync("my-rsa-key", "version-id");

// List all keys
await foreach (KeyProperties keyProps in client.GetPropertiesOfKeysAsync())
{
    Console.WriteLine($"Key: {keyProps.Name}, Enabled: {keyProps.Enabled}");
}

// List key versions
await foreach (KeyProperties version in client.GetPropertiesOfKeyVersionsAsync("my-rsa-key"))
{
    Console.WriteLine($"Version: {version.Version}, Created: {version.CreatedOn}");
}
```

### Update Key Properties

```csharp
KeyVaultKey key = await client.GetKeyAsync("my-rsa-key");

key.Properties.ExpiresOn = DateTimeOffset.UtcNow.AddYears(2);
key.Properties.Tags["environment"] = "production";

KeyVaultKey updatedKey = await client.UpdateKeyPropertiesAsync(key.Properties);
```

### Delete and Purge Keys

```csharp
// Start delete operation
DeleteKeyOperation operation = await client.StartDeleteKeyAsync("my-rsa-key");

// Wait for deletion to complete (required before purge)
await operation.WaitForCompletionAsync();
Console.WriteLine($"Deleted key scheduled purge date: {operation.Value.ScheduledPurgeDate}");

// Purge immediately (if soft-delete is enabled)
await client.PurgeDeletedKeyAsync("my-rsa-key");

// Or recover deleted key
KeyVaultKey recoveredKey = await client.StartRecoverDeletedKeyAsync("my-rsa-key");
```

### Backup and Restore

```csharp
// Backup key
byte[] backup = await client.BackupKeyAsync("my-rsa-key");
await File.WriteAllBytesAsync("key-backup.bin", backup);

// Restore key
byte[] backupData = await File.ReadAllBytesAsync("key-backup.bin");
KeyVaultKey restoredKey = await client.RestoreKeyBackupAsync(backupData);
```

## Cryptographic Operations

### Get CryptographyClient

```csharp
// From KeyClient
KeyVaultKey key = await client.GetKeyAsync("my-rsa-key");
CryptographyClient cryptoClient = client.GetCryptographyClient(
    key.Name, 
    key.Properties.Version);

// Or create directly with key ID
CryptographyClient cryptoClient = new CryptographyClient(
    new Uri("https://myvault.vault.azure.net/keys/my-rsa-key/version"),
    new DefaultAzureCredential());
```

### Encrypt and Decrypt

```csharp
byte[] plaintext = Encoding.UTF8.GetBytes("Secret message to encrypt");

// Encrypt
EncryptResult encryptResult = await cryptoClient.EncryptAsync(
    EncryptionAlgorithm.RsaOaep256, 
    plaintext);
Console.WriteLine($"Encrypted: {Convert.ToBase64String(encryptResult.Ciphertext)}");

// Decrypt
DecryptResult decryptResult = await cryptoClient.DecryptAsync(
    EncryptionAlgorithm.RsaOaep256, 
    encryptResult.Ciphertext);
string decrypted = Encoding.UTF8.GetString(decryptResult.Plaintext);
Console.WriteLine($"Decrypted: {decrypted}");
```

### Wrap and Unwrap Keys

```csharp
// Key to wrap (e.g., AES key)
byte[] keyToWrap = new byte[32]; // 256-bit key
RandomNumberGenerator.Fill(keyToWrap);

// Wrap key
WrapResult wrapResult = await cryptoClient.WrapKeyAsync(
    KeyWrapAlgorithm.RsaOaep256, 
    keyToWrap);

// Unwrap key
UnwrapResult unwrapResult = await cryptoClient.UnwrapKeyAsync(
    KeyWrapAlgorithm.RsaOaep256, 
    wrapResult.EncryptedKey);
```

### Sign and Verify

```csharp
// Data to sign
byte[] data = Encoding.UTF8.GetBytes("Data to sign");

// Sign data (computes hash internally)
SignResult signResult = await cryptoClient.SignDataAsync(
    SignatureAlgorithm.RS256, 
    data);

// Verify signature
VerifyResult verifyResult = await cryptoClient.VerifyDataAsync(
    SignatureAlgorithm.RS256, 
    data, 
    signResult.Signature);
Console.WriteLine($"Signature valid: {verifyResult.IsValid}");

// Or sign pre-computed hash
using var sha256 = SHA256.Create();
byte[] hash = sha256.ComputeHash(data);

SignResult signHashResult = await cryptoClient.SignAsync(
    SignatureAlgorithm.RS256, 
    hash);
```

## Key Resolver

```csharp
using Azure.Security.KeyVault.Keys.Cryptography;

var resolver = new KeyResolver(new DefaultAzureCredential());

// Resolve key by ID to get CryptographyClient
CryptographyClient cryptoClient = await resolver.ResolveAsync(
    new Uri("https://myvault.vault.azure.net/keys/my-key/version"));

// Use for encryption
EncryptResult result = await cryptoClient.EncryptAsync(
    EncryptionAlgorithm.RsaOaep256, 
    plaintext);
```

## Key Rotation

```csharp
// Rotate key (creates new version)
KeyVaultKey rotatedKey = await client.RotateKeyAsync("my-rsa-key");
Console.WriteLine($"New version: {rotatedKey.Properties.Version}");

// Get rotation policy
KeyRotationPolicy policy = await client.GetKeyRotationPolicyAsync("my-rsa-key");

// Update rotation policy
policy.ExpiresIn = "P90D"; // 90 days
policy.LifetimeActions.Add(new KeyRotationLifetimeAction
{
    Action = KeyRotationPolicyAction.Rotate,
    TimeBeforeExpiry = "P30D" // Rotate 30 days before expiry
});

await client.UpdateKeyRotationPolicyAsync("my-rsa-key", policy);
```

## Key Types Reference

| Type | Purpose |
|------|---------|
| `KeyClient` | Key management operations |
| `CryptographyClient` | Cryptographic operations |
| `KeyResolver` | Resolve key ID to CryptographyClient |
| `KeyVaultKey` | Key with cryptographic material |
| `KeyProperties` | Key metadata (no crypto material) |
| `CreateRsaKeyOptions` | RSA key creation options |
| `CreateEcKeyOptions` | EC key creation options |
| `CreateOctKeyOptions` | Symmetric key options |
| `EncryptResult` | Encryption result |
| `DecryptResult` | Decryption result |
| `SignResult` | Signing result |
| `VerifyResult` | Verification result |
| `WrapResult` | Key wrap result |
| `UnwrapResult` | Key unwrap result |

## Algorithms Reference

### Encryption Algorithms
| Algorithm | Key Type | Description |
|-----------|----------|-------------|
| `RsaOaep` | RSA | RSA-OAEP |
| `RsaOaep256` | RSA | RSA-OAEP-256 |
| `Rsa15` | RSA | RSA 1.5 (legacy) |
| `A128Gcm` | Oct | AES-128-GCM |
| `A256Gcm` | Oct | AES-256-GCM |

### Signature Algorithms
| Algorithm | Key Type | Description |
|-----------|----------|-------------|
| `RS256` | RSA | RSASSA-PKCS1-v1_5 SHA-256 |
| `RS384` | RSA | RSASSA-PKCS1-v1_5 SHA-384 |
| `RS512` | RSA | RSASSA-PKCS1-v1_5 SHA-512 |
| `PS256` | RSA | RSASSA-PSS SHA-256 |
| `ES256` | EC | ECDSA P-256 SHA-256 |
| `ES384` | EC | ECDSA P-384 SHA-384 |
| `ES512` | EC | ECDSA P-521 SHA-512 |

### Key Wrap Algorithms
| Algorithm | Key Type | Description |
|-----------|----------|-------------|
| `RsaOaep` | RSA | RSA-OAEP |
| `RsaOaep256` | RSA | RSA-OAEP-256 |
| `A128KW` | Oct | AES-128 Key Wrap |
| `A256KW` | Oct | AES-256 Key Wrap |

## Best Practices

1. **Use Managed Identity** — Prefer `DefaultAzureCredential` over secrets
2. **Enable soft-delete** — Protect against accidental deletion
3. **Use HSM-backed keys** — Set `HardwareProtected = true` for sensitive keys
4. **Implement key rotation** — Use automatic rotation policies
5. **Limit key operations** — Only enable required `KeyOperations`
6. **Set expiration dates** — Always set `ExpiresOn` for keys
7. **Use specific versions** — Pin to versions in production
8. **Cache CryptographyClient** — Reuse for multiple operations

## Error Handling

```csharp
using Azure;

try
{
    KeyVaultKey key = await client.GetKeyAsync("my-key");
}
catch (RequestFailedException ex) when (ex.Status == 404)
{
    Console.WriteLine("Key not found");
}
catch (RequestFailedException ex) when (ex.Status == 403)
{
    Console.WriteLine("Access denied - check RBAC permissions");
}
catch (RequestFailedException ex)
{
    Console.WriteLine($"Key Vault error: {ex.Status} - {ex.Message}");
}
```

## Required RBAC Roles

| Role | Permissions |
|------|-------------|
| Key Vault Crypto Officer | Full key management |
| Key Vault Crypto User | Use keys for crypto operations |
| Key Vault Reader | Read key metadata |

## Related SDKs

| SDK | Purpose | Install |
|-----|---------|---------|
| `Azure.Security.KeyVault.Keys` | Keys (this SDK) | `dotnet add package Azure.Security.KeyVault.Keys` |
| `Azure.Security.KeyVault.Secrets` | Secrets | `dotnet add package Azure.Security.KeyVault.Secrets` |
| `Azure.Security.KeyVault.Certificates` | Certificates | `dotnet add package Azure.Security.KeyVault.Certificates` |
| `Azure.Identity` | Authentication | `dotnet add package Azure.Identity` |

## Reference Links

| Resource | URL |
|----------|-----|
| NuGet Package | https://www.nuget.org/packages/Azure.Security.KeyVault.Keys |
| API Reference | https://learn.microsoft.com/dotnet/api/azure.security.keyvault.keys |
| Quickstart | https://learn.microsoft.com/azure/key-vault/keys/quick-create-net |
| GitHub Source | https://github.com/Azure/azure-sdk-for-net/tree/main/sdk/keyvault/Azure.Security.KeyVault.Keys |

## When to Use
This skill is applicable to execute the workflow or actions described in the overview.

---

# Azure Key Vault Secrets (Java)

Securely store and manage secrets like passwords, API keys, and connection strings.

## Installation

```xml
<dependency>
    <groupId>com.azure</groupId>
    <artifactId>azure-security-keyvault-secrets</artifactId>
    <version>4.9.0</version>
</dependency>
```

## Client Creation

```java
import com.azure.security.keyvault.secrets.SecretClient;
import com.azure.security.keyvault.secrets.SecretClientBuilder;
import com.azure.identity.DefaultAzureCredentialBuilder;

// Sync client
SecretClient secretClient = new SecretClientBuilder()
    .vaultUrl("https://<vault-name>.vault.azure.net")
    .credential(new DefaultAzureCredentialBuilder().build())
    .buildClient();

// Async client
SecretAsyncClient secretAsyncClient = new SecretClientBuilder()
    .vaultUrl("https://<vault-name>.vault.azure.net")
    .credential(new DefaultAzureCredentialBuilder().build())
    .buildAsyncClient();
```

## Create/Set Secret

```java
import com.azure.security.keyvault.secrets.models.KeyVaultSecret;

// Simple secret
KeyVaultSecret secret = secretClient.setSecret("database-password", "P@ssw0rd123!");
System.out.println("Secret name: " + secret.getName());
System.out.println("Secret ID: " + secret.getId());

// Secret with options
KeyVaultSecret secretWithOptions = secretClient.setSecret(
    new KeyVaultSecret("api-key", "sk_live_abc123xyz")
        .setProperties(new SecretProperties()
            .setContentType("application/json")
            .setExpiresOn(OffsetDateTime.now().plusYears(1))
            .setNotBefore(OffsetDateTime.now())
            .setEnabled(true)
            .setTags(Map.of(
                "environment", "production",
                "service", "payment-api"
            ))
        )
);
```

## Get Secret

```java
// Get latest version
KeyVaultSecret secret = secretClient.getSecret("database-password");
String value = secret.getValue();
System.out.println("Secret value: " + value);

// Get specific version
KeyVaultSecret specificVersion = secretClient.getSecret("database-password", "<version-id>");

// Get only properties (no value)
SecretProperties props = secretClient.getSecret("database-password").getProperties();
System.out.println("Enabled: " + props.isEnabled());
System.out.println("Created: " + props.getCreatedOn());
```

## Update Secret Properties

```java
// Get secret
KeyVaultSecret secret = secretClient.getSecret("api-key");

// Update properties (cannot update value - create new version instead)
secret.getProperties()
    .setEnabled(false)
    .setExpiresOn(OffsetDateTime.now().plusMonths(6))
    .setTags(Map.of("status", "rotating"));

SecretProperties updated = secretClient.updateSecretProperties(secret.getProperties());
System.out.println("Updated: " + updated.getUpdatedOn());
```

## List Secrets

```java
import com.azure.core.util.paging.PagedIterable;
import com.azure.security.keyvault.secrets.models.SecretProperties;

// List all secrets (properties only, no values)
for (SecretProperties secretProps : secretClient.listPropertiesOfSecrets()) {
    System.out.println("Secret: " + secretProps.getName());
    System.out.println("  Enabled: " + secretProps.isEnabled());
    System.out.println("  Created: " + secretProps.getCreatedOn());
    System.out.println("  Content-Type: " + secretProps.getContentType());
    
    // Get value if needed
    if (secretProps.isEnabled()) {
        KeyVaultSecret fullSecret = secretClient.getSecret(secretProps.getName());
        System.out.println("  Value: " + fullSecret.getValue().substring(0, 5) + "...");
    }
}

// List versions of a secret
for (SecretProperties version : secretClient.listPropertiesOfSecretVersions("database-password")) {
    System.out.println("Version: " + version.getVersion());
    System.out.println("Created: " + version.getCreatedOn());
    System.out.println("Enabled: " + version.isEnabled());
}
```

## Delete Secret

```java
import com.azure.core.util.polling.SyncPoller;
import com.azure.security.keyvault.secrets.models.DeletedSecret;

// Begin delete (returns poller for soft-delete enabled vaults)
SyncPoller<DeletedSecret, Void> deletePoller = secretClient.beginDeleteSecret("old-secret");

// Wait for deletion
DeletedSecret deletedSecret = deletePoller.poll().getValue();
System.out.println("Deleted on: " + deletedSecret.getDeletedOn());
System.out.println("Scheduled purge: " + deletedSecret.getScheduledPurgeDate());

deletePoller.waitForCompletion();
```

## Recover Deleted Secret

```java
// List deleted secrets
for (DeletedSecret deleted : secretClient.listDeletedSecrets()) {
    System.out.println("Deleted: " + deleted.getName());
    System.out.println("Deletion date: " + deleted.getDeletedOn());
}

// Recover deleted secret
SyncPoller<KeyVaultSecret, Void> recoverPoller = secretClient.beginRecoverDeletedSecret("old-secret");
recoverPoller.waitForCompletion();

KeyVaultSecret recovered = recoverPoller.getFinalResult();
System.out.println("Recovered: " + recovered.getName());
```

## Purge Deleted Secret

```java
// Permanently delete (cannot be recovered)
secretClient.purgeDeletedSecret("old-secret");

// Get deleted secret info first
DeletedSecret deleted = secretClient.getDeletedSecret("old-secret");
System.out.println("Will purge: " + deleted.getName());
secretClient.purgeDeletedSecret("old-secret");
```

## Backup and Restore

```java
// Backup secret (all versions)
byte[] backup = secretClient.backupSecret("important-secret");

// Save to file
Files.write(Paths.get("secret-backup.blob"), backup);

// Restore from backup
byte[] backupData = Files.readAllBytes(Paths.get("secret-backup.blob"));
KeyVaultSecret restored = secretClient.restoreSecretBackup(backupData);
System.out.println("Restored: " + restored.getName());
```

## Async Operations

```java
SecretAsyncClient asyncClient = new SecretClientBuilder()
    .vaultUrl("https://<vault>.vault.azure.net")
    .credential(new DefaultAzureCredentialBuilder().build())
    .buildAsyncClient();

// Set secret async
asyncClient.setSecret("async-secret", "async-value")
    .subscribe(
        secret -> System.out.println("Created: " + secret.getName()),
        error -> System.out.println("Error: " + error.getMessage())
    );

// Get secret async
asyncClient.getSecret("async-secret")
    .subscribe(secret -> System.out.println("Value: " + secret.getValue()));

// List secrets async
asyncClient.listPropertiesOfSecrets()
    .doOnNext(props -> System.out.println("Found: " + props.getName()))
    .subscribe();
```

## Configuration Patterns

### Load Multiple Secrets

```java
public class ConfigLoader {
    private final SecretClient client;
    
    public ConfigLoader(String vaultUrl) {
        this.client = new SecretClientBuilder()
            .vaultUrl(vaultUrl)
            .credential(new DefaultAzureCredentialBuilder().build())
            .buildClient();
    }
    
    public Map<String, String> loadSecrets(List<String> secretNames) {
        Map<String, String> secrets = new HashMap<>();
        for (String name : secretNames) {
            try {
                KeyVaultSecret secret = client.getSecret(name);
                secrets.put(name, secret.getValue());
            } catch (ResourceNotFoundException e) {
                System.out.println("Secret not found: " + name);
            }
        }
        return secrets;
    }
}

// Usage
ConfigLoader loader = new ConfigLoader("https://my-vault.vault.azure.net");
Map<String, String> config = loader.loadSecrets(
    Arrays.asList("db-connection-string", "api-key", "jwt-secret")
);
```

### Secret Rotation Pattern

```java
public void rotateSecret(String secretName, String newValue) {
    // Get current secret
    KeyVaultSecret current = secretClient.getSecret(secretName);
    
    // Disable old version
    current.getProperties().setEnabled(false);
    secretClient.updateSecretProperties(current.getProperties());
    
    // Create new version with new value
    KeyVaultSecret newSecret = secretClient.setSecret(secretName, newValue);
    System.out.println("Rotated to version: " + newSecret.getProperties().getVersion());
}
```

## Error Handling

```java
import com.azure.core.exception.HttpResponseException;
import com.azure.core.exception.ResourceNotFoundException;

try {
    KeyVaultSecret secret = secretClient.getSecret("my-secret");
    System.out.println("Value: " + secret.getValue());
} catch (ResourceNotFoundException e) {
    System.out.println("Secret not found");
} catch (HttpResponseException e) {
    int status = e.getResponse().getStatusCode();
    if (status == 403) {
        System.out.println("Access denied - check permissions");
    } else if (status == 429) {
        System.out.println("Rate limited - retry later");
    } else {
        System.out.println("HTTP error: " + status);
    }
}
```

## Secret Properties

| Property | Description |
|----------|-------------|
| `name` | Secret name |
| `value` | Secret value (string) |
| `id` | Full identifier URL |
| `contentType` | MIME type hint |
| `enabled` | Whether secret can be retrieved |
| `notBefore` | Activation time |
| `expiresOn` | Expiration time |
| `createdOn` | Creation timestamp |
| `updatedOn` | Last update timestamp |
| `recoveryLevel` | Soft-delete recovery level |
| `tags` | User-defined metadata |

## Environment Variables

```bash
AZURE_KEYVAULT_URL=https://<vault-name>.vault.azure.net
```

## Best Practices

1. **Enable Soft Delete** - Protects against accidental deletion
2. **Use Tags** - Tag secrets with environment, service, owner
3. **Set Expiration** - Use `setExpiresOn()` for credentials that should rotate
4. **Content Type** - Set `contentType` to indicate format (e.g., `application/json`)
5. **Version Management** - Don't delete old versions immediately during rotation
6. **Access Logging** - Enable diagnostic logging on Key Vault
7. **Least Privilege** - Use separate vaults for different environments

## Common Secret Types

```java
// Database connection string
secretClient.setSecret(new KeyVaultSecret("db-connection", 
    "Server=myserver.database.windows.net;Database=mydb;...")
    .setProperties(new SecretProperties()
        .setContentType("text/plain")
        .setTags(Map.of("type", "connection-string"))));

// API key
secretClient.setSecret(new KeyVaultSecret("stripe-api-key", "sk_live_...")
    .setProperties(new SecretProperties()
        .setContentType("text/plain")
        .setExpiresOn(OffsetDateTime.now().plusYears(1))));

// JSON configuration
secretClient.setSecret(new KeyVaultSecret("app-config", 
    "{\"endpoint\":\"https://...\",\"key\":\"...\"}")
    .setProperties(new SecretProperties()
        .setContentType("application/json")));

// Certificate password
secretClient.setSecret(new KeyVaultSecret("cert-password", "CertP@ss!")
    .setProperties(new SecretProperties()
        .setContentType("text/plain")
        .setTags(Map.of("certificate", "my-cert"))));
```

## Trigger Phrases

- "Key Vault secrets Java", "secret management Java"
- "store password", "store API key", "connection string"
- "retrieve secret", "rotate secret"
- "Azure secrets", "vault secrets"

## When to Use
This skill is applicable to execute the workflow or actions described in the overview.

---

# Azure Key Vault Keys (Java)

Manage cryptographic keys and perform cryptographic operations in Azure Key Vault and Managed HSM.

## Installation

```xml
<dependency>
    <groupId>com.azure</groupId>
    <artifactId>azure-security-keyvault-keys</artifactId>
    <version>4.9.0</version>
</dependency>
```

## Client Creation

```java
import com.azure.security.keyvault.keys.KeyClient;
import com.azure.security.keyvault.keys.KeyClientBuilder;
import com.azure.security.keyvault.keys.cryptography.CryptographyClient;
import com.azure.security.keyvault.keys.cryptography.CryptographyClientBuilder;
import com.azure.identity.DefaultAzureCredentialBuilder;

// Key management client
KeyClient keyClient = new KeyClientBuilder()
    .vaultUrl("https://<vault-name>.vault.azure.net")
    .credential(new DefaultAzureCredentialBuilder().build())
    .buildClient();

// Async client
KeyAsyncClient keyAsyncClient = new KeyClientBuilder()
    .vaultUrl("https://<vault-name>.vault.azure.net")
    .credential(new DefaultAzureCredentialBuilder().build())
    .buildAsyncClient();

// Cryptography client (for encrypt/decrypt/sign/verify)
CryptographyClient cryptoClient = new CryptographyClientBuilder()
    .keyIdentifier("https://<vault-name>.vault.azure.net/keys/<key-name>/<key-version>")
    .credential(new DefaultAzureCredentialBuilder().build())
    .buildClient();
```

## Key Types

| Type | Description |
|------|-------------|
| `RSA` | RSA key (2048, 3072, 4096 bits) |
| `RSA_HSM` | RSA key in HSM |
| `EC` | Elliptic Curve key |
| `EC_HSM` | Elliptic Curve key in HSM |
| `OCT` | Symmetric key (Managed HSM only) |
| `OCT_HSM` | Symmetric key in HSM |

## Create Keys

### Create RSA Key

```java
import com.azure.security.keyvault.keys.models.*;

// Simple RSA key
KeyVaultKey rsaKey = keyClient.createRsaKey(new CreateRsaKeyOptions("my-rsa-key")
    .setKeySize(2048));

System.out.println("Key name: " + rsaKey.getName());
System.out.println("Key ID: " + rsaKey.getId());
System.out.println("Key type: " + rsaKey.getKeyType());

// RSA key with options
KeyVaultKey rsaKeyWithOptions = keyClient.createRsaKey(new CreateRsaKeyOptions("my-rsa-key-2")
    .setKeySize(4096)
    .setExpiresOn(OffsetDateTime.now().plusYears(1))
    .setNotBefore(OffsetDateTime.now())
    .setEnabled(true)
    .setKeyOperations(KeyOperation.ENCRYPT, KeyOperation.DECRYPT, 
                       KeyOperation.WRAP_KEY, KeyOperation.UNWRAP_KEY)
    .setTags(Map.of("environment", "production")));

// HSM-backed RSA key
KeyVaultKey hsmKey = keyClient.createRsaKey(new CreateRsaKeyOptions("my-hsm-key")
    .setKeySize(2048)
    .setHardwareProtected(true));
```

### Create EC Key

```java
// EC key with P-256 curve
KeyVaultKey ecKey = keyClient.createEcKey(new CreateEcKeyOptions("my-ec-key")
    .setCurveName(KeyCurveName.P_256));

// EC key with other curves
KeyVaultKey ecKey384 = keyClient.createEcKey(new CreateEcKeyOptions("my-ec-key-384")
    .setCurveName(KeyCurveName.P_384));

KeyVaultKey ecKey521 = keyClient.createEcKey(new CreateEcKeyOptions("my-ec-key-521")
    .setCurveName(KeyCurveName.P_521));

// HSM-backed EC key
KeyVaultKey ecHsmKey = keyClient.createEcKey(new CreateEcKeyOptions("my-ec-hsm-key")
    .setCurveName(KeyCurveName.P_256)
    .setHardwareProtected(true));
```

### Create Symmetric Key (Managed HSM only)

```java
KeyVaultKey octKey = keyClient.createOctKey(new CreateOctKeyOptions("my-symmetric-key")
    .setKeySize(256)
    .setHardwareProtected(true));
```

## Get Key

```java
// Get latest version
KeyVaultKey key = keyClient.getKey("my-key");

// Get specific version
KeyVaultKey keyVersion = keyClient.getKey("my-key", "<version-id>");

// Get only key properties (no key material)
KeyProperties keyProps = keyClient.getKey("my-key").getProperties();
```

## Update Key Properties

```java
KeyVaultKey key = keyClient.getKey("my-key");

// Update properties
key.getProperties()
    .setEnabled(false)
    .setExpiresOn(OffsetDateTime.now().plusMonths(6))
    .setTags(Map.of("status", "archived"));

KeyVaultKey updatedKey = keyClient.updateKeyProperties(key.getProperties(),
    KeyOperation.ENCRYPT, KeyOperation.DECRYPT);
```

## List Keys

```java
import com.azure.core.util.paging.PagedIterable;

// List all keys
for (KeyProperties keyProps : keyClient.listPropertiesOfKeys()) {
    System.out.println("Key: " + keyProps.getName());
    System.out.println("  Enabled: " + keyProps.isEnabled());
    System.out.println("  Created: " + keyProps.getCreatedOn());
}

// List key versions
for (KeyProperties version : keyClient.listPropertiesOfKeyVersions("my-key")) {
    System.out.println("Version: " + version.getVersion());
    System.out.println("Created: " + version.getCreatedOn());
}
```

## Delete Key

```java
import com.azure.core.util.polling.SyncPoller;

// Begin delete (soft-delete enabled vaults)
SyncPoller<DeletedKey, Void> deletePoller = keyClient.beginDeleteKey("my-key");

// Wait for deletion
DeletedKey deletedKey = deletePoller.poll().getValue();
System.out.println("Deleted: " + deletedKey.getDeletedOn());

deletePoller.waitForCompletion();

// Purge deleted key (permanent deletion)
keyClient.purgeDeletedKey("my-key");

// Recover deleted key
SyncPoller<KeyVaultKey, Void> recoverPoller = keyClient.beginRecoverDeletedKey("my-key");
recoverPoller.waitForCompletion();
```

## Cryptographic Operations

### Encrypt/Decrypt

```java
import com.azure.security.keyvault.keys.cryptography.models.*;

CryptographyClient cryptoClient = new CryptographyClientBuilder()
    .keyIdentifier("https://<vault>.vault.azure.net/keys/<key-name>")
    .credential(new DefaultAzureCredentialBuilder().build())
    .buildClient();

byte[] plaintext = "Hello, World!".getBytes(StandardCharsets.UTF_8);

// Encrypt
EncryptResult encryptResult = cryptoClient.encrypt(EncryptionAlgorithm.RSA_OAEP, plaintext);
byte[] ciphertext = encryptResult.getCipherText();
System.out.println("Ciphertext length: " + ciphertext.length);

// Decrypt
DecryptResult decryptResult = cryptoClient.decrypt(EncryptionAlgorithm.RSA_OAEP, ciphertext);
String decrypted = new String(decryptResult.getPlainText(), StandardCharsets.UTF_8);
System.out.println("Decrypted: " + decrypted);
```

### Sign/Verify

```java
import java.security.MessageDigest;

// Create digest of data
byte[] data = "Data to sign".getBytes(StandardCharsets.UTF_8);
MessageDigest md = MessageDigest.getInstance("SHA-256");
byte[] digest = md.digest(data);

// Sign
SignResult signResult = cryptoClient.sign(SignatureAlgorithm.RS256, digest);
byte[] signature = signResult.getSignature();

// Verify
VerifyResult verifyResult = cryptoClient.verify(SignatureAlgorithm.RS256, digest, signature);
System.out.println("Valid signature: " + verifyResult.isValid());
```

### Wrap/Unwrap Key

```java
// Key to wrap (e.g., AES key)
byte[] keyToWrap = new byte[32];  // 256-bit key
new SecureRandom().nextBytes(keyToWrap);

// Wrap
WrapResult wrapResult = cryptoClient.wrapKey(KeyWrapAlgorithm.RSA_OAEP, keyToWrap);
byte[] wrappedKey = wrapResult.getEncryptedKey();

// Unwrap
UnwrapResult unwrapResult = cryptoClient.unwrapKey(KeyWrapAlgorithm.RSA_OAEP, wrappedKey);
byte[] unwrappedKey = unwrapResult.getKey();
```

## Backup and Restore

```java
// Backup
byte[] backup = keyClient.backupKey("my-key");

// Save backup to file
Files.write(Paths.get("key-backup.blob"), backup);

// Restore
byte[] backupData = Files.readAllBytes(Paths.get("key-backup.blob"));
KeyVaultKey restoredKey = keyClient.restoreKeyBackup(backupData);
```

## Key Rotation

```java
// Rotate to new version
KeyVaultKey rotatedKey = keyClient.rotateKey("my-key");
System.out.println("New version: " + rotatedKey.getProperties().getVersion());

// Set rotation policy
KeyRotationPolicy policy = new KeyRotationPolicy()
    .setExpiresIn("P90D")  // Expire after 90 days
    .setLifetimeActions(Arrays.asList(
        new KeyRotationLifetimeAction(KeyRotationPolicyAction.ROTATE)
            .setTimeBeforeExpiry("P30D")));  // Rotate 30 days before expiry

keyClient.updateKeyRotationPolicy("my-key", policy);

// Get rotation policy
KeyRotationPolicy currentPolicy = keyClient.getKeyRotationPolicy("my-key");
```

## Import Key

```java
import com.azure.security.keyvault.keys.models.ImportKeyOptions;
import com.azure.security.keyvault.keys.models.JsonWebKey;

// Import existing key material
JsonWebKey jsonWebKey = new JsonWebKey()
    .setKeyType(KeyType.RSA)
    .setN(modulus)
    .setE(exponent)
    .setD(privateExponent)
    // ... other RSA components
    ;

ImportKeyOptions importOptions = new ImportKeyOptions("imported-key", jsonWebKey)
    .setHardwareProtected(false);

KeyVaultKey importedKey = keyClient.importKey(importOptions);
```

## Encryption Algorithms

| Algorithm | Key Type | Description |
|-----------|----------|-------------|
| `RSA1_5` | RSA | RSAES-PKCS1-v1_5 |
| `RSA_OAEP` | RSA | RSAES with OAEP (recommended) |
| `RSA_OAEP_256` | RSA | RSAES with OAEP using SHA-256 |
| `A128GCM` | OCT | AES-GCM 128-bit |
| `A256GCM` | OCT | AES-GCM 256-bit |
| `A128CBC` | OCT | AES-CBC 128-bit |
| `A256CBC` | OCT | AES-CBC 256-bit |

## Signature Algorithms

| Algorithm | Key Type | Hash |
|-----------|----------|------|
| `RS256` | RSA | SHA-256 |
| `RS384` | RSA | SHA-384 |
| `RS512` | RSA | SHA-512 |
| `PS256` | RSA | SHA-256 (PSS) |
| `ES256` | EC P-256 | SHA-256 |
| `ES384` | EC P-384 | SHA-384 |
| `ES512` | EC P-521 | SHA-512 |

## Error Handling

```java
import com.azure.core.exception.HttpResponseException;
import com.azure.core.exception.ResourceNotFoundException;

try {
    KeyVaultKey key = keyClient.getKey("non-existent-key");
} catch (ResourceNotFoundException e) {
    System.out.println("Key not found: " + e.getMessage());
} catch (HttpResponseException e) {
    System.out.println("HTTP error " + e.getResponse().getStatusCode());
    System.out.println("Message: " + e.getMessage());
}
```

## Environment Variables

```bash
AZURE_KEYVAULT_URL=https://<vault-name>.vault.azure.net
```

## Best Practices

1. **Use HSM Keys for Production** - Set `setHardwareProtected(true)` for sensitive keys
2. **Enable Soft Delete** - Protects against accidental deletion
3. **Key Rotation** - Set up automatic rotation policies
4. **Least Privilege** - Use separate keys for different operations
5. **Local Crypto When Possible** - Use `CryptographyClient` with local key material to reduce round-trips

## Trigger Phrases

- "Key Vault keys Java", "cryptographic keys Java"
- "encrypt decrypt Java", "sign verify Java"
- "RSA key", "EC key", "HSM key"
- "key rotation", "wrap unwrap key"

## When to Use
This skill is applicable to execute the workflow or actions described in the overview.

---

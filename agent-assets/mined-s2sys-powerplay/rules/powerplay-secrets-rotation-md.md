---
name: secrets-rotation
description: Secrets management and rotation — Automated rotation, key management, credential lifecycle, audit trails
globs: ["**/*.cs", "**/*.ts", "**/*.js", "**/*.tf", "**/*.bicep", "**/*.yaml", "**/*.yml"]
alwaysApply: false
---

# Secrets Management & Rotation Standards

Secrets (API keys, passwords, tokens) are attack targets. Rotate automatically, store securely, audit access, and never expose them.

---

## Secrets Storage

**ALWAYS**:
- Store secrets in dedicated service (AWS Secrets Manager, Azure Key Vault, HashiCorp Vault)
- Never commit secrets to git (use `.gitignore`, `.env` not committed)
- Use managed identity instead of credentials when possible
- Encrypt secrets at rest and in transit
- Restrict access via IAM (principle of least privilege)
- Audit all secret access (who, when, what)

**NEVER**:
- Hardcode secrets in code
- Store secrets in config files
- Commit `.env` files with real secrets
- Use same secret across environments
- Share credentials via email/chat

### ✅ GOOD Secrets Setup

```csharp
// AWS Secrets Manager
using Amazon.SecretsManager;

public class SecretService
{
    private readonly IAmazonSecretsManager _secretsManager;
    
    public async Task<string> GetSecretAsync(string secretName)
    {
        try
        {
            var response = await _secretsManager.GetSecretValueAsync(
                new GetSecretValueRequest { SecretId = secretName }
            );
            
            // Cache in memory (short TTL)
            return response.SecretString;
        }
        catch (ResourceNotFoundException)
        {
            throw new Exception($"Secret '{secretName}' not found");
        }
    }
}

// Dependency injection
services.AddSingleton<IAmazonSecretsManager>(
    new AmazonSecretsManagerClient(Amazon.RegionEndpoint.USEast1)
);

services.AddScoped<ISecretService, SecretService>();

// Usage (never hardcode)
var dbPassword = await _secretService.GetSecretAsync("prod/db/password");
var apiKey = await _secretService.GetSecretAsync("prod/api/key");
```

```yaml
# Azure Key Vault
- task: AzureKeyVault@2
  inputs:
    azureSubscription: 'Azure Subscription'
    keyVaultName: 'prod-kv'
    secretsFilter: 'db-password,api-key,jwt-secret'
    runnerContext: 'Agent'

# Environment injection
- script: |
    echo "##vso[task.setvariable variable=DB_PASSWORD;issecret=true]$(db-password)"
    echo "##vso[task.setvariable variable=API_KEY;issecret=true]$(api-key)"
```

---

## Automated Rotation

**ALWAYS**:
- Rotate secrets automatically (every 30-90 days)
- Rotate API keys before expiration (schedule ahead)
- Rotate database passwords without downtime (connection pooling)
- Maintain old secret during rotation (graceful transition)
- Update all references before removing old secret
- Test rotation process regularly (disaster recovery)

**NEVER**:
- Manually rotate (error-prone, inconsistent)
- Rotate in production without testing
- Skip rotation for "important" secrets
- Lock out users during rotation

### ✅ GOOD Rotation Setup

```python
# AWS Lambda function for automated rotation
import boto3
import json
from datetime import datetime, timedelta

def lambda_handler(event, context):
    """Rotate RDS password every 30 days"""
    
    secrets_client = boto3.client('secretsmanager')
    rds_client = boto3.client('rds')
    
    secret_name = event['SecretId']
    token = event['ClientRequestToken']
    
    # Get current secret
    secret = secrets_client.get_secret_value(SecretId=secret_name)
    current = json.loads(secret['SecretString'])
    
    # Generate new password
    new_password = generate_secure_password(32)
    
    # Update RDS master user
    rds_client.modify_db_instance(
        DBInstanceIdentifier='production-db',
        MasterUserPassword=new_password,
        ApplyImmediately=False  # During maintenance window
    )
    
    # Store new secret (with version label)
    new_secret = current.copy()
    new_secret['password'] = new_password
    new_secret['rotated_at'] = datetime.utcnow().isoformat()
    
    secrets_client.put_secret_value(
        SecretId=secret_name,
        ClientRequestToken=token,
        Secret=json.dumps(new_secret),
        VersionStages=['AWSPENDING']
    )
    
    # Finalize rotation
    secrets_client.update_secret_version_stage(
        SecretId=secret_name,
        VersionStage='AWSCURRENT',
        MoveToVersionId=token,
        RemoveFromVersionId=secret['VersionIdsToStages']
    )
    
    return {'statusCode': 200, 'message': 'Rotation successful'}

def generate_secure_password(length):
    """Generate cryptographically secure password"""
    import secrets, string
    
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(secrets.choice(chars) for _ in range(length))

# EventBridge rule: trigger every 30 days
# Cron: 0 2 1 * ? (1st of month at 2 AM)
```

```yaml
# Kubernetes secret rotation (using sealed-secrets)
apiVersion: bitnami.com/v1alpha1
kind: SealedSecret
metadata:
  name: db-credentials
  namespace: production
  annotations:
    sealedsecrets.bitnami.com/rotate: "30d"  # Rotate every 30 days
spec:
  encryptedData:
    password: ...sealed...
    username: ...sealed...
```

---

## Credential Lifecycle

**ALWAYS**:
- Track creation date, expiration, last rotated
- Pre-rotate before expiration (7 days before)
- Maintain version history (last 3 versions)
- Log all credential changes (who, when, action)
- Alert on unused credentials (revoke if stale)
- Immediately revoke compromised secrets

**NEVER**:
- Store unencrypted credentials
- Forget to update dependent services
- Let credentials expire (breaks systems)
- Skip audit logs

### ✅ GOOD Credential Tracking

```csharp
// Credential metadata (audit trail)
public class SecretMetadata
{
    public string Name { get; set; }
    public DateTime CreatedAt { get; set; }
    public DateTime ExpiresAt { get; set; }
    public DateTime LastRotatedAt { get; set; }
    public DateTime LastAccessedAt { get; set; }
    public string Owner { get; set; }
    public SecretStatus Status { get; set; }  // Active, Rotating, Expired, Revoked
    public List<AuditLog> Changes { get; set; }
}

public class AuditLog
{
    public DateTime Timestamp { get; set; }
    public string Action { get; set; }  // Created, Rotated, Accessed, Revoked
    public string Actor { get; set; }  // User/service that performed action
    public string Reason { get; set; }
}

// Service for checking expiration
public class SecretExpirationService
{
    public async Task CheckAndRotateAsync()
    {
        var secretsToRotate = await _db.Secrets
            .Where(s => s.Status == SecretStatus.Active)
            .Where(s => s.ExpiresAt <= DateTime.UtcNow.AddDays(7))  // Rotate soon
            .ToListAsync();
        
        foreach (var secret in secretsToRotate)
        {
            await _rotationService.RotateAsync(secret.Name);
            
            // Log rotation
            _logger.LogInformation(
                "Secret {SecretName} rotated by scheduler. " +
                "Old expiry: {ExpiresAt}, New expiry: {NewExpiry}",
                secret.Name, secret.ExpiresAt, DateTime.UtcNow.AddDays(90)
            );
        }
    }
}
```

---

## Credential Compromise

**ALWAYS**:
- Immediately revoke compromised secrets
- Regenerate new credentials
- Update all systems using old credential
- Investigate how credential was leaked
- Alert security team
- Audit access logs during compromise window

**NEVER**:
- Delay revoking compromised secrets
- Reuse compromised values
- Hide breach from team

### ✅ GOOD Compromise Response

```csharp
// Immediate revocation service
public class CompromiseResponseService
{
    public async Task RevokeCompromisedSecretAsync(
        string secretName,
        string reason,
        string discoveredBy)
    {
        // 1. Immediately revoke
        await _secretsManager.RevokeSecretAsync(secretName);
        
        // 2. Generate new secret
        var newSecret = await _secretsManager.GenerateSecretAsync(secretName);
        
        // 3. Alert all services using this secret
        var dependentServices = await _db.ServiceDependencies
            .Where(d => d.SecretName == secretName)
            .Select(d => d.ServiceName)
            .ToListAsync();
        
        foreach (var service in dependentServices)
        {
            await _notificationService.AlertAsync(
                service,
                $"Secret {secretName} compromised. New secret generated. Update immediately.",
                priority: AlertPriority.Critical
            );
        }
        
        // 4. Comprehensive audit
        await _auditService.LogCompromiseAsync(new CompromiseRecord
        {
            SecretName = secretName,
            CompromiseTime = DateTime.UtcNow,
            DiscoveredBy = discoveredBy,
            Reason = reason,
            AffectedServices = dependentServices,
            RevokedAt = DateTime.UtcNow,
            DependentServices = dependentServices
        });
        
        // 5. Investigation trigger
        await _alertingService.NotifySecurityTeamAsync(
            $"Credential compromise detected: {secretName}\n" +
            $"Affected services: {string.Join(", ", dependentServices)}\n" +
            $"Immediate action required: Update all references"
        );
    }
}
```

---

## Secrets Security Checklist

- [ ] All secrets in vault (not in code/config)
- [ ] `.env` files in `.gitignore`
- [ ] Automated rotation (every 30-90 days)
- [ ] Managed identity used when possible
- [ ] Access audit trails enabled
- [ ] Expiration monitoring (alert 7 days before)
- [ ] Compromise response playbook ready
- [ ] Regular rotation testing

---

## Summary

Good secrets management:
1. **Secure storage** — Vault, not code
2. **Short lifetime** — Rotate automatically
3. **Audit access** — Every secret access logged
4. **Immediate action** — Compromise detection and revocation
5. **Automation** — No manual rotation (error-prone)
6. **Testing** — Regular rotation drills

Secrets are keys to the kingdom—protect like Fort Knox.

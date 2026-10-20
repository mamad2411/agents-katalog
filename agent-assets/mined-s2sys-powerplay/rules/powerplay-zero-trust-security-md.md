---
name: zero-trust-security
description: Zero-trust security architecture — Identity verification, least privilege, assume breach mentality, continuous validation
globs: ["**/*.cs", "**/*.ts", "**/*.js", "**/*.tf", "**/*.bicep", "**/*.yaml", "**/*.yml"]
alwaysApply: false
---

# Zero-Trust Security Architecture

Zero-trust security assumes every access request is potentially compromised. Verify every identity, authenticate every connection, authorize every action — trust nothing by default.

---

## Core Zero-Trust Principles

**ALWAYS**:
- Verify every identity (never trust source IP or location)
- Authenticate before authorizing (MFA mandatory)
- Encrypt all data in transit (TLS 1.2+) and at rest
- Segment networks (microsegmentation, no flat networks)
- Log and monitor all access (immutable audit trails)
- Apply least privilege (minimum permissions needed)
- Assume breach mentality (defense in depth)
- Continuous validation (not just initial check)

**NEVER**:
- Trust network perimeter (assume compromised)
- Use single-factor authentication
- Allow unencrypted internal traffic
- Grant broad permissions ("admin" for everything)
- Skip audit logging

### ✅ GOOD Zero-Trust Architecture

```
User Request
    ↓
[Identity Verification]
├─ Username/password + MFA
├─ Certificate validation
├─ Device health check
└─ Continuous behavior analysis
    ↓
[Authentication Gateway]
├─ Token issuance (JWT, OAuth)
├─ Session validation
├─ Rate limiting
└─ Anomaly detection
    ↓
[Microservice Gateway]
├─ Authorization (fine-grained RBAC)
├─ Rate limiting per user
├─ Request signing
└─ Mutual TLS
    ↓
[Audit & Monitoring]
├─ All access logged (immutable)
├─ Real-time anomaly detection
├─ Alert on privilege escalation
└─ Forensic trail
```

---

## Identity & Access Management

**ALWAYS**:
- Use managed identity (no credentials stored)
- Implement MFA (authenticator app, hardware key, SMS fallback)
- Use short-lived tokens (expiry 1-24 hours)
- Rotate credentials regularly (90 days)
- Implement just-in-time (JIT) access elevation
- Audit identity changes (add/remove/role changes)
- Use conditional access (device, location, risk)

**NEVER**:
- Store secrets in code
- Use permanent API keys
- Skip MFA for privileged accounts
- Grant "admin" by default (escalate on need)

### ✅ GOOD Identity Setup

```csharp
// OAuth 2.0 + PKCE (browser-based apps)
var authClient = new HttpClient();
var tokenRequest = new
{
    grant_type = "authorization_code",
    code = authCode,
    code_verifier = codeVerifier,
    client_id = clientId,
    redirect_uri = redirectUri
};

var response = await authClient.PostAsJsonAsync(
    "https://auth.example.com/oauth/token",
    tokenRequest
);

var token = JsonSerializer.Deserialize<TokenResponse>(await response.Content.ReadAsStringAsync());

// Token validation
var handler = new JwtSecurityTokenHandler();
var validatedToken = handler.ValidateToken(token.AccessToken, validationParameters);

// Just-in-time elevation
public async Task<string> ElevatePrivilegeAsync(string userId, string action)
{
    // Check if action requires elevation
    if (!RequiresElevation(action))
        return GetCurrentToken();
    
    // Require MFA verification
    await VerifyMFAAsync(userId);
    
    // Grant temporary elevated token (30 minutes)
    return GenerateElevatedToken(userId, TimeSpan.FromMinutes(30));
}

// Conditional access
public bool IsAccessAllowed(User user, Resource resource)
{
    var checks = new[]
    {
        // Device health check
        user.DeviceIsCompliant && user.DeviceIsEncrypted,
        
        // Location check (VPN required for sensitive data)
        resource.IsPublic || user.IsOnCorporateVPN,
        
        // Risk assessment
        !user.HasAnomalousActivity,
        
        // Time-based access
        IsWithinBusinessHours(user.Timezone) || resource.IsNonCritical,
        
        // Rate limiting
        !user.ExceededRateLimit
    };
    
    return checks.All(c => c);
}
```

---

## Network Segmentation

**ALWAYS**:
- Microsegmentation (divide network into zones)
- Network policies (control traffic between segments)
- Private networks for databases (no internet access)
- VPN/bastion hosts for administrative access
- Service-to-service mutual TLS (mTLS)
- Firewall rules (deny by default, allow specific)

**NEVER**:
- Flat network (all servers can reach all servers)
- Allow database access from internet
- SSH/RDP with password authentication
- Unencrypted internal communication

### ✅ GOOD Network Segmentation

```yaml
# Kubernetes Network Policies (microsegmentation)
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: api-server-netpol
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: api
  policyTypes:
  - Ingress
  - Egress
  
  ingress:
  # Allow from ingress only
  - from:
    - podSelector:
        matchLabels:
          app: ingress-controller
    ports:
    - protocol: TCP
      port: 3000
  
  # Allow from authorized clients
  - from:
    - namespaceSelector:
        matchLabels:
          trusted: "true"
    ports:
    - protocol: TCP
      port: 3000
  
  egress:
  # Allow to database only
  - to:
    - podSelector:
        matchLabels:
          app: postgres
    ports:
    - protocol: TCP
      port: 5432
  
  # Allow DNS
  - to:
    - namespaceSelector:
        matchLabels:
          name: kube-system
    ports:
    - protocol: UDP
      port: 53
  
  # Deny all else
  - to:
    - podSelector: {}

---
# Terraform: AWS Security Groups (firewall rules)
resource "aws_security_group" "database" {
  name = "database-sg"
  
  # Deny by default (no ingress rules = deny all)
  
  # Allow from app tier only
  ingress {
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.app_tier.id]
  }
  
  # Allow egress for DNS, NTP
  egress {
    from_port   = 53
    to_port     = 53
    protocol    = "udp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
```

---

## Data Encryption

**ALWAYS**:
- Encrypt data in transit (TLS 1.2+ for all connections)
- Encrypt data at rest (AES-256 or equivalent)
- Encrypt backups (same as production data)
- Use key management services (HSM, Key Vault)
- Rotate encryption keys (annually)
- Encrypt sensitive fields individually (field-level encryption)
- Use HTTPS everywhere (redirect HTTP → HTTPS)

**NEVER**:
- Store encryption keys with encrypted data
- Use weak encryption (MD5, SHA1, DES)
- Disable TLS verification
- Encrypt with hardcoded keys

### ✅ GOOD Encryption Setup

```csharp
// Data in transit (TLS)
services.AddHttpsRedirection(options =>
{
    options.HttpsPort = 443;
    options.RedirectStatusCode = StatusCodes.Status307TemporaryRedirect;
});

services.AddHsts(options =>
{
    options.MaxAge = TimeSpan.FromDays(365);
    options.IncludeSubDomains = true;
    options.Preload = true;  // HSTS preload list
});

// Database connections with TLS
var connectionString = "Server=db.example.com;Database=app;" +
    "Encrypt=true;TrustServerCertificate=false;Connection Timeout=30;";

// Data at rest (field-level encryption)
public class User
{
    public string Id { get; set; }
    
    [Encrypted]
    public string Email { get; set; }
    
    [Encrypted]
    public string SSN { get; set; }
}

// Encryption service
public class EncryptionService
{
    private readonly IKeyVaultService _keyVault;
    
    public async Task<string> EncryptAsync(string plaintext, string keyId)
    {
        var key = await _keyVault.GetKeyAsync(keyId);
        using (var aes = new AesGcm(key))
        {
            byte[] nonce = new byte[12];
            using (var rng = RandomNumberGenerator.Create())
                rng.GetBytes(nonce);
            
            byte[] plainBytes = Encoding.UTF8.GetBytes(plaintext);
            byte[] ciphertext = new byte[plainBytes.Length];
            byte[] tag = new byte[16];
            
            aes.Encrypt(nonce, plainBytes, null, ciphertext, tag);
            
            // Return: nonce + tag + ciphertext
            return Convert.ToBase64String(nonce.Concat(tag).Concat(ciphertext).ToArray());
        }
    }
}

// Backup encryption (same strength as production)
resource "aws_backup_vault" "app_backup" {
  name        = "app-backup-vault"
  kms_key_arn = aws_kms_key.backup.arn  // Encrypt with KMS
}
```

---

## Least Privilege Access

**ALWAYS**:
- Default deny (no permissions unless explicitly granted)
- Role-based access control (RBAC)
- Attribute-based access control (ABAC) for fine-grained
- Separate roles: reader, writer, admin (never "power user")
- Just-in-time elevation (temporary elevated access)
- Audit trail for all privilege escalations

**NEVER**:
- "Admin" role by default
- Permanent elevated access
- Share credentials
- Grant more permissions than needed

### ✅ GOOD RBAC Setup

```yaml
# Kubernetes RBAC
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: app-developer
  namespace: production
rules:
# Read logs only
- apiGroups: [""]
  resources: ["pods/log"]
  verbs: ["get", "list"]

# View pods (not edit)
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get", "list"]

# No delete, no exec, no create

---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: dev-team-binding
  namespace: production
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: Role
  name: app-developer
subjects:
- kind: Group
  name: "dev-team@company.com"
  apiGroup: rbac.authorization.k8s.io

---
# Azure RBAC
resource "azurerm_role_assignment" "developer_access" {
  scope              = azurerm_resource_group.app.id
  role_definition_name = "Reader"  # Read-only
  principal_id       = azuread_group.developers.object_id
}

resource "azurerm_role_assignment" "admin_access" {
  scope              = azurerm_resource_group.app.id
  role_definition_name = "Owner"  # Full access (rarely used)
  principal_id       = azuread_user.admin.object_id
  
  # Conditional: only during business hours, require MFA
  condition = "((!(user.department equals 'HR')) or (user.location equals 'HQ'))"
  condition_version = "2.0"
}
```

---

## Zero-Trust Security Checklist

- [ ] Identity: MFA required, short-lived tokens, credential rotation
- [ ] Authentication: Every request verified, no trust based on IP
- [ ] Authorization: Least privilege, RBAC, JIT elevation
- [ ] Encryption: TLS in transit, AES-256 at rest, key rotation
- [ ] Network: Microsegmentation, service-to-service mTLS, firewalls
- [ ] Monitoring: All access logged, real-time alerts, audit trails
- [ ] Compliance: Regular penetration tests, vulnerability scans
- [ ] Incident response: Playbooks ready, forensics capability

---

## Summary

Good zero-trust security:
1. **Trust nothing** — Every identity verified, every connection authenticated
2. **Verify always** — Continuous validation, not just at entry
3. **Encrypt everything** — In transit and at rest
4. **Segment networks** — Microsegmentation, firewall rules
5. **Least privilege** — Minimal permissions, JIT elevation
6. **Audit everything** — Immutable logs, forensic trail
7. **Assume breach** — Defense in depth, multiple layers

Zero-trust is a mindset: verify, validate, monitor, repeat.

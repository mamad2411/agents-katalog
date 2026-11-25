---
name: compliance-awareness
description: Practical engineering guidance for SOC 2, GDPR, HIPAA compliance and data classification. Covers access controls, audit logging, change management, right to deletion, data portability, consent, PHI encryption, and data classification levels. Engineering checks, not legal advice.
invoke_when: Use when handling PII, health data, or financial data, implementing user deletion, data export, consent management, audit logging, access controls, or building for regulated industries (healthcare, finance, GDPR).
---

# Compliance Awareness

**Disclaimer:** This skill provides practical engineering patterns for compliance. It is not legal advice. Consult legal counsel for your specific compliance obligations.

## Core Principle

Compliance is a set of engineering constraints, not a checkbox exercise. Build compliance into the system architecture from day one. Retrofitting compliance is 10x harder and 10x more expensive than building it in.

---

## 1. Data Classification Levels

Every field your system stores must be classified. The classification determines how the data is stored, accessed, logged, and deleted.

| Level | Definition | Examples | Storage | Access | Logging |
|---|---|---|---|---|---|
| **Public** | Data intended for public consumption | Marketing copy, public API docs, product names | No restrictions | No restrictions | Standard |
| **Internal** | Data for internal use only, low risk if leaked | Internal wiki, architecture diagrams, sprint boards | Standard encryption | Authentication required | Standard |
| **Confidential** | PII or business-sensitive data | Names, emails, addresses, financial reports, revenue data | Encrypted at rest (AES-256), encrypted in transit (TLS 1.2+) | Role-based access, audit logged | Audit logged, PII masked in application logs |
| **Restricted** | Highest sensitivity, regulatory risk | Passwords, API keys, SSNs, health records, payment card numbers | Encrypted with KMS/HSM, separate data store | Minimal access, MFA required, audit logged | Never in logs, access alerts |

### Implementing Data Classification

```typescript
// Tag every database field with its classification
// This drives encryption, access control, and logging behavior

interface FieldClassification {
  field: string;
  classification: 'public' | 'internal' | 'confidential' | 'restricted';
  regulations: string[];         // ['gdpr', 'hipaa', 'pci-dss']
  retentionDays: number;         // How long to keep before purging
  piiType?: string;              // 'name' | 'email' | 'ssn' | 'health_record'
}

const userTableClassification: FieldClassification[] = [
  { field: 'id', classification: 'internal', regulations: [], retentionDays: -1 },
  { field: 'email', classification: 'confidential', regulations: ['gdpr'], retentionDays: 365, piiType: 'email' },
  { field: 'name', classification: 'confidential', regulations: ['gdpr'], retentionDays: 365, piiType: 'name' },
  { field: 'password_hash', classification: 'restricted', regulations: [], retentionDays: -1 },
  { field: 'ssn', classification: 'restricted', regulations: ['gdpr'], retentionDays: 90, piiType: 'ssn' },
  { field: 'health_notes', classification: 'restricted', regulations: ['hipaa', 'gdpr'], retentionDays: 2555, piiType: 'health_record' },
];
```

### Classification Checklist

- [ ] Every database table has a classification document listing each field's level.
- [ ] Restricted data is stored in a separate data store with additional access controls.
- [ ] Confidential and restricted fields are encrypted at rest.
- [ ] PII is never stored in application logs, error tracking systems, or analytics.
- [ ] Data retention periods are defined and enforced for every classified field.

---

## 2. SOC 2

SOC 2 is an audit framework based on five Trust Services Criteria: Security, Availability, Processing Integrity, Confidentiality, and Privacy. Most startups focus on Security and Availability first.

### Access Controls

**What SOC 2 auditors check:** Who has access to what, and is it the minimum needed?

**Engineering requirements:**
- Role-based access control (RBAC) for all systems.
- MFA enforced for all production access and admin panels.
- Principle of least privilege: no engineer has more access than needed for their role.
- Access reviews quarterly: remove access for people who no longer need it.
- Separate production credentials from staging/development.
- No shared accounts or shared credentials.

```python
# RBAC implementation -- define roles with explicit permissions
ROLES = {
    "developer": {
        "permissions": ["read:code", "write:code", "read:staging_logs"],
        "production_access": False,
    },
    "oncall_engineer": {
        "permissions": ["read:code", "write:code", "read:production_logs", "restart:services"],
        "production_access": True,  # Read-only DB access
    },
    "admin": {
        "permissions": ["read:code", "write:code", "read:production_logs",
                        "write:production_db", "manage:users"],
        "production_access": True,
        "requires_mfa": True,
        "requires_approval": True,  # Just-in-time access
    },
}
```

### Audit Logging

**What SOC 2 auditors check:** Can you trace who did what, when, and from where?

**Engineering requirements:**
- Log all authentication events (login, logout, failed login, MFA challenges).
- Log all authorization events (permission granted, permission denied, role changes).
- Log all data access to confidential and restricted data.
- Log all administrative actions (user creation, permission changes, config changes).
- Logs are immutable: append-only, shipped to a separate system.
- Logs are retained for at least 1 year.

```typescript
// Comprehensive audit logging
async function auditLog(event: AuditEvent): Promise<void> {
  const entry = {
    timestamp: new Date().toISOString(),
    eventType: event.type,            // 'auth.login' | 'data.read' | 'admin.role_change'
    actor: {
      userId: event.userId,
      email: event.userEmail,
      role: event.userRole,
      ip: event.sourceIp,
      userAgent: event.userAgent,
    },
    action: event.action,             // 'created' | 'read' | 'updated' | 'deleted'
    resource: {
      type: event.resourceType,       // 'user' | 'order' | 'config'
      id: event.resourceId,
    },
    result: event.result,             // 'success' | 'denied' | 'error'
    metadata: event.metadata,         // Additional context (never PII)
  };

  // Write to immutable audit store -- this must not fail silently
  await auditStore.append(entry);
}
```

### Change Management

**What SOC 2 auditors check:** How do changes get into production, and who approved them?

**Engineering requirements:**
- All code changes go through pull request review with at least one approver.
- CI/CD pipeline enforces tests, linting, and security scanning before merge.
- No direct commits to the main branch (branch protection enabled).
- No direct access to production databases for writes (read-only access for debugging only).
- Infrastructure changes use Infrastructure as Code (Terraform, CloudFormation) with PR review.
- Deployment history is auditable (who deployed what, when).

### SOC 2 Checklist

- [ ] RBAC is implemented with documented roles and permissions.
- [ ] MFA is enforced for all production access.
- [ ] Access reviews happen quarterly with documented results.
- [ ] All authentication, authorization, and data access events are audit logged.
- [ ] Audit logs are immutable, stored in a separate system, retained for 1+ year.
- [ ] All code changes go through PR review with CI checks.
- [ ] No engineer has direct write access to production databases.
- [ ] Infrastructure is managed as code with PR review.
- [ ] All data stores have encryption at rest enabled.
- [ ] All data in transit uses TLS 1.2+.

---

## 3. GDPR (General Data Protection Regulation)

Applies to any system that processes data of EU residents, regardless of where your company is based.

### Right to Deletion (Article 17)

A user can request that all their personal data be deleted. You must comply within 30 days.

**Engineering requirements:**
- Implement a `DELETE /v1/users/{id}` endpoint that cascades deletion through all data stores.
- Identify every location where user data is stored: databases, caches, logs, backups, analytics, third-party services.
- For logs and backups where deletion is impractical, anonymize the data instead.
- Document the data map: "For user X, their data exists in these N locations."

```python
async def delete_user_data(user_id: str) -> DeletionReport:
    """Delete all user data across all systems. Returns a report of what was deleted."""
    report = DeletionReport(user_id=user_id)

    # 1. Primary database -- cascade delete
    deleted_rows = await db.execute(
        "DELETE FROM users WHERE id = %s RETURNING id", (user_id,)
    )
    report.add("primary_db.users", deleted_rows)

    # 2. Related tables
    for table in ["orders", "addresses", "payment_methods", "preferences"]:
        deleted = await db.execute(
            f"DELETE FROM {table} WHERE user_id = %s", (user_id,)
        )
        report.add(f"primary_db.{table}", deleted)

    # 3. Cache
    await redis.delete(f"user:{user_id}", f"session:{user_id}")
    report.add("redis_cache", "cleared")

    # 4. Search index
    await elasticsearch.delete(index="users", id=user_id)
    report.add("search_index", "deleted")

    # 5. Third-party services
    await analytics_service.delete_user(user_id)
    report.add("analytics", "deletion_requested")

    await email_service.delete_subscriber(user_id)
    report.add("email_service", "deletion_requested")

    # 6. Audit log -- record the deletion itself (this is required, not a contradiction)
    await audit_log({
        "action": "user.deleted",
        "actor": "system",       # Or the admin who processed the request
        "resource": f"user:{user_id}",
        "details": report.to_dict(),
    })

    return report
```

### Data Portability (Article 20)

A user can request all their personal data in a machine-readable format.

```typescript
// GET /v1/users/{id}/export
async function exportUserData(userId: string): Promise<UserDataExport> {
  const [user, orders, addresses, preferences] = await Promise.all([
    db.users.findById(userId),
    db.orders.findByUserId(userId),
    db.addresses.findByUserId(userId),
    db.preferences.findByUserId(userId),
  ]);

  return {
    exportDate: new Date().toISOString(),
    format: 'json',
    data: {
      profile: { name: user.name, email: user.email, createdAt: user.createdAt },
      orders: orders.map(o => ({ id: o.id, total: o.total, date: o.createdAt })),
      addresses: addresses.map(a => ({ street: a.street, city: a.city, country: a.country })),
      preferences: preferences,
    },
  };
}
```

### Consent Management

- Record exactly what the user consented to, when, and how.
- Consent must be freely given, specific, informed, and unambiguous.
- Pre-checked boxes are not valid consent.
- Users must be able to withdraw consent as easily as they gave it.

```sql
CREATE TABLE consent_records (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(id),
    consent_type VARCHAR(100) NOT NULL,    -- 'marketing_email', 'analytics_tracking', 'data_sharing'
    granted BOOLEAN NOT NULL,
    granted_at TIMESTAMP,
    withdrawn_at TIMESTAMP,
    ip_address INET,
    consent_text TEXT NOT NULL,            -- The exact text the user agreed to
    version VARCHAR(20) NOT NULL           -- Version of the consent text
);
```

### GDPR Checklist

- [ ] A data map exists documenting where every type of user data is stored.
- [ ] User deletion cascades through all data stores and third-party services.
- [ ] User data export returns all personal data in JSON or CSV format.
- [ ] Consent is recorded with timestamps, IP, and the exact text agreed to.
- [ ] Users can withdraw consent through the same channel they gave it.
- [ ] Data collection is minimized: every stored field has a documented purpose.
- [ ] Privacy policy is accurate and reflects actual data practices.
- [ ] Data processing agreements exist with all third-party processors.
- [ ] A breach notification process exists (72-hour deadline).

---

## 4. HIPAA (Health Insurance Portability and Accountability Act)

Applies to any system that stores, processes, or transmits Protected Health Information (PHI). PHI includes any health information that can be linked to a specific individual.

### PHI Encryption

**Engineering requirements:**
- All PHI encrypted at rest using AES-256 with keys managed by KMS/HSM.
- All PHI encrypted in transit using TLS 1.2+ (no exceptions).
- Encryption keys are rotated annually.
- PHI is stored in a dedicated, isolated data store (not co-mingled with general application data).

```python
# PHI-specific database with field-level encryption
from cryptography.fernet import Fernet

class PHIStore:
    def __init__(self, encryption_key: bytes):
        self.cipher = Fernet(encryption_key)

    def store_record(self, patient_id: str, record: dict) -> None:
        # Encrypt sensitive fields individually
        encrypted_record = {
            "patient_id": patient_id,  # De-identified reference
            "diagnosis": self.cipher.encrypt(record["diagnosis"].encode()),
            "medications": self.cipher.encrypt(json.dumps(record["medications"]).encode()),
            "notes": self.cipher.encrypt(record["notes"].encode()),
            "created_at": datetime.utcnow().isoformat(),
            "accessed_by": [],  # Access audit trail
        }
        self.phi_db.insert(encrypted_record)

    def read_record(self, patient_id: str, accessor_id: str, justification: str) -> dict:
        # Every PHI read is logged with who accessed it and why
        audit_log({
            "action": "phi.read",
            "actor": accessor_id,
            "resource": f"patient:{patient_id}",
            "justification": justification,
        })
        record = self.phi_db.find_one({"patient_id": patient_id})
        return self._decrypt_record(record)
```

### Access Controls for PHI

- Minimum necessary rule: only grant access to the specific PHI needed for the task.
- Every PHI access is logged with the user ID, timestamp, record accessed, and justification.
- Access to PHI requires role-based authorization AND is audited.
- Automatic session timeout after 15 minutes of inactivity for PHI-accessing applications.
- Emergency access ("break the glass") procedure exists with post-access review.

### Business Associate Agreements (BAAs)

Every third-party service that can access PHI must have a signed BAA. This includes:
- Cloud providers (AWS, GCP, Azure -- they offer BAAs).
- Logging and monitoring services (verify they do not store PHI in logs).
- Analytics services (PHI must not be sent to analytics without a BAA).
- Email services (if sending PHI via email).

### HIPAA Checklist

- [ ] All PHI fields are identified and documented.
- [ ] PHI is encrypted at rest (AES-256) and in transit (TLS 1.2+).
- [ ] PHI is stored in an isolated data store, not co-mingled with general data.
- [ ] Every PHI access is logged with user ID, timestamp, and justification.
- [ ] PHI never appears in application logs, error tracking, or analytics.
- [ ] Access to PHI follows the minimum necessary principle.
- [ ] All vendors handling PHI have signed BAAs.
- [ ] Encryption keys are managed through KMS/HSM and rotated annually.
- [ ] Session timeouts are enforced for PHI-accessing applications (15 minutes).
- [ ] A breach notification process exists (60-day deadline for affected individuals).
- [ ] Employee training on PHI handling is documented.

---

## 5. Practical Patterns

### Soft Delete with Scheduled Purge

For compliance, implement a multi-stage deletion process:

```typescript
// Stage 1: Soft delete -- mark as deleted, stop showing in queries
await db.users.update(userId, {
  deletedAt: new Date(),
  status: 'pending_deletion',
});

// Stage 2: Anonymize PII after 30 days (retention period)
// Background job runs daily
async function anonymizeDeletedUsers(): Promise<void> {
  const users = await db.users.find({
    status: 'pending_deletion',
    deletedAt: { $lt: daysAgo(30) },
  });

  for (const user of users) {
    await db.users.update(user.id, {
      email: `deleted_${user.id}@anonymized.local`,
      name: 'DELETED USER',
      phone: null,
      address: null,
      status: 'anonymized',
      anonymizedAt: new Date(),
    });
  }
}

// Stage 3: Hard delete after legal hold period (if applicable)
// Only after confirming no legal hold exists
```

### Data Masking for Logs

```typescript
const SENSITIVE_PATTERNS: Array<{ pattern: RegExp; replacement: string }> = [
  { pattern: /\b\d{3}-\d{2}-\d{4}\b/g, replacement: '***-**-****' },           // SSN
  { pattern: /\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b/g, replacement: '****-****-****-****' }, // Credit card
  { pattern: /\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b/g, replacement: '***@***.***' }, // Email
];

function maskSensitiveData(text: string): string {
  let masked = text;
  for (const { pattern, replacement } of SENSITIVE_PATTERNS) {
    masked = masked.replace(pattern, replacement);
  }
  return masked;
}
```

---

## Overall Compliance Checklist

- [ ] Data classification levels are defined and every stored field is classified.
- [ ] Restricted data uses dedicated storage with enhanced encryption and access controls.
- [ ] Audit logging covers authentication, authorization, data access, and admin actions.
- [ ] User deletion and data export functionality exists and has been tested.
- [ ] Consent records include timestamps, IP, consent text version, and withdrawal capability.
- [ ] PHI (if applicable) is encrypted, isolated, and access-logged.
- [ ] BAAs exist with all vendors who handle sensitive data.
- [ ] Access reviews happen quarterly.
- [ ] Data retention periods are defined and enforced.
- [ ] PII is masked in all logs, error tracking, and analytics.

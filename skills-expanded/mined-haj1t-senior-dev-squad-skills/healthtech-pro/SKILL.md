---
name: healthtech-pro
description: "HIPAA compliance, FHIR, EHR integration, audit, PHI protection. Use when building or auditing healthcare technology systems."
---

# HealthTech Pro

## Purpose

Build HIPAA-compliant healthcare applications: FHIR API patterns, EHR integration, PHI protection, audit logging, and clinical workflow automation.

## When to Use

**Use this when:**
- Building any application that stores, transmits, or displays Protected Health Information (PHI)
- Designing FHIR R4 API endpoints or integrating with an EHR system (Epic, Cerner, Allscripts)
- Reviewing existing healthcare code for HIPAA audit trail gaps, PHI leaks, or BAA coverage holes

**Use this ESPECIALLY when:**
- A new data field might qualify as PHI — name, DOB, SSN, diagnosis code, device identifier
- Connecting a third-party service (email, SMS, analytics, logging) where PHI could flow outside a BAA boundary
- Implementing patient access APIs where the minimum-necessary standard and role-based access must be enforced together

**Don't skip when:**
- Adding any logging, debugging, or error-reporting integration — PHI masking must be verified before enabling
- Changing the retention or deletion logic for patient records, even for a "temporary" data store
- Onboarding a new cloud vendor, even for non-clinical infrastructure, because BAA gap analysis is required first

## Core Patterns

### 1. PHI Protection

```typescript
// All PII/PHI data must be encrypted at rest + in transit
class PHIProtector {
  // Encrypt PHI fields before storing
  async encryptPatientData(patient: CreatePatientRequest): Promise<EncryptedPatient> {
    return {
      ...patient,
      ssn: await encrypt(patient.ssn, process.env.PHI_ENCRYPTION_KEY),
      dob: await encrypt(patient.dob, process.env.PHI_ENCRYPTION_KEY),
      medicalRecordNumber: await encrypt(patient.medicalRecordNumber, process.env.PHI_ENCRYPTION_KEY),
    }
  }

  // Mask PHI in logs
  maskForLogging(patient: Patient): SafePatient {
    return {
      id: patient.id,
      age: calculateAge(patient.dob),       // Not exact DOB
      gender: patient.gender,
      zip3: patient.zip.substring(0, 3),     // Only first 3 digits
      // No: ssn, dob, full address, phone, email
    }
  }
}
```

### 2. FHIR API Implementation

```typescript
// HL7 FHIR R4 Patient endpoint
@FHIRResource('Patient')
class PatientResource {
  async search(params: FHIRSearchParams): Promise<Bundle> {
    // Audit every access
    await audit.log('Patient.search', { params, user: req.user })

    // Scoped by organization
    const patients = await db.patient.findMany({
      where: { organizationId: req.user.orgId },
    })

    return {
      resourceType: 'Bundle',
      type: 'searchset',
      total: patients.length,
      entry: patients.map(p => ({
        resource: this.toFHIR(p),
      })),
    }
  }

  private toFHIR(patient: Patient): FHIRPatient {
    return {
      resourceType: 'Patient',
      id: patient.id,
      identifier: [{ system: 'urn:oid:1.2.3.4', value: patient.medicalRecordNumber }],
      name: [{ given: [patient.firstName], family: patient.lastName }],
      birthDate: patient.dob,
      gender: patient.gender,
      address: [{
        line: [patient.addressLine1],
        city: patient.city,
        state: patient.state,
        postalCode: patient.zip,
      }],
    }
  }
}
```

### 3. Audit Logging (HIPAA Required)

```sql
-- Every PHI access must be logged
CREATE TABLE hipaa_audit_log (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    timestamp       TIMESTAMPTZ NOT NULL DEFAULT now(),
    user_id         UUID NOT NULL,
    action          TEXT NOT NULL,     -- 'create', 'read', 'update', 'delete'
    resource_type   TEXT NOT NULL,     -- 'Patient', 'Observation', 'DocumentReference'
    resource_id     UUID NOT NULL,
    patient_id      UUID NOT NULL,     -- Which patient's data was accessed
    ip_address      INET,
    user_agent      TEXT,
    reason_code     TEXT,              -- 'treatment', 'payment', 'operations'
    changes         JSONB              -- For updates: { before: {}, after: {} }
);

CREATE INDEX idx_hipaa_patient ON hipaa_audit_log(patient_id, timestamp DESC);
CREATE INDEX idx_hipaa_user ON hipaa_audit_log(user_id, timestamp DESC);

-- Retention: minimum 6 years (HIPAA requirement)
-- Consider using table partitioning by month
```

### 4. BAA Compliance

```typescript
// Business Associate Agreement checks
const BAA_REQUIRED_SERVICES = [
  'aws:healthlake',
  'gcp:healthcare-api',
  'azure:healthcare-apis',
  'twilio:sendgrid',
]

function validateBAACoverage(service: string): void {
  if (BAA_REQUIRED_SERVICES.includes(service)) {
    throw new Error(`${service} requires a signed BAA before processing PHI`)
  }
}
```

### Checklist

- [ ] PHI encrypted at rest (AES-256) and in transit (TLS 1.2+)
- [ ] All PHI access logged (HIPAA audit trail)
- [ ] Minimum necessary standard (only access PHI needed for the task)
- [ ] Automatic logout after inactivity
- [ ] Session timeout < 15 minutes for clinical workstations
- [ ] BAA in place with all service providers
- [ ] Data retention: 6 years minimum, with purge process
- [ ] Breach notification process documented
- [ ] Role-based access control (clinician vs admin vs billing)
- [ ] FHIR R4 API for interoperability
- [ ] De-identification for research/non-clinical use

## Related Skills

- **security-reviewer** — always pair; healthtech-pro governs HIPAA/FHIR domain rules while security-reviewer covers OWASP, injection, and general API hardening
- **backend-senior-engineer** — for the broader REST/gRPC service architecture that hosts FHIR endpoints and clinical workflows
- **code-reviewer** — when designing or auditing FHIR-conformant API contracts, search parameter support, and capability statements
- **postgres-pro** — for PHI-at-rest schema design, audit log table partitioning, row-level security for multi-tenant patient data, and retention policies
- **test-engineer** — writing integration tests against FHIR sandboxes, mocking EHR responses, and validating audit trail completeness
- **devops-release-engineer** — for HIPAA-compliant infrastructure pipelines: encryption-at-rest enforcement, VPC configurations, and audit log archival automation

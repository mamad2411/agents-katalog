---
name: ehr-integration
description: "Integrate with Electronic Health Record (EHR) systems including Epic, Cerner, and other FHIR-compliant platforms. Covers FHIR R4 APIs, SMART on FHIR authentication, patient data access, clinical workflows, and HIPAA compliance."
license: Apache 2.0
tags: ["ehr", "epic", "cerner", "fhir", "healthcare", "hipaa", "clinical", "health-it"]
difficulty: advanced
time_to_master: "14-24 weeks"
version: "1.0.0"
---

# EHR Integration

## Overview

Electronic Health Record (EHR) systems — primarily Epic (38% market share) and Oracle Health/Cerner (22%) — manage patient data for hospitals and health systems. The HL7 FHIR (Fast Healthcare Interoperability Resources) standard provides a modern REST API for accessing patient demographics, clinical observations, medications, allergies, and care plans. Integrating with EHR systems enables AI-powered clinical decision support, care coordination, and administrative automation.

## When to Use This Skill

- Building FHIR-compliant integrations with Epic or Cerner
- Implementing SMART on FHIR authentication for healthcare apps
- Creating patient data access workflows (demographics, conditions, medications)
- Building clinical decision support tools
- Automating healthcare administrative workflows (scheduling, referrals)

## Core Concepts

### EHR Platform Landscape

| Platform | Market Share | FHIR Support | Auth | Certification |
|----------|-------------|-------------|------|---------------|
| Epic | 38% | FHIR R4 | SMART on FHIR | ONC-certified |
| Oracle Health (Cerner) | 22% | FHIR R4 | SMART on FHIR | ONC-certified |
| MEDITECH | 16% | FHIR R4 | SMART on FHIR | ONC-certified |
| Allscripts | 5% | FHIR R4 | OAuth 2.0 | ONC-certified |

### FHIR Resource Types

```
Patient ──────────► Demographics (name, DOB, address, contact)
  │
  ├── Condition ──► Diagnoses (ICD-10 codes, onset, status)
  │
  ├── Observation ► Vitals, lab results (LOINC codes)
  │
  ├── MedicationRequest ► Prescriptions (RxNorm codes)
  │
  ├── AllergyIntolerance ► Allergies & drug sensitivities
  │
  ├── Procedure ──► Surgical/clinical procedures (CPT codes)
  │
  ├── Encounter ──► Visits, admissions, appointments
  │
  ├── DocumentReference ► Clinical notes, reports
  │
  └── CarePlan ───► Treatment plans with goals and activities
```

### SMART on FHIR Authentication

```
┌──────────┐     ┌──────────────┐     ┌──────────┐
│  App     │────►│ EHR Auth     │────►│ Launch   │
│          │     │ Endpoint     │     │ Context  │
└──────────┘     └──────────────┘     └────┬─────┘
                                          │
     ┌─────────────────────────────────────┘
     │ authorization_code + launch context
     ▼
┌──────────┐     ┌──────────────┐
│ Token    │────►│ FHIR Server  │
│ Exchange │     │ (with token) │
└──────────┘     └──────────────┘
```

## Implementation Guide

### FHIR Client Setup

```typescript
import FHIR from "fhirclient";

// SMART on FHIR launch
FHIR.oauth2.authorize({
  clientId: process.env.FHIR_CLIENT_ID,
  scope: "launch patient/Patient.read patient/Observation.read patient/Condition.read patient/MedicationRequest.read",
  redirectUri: "/callback",
});

// After authorization - query patient data
const client = await FHIR.oauth2.ready();

// Get patient demographics
const patient = await client.patient.read();
console.log(`Patient: ${patient.name[0].given.join(" ")} ${patient.name[0].family}`);
console.log(`DOB: ${patient.birthDate}`);
console.log(`MRN: ${patient.identifier.find(i => i.type?.coding?.[0]?.code === "MR")?.value}`);
```

### Querying Clinical Data

```typescript
// Get active conditions (diagnoses)
const conditions = await client.request(
  `Condition?patient=${patientId}&clinical-status=active&_sort=-onset-date&_count=20`
);

// Get recent lab results
const labs = await client.request(
  `Observation?patient=${patientId}&category=laboratory&_sort=-date&_count=20`
);

// Get current medications
const medications = await client.request(
  `MedicationRequest?patient=${patientId}&status=active&_include=MedicationRequest:medication`
);

// Get allergies
const allergies = await client.request(
  `AllergyIntolerance?patient=${patientId}&clinical-status=active`
);

// Search patients by identifier or name
const patients = await client.request(
  `Patient?family=Smith&given=John&birthdate=1985-03-15`
);
```

### Patient Summary Builder

```typescript
async function buildPatientSummary(client, patientId) {
  // Fetch all relevant data in parallel
  const [patient, conditions, meds, allergies, vitals] = await Promise.all([
    client.request(`Patient/${patientId}`),
    client.request(`Condition?patient=${patientId}&clinical-status=active`),
    client.request(`MedicationRequest?patient=${patientId}&status=active`),
    client.request(`AllergyIntolerance?patient=${patientId}`),
    client.request(`Observation?patient=${patientId}&category=vital-signs&_sort=-date&_count=10`),
  ]);

  return {
    demographics: {
      name: formatName(patient.name[0]),
      dob: patient.birthDate,
      gender: patient.gender,
      mrn: getMRN(patient),
    },
    activeConditions: conditions.entry?.map(e => ({
      condition: e.resource.code.text || e.resource.code.coding[0].display,
      icd10: e.resource.code.coding.find(c => c.system.includes("icd"))?.code,
      onset: e.resource.onsetDateTime,
    })) || [],
    medications: meds.entry?.map(e => ({
      medication: e.resource.medicationCodeableConcept?.text || "Unknown",
      dosage: e.resource.dosageInstruction?.[0]?.text,
      prescriber: e.resource.requester?.display,
    })) || [],
    allergies: allergies.entry?.map(e => ({
      substance: e.resource.code.text,
      reaction: e.resource.reaction?.[0]?.manifestation?.[0]?.text,
      severity: e.resource.reaction?.[0]?.severity,
    })) || [],
    recentVitals: vitals.entry?.map(e => ({
      type: e.resource.code.text,
      value: `${e.resource.valueQuantity?.value} ${e.resource.valueQuantity?.unit}`,
      date: e.resource.effectiveDateTime,
    })) || [],
  };
}
```

### Clinical Terminology

| System | Purpose | Example |
|--------|---------|---------|
| ICD-10 | Diagnoses | E11.9 (Type 2 Diabetes) |
| LOINC | Lab tests/vitals | 2339-0 (Blood Glucose) |
| RxNorm | Medications | 860975 (Metformin 500mg) |
| CPT | Procedures | 99213 (Office Visit) |
| SNOMED CT | Clinical terms | 44054006 (Diabetes mellitus) |

## HIPAA Compliance Requirements

| Requirement | Implementation |
|-------------|---------------|
| Minimum Necessary | Only request FHIR resources needed for the use case |
| Access Logging | Log every FHIR API call with user, patient, resource, timestamp |
| Encryption at Rest | Encrypt stored PHI with AES-256 |
| Encryption in Transit | TLS 1.2+ for all API calls |
| Access Controls | Role-based access, session timeouts, MFA |
| Audit Trail | Immutable log of all PHI access and modifications |
| BAA | Execute Business Associate Agreement before accessing PHI |
| De-identification | Remove 18 HIPAA identifiers for research/analytics use |

## Best Practices

1. **Always use SMART on FHIR** — don't build custom auth for EHR access
2. **Minimize data access** — only request the FHIR resources you need
3. **Cache nothing containing PHI** — or encrypt with strict TTLs
4. **Use `_include` to reduce round trips** — fetch related resources in one call
5. **Handle pagination** — FHIR bundles use `link[rel=next]` for pagination
6. **Test in sandbox first** — both Epic and Cerner provide FHIR sandboxes
7. **Map clinical codes carefully** — always cross-reference ICD-10, LOINC, RxNorm

## Resources

- [HL7 FHIR R4 Specification](https://www.hl7.org/fhir/)
- [Epic FHIR Documentation](https://fhir.epic.com/)
- [SMART on FHIR Guide](https://docs.smarthealthit.org/)
- [fhirclient.js Library](https://github.com/smart-on-fhir/client-js)

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-03-31 | Initial documentation |

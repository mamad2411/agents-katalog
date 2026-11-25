---
name: healthcare-systems
version: 1.0.0
min_mindforge_version: 10.2.0
status: stable
triggers: healthcare system, HIPAA compliance, HL7 FHIR, PHI handling, clinical workflow, EHR integration, health data exchange, medical record system, healthcare interoperability, patient data protection, health information exchange, clinical data model
compose: compliance-as-code
---

# Skill — Healthcare Systems

## When this skill activates
This skill activates when designing, building, or auditing healthcare systems that handle Protected Health Information (PHI), integrate with Electronic Health Records (EHR), implement clinical workflows, or require HIPAA compliance and healthcare interoperability standards.

## Mandatory actions when this skill is active

### Before writing any code
1. Conduct HIPAA compliance audit: identify all PHI touchpoints (patient names, DOB, SSN, medical records, diagnoses, prescriptions) and document encryption requirements (AES-256 at rest, TLS 1.3 in transit)
2. Review HL7 FHIR resource specifications for all clinical data models (Patient, Observation, Condition, MedicationRequest, Encounter) and validate against FHIR R4 or R5 conformance requirements
3. Map clinical workflows to business requirements: patient registration, provider authentication, order entry (CPOE), medication administration records (MAR), clinical notes (SOAP), discharge summaries, and continuity of care documents (CCD)

### During implementation
- Implement BAA-compliant audit logging for all PHI access: capture user identity, timestamp, action type, resource accessed, IP address, and store logs in WORM (write-once-read-many) storage with 7-year retention
- Enforce role-based access control (RBAC) with principle of least privilege: separate roles for physicians, nurses, pharmacists, billing staff, and patients, with explicit consent workflows for data sharing between organizations
- Use FHIR-native authentication (SMART on FHIR) with OAuth 2.0 authorization code flow, patient-level scopes (patient/*.read), and refresh token rotation for mobile health apps
- Implement de-identification pipelines for research datasets: remove 18 HIPAA identifiers (names, dates, geocodes, phone numbers, medical record numbers) using regex patterns and NLP entity recognition
- Design interoperability interfaces using FHIR REST APIs with proper content negotiation (application/fhir+json), search parameters (?patient=123&category=vital-signs), and batch/transaction bundles for atomic operations

### After implementation
- Execute security testing: penetration testing for OWASP Top 10 healthcare vulnerabilities (SQL injection in patient search, XSS in clinical notes, broken authentication), vulnerability scanning, and threat modeling for ransomware/data exfiltration scenarios
- Validate FHIR conformance using HL7 validation tools: check resource structure, cardinality constraints, required terminology bindings (LOINC for labs, SNOMED CT for diagnoses, RxNorm for medications), and profile compliance
- Conduct end-to-end clinical workflow testing with real provider scenarios: patient check-in, vital signs capture, order placement, results review, prescription writing, and documentation with audit trail verification

## Self-check before task completion
- [ ] All PHI is encrypted at rest (AES-256) and in transit (TLS 1.3), with key management via HSM or cloud KMS
- [ ] Audit logs capture all PHI access events with user attribution and are tamper-evident (cryptographic hashing or blockchain anchoring)
- [ ] FHIR resources validate against published profiles, use standard terminologies (LOINC/SNOMED/RxNorm), and implement proper search parameters
- [ ] Access control enforces least privilege, requires MFA for administrative access, and implements automatic session timeouts (15 minutes idle)
- [ ] Business Associate Agreement (BAA) requirements are documented, including breach notification procedures and subprocessor agreements
- [ ] Clinical workflows have been validated by domain experts (physicians, nurses) for safety and usability

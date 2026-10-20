---
name: database-security-auditor
description: Audit database security. Use when reviewing DB access, encryption,
  and data protection.
metadata:
  tags: database, security, auditor
---

# Database Security Auditing

## Use this skill when
- Reviewing DB access and roles
- Checking encryption posture
- Verifying data protection and audit trails

## Do not use this skill when
- App-level auth (use auth skills)
- Network-wide security (use infrastructure-security)

## Instructions
1. Map who can access the database and with what rights.
2. Check default accounts, shared creds, and password policies.
3. Verify encryption at rest and in transit.
4. Review audit logging for privileged and schema changes.
5. Check export/backup exposure and cleanup.
6. Assess sensitive columns and masking/redaction.
7. Report with severity and remediation.

## Checklist
- Least privilege holds
- Encryption on
- Audit trail active

## Output Format
- Area | finding | severity | fix

## Common Mistakes
- Assuming the network protects the DB
- Missing backup/export exposure
- Skipping enormous-privilege accounts

## References
- `references/checklist.md` – Access, encryption, data protection, exposure, and operations checklist

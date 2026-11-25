---
name: clinical-compliance-doc
description: >
  Ensures all development meets clinical compliance and security standards.
  Focuses on HIPAA-friendly logging, audit trails, risk assessment, and scientific nomenclature.
---

# Clinical Compliance & Security

This skill provides guidelines for maintaining the documentation and architectural safeguards required for clinical environments.

## Compliance Standards

- **HIPAA**: Ensure no PHI (Protected Health Information) is logged or stored.
- **Audit Trails**: Every write operation to the database or GCS must be logged with a timestamp and actor ID.
- **Synthetic Data Only**: This repo uses synthetic patient data exclusively (PatientOne: PAT001-OVC-2025). No real patient data should ever be committed.

## Scientific Nomenclature

When editing data loaders, models, or documentation:
- **Gene names**: Follow HUGO standards (e.g., use `GZMB`, not `gzm-b`; use `BRCA1`, not `brca-1`)
- **Disease labels**: Use consistent terminology (e.g., `HGSOC` for High-grade serous ovarian cancer)
- **Tissue/cell type labels**: Must match the project ontology in PatientOne data

## Infrastructure Hooks

Use the tools in `infrastructure/` to enforce compliance:
- **Audit Logs**: Reference `infrastructure/audit/` for current logging schemas
- **Hospital Deployment**: Follow the patterns in `infrastructure/hospital-deployment/` when drafting deployment plans

## Code Review Checklist

When reviewing PRs for compliance:
- [ ] Check for hardcoded credentials or API keys
- [ ] Verify `allow_list` vs `block_list` configs for data tools
- [ ] Ensure error messages do not leak internal system paths or data snippets
- [ ] Gene names follow HUGO standards
- [ ] No PHI/PII in logs, comments, or test fixtures

---

**Use this skill when:**
- Drafting implementation plans for clinical features
- Reviewing infrastructure changes
- Writing security reports for funders or hospital partners
- Verifying scientific nomenclature in code or documentation

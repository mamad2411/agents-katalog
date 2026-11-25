---
name: phi-compliance-checker
description: Scan codebases for PHI/PII patterns before customer demos. Detects HIPAA Safe Harbor identifiers, healthcare-specific IDs (MRN, NPI, DEA), and clinical data formats (HL7, FHIR) in code, SQL, configs, and notebooks.
triggers:
  - scan for PHI
  - check for HIPAA compliance
  - PHI compliance check
  - is this demo safe to show
  - check for patient data
  - scan for PII
  - pre-demo compliance check
---

# PHI Compliance Checker

Scan a project directory for PHI/PII patterns grounded in HIPAA Safe Harbor (18 identifiers). Detects SSNs, MRNs, patient names, DOB, phone numbers, NPI/DEA numbers, HL7 segments, and FHIR references in source code, SQL, configs, CSV, and notebooks.

## Quick Start

Run the scanner against the target directory:

```bash
python3 {{skill_path}}/resources/phi_scanner.py /path/to/project
```

## Workflow

<step number="1">
Run the scanner against the target directory. Default output is a colored terminal report.

```bash
python3 {{skill_path}}/resources/phi_scanner.py TARGET_DIR
```

For CI or downstream processing, use JSON:

```bash
python3 {{skill_path}}/resources/phi_scanner.py TARGET_DIR --format json --output phi-report.json
```

Additional options:
- `--severity critical` — only show CRITICAL findings
- `--respect-gitignore` — skip files in .gitignore
- `--patterns custom.json` — load org-specific pattern overrides
- `--no-color` — disable ANSI colors
</step>

<step number="2">
Present findings to the user grouped by severity:

- **CRITICAL** — must be fixed before any demo (real SSNs, MRNs, patient names)
- **WARNING** — review and confirm data is synthetic (DOB, phone, PHI column names)
- **INFO** — awareness items (HL7 segments, FHIR references, IP addresses)

For each CRITICAL finding, suggest a specific fix:
- Real-looking SSN → replace with `000-00-0000` or remove
- MRN with real format → replace with `PAT00001` style synthetic ID
- Patient name → replace with `Patient A` / `John Doe`
- DOB → replace with `1900-01-01` or remove
</step>

<step number="3">
If the user approves fixes, apply them. Then re-scan to verify:

```bash
python3 {{skill_path}}/resources/phi_scanner.py TARGET_DIR --severity critical
```

A clean scan (exit code 0) means no CRITICAL or WARNING findings remain.
</step>

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Clean — no CRITICAL or WARNING findings |
| 1 | WARNING findings present — review recommended |
| 2 | CRITICAL findings — must remediate before demo |

## Custom Patterns

Create a JSON override file to add org-specific patterns:

```json
{
  "custom_patterns": [
    {
      "name": "org_mrn",
      "pattern": "HOSP-\\d{8}",
      "severity": "CRITICAL",
      "safe_harbor_id": 8,
      "description": "Hospital-specific MRN format"
    }
  ],
  "allowlist_patterns": ["TESTPAT-\\d+"],
  "allowlist_names": ["Dr. Demo"]
}
```

Then run: `python3 phi_scanner.py . --patterns custom.json`

## Suppressing Findings

Create a `.phi-scan-ignore` file at the project root (same syntax as `.gitignore`) to suppress findings in specific files or directories:

```
# Exclude reference docs with intentional PHI examples
docs/phi-examples/
tests/fixtures/phi_samples.csv
```

## What It Detects

| Category | Safe Harbor # | Severity | Validated |
|----------|:---:|:---:|:---:|
| SSN | 7 | CRITICAL | Prefix validation |
| MRN | 8 | CRITICAL | Format check |
| Patient names | 1 | WARNING→CRITICAL | Context escalation |
| Phone numbers | 4 | INFO→WARNING | Context escalation |
| Email | 6 | INFO→WARNING | Context escalation |
| DOB | 3 | WARNING | Label detection |
| Addresses | 2 | INFO→WARNING | Context escalation |
| PHI columns | — | WARNING | Schema keywords |
| NPI | 18 | WARNING | Luhn checksum |
| DEA | 11 | WARNING | DEA checksum |
| HL7 segments | — | INFO | Segment prefix |
| FHIR refs | — | INFO | Resource type |

## References

- [HIPAA Safe Harbor Method](https://www.hhs.gov/hipaa/for-professionals/privacy/special-topics/de-identification/index.html)
- [NIST SP 800-188](https://csrc.nist.gov/publications/detail/sp/800-188/final)
- [Philter (UCSF)](https://github.com/BCHSI/philter-ucsf)
- [Microsoft Presidio](https://github.com/microsoft/presidio)

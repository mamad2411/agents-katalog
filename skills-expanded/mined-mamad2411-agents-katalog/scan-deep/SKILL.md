---
name: scan-deep
description: "Deep security scan that enriches an initial JSON scan report. Reads a basic scan JSON (with target, stack, and initial findings), performs in-depth validation and discovery using scan-fase methodologies, removes false positives, and outputs an enriched JSON validated against the Pydantic schema. This skill should be used when the user provides a basic scan JSON and wants a deeper security analysis. Invoke with /scan-deep {client_name}."
---

# Deep Security Scan

## Purpose

Take an initial basic scan JSON and go deeper: validate existing findings, identify false
positives, discover new vulnerabilities through hands-on testing, and produce an enriched
JSON output in the standard format validated against the Pydantic schema.

## Invocation

```
/scan-deep {client_name}
```

## Prerequisites

- Initial scan JSON must exist at `clients/{client_name}/initial-scan.json`
- JSON must conform to the `ScanReport` Pydantic schema (see `app/models/scan_output.py`)

## Workflow

### Phase 1: Load and Parse Initial Scan

1. Read `clients/{client_name}/initial-scan.json`
2. Validate against Pydantic schema:
   ```bash
   python -m app.validators.finding_validator clients/{client_name}/initial-scan.json
   ```
3. Extract `target.url`, `target.domain`, `stack`, and existing `findings`
4. If validation fails, report errors and stop

### Phase 2: Analyze Initial Findings

For each finding in the initial JSON:

1. **Classify** as actionable or noise:
   - Findings on non-existent technology (e.g., WordPress paths on a Next.js site) = false positive
   - Duplicate findings covering the same issue = merge into one
   - Findings without real evidence = flag for re-testing
2. **Mark for validation** findings that need hands-on verification
3. **Note severity** findings that may be over/under-rated

### Phase 3: Deep Reconnaissance

Based on `stack` detected, execute relevant discovery:

**For any stack:**
- Extract all JS bundle URLs and analyze for secrets, API endpoints, env vars
- Probe common API routes (/api/*, /graphql, /auth/*)
- Test security headers (CSP, HSTS, X-Frame-Options, etc.)
- Test CORS configuration with multiple origins
- Check for source maps, debug endpoints, exposed configs

**For Supabase backends:**
- Extract Supabase URL and anon key from JS bundles
- Run GraphQL introspection to discover full schema
- Test RLS on ALL discovered tables (REST + GraphQL)
- Test RPC functions for anonymous access
- Check auth settings (disable_signup, mailer_autoconfirm)
- Test storage buckets
- Test write operations (INSERT/UPDATE/DELETE) on each table

**For Firebase backends:**
- Extract Firebase config from JS
- Test Firestore rules
- Test Realtime Database rules
- Check Storage rules
- Test Cloud Functions

**For Custom API backends (Django, FastAPI, Node.js, etc.):**
- Enumerate API endpoints from JS bundles
- Test authentication endpoints for rate limiting
- Check for admin panel exposure (/admin/, /docs, /swagger)
- Test IDOR on discovered endpoints
- Check for debug mode indicators

### Phase 4: Targeted Testing

Based on initial findings and discovery, run targeted tests:

| Initial Finding | Deep Test |
|---|---|
| Missing headers | Verify each header, test exploitability |
| No rate limiting | Test with actual requests (15+), check all auth endpoints |
| CORS issues | Test origin reflection vs wildcard, check credentials header |
| RLS issues | Test ALL CRUD operations, test via GraphQL too |
| Auth weaknesses | Test password policy, user enumeration, signup flow |
| Exposed secrets | Verify if keys are valid and what access they grant |

### Phase 5: False Positive Analysis

For each finding (initial + new), apply these checks:

1. **CORS on Supabase**: If origin reflection exists but NO `Access-Control-Allow-Credentials` header
   and auth is via API key (not cookies), downgrade to INFO (default Supabase behavior)
2. **GraphQL introspection on Supabase**: If RLS is active on most tables and data is protected,
   classify as INFO (schema exposed but data safe)
3. **Admin paths returning 403**: If the technology is NOT the one probed (e.g., /wp-admin on Next.js),
   remove as false positive (Vercel returns 403 for any non-existent path)
4. **Duplicate findings**: Merge findings about the same underlying issue (e.g., missing X-Frame-Options
   should not appear as both a header issue AND a clickjacking/auth bypass issue)
5. **HSTS contradiction**: If one finding says HSTS is missing and another says HSTS is weak,
   test and keep only the accurate one
6. **Potential/unconfirmed findings**: Remove any finding that says "potential" or "possible" without
   actual proof-of-concept evidence
7. **Unverified version-dependent findings (100% Certainty Rule)**:
   - If a finding depends on a specific software version (e.g., CVE affecting n8n < 1.121.0) and the version CANNOT be determined remotely, do NOT classify as HIGH/CRITICAL
   - Downgrade to MEDIUM and prefix evidence with "UNVERIFIED:"
   - Add "ACTION REQUIRED: Client must verify version" in evidence
   - Severity MUST reflect only what was ACTUALLY proven, never what could theoretically happen
   - A service being publicly accessible = confirmed finding (open_port/sensitive_data_exposed)
   - A service being vulnerable to a specific CVE = ONLY confirmed if version is verified

### Phase 6: Build Output JSON

1. Start with initial scan `target` and `stack` (enrich `stack` if new info discovered)
2. Build findings list:
   - Keep validated initial findings (with corrected severity if needed)
   - Add new findings discovered during deep testing
   - Remove false positives identified in Phase 5
   - Assign sequential IDs: FIND-001, FIND-002, etc.
   - Order by severity: CRITICAL, HIGH, MEDIUM, LOW, INFO
3. Every finding MUST have:
   - `evidence`: at least one concrete proof item (curl command + response, actual data seen)
   - `cwe`: valid CWE identifier (or null if not applicable)
   - `type`: value from `FindingType` enum (see `app/models/enums.py`)
   - `category`: value from `Category` enum
4. Validate output against Pydantic schema:
   ```bash
   python -m app.validators.finding_validator clients/{client_name}/deep-scan.json
   ```

### Phase 7: Write Output

Save the enriched JSON to `clients/{client_name}/deep-scan.json`

## Output Format

The output MUST conform to the `ScanReport` Pydantic model:

```json
{
  "target": {
    "url": "https://example.com/",
    "domain": "example.com"
  },
  "stack": {
    "framework": "Next.js",
    "technologies": ["Vercel", "Tailwind CSS"],
    "cdn_waf": "Vercel",
    "webserver": "Vercel",
    "backend": "Supabase",
    "backend_project": "abcdefghijk"
  },
  "findings": [
    {
      "id": "FIND-001",
      "type": "rls_missing",
      "name": "RLS Missing on org_overrides",
      "severity": "CRITICAL",
      "category": "access_control",
      "location": {
        "endpoint": "/rest/v1/org_overrides",
        "parameter": null,
        "method": "GET/POST/PATCH/DELETE"
      },
      "evidence": [
        "GET returns all records with anon key",
        "POST with test data returned HTTP 201",
        "Test data cleaned up after verification"
      ],
      "cwe": "CWE-862"
    }
  ]
}
```

## Validation

Reference files for valid enum values:
- `app/models/enums.py` - All valid values for `severity`, `category`, `type`
- `app/models/scan_output.py` - Full Pydantic model definitions
- `schemas/scan-output.schema.json` - Generated JSON Schema

To validate any scan JSON:
```bash
python -m app.validators.finding_validator path/to/scan.json
```

## Key Principles

1. **Only confirmed vulnerabilities** - Every finding must have proof-of-concept evidence
2. **No false positives** - Apply Phase 5 checks rigorously
3. **Clean up after testing** - If write tests succeed, revert/delete test data
4. **Accurate severity** - Follow CVSS scoring, do not inflate
5. **Consistent format** - All output validated against Pydantic schema
6. **Enrich, not replace** - Build on the initial scan, do not ignore it

## Error Handling

- If initial JSON is invalid: report validation errors and stop
- If target is unreachable: set finding status and continue with what is testable
- If a test is blocked (e.g., signup disabled): document as evidence, not as vulnerability
- If tools are unavailable (nuclei, nmap): skip those tests, note in output

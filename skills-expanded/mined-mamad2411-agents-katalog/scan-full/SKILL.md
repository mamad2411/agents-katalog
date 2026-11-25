---
name: scan-full
description: "Execute a complete end-to-end security scan orchestrating all phases (FASE 0-21) in optimized parallel waves, then enrich results via /scan-deep to produce the final validated JSON report. This skill should be used when the user wants to run a full security scan on a target URL without manually invoking each phase. Invoke with /scan-full {url} {client_name}."
---

# Full Security Scan Orchestrator

Execute all scan phases (FASE 0 through FASE 21) on a target URL using optimized parallel waves, then enrich results with `/scan-deep` to produce the final validated JSON report.

## Invocation

```
/scan-full {target_url} {client_name}
```

**Example:** `/scan-full https://myapp.com myapp`

## Parameters

- `{target_url}` - Target URL to scan (required)
- `{client_name}` - Client folder name under `clients/` (required)

## Execution Workflow

### Step 1: Setup

1. Create the client directory:
   ```bash
   mkdir -p clients/{client_name}
   ```
2. Initialize `clients/{client_name}/SCAN-IN-PROGRESS.md` with target URL and start timestamp

### Step 2: Ownership Verification

Verify ownership of the target domain before any invasive tests:
1. Meta tag: `<meta name="securedev-verify" content="sd_verify_{token}" />`
2. DNS TXT: `_securedev-verify.{domain}`
3. .well-known file: `https://{domain}/.well-known/securedev-verify.txt`
4. Root file: `https://{domain}/securedev-verify.txt`

If ownership cannot be verified, STOP and ask the user for confirmation. Do NOT proceed with invasive testing without authorization.

### Step 3: WAVE 1 - Backend Detection (Sequential, MANDATORY FIRST)

Invoke `/scan-fase-0 {target_url}` and wait for completion.

Record from results:
- `backend_type` (supabase, firebase, custom_api, etc.)
- `configs_extracted` (URLs, keys, project IDs)
- `scan_path` (applicable phases)
- `app_subdomains` (discovered application subdomains)

If app subdomains found, expand scope to include them in all subsequent phases.

### Step 4: WAVE 2 - Independent Reconnaissance (6 Parallel)

Launch these 6 phases in parallel using the Agent tool (`subagent_type: "general-purpose"`). Each agent invokes its corresponding `/scan-fase-N` skill:

| Agent | Skill to Invoke | Description |
|-------|-----------------|-------------|
| 1 | `/scan-fase-1 {url}` | Adaptive Reconnaissance |
| 2 | `/scan-fase-7 {url}` | Security Headers Analysis |
| 3 | `/scan-fase-10 {url}` | Third-Party Discovery |
| 4 | `/scan-fase-11 {url}` | Auth Bypass Testing |
| 5 | `/scan-fase-12 {url}` | JS Bundle Deep Analysis |
| 6 | `/scan-fase-19 {url}` | Infrastructure & Network Testing |

Wait for all 6 to complete before proceeding.

### Step 5: WAVE 3 - Config-Dependent Phases (3 Parallel)

Launch these 3 phases in parallel:

| Agent | Skill to Invoke | Description |
|-------|-----------------|-------------|
| 1 | `/scan-fase-2 {url}` | Schema Discovery |
| 2 | `/scan-fase-5 {url}` | Authentication Testing |
| 3 | `/scan-fase-8 {url}` | JWT Analysis |

Wait for all 3 to complete before proceeding.

### Step 6: WAVE 4 - Schema-Dependent Phases (Up to 10 Parallel)

Launch applicable phases based on backend type from FASE 0:

| Agent | Skill to Invoke | Condition |
|-------|-----------------|-----------|
| 1 | `/scan-fase-3 {url}` | Supabase only |
| 2 | `/scan-fase-4 {url}` | Supabase only |
| 3 | `/scan-fase-6 {url}` | If WebSocket/Realtime detected |
| 4 | `/scan-fase-9 {url}` | Always |
| 5 | `/scan-fase-15 {url}` | Always |
| 6 | `/scan-fase-16 {url}` | Always |
| 7 | `/scan-fase-17 {url}` | If GraphQL detected |
| 8 | `/scan-fase-18 {url}` | If WebSocket detected |
| 9 | `/scan-fase-20 {url}` | Supabase only |
| 10 | `/scan-fase-21 {url}` | Always |

Skip phases that do not apply to the detected backend.

### Step 7: WAVE 5 - Authenticated Testing (Conditional)

Invoke `/scan-fase-14 {url}` only if:
- Test credentials are available, OR
- Signup is enabled (`disable_signup: false`)

If blocked, document: "FASE 14 blocked - signup disabled by design (POSITIVE security measure)" and proceed.

### Step 8: Compile Initial Scan JSON

After all phases complete:

1. Collect all findings from every phase
2. Deduplicate (same vulnerability from multiple phases)
3. Assign sequential IDs: FIND-001, FIND-002, etc.
4. Order by severity: CRITICAL > HIGH > MEDIUM > LOW > INFO
5. Build the `ScanReport` JSON:
   ```json
   {
     "target": { "url": "{url}", "domain": "{domain}" },
     "stack": { "framework": "...", "technologies": [...], "backend": "..." },
     "findings": [...]
   }
   ```
6. Save to `clients/{client_name}/initial-scan.json`
7. Validate:
   ```bash
   python -m app.validators.finding_validator clients/{client_name}/initial-scan.json
   ```
8. Fix any validation errors and re-validate until VALID

### Step 9: Deep Scan Enrichment

Invoke `/scan-deep {client_name}` to:
- Re-validate all findings with hands-on testing
- Remove false positives
- Discover additional vulnerabilities
- Produce `clients/{client_name}/deep-scan.json`

### Step 10: Final Validation and Judge Mode

1. Validate deep scan JSON:
   ```bash
   python -m app.validators.finding_validator clients/{client_name}/deep-scan.json
   ```

2. Self-review (Judge Mode):
   - Every finding has test evidence
   - CVSS scores are accurate (no inflation)
   - No unverified findings marked as confirmed
   - Severity matches actual impact
   - No duplicates

3. Present summary to user:
   - Total findings by severity breakdown
   - Key critical/high vulnerabilities
   - Phases completed vs skipped
   - Final JSON path: `clients/{client_name}/deep-scan.json`

## Error Handling

- **Phase fails**: Log error in SCAN-IN-PROGRESS.md, continue with remaining phases, note in final report
- **Ownership fails**: STOP entirely, ask user
- **Backend not detected**: Use minimal scan path (FASE 1, 7, 12, 15, 21)
- **Validation fails**: Fix JSON errors and re-validate before delivering

## Output Files

| File | Description |
|------|-------------|
| `clients/{client_name}/SCAN-IN-PROGRESS.md` | Live progress log |
| `clients/{client_name}/initial-scan.json` | Raw scan results (all phases) |
| `clients/{client_name}/deep-scan.json` | Final enriched + validated JSON |

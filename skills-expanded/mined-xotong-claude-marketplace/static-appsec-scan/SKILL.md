---
name: static-appsec-scan
description: Use AskUserQuestion for scan type, auto-detect inputs, run scans, then offer remediation
---

# Static AppSec Scan

This skill uses `AskUserQuestion` to get the user's scan type choice, then automatically detects technical inputs (language, image) from the repository.

## Important: Use `AskUserQuestion` Tool for All User Prompts

**CRITICAL:** Use the `AskUserQuestion` tool for all user interactions. Never run shell scripts without command-line arguments.

**Correct pattern:**
1. Call `AskUserQuestion` to get user's choice
2. Wait for the user's response (tool pauses for input)
3. Use the returned answer to build command-line arguments
4. Run the shell script with all arguments specified

## Step 1: Ask User for Scan Type (Required)

**Always use `AskUserQuestion` tool** — do not auto-detect the scan type and do not use shell prompts.

Call `AskUserQuestion` with these 4 options. For "all", user types "all" in chat:

```json
{
  "questions": [{
    "question": "What type of security scan would you like to run? (Type 'all' in chat for full scan)",
    "header": "Scan type",
    "options": [
      {"label": "Secret Detection", "description": "Find exposed credentials and secrets"},
      {"label": "Image Scan", "description": "Scan container image for vulnerabilities"},
      {"label": "SAST", "description": "Static Application Security Testing (code)"},
      {"label": "SCA", "description": "Software Composition Analysis (dependencies)"}
    ],
    "multiSelect": false
  }]
}
```

**Handle user input:**
- If user selects an option from the UI → use that scan type
- If user types "all" in chat → run `--scan-type all`

**Map the selection to `--scan-type` value:**
| Returned label | `--scan-type` value |
|----------------|---------------------|
| "Secret Detection" | `secret` |
| "Image Scan" | `container` |
| "SAST" | `sast` |
| "SCA" | `dependency` |
| User types "all" | `all` |

**CRITICAL:** After receiving the answer, immediately run the script with `--scan-type` specified. Never run `./scripts/run-static-scan.sh` without arguments.

---

## Step 2: Auto-Detect Technical Inputs (Non-Interactive)

After the user selects a scan type, automatically detect the technical inputs:

```bash
# Run detection script (non-interactive mode - returns ALL Dockerfiles)
./plugins/appsec/skills/static-appsec-scan/scripts/detect-inputs.sh
```

The script outputs JSON with detected values:
```json
{
  "language": "javascript",
  "source_path": ".",
  "dockerfile_count": 3,
  "dockerfiles": ["Dockerfile", "services/api/Dockerfile", "services/web/Dockerfile.prod"]
}
```

**Detection logic:**
- **Languages**: Detects ALL languages present in the repo: `package.json`/`*.js`/`*.ts` (javascript), `pom.xml`/`*.java` (maven), `build.gradle` (gradle), `requirements.txt`/`pyproject.toml`/`uv.lock`/`*.py` (python including UV), `go.mod`/`*.go` (go)
- **Services**: Detects service directories by finding dependency manifests (e.g., `services/api/package.json`, `backend/pom.xml`). Each service is scanned separately for dependencies.
- **Source path**: Detects `src/` or `app/` directories, defaults to `.`
- **Dockerfiles**: Recursively searches the entire repository for all `Dockerfile` and `Dockerfile.*` files (case-insensitive)

**Multi-language SAST support:** When multiple languages are detected, SAST runs separately for each language and the reports are merged into a single combined report.

**Multi-service dependency scanning:** When multiple services are detected (e.g., monorepo with `services/api/package.json`, `services/web/package.json`, `backend/pom.xml`), dependency scanning runs separately for each service and merges all vulnerability findings into a combined report with service metadata.

### Batch Confirmation with User (Using AskUserQuestion)

**IMPORTANT:** Batch ALL questions into a single `AskUserQuestion` call to avoid multiple rounds:

```json
{
  "questions": [
    {
      "question": "Scan type: Image Scan. Found 3 Dockerfile(s). Which would you like to scan?",
      "header": "Select Dockerfiles",
      "options": [
        {"label": "All Dockerfiles", "description": "Scan all 3 detected Dockerfiles"},
        {"label": "Select specific", "description": "Choose which Dockerfiles to scan"},
        {"label": "Cancel", "description": "Skip this scan"}
      ],
      "multiSelect": false
    }
  ]
}
```

If user selects "Select specific", ask a follow-up `AskUserQuestion` with the list of Dockerfiles.

---

## Step 2a: Ask for JFROG_TOKEN (For Container Scans) - BATCHED

**For container scans**, check if the base images require JFROG authentication. Extract base images:

```bash
# Extract base image from each Dockerfile
for f in "${DOCKERFILES[@]}"; do
  grep -i "^FROM" "$f" | head -1 | awk '{print $2}'
done
```

Then **batch** the JFROG question together with the Dockerfile selection:

```json
{
  "questions": [{
    "question": "Base images are from private registry (docker-cicd-test.artifactory.<YOUR_DOMAIN>). Provide JFROG_TOKEN?",
    "header": "JFROG auth",
    "options": [
      {"label": "Yes, here's the token", "description": "I'll provide the JFROG_TOKEN"},
      {"label": "No, images are public", "description": "No authentication needed"}
    ],
    "multiSelect": false
  }]
}
```

If the user provides the token, pass it to the script via `--jfrog-token` argument to avoid interactive prompts.

---

## Step 2b: Run Detection with Selected Dockerfiles

Once the user has selected which Dockerfiles to scan and provided the JFROG_TOKEN (if needed), run the detection script with the `--dockerfiles` flag:

```bash
# Non-interactive: pass selected Dockerfiles as comma-separated list
./plugins/appsec/skills/static-appsec-scan/scripts/detect-inputs.sh --dockerfiles "services/chatbot/Dockerfile,services/gateway/Dockerfile"
```

This returns only the specified Dockerfiles without any interactive prompts.

---

## Step 3: Run the Scan

**IMPORTANT:** Run the script with all arguments provided. Never run it interactively.

**Before running, verify you have these values:**
- `SCAN_TYPE` — from Step 1 `AskUserQuestion` answer
- `LANGUAGE` — from auto-detect (Step 2) or user override
- `SOURCE_PATH` — from auto-detect (Step 2), usually `.`
- `DOCKERFILES` — comma-separated list from user selection
- `JFROG_TOKEN` — from Step 2a (only for container/all scans, if base image requires auth)

**For container scans with selected Dockerfiles:**

```bash
./plugins/appsec/skills/static-appsec-scan/scripts/run-static-scan.sh \
  --scan-type container \
  --language javascript \
  --source-path . \
  --dockerfiles "services/chatbot/Dockerfile,services/gateway/Dockerfile" \
  --jfrog-token "<TOKEN>"
```

**For other scan types (SAST, secret, dependency):**

```bash
./plugins/appsec/skills/static-appsec-scan/scripts/run-static-scan.sh \
  --scan-type <TYPE> \
  --language <LANG> \
  --source-path <PATH> \
  [--jfrog-token <TOKEN>]
```

**If you see prompts like "Select scan type: 1) 2) 3) 4)"** — you ran the script without arguments. Stop and re-run with `--scan-type` specified.

**Container Scan Flow (Multiple Dockerfiles):**
When `--scan-type container` or `--scan-type all` is specified:

1. The `detect-inputs.sh` script recursively searches for all Dockerfiles and prompts the user to confirm each one
2. For each confirmed Dockerfile:
   - The script updates the pipeline with the Dockerfile path
   - Runs `build_job` — builds the Docker image and saves it as a GitLab artifact
   - Runs `container_scanning` job — loads the image from artifact and scans it for vulnerabilities
   - Downloads scan results to a per-Dockerfile subdirectory: `glci-artifacts/container_<safe-name>/`
3. After all Dockerfiles are scanned:
   - All individual reports are merged into a single combined report
   - The merged report is saved as `gl-container-scanning-report-merged.json`
   - A copy is also saved as `gl-container-scanning-report.json` for backward compatibility

The `container_scanning` job always runs after `build_job` completes (enforced by the `needs` directive in the pipeline).

The script will:
1. Copy the pipeline template to the project root
2. Create `glci-artifacts/` directory
3. Loop through each confirmed Dockerfile, running `glci run container_scanning` for each
4. Merge all container scan reports into a combined report
5. Output a summary table with the **total findings aggregated across all scanned Dockerfiles**

**Artifact structure for multi-Dockerfile scans:**
```
glci-artifacts/
├── container_Dockerfile/
│   ├── container_scanning.zip
│   └── gl-container-scanning-report.json  (per-Dockerfile report)
├── container_services_api_Dockerfile/
│   ├── container_scanning.zip
│   └── gl-container-scanning-report.json  (per-Dockerfile report)
├── gl-container-scanning-report-merged.json  (all vulnerabilities combined)
└── gl-container-scanning-report.json  (copy of merged for backward compatibility)
```

**Do NOT:**
- Search for .gitlab-ci.yml
- Try to run glci directly
- Check for glci installation

**Scan type arguments:**
- `all` — Full scan (SAST + Secret Detection + Container + SCA). If multiple Dockerfiles are found, user is prompted to select which ones to scan. Each selected Dockerfile is built and scanned. **Multi-language SAST**: If multiple languages are detected, SAST runs separately for each language and reports are merged. **Multi-service dependency scanning**: If multiple services are detected (monorepo), dependency scanning runs for each service and merges findings.
- `secret` — Secret detection only
- `container` — Container image scan. If multiple Dockerfiles are found, user is prompted to select which ones to scan. Each selected Dockerfile is built and scanned.
- `sast` — Static Application Security Testing. **Multi-language support**: Automatically detects all languages in the repo and runs SAST for each one, then merges the reports.
- `dependency` — SCA/dependency scan. **Multi-service support**: Automatically detects all services in the repo (e.g., `services/api/`, `backend/`) and runs dependency scanning for each service, then merges all vulnerability findings into a combined report with service metadata.

---

## Step 4: Review Findings

After the scan completes, check the summary table output. If vulnerabilities were found, the script will list the report files:

- **SAST:** `glci-artifacts/gl-sast-report.json` (and `fortify.html`)
- **Secret Detection:** `glci-artifacts/gl-secret-detection-report.json`
- **Container Scanning:** 
  - Merged report (all Dockerfiles): `glci-artifacts/gl-container-scanning-report-merged.json`
  - Per-Dockerfile reports: `glci-artifacts/container_<name>/gl-container-scanning-report.json`
- **SCA/Dependency:**
  - Multi-service merged: `glci-artifacts/vulnerability-findings-<scan-id>-merged.json`
  - Per-service reports: `glci-artifacts/svc-<service-name>/vulnerability-findings-*.json`
  - Single service: `glci-artifacts/vulnerability-findings-*.json`

**For container scans with multiple Dockerfiles**, the merged report contains all vulnerabilities from all scanned images, with metadata showing which Dockerfiles were included. Individual per-Dockerfile reports are also retained in their respective subdirectories for detailed analysis of a specific image.

**For dependency scans with multiple services** (monorepo), the merged report contains all vulnerabilities from all scanned services, with each finding tagged with `service_path` and `service_language`. Individual per-service reports are retained in `glci-artifacts/svc-<service-name>/` subdirectories.

---

## Step 5: Remediation (User-Initiated)

**Only after the scan completes successfully**, prompt the user using `AskUserQuestion`:

```json
{
  "questions": [{
    "question": "Scan complete. Found " + count + " vulnerabilities. Would you like to remediate them one by one?",
    "header": "Remediate",
    "options": [
      {"label": "Yes, remediate", "description": "Fix vulnerabilities one by one"},
      {"label": "No, skip remediation", "description": "Review findings without making changes"}
    ],
    "multiSelect": false
  }]
}
```

Wait for the user's selection. If the user selects "Yes, remediate":

1. **Read the scan result files** to identify each vulnerability:
   - Parse the JSON reports to extract: vulnerability type, severity, file path, line number, description, and **suggested_solution** (if present)
   - List them for the user to review

2. **Remediate one vulnerability at a time using `AskUserQuestion`:**
   - Present the first vulnerability details (type, severity, file, line, description, suggested_solution)
   - Call `AskUserQuestion` for each fix decision:
   ```json
   {
     "questions": [{
       "question": "Fix this vulnerability?",
       "header": "Fix " + severity,
       "options": [
         {"label": "Apply fix", "description": "Apply the suggested remediation"},
         {"label": "Skip this one", "description": "Skip and move to next vulnerability"}
       ],
       "multiSelect": false
     }]
   }
   ```
   - If user selects "Apply fix": apply the fix, confirm completion
   - Move to the next vulnerability

3. **Continue until all vulnerabilities are addressed** or the user stops

**Remediation guidelines:**
- Always show the vulnerable code before suggesting changes
- Check for suggested_solution in the findings JSON first
- If no suggested_solution exists, use your own knowledge to propose a fix
- Suggest the minimal fix needed
- Never batch multiple fixes together
- Get explicit confirmation before each change

---

## Step 5a: Package Availability Check (For Dependency Remediations)

**IMPORTANT:** When a vulnerability remediation involves changing or upgrading a package/library (e.g., "upgrade lodash to 4.17.21", "replace moment.js with day.js"), you MUST check if the recommended package is available in the company's approved repositories before suggesting the fix.

### Available Company Repositories

The script checks these repositories:
- **npm-airlock:** `https://artifactory.<YOUR_DOMAIN>/artifactory/api/npm/npm-airlock/`
- **maven-airlock:** `https://artifactory.<YOUR_DOMAIN>/artifactory/maven-airlock`
- **pypi-airlock:** `https://artifactory.<YOUR_DOMAIN>/artifactory/api/pypi/pypi-airlock/simple`
- **docker-airlock:** `docker-airlock.artifactory.<YOUR_DOMAIN>`

### Check Package Availability

Before recommending a package upgrade or replacement, run the availability check:

```bash
# For JavaScript/npm packages
./plugins/appsec/skills/static-appsec-scan/scripts/check-package-availability.sh --package <package-name> --language javascript

# For Java/Maven packages
./plugins/appsec/skills/static-appsec-scan/scripts/check-package-availability.sh --package <group-id/artifact-id> --language java

# For Python packages
./plugins/appsec/skills/static-appsec-scan/scripts/check-package-availability.sh --package <package-name> --language python

# For Docker images
./plugins/appsec/skills/static-appsec-scan/scripts/check-package-availability.sh --package <image-name> --language docker
```

**Expected outputs:**
- `available:<repo-url>` — Package found in company repository (safe to recommend)
- `not_found` — Package not found in any company repository
- `error:<message>` — Check failed (handle gracefully)

### Decision Logic

**If package is available (`available:<repo-url>`):**
- Proceed with the remediation recommendation
- Include the repository URL in your recommendation so the user knows where to pull from
- Example: "Upgrade `lodash` to `4.17.21` (available at npm-airlock)"

**If package is NOT available (`not_found`):**
- Do NOT recommend upgrading to this package
- Tell the user: "This package is not available in the company's approved repositories. You will need to bring in the required package manually through the proper procurement process."
- Suggest alternative remediations if possible:
  - Code-level fixes that don't require new dependencies
  - Configuration changes
  - Using an already-approved alternative package

**Example remediation flow for dependency vulnerabilities:**

1. Identify the vulnerable package from the scan report
2. Determine the recommended fix (e.g., "upgrade to version X.Y.Z")
3. Run the availability check script
4. Based on the result:
   - **Available:** "The fix is to upgrade `<package>` to `<version>`. This package is available in the company npm-airlock repository. Run: `npm install <package>@<version>`"
   - **Not available:** "The recommended fix involves upgrading `<package>`, but this package is not available in the company's approved repositories. You will need to bring in the required package manually through the proper procurement process. Alternative: consider refactoring to avoid this dependency."

**Important:** This check applies only to remediations that involve adding or changing packages/libraries. It does NOT apply to:
- Code-level fixes (e.g., input validation, error handling)
- Configuration changes (e.g., setting security flags)
- Removing unused dependencies

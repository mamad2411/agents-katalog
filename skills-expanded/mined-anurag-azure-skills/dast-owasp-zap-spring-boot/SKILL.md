---
name: "dast-owasp-zap-spring-boot"
description: "Run Dynamic Application Security Testing (DAST) against deployed LeadPerfection Spring Boot 3.2.x microservices using OWASP ZAP — active scan, authenticated scan with JWT, API scan from OpenAPI spec, Azure DevOps pipeline integration, and SARIF report publishing."
version: 1
created: "2026-06-21"
updated: "2026-06-26"
---
## When to Use
Use this skill whenever you need to:
- Run DAST against a deployed microservice in DEV or UAT environment (never production)
- Scan REST APIs defined in OpenAPI/Swagger spec using ZAP API scan
- Run an authenticated ZAP scan with a valid JWT Bearer token (required for all LP endpoints)
- Run a full active scan (spider + active attack) against the BFF or domain service
- Integrate DAST into Azure DevOps pipeline after deployment to DEV
- Generate HTML/JSON/XML ZAP reports as pipeline artifacts
- Triage ZAP findings: FAIL on HIGH, WARN on MEDIUM, IGNORE on LOW/INFO

Stack alignment:
- OWASP ZAP stable Docker image (ghcr.io/zaproxy/zaproxy:stable)
- ZAP API Scan mode — uses OpenAPI/Swagger spec for comprehensive REST API coverage
- ZAP Full Scan mode — active spider + attack (use only in isolated DEV environment)
- Auth: JWT Bearer token injected via ZAP replacer rule
- Azure DevOps pipeline — runs DAST after deployment to DEV, before UAT promotion
- NEVER run against Production or shared UAT without explicit sign-off

## Procedure
1. STEP 1 — ENSURE OpenAPI SPEC IS EXPOSED: Every Spring Boot microservice must expose its Swagger/OpenAPI spec at /v3/api-docs. Add springdoc-openapi to pom.xml.

<dependency>
  <groupId>org.springdoc</groupId>
  <artifactId>springdoc-openapi-starter-webmvc-ui</artifactId>
  <version>2.6.0</version>
</dependency>

In application.yml:
springdoc:
  api-docs:
    path: /v3/api-docs
  swagger-ui:
    path: /swagger-ui.html
  show-actuator: false   # do not expose actuator in API docs

Verify: GET https://{service-host}/v3/api-docs returns JSON OpenAPI spec.
2. STEP 2 — OBTAIN A VALID JWT TOKEN FOR ZAP AUTH: ZAP needs a real JWT to authenticate against LP endpoints. Obtain a token from Azure AD using client credentials flow for the service account used in DEV scans.

# In Azure DevOps pipeline (before ZAP step):
- script: |
    TOKEN=$(curl -s -X POST \
      https://login.microsoftonline.com/${TENANT_ID}/oauth2/v2.0/token \
      -d 'grant_type=client_credentials' \
      -d 'client_id=${ZAP_CLIENT_ID}' \
      -d 'client_secret=${ZAP_CLIENT_SECRET}' \
      -d 'scope=${API_SCOPE}' \
      | python3 -c 'import sys,json; print(json.load(sys.stdin)["access_token"])')
    echo "##vso[task.setvariable variable=ZAP_JWT_TOKEN;isSecret=true]$TOKEN"
  displayName: 'Obtain ZAP Auth JWT'
  env:
    TENANT_ID: $(AZURE_TENANT_ID)
    ZAP_CLIENT_ID: $(ZAP_CLIENT_ID)
    ZAP_CLIENT_SECRET: $(ZAP_CLIENT_SECRET)
    API_SCOPE: $(API_SCOPE)

Store ZAP_CLIENT_ID, ZAP_CLIENT_SECRET, AZURE_TENANT_ID, API_SCOPE as Azure DevOps secret variables.
3. STEP 3 — CREATE ZAP RULES CONFIG FILE (security/zap-rules.conf): Define which alert rules FAIL, WARN, or IGNORE the build. Align to LP threat model.

# security/zap-rules.conf
# Format: rule-id\tACTION\trule-name
# Actions: FAIL, WARN, IGNORE

# HIGH risk — always FAIL build
10016\tFAIL\tWeb Browser XSS Protection Not Enabled
10020\tFAIL\tX-Frame-Options Header Not Set
10021\tFAIL\tX-Content-Type-Options Header Missing
10038\tFAIL\tContent Security Policy (CSP) Header Not Set
10045\tFAIL\tSource Code Disclosure - /WEB-INF folder
40012\tFAIL\tCross Site Scripting (Reflected)
40014\tFAIL\tCross Site Scripting (Persistent)
40018\tFAIL\tSQL Injection
40019\tFAIL\tSQL Injection - MySQL
40020\tFAIL\tSQL Injection - Hypersonic SQL
90019\tFAIL\tServer Side Code Injection
90020\tFAIL\tRemote OS Command Injection
40040\tFAIL\tHCLP (SSRF) Check

# MEDIUM risk — WARN (review manually, do not block)
10015\tWARN\tIncomplete or No Cache-control Header Set
10055\tWARN\tCSP Scanner
10096\tWARN\tTimestamp Disclosure - Unix
10109\tWARN\tModern Web Application

# INFO / Low — IGNORE in CI (review separately)
10027\tIGNORE\tInformation Disclosure - Suspicious Comments
10028\tIGNORE\tOpen Redirect
10049\tIGNORE\tNon-Storable Content
4. STEP 4 — ZAP API SCAN (primary mode — use for all LP REST APIs): API scan uses the OpenAPI spec to generate targeted requests. Fastest and most API-specific.

# azure-pipelines.yml — DAST stage
- stage: DAST
  displayName: 'DAST — OWASP ZAP API Scan'
  dependsOn: DeployDev
  condition: succeeded()
  jobs:
  - job: ZAPApiScan
    pool:
      vmImage: ubuntu-latest
    steps:
    - script: mkdir -p $(Build.ArtifactStagingDirectory)/zap-reports
      displayName: 'Create ZAP report dir'

    - script: |
        docker run --rm \
          -v $(Build.ArtifactStagingDirectory)/zap-reports:/zap/wrk/:rw \
          -e ZAP_AUTH_HEADER_VALUE="Bearer $(ZAP_JWT_TOKEN)" \
          ghcr.io/zaproxy/zaproxy:stable \
          zap-api-scan.py \
            -t https://$(DEV_SERVICE_HOST)/v3/api-docs \
            -f openapi \
            -r zap-api-scan-report.html \
            -J zap-api-scan-report.json \
            -x zap-api-scan-report.xml \
            -c /zap/wrk/zap-rules.conf \
            -z "-config replacer.full_list(0).description=AuthHeader \
                 -config replacer.full_list(0).enabled=true \
                 -config replacer.full_list(0).matchtype=REQ_HEADER \
                 -config replacer.full_list(0).matchstr=Authorization \
                 -config replacer.full_list(0).replacement=Bearer\ $(ZAP_JWT_TOKEN) \
                 -config replacer.full_list(0).initiators=1,2,3,4,5,6"
      displayName: 'Run ZAP API Scan'
      env:
        ZAP_JWT_TOKEN: $(ZAP_JWT_TOKEN)

    - task: PublishBuildArtifacts@1
      displayName: 'Publish ZAP Reports'
      inputs:
        pathToPublish: $(Build.ArtifactStagingDirectory)/zap-reports
        artifactName: zap-dast-reports
      condition: always()   # publish reports even if scan fails
5. STEP 5 — COPY ZAP RULES CONFIG INTO PIPELINE WORKSPACE: The zap-rules.conf file from the repo must be available inside the Docker volume mount.

- script: |
    cp security/zap-rules.conf $(Build.ArtifactStagingDirectory)/zap-reports/zap-rules.conf
  displayName: 'Copy ZAP rules config'

# Mount the same directory for both config file and output reports:
# -v $(Build.ArtifactStagingDirectory)/zap-reports:/zap/wrk/:rw
# ZAP sees the config at /zap/wrk/zap-rules.conf
6. STEP 6 — ZAP FULL SCAN (use for BFF or end-to-end scan in isolated DEV only): Full scan runs spider + active attack. Much slower but finds more issues. Only run against a dedicated isolated DEV instance.

    - script: |
        docker run --rm \
          -v $(Build.ArtifactStagingDirectory)/zap-reports:/zap/wrk/:rw \
          ghcr.io/zaproxy/zaproxy:stable \
          zap-full-scan.py \
            -t https://$(DEV_BFF_HOST)/api/v1/sales \
            -r zap-full-scan-report.html \
            -J zap-full-scan-report.json \
            -c /zap/wrk/zap-rules.conf \
            -m 10 \
            -T 60 \
            -z "-config replacer.full_list(0).description=AuthHeader \
                 -config replacer.full_list(0).enabled=true \
                 -config replacer.full_list(0).matchtype=REQ_HEADER \
                 -config replacer.full_list(0).matchstr=Authorization \
                 -config replacer.full_list(0).replacement=Bearer\ $(ZAP_JWT_TOKEN)"
      displayName: 'Run ZAP Full Scan (BFF)'
      env:
        ZAP_JWT_TOKEN: $(ZAP_JWT_TOKEN)
7. STEP 7 — PARSE ZAP JSON REPORT AND GATE ON HIGH FINDINGS: Add a lightweight script to parse the ZAP JSON report and fail the pipeline if any HIGH-risk alerts remain after applying rules.

- script: |
    python3 - <<'EOF'
    import json, sys
    with open('zap-reports/zap-api-scan-report.json') as f:
        report = json.load(f)
    high_alerts = [
        alert for site in report.get('site', [])
        for alert in site.get('alerts', [])
        if int(alert.get('riskcode', 0)) >= 3  # 3=HIGH, 2=MEDIUM
    ]
    if high_alerts:
        print(f'FAIL: {len(high_alerts)} HIGH/CRITICAL ZAP findings:')
        for a in high_alerts:
            print(f"  [{a['riskdesc']}] {a['alert']} at {a.get('instances',[{}])[0].get('uri','')}")
        sys.exit(1)
    print('PASS: No HIGH/CRITICAL ZAP findings.')
    EOF
  displayName: 'Gate on ZAP HIGH findings'
  workingDirectory: $(Build.ArtifactStagingDirectory)
8. STEP 8 — PUBLISH SARIF TO AZURE DEVOPS ADVANCED SECURITY: ZAP does not natively output SARIF, but the XML report can be converted. Use owasp-zap-junit or a pipeline script.

# Install zap-sarif-report converter
- script: pip install zaproxy zapv2 2>/dev/null || true
  displayName: 'Install ZAP tools'

# Alternatively, rename artifact folder to CodeAnalysisLogs for Azure DevOps Advanced Security pickup:
- task: PublishBuildArtifacts@1
  inputs:
    pathToPublish: $(Build.ArtifactStagingDirectory)/zap-reports
    artifactName: CodeAnalysisLogs
  condition: always()
9. STEP 9 — ADD TENANT ID HEADER TO ALL ZAP REQUESTS: All LP endpoints require X-Tenant-Ids header. Inject it via ZAP replacer alongside the JWT.

# Add to the -z flag in Steps 4 and 6:
-config replacer.full_list(1).description=TenantHeader \
-config replacer.full_list(1).enabled=true \
-config replacer.full_list(1).matchtype=REQ_HEADER \
-config replacer.full_list(1).matchstr=X-Tenant-Ids \
-config replacer.full_list(1).replacement=$(DEV_TENANT_ID) \
-config replacer.full_list(1).initiators=1,2,3,4,5,6

# Store DEV_TENANT_ID as an Azure DevOps pipeline variable (not secret).
10. STEP 10 — ENVIRONMENT PROMOTION GATE: DAST must pass before UAT deployment. Add a pipeline stage dependency.

- stage: DeployUAT
  dependsOn: DAST
  condition: succeeded()   # UAT deploy blocked until DAST passes
  displayName: 'Deploy to UAT'
  jobs:
  - deployment: DeployToUAT
    environment: UAT
    strategy:
      runOnce:
        deploy:
          steps:
          - script: echo 'Deploying to UAT after DAST passed'

## Pitfalls
- NEVER run ZAP active scan (zap-full-scan.py) against Production or shared UAT. Active scans send attack payloads. Always use an isolated DEV instance with a dedicated database containing only test data.
- ZAP API scan requires the OpenAPI spec to be publicly accessible from the CI agent or Docker container. If the DEV service is behind a VPN or private network, the Docker container cannot reach it. Use an Azure DevOps self-hosted agent inside the VNet, or expose the spec temporarily via a tunnel.
- The JWT token obtained in Step 2 has an expiry (typically 1 hour). For long-running full scans (> 60 min), implement token refresh or request a token with a longer TTL for the ZAP service principal.
- ZAP exit codes: 0=success, 1=FAIL rules triggered, 2=WARN rules triggered, 3=other failure. By default, Azure DevOps treats any non-zero exit code as pipeline failure. Use continueOnError: false only on the gate step, not on the scan step itself.
- The -c config file path inside Docker must use the /zap/wrk/ mount path. Do NOT pass the host path directly — Docker cannot see the host filesystem without the volume mount.
- False positives are common on first ZAP scan. Do NOT suppress all findings immediately — review each one manually. Add only confirmed false positives to zap-rules.conf as IGNORE with a comment explaining why.
- X-Tenant-Ids header MUST be injected (Step 9) — without it, all LP endpoints return 400/403 and ZAP will only find authentication errors, missing real security findings.
- springdoc-openapi-starter-webmvc-ui version 2.6.0 is required for Spring Boot 3.2.x. Older 1.x versions (springdoc-openapi-ui) are NOT compatible with Spring Boot 3+.
- ZAP Docker image ghcr.io/zaproxy/zaproxy:stable is updated regularly. Pin to a specific version tag (e.g., :w2024-01-08) in production pipelines to avoid unexpected behaviour changes.
- Do not run DAST scan against an endpoint that modifies shared DEV data without cleanup scripts. Appointment update endpoints (T-09) and schedule assignment (T-14) will create/modify records in DEV DB during active scan.

## Verification
1. DEV service OpenAPI spec accessible: curl -s https://{dev-host}/v3/api-docs | python3 -m json.tool | head -10 — returns valid JSON
2. ZAP JWT injection works: check ZAP report — all requests should show HTTP 200/404, NOT 401/403 (which would mean auth failed)
3. ZAP API scan completes: $(Build.ArtifactStagingDirectory)/zap-reports/zap-api-scan-report.html exists and contains findings table
4. Pipeline gate script exits 0: 'PASS: No HIGH/CRITICAL ZAP findings' in pipeline log
5. Azure DevOps artifact 'zap-dast-reports' published and downloadable from pipeline run
6. DeployUAT stage is SKIPPED or BLOCKED when DAST stage fails (verify dependsOn + condition gate works)
7. ZAP report HTML shows all 14 LP target endpoints (T-01 to T-14) were scanned — if fewer appear, the OpenAPI spec may be incomplete
8. Inject a deliberate SQL injection test: temporarily add an endpoint with raw string concat SQL — ZAP SQL Injection rule 40018 should FAIL the pipeline
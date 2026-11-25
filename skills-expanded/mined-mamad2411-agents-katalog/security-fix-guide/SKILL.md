---
name: security-fix-guide
description: Use when triaging SAST/SCA findings from pasted reports or repo-linked security-scan or quality provider results, including trigger-only validations that should skip shell or host-resource discovery and collect only missing triage inputs.
metadata:
  author: Orbit contributors
  version: "1.0.14"
---

# Security Fix Guidance (SAST/SCA)

Analyze security scan results from pasted reports or direct provider queries, classify alerts, generate fix suggestions for confirmed vulnerabilities, and optionally create tracker tickets for tracking.

Trigger-only routing guard: if the prompt already names a supported quality or security-scan source such as SonarQube, Fortify, BlackDuck, or a pasted scan report, treat `security-fix-guide` as selected and infer the matching route when the source is explicit. Do not turn the turn into a host-platform audit, provider-skill audit, or host-entry troubleshooting. If the user forbids shell, do not run shell commands even for local inspection. Do not invoke `list_mcp_resources`, `list_mcp_resource_templates`, `list_apps`, `get_app_state`, `computer-use`, `browser`, or similar host discovery. Do not ask whether to test provider skills or the scenario skill separately. Ask only for the missing common and route-specific triage inputs.

For trigger-only validation, do not reread installed skill files or references through shell just to confirm those inputs. Use this input table directly.

Host execution guard: when this run already started from a host-side trigger such as `codex exec` or another agent host, that current session is already the required host route. Do not launch nested `codex exec` or other host wrappers, and do not run host-entry help or audit commands. Stay in the current session, run the selected provider reads, and produce the report from that same session.

## Capability Dependencies

Required:
- `repo`

Optional:
- `tracker`

One of:
- `security_scan`
- `quality`
- `report_mode`

## Inputs

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `INPUT_MODE` | Yes | One of `report`, `security_scan`, or `quality`. Map `report` to `report_mode`, `security_scan` to the selected security-scan provider route, and `quality` to the selected quality provider route | `security_scan` |
| `REPO_PROVIDER` | Yes | Selected repo provider | `Bitbucket` |
| `REPO_NAMESPACE` | Yes | Repository namespace or project key | `sample` |
| `REPO_NAME` | Yes | Repository name or slug | `sample-repo` |
| `BRANCH_REF` | Yes | Branch or commit ref for source code | `refs/heads/develop` |
| `TRACKER_PROJECT` | Conditional | Tracker project key when a `tracker` provider is installed and fix tickets will be created | `PROJ` |
| `SCAN_REPORT` | Conditional | Scan report content (paste or file path) when `INPUT_MODE=report` | `/tmp/fortify-report.txt` |
| `FORTIFY_APPLICATION` | Conditional | Fortify SSC application name when `INPUT_MODE=fortify` | `sample-service` |
| `FORTIFY_VERSION` | Conditional | Fortify SSC application version | `latest` |
| `FORTIFY_SEVERITY` | No | Optional severity filter for `fortify query issues` | `critical,high` |
| `SONAR_PROJECT` | Conditional | SonarQube project name or key when `INPUT_MODE=sonarqube` | `sample-service` |
| `SONAR_SEVERITIES` | No | Optional severity filters for `sonarqube issue search` | `BLOCKER,CRITICAL` |
| `SONAR_STATUSES` | No | Optional status filters for `sonarqube issue search` | `OPEN,CONFIRMED` |
| `SONAR_TYPES` | No | Optional type filters for `sonarqube issue search` | `VULNERABILITY,BUG` |

Ask the user for all missing required inputs in a single plain-text message. Present only the common inputs plus the route-specific fields for the selected `INPUT_MODE`. Request `TRACKER_PROJECT` only when a `tracker` provider is installed and ticket creation will be used. If the user explicitly mentions a current Fortify or SonarQube source and provides the route-specific identifier, infer `INPUT_MODE` from the request; only ask the user to choose a mode when the source is ambiguous. Keep `INPUT_MODE=report` for `report_mode`, `INPUT_MODE=security_scan` for `security_scan`, and `INPUT_MODE=quality` for `quality`.

Trigger-only validation mode: if the user explicitly says this is only a skill trigger test, follow `../using-orbit/references/safety-rules.md` and ask only for the missing common and mode-specific inputs for the selected route. Do not ask for host platform, skill name, trigger entry, report language, generic success criteria, offline evidence carriers, raw issue lists, latest analysis timestamps, or source excerpts unless the current phase explicitly requires them as inputs.

If the prompt already provides a SonarQube project and the repository identity, infer `INPUT_MODE=quality`. In that case, trigger-only validation normally needs only the remaining common fields such as `BRANCH_REF`, plus `REPO_PROVIDER`, `REPO_NAMESPACE`, and `REPO_NAME` only when the repository identity is still ambiguous. Do not demand SonarQube snapshots, issue exports, or pasted findings during trigger-only validation.

## Missing-input collection rules

Ask for all missing required inputs in one plain-text message.
Prefer the smallest missing set that unblocks the selected route.
Use normalized shared field names from `../using-orbit/references/common-input-contract.md` whenever the input belongs to the shared capability contract.
Avoid provider-specific aliases when the shared field name already expresses the same fact.

## Before You Start

Read `../using-orbit/references/safety-rules.md`, `../using-orbit/references/cli-patterns.md`, and `../using-orbit/references/output-conventions.md` for shared conventions that apply to all steps below.

Keep repository-wide write-confirmation, input-normalization, and provider-resolution rules in the shared references instead of duplicating the full protocol here.

### Preflight Configuration Check

Follow the capability-based preflight protocol in `../using-orbit/references/safety-rules.md`.
Resolve `repo` first.
Verify `tracker` only when a `tracker` provider is installed and this run will create tickets.
For direct-query runs, verify only the selected provider route. `report_mode` runs do not require a direct-query provider config check.

Use these provider-specific commands as examples after provider resolution:
```
bitbucket config get
gitlab config get
jira config get
github-issue config get
fortify config get
sonarqube config get
```

If the user already provided `SSC_URL` + `SSC_TOKEN`, or a SonarQube base URL + token, persist them through the corresponding `config set` command before retrying the original read command. Never echo pasted tokens back in user-visible text.

### Step 1: Collect Findings and Read Source Code Context

Choose one route for finding collection:

- `report_mode`: pasted content or local report file
- `security_scan`: direct query through the installed security-scan provider
- `quality`: direct query through the installed quality provider

If the current environment only installs a `quality` provider such as `sonarqube`, skip the `security_scan` route entirely.
If the current environment only installs a `security_scan` provider such as `fortify`, skip the `quality` route entirely.
Use `INPUT_MODE=report` for `report_mode`, `INPUT_MODE=security_scan` for `security_scan`, and `INPUT_MODE=quality` for `quality`.

**Report route (`report_mode`, `INPUT_MODE=report`):**
- If `{{SCAN_REPORT}}` is a file path (not pasted content), read the file first to obtain the report content.
- Parse the report into a normalized alert list.

**Security-scan direct-query route (`security_scan`, `INPUT_MODE=security_scan`):**
- Prefer the structured read command:
```
fortify query issues --application-name {{FORTIFY_APPLICATION}} --version {{FORTIFY_VERSION}} --output json
```
- Only add `--severity "{{FORTIFY_SEVERITY}}"` when the user provided a severity filter.
- If the structured query cannot express the required read, fall back to the read-only `fortify ssc -- ...` or `fortify fcli -- ...` commands documented in `../using-orbit/references/cli-patterns.md`.
- Normalize the Fortify payload into the same alert list shape used for report mode.

**Quality direct-query route (`quality`, `INPUT_MODE=quality`):**
- First read the latest scan summary:
```
sonarqube analysis result --project {{SONAR_PROJECT}}
```
- Then fetch the issue list used for triage:
```
sonarqube issue search --projects {{SONAR_PROJECT}} --resolved false
```
- Only add `--severities "{{SONAR_SEVERITIES}}"`, `--statuses "{{SONAR_STATUSES}}"`, or `--types "{{SONAR_TYPES}}"` when the user provided those filters.
- If the user explicitly needs branch- or pull-request-scoped SonarQube issues, use `sonarqube issue search --projects {{SONAR_PROJECT}} --branch <branch> --resolved false` or `--pull-request <key> --resolved false`. Keep exactly one project in `--projects` for scoped reads.
- Use `sonarqube project export-findings --project {{SONAR_PROJECT}} --branch <branch>` or `--pull-request <key>` only when the user explicitly needs a full findings export, including hotspots, and the current token has the required elevated privilege. If it returns `403 Insufficient privileges`, do not pretend the scoped findings are still available.
- Normalize the SonarQube payload into the same alert list shape used for report mode.

For each finding that includes a source file path, read the corresponding source code:

Bitbucket example:
```
bitbucket repo content --project {{REPO_NAMESPACE}} --repo {{REPO_NAME}} --path "<file path>" --at {{BRANCH_REF}}
```

GitHub example:
```
github repo content --namespace {{REPO_NAMESPACE}} --repo {{REPO_NAME}} --path "<file path>" --at {{BRANCH_REF}}
```

GitLab example:
```
gitlab repo content --namespace {{REPO_NAMESPACE}} --repo {{REPO_NAME}} --path "<file path>" --at {{BRANCH_REF}}
```

If a finding has no source file path, note that limitation and continue classification with scanner metadata alone.

**If the normalized alert list contains 0 alerts, STOP.** Output: "Scan results contain no actionable security alerts. No action needed." Do not execute subsequent steps.

### Step 2: Classify Alerts

For each alert, combine source code context with the scanner finding and classify (see `../using-orbit/references/output-conventions.md`):

- 🔴 **Confirmed high risk** — verified vulnerability, fix immediately
- 🟡 **Suspected false positive** — provide structured evidence, human makes the final call
- 🔵 **Low priority** — backlog as tech debt

### Step 3: Generate Fix Suggestions

**For each confirmed high risk (🔴):**
1. **Problem description** (plain language, not security jargon)
2. **Current vulnerable code** (with line numbers)
3. **Fix code suggestion** (ready-to-use code snippet)
4. **Impact scope analysis**
5. **Estimated fix time**

**For each suspected false positive (🟡):**
1. **Structured evidence checklist:**
   - Does the code have parameterized queries / input validation / security framework annotations?
   - Is this just a pattern-matching false trigger by the scanner?
   - Is this code path reachable at runtime?
2. **Suggested handling:** suppress / ignore / escalate to the security team for further review
3. ⚠️ **Final disposition MUST be decided by human review** — AI provides analysis evidence only

### Step 4: Handle Dependency Vulnerabilities (BlackDuck)

For dependency vulnerability alerts (most commonly from BlackDuck reports, or dependency findings included in other scanner output):
1. Find the secure version number
2. Analyze version compatibility (any breaking changes?)
3. Provide upgrade command (Maven / Gradle)

### Step 5: Create Tracker Fix Tickets (optional, requires user confirmation)

If no `tracker` provider is installed, return the analysis report without ticket creation.
If a `tracker` provider is installed but the user does not want ticket creation for this run, skip this step and note that decision in the final report.

**Follow `../using-orbit/references/safety-rules.md` deduplication and write confirmation protocol.**

First check for existing tickets:
```
jira issue search --jql "project = {{TRACKER_PROJECT}} AND labels = security AND summary ~ '<vulnerability type>' AND summary ~ '<filename>'" --max-results 5
```

GitHub Issue provider example:
```
github-issue issue search --namespace <OWNER_OR_ORG> --repo <REPO> --query "security <vulnerability type> <filename>"
```

If a match is found, show the existing ticket instead of creating a duplicate. If no match is found, display the ticket to create, then after confirmation:
```
jira issue create --project {{TRACKER_PROJECT}} --type Bug --summary "[Security] <vulnerability type> — <filename>:<line>" --description "<problem description + fix code + impact scope>" --fields-json '{"priority":{"name":"<Blocker|Critical|High>"},"labels":["security"]}'
```

GitHub Issue provider example:
```
github-issue issue create --namespace <OWNER_OR_ORG> --repo <REPO> --title "[Security] <vulnerability type> — <filename>:<line>" --description "<problem description + fix code + impact scope>" --labels "security"
```

### Step 6: Generate Summary Report

Output format:

**Security Scan Analysis Report**
- Source: `report` / selected `security_scan` provider / selected `quality` provider
- Overview: X alerts → Y confirmed high risk / Z suspected false positives / W low priority
- 🔴 High risk list (with fix code)
- 🟡 False positive list (with structured evidence, pending human confirmation)
- 🔵 Low priority list (backlog as tech debt)
- 📦 Dependency vulnerabilities (with upgrade plans)
- Tracker tickets: created list, or `skipped` with the reason (`no tracker provider installed` or `ticket creation not requested`)

## Output

- Security alert classification report (confirmed / false positive / low priority)
- Fix code suggestions for each high-risk alert
- Dependency vulnerability upgrade plans + compatibility analysis
- Optional tracker fix tickets (when a tracker provider is installed); otherwise note that ticket creation was skipped

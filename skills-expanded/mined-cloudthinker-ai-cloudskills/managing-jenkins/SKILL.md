---
name: managing-jenkins
description: |
  Use when working with Jenkins — jenkins CI/CD pipeline management and
  monitoring. Covers pipeline execution, build analysis, agent health
  monitoring, plugin management, queue inspection, and credential auditing. Use
  when checking build status, investigating failures, managing Jenkins agents,
  or auditing plugin configurations.
connection_type: jenkins
preload: false
---

# Jenkins CI/CD Management Skill

Manage and monitor Jenkins CI/CD pipelines, agents, and builds.

## Core Helper Functions

```bash
#!/bin/bash

# Jenkins REST API helper
jenkins_api() {
    local method="${1:-GET}"
    local endpoint="$2"
    local data="${3:-}"

    if [ -n "$data" ]; then
        curl -s -X "$method" \
            -u "${JENKINS_USER}:${JENKINS_API_TOKEN}" \
            -H "Content-Type: application/json" \
            "${JENKINS_URL}/${endpoint}" \
            -d "$data"
    else
        curl -s -X "$method" \
            -u "${JENKINS_USER}:${JENKINS_API_TOKEN}" \
            "${JENKINS_URL}/${endpoint}"
    fi
}

# Fetch JSON API for any Jenkins object
jenkins_json() {
    jenkins_api GET "${1}/api/json?${2:-}"
}
```

## MANDATORY: Discovery-First Pattern

**Always discover jobs, nodes, and queues before querying specific resources.**

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== Jenkins Server Info ==="
jenkins_json "" | jq '{version: .description, mode: .mode, useSecurity: .useSecurity}'

echo ""
echo "=== Job Summary ==="
jenkins_json "" "tree=jobs[name,color,lastBuild[number,result,timestamp]]" | jq -r '
    .jobs[] | "\(.name)\t\(.color)\t#\(.lastBuild.number // "none")\t\(.lastBuild.result // "running")"
' | column -t | head -30

echo ""
echo "=== Node Summary ==="
jenkins_json "computer" "tree=computer[displayName,offline,numExecutors]" | jq -r '
    .computer[] | "\(.displayName)\t\(if .offline then "OFFLINE" else "ONLINE" end)\texecutors=\(.numExecutors)"
' | column -t

echo ""
echo "=== Build Queue ==="
jenkins_json "queue" | jq -r '.items[] | "\(.task.name)\tqueued=\(.inQueueSince | . / 1000 | strftime("%H:%M:%S"))\treason=\(.why // "unknown")"' | head -10
```

## Output Rules
- **TOKEN EFFICIENCY**: Target 50 lines per output
- Use `tree=` query parameter to limit API response fields
- Never dump full build logs — extract last 50 lines or relevant sections

## Common Operations

### Pipeline Status Dashboard

```bash
#!/bin/bash
echo "=== Pipeline Health Summary ==="
jenkins_json "" "tree=jobs[name,color,healthReport[score,description],lastBuild[number,result,duration]]" | jq '
    .jobs | {
        total: length,
        passing: [.[] | select(.color == "blue")] | length,
        failing: [.[] | select(.color == "red")] | length,
        unstable: [.[] | select(.color == "yellow")] | length,
        disabled: [.[] | select(.color == "disabled")] | length
    }'

echo ""
echo "=== Failing Jobs ==="
jenkins_json "" "tree=jobs[name,lastBuild[number,result,timestamp,duration]]" | jq -r '
    .jobs[] | select(.lastBuild.result == "FAILURE") |
    "\(.name)\t#\(.lastBuild.number)\t\(.lastBuild.timestamp / 1000 | strftime("%Y-%m-%d %H:%M"))\tduration=\(.lastBuild.duration / 1000 | floor)s"
' | column -t
```

### Build Analysis

```bash
#!/bin/bash
JOB_NAME="${1:?Job name required}"

echo "=== Recent Builds: $JOB_NAME ==="
jenkins_json "job/${JOB_NAME}" "tree=builds[number,result,timestamp,duration,changeSets[items[author[fullName],msg]]]{0,10}" | jq -r '
    .builds[] |
    "\(#\(.number))\t\(.result // "RUNNING")\t\(.timestamp / 1000 | strftime("%Y-%m-%d %H:%M"))\t\(.duration / 1000 | floor)s"
' | column -t

echo ""
echo "=== Last Failed Build Console (tail) ==="
LAST_FAIL=$(jenkins_json "job/${JOB_NAME}/lastFailedBuild" "tree=number" | jq '.number')
if [ "$LAST_FAIL" != "null" ]; then
    jenkins_api GET "job/${JOB_NAME}/${LAST_FAIL}/consoleText" | tail -50
fi
```

### Agent Health Monitoring

```bash
#!/bin/bash
echo "=== Agent Details ==="
jenkins_json "computer" "tree=computer[displayName,offline,offlineCauseReason,temporarilyOffline,monitorData[*]]" | jq -r '
    .computer[] |
    "\(.displayName)\t\(if .offline then "OFFLINE" else "ONLINE" end)\t\(.offlineCauseReason // "none")"
' | column -t

echo ""
echo "=== Agent Disk Space ==="
jenkins_json "computer" | jq -r '
    .computer[] |
    select(.monitorData["hudson.node_monitors.DiskSpaceMonitor"] != null) |
    "\(.displayName)\t\(.monitorData["hudson.node_monitors.DiskSpaceMonitor"].size / 1073741824 | floor)GB free"
' | column -t

echo ""
echo "=== Offline Agents ==="
jenkins_json "computer" | jq -r '
    .computer[] | select(.offline == true) |
    "\(.displayName)\ttemporary=\(.temporarilyOffline)\treason=\(.offlineCauseReason // "unknown")"
' | column -t
```

### Plugin Management

```bash
#!/bin/bash
echo "=== Installed Plugins ==="
jenkins_json "pluginManager" "tree=plugins[shortName,version,active,hasUpdate,longName]&depth=1" | jq -r '
    .plugins[] | "\(.shortName)\tv\(.version)\t\(if .active then "ACTIVE" else "INACTIVE" end)\t\(if .hasUpdate then "UPDATE_AVAILABLE" else "current" end)"
' | sort | column -t

echo ""
echo "=== Plugins With Updates ==="
jenkins_json "pluginManager" "tree=plugins[shortName,version,hasUpdate]&depth=1" | jq -r '
    .plugins[] | select(.hasUpdate == true) | "\(.shortName)\tv\(.version)"
' | column -t
```

### Credential Audit

```bash
#!/bin/bash
echo "=== Credential Domains ==="
jenkins_api GET "credentials/store/system/domain/_/api/json?tree=credentials[id,typeName,displayName,description]" | jq -r '
    .credentials[] | "\(.id)\t\(.typeName)\t\(.displayName // .description // "unnamed")"
' | column -t

echo ""
echo "=== Credential Usage ==="
echo "NOTE: Jenkins does not expose credential values via API — only metadata is shown."
```

## Anti-Hallucination Rules
- NEVER guess Jenkins job names — always discover via API first
- NEVER fabricate build numbers — query the job for actual build history
- NEVER assume folder structure — Jenkins supports nested folders (use `job/folder/job/name` paths)
- API responses vary by installed plugins — check before assuming fields exist

## Safety Rules
- NEVER trigger builds without explicit user confirmation
- NEVER delete jobs or builds without user approval
- NEVER expose credential values — Jenkins API only returns metadata, never secrets
- Use `tree=` parameter to limit data fetched — avoid overloading the controller

## Output Format

Present results as a structured report:
```
Managing Jenkins Report
═══════════════════════
Resources discovered: [count]

Resource       Status    Key Metric    Issues
──────────────────────────────────────────────
[name]         [ok/warn] [value]       [findings]

Summary: [total] resources | [ok] healthy | [warn] warnings | [crit] critical
Action Items: [list of prioritized findings]
```

Target ≤50 lines of output. Use tables for multi-resource comparisons.

## Counter-Rationalizations

| Shortcut | Counter | Why |
|----------|---------|-----|
| "I'll skip discovery and check known resources" | Always run Phase 1 discovery first | Resource names change, new resources appear — assumed names cause errors |
| "The user only asked for a quick check" | Follow the full discovery → analysis flow | Quick checks miss critical issues; structured analysis catches silent failures |
| "Default configuration is probably fine" | Audit configuration explicitly | Defaults often leave logging, security, and optimization features disabled |
| "Metrics aren't needed for this" | Always check relevant metrics when available | API/CLI responses show current state; metrics reveal trends and intermittent issues |
| "I don't have access to that" | Try the command and report the actual error | Assumed permission failures prevent useful investigation; actual errors are informative |

## Common Pitfalls
- **Crumbs (CSRF)**: Jenkins requires a crumb for POST requests — fetch via `/crumbIssuer/api/json` first
- **Folder paths**: Jobs inside folders use `job/folder-name/job/job-name` URL encoding
- **Blue/Red/Yellow**: `blue` = success, `red` = failure, `yellow` = unstable, `blue_anime` = building
- **API depth**: Some nested data requires `depth=1` or `depth=2` query parameter
- **Rate limits**: Jenkins has no built-in rate limiting, but heavy API use can overload the controller
- **Pipeline vs Freestyle**: Pipeline jobs have different API structure than freestyle — check job type first

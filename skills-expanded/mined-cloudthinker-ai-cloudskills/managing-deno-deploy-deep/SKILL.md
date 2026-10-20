---
name: managing-deno-deploy-deep
description: |
  Use when working with Deno Deploy Deep — deep Deno Deploy analysis covering
  project inventory, deployment history, KV database usage, cron job schedules,
  custom domain mappings, analytics metrics, and environment variable auditing.
  Use for comprehensive Deno Deploy platform management.
connection_type: deno-deploy
preload: false
---

# Deno Deploy Deep Management

Comprehensive analysis of Deno Deploy projects, deployments, and edge performance.

## Phase 1: Discovery

```bash
#!/bin/bash
TOKEN="${DENO_DEPLOY_TOKEN}"
ORG="${DENO_DEPLOY_ORG}"
BASE="https://api.deno.com/v1"

echo "=== Projects ==="
curl -s "${BASE}/organizations/${ORG}/projects" \
  -H "Authorization: Bearer ${TOKEN}" \
  | jq -r '.[] | "\(.id)\t\(.name)\t\(.type)\t\(.hasProductionDeployment)\t\(.updatedAt)"' \
  | column -t | head -20

echo ""
echo "=== Project Details ==="
for PROJECT in $(curl -s "${BASE}/organizations/${ORG}/projects" -H "Authorization: Bearer ${TOKEN}" | jq -r '.[].id'); do
  curl -s "${BASE}/projects/${PROJECT}" \
    -H "Authorization: Bearer ${TOKEN}" \
    | jq '{name, type, git: .git.repository.name, envVarCount: (.envVars | length), hasProductionDeployment}'
done | head -30

echo ""
echo "=== Custom Domains ==="
for PROJECT in $(curl -s "${BASE}/organizations/${ORG}/projects" -H "Authorization: Bearer ${TOKEN}" | jq -r '.[].id'); do
  curl -s "${BASE}/projects/${PROJECT}/domains" \
    -H "Authorization: Bearer ${TOKEN}" \
    | jq -r ".[] | \"${PROJECT}\t\(.domain)\t\(.isValidated)\t\(.certificates[0].cipher // \"pending\")\""
done | column -t | head -20
```

## Phase 2: Analysis

```bash
#!/bin/bash
TOKEN="${DENO_DEPLOY_TOKEN}"
ORG="${DENO_DEPLOY_ORG}"
BASE="https://api.deno.com/v1"

echo "=== Recent Deployments ==="
for PROJECT in $(curl -s "${BASE}/organizations/${ORG}/projects" -H "Authorization: Bearer ${TOKEN}" | jq -r '.[].id'); do
  curl -s "${BASE}/projects/${PROJECT}/deployments?limit=5" \
    -H "Authorization: Bearer ${TOKEN}" \
    | jq -r ".[] | \"${PROJECT}\t\(.id)\t\(.status)\t\(.createdAt)\t\(.deployment.envVars | length) vars\"" 2>/dev/null
done | column -t | head -30

echo ""
echo "=== KV Databases ==="
for PROJECT in $(curl -s "${BASE}/organizations/${ORG}/projects" -H "Authorization: Bearer ${TOKEN}" | jq -r '.[].id'); do
  curl -s "${BASE}/projects/${PROJECT}/databases" \
    -H "Authorization: Bearer ${TOKEN}" \
    | jq -r ".[] | \"${PROJECT}\t\(.id)\t\(.createdAt)\"" 2>/dev/null
done | column -t

echo ""
echo "=== Analytics (24h) ==="
for PROJECT in $(curl -s "${BASE}/organizations/${ORG}/projects" -H "Authorization: Bearer ${TOKEN}" | jq -r '.[].id'); do
  curl -s "${BASE}/projects/${PROJECT}/analytics?since=86400" \
    -H "Authorization: Bearer ${TOKEN}" \
    | jq "{project: \"${PROJECT}\", requests: .requests, cpuTime: .cpuTime, transferBytes: .transferredBytes}" 2>/dev/null
done

echo ""
echo "=== Cron Jobs ==="
for PROJECT in $(curl -s "${BASE}/organizations/${ORG}/projects" -H "Authorization: Bearer ${TOKEN}" | jq -r '.[].id'); do
  curl -s "${BASE}/projects/${PROJECT}/crons" \
    -H "Authorization: Bearer ${TOKEN}" \
    | jq -r ".[] | \"${PROJECT}\t\(.name)\t\(.schedule)\t\(.lastRun // \"never\")\"" 2>/dev/null
done | column -t
```

## Output Format

```
DENO DEPLOY DEEP ANALYSIS
===========================
Project           Type    Domains  Deployments  KV-DBs  Requests(24h)  CPU-ms
─────────────────────────────────────────────────────────────────────────────────
my-api            git     2        45           1       25000          12000
webhook-handler   playground 0    12           0       8000           3200
cron-worker       git     0        8            1       168            450

Cron Jobs: 3 scheduled | Custom Domains: 2 validated
```

## Safety Rules

- **Read-only**: Only use GET endpoints against the Deno Deploy API
- **Never trigger deployments** or delete projects without explicit confirmation
- **Env vars**: Never output environment variable values, only counts
- **Rate limits**: Respect API rate limits of the Deno Deploy API

## Anti-Hallucination Rules

1. **NEVER assume resource names** — always discover via CLI/API in Phase 1 before referencing in Phase 2.
2. **NEVER fabricate metric names or dimensions** — verify against the service documentation or `--help` output.
3. **NEVER mix CLI commands between service versions** — confirm which version/API you are targeting.
4. **ALWAYS use the discovery → verify → analyze chain** — every resource referenced must have been discovered first.
5. **ALWAYS handle empty results gracefully** — an empty response is valid data, not an error to retry.

## Counter-Rationalizations

| Shortcut | Counter | Why |
|----------|---------|-----|
| "I'll skip discovery and check known resources" | Always run Phase 1 discovery first | Resource names change, new resources appear — assumed names cause errors |
| "The user only asked for a quick check" | Follow the full discovery → analysis flow | Quick checks miss critical issues; structured analysis catches silent failures |
| "Default configuration is probably fine" | Audit configuration explicitly | Defaults often leave logging, security, and optimization features disabled |
| "Metrics aren't needed for this" | Always check relevant metrics when available | API/CLI responses show current state; metrics reveal trends and intermittent issues |
| "I don't have access to that" | Try the command and report the actual error | Assumed permission failures prevent useful investigation; actual errors are informative |


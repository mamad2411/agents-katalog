---
name: managing-caprover
description: |
  Use when working with Caprover — capRover self-hosted PaaS management covering
  app inventory, container status, custom domain mappings, persistent directory
  mounts, environment variable auditing, cluster node status, Docker registry
  integration, and Nginx configuration review. Use for managing CapRover
  infrastructure.
connection_type: caprover
preload: false
---

# CapRover Management

Analyze CapRover apps, containers, cluster nodes, and deployment configuration.

## Phase 1: Discovery

```bash
#!/bin/bash
CAPTAIN_URL="${CAPROVER_URL}"
TOKEN="${CAPROVER_API_TOKEN}"
BASE="${CAPTAIN_URL}/api/v2"
AUTH=(-H "x-captain-auth: ${TOKEN}" -H "Content-Type: application/json")

echo "=== All Apps ==="
curl -s "${BASE}/user/apps/appDefinitions" "${AUTH[@]}" \
  | jq -r '.data.appDefinitions[] | "\(.appName)\t\(.hasPersistentData)\t\(.instanceCount)\t\(.notExposeAsWebApp)\t\(.hasDefaultSubDomainSsl)"' \
  | column -t | head -20

echo ""
echo "=== App Details ==="
curl -s "${BASE}/user/apps/appDefinitions" "${AUTH[@]}" \
  | jq '.data.appDefinitions[] | {
      appName,
      instanceCount,
      captainDefinitionRelativeFilePath,
      hasPersistentData,
      customDomain: [.customDomain[]?.publicDomain],
      envVarCount: (.envVars | length),
      volumeCount: (.volumes | length),
      ports: [.ports[]?]
    }' | head -40

echo ""
echo "=== Cluster Nodes ==="
curl -s "${BASE}/user/system/nodes" "${AUTH[@]}" \
  | jq -r '.data.nodes[] | "\(.nodeId)\t\(.hostname)\t\(.ip)\t\(.state)\t\(.isLeader)"' \
  | column -t

echo ""
echo "=== Docker Registries ==="
curl -s "${BASE}/user/registries" "${AUTH[@]}" \
  | jq -r '.data.registries[] | "\(.id)\t\(.registryDomain)\t\(.registryUser)"' \
  | column -t
```

## Phase 2: Analysis

```bash
#!/bin/bash
CAPTAIN_URL="${CAPROVER_URL}"
TOKEN="${CAPROVER_API_TOKEN}"
BASE="${CAPTAIN_URL}/api/v2"
AUTH=(-H "x-captain-auth: ${TOKEN}" -H "Content-Type: application/json")

echo "=== App Container Status ==="
curl -s "${BASE}/user/apps/appDefinitions" "${AUTH[@]}" \
  | jq '.data.appDefinitions[] | {
      appName,
      instanceCount,
      versions: [.versions[]? | {version, timeStamp, deployedImageName}] | last(3)
    }' | head -30

echo ""
echo "=== Custom Domains & SSL ==="
curl -s "${BASE}/user/apps/appDefinitions" "${AUTH[@]}" \
  | jq -r '.data.appDefinitions[] | select(.customDomain | length > 0) | "\(.appName)\t\(.customDomain | map(.publicDomain) | join(","))\tSSL:\(.hasDefaultSubDomainSsl)"' \
  | column -t

echo ""
echo "=== Persistent Directories ==="
curl -s "${BASE}/user/apps/appDefinitions" "${AUTH[@]}" \
  | jq -r '.data.appDefinitions[] | select(.volumes | length > 0) | "\(.appName)\t\(.volumes | map(.containerPath) | join(","))"' \
  | column -t

echo ""
echo "=== Resource Limits ==="
curl -s "${BASE}/user/apps/appDefinitions" "${AUTH[@]}" \
  | jq '.data.appDefinitions[] | select(.containerHttpPort != null) | {
      appName,
      containerHttpPort: .containerHttpPort,
      httpPort: .containerHttpPort,
      websocketSupport: .websocketSupport
    }'

echo ""
echo "=== System Info ==="
curl -s "${BASE}/user/system/info" "${AUTH[@]}" \
  | jq '.data | {
      hasRootSsl: .hasRootSsl,
      rootDomain: .rootDomain,
      captainVersion: .captainVersion,
      dockerVersion: .dockerVersion
    }'

echo ""
echo "=== Nginx Config Status ==="
curl -s "${BASE}/user/system/nginxconfig" "${AUTH[@]}" \
  | jq '{baseConfig: (.data.baseConfig.customValue | length > 0), captainConfig: (.data.captainConfig.customValue | length > 0)}' 2>/dev/null
```

## Output Format

```
CAPROVER ANALYSIS
==================
App              Instances  Domains              SSL   Volumes  Env-Vars
────────────────────────────────────────────────────────────────────────
web-app          2          app.example.com       Yes   1        8
api-server       3          api.example.com       Yes   0        12
worker           1          none                  No    2        5

Cluster: 2 nodes (1 leader) | Docker: v24.0.7 | Captain: v1.12.0
Root Domain: captain.example.com | Root SSL: Yes
```

## Safety Rules

- **Read-only**: Only use GET endpoints against the CapRover API
- **Never deploy, scale, or delete** apps without explicit confirmation
- **Env vars**: Never output environment variable values, only counts
- **Auth token**: Keep the captain auth token secure, rotate regularly

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


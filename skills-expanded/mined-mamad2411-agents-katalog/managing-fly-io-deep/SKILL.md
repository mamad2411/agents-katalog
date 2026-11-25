---
name: managing-fly-io-deep
description: |
  Use when working with Fly Io Deep — deep Fly.io analysis covering app
  inventory, machine status, volume management, autoscaling configuration,
  health check results, certificate status, secrets auditing, and region
  distribution. Use for comprehensive Fly.io platform assessment and
  optimization.
connection_type: fly-io
preload: false
---

# Fly.io Deep Management

Comprehensive analysis of Fly.io apps, machines, volumes, and global deployment status.

## Phase 1: Discovery

```bash
#!/bin/bash
TOKEN="${FLY_API_TOKEN}"
BASE="https://api.machines.dev/v1"
AUTH=(-H "Authorization: Bearer ${TOKEN}" -H "Content-Type: application/json")

echo "=== Apps Inventory ==="
flyctl apps list --json 2>/dev/null \
  | jq -r '.[] | "\(.Name)\t\(.Organization.Slug)\t\(.Status)\t\(.Deployed)\t\(.Hostname)"' \
  | column -t | head -20

echo ""
echo "=== Machines per App ==="
for APP in $(flyctl apps list --json 2>/dev/null | jq -r '.[].Name'); do
  curl -s "${BASE}/apps/${APP}/machines" "${AUTH[@]}" \
    | jq -r ".[] | \"${APP}\t\(.id)\t\(.state)\t\(.region)\t\(.config.guest.cpus)cpu/\(.config.guest.memory_mb)MB\t\(.config.image | split(\":\") | last)\"" 2>/dev/null
done | column -t | head -30

echo ""
echo "=== Volumes ==="
for APP in $(flyctl apps list --json 2>/dev/null | jq -r '.[].Name'); do
  flyctl volumes list --app "$APP" --json 2>/dev/null \
    | jq -r ".[] | \"${APP}\t\(.id)\t\(.name)\t\(.region)\t\(.size_gb)GB\t\(.state)\"" 2>/dev/null
done | column -t | head -20

echo ""
echo "=== Certificates ==="
for APP in $(flyctl apps list --json 2>/dev/null | jq -r '.[].Name'); do
  flyctl certs list --app "$APP" --json 2>/dev/null \
    | jq -r ".[] | \"${APP}\t\(.hostname)\t\(.clientStatus)\t\(.source)\"" 2>/dev/null
done | column -t | head -20
```

## Phase 2: Analysis

```bash
#!/bin/bash
TOKEN="${FLY_API_TOKEN}"
BASE="https://api.machines.dev/v1"
AUTH=(-H "Authorization: Bearer ${TOKEN}" -H "Content-Type: application/json")

echo "=== Machine Health Checks ==="
for APP in $(flyctl apps list --json 2>/dev/null | jq -r '.[].Name'); do
  for MACHINE in $(curl -s "${BASE}/apps/${APP}/machines" "${AUTH[@]}" | jq -r '.[].id' 2>/dev/null); do
    curl -s "${BASE}/apps/${APP}/machines/${MACHINE}" "${AUTH[@]}" \
      | jq "{app: \"${APP}\", machine: .id, state: .state, checks: [.checks[]? | {name, status, output: .output[0:50]}]}" 2>/dev/null
  done
done | head -30

echo ""
echo "=== Region Distribution ==="
for APP in $(flyctl apps list --json 2>/dev/null | jq -r '.[].Name'); do
  echo "--- ${APP} ---"
  curl -s "${BASE}/apps/${APP}/machines" "${AUTH[@]}" \
    | jq -r '.[].region' 2>/dev/null | sort | uniq -c | sort -rn
done

echo ""
echo "=== Autoscaling Config ==="
for APP in $(flyctl apps list --json 2>/dev/null | jq -r '.[].Name'); do
  flyctl autoscale show --app "$APP" --json 2>/dev/null \
    | jq "{app: \"${APP}\", min: .MinCount, max: .MaxCount, balanceRegions: .BalanceRegions}" 2>/dev/null
done

echo ""
echo "=== Secrets (names only) ==="
for APP in $(flyctl apps list --json 2>/dev/null | jq -r '.[].Name'); do
  SECRETS=$(flyctl secrets list --app "$APP" --json 2>/dev/null | jq -r '.[].Name' 2>/dev/null | tr '\n' ', ')
  [ -n "$SECRETS" ] && echo "${APP}: ${SECRETS}"
done

echo ""
echo "=== Resource Summary ==="
for APP in $(flyctl apps list --json 2>/dev/null | jq -r '.[].Name'); do
  curl -s "${BASE}/apps/${APP}/machines" "${AUTH[@]}" \
    | jq "{app: \"${APP}\", machines: length, total_cpus: [.[].config.guest.cpus] | add, total_memory_mb: [.[].config.guest.memory_mb] | add}" 2>/dev/null
done
```

## Output Format

```
FLY.IO DEEP ANALYSIS
======================
App              Machines  Regions    CPU/Mem       Volumes  Status    Checks
──────────────────────────────────────────────────────────────────────────────
web-api          3         iad,lhr    2cpu/512MB    0        deployed  passing
worker           2         iad        4cpu/1024MB   2x10GB   deployed  passing
cron-job         1         iad        1cpu/256MB    0        deployed  passing

Regions: iad(4) lhr(2) | Total: 6 machines, 10 CPUs, 2.5GB RAM
Certificates: 3 valid | Secrets: 12 across 3 apps
```

## Safety Rules

- **Read-only**: Only use `flyctl * list`, `show` and GET endpoints
- **Never deploy, scale, or destroy** machines without explicit confirmation
- **Secrets**: Never output secret values, only list names
- **Rate limits**: Fly Machines API has no published rate limit but use reasonable request rates

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


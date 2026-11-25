---
name: managing-anyscale
description: |
  Use when working with Anyscale — anyscale platform management covering Ray
  clusters, services, model deployments, jobs, and usage analytics. Use when
  monitoring deployed services, analyzing cluster utilization, reviewing job
  status, managing model endpoints, or troubleshooting Anyscale deployments.
connection_type: anyscale
preload: false
---

# Anyscale Management Skill

Manage and analyze Anyscale platform resources including services, clusters, jobs, and deployments.

## API Conventions

### Authentication
All API calls use Bearer API key, injected automatically.

### Base URL
`https://api.anyscale.com/v2`

### Core Helper Function

```bash
#!/bin/bash

anyscale_api() {
    local method="$1"
    local endpoint="$2"
    local data="${3:-}"

    if [ -n "$data" ]; then
        curl -s -X "$method" \
            -H "Authorization: Bearer $ANYSCALE_API_KEY" \
            -H "Content-Type: application/json" \
            "https://api.anyscale.com/v2${endpoint}" \
            -d "$data"
    else
        curl -s -X "$method" \
            -H "Authorization: Bearer $ANYSCALE_API_KEY" \
            "https://api.anyscale.com/v2${endpoint}"
    fi
}
```

## Output Rules
- Target ≤50 lines per script output
- Use `jq` to extract only needed fields
- Never dump full API responses

## Phase 1: Discovery

```bash
#!/bin/bash
echo "=== Services ==="
anyscale_api GET "/services?count=20" \
    | jq -r '.results[] | "\(.id[0:16])\t\(.name)\t\(.state)\t\(.created_at[0:10])"' \
    | column -t | head -15

echo ""
echo "=== Clusters ==="
anyscale_api GET "/sessions?count=20" \
    | jq -r '.results[] | "\(.id[0:16])\t\(.name)\t\(.state)\t\(.created_at[0:10])"' \
    | column -t | head -15

echo ""
echo "=== Jobs ==="
anyscale_api GET "/jobs?count=20" \
    | jq -r '.results[] | "\(.id[0:16])\t\(.name[0:30])\t\(.state)\t\(.created_at[0:10])"' \
    | column -t | head -15

echo ""
echo "=== Cloud Configurations ==="
anyscale_api GET "/clouds" \
    | jq -r '.results[] | "\(.id[0:16])\t\(.name)\t\(.provider)\t\(.region)"' | head -10
```

## Phase 2: Analysis

### Service Health

```bash
#!/bin/bash
echo "=== Service Status Summary ==="
anyscale_api GET "/services?count=50" \
    | jq -r '.results[] | .state' | sort | uniq -c | sort -rn

echo ""
echo "=== Running Services ==="
anyscale_api GET "/services?count=20&state=RUNNING" \
    | jq -r '.results[] | "\(.name)\t\(.state)\t\(.current_version)\t\(.base_url[0:40])"' \
    | column -t | head -15

echo ""
echo "=== Failed Services ==="
anyscale_api GET "/services?count=10&state=SYSTEM_FAILURE,UNHEALTHY" \
    | jq -r '.results[] | "\(.name)\t\(.state)\t\(.status_message[0:60])"' | head -10
```

### Job & Cluster Analytics

```bash
#!/bin/bash
echo "=== Job Status Summary ==="
anyscale_api GET "/jobs?count=100" \
    | jq -r '.results[] | .state' | sort | uniq -c | sort -rn

echo ""
echo "=== Active Clusters ==="
anyscale_api GET "/sessions?count=20&state=RUNNING" \
    | jq -r '.results[] | "\(.name)\t\(.state)\t\(.head_node_type)\t\(.num_workers) workers"' \
    | column -t | head -10

echo ""
echo "=== Recent Failed Jobs ==="
anyscale_api GET "/jobs?count=10&state=FAILED" \
    | jq -r '.results[] | "\(.id[0:16])\t\(.name[0:30])\t\(.created_at[0:10])\t\(.error_message[0:50] // "no error")"' \
    | head -10
```

## Output Format

```
=== Anyscale Account ===
Services: <n>  Clusters: <n>  Jobs: <n>

--- Service Health ---
Running: <n>  Unhealthy: <n>  Failed: <n>

--- Job Summary ---
Succeeded: <n>  Running: <n>  Failed: <n>

--- Clusters ---
Active: <n>  Total Workers: <n>
```

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

## Common Pitfalls
- **Service states**: `STARTING`, `RUNNING`, `UPDATING`, `UNHEALTHY`, `SYSTEM_FAILURE`, `TERMINATED`
- **Pagination**: Use `count` and `paging_token` for list endpoints
- **Rate limits**: Check response headers for current rate limit status
- **Cloud scoping**: Resources are scoped to specific cloud configurations

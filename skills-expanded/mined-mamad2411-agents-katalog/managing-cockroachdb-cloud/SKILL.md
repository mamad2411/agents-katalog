---
name: managing-cockroachdb-cloud
description: |
  Use when working with Cockroachdb Cloud — cockroachDB Cloud (Serverless &
  Dedicated) management via the ccloud CLI and CockroachDB Cloud API. Covers
  clusters, databases, SQL users, networking, backups, and metrics. Use when
  managing CockroachDB Cloud clusters or reviewing database health.
connection_type: cockroachdb-cloud
preload: false
---

# Managing CockroachDB Cloud

Manage CockroachDB Cloud using the `ccloud` CLI and CockroachDB Cloud API.

## MANDATORY: Discovery-First Pattern

**Always discover available resources before performing analysis.**

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== Clusters ==="
ccloud cluster list --output json 2>/dev/null | jq -r '.[] | "\(.id)\t\(.name)\t\(.plan)\t\(.cloud_provider)\t\(.state)\t\(.regions[0].name)"' | head -20 || \
curl -s "https://cockroachlabs.cloud/api/v1/clusters" \
    -H "Authorization: Bearer $CC_API_KEY" | jq -r '.clusters[] | "\(.id)\t\(.name)\t\(.plan)\t\(.cloud_provider)\t\(.state)\t\(.regions[0].name)"' | head -20

echo ""
echo "=== SQL Users ==="
for cluster_id in $(ccloud cluster list --output json 2>/dev/null | jq -r '.[].id' | head -5); do
    echo "--- Cluster: $cluster_id ---"
    ccloud cluster sql-user list --cluster-id "$cluster_id" --output json 2>/dev/null | jq -r '.[] | "\(.name)"' | head -10
done

echo ""
echo "=== Databases ==="
for cluster_id in $(ccloud cluster list --output json 2>/dev/null | jq -r '.[].id' | head -5); do
    echo "--- Cluster: $cluster_id ---"
    ccloud cluster db list --cluster-id "$cluster_id" --output json 2>/dev/null | jq -r '.[] | "\(.name)"' | head -10
done
```

### Phase 2: Analysis

```bash
#!/bin/bash

CLUSTER_ID="${1:?Cluster ID required}"

echo "=== Cluster Details ==="
ccloud cluster get "$CLUSTER_ID" --output json 2>/dev/null | jq '{
    id, name, plan, state, cloud_provider,
    cockroach_version, creator_id,
    regions: [.regions[] | {name: .name, node_count: .node_count, sql_dns: .sql_dns}],
    config: .config,
    created_at, updated_at
}' || \
curl -s "https://cockroachlabs.cloud/api/v1/clusters/$CLUSTER_ID" \
    -H "Authorization: Bearer $CC_API_KEY" | jq '{id, name, plan, state, cloud_provider, cockroach_version, regions}'

echo ""
echo "=== Networking (Allowed IPs) ==="
ccloud cluster networking allowlist list --cluster-id "$CLUSTER_ID" --output json 2>/dev/null | jq -r '.[] | "\(.cidr_ip)/\(.cidr_mask)\t\(.name)\t\(.sql)\t\(.ui)"' | head -10

echo ""
echo "=== Backups ==="
curl -s "https://cockroachlabs.cloud/api/v1/clusters/$CLUSTER_ID/backups" \
    -H "Authorization: Bearer $CC_API_KEY" | jq -r '.backups[] | "\(.id)\t\(.status)\t\(.created_at)\t\(.expires_at)"' | head -10

echo ""
echo "=== Cluster Metrics ==="
curl -s "https://cockroachlabs.cloud/api/v1/clusters/$CLUSTER_ID/metrics" \
    -H "Authorization: Bearer $CC_API_KEY" | jq '{storage_used, request_units_used, row_count, regions_count}' 2>/dev/null | head -10

echo ""
echo "=== Connection String ==="
ccloud cluster sql --cluster-id "$CLUSTER_ID" --url 2>/dev/null | head -3
```

## Output Format

```
CLUSTER_ID                            NAME       PLAN        PROVIDER  STATE   REGION
abc123-def456-ghi789                  prod-db    dedicated   AWS       CREATED us-east-1
def456-ghi789-jkl012                  dev-db     serverless  GCP       CREATED us-central1
```

## Safety Rules
- Use read-only commands: `list`, `get`
- Never run `delete`, `drop`, `update` without explicit user confirmation
- Use `--output json` with jq for structured output parsing
- Limit output with `| head -N` to stay under 50 lines

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


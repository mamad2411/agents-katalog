---
name: managing-appwrite
description: |
  Use when working with Appwrite — appwrite backend platform management covering
  project inventory, database collections, user authentication stats, storage
  bucket usage, function deployments, webhook configuration, and platform
  health. Use for comprehensive Appwrite project assessment and resource
  monitoring.
connection_type: appwrite
preload: false
---

# Appwrite Management

Analyze Appwrite projects, databases, auth, storage, and serverless functions.

## Phase 1: Discovery

```bash
#!/bin/bash
TOKEN="${APPWRITE_API_KEY}"
ENDPOINT="${APPWRITE_ENDPOINT:-https://cloud.appwrite.io/v1}"
PROJECT="${APPWRITE_PROJECT_ID}"
AUTH=(-H "X-Appwrite-Key: ${TOKEN}" -H "X-Appwrite-Project: ${PROJECT}" -H "Content-Type: application/json")

echo "=== Databases ==="
curl -s "${ENDPOINT}/databases" "${AUTH[@]}" \
  | jq -r '.databases[] | "\(.name)\t\(.$id)\t\(.enabled)\t\(.$createdAt)"' \
  | column -t | head -20

echo ""
echo "=== Collections per Database ==="
for DB in $(curl -s "${ENDPOINT}/databases" "${AUTH[@]}" | jq -r '.databases[].$id'); do
  curl -s "${ENDPOINT}/databases/${DB}/collections" "${AUTH[@]}" \
    | jq -r ".collections[] | \"${DB}\t\(.name)\t\(.\$id)\t\(.enabled)\t\(.documentSecurity)\"" 2>/dev/null
done | column -t | head -20

echo ""
echo "=== Storage Buckets ==="
curl -s "${ENDPOINT}/storage/buckets" "${AUTH[@]}" \
  | jq -r '.buckets[] | "\(.name)\t\(.$id)\t\(.maximumFileSize)\t\(.encryption)\t\(.antivirus)"' \
  | column -t | head -20

echo ""
echo "=== Functions ==="
curl -s "${ENDPOINT}/functions" "${AUTH[@]}" \
  | jq -r '.functions[] | "\(.name)\t\(.runtime)\t\(.status)\t\(.timeout)s\t\(.schedule // \"none\")"' \
  | column -t | head -20
```

## Phase 2: Analysis

```bash
#!/bin/bash
TOKEN="${APPWRITE_API_KEY}"
ENDPOINT="${APPWRITE_ENDPOINT:-https://cloud.appwrite.io/v1}"
PROJECT="${APPWRITE_PROJECT_ID}"
AUTH=(-H "X-Appwrite-Key: ${TOKEN}" -H "X-Appwrite-Project: ${PROJECT}" -H "Content-Type: application/json")

echo "=== User Stats ==="
curl -s "${ENDPOINT}/users" "${AUTH[@]}" \
  | jq '{total_users: .total}' 2>/dev/null

echo ""
echo "=== Function Deployments ==="
for FN in $(curl -s "${ENDPOINT}/functions" "${AUTH[@]}" | jq -r '.functions[].$id'); do
  NAME=$(curl -s "${ENDPOINT}/functions/${FN}" "${AUTH[@]}" | jq -r '.name')
  curl -s "${ENDPOINT}/functions/${FN}/deployments" "${AUTH[@]}" \
    | jq -r ".deployments[:3][] | \"${NAME}\t\(.\$id[0:8])\t\(.status)\t\(.buildSize // 0)\t\(.\$createdAt)\"" 2>/dev/null
done | column -t | head -20

echo ""
echo "=== Webhooks ==="
curl -s "${ENDPOINT}/projects/${PROJECT}/webhooks" "${AUTH[@]}" \
  | jq -r '.webhooks[] | "\(.name)\t\(.url[0:40])\t\(.enabled)\t\(.events | length) events"' 2>/dev/null \
  | column -t | head -10

echo ""
echo "=== Teams ==="
curl -s "${ENDPOINT}/teams" "${AUTH[@]}" \
  | jq -r '.teams[] | "\(.name)\t\(.$id)\t\(.total) members\t\(.$createdAt)"' \
  | column -t | head -10

echo ""
echo "=== Health Checks ==="
for CHECK in db cache queue certificates; do
  STATUS=$(curl -s "${ENDPOINT}/health/${CHECK}" "${AUTH[@]}" | jq -r '.status // "unknown"' 2>/dev/null)
  echo "${CHECK}: ${STATUS}"
done
```

## Output Format

```
APPWRITE ANALYSIS
===================
Database         Collections  Docs     Functions  Storage Buckets
──────────────────────────────────────────────────────────────────
main-db          8            12,450   5          3
analytics-db     3            45,200   2          1

Users: 1,245 total | Teams: 4 | Webhooks: 6 active
Health: DB(ok) Cache(ok) Queue(ok) Certs(ok)
Deployments: 7 recent (6 successful, 1 failed)
```

## Safety Rules

- **Read-only**: Only use GET/list endpoints against the Appwrite API
- **Never create, update, or delete** databases, collections, or users without confirmation
- **API keys**: Never output API key values in results
- **Rate limits**: Respect Appwrite rate limits (default 60 requests per minute)

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


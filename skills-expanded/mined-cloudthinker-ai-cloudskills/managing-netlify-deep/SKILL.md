---
name: managing-netlify-deep
description: |
  Use when working with Netlify Deep — deep Netlify platform analysis covering
  site inventory, deploy history, serverless function logs, edge function
  status, form submissions, bandwidth usage, build plugin configurations, and
  DNS/domain settings. Use for comprehensive Netlify project health assessment.
connection_type: netlify
preload: false
---

# Netlify Deep Management

Comprehensive analysis of Netlify sites, deployments, serverless functions, and platform health.

## Phase 1: Discovery

```bash
#!/bin/bash
TOKEN="${NETLIFY_AUTH_TOKEN}"
BASE="https://api.netlify.com/api/v1"

echo "=== Sites Inventory ==="
curl -s "${BASE}/sites" \
  -H "Authorization: Bearer ${TOKEN}" \
  | jq -r '.[] | "\(.id)\t\(.name)\t\(.ssl_url)\t\(.published_deploy.published_at)\t\(.build_settings.repo_url // "manual")"' \
  | column -t | head -20

echo ""
echo "=== Site Build Settings ==="
curl -s "${BASE}/sites" \
  -H "Authorization: Bearer ${TOKEN}" \
  | jq '.[] | {name, framework: .build_settings.provider, cmd: .build_settings.cmd, dir: .build_settings.dir, branch: .build_settings.repo_branch}' \
  | head -30

echo ""
echo "=== Custom Domains ==="
for SITE_ID in $(curl -s "${BASE}/sites" -H "Authorization: Bearer ${TOKEN}" | jq -r '.[].id'); do
  SITE_NAME=$(curl -s "${BASE}/sites/${SITE_ID}" -H "Authorization: Bearer ${TOKEN}" | jq -r '.name')
  curl -s "${BASE}/sites/${SITE_ID}/domains" \
    -H "Authorization: Bearer ${TOKEN}" \
    | jq -r ".[] | \"${SITE_NAME}\t\(.hostname)\t\(.ssl.state // \"pending\")\""
done | column -t | head -20

echo ""
echo "=== Serverless Functions ==="
for SITE_ID in $(curl -s "${BASE}/sites" -H "Authorization: Bearer ${TOKEN}" | jq -r '.[].id'); do
  SITE_NAME=$(curl -s "${BASE}/sites/${SITE_ID}" -H "Authorization: Bearer ${TOKEN}" | jq -r '.name')
  curl -s "${BASE}/sites/${SITE_ID}/functions" \
    -H "Authorization: Bearer ${TOKEN}" \
    | jq -r ".[] | \"${SITE_NAME}\t\(.n)\t\(.a // \"unknown\")\"" 2>/dev/null
done | column -t | head -20
```

## Phase 2: Analysis

```bash
#!/bin/bash
TOKEN="${NETLIFY_AUTH_TOKEN}"
BASE="https://api.netlify.com/api/v1"

echo "=== Recent Deploys ==="
for SITE_ID in $(curl -s "${BASE}/sites" -H "Authorization: Bearer ${TOKEN}" | jq -r '.[].id' | head -5); do
  SITE_NAME=$(curl -s "${BASE}/sites/${SITE_ID}" -H "Authorization: Bearer ${TOKEN}" | jq -r '.name')
  curl -s "${BASE}/sites/${SITE_ID}/deploys?per_page=5" \
    -H "Authorization: Bearer ${TOKEN}" \
    | jq -r ".[] | \"${SITE_NAME}\t\(.id[0:8])\t\(.state)\t\(.deploy_time // 0)s\t\(.created_at)\t\(.branch // \"production\")\""
done | column -t | head -30

echo ""
echo "=== Build Plugins ==="
for SITE_ID in $(curl -s "${BASE}/sites" -H "Authorization: Bearer ${TOKEN}" | jq -r '.[].id'); do
  curl -s "${BASE}/sites/${SITE_ID}/plugins" \
    -H "Authorization: Bearer ${TOKEN}" \
    | jq -r ".[].package" 2>/dev/null
done | sort | uniq -c | sort -rn | head -15

echo ""
echo "=== Bandwidth Usage ==="
curl -s "${BASE}/accounts" \
  -H "Authorization: Bearer ${TOKEN}" \
  | jq '.[] | {name: .name, bandwidth_used: .capabilities.bandwidth.used, bandwidth_included: .capabilities.bandwidth.included}'

echo ""
echo "=== Form Submissions ==="
for SITE_ID in $(curl -s "${BASE}/sites" -H "Authorization: Bearer ${TOKEN}" | jq -r '.[].id'); do
  FORMS=$(curl -s "${BASE}/sites/${SITE_ID}/forms" -H "Authorization: Bearer ${TOKEN}" | jq -r '.[] | "\(.name)\t\(.submission_count) submissions"' 2>/dev/null)
  [ -n "$FORMS" ] && echo "$FORMS"
done | column -t

echo ""
echo "=== Deploy Failure Rate ==="
for SITE_ID in $(curl -s "${BASE}/sites" -H "Authorization: Bearer ${TOKEN}" | jq -r '.[].id' | head -5); do
  SITE_NAME=$(curl -s "${BASE}/sites/${SITE_ID}" -H "Authorization: Bearer ${TOKEN}" | jq -r '.name')
  TOTAL=$(curl -s "${BASE}/sites/${SITE_ID}/deploys?per_page=20" -H "Authorization: Bearer ${TOKEN}" | jq 'length')
  FAILED=$(curl -s "${BASE}/sites/${SITE_ID}/deploys?per_page=20" -H "Authorization: Bearer ${TOKEN}" | jq '[.[] | select(.state=="error")] | length')
  echo "${SITE_NAME}: ${FAILED}/${TOTAL} failed"
done
```

## Output Format

```
NETLIFY DEEP ANALYSIS
=======================
Site              Domains  Functions  Last Deploy    Build Time  Status
───────────────────────────────────────────────────────────────────────
my-app            2        3          2h ago         45s         ready
docs-site         1        0          1d ago         120s        ready
api-proxy         1        5          30m ago        30s         ready

Deploy Success Rate: 95% (19/20 recent) | Bandwidth: 45/100 GB used
Build Plugins: 4 unique | Forms: 2 active
```

## Safety Rules

- **Read-only**: Only use GET endpoints against the Netlify API
- **Never trigger deploys** or delete sites without explicit confirmation
- **Env vars**: Use `GET /sites/{id}/env` but never output secret values
- **Rate limits**: Netlify API limit is 500 requests per minute per token

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


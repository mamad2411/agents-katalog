---
name: managing-launchdarkly
description: |
  Use when working with Launchdarkly — launchDarkly feature flag management,
  targeting rules, environments, experimentation, and audit logging. Covers flag
  lifecycle, user targeting, percentage rollouts, prerequisite flags, flag
  scheduling, and SDK connection status. Use when managing feature flags,
  reviewing targeting rules, analyzing flag usage, auditing changes, or
  monitoring SDK connections in LaunchDarkly.
connection_type: launchdarkly
preload: false
---

# LaunchDarkly Management Skill

Manage and analyze feature flags, targeting rules, environments, and experiments in LaunchDarkly.

## API Conventions

### Authentication
All API calls use the `Authorization: $LAUNCHDARKLY_API_KEY` header. Never hardcode tokens.

### Base URL
`https://app.launchdarkly.com/api/v2`

### Core Helper Function

```bash
#!/bin/bash

ld_api() {
    local method="$1"
    local endpoint="$2"
    local data="${3:-}"

    if [ -n "$data" ]; then
        curl -s -X "$method" \
            -H "Authorization: $LAUNCHDARKLY_API_KEY" \
            -H "Content-Type: application/json" \
            "https://app.launchdarkly.com/api/v2${endpoint}" \
            -d "$data"
    else
        curl -s -X "$method" \
            -H "Authorization: $LAUNCHDARKLY_API_KEY" \
            -H "Content-Type: application/json" \
            "https://app.launchdarkly.com/api/v2${endpoint}"
    fi
}
```

## Output Rules
- **TOKEN EFFICIENCY**: Extract only needed fields with `jq`
- Target <=50 lines per script output
- Never dump full API responses

## Discovery Phase

### List Projects and Environments

```bash
#!/bin/bash
echo "=== Projects ==="
ld_api GET "/projects" \
    | jq -r '.items[] | "\(.key)\t\(.name)\t\(.environments | length) envs"' | column -t

echo ""
PROJECT_KEY="${1:-default}"
echo "=== Environments ==="
ld_api GET "/projects/${PROJECT_KEY}" \
    | jq -r '.environments[] | "\(.key)\t\(.name)\t\(.color)"' | column -t
```

### List Feature Flags

```bash
#!/bin/bash
PROJECT_KEY="${1:-default}"

echo "=== Feature Flags ==="
ld_api GET "/flags/${PROJECT_KEY}?limit=25&sort=creationDate" \
    | jq -r '.items[] | "\(.kind)\t\(.key)\t\(.name[0:40])\t\(.archived)"' | column -t

echo ""
echo "=== Flag Summary ==="
ld_api GET "/flags/${PROJECT_KEY}?limit=100" \
    | jq '{total: .totalCount, by_kind: (.items | group_by(.kind) | map({(.[0].kind): length}) | add), archived: ([.items[] | select(.archived)] | length)}'
```

## Analysis Phase

### Flag Status by Environment

```bash
#!/bin/bash
PROJECT_KEY="${1:-default}"
ENV_KEY="${2:-production}"

echo "=== Flag Status in ${ENV_KEY} ==="
ld_api GET "/flags/${PROJECT_KEY}?limit=25&env=${ENV_KEY}" \
    | jq -r '.items[] | "\(.key)\t\(.environments["'"${ENV_KEY}"'"].on)\t\(.environments["'"${ENV_KEY}"'"].rules | length) rules"' \
    | column -t

echo ""
echo "=== Stale Flags (not evaluated in 7 days) ==="
ld_api GET "/flags/${PROJECT_KEY}?limit=50&env=${ENV_KEY}&filter=query:\"state:live,stale\"" \
    | jq -r '.items[0:10][] | "\(.key)\t\(.name[0:40])"' | column -t
```

### Audit Log

```bash
#!/bin/bash
echo "=== Recent Changes ==="
ld_api GET "/auditlog?limit=20" \
    | jq -r '.items[] | "\(.date | todate | .[0:16])\t\(.member.email // "api")\t\(.kind)\t\(.name[0:40])"' \
    | column -t

echo ""
echo "=== Changes by Type ==="
ld_api GET "/auditlog?limit=50" \
    | jq -r '.items[] | .kind' | sort | uniq -c | sort -rn | head -10
```

## Output Format
- Use tab-separated columns with `column -t`
- Limit lists to 15-25 items
- Show summaries before details

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
- **No Bearer prefix**: Auth header is just the API key, not `Bearer $KEY`
- **Project-scoped flags**: Flag endpoints require the project key in the path
- **Environment-specific state**: Flag on/off state and rules are per-environment
- **Semantic patching**: Updates use JSON Patch format or semantic patch operations
- **Flag kinds**: `boolean` or `multivariate` (string, number, JSON)
- **Rate limits**: 10 requests per second for standard API
- **Pagination**: Use `limit` and `offset`, max 20 items per page by default

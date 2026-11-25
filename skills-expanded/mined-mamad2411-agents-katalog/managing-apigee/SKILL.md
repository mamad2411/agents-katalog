---
name: managing-apigee
description: |
  Use when working with Apigee — apigee API platform management - API proxy
  deployment, environment configuration, analytics and traffic analysis,
  developer and app management. Use when managing Apigee-based API
  infrastructure, deploying proxies, analyzing API traffic patterns, or managing
  developer portal resources.
connection_type: apigee
preload: false
---

# Apigee API Management Skill

Manage Apigee API proxies, environments, developers, apps, and analytics via the Management API.

## Core Helper Functions

```bash
#!/bin/bash

# Apigee Management API
APIGEE_ORG="${APIGEE_ORG:-}"
APIGEE_BASE="https://apigee.googleapis.com/v1/organizations/${APIGEE_ORG}"
APIGEE_TOKEN="${APIGEE_TOKEN:-$(gcloud auth print-access-token 2>/dev/null)}"

# Apigee API wrapper
apigee_api() {
    local method="${1:-GET}"
    local endpoint="$2"
    shift 2
    curl -s -X "$method" "${APIGEE_BASE}${endpoint}" \
        -H "Authorization: Bearer ${APIGEE_TOKEN}" \
        -H "Content-Type: application/json" "$@" | jq '.'
}

# List helper with field extraction
apigee_list() {
    local endpoint="$1"
    apigee_api GET "$endpoint"
}
```

## MANDATORY: Discovery-First Pattern

**Always inspect the Apigee organization and environments before performing operations.**

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== Organization Info ==="
apigee_api GET "" | jq '{name: .name, display_name: .displayName, type: .type, runtime_type: .runtimeType, state: .state}'

echo ""
echo "=== Environments ==="
apigee_api GET "/environments" | jq '.'

echo ""
echo "=== API Proxies ==="
apigee_api GET "/apis" | jq '{total: (.proxies | length), proxies: [.proxies[] | {name, revision: .revision | last}]}'

echo ""
echo "=== Environment Groups ==="
apigee_api GET "/envgroups" | jq '[.environmentGroups[] | {name, hostnames}]'
```

## Output Rules
- **TOKEN EFFICIENCY**: Target <=50 lines per output
- Always extract specific fields from API responses with jq
- Never dump full proxy bundles -- extract metadata only

## Common Operations

### API Proxy Management

```bash
#!/bin/bash

echo "=== API Proxies with Deployment Status ==="
for env in $(apigee_api GET "/environments" | jq -r '.[]'); do
    echo "--- Environment: $env ---"
    apigee_api GET "/environments/${env}/deployments" | jq '[.deployments[] | {
        api_proxy: .apiProxy,
        revision: .revision,
        state: .state,
        deployed_at: .deployStartTime
    }]'
done

echo ""
echo "=== Proxy Revisions ==="
PROXY="${1:-}"
if [ -n "$PROXY" ]; then
    apigee_api GET "/apis/${PROXY}/revisions" | jq '.'
    echo "Latest revision details:"
    latest=$(apigee_api GET "/apis/${PROXY}/revisions" | jq -r '.[-1]')
    apigee_api GET "/apis/${PROXY}/revisions/${latest}" | jq '{name, revision, basepaths: .basepaths, policies, proxy_endpoints: .proxies, target_endpoints: .targets}'
fi

echo ""
echo "=== Undeployed Proxies ==="
all_proxies=$(apigee_api GET "/apis" | jq -r '.proxies[].name')
for proxy in $all_proxies; do
    deployed=$(apigee_api GET "/apis/${proxy}/deployments" | jq '.deployments | length')
    if [ "$deployed" -eq 0 ]; then
        echo "  Not deployed: $proxy"
    fi
done
```

### Environment and Deployment Analysis

```bash
#!/bin/bash
ENV="${1:?Environment name required}"

echo "=== Environment Details: $ENV ==="
apigee_api GET "/environments/${ENV}" | jq '{name, description, state: .state, deployment_type: .deploymentType}'

echo ""
echo "=== Deployments in $ENV ==="
apigee_api GET "/environments/${ENV}/deployments" | jq '[.deployments[] | {proxy: .apiProxy, revision: .revision, state: .state}] | sort_by(.proxy)'

echo ""
echo "=== Target Servers ==="
apigee_api GET "/environments/${ENV}/targetservers" | jq '[.[] | {name, host, port, is_enabled: .isEnabled, ssl_info: (.sSLInfo.enabled // false)}]'

echo ""
echo "=== Keystores and Truststores ==="
apigee_api GET "/environments/${ENV}/keystores" | jq '.'
```

### Analytics and Traffic Analysis

```bash
#!/bin/bash
ENV="${1:-prod}"
TIMERANGE="01/01/$(date +%Y)~$(date +%m/%d/%Y)"

echo "=== API Traffic Summary ==="
apigee_api GET "/environments/${ENV}/stats/apiproxy?select=sum(message_count),avg(total_response_time)&timeRange=${TIMERANGE}&timeUnit=day" \
    | jq '.environments[0].dimensions[] | {proxy: .name, metrics: [.metrics[] | {name: .name, values: [.values[] | .value] | add}]}'

echo ""
echo "=== Error Rates by Proxy ==="
apigee_api GET "/environments/${ENV}/stats/apiproxy?select=sum(is_error),sum(message_count)&timeRange=${TIMERANGE}" \
    | jq '[.environments[0].dimensions[] | {proxy: .name, errors: .metrics[0].values[0].value, total: .metrics[1].values[0].value}]'

echo ""
echo "=== Top Developers by Traffic ==="
apigee_api GET "/environments/${ENV}/stats/developer_email?select=sum(message_count)&timeRange=${TIMERANGE}&sortby=sum(message_count)&sort=DESC&limit=10" \
    | jq '[.environments[0].dimensions[] | {developer: .name, calls: .metrics[0].values[0].value}]'
```

### Developer and App Management

```bash
#!/bin/bash

echo "=== Developers ==="
apigee_api GET "/developers" | jq '[.developer[] | {email, first_name: .firstName, last_name: .lastName, status}] | sort_by(.email)'

echo ""
echo "=== Developer Apps ==="
DEV_EMAIL="${1:-}"
if [ -n "$DEV_EMAIL" ]; then
    apigee_api GET "/developers/${DEV_EMAIL}/apps" | jq '.app[]'
    for app in $(apigee_api GET "/developers/${DEV_EMAIL}/apps" | jq -r '.app[]'); do
        apigee_api GET "/developers/${DEV_EMAIL}/apps/${app}" | jq '{name, status, credentials: [.credentials[] | {consumer_key: .consumerKey[0:8], status, api_products: [.apiProducts[] | {name: .apiproduct, status}]}]}'
    done
fi

echo ""
echo "=== API Products ==="
apigee_api GET "/apiproducts" | jq '[.apiProduct[] | {name, display_name: .displayName, approval_type: .approvalType, proxies, environments, quota: .quota, quota_interval: .quotaInterval}]'
```

## Safety Rules
- **Read-only by default**: Only use GET requests for discovery and inspection
- **Never undeploy** proxies from production without explicit user confirmation
- **Never expose** consumer keys/secrets or developer credentials in output
- **Deployment caution**: Deploying a new revision unlinks the previous one; ensure rollback readiness
- **Environment isolation**: Never promote directly to production; validate in test/staging first

## Output Format

Present results as a structured report:
```
Managing Apigee Report
══════════════════════
Resources discovered: [count]

Resource       Status    Key Metric    Issues
──────────────────────────────────────────────
[name]         [ok/warn] [value]       [findings]

Summary: [total] resources | [ok] healthy | [warn] warnings | [crit] critical
Action Items: [list of prioritized findings]
```

Target ≤50 lines of output. Use tables for multi-resource comparisons.

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
- **Revision immutability**: Proxy revisions are immutable; changes require a new revision
- **Deployment slots**: Each environment has limited deployment slots; undeployed revisions free slots
- **Quota enforcement**: Quotas are set on API products, not proxies; misconfigured products bypass limits
- **Shared flows**: Changes to shared flows affect all proxies referencing them across environments
- **Analytics lag**: Analytics data can be delayed 10-15 minutes; do not use for real-time monitoring

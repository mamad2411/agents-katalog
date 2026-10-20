---
name: gcp-cloud-armor
description: |
  Use when working with Gcp Cloud Armor — google Cloud Armor security policy
  management, WAF rule configuration, adaptive protection analysis, and edge
  security policy management via gcloud CLI.
connection_type: gcp
preload: false
---

# Cloud Armor Skill

Manage and analyze Google Cloud Armor security policies using `gcloud compute security-policies` commands.

## Discovery-First Rule

**ALWAYS discover before acting.** Never assume policy names, rule priorities, or backend service names.

```bash
# Discover security policies
gcloud compute security-policies list --format=json \
  | jq '[.[] | {name: .name, type: .type, adaptiveProtection: .adaptiveProtectionConfig.layer7DdosDefenseConfig.enable, ruleCount: .rules | length}]'
```

## Parallel Execution Requirement

**ALL independent operations MUST run in parallel using background jobs (&) and wait.**

```bash
for policy in $(gcloud compute security-policies list --format="value(name)"); do
  {
    gcloud compute security-policies describe "$policy" --format=json
  } &
done
wait
```

## Helper Functions

```bash
# Get policy details with rules
get_policy_details() {
  local policy="$1"
  gcloud compute security-policies describe "$policy" --format=json \
    | jq '{name: .name, type: .type, fingerprint: .fingerprint, adaptiveProtection: .adaptiveProtectionConfig, advancedOptions: .advancedOptionsConfig, rules: [.rules[] | {priority: .priority, action: .action, description: .description, preview: .preview, match: .match}]}'
}

# List rules in a policy
list_rules() {
  local policy="$1"
  gcloud compute security-policies rules list "$policy" --format=json \
    | jq '[.[] | {priority: .priority, action: .action, description: .description, preview: .preview, matchType: (if .match.expr then "CEL" elif .match.config then "IP/Range" else "default" end), rateLimit: .rateLimitOptions}]'
}

# Get backend services using a policy
get_backend_services() {
  gcloud compute backend-services list --format=json \
    | jq '[.[] | select(.securityPolicy) | {name: .name, securityPolicy: .securityPolicy | split("/") | last, protocol: .protocol}]'
}

# Get security policy logs
get_armor_logs() {
  local policy="$1" limit="${2:-50}"
  gcloud logging read "resource.type=\"http_load_balancer\" AND jsonPayload.enforcedSecurityPolicy.name=\"$policy\"" --limit="$limit" --format=json \
    | jq '[.[] | {timestamp: .timestamp, action: .jsonPayload.enforcedSecurityPolicy.outcome, rule: .jsonPayload.enforcedSecurityPolicy.priority, remoteIp: .httpRequest.remoteIp, requestUrl: .httpRequest.requestUrl}]'
}
```

## Common Operations

### 1. Security Policy Overview

```bash
policies=$(gcloud compute security-policies list --format="value(name)")
for policy in $policies; do
  {
    get_policy_details "$policy"
  } &
done
wait
```

### 2. WAF Rule Analysis

```bash
# Detailed rule inspection
list_rules "$POLICY"

# Check preconfigured WAF rules (OWASP)
gcloud compute security-policies describe "$POLICY" --format=json \
  | jq '[.rules[] | select(.match.expr.expression | contains("evaluatePreconfiguredWaf")) | {priority: .priority, action: .action, wafRule: .match.expr.expression, preview: .preview}]'

# Available preconfigured rules
gcloud compute security-policies list-preconfigured-expression-sets --format=json
```

### 3. Adaptive Protection

```bash
# Check adaptive protection config
gcloud compute security-policies describe "$POLICY" --format=json \
  | jq '{adaptiveProtection: .adaptiveProtectionConfig.layer7DdosDefenseConfig, autoDeployConfig: .adaptiveProtectionConfig.autoDeployConfig}'

# Check adaptive protection events via logging
gcloud logging read "resource.type=\"http_load_balancer\" AND jsonPayload.enforcedSecurityPolicy.adaptiveProtection" --limit=20 --format=json
```

### 4. Rate Limiting Rules

```bash
# List rate limiting rules
gcloud compute security-policies describe "$POLICY" --format=json \
  | jq '[.rules[] | select(.rateLimitOptions) | {priority: .priority, action: .action, rateLimitThreshold: .rateLimitOptions.rateLimitThreshold, conformAction: .rateLimitOptions.conformAction, exceedAction: .rateLimitOptions.exceedAction, enforceOnKey: .rateLimitOptions.enforceOnKey, banDuration: .rateLimitOptions.banDurationSec}]'
```

### 5. Policy Attachment and Coverage

```bash
# Which backend services have security policies
get_backend_services

# Backend services WITHOUT security policies (unprotected)
gcloud compute backend-services list --format=json \
  | jq '[.[] | select(.securityPolicy == null) | {name: .name, protocol: .protocol, backends: [.backends[]?.group | split("/") | last]}]'

# Edge security policies
gcloud compute security-policies list --filter="type=CLOUD_ARMOR_EDGE" --format=json \
  | jq '[.[] | {name: .name, ruleCount: .rules | length}]'
```

## Output Format

Present results as a structured report:
```
Gcp Cloud Armor Report
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

1. **Preview mode**: Rules in preview mode (`preview: true`) log matches but do not enforce. Always check preview status before assuming protection.
2. **Rule priority ordering**: Lower priority number = higher precedence. The default rule (priority 2147483647) is always last. Ensure custom rules have appropriate priorities.
3. **CEL expression limits**: Custom CEL expressions have complexity limits. Overly complex expressions cause policy update failures.
4. **Rate limiting granularity**: `enforceOnKey` determines rate limit scope (IP, header, etc.). Without it, rate limiting applies globally, not per-client.
5. **Adaptive protection delay**: Adaptive protection needs traffic baseline data. New policies may not generate alerts for the first 24-48 hours.

---
name: managing-aws-cloudfront-deep
description: |
  Use when working with Aws Cloudfront Deep — advanced AWS CloudFront management
  covering distribution lifecycle, behavior configuration, Lambda@Edge
  functions, origin groups for failover, real-time logs, field-level encryption,
  and cache policy optimization. Use for deep CloudFront troubleshooting,
  performance tuning, advanced origin configuration, or Lambda@Edge debugging.
connection_type: aws
preload: false
---

# AWS CloudFront Deep Skill

Advanced CloudFront management including Lambda@Edge, origin groups, cache policies, and real-time monitoring.

## Core Helper Functions

```bash
#!/bin/bash
export AWS_PAGER=""

# Get distribution config
cf_config() {
    local dist_id="$1"
    aws cloudfront get-distribution-config --id "$dist_id" --output json
}

# Get CloudFront metrics
cf_metric() {
    local dist_id="$1" metric="$2" stat="${3:-Average}" days="${4:-7}"
    local end_time start_time
    end_time=$(date -u +"%Y-%m-%dT%H:%M:%S")
    start_time=$(date -u -d "$days days ago" +"%Y-%m-%dT%H:%M:%S" 2>/dev/null || date -u -v-${days}d +"%Y-%m-%dT%H:%M:%S")
    aws cloudwatch get-metric-statistics \
        --namespace AWS/CloudFront --metric-name "$metric" \
        --dimensions Name=DistributionId,Value="$dist_id" Name=Region,Value=Global \
        --start-time "$start_time" --end-time "$end_time" \
        --period $((days * 86400)) --statistics "$stat" \
        --output text --query 'Datapoints[0].'$stat
}
```

## MANDATORY: Discovery-First Pattern

### Phase 1: Discovery

```bash
#!/bin/bash
export AWS_PAGER=""

echo "=== Distribution Inventory ==="
aws cloudfront list-distributions --output json | jq -r '
    .DistributionList.Items[] | "\(.Id)\t\(.DomainName)\t\(.Status)\t\(.Enabled)\t\(.PriceClass)\t\(.Origins.Quantity) origins"
' | column -t | head -20

echo ""
echo "=== Cache Policies ==="
aws cloudfront list-cache-policies --output json | jq -r '
    .CachePolicyList.Items[] | "\(.CachePolicy.Id[:12])\t\(.CachePolicy.CachePolicyConfig.Name)\t\(.CachePolicy.CachePolicyConfig.DefaultTTL)s TTL"
' | column -t | head -10

echo ""
echo "=== Origin Request Policies ==="
aws cloudfront list-origin-request-policies --output json | jq -r '
    .OriginRequestPolicyList.Items[] | "\(.OriginRequestPolicy.Id[:12])\t\(.OriginRequestPolicy.OriginRequestPolicyConfig.Name)"
' | column -t | head -10

echo ""
echo "=== Functions ==="
aws cloudfront list-functions --output json 2>/dev/null | jq -r '
    .FunctionList.Items[]? | "\(.Name)\t\(.FunctionConfig.Runtime)\t\(.Status)\t\(.FunctionMetadata.Stage)"
' | column -t | head -10
```

### Phase 2: Analysis

```bash
#!/bin/bash
export AWS_PAGER=""
DIST_ID="${1:?Distribution ID required}"

echo "=== Performance Metrics (7d) ==="
for metric in CacheHitRate Requests 4xxErrorRate 5xxErrorRate BytesDownloaded; do
    val=$(cf_metric "$DIST_ID" "$metric")
    printf "%s: %s\n" "$metric" "${val:-N/A}"
done

echo ""
echo "=== Behavior Configuration ==="
cf_config "$DIST_ID" | jq '
    .DistributionConfig.CacheBehaviors.Items[]? | {
        PathPattern, ViewerProtocolPolicy, AllowedMethods: .AllowedMethods.Items,
        CachePolicyId: .CachePolicyId[:12], Compress
    }' | head -30

echo ""
echo "=== Origin Groups (Failover) ==="
cf_config "$DIST_ID" | jq '
    .DistributionConfig.OriginGroups.Items[]? | {
        Id, Members: [.Members.Items[].OriginId],
        FailoverCodes: .FailoverCriteria.StatusCodes.Items
    }'

echo ""
echo "=== Lambda@Edge Associations ==="
cf_config "$DIST_ID" | jq '
    [.DistributionConfig | .DefaultCacheBehavior, .CacheBehaviors.Items[]?] |
    .[] | select(.LambdaFunctionAssociations.Quantity > 0) |
    .LambdaFunctionAssociations.Items[] | {EventType, LambdaFunctionARN: .LambdaFunctionARN[-40:]}
' | head -20
```

## Output Rules
- **TOKEN EFFICIENCY**: Target <=50 lines per output
- Use parallel execution with `&` and `wait` for multi-distribution queries
- CloudFront API calls must go through us-east-1

## Safety Rules
- **Read-only by default**: Use list/get/describe for inspection
- **Distribution updates take 15-20 min** to deploy globally
- **Never delete distributions** without disabling first and confirming
- **Lambda@Edge changes** propagate to all edge locations -- test thoroughly

## Output Format

Present results as a structured report:
```
Managing Aws Cloudfront Deep Report
═══════════════════════════════════
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
- **All API calls route to us-east-1** regardless of configured region
- **CacheHitRate is 0-100** not 0-1; do not multiply by 100
- **Invalidation costs**: First 1000 paths/month free, then $0.005/path
- **Origin groups require two origins** and specific failover status codes
- **Cache policy vs legacy settings**: New distributions should use managed cache policies

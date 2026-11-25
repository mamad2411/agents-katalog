# Skill: CDN Troubleshooting

## Purpose

Diagnose and resolve CDN/edge networking issues including cache misses, origin failures, TLS problems, latency issues, purge failures, and routing anomalies. Provides systematic diagnostic workflows with provider-specific tools and commands.

## Core Knowledge

### Cache Miss Analysis

#### Understanding X-Cache Headers

| Provider | Header | Values |
|----------|--------|--------|
| Azure Front Door | `X-Cache` | `TCP_HIT`, `TCP_MISS`, `TCP_REMOTE_HIT`, `TCP_PARTIAL_HIT`, `PRIVATE_NOSTORE`, `CONFIG_NOCACHE` |
| AWS CloudFront | `X-Cache` | `Hit from cloudfront`, `Miss from cloudfront`, `RefreshHit from cloudfront`, `Error from cloudfront` |
| GCP Cloud CDN | `cdn-cache-status` (in logs) | `hit`, `miss`, `revalidated`, `stale`, `denied` |
| Cloudflare | `cf-cache-status` | `HIT`, `MISS`, `EXPIRED`, `STALE`, `BYPASS`, `DYNAMIC`, `REVALIDATED` |

#### Diagnostic Flow for Cache Misses

```
Cache Miss?
├── Check Cache-Control header from origin
│   ├── no-store/no-cache/private → Origin not allowing cache
│   ├── max-age=0 → Immediate expiry
│   └── OK (public, max-age>0)
├── Check Vary header
│   ├── Vary: * → Uncacheable
│   ├── Vary: Cookie → Likely destroying hit ratio
│   └── Vary: Accept-Encoding → Normal
├── Check query string handling
│   ├── Unique query params per request (timestamps, nonces)
│   └── CDN including all query strings in cache key
├── Check request method
│   ├── POST/PUT/DELETE → Not cached
│   └── GET/HEAD → Should be cached
├── Check Set-Cookie in response
│   └── Some CDNs skip cache if Set-Cookie present
└── Check content size
    └── Some CDNs have minimum/maximum cacheable size
```

#### Commands for Cache Analysis

**Azure Front Door:**
```bash
# Check response headers
curl -sI "https://myapp.azurefd.net/static/app.js" | grep -i "x-cache\|cache-control\|age\|x-azure"

# Expected HIT response:
# X-Cache: TCP_HIT
# Age: 3245
# X-Azure-Ref: 0abc123...

# Log Analytics query for cache stats
az monitor log-analytics query \
  --workspace <workspace-id> \
  --analytics-query "
    AzureDiagnostics
    | where Category == 'FrontDoorAccessLog'
    | where TimeGenerated > ago(1h)
    | summarize count() by cacheStatus_s
    | order by count_ desc
  "
```

**AWS CloudFront:**
```bash
# Check response headers
curl -sI "https://d111111abcdef8.cloudfront.net/static/app.js" \
  | grep -i "x-cache\|x-amz-cf-pop\|x-amz-cf-id\|age\|cache-control"

# Expected HIT:
# X-Cache: Hit from cloudfront
# X-Amz-Cf-Pop: IAD89-C3
# Age: 1234

# Enable real-time logs for debugging
aws cloudfront create-realtime-log-config \
  --name debug-cache \
  --sampling-rate 100 \
  --fields "timestamp" "c-ip" "cs-uri-stem" "x-edge-result-type" "x-edge-response-result-type" \
  --end-points '{
    "StreamType": "Kinesis",
    "KinesisStreamConfig": {
      "RoleARN": "arn:aws:iam::123456789012:role/cf-realtime-log-role",
      "StreamARN": "arn:aws:kinesis:us-east-1:123456789012:stream/cf-logs"
    }
  }'
```

**GCP Cloud CDN:**
```bash
# Check via Cloud Logging
gcloud logging read '
  resource.type="http_load_balancer"
  AND httpRequest.requestUrl:"static/app.js"
  AND jsonPayload.statusDetails!=""
' --limit=10 --format="table(
  timestamp,
  jsonPayload.statusDetails,
  jsonPayload.cacheHit,
  jsonPayload.cacheLookup,
  jsonPayload.cacheFillBytes
)"

# Cache hit/miss fields in logs:
# jsonPayload.cacheHit: true/false
# jsonPayload.cacheLookup: true (CDN attempted lookup)
# jsonPayload.cacheFillBytes: bytes fetched from origin (>0 = miss)
```

### Origin Health and Failover Issues

#### Symptoms
- Elevated 502/503/504 errors
- Intermittent timeouts
- Failover not triggering
- Unexpected origin selection

#### Diagnostic Steps

**1. Verify origin reachability from CDN:**
```bash
# Azure Front Door — check origin health via portal or CLI
az afd origin show \
  --resource-group myRG \
  --profile-name myFD \
  --origin-group-name myOG \
  --origin-name primary-origin \
  --query "{state:enabledState, health:properties.healthState}"

# Test origin directly (bypass CDN)
curl -sI "https://webapp-eastus.azurewebsites.net/health" \
  -H "Host: webapp-eastus.azurewebsites.net" \
  --resolve "webapp-eastus.azurewebsites.net:443:20.1.2.3"
```

**2. Check health probe configuration:**
```bash
# Common issues:
# - Probe path returns non-2xx (forgot /health endpoint)
# - Probe interval too aggressive (origin overwhelmed)
# - Origin firewall blocking CDN probe IPs
# - Probe using HTTP but origin requires HTTPS
# - Host header mismatch

# Azure — list health probe settings
az afd origin-group show \
  --resource-group myRG \
  --profile-name myFD \
  --origin-group-name myOG \
  --query healthProbeSettings
```

**3. AWS CloudFront origin failover debug:**
```bash
# Check origin group configuration
aws cloudfront get-distribution --id E1A2B3C4D5E6F7 \
  --query 'Distribution.DistributionConfig.OriginGroups'

# CloudFront failover triggers on: 500, 502, 503, 504, or connection timeout
# Does NOT trigger on: 400, 401, 403, 404 (these are forwarded to client)

# Check CloudFront error rate metrics
aws cloudwatch get-metric-statistics \
  --namespace AWS/CloudFront \
  --metric-name 5xxErrorRate \
  --dimensions Name=DistributionId,Value=E1A2B3C4D5E6F7 \
  --start-time $(date -u -d '1 hour ago' +%Y-%m-%dT%H:%M:%S) \
  --end-time $(date -u +%Y-%m-%dT%H:%M:%S) \
  --period 300 \
  --statistics Average
```

### TLS / Certificate Problems

#### Common Issues

| Issue | Symptom | Resolution |
|-------|---------|------------|
| Certificate expired | ERR_CERT_DATE_INVALID | Renew cert, check auto-renewal |
| CN/SAN mismatch | ERR_CERT_COMMON_NAME_INVALID | Add correct domain to SAN |
| Intermediate cert missing | Works in some browsers, fails in others | Include full chain |
| TLS version mismatch | Handshake failure | Check minimum TLS version on CDN |
| OCSP stapling failure | Slow TLS handshake | Enable OCSP stapling |
| Mixed content | Partial page load | Ensure all resources use HTTPS |

#### Diagnostic Commands

```bash
# Check certificate presented by CDN edge
openssl s_client -connect myapp.azurefd.net:443 -servername myapp.azurefd.net </dev/null 2>/dev/null \
  | openssl x509 -noout -dates -subject -issuer -ext subjectAltName

# Check full certificate chain
openssl s_client -connect myapp.azurefd.net:443 -servername myapp.azurefd.net -showcerts </dev/null 2>/dev/null

# Verify TLS version and cipher
curl -v --tlsv1.2 "https://myapp.azurefd.net/" 2>&1 | grep -E "SSL connection|subject:|issuer:"

# Check for HTTP/2 and HTTP/3 support
curl -sI --http2 "https://myapp.azurefd.net/" | grep -i "^http/"
curl -sI --http3 "https://myapp.azurefd.net/" | grep -i "^http/"  # requires curl 7.66+

# Test OCSP stapling
openssl s_client -connect myapp.azurefd.net:443 -servername myapp.azurefd.net -status </dev/null 2>/dev/null \
  | grep -A5 "OCSP Response Status"
```

**Azure Front Door certificate troubleshooting:**
```bash
# Check custom domain TLS state
az afd custom-domain show \
  --resource-group myRG \
  --profile-name myFD \
  --custom-domain-name "www-example-com" \
  --query "{state:tlsSettings.certificateType, validationState:validationProperties.validationToken}"

# AFD managed cert validation requires CNAME:
# _dnsauth.www.example.com → <token>.azurefd.net
```

### Latency Debugging

#### TTFB Breakdown

```
Total TTFB = DNS + TCP + TLS + Edge Processing + Origin Fetch (if miss)

┌──────┬──────┬──────┬────────────────┬────────────────────┐
│ DNS  │ TCP  │ TLS  │ Edge (WAF,     │ Origin (if cache   │
│      │      │      │  rules, cache  │  miss/expired)     │
│      │      │      │  lookup)       │                    │
└──────┴──────┴──────┴────────────────┴────────────────────┘
```

**Measure with curl:**
```bash
curl -w @- -o /dev/null -s "https://myapp.azurefd.net/api/data" <<'EOF'
    DNS:        %{time_namelookup}s
    TCP:        %{time_connect}s
    TLS:        %{time_appconnect}s
    TTFB:       %{time_starttransfer}s
    Total:      %{time_total}s
    Size:       %{size_download} bytes
    HTTP Code:  %{http_code}
    Remote IP:  %{remote_ip}
EOF
```

**Expected results (cache hit from nearby POP):**
```
DNS:        0.012s
TCP:        0.025s
TLS:        0.055s
TTFB:       0.065s    ← Only ~10ms edge processing
Total:      0.070s
```

**Slow results (cache miss, origin in distant region):**
```
DNS:        0.012s
TCP:        0.025s
TLS:        0.055s
TTFB:       0.350s    ← 295ms origin fetch time
Total:      0.500s
```

#### Provider-Specific Latency Headers

**Azure Front Door:**
```
X-Azure-Ref: 0abc123...  (use for support cases)
X-Azure-RequestId: ...    (track request through pipeline)
```

**AWS CloudFront:**
```
X-Amz-Cf-Pop: IAD89-C3   (POP identifier: airport code + node)
X-Amz-Cf-Id: abc123...   (request trace ID)
Via: 1.1 abc123.cloudfront.net (CloudFront)
```

**GCP:**
```
Via: 1.1 google            (served through Google's network)
Server-Timing: cdn-cache;desc=hit  (cache status as Server-Timing)
```

#### Latency Troubleshooting Tree

```
High TTFB?
├── DNS slow (>50ms)
│   └── Check DNS resolution, TTL, provider
├── TLS slow (>100ms)
│   ├── Check cipher suite selection
│   ├── Check OCSP stapling
│   └── Consider 0-RTT (TLS 1.3) / HTTP/3
├── Edge processing slow
│   ├── Complex WAF rules evaluation
│   ├── Large Rules Engine rule sets
│   └── Edge compute function timeout
└── Origin slow (high TTFB on miss)
    ├── Origin application slow
    ├── Origin geographically distant (enable origin shield)
    ├── Connection pool exhaustion (keepalive)
    └── Cold start (serverless origin)
```

### Purge/Invalidation Not Taking Effect

#### Common Causes

1. **TTL not expired on edge** — Purge reaches some POPs but not all (propagation delay)
2. **Browser cache** — Content cached locally (user needs hard refresh)
3. **Intermediate caches** — ISP/corporate proxies caching stale content
4. **Wrong purge path** — Case sensitivity, missing query string
5. **DNS cache** — Client resolving to old IP after CDN change
6. **Cache key mismatch** — Purging `/path` but content cached as `/path?v=1`

#### Diagnostic Steps

```bash
# 1. Verify purge was accepted
# Azure
az afd endpoint purge --resource-group myRG --profile-name myFD \
  --endpoint-name ep1 --content-paths "/index.html" --no-wait

# 2. Wait for propagation (typically 2-60 seconds)
sleep 10

# 3. Test from multiple locations (bypass local cache)
curl -sI "https://myapp.azurefd.net/index.html" \
  -H "Cache-Control: no-cache" \
  -H "Pragma: no-cache" \
  | grep -i "x-cache\|age\|last-modified\|etag"

# 4. If still hitting cache, test with unique query param
curl -sI "https://myapp.azurefd.net/index.html?purge-test=$(date +%s)" \
  | grep -i "x-cache"
# If this returns MISS but original returns HIT → cache key includes query string

# 5. Check purge status (AWS)
aws cloudfront get-invalidation \
  --distribution-id E1A2B3C4D5E6F7 \
  --id I1234567890ABC
# Status: InProgress → still propagating
# Status: Completed → should be effective

# 6. Test from different POPs using DNS resolution to specific edge
# Azure POPs can be tested via different geographic curl endpoints
# AWS — use CloudFront Functions to add POP header for verification
```

### Routing Issues (Wrong POP, Unexpected Routing)

#### Symptoms
- Traffic routed to distant POP (high latency)
- Geographic routing not working (wrong origin selected)
- After failover, traffic not returning to primary

#### Diagnostic Steps

```bash
# 1. Identify which POP is serving the request
curl -sI "https://myapp.azurefd.net/" | grep -i "x-amz-cf-pop\|x-azure-ref\|x-served-by\|cf-ray"

# Azure Front Door: X-Azure-Ref contains POP info (encoded)
# CloudFront: X-Amz-Cf-Pop = airport code (IAD, AMS, NRT)
# Cloudflare: CF-Ray: abc123-IAD (last 3 chars = POP code)

# 2. Check DNS resolution (is anycast routing correctly?)
nslookup myapp.azurefd.net
# Should resolve to Front Door anycast IP

dig +short myapp.azurefd.net
# Multiple IPs = anycast addresses

# 3. Traceroute to CDN to verify path
traceroute -n myapp.azurefd.net
# Look for geographic hops that indicate routing to distant POP

# 4. Test from multiple locations (use online tools)
# Azure: Network Watcher Connection Monitor
# AWS: CloudFront real-time logs with c-ip and x-edge-location
# Tools: KeyCDN Tools, CDN Planet, Pingdom

# 5. Check if ISP/corporate network has broken BGP routing
# Anycast depends on correct BGP announcements
# Check BGP looking glass: bgp.he.net, stat.ripe.net
```

**Azure Front Door routing debug:**
```bash
# Check effective routing rules
az afd route list \
  --resource-group myRG \
  --profile-name myFD \
  --endpoint-name myEndpoint \
  --query "[].{name:name, patterns:patternsToMatch, origin:originGroup.id}"

# Check origin group health
az afd origin-group list \
  --resource-group myRG \
  --profile-name myFD \
  --query "[].{name:name, probes:healthProbeSettings, lb:loadBalancingSettings}"
```

**AWS CloudFront routing debug:**
```bash
# List all behaviors (routing rules) for distribution
aws cloudfront get-distribution-config --id E1A2B3C4D5E6F7 \
  --query 'DistributionConfig.CacheBehaviors.Items[].{path:PathPattern,origin:TargetOriginId}'

# Check if CloudFront is using expected POP
# Real-time logs field: x-edge-location
```

### Diagnostic Tools by Provider

#### Azure Front Door

| Tool | Purpose |
|------|---------|
| Azure Monitor / Log Analytics | Access logs, WAF logs, health probe logs |
| Front Door diagnostics blade | Built-in troubleshooting |
| Network Watcher | Connectivity from Azure VMs |
| `az afd` CLI | Configuration inspection |
| `X-Azure-Ref` header | Support case correlation |

```kusto
// Log Analytics: Top cache miss URLs
AzureDiagnostics
| where Category == "FrontDoorAccessLog"
| where cacheStatus_s == "MISS"
| summarize MissCount=count() by requestUri_s
| top 20 by MissCount
| project requestUri_s, MissCount

// Log Analytics: Slow requests (TTFB > 1s)
AzureDiagnostics
| where Category == "FrontDoorAccessLog"
| where timeTaken_d > 1000
| project TimeGenerated, requestUri_s, timeTaken_d,
    httpStatusCode_d, cacheStatus_s, pop_s
| order by timeTaken_d desc
| take 50

// Log Analytics: WAF blocks
AzureDiagnostics
| where Category == "FrontDoorWebApplicationFirewallLog"
| where action_s == "Block"
| summarize BlockCount=count() by ruleName_s, clientIP_s
| top 20 by BlockCount
```

#### AWS CloudFront

| Tool | Purpose |
|------|---------|
| CloudWatch Metrics | Error rates, cache hit ratio, requests, bytes |
| Real-time logs | Per-request debugging (Kinesis) |
| Standard logs (S3) | Batch analysis, compliance |
| CloudFront Functions console | Test functions in isolation |
| AWS WAF sampled requests | View blocked/allowed request details |

```bash
# Key CloudWatch metrics
aws cloudwatch get-metric-data --cli-input-json '{
  "MetricDataQueries": [
    {"Id": "hits", "MetricStat": {"Metric": {"Namespace": "AWS/CloudFront", "MetricName": "CacheHitRate", "Dimensions": [{"Name": "DistributionId", "Value": "E1A2B3C4D5E6F7"}]}, "Period": 300, "Stat": "Average"}},
    {"Id": "errors", "MetricStat": {"Metric": {"Namespace": "AWS/CloudFront", "MetricName": "5xxErrorRate", "Dimensions": [{"Name": "DistributionId", "Value": "E1A2B3C4D5E6F7"}]}, "Period": 300, "Stat": "Average"}},
    {"Id": "latency", "MetricStat": {"Metric": {"Namespace": "AWS/CloudFront", "MetricName": "OriginLatency", "Dimensions": [{"Name": "DistributionId", "Value": "E1A2B3C4D5E6F7"}]}, "Period": 300, "Stat": "p99"}}}
  ],
  "StartTime": "2024-01-01T00:00:00Z",
  "EndTime": "2024-01-01T01:00:00Z"
}'
```

#### GCP Cloud CDN

| Tool | Purpose |
|------|---------|
| Cloud Logging | Per-request logs with cache status |
| Cloud Monitoring | Dashboards, alerting |
| Network Intelligence Center | Traffic visualization |
| `gcloud compute` CLI | Configuration inspection |

```bash
# Cache hit ratio over last hour
gcloud logging read '
  resource.type="http_load_balancer"
  AND timestamp>="2024-01-01T00:00:00Z"
' --limit=1000 --format=json \
  | jq '[.[] | .jsonPayload.cacheHit] | {total: length, hits: [.[] | select(. == true)] | length}'

# Requests by cache status
gcloud logging read '
  resource.type="http_load_balancer"
' --limit=1000 --format="value(jsonPayload.statusDetails)" | sort | uniq -c | sort -rn
```

### Quick Reference: Troubleshooting Checklist

```
□ 1. Reproduce the issue (specific URL, time, location)
□ 2. Check response headers (X-Cache, Cache-Control, Age)
□ 3. Verify CDN configuration (routes, behaviors, cache policies)
□ 4. Check origin health (probes, direct access)
□ 5. Review logs (access logs, WAF logs, error logs)
□ 6. Test from multiple locations/POPs
□ 7. Check DNS resolution chain
□ 8. Verify TLS certificate validity
□ 9. Compare expected vs actual cache key
□ 10. Check for recent config changes (deployment, purge, rule update)
```

---

**Analysis only — verify against vendor documentation before applying.**

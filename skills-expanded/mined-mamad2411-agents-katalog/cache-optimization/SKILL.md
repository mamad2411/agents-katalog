# Skill: Cache Optimization

## Purpose

Design and optimize caching strategies at the CDN edge to maximize cache hit ratio, minimize origin load, and deliver content with minimal latency. Covers cache key design, TTL strategies, invalidation patterns, compression, and streaming optimization.

## Core Knowledge

### Cache-Control Headers

The `Cache-Control` response header is the primary mechanism for controlling CDN and browser caching:

```
Cache-Control: public, max-age=31536000, immutable
               │       │                  │
               │       │                  └─ Don't revalidate on navigation
               │       └─ Cache for 1 year
               └─ CDN and browser may cache
```

**Key directives:**

| Directive | Meaning | Use Case |
|-----------|---------|----------|
| `public` | Any cache (CDN, proxy, browser) may store | Static assets, public pages |
| `private` | Only browser may cache (not CDN) | User-specific content |
| `no-cache` | Must revalidate before using cached copy | Frequently updated HTML |
| `no-store` | Never cache | Sensitive data (banking, PII) |
| `max-age=N` | Fresh for N seconds | All cacheable content |
| `s-maxage=N` | CDN-specific max-age (overrides max-age for shared caches) | CDN-specific TTL |
| `stale-while-revalidate=N` | Serve stale while revalidating in background | Non-critical freshness |
| `stale-if-error=N` | Serve stale if origin returns 5xx | Availability over freshness |
| `immutable` | Never revalidate (content never changes at this URL) | Fingerprinted assets |
| `must-revalidate` | Don't serve stale, ever | Financial data, inventory |

**Recommended patterns:**

```
# Fingerprinted static assets (app.a1b2c3.js)
Cache-Control: public, max-age=31536000, immutable

# HTML pages (may change frequently)
Cache-Control: public, max-age=0, must-revalidate
# or
Cache-Control: public, max-age=60, stale-while-revalidate=600

# API responses (user-specific)
Cache-Control: private, max-age=0, no-cache

# Images (moderate TTL)
Cache-Control: public, max-age=86400, stale-while-revalidate=604800

# Versioned API (stable within version)
Cache-Control: public, s-maxage=3600, max-age=60, stale-while-revalidate=86400
```

### Vary Header Handling

The `Vary` header tells caches to store separate copies for different request header values:

```
Vary: Accept-Encoding, Accept-Language
```

**Impact on cache efficiency:**
- Each unique combination of Vary header values = separate cache entry
- `Vary: *` = never cache (effectively `no-store`)
- `Vary: Accept-Encoding` is standard and expected (gzip vs br vs none)
- `Vary: Cookie` = cache per unique cookie value (usually destroys hit ratio)
- `Vary: User-Agent` = thousands of variants (avoid! use `Vary: Accept` for content negotiation instead)

**Best practices:**
- Minimize Vary headers — each one multiplies cache entries
- Use `Vary: Accept-Encoding` (handled automatically by most CDNs)
- For device-specific content, use CloudFront device headers (`CloudFront-Is-Mobile-Viewer`) rather than `Vary: User-Agent`
- For language, use `Vary: Accept-Language` only if you serve different content per language from the same URL

### Cache Key Design

The cache key determines what constitutes a "unique" cached object. Default: `scheme + host + path`.

**Additional cache key components:**

| Component | Include When | Impact |
|-----------|-------------|--------|
| Query strings | Different content per query param | Higher miss ratio if many unique params |
| Headers | Content negotiation (Accept, Accept-Language) | Multiplies cache entries |
| Cookies | User segmentation at edge | Typically destroys cache ratio |
| Device type | Different content per device | 2–3x entries (mobile/tablet/desktop) |
| Protocol | Different response per HTTP vs HTTPS | Rare in practice |

#### Azure Front Door Cache Key

```bicep
resource route 'Microsoft.Cdn/profiles/afdEndpoints/routes@2023-05-01' = {
  properties: {
    cacheConfiguration: {
      compressionSettings: {
        isCompressionEnabled: true
        contentTypesToCompress: [
          'text/html'
          'text/css'
          'application/javascript'
          'application/json'
        ]
      }
      queryStringCachingBehavior: 'IncludeSpecifiedQueryStrings'
      queryParameters: 'version,locale'  // Only these affect cache key
    }
  }
}
```

#### AWS CloudFront Cache Policy

```json
{
  "CachePolicyConfig": {
    "Name": "OptimizedCachePolicy",
    "DefaultTTL": 86400,
    "MaxTTL": 31536000,
    "MinTTL": 0,
    "ParametersInCacheKeyAndForwardedToOrigin": {
      "EnableAcceptEncodingGzip": true,
      "EnableAcceptEncodingBrotli": true,
      "HeadersConfig": {
        "HeaderBehavior": "whitelist",
        "Headers": {
          "Items": ["Accept-Language"],
          "Quantity": 1
        }
      },
      "CookiesConfig": {
        "CookieBehavior": "whitelist",
        "Cookies": {
          "Items": ["session_variant"],
          "Quantity": 1
        }
      },
      "QueryStringsConfig": {
        "QueryStringBehavior": "whitelist",
        "QueryStrings": {
          "Items": ["v", "w", "h", "q"],
          "Quantity": 4
        }
      }
    }
  }
}
```

#### GCP Cloud CDN Cache Key Policy

```bash
gcloud compute backend-services update my-backend \
  --cache-key-policy-include-protocol=false \
  --cache-key-policy-include-host=true \
  --cache-key-policy-include-query-string=true \
  --cache-key-policy-query-string-whitelist="version,locale" \
  --cache-key-policy-include-named-cookies="variant" \
  --cache-key-policy-include-http-headers="Accept-Language" \
  --global
```

### TTL Strategies by Content Type

| Content Type | Recommended TTL | Strategy |
|-------------|-----------------|----------|
| Fingerprinted assets (JS/CSS with hash) | 1 year (31536000s) | immutable, cache-bust via filename |
| Images/media | 1 day – 1 week | Moderate TTL + stale-while-revalidate |
| HTML pages | 0 – 5 min | Short TTL or revalidation |
| API responses (public) | 10s – 5 min | s-maxage + stale-while-revalidate |
| API responses (user) | 0 (private) | no-cache or private |
| Fonts | 1 year | Immutable, served with CORS |
| Video/HLS manifests | 1 – 6s | Very short (live), long (VOD) |
| Video/HLS segments | 1 year (VOD), 60s (live) | Segments never change once written |
| JSON config/feature flags | 30 – 60s | Short TTL for quick updates |

### Cache Purge / Invalidation Patterns

#### Azure Front Door

```bash
# Purge specific paths
az afd endpoint purge \
  --resource-group myRG \
  --profile-name myFD \
  --endpoint-name myEndpoint \
  --content-paths "/css/*" "/js/app.*.js" "/index.html"

# Purge all content
az afd endpoint purge \
  --resource-group myRG \
  --profile-name myFD \
  --endpoint-name myEndpoint \
  --content-paths "/*"
```

#### AWS CloudFront

```bash
# Create invalidation
aws cloudfront create-invalidation \
  --distribution-id E1A2B3C4D5E6F7 \
  --paths "/images/*" "/index.html" "/api/config.json"

# Check invalidation status
aws cloudfront get-invalidation \
  --distribution-id E1A2B3C4D5E6F7 \
  --id I1A2B3C4D5E6F7

# Note: First 1,000 paths/month free, then $0.005/path
# Wildcard (*) counts as one path
```

#### GCP Cloud CDN

```bash
# Invalidate by URL pattern
gcloud compute url-maps invalidate-cdn-cache cdn-url-map \
  --path="/static/*" \
  --global

# Invalidate by tag (requires cache tags in response)
gcloud compute url-maps invalidate-cdn-cache cdn-url-map \
  --tags="product-123,homepage" \
  --global
```

**Invalidation best practices:**
1. **Prefer cache-busting over purging** — Use content-addressable URLs (`app.abc123.js`)
2. **Purge surgically** — Wildcard `/*` purges are expensive (origin thundering herd)
3. **Batch purges** — Collect paths, purge once (not per-deploy file)
4. **Use tags/keys** — Tag responses for group invalidation (GCP supports this natively)
5. **Warm after purge** — Pre-fetch critical paths after purging to avoid cold cache

### Stale-While-Revalidate (SWR) and Stale-If-Error

```
Cache-Control: public, max-age=60, stale-while-revalidate=3600, stale-if-error=86400
                       │              │                           │
                       │              │                           └─ Serve stale up to 1 day
                       │              │                               if origin returns 5xx
                       │              └─ After 60s, serve stale and revalidate in background
                       │                  (for up to 1 hour after expiry)
                       └─ Fresh for 60 seconds
```

**Timeline:**
```
0s ────── 60s ────── 3660s ────── 86460s
│  FRESH  │   SWR    │    ERROR   │  MUST REVALIDATE
│         │  (stale  │   (stale   │  (or fetch new)
│         │   OK)    │    OK if   │
│         │          │    error)  │
```

**Provider support:**
- Azure Front Door: Honors origin SWR headers ✓
- AWS CloudFront: Honors SWR and stale-if-error ✓
- GCP Cloud CDN: Honors SWR (serve-while-stale setting) ✓
- Cloudflare: Full support ✓

### Compression at the Edge

#### Supported algorithms:

| Algorithm | Ratio | Speed | Support |
|-----------|-------|-------|---------|
| gzip | Good (~70%) | Fast | Universal |
| Brotli (br) | Better (~80%) | Slower compress, fast decompress | All modern browsers |
| zstd | Best (~85%) | Fast | Emerging (Chrome 123+) |

#### Configuration:

**Azure Front Door:**
```bicep
cacheConfiguration: {
  compressionSettings: {
    isCompressionEnabled: true
    contentTypesToCompress: [
      'text/html'
      'text/css'
      'text/javascript'
      'application/javascript'
      'application/json'
      'application/xml'
      'image/svg+xml'
      'font/woff2'  // Already compressed, skip
    ]
  }
}
```

**AWS CloudFront:** Enable `Compress: true` on cache behaviors (automatic gzip + Brotli based on `Accept-Encoding`).

**GCP Cloud CDN:**
```bash
gcloud compute backend-services update my-backend \
  --compression-mode=AUTOMATIC \
  --global
```

**Do NOT compress:**
- Images (JPEG, PNG, WebP — already compressed)
- Video (MP4, WebM — already compressed)
- Fonts (WOFF2 — already Brotli compressed)
- Archives (ZIP, tar.gz)

### Video/Streaming Optimization

#### Byte-Range Requests

CDN must support splitting large files into byte ranges for video seeking:

```
Client: GET /video.mp4
        Range: bytes=1048576-2097151

CDN: 206 Partial Content
     Content-Range: bytes 1048576-2097151/104857600
     Content-Length: 1048576
```

**CDN configuration for byte-range:**
- Azure Front Door: Supports byte-range by default; origin must support it
- CloudFront: Forwards Range header to origin; caches partial responses
- Cloud CDN: Byte-range caching supported with proper origin headers

#### HLS/DASH Streaming

```
┌────────┐    ┌─────────┐    ┌──────────┐    ┌────────────────┐
│ Player │───▶│  CDN    │───▶│ Packager │───▶│ Media Storage  │
│        │    │         │    │ (origin) │    │ (S3/Blob/GCS)  │
└────────┘    └─────────┘    └──────────┘    └────────────────┘
    │              │
    │  1. Request manifest (.m3u8/.mpd)
    │  2. Parse manifest, request segments (.ts/.m4s)
    │  3. CDN caches segments with long TTL
```

**Cache settings for streaming:**
```
# HLS manifest (live) — very short TTL
*.m3u8 → Cache-Control: public, max-age=2, stale-while-revalidate=1

# HLS manifest (VOD) — moderate TTL
*.m3u8 → Cache-Control: public, max-age=3600

# Media segments — immutable once created
*.ts, *.m4s → Cache-Control: public, max-age=31536000, immutable

# DASH manifest (live)
*.mpd → Cache-Control: public, max-age=2
```

## Cache Hit Ratio Optimization Checklist

1. **Normalize cache keys** — Sort query parameters, lowercase paths
2. **Minimize Vary headers** — Only Accept-Encoding if possible
3. **Use s-maxage** — Longer CDN TTL, shorter browser TTL
4. **Enable SWR** — Serve stale during revalidation
5. **Fingerprint static assets** — Allow immutable caching
6. **Strip tracking parameters** — Remove utm_*, fbclid from cache key
7. **Origin Shield** — Reduce origin requests from multiple POPs
8. **Pre-warm cache** — Fetch critical paths after deploy/purge
9. **Avoid cache-busting cookies** — Don't send session cookies to CDN
10. **Monitor hit ratio** — Target >90% for static, >60% for dynamic

## Provider-Specific Metrics

**Azure Front Door:**
```kusto
// Cache hit ratio in Log Analytics
AzureDiagnostics
| where Category == "FrontDoorAccessLog"
| summarize
    TotalRequests = count(),
    CacheHits = countif(cacheStatus_s in ("HIT", "PARTIAL_HIT", "REMOTE_HIT")),
    CacheMisses = countif(cacheStatus_s == "MISS")
    by bin(TimeGenerated, 1h)
| extend HitRatio = round(100.0 * CacheHits / TotalRequests, 2)
```

**AWS CloudFront:**
```bash
# Get cache statistics (real-time monitoring)
aws cloudfront get-distribution --id E1A2B3C4D5E6F7 --query 'Distribution.Status'

# CloudWatch metrics
aws cloudwatch get-metric-statistics \
  --namespace AWS/CloudFront \
  --metric-name CacheHitRate \
  --dimensions Name=DistributionId,Value=E1A2B3C4D5E6F7 \
  --start-time 2024-01-01T00:00:00Z \
  --end-time 2024-01-02T00:00:00Z \
  --period 3600 \
  --statistics Average
```

**GCP Cloud CDN:**
```bash
# Cache hit ratio via Monitoring
gcloud logging read 'resource.type="http_load_balancer" AND jsonPayload.cacheHit=true' \
  --limit=100 --format=json
```

---

**Analysis only — verify against vendor documentation before applying.**

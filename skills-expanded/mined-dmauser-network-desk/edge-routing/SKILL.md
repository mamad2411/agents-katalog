# Skill: Edge Routing & Traffic Management

## Purpose

Design and implement intelligent traffic routing at the CDN edge layer — covering anycast principles, geographic and latency-based routing, edge compute logic, and advanced deployment patterns like A/B testing and canary releases at the edge.

## Core Knowledge

### Anycast Routing Principles

Anycast assigns the same IP address to multiple edge POPs globally. BGP routing directs clients to the nearest POP based on network topology (not geographic distance).

```
                    ┌─────────────────────────────────┐
                    │        Anycast IP: 1.2.3.4      │
                    └─────────────────────────────────┘
                         │           │           │
                    ┌────┴───┐  ┌────┴───┐  ┌────┴───┐
                    │POP: AMS│  │POP: IAD│  │POP: NRT│
                    │(Europe)│  │(US-East)│ │(Asia)  │
                    └────────┘  └─────────┘ └────────┘
                         ▲           ▲           ▲
                    EU clients   US clients  APAC clients
```

**Key characteristics:**
- Single DNS resolution → same IP for all clients
- BGP path selection determines which POP receives traffic
- Failover is automatic — if a POP goes down, BGP withdraws the route
- No DNS TTL propagation delay for failover
- Not suitable for stateful TCP sessions without connection persistence

**CDN anycast implementations:**
- Azure Front Door: All endpoints use anycast by default
- AWS CloudFront: Edge locations announced via anycast
- GCP Cloud CDN: Global external IP (anycast)
- Cloudflare: All 300+ POPs share anycast IPs

### Geographic Routing

Route traffic based on client geographic location (resolved from client IP via GeoIP database).

**Use cases:**
- Content localization (language-specific origins)
- Data residency compliance (EU data stays in EU)
- License/regulatory restrictions (geo-blocking)
- Regional pricing or feature differentiation

### Latency-Based Routing

Route traffic to the origin or POP that provides lowest latency, measured dynamically.

**Azure Front Door latency routing:**
```
Client → Nearest POP → Measure latency to all origin groups → Route to fastest
         (anycast)      (probes every 30s)                     (within threshold)
```

- `additionalLatencyInMilliseconds`: Tolerance before switching origins (e.g., 50ms)
- Prevents flapping between origins with similar latency
- Combined with priority for failover scenarios

### Azure Traffic Manager vs Front Door Routing

| Feature | Traffic Manager | Front Door |
|---------|----------------|------------|
| Layer | DNS (L3/L4) | HTTP reverse proxy (L7) |
| Protocol | Any (TCP/UDP) | HTTP/HTTPS/WebSocket |
| Routing methods | Priority, Weighted, Performance, Geographic, MultiValue, Subnet | Latency-based with priority/weight |
| Failover speed | DNS TTL (30s–300s) | Instant (active health probes) |
| Caching | ✗ | ✓ |
| WAF | ✗ | ✓ |
| SSL offload | ✗ | ✓ |
| Session affinity | ✗ | ✓ |
| Edge compute | ✗ | Rules Engine |
| Cost | Low (DNS queries) | Higher (per-request + egress) |

**When to use Traffic Manager:**
- Non-HTTP protocols (TCP, UDP gaming, MQTT)
- Simple DNS-level failover
- Cost-sensitive with relaxed failover SLA
- Hybrid with on-premises endpoints

**When to use Front Door:**
- Web applications needing instant failover
- WAF + CDN + routing in a single service
- Path-based routing to multiple backends
- SSL offload and HTTP/2 multiplexing

### AWS CloudFront Behaviors and Cache Policies

CloudFront uses **cache behaviors** to match URL patterns and apply specific configurations:

```json
{
  "CacheBehaviors": {
    "Items": [
      {
        "PathPattern": "/api/*",
        "TargetOriginId": "api-origin",
        "ViewerProtocolPolicy": "https-only",
        "AllowedMethods": ["GET", "HEAD", "OPTIONS", "PUT", "POST", "PATCH", "DELETE"],
        "CachePolicyId": "4135ea2d-6df8-44a3-9df3-4b5a84be39ad",
        "OriginRequestPolicyId": "216adef6-5c7f-47e4-b989-5492eafa07d3",
        "ResponseHeadersPolicyId": "67f7725c-6f97-4210-82d7-5512b31e9d03",
        "Compress": true,
        "FunctionAssociations": {
          "Items": [
            {
              "EventType": "viewer-request",
              "FunctionARN": "arn:aws:cloudfront::123456789012:function/url-rewrite"
            }
          ]
        }
      },
      {
        "PathPattern": "/static/*",
        "TargetOriginId": "s3-origin",
        "ViewerProtocolPolicy": "redirect-to-https",
        "AllowedMethods": ["GET", "HEAD"],
        "CachePolicyId": "658327ea-f89d-4fab-a63d-7e88639e58f6",
        "Compress": true
      }
    ]
  }
}
```

**Managed Cache Policies:**
| Policy | Cache Key | TTL | Use Case |
|--------|-----------|-----|----------|
| CachingOptimized | Host, path | default 86400s | Static assets |
| CachingOptimizedForUncompressedObjects | Host, path (no Accept-Encoding) | 86400s | Already compressed (video) |
| CachingDisabled | — | 0 | Dynamic API |
| Amplify | Host, path, Authorization | 600s | Amplify hosting |

### GCP URL Maps and Backend Services

GCP Cloud CDN routing is configured through URL maps attached to a global HTTPS load balancer:

```yaml
# URL map with host and path rules
name: cdn-url-map
defaultService: projects/my-project/global/backendServices/default-backend
hostRules:
  - hosts: ["api.example.com"]
    pathMatcher: api-matcher
  - hosts: ["static.example.com"]
    pathMatcher: static-matcher
pathMatchers:
  - name: api-matcher
    defaultService: projects/my-project/global/backendServices/api-backend
    routeRules:
      - matchRules:
          - prefixMatch: /v2/
        service: projects/my-project/global/backendServices/api-v2-backend
        priority: 1
      - matchRules:
          - prefixMatch: /v1/
        service: projects/my-project/global/backendServices/api-v1-backend
        priority: 2
  - name: static-matcher
    defaultService: projects/my-project/global/backendBuckets/static-bucket
    routeRules:
      - matchRules:
          - prefixMatch: /images/
        service: projects/my-project/global/backendBuckets/image-bucket
        routeAction:
          cdnPolicy:
            cacheMode: CACHE_ALL_STATIC
            defaultTtl: 86400s
            maxTtl: 604800s
```

```bash
# Create URL map with path-based routing
gcloud compute url-maps create cdn-url-map \
  --default-service=default-backend \
  --global

# Add path matcher
gcloud compute url-maps add-path-matcher cdn-url-map \
  --path-matcher-name=api-paths \
  --default-service=api-backend \
  --path-rules="/v2/*=api-v2-backend,/v1/*=api-v1-backend" \
  --new-hosts="api.example.com" \
  --global
```

## Edge Compute

### Azure Front Door Rules Engine

Rules Engine applies request/response transformations at the edge before reaching origin:

```bicep
resource ruleSet 'Microsoft.Cdn/profiles/ruleSets@2023-05-01' = {
  parent: frontDoor
  name: 'EdgeRules'
}

resource redirectRule 'Microsoft.Cdn/profiles/ruleSets/rules@2023-05-01' = {
  parent: ruleSet
  name: 'HttpsRedirect'
  properties: {
    order: 1
    conditions: [
      {
        name: 'RequestScheme'
        parameters: {
          typeName: 'DeliveryRuleRequestSchemeConditionParameters'
          matchValues: ['HTTP']
          operator: 'Equal'
        }
      }
    ]
    actions: [
      {
        name: 'UrlRedirect'
        parameters: {
          typeName: 'DeliveryRuleUrlRedirectActionParameters'
          redirectType: 'PermanentRedirect'
          destinationProtocol: 'Https'
        }
      }
    ]
  }
}

resource headerRule 'Microsoft.Cdn/profiles/ruleSets/rules@2023-05-01' = {
  parent: ruleSet
  name: 'AddSecurityHeaders'
  properties: {
    order: 2
    conditions: []
    actions: [
      {
        name: 'ModifyResponseHeader'
        parameters: {
          typeName: 'DeliveryRuleHeaderActionParameters'
          headerAction: 'Overwrite'
          headerName: 'Strict-Transport-Security'
          value: 'max-age=31536000; includeSubDomains'
        }
      }
      {
        name: 'ModifyResponseHeader'
        parameters: {
          typeName: 'DeliveryRuleHeaderActionParameters'
          headerAction: 'Overwrite'
          headerName: 'X-Content-Type-Options'
          value: 'nosniff'
        }
      }
    ]
  }
}
```

### GCP Service Extensions

Use **Service Extensions** for lightweight request/response logic on supported global external Application Load Balancer paths, including header manipulation, custom routing decisions, and policy enforcement adjacent to Cloud CDN. Verify current triggers, supported load balancers, and limits: https://cloud.google.com/cdn/docs/integration-with-service-extensions.

### AWS CloudFront Functions

Lightweight JavaScript functions running at edge locations (viewer-request/viewer-response):

```javascript
// CloudFront Function: URL rewrite for SPA
function handler(event) {
  var request = event.request;
  var uri = request.uri;

  // If path doesn't have an extension, serve index.html (SPA routing)
  if (!uri.includes('.')) {
    request.uri = '/index.html';
  }

  return request;
}
```

```javascript
// CloudFront Function: A/B testing via cookie
function handler(event) {
  var request = event.request;
  var headers = request.headers;
  var cookies = request.cookies;

  // Check for existing experiment cookie
  if (cookies['ab-experiment']) {
    var variant = cookies['ab-experiment'].value;
    request.headers['x-variant'] = { value: variant };
    return request;
  }

  // Assign variant (80/20 split)
  var variant = Math.random() < 0.8 ? 'control' : 'treatment';
  request.headers['x-variant'] = { value: variant };

  return request;
}
```

```javascript
// CloudFront Function: Viewer-response to set experiment cookie
function handler(event) {
  var response = event.response;
  var request = event.request;

  if (request.headers['x-variant'] && !request.cookies['ab-experiment']) {
    var variant = request.headers['x-variant'].value;
    response.cookies['ab-experiment'] = {
      value: variant,
      attributes: 'Path=/; Max-Age=86400; Secure; HttpOnly'
    };
  }

  return response;
}
```

### Lambda@Edge

Full Node.js/Python runtime for complex edge logic (origin-request/origin-response):

```javascript
// Lambda@Edge: Dynamic origin selection based on device type
exports.handler = async (event) => {
  const request = event.Records[0].cf.request;
  const headers = request.headers;

  const userAgent = headers['user-agent']?.[0]?.value || '';
  const isMobile = /Mobile|Android|iPhone/i.test(userAgent);

  if (isMobile) {
    // Route to mobile-optimized origin
    request.origin = {
      custom: {
        domainName: 'mobile-api.example.com',
        port: 443,
        protocol: 'https',
        sslProtocols: ['TLSv1.2'],
        readTimeout: 30,
        keepaliveTimeout: 5,
        path: '/m'
      }
    };
    request.headers['host'] = [{ key: 'host', value: 'mobile-api.example.com' }];
  }

  return request;
};
```

```javascript
// Lambda@Edge: Origin-response — generate resized images on cache miss
const sharp = require('sharp');
const AWS = require('aws-sdk');
const s3 = new AWS.S3();

exports.handler = async (event) => {
  const response = event.Records[0].cf.response;
  const request = event.Records[0].cf.request;

  // Only process on cache miss (origin returned 200)
  if (response.status !== '200') return response;

  const params = new URLSearchParams(request.querystring);
  const width = parseInt(params.get('w')) || null;

  if (!width) return response;

  // Fetch from S3, resize, return
  const bucket = 'my-images-bucket';
  const key = request.uri.substring(1);

  const s3Object = await s3.getObject({ Bucket: bucket, Key: key }).promise();
  const resized = await sharp(s3Object.Body).resize(width).toBuffer();

  response.body = resized.toString('base64');
  response.bodyEncoding = 'base64';
  response.headers['content-type'] = [{ key: 'Content-Type', value: 'image/webp' }];
  response.headers['cache-control'] = [{ key: 'Cache-Control', value: 'public, max-age=31536000' }];

  return response;
};
```

### CloudFront Functions vs Lambda@Edge

| Feature | CloudFront Functions | Lambda@Edge |
|---------|---------------------|-------------|
| Runtime | JavaScript (ES 5.1) | Node.js / Python |
| Execution time | < 1ms | Up to 30s (origin) / 5s (viewer) |
| Memory | 2 MB | 128–10,240 MB |
| Network access | ✗ | ✓ |
| Body access | ✗ | ✓ |
| Triggers | viewer-request, viewer-response | All four events |
| Scale | Millions RPS | Thousands RPS (per region) |
| Cost | $0.10/million | $0.60/million + duration |
| Use case | Headers, redirects, rewrites | Dynamic origin, auth, image processing |

## A/B Testing at the Edge

### Architecture Pattern

```
┌────────┐    ┌─────────────┐    ┌──────────────┐    ┌─────────────┐
│ Client │───▶│ CDN Edge    │───▶│ Variant      │───▶│ Origin A    │
│        │    │ (assign     │    │ Router       │    │ (control)   │
│        │    │  variant)   │    │              │───▶│ Origin B    │
│        │    └─────────────┘    └──────────────┘    │ (treatment) │
└────────┘                                           └─────────────┘
```

**Implementation considerations:**
1. **Consistent assignment** — Use cookie or header to persist variant
2. **Cache separation** — Include variant in cache key to avoid serving wrong content
3. **Measurement** — Pass variant header to origin for server-side analytics
4. **Gradual rollout** — Start at 1%, increase to 5%, 20%, 50%, 100%

### Canary Deployments at Edge

**Azure Front Door weighted routing:**
```bicep
// 95% to stable, 5% to canary
resource originStable 'Microsoft.Cdn/profiles/originGroups/origins@2023-05-01' = {
  properties: {
    hostName: 'app-stable.azurewebsites.net'
    priority: 1
    weight: 950
  }
}

resource originCanary 'Microsoft.Cdn/profiles/originGroups/origins@2023-05-01' = {
  properties: {
    hostName: 'app-canary.azurewebsites.net'
    priority: 1
    weight: 50
  }
}
```

**AWS CloudFront continuous deployment:**
```bash
# Create staging distribution for canary
aws cloudfront create-distribution --distribution-config file://staging-config.json

# Create continuous deployment policy (header-based or weight-based)
aws cloudfront create-continuous-deployment-policy \
  --continuous-deployment-policy-config '{
    "StagingDistributionDnsNames": {
      "Quantity": 1,
      "Items": ["d111111abcdef8.cloudfront.net"]
    },
    "Enabled": true,
    "TrafficConfig": {
      "Type": "SingleWeight",
      "SingleWeightConfig": {
        "Weight": 0.05,
        "SessionStickinessConfig": {
          "IdleTTL": 300,
          "MaximumTTL": 600
        }
      }
    }
  }'
```

## Routing Decision Tree

```
Is it HTTP/HTTPS traffic?
├── Yes → Use L7 CDN/Edge (Front Door, CloudFront, Cloud CDN)
│   ├── Need WAF? → Azure FD Premium, CF+WAF, Cloud Armor
│   ├── Need edge compute? → CF Functions/Lambda@Edge, FD Rules Engine, or GCP Service Extensions
│   ├── Need private origin? → Azure FD Premium, CF VPC Origins
│   └── Need WebSocket? → Azure FD, CloudFront
└── No (TCP/UDP)
    ├── Azure → Traffic Manager (DNS) or Azure Load Balancer
    ├── AWS → Global Accelerator (anycast TCP/UDP)
    └── GCP → TCP/SSL Proxy LB
```

---

**Analysis only — verify against vendor documentation before applying.**

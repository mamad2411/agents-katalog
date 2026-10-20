# Skill: CDN Architecture Design

## Purpose

Design content delivery network architectures that optimize for performance, reliability, and cost across Azure Front Door, AWS CloudFront, and GCP Cloud CDN. Covers origin configuration, multi-origin failover, origin shielding, protocol optimization, and private origin connectivity.

## Core Knowledge

### Origin Types

#### Storage Origins
- Azure Blob Storage / Static Website hosting
- AWS S3 (bucket as origin with OAC/OAI)
- GCP Cloud Storage (bucket backend)
- Best for: static assets, media files, SPA hosting

#### Application Origins
- Azure App Service, Container Apps, AKS
- AWS ALB, API Gateway, ECS/EKS
- GCP Cloud Run, GKE, Compute Engine instance groups
- Best for: dynamic content, API responses, SSR applications

#### Custom Origins
- Any HTTP/HTTPS endpoint with a public or private IP
- On-premises servers via hybrid connectivity
- Third-party SaaS endpoints
- Best for: legacy migrations, multi-cloud backends

#### Origin Groups (Failover)
- Primary + secondary origins with health probes
- Active-passive or active-active configurations
- Weighted distribution across origins

### Multi-Origin Failover

```
┌─────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   Client    │────▶│   CDN Edge POP   │────▶│  Origin Group   │
└─────────────┘     └──────────────────┘     │                 │
                                              │  ┌───────────┐  │
                                              │  │ Primary   │  │
                                              │  │ (weight:80)│  │
                                              │  └───────────┘  │
                                              │  ┌───────────┐  │
                                              │  │ Secondary │  │
                                              │  │ (weight:20)│  │
                                              │  └───────────┘  │
                                              └─────────────────┘
```

**Health Probe Configuration:**
- Probe path: `/health` or `/.well-known/health`
- Probe interval: 30s (Azure), 5–30s (CloudFront)
- Threshold: 3 consecutive failures before failover
- Protocol: HTTPS preferred, match origin protocol

### Origin Shielding

Origin shielding reduces load on the origin by consolidating cache fills through a designated intermediate cache tier.

**When to use:**
- High traffic with many edge POPs hitting origin
- Origin cannot handle thundering herd on cache expiry
- Geographic concentration of origin infrastructure

**Provider implementations:**
- Azure Front Door: Built-in for supported tiers; verify current tier capabilities in Azure docs
- AWS CloudFront: Origin Shield (per-region, additional request cost — verify current pricing in AWS docs)
- GCP Cloud CDN: Built-in with Cloud CDN cache hierarchy
- Akamai: Tiered Distribution / SureRoute
- Cloudflare: Tiered Cache (free), Argo Tiered Cache (paid)

### Protocol Optimization

| Protocol | Benefit | Support |
|----------|---------|---------|
| HTTP/2 | Multiplexing, header compression, server push | All CDNs (client-side default) |
| HTTP/3 (QUIC) | 0-RTT, no head-of-line blocking, connection migration | Azure FD ✓, CloudFront ✓, Cloud CDN ✓ |
| WebSocket | Persistent bidirectional connections | Azure FD ✓, CloudFront ✓ (limited), Cloud CDN ✗ |
| gRPC | Binary protocol, streaming | Azure FD (Premium) ✓, CloudFront ✗, Cloud CDN ✓ |

### Global vs Regional CDN Patterns

**Global CDN (Anycast):**
- Single entry point, globally distributed POPs
- Best for: public-facing websites, global APIs, media delivery
- Examples: Azure Front Door, CloudFront, Cloud CDN

**Regional CDN:**
- Dedicated POPs in specific regions only
- Best for: compliance (data residency), region-locked content, cost optimization
- Examples: Azure CDN profiles with region restrictions, CloudFront geo-restriction

## Provider Examples

### Azure Front Door (Standard/Premium)

```bicep
resource frontDoor 'Microsoft.Cdn/profiles@2023-05-01' = {
  name: 'fd-global-cdn'
  location: 'global'
  sku: {
    name: 'Premium_AzureFrontDoor'  // or Standard_AzureFrontDoor
  }
}

resource endpoint 'Microsoft.Cdn/profiles/afdEndpoints@2023-05-01' = {
  parent: frontDoor
  name: 'ep-webapp'
  location: 'global'
  properties: {
    enabledState: 'Enabled'
  }
}

resource originGroup 'Microsoft.Cdn/profiles/originGroups@2023-05-01' = {
  parent: frontDoor
  name: 'og-webapp'
  properties: {
    loadBalancingSettings: {
      sampleSize: 4
      successfulSamplesRequired: 3
      additionalLatencyInMilliseconds: 50
    }
    healthProbeSettings: {
      probePath: '/health'
      probeRequestType: 'HEAD'
      probeProtocol: 'Https'
      probeIntervalInSeconds: 30
    }
    sessionAffinityState: 'Disabled'
  }
}

resource originPrimary 'Microsoft.Cdn/profiles/originGroups/origins@2023-05-01' = {
  parent: originGroup
  name: 'origin-eastus'
  properties: {
    hostName: 'webapp-eastus.azurewebsites.net'
    httpPort: 80
    httpsPort: 443
    originHostHeader: 'webapp-eastus.azurewebsites.net'
    priority: 1
    weight: 1000
    enabledState: 'Enabled'
    enforceCertificateNameCheck: true
  }
}

resource originSecondary 'Microsoft.Cdn/profiles/originGroups/origins@2023-05-01' = {
  parent: originGroup
  name: 'origin-westus'
  properties: {
    hostName: 'webapp-westus.azurewebsites.net'
    httpPort: 80
    httpsPort: 443
    originHostHeader: 'webapp-westus.azurewebsites.net'
    priority: 2
    weight: 1000
    enabledState: 'Enabled'
    enforceCertificateNameCheck: true
  }
}
```

**Private Link Origin (Premium only):**

```bicep
resource originPrivate 'Microsoft.Cdn/profiles/originGroups/origins@2023-05-01' = {
  parent: originGroup
  name: 'origin-private'
  properties: {
    hostName: 'internal-api.privatelink.azurewebsites.net'
    httpPort: 80
    httpsPort: 443
    originHostHeader: 'internal-api.azurewebsites.net'
    priority: 1
    weight: 1000
    enabledState: 'Enabled'
    sharedPrivateLinkResource: {
      privateLink: {
        id: '/subscriptions/{sub}/resourceGroups/{rg}/providers/Microsoft.Web/sites/internal-api'
      }
      groupId: 'sites'
      privateLinkLocation: 'eastus2'
      requestMessage: 'Front Door Private Link connection'
    }
  }
}
```

### AWS CloudFront

```json
{
  "DistributionConfig": {
    "Origins": {
      "Quantity": 2,
      "Items": [
        {
          "Id": "primary-alb",
          "DomainName": "alb-primary.us-east-1.elb.amazonaws.com",
          "CustomOriginConfig": {
            "HTTPPort": 80,
            "HTTPSPort": 443,
            "OriginProtocolPolicy": "https-only",
            "OriginSslProtocols": { "Items": ["TLSv1.2"], "Quantity": 1 },
            "OriginReadTimeout": 30,
            "OriginKeepaliveTimeout": 5
          },
          "OriginShield": {
            "Enabled": true,
            "OriginShieldRegion": "us-east-1"
          }
        },
        {
          "Id": "s3-static",
          "DomainName": "my-bucket.s3.us-east-1.amazonaws.com",
          "S3OriginConfig": {
            "OriginAccessIdentity": ""
          },
          "OriginAccessControlId": "E2TB3FJSLURP4A"
        }
      ]
    },
    "OriginGroups": {
      "Quantity": 1,
      "Items": [
        {
          "Id": "failover-group",
          "FailoverCriteria": {
            "StatusCodes": { "Items": [500, 502, 503, 504], "Quantity": 4 }
          },
          "Members": {
            "Items": [
              { "OriginId": "primary-alb" },
              { "OriginId": "s3-static" }
            ],
            "Quantity": 2
          }
        }
      ]
    },
    "DefaultCacheBehavior": {
      "TargetOriginId": "failover-group",
      "ViewerProtocolPolicy": "redirect-to-https",
      "AllowedMethods": ["GET", "HEAD", "OPTIONS"],
      "CachePolicyId": "658327ea-f89d-4fab-a63d-7e88639e58f6",
      "Compress": true
    },
    "HttpVersion": "http2and3",
    "PriceClass": "PriceClass_100"
  }
}
```

**AWS CLI — Create distribution with OAC for S3:**

```bash
# Create Origin Access Control
aws cloudfront create-origin-access-control \
  --origin-access-control-config \
    Name=my-oac,SigningProtocol=sigv4,SigningBehavior=always,OriginAccessControlOriginType=s3

# S3 bucket policy for OAC
cat <<'EOF'
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowCloudFrontServicePrincipal",
      "Effect": "Allow",
      "Principal": { "Service": "cloudfront.amazonaws.com" },
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::my-bucket/*",
      "Condition": {
        "StringEquals": {
          "AWS:SourceArn": "arn:aws:cloudfront::123456789012:distribution/EDFDVBD6EXAMPLE"
        }
      }
    }
  ]
}
EOF
```

### GCP Cloud CDN

```bash
# Create a backend bucket with Cloud CDN enabled
gcloud compute backend-buckets create cdn-backend-bucket \
  --gcs-bucket-name=my-static-assets \
  --enable-cdn \
  --cache-mode=CACHE_ALL_STATIC \
  --default-ttl=3600 \
  --max-ttl=86400 \
  --client-ttl=3600

# Create a backend service with Cloud CDN
gcloud compute backend-services create cdn-backend-service \
  --protocol=HTTPS \
  --port-name=https \
  --health-checks=https-health-check \
  --enable-cdn \
  --cache-mode=USE_ORIGIN_HEADERS \
  --global

# Add NEG or instance group as backend
gcloud compute backend-services add-backend cdn-backend-service \
  --network-endpoint-group=api-neg \
  --network-endpoint-group-zone=us-central1-a \
  --balancing-mode=RATE \
  --max-rate-per-endpoint=100 \
  --global

# URL map for routing
gcloud compute url-maps create cdn-url-map \
  --default-service=cdn-backend-service \
  --global

# HTTPS proxy with HTTP/3
gcloud compute target-https-proxies create cdn-https-proxy \
  --url-map=cdn-url-map \
  --ssl-certificates=my-cert \
  --quic-override=ENABLE \
  --global

# Global forwarding rule (anycast IP)
gcloud compute forwarding-rules create cdn-forwarding-rule \
  --target-https-proxy=cdn-https-proxy \
  --ports=443 \
  --global \
  --ip-version=IPV4
```

### Private Origin Connectivity

| Provider | Mechanism | Supported Origins |
|----------|-----------|-------------------|
| Azure Front Door Premium | Private Link | App Service, Storage, ALB, AKS, Custom (any PE-enabled) |
| AWS CloudFront | VPC Origin | Private ALB/NLB origins; verify current restrictions: https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/private-content-vpc-origins.html |
| GCP Cloud CDN | Internal backend via PSC | Internal HTTP(S) LB, Cloud Run (internal) |

**CloudFront VPC Origin restrictions:** Verify current restrictions in AWS docs. Notable constraints include no Gateway Load Balancer origins, no dual-stack NLB origins, no NLB TLS listeners, security-group requirements for NLB origins, and feature exclusions such as gRPC or Lambda@Edge origin triggers.

**Azure Private Link Origin Flow:**
```
Client → Front Door POP → Microsoft Backbone → Private Endpoint → Origin (no public IP)
```

**Benefits:**
- Origin has no public IP exposure
- Traffic stays on provider backbone
- Simplifies NSG/firewall rules on origin
- Eliminates IP allowlisting maintenance

### GCP Media CDN

Use **Cloud CDN** for general web acceleration behind global external Application Load Balancers or backend buckets. Consider **Media CDN** for large-scale media delivery such as HLS/DASH streaming, video-on-demand, large downloads, and origin protection where media-specific cache behavior and performance/cost controls matter. Verify current product fit and feature differences: https://docs.cloud.google.com/cdn/docs/choose-cdn-product.

| Requirement | Prefer Cloud CDN | Prefer Media CDN |
|-------------|------------------|------------------|
| Web apps/APIs/static assets | Yes | Usually no |
| HLS/DASH or large media libraries | Sometimes | Yes |
| Tight ALB/WAF integration | Yes | Verify fit |
| Media origin protection and cache efficiency | Verify fit | Yes |

## Design Decision Matrix

| Requirement | Azure | AWS | GCP |
|-------------|-------|-----|-----|
| Global anycast + WAF | Front Door Premium | CloudFront + WAF | Cloud CDN + Cloud Armor |
| Private origins | Front Door Premium (Private Link) | VPC Origins | PSC + Internal LB |
| HTTP/3 | ✓ Default | ✓ Opt-in | ✓ QUIC override |
| WebSocket | ✓ | ✓ | ✗ |
| gRPC | Premium only | ✗ | ✓ |
| Origin shield | Built-in | Paid add-on ($) | Built-in hierarchy |
| Real-time logs | ✓ (Log Analytics) | ✓ (Kinesis/S3) | ✓ (Cloud Logging) |
| Edge compute | Rules Engine | CF Functions + Lambda@Edge | Service Extensions for supported global external Application Load Balancer paths; verify current limits: https://cloud.google.com/cdn/docs/integration-with-service-extensions |
| Cost model | Per-request + egress | Per-request + egress | Per-request + egress (cache egress free) |

---

**Analysis only — verify against vendor documentation before applying.**

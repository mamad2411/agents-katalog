# Skill: Security at the Edge (WAF & DDoS)

## Purpose

Design and implement security policies at the CDN/edge layer including Web Application Firewall (WAF) rules, bot management, rate limiting, DDoS protection, and geo-blocking across Azure Front Door, AWS CloudFront, and GCP Cloud CDN/Cloud Armor.

## Core Knowledge

### Security Layers at the Edge

```
┌─────────────────────────────────────────────────────────────────┐
│                        CDN Edge POP                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌───────────────┐  │
│  │ DDoS     │  │ Geo-     │  │ Rate     │  │ WAF           │  │
│  │ Absorb   │──▶│ Fence    │──▶│ Limit    │──▶│ (OWASP/Custom)│──▶ Origin
│  │ (L3/L4/7)│  │ IP Rep   │  │ Bot Mgmt │  │               │  │
│  └──────────┘  └──────────┘  └──────────┘  └───────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

**Defense-in-depth order:**
1. **DDoS absorption** — Volumetric attack mitigation (always-on)
2. **IP reputation / Geo-blocking** — Block known-bad IPs and restricted regions
3. **Rate limiting** — Throttle abusive clients
4. **Bot management** — Challenge or block automated traffic
5. **WAF rules** — Inspect request content (SQL injection, XSS, etc.)

### Azure Front Door WAF Policies

#### Policy Structure

```bicep
resource wafPolicy 'Microsoft.Network/FrontDoorWebApplicationFirewallPolicies@2022-05-01' = {
  name: 'waf-global-policy'
  location: 'global'
  sku: {
    name: 'Premium_AzureFrontDoor'
  }
  properties: {
    policySettings: {
      enabledState: 'Enabled'
      mode: 'Prevention'  // or 'Detection'
      requestBodyCheck: 'Enabled'
      maxRequestBodySizeInKb: 128
      customBlockResponseStatusCode: 403
      customBlockResponseBody: base64('{"error":"blocked","requestId":"${requestId}"}')
    }
    managedRules: {
      managedRuleSets: [
        {
          ruleSetType: 'Microsoft_DefaultRuleSet'
          ruleSetVersion: '2.1'
          ruleGroupOverrides: [
            {
              ruleGroupName: 'SQLI'
              rules: [
                {
                  ruleId: '942110'
                  enabledState: 'Enabled'
                  action: 'Block'
                }
              ]
            }
          ]
          exclusions: [
            {
              matchVariable: 'RequestHeaderNames'
              selectorMatchOperator: 'Equals'
              selector: 'X-Custom-Auth'
            }
          ]
        }
        {
          ruleSetType: 'Microsoft_BotManagerRuleSet'
          ruleSetVersion: '1.1'
        }
      ]
    }
    customRules: {
      rules: [
        {
          name: 'RateLimitPerIP'
          priority: 100
          enabledState: 'Enabled'
          ruleType: 'RateLimitRule'
          rateLimitDurationInMinutes: 1
          rateLimitThreshold: 1000
          matchConditions: [
            {
              matchVariable: 'RequestUri'
              operator: 'Contains'
              matchValue: ['/api/']
              transforms: ['Lowercase']
            }
          ]
          action: 'Block'
        }
        {
          name: 'GeoBlockSanctioned'
          priority: 50
          enabledState: 'Enabled'
          ruleType: 'MatchRule'
          matchConditions: [
            {
              matchVariable: 'RemoteAddr'
              operator: 'GeoMatch'
              matchValue: ['KP', 'IR', 'SY', 'CU']  // Sanctioned countries
              negateCondition: false
            }
          ]
          action: 'Block'
        }
        {
          name: 'AllowKnownPartners'
          priority: 10
          enabledState: 'Enabled'
          ruleType: 'MatchRule'
          matchConditions: [
            {
              matchVariable: 'RemoteAddr'
              operator: 'IPMatch'
              matchValue: ['203.0.113.0/24', '198.51.100.0/24']
            }
          ]
          action: 'Allow'
        }
      ]
    }
  }
}
```

#### Azure WAF Managed Rule Sets

| Rule Set | Purpose | Version |
|----------|---------|---------|
| Microsoft_DefaultRuleSet (DRS) | OWASP Top 10 protection | 2.1 |
| Microsoft_BotManagerRuleSet | Bot classification & mitigation | 1.1 |

**DRS 2.1 Rule Groups:**
- SQLI — SQL injection attacks
- XSS — Cross-site scripting
- LFI — Local file inclusion
- RFI — Remote file inclusion
- RCE — Remote code execution
- PROTOCOL — Protocol violations
- SESSION — Session fixation
- JAVA — Java-specific attacks
- PHP — PHP-specific attacks
- MS-ThreatIntel — Microsoft Threat Intelligence feeds

### AWS WAF with CloudFront

#### WebACL Configuration

```json
{
  "Name": "cloudfront-waf-acl",
  "Scope": "CLOUDFRONT",
  "DefaultAction": { "Allow": {} },
  "Rules": [
    {
      "Name": "AWSManagedRulesCommonRuleSet",
      "Priority": 1,
      "Statement": {
        "ManagedRuleGroupStatement": {
          "VendorName": "AWS",
          "Name": "AWSManagedRulesCommonRuleSet",
          "ExcludedRules": [
            { "Name": "SizeRestrictions_BODY" }
          ]
        }
      },
      "OverrideAction": { "None": {} },
      "VisibilityConfig": {
        "SampledRequestsEnabled": true,
        "CloudWatchMetricsEnabled": true,
        "MetricName": "AWSCommonRules"
      }
    },
    {
      "Name": "AWSManagedRulesSQLiRuleSet",
      "Priority": 2,
      "Statement": {
        "ManagedRuleGroupStatement": {
          "VendorName": "AWS",
          "Name": "AWSManagedRulesSQLiRuleSet"
        }
      },
      "OverrideAction": { "None": {} },
      "VisibilityConfig": {
        "SampledRequestsEnabled": true,
        "CloudWatchMetricsEnabled": true,
        "MetricName": "AWSSQLiRules"
      }
    },
    {
      "Name": "AWSManagedRulesBotControlRuleSet",
      "Priority": 3,
      "Statement": {
        "ManagedRuleGroupStatement": {
          "VendorName": "AWS",
          "Name": "AWSManagedRulesBotControlRuleSet",
          "ManagedRuleGroupConfigs": [
            {
              "AWSManagedRulesBotControlRuleSet": {
                "InspectionLevel": "TARGETED"
              }
            }
          ]
        }
      },
      "OverrideAction": { "None": {} },
      "VisibilityConfig": {
        "SampledRequestsEnabled": true,
        "CloudWatchMetricsEnabled": true,
        "MetricName": "BotControl"
      }
    },
    {
      "Name": "RateLimitAPI",
      "Priority": 10,
      "Statement": {
        "RateBasedStatement": {
          "Limit": 2000,
          "AggregateKeyType": "IP",
          "ScopeDownStatement": {
            "ByteMatchStatement": {
              "SearchString": "/api/",
              "FieldToMatch": { "UriPath": {} },
              "TextTransformations": [{ "Priority": 0, "Type": "LOWERCASE" }],
              "PositionalConstraint": "STARTS_WITH"
            }
          }
        }
      },
      "Action": { "Block": {} },
      "VisibilityConfig": {
        "SampledRequestsEnabled": true,
        "CloudWatchMetricsEnabled": true,
        "MetricName": "RateLimitAPI"
      }
    },
    {
      "Name": "GeoBlock",
      "Priority": 5,
      "Statement": {
        "GeoMatchStatement": {
          "CountryCodes": ["KP", "IR", "SY", "CU"]
        }
      },
      "Action": { "Block": {} },
      "VisibilityConfig": {
        "SampledRequestsEnabled": true,
        "CloudWatchMetricsEnabled": true,
        "MetricName": "GeoBlock"
      }
    }
  ],
  "VisibilityConfig": {
    "SampledRequestsEnabled": true,
    "CloudWatchMetricsEnabled": true,
    "MetricName": "cloudfront-waf"
  }
}
```

**AWS CLI:**
```bash
# Create WebACL for CloudFront (must be in us-east-1)
aws wafv2 create-web-acl \
  --name cloudfront-waf-acl \
  --scope CLOUDFRONT \
  --region us-east-1 \
  --default-action Allow={} \
  --rules file://waf-rules.json \
  --visibility-config SampledRequestsEnabled=true,CloudWatchMetricsEnabled=true,MetricName=cloudfront-waf

# Associate with CloudFront distribution
aws cloudfront update-distribution \
  --id E1A2B3C4D5E6F7 \
  --distribution-config file://dist-config-with-waf.json
```

#### AWS Managed Rule Groups

| Rule Group | WCU Cost | Purpose |
|------------|----------|---------|
| AWSManagedRulesCommonRuleSet | 700 | Core OWASP rules |
| AWSManagedRulesSQLiRuleSet | 200 | SQL injection |
| AWSManagedRulesKnownBadInputsRuleSet | 200 | Log4j, path traversal |
| AWSManagedRulesBotControlRuleSet | 50 base WCU — verify current WCU in AWS docs | Bot detection; pricing/inspection level is separate |
| AWSManagedRulesATPRuleSet | 50 | Account takeover prevention |
| AWSManagedRulesACFPRuleSet | 50 | Account creation fraud |
| AWSManagedRulesAmazonIpReputationList | 25 | Known malicious IPs |
| AWSManagedRulesAnonymousIpList | 50 | VPN, Tor, proxy IPs |

Verify current WCU quotas and managed rule group capacities before deployment: https://docs.aws.amazon.com/waf/latest/developerguide/limits.html.

### GCP Cloud Armor Policies

```bash
# Create security policy
gcloud compute security-policies create cdn-waf-policy \
  --description="CDN WAF policy" \
  --type=CLOUD_ARMOR

# Enable preconfigured WAF rules (OWASP ModSecurity CRS 3.3)
gcloud compute security-policies rules create 1000 \
  --security-policy=cdn-waf-policy \
  --expression="evaluatePreconfiguredExpr('sqli-v33-stable')" \
  --action=deny-403 \
  --description="Block SQL injection"

gcloud compute security-policies rules create 1001 \
  --security-policy=cdn-waf-policy \
  --expression="evaluatePreconfiguredExpr('xss-v33-stable')" \
  --action=deny-403 \
  --description="Block XSS"

gcloud compute security-policies rules create 1002 \
  --security-policy=cdn-waf-policy \
  --expression="evaluatePreconfiguredExpr('lfi-v33-stable')" \
  --action=deny-403 \
  --description="Block LFI"

# Geo-blocking rule
gcloud compute security-policies rules create 500 \
  --security-policy=cdn-waf-policy \
  --expression="origin.region_code == 'KP' || origin.region_code == 'IR'" \
  --action=deny-403 \
  --description="Block sanctioned countries"

# Rate limiting
gcloud compute security-policies rules create 100 \
  --security-policy=cdn-waf-policy \
  --expression="true" \
  --action=throttle \
  --rate-limit-threshold-count=1000 \
  --rate-limit-threshold-interval-sec=60 \
  --conform-action=allow \
  --exceed-action=deny-429 \
  --enforce-on-key=IP \
  --description="Rate limit 1000 req/min per IP"

# Adaptive protection (ML-based DDoS detection)
gcloud compute security-policies update cdn-waf-policy \
  --enable-layer7-ddos-defense \
  --layer7-ddos-defense-rule-visibility=STANDARD

# Attach policy to backend service
gcloud compute backend-services update cdn-backend-service \
  --security-policy=cdn-waf-policy \
  --global
```

#### GCP Cloud Armor Preconfigured Rules

| Rule Expression | Coverage |
|-----------------|----------|
| `sqli-v33-stable` | SQL injection (CRS 942xxx) |
| `xss-v33-stable` | Cross-site scripting (CRS 941xxx) |
| `lfi-v33-stable` | Local file inclusion (CRS 930xxx) |
| `rfi-v33-stable` | Remote file inclusion (CRS 931xxx) |
| `rce-v33-stable` | Remote code execution (CRS 932xxx) |
| `methodenforcement-v33-stable` | HTTP method enforcement |
| `scannerdetection-v33-stable` | Scanner/crawler detection |
| `protocolattack-v33-stable` | Protocol violations |
| `php-v33-stable` | PHP attacks |
| `sessionfixation-v33-stable` | Session fixation |
| `java-v33-stable` | Java attacks (Log4j included) |
| `cve-canary` | Emerging CVEs (auto-updated) |

### Bot Management

#### Bot Classification Tiers

| Category | Examples | Action |
|----------|----------|--------|
| Verified bots | Googlebot, Bingbot, GPTBot | Allow (verify via reverse DNS) |
| Good bots | SEO tools, uptime monitors | Allow with monitoring |
| Suspicious bots | Scrapers, headless browsers | Challenge (CAPTCHA/JS challenge) |
| Malicious bots | Credential stuffing, DDoS tools | Block |

#### Azure Bot Manager

```bicep
// Bot Manager rule set in WAF policy
{
  ruleSetType: 'Microsoft_BotManagerRuleSet'
  ruleSetVersion: '1.1'
  ruleGroupOverrides: [
    {
      ruleGroupName: 'GoodBots'
      rules: [
        {
          ruleId: 'Bot100'  // Good bot (verified search engines)
          enabledState: 'Enabled'
          action: 'Allow'
        }
      ]
    }
    {
      ruleGroupName: 'BadBots'
      rules: [
        {
          ruleId: 'Bot200'  // Bad bot signatures
          enabledState: 'Enabled'
          action: 'Block'
        }
      ]
    }
  ]
}
```

#### AWS Bot Control (Targeted)

Targeted bot control uses ML-based behavioral analysis:
- Browser fingerprinting
- Client-side challenge tokens
- Request pattern analysis
- IP reputation + behavioral correlation

```json
{
  "Name": "BotControlTargeted",
  "Statement": {
    "ManagedRuleGroupStatement": {
      "VendorName": "AWS",
      "Name": "AWSManagedRulesBotControlRuleSet",
      "ManagedRuleGroupConfigs": [
        {
          "AWSManagedRulesBotControlRuleSet": {
            "InspectionLevel": "TARGETED",
            "EnableMachineLearning": true
          }
        }
      ],
      "RuleActionOverrides": [
        {
          "Name": "CategoryAdvertising",
          "ActionToUse": { "Allow": {} }
        },
        {
          "Name": "CategorySearchEngine",
          "ActionToUse": { "Allow": {} }
        },
        {
          "Name": "SignalNonBrowserUserAgent",
          "ActionToUse": { "Challenge": {} }
        }
      ]
    }
  }
}
```

### Rate Limiting at the Edge

**Rate limiting strategies:**

| Strategy | Description | Use Case |
|----------|-------------|----------|
| Per-IP | Count requests from single IP | General abuse prevention |
| Per-IP + Path | Count per IP scoped to specific paths | API endpoint protection |
| Per-Header | Count by custom header (API key, tenant) | Multi-tenant rate limiting |
| Per-Cookie | Count by session cookie | Authenticated user limits |
| Per-Geographic | Limit per country/region | Regional traffic shaping |
| Sliding window | Count over rolling time window | Smooth rate enforcement |
| Token bucket | Allow bursts up to bucket size | Bursty workloads |

**Azure Front Door rate limiting:**
```
Rate limit = rateLimitThreshold / rateLimitDurationInMinutes

Example: 1000 requests per 1 minute per IP for /api/* paths
```

**AWS WAF rate-based rules:**
- Current documented minimum threshold is 10 requests per evaluation window; verify current quotas before deployment: https://docs.aws.amazon.com/waf/latest/developerguide/limits.html.
- Evaluation windows and aggregate keys change over time; verify supported windows and keys in AWS WAF documentation.
- Aggregate keys include IP/forwarded IP and supported custom keys (headers, query, cookies) where available.

**GCP Cloud Armor throttle:**
- Rate threshold: count per interval
- Enforce on: IP, ALL (global), XFF_IP, HTTP_HEADER, HTTP_COOKIE, REGION_CODE

### DDoS Protection at CDN Layer (L7)

| Provider | Service | Coverage |
|----------|---------|----------|
| Azure | DDoS Protection Standard + Front Door | L3/L4/L7 |
| AWS | Shield Standard (free) + Shield Advanced ($3K/mo) + WAF | L3/L4/L7 |
| GCP | Cloud Armor Adaptive Protection (ML-based) | L7 |
| Cloudflare | Always-on DDoS mitigation | L3/L4/L7 |

**Azure DDoS + Front Door:**
- Front Door inherently absorbs L7 DDoS via global distribution
- DDoS Protection Standard protects origin VNet
- WAF rate-limiting handles application-layer floods

**AWS Shield Advanced with CloudFront:**
```bash
# Enable Shield Advanced on CloudFront distribution
aws shield create-protection \
  --name "CDN-Protection" \
  --resource-arn "arn:aws:cloudfront::123456789012:distribution/E1A2B3C4D5E6F7"

# Configure proactive engagement (DRT assistance)
aws shield update-emergency-contact-settings \
  --emergency-contact-list EmailAddress=security@example.com,PhoneNumber=+1234567890
```

**GCP Adaptive Protection:**
```bash
# ML-based attack detection — automatically detects anomalous traffic patterns
gcloud compute security-policies update cdn-waf-policy \
  --enable-layer7-ddos-defense \
  --layer7-ddos-defense-rule-visibility=STANDARD
  # STANDARD: generates alerts
  # PREMIUM: auto-deploys rules (requires Cloud Armor Enterprise)
```

### Geo-Blocking / Geo-Fencing

**Implementation approaches:**

1. **CDN-level restriction** — Block before reaching edge logic
2. **WAF rule** — Block with custom response/redirect
3. **Edge compute** — Redirect to localized content

**Azure Front Door geo-filtering:**
```bicep
// Custom WAF rule
{
  name: 'GeoAllowUS_EU'
  priority: 1
  ruleType: 'MatchRule'
  matchConditions: [
    {
      matchVariable: 'RemoteAddr'
      operator: 'GeoMatch'
      matchValue: ['US', 'CA', 'GB', 'DE', 'FR', 'NL', 'IE']
      negateCondition: true  // Block if NOT in allowed list
    }
  ]
  action: 'Block'
}
```

**AWS CloudFront geographic restrictions:**
```json
{
  "Restrictions": {
    "GeoRestriction": {
      "RestrictionType": "whitelist",
      "Quantity": 5,
      "Items": ["US", "CA", "GB", "DE", "FR"]
    }
  }
}
```

**GCP Cloud Armor:**
```bash
gcloud compute security-policies rules create 200 \
  --security-policy=cdn-waf-policy \
  --expression="!(origin.region_code == 'US' || origin.region_code == 'CA' || origin.region_code == 'GB')" \
  --action=deny-403
```

### IP Reputation Lists

**Sources:**
- Provider-managed: Azure Threat Intelligence, AWS IP Reputation List, GCP Threat Intelligence
- Third-party: Spamhaus, AbuseIPDB, Project Honeypot
- Custom: Internal honeypot data, abuse reports

**Azure — Threat Intelligence feed (auto-updated):**
```bicep
{
  ruleSetType: 'Microsoft_DefaultRuleSet'
  ruleSetVersion: '2.1'
  // MS-ThreatIntel rule group is included by default
}
```

**AWS — Managed IP reputation:**
```json
{
  "Name": "AWSIPReputation",
  "Statement": {
    "ManagedRuleGroupStatement": {
      "VendorName": "AWS",
      "Name": "AWSManagedRulesAmazonIpReputationList"
    }
  }
}
```

**GCP — Threat intelligence:**
```bash
gcloud compute security-policies rules create 300 \
  --security-policy=cdn-waf-policy \
  --expression="evaluateThreatIntelligence('iplist-known-malicious-ips')" \
  --action=deny-403
```

## Security Decision Matrix

| Requirement | Azure Front Door | AWS CloudFront + WAF | GCP Cloud Armor |
|-------------|-----------------|---------------------|-----------------|
| OWASP Top 10 | DRS 2.1 | Common Rule Set | CRS 3.3 preconfigured |
| Bot management | Bot Manager 1.1 | Bot Control (Targeted) | reCAPTCHA Enterprise integration |
| Rate limiting | Custom rules (per min) | Rate-based rules (per 5 min) | Throttle action (per sec/min) |
| Geo-blocking | WAF custom rule | Native + WAF | CEL expression |
| IP reputation | MS Threat Intelligence | IP Reputation List | Threat Intelligence feeds |
| Adaptive DDoS | ✗ (use DDoS Protection) | Shield Advanced | Adaptive Protection ML |
| Custom responses | Custom block response body | Custom response (headers + body) | Custom error pages |
| Logging | Log Analytics | CloudWatch + S3 | Cloud Logging |
| Cost (WAF) | Included in FD Premium | $5/WebACL + $1/rule + $0.60/M req | $5/policy + $1/rule + $0.75/M req |

---

**Analysis only — verify against vendor documentation before applying.**

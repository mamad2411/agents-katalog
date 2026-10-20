# Skill: WAF Rules Configuration (`lb_waf_rules`)

Design and configure Web Application Firewall (WAF) policies across Azure WAF, AWS WAF, and GCP Cloud Armor. Covers managed rulesets, custom rules, exclusions, bot protection, and rate limiting.

---

## WAF Fundamentals

A WAF inspects HTTP/HTTPS traffic at Layer 7 and blocks requests matching known attack patterns (SQL injection, XSS, path traversal, etc.). WAF operates in two modes:

| Mode | Behavior | When to Use |
|---|---|---|
| **Detection** | Logs matches but allows all traffic | Initial deployment — run for 2–4 weeks to identify false positives before switching to Prevention |
| **Prevention** | Blocks matching traffic | Production — after tuning exclusions |

**Always deploy in Detection mode first.** Switching directly to Prevention will almost certainly block legitimate traffic.

---

## Azure WAF

Azure WAF is available on **Application Gateway v2** (regional) and **Front Door Standard/Premium** (global).

### Managed Rulesets

```bash
# Create WAF policy with OWASP 3.2 managed rules (Application Gateway)
az network application-gateway waf-policy create \
  --resource-group myRG \
  --name myWAFPolicy

az network application-gateway waf-policy managed-rule rule-set add \
  --policy-name myWAFPolicy \
  --resource-group myRG \
  --type OWASP \
  --version 3.2

# Front Door WAF with DRS 2.1
az network front-door waf-policy managed-rule-definition list --query "[].{ruleSetType:ruleSetType, version:ruleSetVersion}" --output table

az afd waf-policy managed-rule-set add \
  --policy-name myFDWAFPolicy \
  --resource-group myRG \
  --type Microsoft_DefaultRuleSet \
  --version 2.1
```

**Azure OWASP CRS / DRS rule groups:**

| Rule Group | Protects Against |
|---|---|
| SQL Injection (SQLi) | `' OR 1=1 --`, UNION-based injection, blind SQLi |
| Cross-Site Scripting (XSS) | `<script>`, event handlers, encoded XSS payloads |
| Local File Inclusion (LFI) | `../../etc/passwd`, directory traversal |
| Remote File Inclusion (RFI) | Remote URL execution in include statements |
| Remote Code Execution (RCE) | OS command injection, code evaluation |
| Protocol Violations | Malformed HTTP, invalid headers |
| Protocol Anomalies | Missing Host header, unusual methods |
| Scanners/Bots | Scanner user-agents, probe patterns |

### Custom Rules

```bash
# Block requests from specific countries (Front Door)
az afd waf-policy custom-rule create \
  --policy-name myFDWAFPolicy \
  --resource-group myRG \
  --name BlockCountries \
  --priority 100 \
  --action Block \
  --rule-type MatchRule \
  --match-variable RemoteAddr \
  --operator GeoMatch \
  --match-values "CN" "RU" "KP"

# Rate limit: max 1000 requests per 5 minutes per IP
az afd waf-policy custom-rule create \
  --policy-name myFDWAFPolicy \
  --resource-group myRG \
  --name RateLimit \
  --priority 200 \
  --action Block \
  --rule-type RateLimitRule \
  --rate-limit-threshold 1000 \
  --rate-limit-duration-in-minutes 5 \
  --match-variable RemoteAddr \
  --operator IPMatch \
  --match-values "0.0.0.0/0"
```

### Exclusions

When managed rules create false positives (e.g., a CMS editor with HTML in the body), add exclusions rather than disabling the rule:

```bash
# Exclude a specific request body field from rule 942130 (SQLi detection)
az network application-gateway waf-policy managed-rule exclusion add \
  --policy-name myWAFPolicy \
  --resource-group myRG \
  --match-variable RequestBodyPostArgNames \
  --selector-match-operator Contains \
  --selector "editor_content" \
  --type OWASP \
  --version 3.2 \
  --group-name REQUEST-942-APPLICATION-ATTACK-SQLI \
  --rule-id 942130
```

### Bot Protection

Azure Front Door Premium includes Microsoft Bot Manager ruleset:
- **Good bots**: Search engines (Googlebot, Bingbot) — allow.
- **Bad bots**: Scrapers, spam bots — block.
- **Unknown bots**: CAPTCHA challenge or rate limit.

---

## AWS WAF v2

AWS WAF v2 attaches to **ALB**, **CloudFront**, **API Gateway**, and **AppSync**.

### Managed Rule Groups

```bash
# Create web ACL with AWS Managed Rules Core Rule Set
aws wafv2 create-web-acl \
  --name myWebACL \
  --scope REGIONAL \
  --default-action Allow={} \
  --rules '[
    {
      "Name": "AWSManagedRulesCommonRuleSet",
      "Priority": 1,
      "Statement": {
        "ManagedRuleGroupStatement": {
          "VendorName": "AWS",
          "Name": "AWSManagedRulesCommonRuleSet"
        }
      },
      "OverrideAction": {"None": {}},
      "VisibilityConfig": {
        "SampledRequestsEnabled": true,
        "CloudWatchMetricsEnabled": true,
        "MetricName": "AWSCoreRules"
      }
    }
  ]' \
  --visibility-config SampledRequestsEnabled=true,CloudWatchMetricsEnabled=true,MetricName=myWebACL
```

**Key AWS managed rule groups:**

| Rule Group | Description |
|---|---|
| `AWSManagedRulesCommonRuleSet` | OWASP Top 10 coverage — SQLi, XSS, LFI, RFI |
| `AWSManagedRulesSQLiRuleSet` | Additional SQL injection patterns |
| `AWSManagedRulesKnownBadInputsRuleSet` | Log4j/JNDI, Java deserialization, host header abuse |
| `AWSManagedRulesBotControlRuleSet` | Bot detection and management (additional cost) |
| `AWSManagedRulesATPRuleSet` | Account takeover prevention (login page protection) |

### Custom Rules and Rate Limiting

```bash
# Rate-based rule: block IPs exceeding 2000 requests per 5 minutes
aws wafv2 create-web-acl --name myACL --scope REGIONAL \
  --default-action Allow={} \
  --rules '[{
    "Name": "RateLimit",
    "Priority": 1,
    "Statement": {
      "RateBasedStatement": {
        "Limit": 2000,
        "AggregateKeyType": "IP"
      }
    },
    "Action": {"Block": {}},
    "VisibilityConfig": {"SampledRequestsEnabled":true,"CloudWatchMetricsEnabled":true,"MetricName":"RateLimit"}
  }]' \
  --visibility-config SampledRequestsEnabled=true,CloudWatchMetricsEnabled=true,MetricName=myACL
```

### AWS WAF Logging

```bash
# Enable logging to CloudWatch Logs
aws wafv2 put-logging-configuration \
  --logging-configuration ResourceArn=arn:aws:wafv2:...,LogDestinationConfigs=["arn:aws:logs:..."]
```

---

## GCP Cloud Armor

Cloud Armor attaches to **external HTTP(S) Load Balancers** and **external TCP/SSL Proxy LBs**.

### Security Policies

```bash
# Create security policy with preconfigured WAF rules
gcloud compute security-policies create my-policy \
  --description "WAF policy"

# Enable OWASP ModSecurity CRS 3.3 rules
gcloud compute security-policies rules create 1000 \
  --security-policy my-policy \
  --expression "evaluatePreconfiguredExpr('sqli-v33-stable')" \
  --action deny-403

gcloud compute security-policies rules create 1001 \
  --security-policy my-policy \
  --expression "evaluatePreconfiguredExpr('xss-v33-stable')" \
  --action deny-403

# Rate limiting
gcloud compute security-policies rules create 2000 \
  --security-policy my-policy \
  --expression "true" \
  --action throttle \
  --rate-limit-threshold-count 1000 \
  --rate-limit-threshold-interval-sec 60 \
  --conform-action allow \
  --exceed-action deny-429 \
  --enforce-on-key IP

# Apply to backend service
gcloud compute backend-services update my-backend \
  --security-policy my-policy --global
```

**Cloud Armor preconfigured rules:**

| Expression | Coverage |
|---|---|
| `sqli-v33-stable` | SQL injection (stable sensitivity) |
| `xss-v33-stable` | Cross-site scripting |
| `lfi-v33-stable` | Local file inclusion |
| `rfi-v33-stable` | Remote file inclusion |
| `rce-v33-stable` | Remote code execution |
| `methodenforcement-v33-stable` | HTTP method enforcement |
| `scannerdetection-v33-stable` | Scanner/probe detection |

**Cloud Armor Adaptive Protection** (ML-based): Automatically detects and mitigates L7 DDoS attacks. Enable on the security policy.

---

## WAF Tuning Workflow

1. **Deploy in Detection/Count mode** for 2–4 weeks.
2. **Review logs** — identify false positives by analyzing blocked requests against known-good traffic.
3. **Add exclusions** for legitimate traffic patterns (CMS content, API payloads with SQL-like syntax, encoded data).
4. **Switch to Prevention/Block mode** rule-by-rule, starting with high-confidence rule groups (protocol violations, scanners) and ending with broad groups (SQLi, XSS).
5. **Monitor continuously** — new application features may trigger new false positives.
6. **Review quarterly** — update managed rulesets, review custom rules, check for new CVEs.

---

## Common WAF Mistakes

1. **Enabling Prevention mode without tuning** — blocks legitimate users on day one.
2. **Disabling entire rule groups** instead of adding targeted exclusions — leaves security gaps.
3. **No logging** — WAF is useless if you can't see what it's blocking. Always enable full logging.
4. **Ignoring rate limiting** — WAF rules alone won't stop volumetric L7 DDoS. Add rate-based rules.
5. **Not testing after application changes** — a new API endpoint or form field can trigger existing rules.

**Analysis only — verify against vendor documentation before applying.**

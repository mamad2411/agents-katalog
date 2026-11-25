---
name: aws-waf-bot-control
description: >
  AWS WAF Bot Control managed rule groups for owned applications: common vs targeted
  inspection levels, labels, token SDK, CAPTCHA/Challenge actions, allowlisting good
  bots, false-positive tuning, and logging. Use when reducing scrapers, credential
  stuffing, or fake browsers on CloudFront/ALB/API Gateway — not for attacking third-party
  sites or bypassing bots without authorization.
---

# AWS WAF Bot Control

## Scope And Authorization

- **In scope:** AWS WAF WebACLs protecting applications you own or are authorized to harden.
- **Out of scope:** Using Bot Control knowledge to attack or evade third-party defenses without authorization.
- Bot Control incurs managed rule costs — track sampling and targeted tiers.
- Pair volumetric DDoS with `aws-shield-advanced-notes`; CAPTCHA research ethics with `captcha-bypass-research` only for authorized control testing.
- Use `code-quality-standards` for automation/IaC.

## When To Use

- Enabling AWSManagedRulesBotControlRuleSet on CloudFront, ALB, API Gateway, or AppSync.
- Tuning false positives for mobile apps, partners, or monitoring bots.
- Adding Challenge/CAPTCHA actions for suspicious bot labels.
- Investigating WAF labels (`awswaf:managed:aws:bot-control:...`) in logs.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Network DDoS / Shield Advanced | `aws-shield-advanced-notes` |
| Rate-limit testing methodology | `rate-limit-bypass-testing` (authorized) |
| Generic CAPTCHA control research | `captcha-bypass-research` (authorized) |
| Security groups | `aws-security-groups-review` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Topic | Guidance |
| --- | --- |
| Common level | Baseline bot signals; lower cost; first step |
| Targeted level | Stronger inspection/ML-style signals; higher cost |
| Labels | Use in subsequent rules for custom allow/deny/challenge |
| Tokens | AWS WAF JS SDK / application integration for challenge tokens |
| Actions | Allow, Block, Count, CAPTCHA, Challenge |
| Tooling | `wafv2` CLI, WAF logging to S3/Firehose/CloudWatch, Firewall Manager |

## Workflow

### 1. Confirm scope and success criteria

1. Resource ARNs, WebACL scope (CLOUDFRONT vs REGIONAL), traffic baseline, business-critical good bots.
2. Success: malicious bot volume down; false positive rate under agreed threshold; logs show labels.
3. Start with **Count** mode before Block.

### 2. Inventory WAF and traffic

```bash
aws sts get-caller-identity
aws wafv2 list-web-acls --scope REGIONAL --region us-east-1
aws wafv2 get-web-acl --name "$NAME" --scope REGIONAL --id "$ID" --region us-east-1
# CloudFront scope uses --scope CLOUDFRONT --region us-east-1
aws wafv2 get-logging-configuration --resource-arn "$WEBACL_ARN"
```

1. List existing managed rule groups and rule priorities.
2. Sample access logs for bot-like UAs and spike paths (`/login`, `/search`).
3. Inventory legitimate automation (status crawlers, payment webhooks, partner IPs).

### 3. Baseline with Count

1. Add Bot Control rule group in Count; emit labels without blocking.
2. Run 1–2 weeks (or sufficient traffic) and analyze label distribution.
3. Measure conversion/login success rates for humans (mobile/web).

### 4. Enable and tune Bot Control

```json
{
  "Name": "AWS-AWSManagedRulesBotControlRuleSet",
  "Priority": 20,
  "OverrideAction": { "None": {} },
  "Statement": {
    "ManagedRuleGroupStatement": {
      "VendorName": "AWS",
      "Name": "AWSManagedRulesBotControlRuleSet",
      "ManagedRuleGroupConfigs": [{
        "AWSManagedRulesBotControlRuleSet": { "InspectionLevel": "COMMON" }
      }]
    }
  },
  "VisibilityConfig": {
    "SampledRequestsEnabled": true,
    "CloudWatchMetricsEnabled": true,
    "MetricName": "BotControl"
  }
}
```

```bash
aws wafv2 update-web-acl --scope REGIONAL --id "$ID" --name "$NAME" \
  --default-action Allow={} --lock-token "$TOKEN" \
  --visibility-config ... --rules file://rules.json
```

**Tuning patterns:**

1. Rule action overrides: set specific bot categories to Count while blocking others.
2. Allowlist good bots by verified IP / known bot labels + reverse DNS process.
3. Insert custom rules: if label `...targeted...` AND path `/login` → Challenge/CAPTCHA.
4. Integrate AWS WAF application integration SDK for token-based challenges on SPAs.
5. Exclude health checks and internal paths carefully (not overly broad).

### 5. Verify with evidence

```bash
aws wafv2 get-sampled-requests --web-acl-arn "$WEBACL_ARN" --rule-metric-name BotControl \
  --scope REGIONAL --time-window StartTime=...,EndTime=... --max-items 50
# Inspect LOG fields: action, httpRequest, labels
```

1. Synthetic human browser path succeeds; simple curl scrapers get Challenge/Block as intended.
2. Partner webhooks still 200 (allowlist verified).
3. Compare bot request ratio and login failure rates before/after Block enablement.

### 6. Observe and harden

1. Dashboards: blocked vs challenged vs allowed; top labels; false positive tickets.
2. Alarms on sudden Block spikes (possible self-DoS from bad rule).
3. Combine with rate-based rules on `/login` and Shield for volumetric events.

### 7. Hand off

1. Document inspection level, overrides, allowlists, and owners.
2. Process for vendor bots requesting allowlist (ticket + expiry).
3. Cost review when moving COMMON → TARGETED.

## Action Ladder

| Stage | Action | Purpose |
| --- | --- | --- |
| 1 | Count all Bot Control | Learn labels |
| 2 | Challenge suspicious | Friction for likely bots |
| 3 | Block known bad categories | Enforce |
| 4 | CAPTCHA on sensitive paths | Step-up |
| 5 | Targeted inspection | Harder abuse |

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Rollout | Count → Challenge → Block | Immediate Block on TARGETED in prod |
| Allowlists | Scoped IPs/ASNs + expiry | Wide `0.0.0.0/0` exceptions |
| Mobile apps | Token SDK / header design | Treating all non-browser as Block forever |
| Logging | Labels + path redaction | Full auth headers in logs |
| Scope | WAF + app rate limits + credential hygiene | WAF as only anti-abuse control |

## Output Checklist

- [ ] WebACL and protected resources inventoried
- [ ] Legitimate bots and critical paths listed
- [ ] Bot Control added in Count; baseline analyzed
- [ ] Inspection level chosen (COMMON/TARGETED)
- [ ] Overrides/allowlists documented with owners
- [ ] Challenge/CAPTCHA/token integration planned where needed
- [ ] Before/after metrics evidenced
- [ ] Logging and alarms configured
- [ ] Cost impact reviewed
- [ ] `code-quality-standards` applied if IaC shipped

## Rules

- Authorized applications only; no offensive bot-evasion against third parties.
- Prefer progressive enforcement to avoid customer outages.
- Review allowlists on a schedule; no permanent silent holes.
- Protect log sinks — requests may include tokens/PII.
- Coordinate with Shield and app-layer auth controls.

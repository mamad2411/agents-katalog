---
name: aws-shield-advanced-notes
description: >
  AWS Shield Advanced operational notes for owned accounts: protection scopes
  (CloudFront, Route 53, ALB/CLB/NLB, EIPs), SRT engagement, DDoS response team
  runbooks, health-based detection, DRTs, cost protection, and WAF integration.
  Use when enabling or reviewing Shield Advanced coverage and incident readiness —
  not for launching DDoS attacks or testing third-party resilience without authorization.
---

# AWS Shield Advanced Notes

## Scope And Authorization

- **In scope:** DDoS protection design and operations for AWS resources you own or are authorized to defend.
- **Out of scope:** Generating attack traffic against systems without written authorization; abusing SRT processes.
- Shield Advanced is a commercial subscription — track protected resources and billing ownership.
- Pair edge WAF rules with `aws-waf-bot-control` where application-layer bots are the issue.
- Use `code-quality-standards` for automation/IaC.

## When To Use

- Subscribing to Shield Advanced or auditing which resources are protected.
- Building a DDoS runbook: detection, SRT contact, traffic scrubbing expectations, comms.
- Associating Route 53 health checks for health-based detection.
- Coordinating Shield + AWS WAF + CloudFront/ALB architecture.
- Post-incident review of volumetric vs application-layer events.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Bot Control / L7 managed rules | `aws-waf-bot-control` |
| Security groups / network exposure | `aws-security-groups-review` |
| Generic observability | `observability-metrics-tracing` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Topic | Notes |
| --- | --- |
| Shield Standard | Automatic baseline for all customers (common L3/L4) |
| Shield Advanced | Enhanced detection, SRT, cost protection, richer metrics |
| Protectable | CloudFront, Route 53, Global Accelerator, ALB/CLB/NLB, Elastic IPs (EC2/NLB patterns) |
| Application layer | Pair with AWS WAF on supported resources |
| SRT | Shield Response Team — proactive engagement with business support-style readiness |
| Tooling | `aws shield` CLI, Console, CloudWatch `AWS/DDoSProtection`, Firewall Manager |

## Workflow

### 1. Confirm scope and success criteria

1. Business-critical public endpoints, RTO/RPO for availability, on-call roster, authorization for SRT data sharing.
2. Success: all critical resources protected; alarms route to on-call; runbook exercised in tabletop.
3. Clarify whether Global Accelerator / multi-region failover is in scope.

### 2. Inventory exposure and protections

```bash
aws sts get-caller-identity
aws shield get-subscription-state
aws shield list-protections
aws shield list-protected-resources
aws cloudfront list-distributions --query "DistributionList.Items[].{Id:Id,Domain:DomainName,Aliases:Aliases}"
aws elbv2 describe-load-balancers --query "LoadBalancers[].{Arn:LoadBalancerArn,Scheme:Scheme,DNS:DNSName}"
```

1. List public EIPs and DNS apex records that must stay up.
2. Note existing WAF WebACLs attached to CloudFront/ALB.
3. Confirm Enterprise/Business support level expectations for SRT.

### 3. Baseline metrics and architecture

1. Capture normal traffic patterns (requests, bandwidth, SYN, 4xx/5xx).
2. Document origin hardening: private ALB, CloudFront-only SG/prefix, no open origins.
3. Identify single points of failure (one region ALB, single EIP app).

### 4. Enable protections and detection

```bash
# Example: protect a CloudFront distribution (IDs are illustrative)
aws shield create-protection \
  --name "cf-prod-edge" \
  --resource-arn "arn:aws:cloudfront::123456789012:distribution/EDFDVBD6EXAMPLE"

# Associate health check for health-based detection where applicable
aws shield associate-health-check \
  --protection-id "$PROTECTION_ID" \
  --health-check-arn "arn:aws:route53:::healthcheck/..."
```

1. Enable proactive engagement contacts if your support tier and process allow.
2. Ensure AWS WAF rate-based rules and managed groups cover L7 floods; Shield does not replace app auth.
3. Use Firewall Manager for org-wide Shield Advanced policy if multi-account.
4. Document emergency: contact SRT, elevate case, temporary WAF blocks, scale origins, DNS failover.

### 5. Verify with evidence

```bash
aws shield describe-protection --protection-id "$PROTECTION_ID"
aws shield list-attacks --start-time startTime=1700000000 --end-time endTime=1700003600
aws cloudwatch list-metrics --namespace AWS/DDoSProtection
```

1. Tabletop: who pages, who talks to SRT, who freezes deploys, who updates status page.
2. Confirm CloudWatch alarms on `DDoSDetected` / volumetric metrics (names vary by resource).
3. Confirm cost protection understanding with FinOps (eligible charges during attacks).

### 6. Observe and harden

1. Continuous protection inventory drift: new public ALB without protection.
2. Review attack reports post-event; add WAF rules for recurring patterns.
3. Keep origin locked down so attackers cannot bypass CloudFront/Shield path.

### 7. Hand off

1. Living runbook: contacts, protection IDs, WAF WebACL IDs, status page owner.
2. Quarterly tabletop + after-action reviews.
3. Link bot/L7 skill for application abuse distinct from volumetric DDoS.

## Architecture Checklist

| Layer | Control |
| --- | --- |
| DNS | Route 53 + health checks; multi-value / failover as designed |
| Edge | CloudFront/GA + Shield Advanced + WAF |
| Load balancer | Protected ALB/NLB; no unnecessary public listeners |
| Origin | SG limited to edge / prefix lists; least ports |
| App | Auth, rate limits, bot control, graceful degradation |
| Ops | Alarms, SRT process, comms templates |

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Coverage | All critical public ARNs protected | Only “main” CF; forgotten regional EIP |
| Origins | Not directly reachable from Internet | Open SG to world “for debugging” |
| L7 | WAF + app rate limits | Expect Shield alone to stop credential stuffing |
| Process | Named SRT/on-call owners | “Someone will notice downtime” |
| Testing | Authorized game days | Unannounced attacks on prod |

## Output Checklist

- [ ] Subscription state and billing owner confirmed
- [ ] Critical public resources inventoried
- [ ] Protections created/verified for each critical ARN
- [ ] Health checks associated where appropriate
- [ ] WAF/edge/origin hardening aligned
- [ ] CloudWatch alarms and on-call routing tested
- [ ] SRT/proactive engagement contacts documented
- [ ] DDoS runbook and tabletop completed
- [ ] Drift monitoring for new public endpoints
- [ ] `code-quality-standards` applied if automation shipped

## Rules

- Defensive use on authorized resources only — never attack third parties.
- Shield Advanced complements, not replaces, WAF and secure architecture.
- Keep SRT contact data and architecture diagrams access-controlled.
- Review protection inventory after every major network change.
- Prefer evidence from AWS attack reports over speculation.

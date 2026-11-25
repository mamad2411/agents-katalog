---
name: cdn-waf-bypass-awareness
description: >
  Awareness of CDN/WAF bypass patterns for defending owned origins: origin IP exposure,
  direct-connect gaps, alternate hosts, path normalization differentials, and header
  trust issues. Use when hardening origin allowlists, reviewing Cloudflare/Fastly/Akamai
  + origin setups, or authorized bypass testing on your stack — not for attacking third parties.
---

# Cdn Waf Bypass Awareness

## Scope And Authorization

- **In scope:** Your CDN/WAF and origins; authorized defensive testing on owned assets.
- **Out of scope:** Bypassing third-party WAFs to attack sites you do not own.
- Goal: **close** bypasses, not publish exploit kits.
- Pair with `cdn-cache-key-design`, origin hardening, `ssrf-server-side-request-forgery` when relevant.

## When To Use

- Deploying CDN/WAF in front of origin and needing “origin only accepts CDN” assurance.
- Incident: attackers hit origin IP directly.
- Reviewing header trust (`X-Forwarded-For`, `True-Client-IP`) for spoofing.
- Authorized purple-team of your edge rules.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| CDN cache keys | `cdn-cache-key-design` |
| App WAF rule writing deep | WAF vendor skills |
| Generic SSRF | `ssrf-server-side-request-forgery` |
| TLS cert management | cert-manager skills |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Bypass class | Defense direction |
| --- | --- |
| Origin IP disclosure | DNS history, cert SANs, leaks → rotate + firewall |
| Direct origin hit | Allowlist CDN egress IPs / mTLS / authenticated origin pulls |
| Alternate domains | Old hosts, default URLs, staging | Inventory + same policy |
| Path normalization | `%2e%2e`, `//`, case | Normalize at edge + origin consistently |
| Scheme/host confusion | HTTP on origin, wrong SNI | Force HTTPS; validate Host |
| Header spoof | Client-supplied forwarding headers | Trust only CDN-to-origin connection |

## Workflow

### 1. Confirm scope and success criteria

1. Edge providers, origin types (LB, K8s, object storage), RoE for testing.
2. Success: unauthenticated Internet cannot reach origin app ports; tests from non-CDN IPs fail; docs for IP allowlist maintenance.
3. Staging first for any blocking changes.

### 2. Discover origin exposure (authorized)

```bash
# Passive / careful active on your assets only
dig +short origin-likely.example.com
# Historical DNS / cert transparency for your domains (defensive inventory)
# Check if origin answers on public IP
curl -sI --resolve app.example.com:443:$ORIGIN_IP https://app.example.com/ || true
```

1. Search config repos for origin hostnames, raw IPs in docs.
2. Cloud metadata: security groups open 80/443 to `0.0.0.0/0` behind CDN.
3. Subdomain takeover / stale origins list.

### 3. Lock down origin

| Control | Notes |
| --- | --- |
| SG/NSG/firewall | Only CDN IP ranges (vendor published list automation) |
| Authenticated origin | Cloudflare authenticated origin pull / mTLS |
| Shared secret header | Weak alone if origin still public — combine with IP allowlist |
| Private origin | VPC private + CDN private connectivity where available |
| Disable direct DNS | No public A record to origin |

```bash
# After lockdown: from Internet host without CDN
curl -sI https://$ORIGIN_IP/  # expect timeout/refuse
```

1. Automate CDN IP range updates (AWS prefix lists, cron scripts) — stale lists break prod.
2. Prefer mTLS over static secret headers when supported.

### 4. Review edge/origin differentials

1. Path normalization: send path variants in **authorized** tests; compare edge block vs origin accept.
2. HTTP/2 vs HTTP/1 smuggling-ish differentials — hand to HTTP desync skills if suspected.
3. Cache poisoning keys — `cdn-cache-key-design`.
4. Bypass via alternate ports (8080 open) or country-specific POPs misconfig.

### 5. Header trust model

```text
Internet client → CDN/WAF → Origin
Origin must NOT trust client-controlled X-Forwarded-For without CDN validation
```

1. At origin, use connection client IP only if it is CDN, then read CDN’s trusted client IP header set by CDN.
2. Strip client-supplied spoof headers at CDN.
3. App rate limits and auth logs use real client IP post-CDN.

### 6. Authorized test checklist

| Test | Expected after hardening |
| --- | --- |
| Direct origin IP HTTPS | Fail |
| Secret header from Internet to origin IP | Fail (IP allowlist) |
| Old staging hostname | Protected or offline |
| Blocked payload via CDN | Blocked |
| Same payload direct (should not reach) | N/A / fail connect |
| Spoof `X-Forwarded-For: 127.0.0.1` | No privilege gain |

Document results for compliance evidence.

### 7. Hand off

1. Runbook: update CDN IP allowlists; origin cert rotation with mTLS.
2. Continuous: attack surface monitoring for origin IP leaks.
3. Alert on origin traffic not matching CDN ASN/header patterns.
4. Apply `code-quality-standards` to automation.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Origin | Private + allowlist/mTLS | Public origin “behind CDN” only by DNS |
| Secret header | Plus network allowlist | Header alone world-open |
| IP lists | Automated updates | Manual yearly paste |
| Host header | Allowlist virtual hosts | Default vhost serves app |
| Testing | Owned assets + RoE | Random WAF bypass on third parties |
| Logs | Real client IP via trusted path | Trust raw XFF from clients |

## Output Checklist

- [ ] Origin inventory and public exposure checked
- [ ] Firewall/mTLS/authenticated origin applied
- [ ] Direct-IP access verified blocked
- [ ] Header trust model documented
- [ ] Normalization differentials reviewed
- [ ] Alternate hostnames covered
- [ ] IP range update automation
- [ ] Alerts for non-CDN origin traffic
- [ ] Authorized test evidence stored
- [ ] IaC follows `code-quality-standards`

## Rules

- Defensive hardening and authorized testing only.
- CDN is not protection if origin is world-open.
- Do not teach third-party attack recipes; focus on closing gaps.
- Keep vendor IP allowlists fresh.
- Cache and WAF policy details may need sibling skills.

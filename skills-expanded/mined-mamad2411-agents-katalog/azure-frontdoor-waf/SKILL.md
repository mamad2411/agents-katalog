---
name: azure-frontdoor-waf
description: >
  Azure Front Door (Standard/Premium) WAF policies for owned applications: managed
  rule sets, custom rules, bot manager (SKU-dependent), rate limiting, exclusion
  lists, Detection vs Prevention mode, and logging to Log Analytics. Use when
  protecting public origins behind Front Door — not for attacking third-party sites
  or bypassing WAF without authorization.
---

# Azure Front Door WAF

## Scope And Authorization

- **In scope:** Front Door profiles, endpoints, and WAF policies in tenants you own or are authorized to harden.
- **Out of scope:** Offensive testing of third-party Front Door endpoints; disabling WAF in prod without ticket.
- Prefer Detection mode baseline before Prevention; false positives can block customers.
- Pair origin hardening with private link/origins; `code-quality-standards` for IaC.

## When To Use

- Attaching WAF policy to Front Door custom domains/routes.
- Tuning OWASP managed rules, bot protection, geo/IP custom rules.
- Investigating blocked requests via WAF logs (`AzureDiagnostics` / resource-specific tables).
- Migrating Application Gateway WAF concepts to Front Door edge.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| AWS WAF Bot Control | `aws-waf-bot-control` |
| Blob public access | `azure-blob-misconfig` |
| NSG east-west controls | `azure-nsg-review` |
| Authorized CAPTCHA research | `captcha-bypass-research` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Topic | Guidance |
| --- | --- |
| SKU | Premium unlocks richer managed rules / bot features vs Standard — verify current SKU matrix |
| Policy modes | Detection (log only) vs Prevention (enforce) |
| Managed rules | Default Microsoft rule sets; version pin and drift review |
| Custom rules | IP match, geo, rate limit, session attributes — higher priority evaluation order |
| Exclusions | Selective match variable exclusions for false positives |
| Tooling | `az network front-door waf-policy` / AFD CLI, Portal, Log Analytics, Sentinel |

## Workflow

### 1. Confirm scope and success criteria

1. Front Door profile, endpoints, routes, origins, environments, authorization.
2. Success: WAF associated; Detection baseline done; Prevention on with acceptable FP rate; logs queryable.
3. Origin locked so clients cannot bypass Front Door (Private Link / IP allowlist).

### 2. Inventory Front Door and WAF

```bash
az account show
az afd profile list -g "$RG" -o table
az afd endpoint list --profile-name "$PROFILE" -g "$RG" -o table
az network front-door waf-policy list -g "$RG" -o table
az network front-door waf-policy show -g "$RG" -n "$WAF" -o jsonc
```

1. Note policy mode, rule set versions, custom rules order.
2. Confirm security policy association on domains/routes.
3. Check logging destination (workspace ID).

### 3. Baseline in Detection

1. Attach policy in **Detection**; collect 7 days of traffic samples if possible.
2. Query top rule IDs, paths, and client ASNs.
3. Identify legitimate automation (payment, health, partners) for allow rules.

### 4. Configure managed + custom rules

```bash
# Create policy in Detection first
az network front-door waf-policy create -g "$RG" -n "$WAF" \
  --sku Premium_AzureFrontDoor \
  --mode Detection

# Managed rule set (names/versions — confirm current)
az network front-door waf-policy managed-rules add -g "$RG" -n "$WAF" \
  --type Microsoft_DefaultRuleSet --version 2.1 --action Block

# Example custom rate limit (illustrative parameters)
az network front-door waf-policy rule create -g "$RG" -n "$WAF" \
  --name RateLimitLogin --priority 100 --rule-type RateLimitRule \
  --action Block --rate-limit-duration 1 --rate-limit-threshold 100 \
  --defer  # complete match conditions per CLI help

# Associate via security policy on AFD (CLI surface evolves — use Portal/Bicep if needed)
```

1. Add allowlist custom rules **before** broad blocks (priority numbers).
2. Use exclusions for known false positive fields (e.g. body field with SQL-like content in CMS).
3. Bot manager rules (Premium): start with log/challenge behaviors per feature set.
4. Switch to **Prevention** after sign-off; monitor closely for 48h.

### 5. Verify with evidence

```bash
# Kusto (Log Analytics) — table names vary by diagnostic setting
# AzureDiagnostics | where Category contains "FrontDoor" or Category contains "FrontdoorWebApplicationFirewallLog"
# | summarize count() by action_s, ruleName_s
curl -sI "https://$ENDPOINT_HOST/" | head -n5
# Authorized negative test only on owned apps
```

1. Blocked malicious probe (lab payloads) shows action Block.
2. Critical user journeys succeed (login, checkout).
3. Bypass check: origin rejects direct Internet hits if designed private.

### 6. Observe and harden

1. Dashboards: blocked vs allowed, top rules, challenge rates.
2. Alert on sudden Block spikes (self-DoS) and on WAF policy deletions.
3. Quarterly rule set version upgrades in nonprod first.

### 7. Hand off

1. Policy catalog: priorities, exclusions, owners, mode.
2. FP handling process (ticket → exclusion → expiry).
3. Bicep/Terraform for policy + association.

## Mode Rollout

| Stage | Mode | Actions |
| --- | --- | --- |
| 1 | Detection | Managed rules on, monitor only |
| 2 | Detection | Custom rate limits in log |
| 3 | Prevention | Enforce with allowlists ready |
| 4 | Prevention | Tighten bots/geo; remove temp exclusions |

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Rollout | Detection → Prevention | Prevention big-bang on prod Friday |
| Origins | Private Link / restricted | Public origin bypasses WAF |
| Exclusions | Field-scoped + expiry | Disable entire rule set |
| Logging | Resource-specific tables + retention | No logs, guess FPs |
| Rate limits | On login/search paths | Global 10 rps breaking mobile |

## Output Checklist

- [ ] Front Door endpoints and origins inventoried
- [ ] WAF policy created and associated
- [ ] Detection baseline analyzed
- [ ] Managed + custom rules tuned
- [ ] Prevention enabled with owner approval
- [ ] Logs and alerts verified
- [ ] Origin bypass mitigated
- [ ] Exclusion register with expiry
- [ ] `code-quality-standards` applied to IaC

## Rules

- Authorized applications only.
- Progressive enforcement; track false positives.
- WAF is not a substitute for secure app code.
- Keep origins non-bypassable.
- Redact sensitive URL/query data in exported logs.

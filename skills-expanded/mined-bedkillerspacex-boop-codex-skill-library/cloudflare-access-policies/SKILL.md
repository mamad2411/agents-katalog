---
name: cloudflare-access-policies
description: >
  Design Cloudflare Zero Trust Access policies: applications, IdP integration,
  allow/deny/bypass rules, device posture, service tokens, and session duration.
  Use for owned Cloudflare Zero Trust when protecting internal apps or admin paths —
  not for bypassing Access on systems you do not administer.
---

# Cloudflare Access Policies

## Scope And Authorization

- **In scope:** Cloudflare accounts/zones and apps you own or administer.
- **Out of scope:** attacking Access-protected third-party apps; sharing service tokens broadly.
- Prefer staging Access apps before production lockout.
- Redact service token clients secrets and JWT signing material.
- Pair with `cloudflare-tunnel-ops` when origins are tunneled.

## When To Use

- Putting admin UIs, staging, or internal tools behind **Cloudflare Access**.
- Writing policy rules (emails, groups, geo, IP, device posture, IdP claims).
- Service-to-service access via **service tokens** or mTLS.
- Tokens: Cloudflare Access, Zero Trust, application policy, WARP, service token, IdP.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Tunnel / cloudflared install | `cloudflare-tunnel-ops` |
| Workers bindings/secrets | `cloudflare-workers-bindings` |
| R2 public buckets | `cloudflare-r2-public-access` |
| Generic SSO/SAML deep dive | `saml-sso-basics` |
| WAF rule engineering alone | WAF skill / CF WAF docs |

## Building Blocks

| Object | Role |
| --- | --- |
| Identity provider | SSO source (Google, Okta, Azure AD, One-time PIN, etc.) |
| Application | Hostname/path protected by Access |
| Policy | Ordered rules: include / require / exclude |
| Action | Allow, Block, Bypass, Service Auth |
| Session | JWT cookie lifetime / refresh |
| Device posture | WARP + posture integrations |

## Workflow

### 1. Confirm scope and success criteria

1. App hostnames, user populations, break-glass accounts, IdP owner.
2. Success: only intended identities reach origin; logs show denies; automation uses service auth not shared passwords.
3. Rollback: temporary Bypass policy with ticket + expiry (never silent permanent Bypass).

### 2. Inventory

```bash
# Terraform / dashboard inventory preferred
# Example: list via API with scoped token (redact output)
curl -s -H "Authorization: Bearer $CF_API_TOKEN" \
  "https://api.cloudflare.com/client/v4/accounts/$ACCOUNT_ID/access/apps" | jq '.result[].name'
```

1. Map DNS (proxied) → origin (tunnel or public).
2. Existing Bypass rules and IP allowlists (risk).

### 3. Design policy model

| Audience | Policy pattern |
| --- | --- |
| Employees | Allow corporate email / IdP group + optional WARP |
| Admins | Stricter group + device posture + shorter session |
| CI / bots | Service token or mTLS; never long-lived user JWT in CI logs |
| Vendors | Time-boxed list / temporary group |
| Public health | Bypass only for specific paths if unavoidable |

**Rule order mental model:** evaluate includes/requires carefully; deny by default when no allow matches.

### 4. Implement

1. Create Access application for `admin.example.com` (self-hosted) or SaaS app type as applicable.
2. Attach IdP; enforce org-only domains.
3. Policies:
   - Allow: `group = eng-admin` AND `country ≠ high-risk` (as policy requires)
   - Require: device posture healthy (if licensed/configured)
   - Block: everyone else
4. Session duration: short for admin; configure re-auth for sensitive apps.
5. **Origin trust:** prefer tunnel + **Cloudflare origin cert** or authenticated origin pulls so Access cannot be bypassed via direct origin IP.
6. Service tokens: create per automation identity; store client id/secret in vault; rotate.

### 5. Verify

```bash
# Unauthenticated browser: Access login wall
# Unauthorized user: denied
# Authorized user: app loads; Cf-Access-Jwt-Assertion present at origin (if validated)
# Direct origin IP (should fail if origin locked): connection denied
```

1. Prove Bypass not present on admin app.
2. Prove expired service token fails.
3. Check Access audit logs for test events.

### 6. Operate

1. Alert on anomalous Access failures / new Bypass policies.
2. Quarterly review: service tokens, group membership, Bypass exceptions.
3. Document break-glass IdP account with hardware key.

### 7. Hand off

1. Policy-as-code (Terraform) preferred for reviewable diffs.
2. Runbook: add user, revoke user, rotate service token, origin IP leak response.
3. Link tunnel ops if `cloudflared` fronts the app.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Default | Deny unless allow match | Global Bypass |
| Origin | Tunnel + no public origin | Access on orange-cloud only, origin open |
| Bots | Service tokens | Shared employee login in CI |
| Sessions | Short admin sessions | Infinite session on payroll |
| Changes | Terraform + PR | Clickops without audit |

## Output Checklist

- [ ] Apps and audiences listed
- [ ] IdP and groups verified
- [ ] Policies implemented (allow/require/block)
- [ ] Origin not bypassable via direct IP
- [ ] Service tokens inventoried and vaulted
- [ ] AuthZ allow/deny tests evidenced
- [ ] Audit log review path set
- [ ] Bypass exceptions ticketed with expiry
- [ ] Break-glass documented

## Rules

- Administer only owned CF Zero Trust orgs.
- Never commit service token secrets.
- Prefer reversible policy with staged enforcement.
- Focus on **Access policies**; tunnel/WAF/R2 are sibling skills.

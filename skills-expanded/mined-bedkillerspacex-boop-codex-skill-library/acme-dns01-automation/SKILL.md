---
name: acme-dns01-automation
description: >
  Automate ACME DNS-01 certificate issuance and renewal for owned zones: TXT hooks,
  provider APIs, propagation waits, wildcards, multi-name certs, cleanup, staging, and
  rate-limit safety. Use when wiring Certbot, lego, acme.sh, Caddy, or Traefik DNS-01
  solvers; debugging _acme-challenge TXT failures; choosing DNS API scopes; or automating
  wildcard TLS without opening HTTP-01 on port 80 — not for third-party zone takeover
  or unowned ACME/DNS accounts.
---

# ACME DNS-01 Automation

## Scope And Authorization

- **In scope:** DNS zones and ACME accounts you own or operate under authorization.
- **Out of scope:** Creating `_acme-challenge` records in zones you do not control; certificate issuance for domains you do not own.
- Prefer **Let's Encrypt staging** (or other CA staging) until the flow is green.
- Protect DNS API tokens like production secrets; scope them to TXT edit on challenge names only when the provider allows.
- Pair automation code with `code-quality-standards` and `secrets-management-hygiene`.

## When To Use

- Issuing **wildcard** certs (`*.example.com`) requiring DNS-01.
- Hosts without inbound :80/:443 for HTTP-01 (private networks, batch jobs).
- Multi-name certificates spanning zones with API-driven DNS.
- Debugging intermittent propagation failures or stale TXT records.
- Migrating from manual DNS updates to Certbot/lego/acme.sh/Caddy/Traefik.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| General DNSSEC/CAA hygiene | DNS / catalog DNS skills |
| HTTP-01 only simple web servers | Server TLS runbooks / reverse-proxy skills |
| Azure/other cloud-specific edge certs without ACME | Cloud cert skills as applicable |
| Container registry trust | `acr-content-trust` |
| Secrets inventory program | `secrets-management-hygiene` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Concept | Detail |
| --- | --- |
| DNS-01 | Prove control by publishing `TXT` at `_acme-challenge.<name>` |
| Order | ACME client creates order → challenge token → DNS set → finalize |
| Propagation | Authoritative vs recursive visibility; TTLs; multi-NS lag |
| Wildcard | Must use DNS-01; `*.example.com` + often `example.com` SAN |
| CAA | Zone may restrict which CAs can issue |
| Rate limits | Failed validations and duplicate certs count against CA limits |
| Cleanup | Remove TXT after validation to reduce attack clutter |

## Workflow

### 1. Confirm zone ownership and success criteria

1. Record domains, registrar/DNS provider, ACME CA (LE/ZeroSSL/private), cert destinations (LB, ingress, disk).
2. Success: staging cert issued; production cert renews unattended; TXT cleaned up; monitoring on expiry.
3. Verify public CAA allows your CA: `dig CAA example.com`.

### 2. Least-privilege DNS credentials

| Provider pattern | Prefer |
| --- | --- |
| Scoped API token | TXT create/delete on `_acme-challenge.*` only |
| Separate “ACME” zone/user | No apex A/NS change rights |
| Split horizon | Ensure challenge published where CA resolvers see it |

```bash
# Store tokens in secret manager / env — never commit
export DO_AUTH_TOKEN=...          # example provider
export AWS_ACCESS_KEY_ID=...      # Route53 IAM user limited to hosted zone
```

1. IAM/API policies: deny zone delete and NS changes.
2. Rotate tokens on a schedule; audit who can read them in CI.

### 3. Dry-run on staging ACME

**Certbot manual (debug):**

```bash
certbot certonly --manual --preferred-challenges dns \
  --test-cert \
  -d 'example.com' -d '*.example.com' \
  --manual-public-ip-logging-ok
# Place TXT as instructed; verify before continue
```

**lego (API example shape):**

```bash
lego --email ops@example.com --dns route53 -d 'example.com' -d '*.example.com' \
  --server https://acme-staging-v02.api.letsencrypt.org/directory \
  run
```

**acme.sh:**

```bash
acme.sh --issue --dns dns_cf -d example.com -d '*.example.com' --staging
```

### 4. Propagation and verification

```bash
# Check authoritative NS (replace ns-xx)
dig +short TXT _acme-challenge.example.com @ns1.provider.example
# Check public resolvers
dig +short TXT _acme-challenge.example.com @1.1.1.1
dig +short TXT _acme-challenge.example.com @8.8.8.8
```

1. Wait for **all** authoritative NS to agree before ACME poll.
2. Configure client `--dns-propagation-seconds` / provider wait hooks appropriately (often 30–120s+).
3. If using CNAMEs to a dedicated challenge zone (`_acme-challenge.example.com CNAME to acme.example.net`), ensure the client writes the **target** zone.

### 5. Production automation patterns

| Runtime | Pattern |
| --- | --- |
| Cron + certbot/lego | Deploy hook reloads nginx/haproxy |
| Kubernetes | `cert-manager` DNS01 solver with scoped secrets |
| Caddy | `dns` provider modules; automatic renew |
| Traefik | CertificatesResolvers with DNS challenge |

**Post-issue hook sketch:**

```bash
#!/usr/bin/env bash
set -euo pipefail
install -m 600 fullchain.pem /etc/ssl/app/fullchain.pem
install -m 600 privkey.pem /etc/ssl/app/privkey.pem
systemctl reload nginx
```

1. Renew at ~30 days remaining; randomize cron minutes.
2. Alert if cert expiry &lt; 14 days (`openssl x509 -enddate -noout -in fullchain.pem`).
3. Keep private keys mode `600` / secret store; never log keys.

### 6. Failure diagnosis table

| Symptom | Checks |
| --- | --- |
| NXDOMAIN on challenge | Wrong zone, typo, API wrote different account |
| Old TXT still present | Cleanup failed; multiple concurrent issues |
| ServFail / timeout | Provider lag; increase wait; NS inconsistency |
| CAA error | Add/fix CAA for your CA |
| Rate limited | Use staging; avoid re-issue loops; respect CA limits |
| Wildcard mismatch | Names must match order; include apex if needed |

### 7. Hand off

1. Document provider, secret location, renew unit/cron, reload hook, and owner.
2. Runbook: emergency re-issue, token rotation, CA outage fallback.
3. Remove staging certs from prod trust stores if mistakenly mixed.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Credentials | TXT-only token in vault | Global DNS admin key in git |
| Testing | Staging ACME first | Burn prod rate limits debugging |
| Propagation | Wait on authoritative NS | Sleep 5s and hope |
| Cleanup | Delete TXT after success | Leave challenge tokens forever |
| Wildcards | DNS-01 + monitored renew | Manual yearly copy-paste |

## Output Checklist

- [ ] Zone ownership and CAA verified
- [ ] Least-privilege DNS credentials stored safely
- [ ] Staging issuance succeeded for all names
- [ ] Propagation strategy validated with dig
- [ ] Production renew automation + reload hook
- [ ] Expiry monitoring/alerts configured
- [ ] TXT cleanup confirmed
- [ ] Rate-limit and failure runbook written
- [ ] Secrets not in repo; `code-quality-standards` on hooks

## Rules

- Only automate ACME for domains you control.
- Never commit ACME account keys or DNS tokens.
- Prefer staging until green; respect CA rate limits.
- DNS-01 tokens prove domain control — protect write access carefully.
- Route non-ACME TLS or registry signing to other skills.

---
name: cert-manager-http01-dns01
description: >
  cert-manager ACME HTTP-01 and DNS-01 solvers for owned domains: ingress-based HTTP
  challenges, DNS provider credentials, wildcard certs, multi-solver selectors, and
  debugging stuck Challenges. Use when HTTP-01 failing, DNS-01 Route53/Cloud DNS,
  wildcard Certificate, or solver selection — pair with `cert-manager-basics`.
---

# Cert Manager Http01 Dns01

## Scope And Authorization

- **In scope:** Domains, DNS zones, and clusters you control.
- **Out of scope:** Pointing challenges at third-party domains; over-privileged DNS tokens beyond need.
- DNS credentials can often rebind zones — store as Secrets with least privilege.
- Pair with `cert-manager-basics`.

## When To Use

- Choosing between HTTP-01 and DNS-01 for ACME.
- Issuing **wildcard** certificates (requires DNS-01).
- Debugging `Challenge` pending/invalid, 404 on `/.well-known/acme-challenge`.
- Multi-tenant clusters needing solver selectors per DNS zone.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| cert-manager install/Certificate CRDs | `cert-manager-basics` |
| Public CT monitoring | `certificate-transparency-basics` |
| Manual openssl certs | TLS admin skills |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Solver | Works when | Cannot |
| --- | --- | --- |
| HTTP-01 | Port 80 reachable on auth domain; ingress routes challenge | Wildcards; pure private offline HTTP |
| DNS-01 | API to create TXT `_acme-challenge` | Without DNS API credentials |

## Workflow

### 1. Confirm scope and success criteria

1. Domains, wildcard needs, CDN-in-front complications, DNS provider.
2. Success: Order valid; Certificate Ready; least-priv DNS IAM; staging tested.
3. Note CDN: HTTP-01 must reach challenge responder (bypass cache/WAF carefully).

### 2. Choose solver

| Scenario | Prefer |
| --- | --- |
| Single public site, no wildcards | HTTP-01 |
| Wildcards `*.example.com` | DNS-01 |
| Private only services with public DNS | DNS-01 |
| Many domains on one ingress | HTTP-01 with correct class |
| Split DNS zones | Solver `selector` dnsZones |

### 3. HTTP-01 setup

```yaml
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: le-http01
spec:
  acme:
    server: https://acme-staging-v02.api.letsencrypt.org/directory
    email: sre@example.com
    privateKeySecretRef:
      name: le-http01-account
    solvers:
      - http01:
          ingress:
            class: nginx   # or ingressTemplate / gateway variants per version
```

**Checks:**

1. From Internet: `http://domain/.well-known/acme-challenge/<token>` must return key auth (during challenge).
2. No forced HTTPS redirect that breaks challenge without exception.
3. WAF/CDN allowlist ACME paths; cache bypass for challenge path.
4. Correct ingress class; no conflicting Ingress rules.

```bash
kubectl get challenges.acme.cert-manager.io -A
kubectl describe challenge -n app NAME
```

### 4. DNS-01 setup

```yaml
solvers:
  - dns01:
      route53:
        region: us-east-1
        hostedZoneID: ZXXXXXXXX
        # prefer IRSA/workload identity over static keys
    selector:
      dnsZones:
        - example.com
```

**Provider notes (conceptual):**

| Provider | Least privilege idea |
| --- | --- |
| Route53 | `change` only on specific hosted zone |
| Google Cloud DNS | `dns.resourceRecordSets.*` on zone |
| Cloudflare | Zone DNS edit token, not global key |
| Azure DNS | Zone contributor scoped |

1. Never commit access keys; use mounted Secrets / IRSA.
2. Propagation time: increase `propagationTimeout` / `pollingInterval` if needed for slow DNS.
3. Split-horizon DNS: ACME validation uses **public** resolvers — public TXT must be visible.

### 5. Wildcard certificates

```yaml
spec:
  dnsNames:
    - example.com
    - "*.example.com"
  issuerRef:
    name: le-dns01
    kind: ClusterIssuer
```

1. Requires DNS-01.
2. Consider security of wildcard private keys (blast radius).
3. Separate certs per app when least privilege preferred over one mega-wildcard.

### 6. Multi-solver selection

```yaml
solvers:
  - selector:
      dnsZones: ["example.com"]
    dns01: { route53: { ... } }
  - selector:
      dnsZones: ["other.org"]
    dns01: { cloudflare: { ... } }
  - http01:
      ingress: { class: nginx }
```

1. More specific selectors first — read cert-manager selection rules for your version.
2. Test each zone independently on staging ACME.

### 7. Troubleshoot and verify

| Issue | HTTP-01 | DNS-01 |
| --- | --- | --- |
| 404 challenge | Ingress path/class, CDN | N/A |
| NXDOMAIN TXT | N/A | Wrong zone/creds/propagation |
| Unauthorized | N/A | IAM/token scope |
| Rate limit | Both — use staging | Both |
| Stuck pending | Events + controller logs | Same |

```bash
# DNS-01 visibility
dig TXT _acme-challenge.www.example.com +short
# After success
kubectl get certificate -A
openssl s_client -connect www.example.com:443 -servername www.example.com </dev/null 2>/dev/null | openssl x509 -noout -dates -subject
```

### 8. Hand off

1. Document solver per domain zone; secret rotation for DNS tokens.
2. Alerts on Challenge failures.
3. Promote staging issuer config to prod ACME URL.
4. Apply `code-quality-standards` to manifests; restrict Secret access.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Wildcards | DNS-01 + scoped IAM | HTTP-01 attempts for `*.domain` |
| CDN | Challenge path bypass | Cached 404 on ACME path |
| Creds | Zone-scoped + IRSA | Global DNS admin key in git |
| Testing | Staging ACME | Prod LE from broken loops |
| Selectors | Explicit dnsZones | One wrong solver for all domains |
| Redirects | ACME exception on HTTP | Global HTTPS redirect breaks HTTP-01 |

## Output Checklist

- [ ] Solver choice justified (HTTP vs DNS, wildcards)
- [ ] Staging ACME success for each domain class
- [ ] HTTP-01 Internet reachability verified OR DNS-01 TXT public
- [ ] DNS credentials least-privilege and not in git
- [ ] Selectors correct for multi-zone
- [ ] Wildcard risk accepted if used
- [ ] Challenges cleaned up / Orders valid
- [ ] Prod issuer cutover done
- [ ] Runbook for stuck challenges
- [ ] `cert-manager-basics` install health OK

## Rules

- Only solve challenges for domains you control.
- Least-privilege DNS credentials mandatory.
- Staging first; respect ACME rate limits.
- CDN/WAF must not break HTTP-01.
- Certificate object lifecycle → `cert-manager-basics`.

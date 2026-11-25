---
name: certificate-expiry-page
description: >
  User-facing and ops handling of TLS certificate expiry for owned sites: monitoring
  before expiry, graceful maintenance pages, HSTS caveats, client error UX, and
  emergency re-issue. Use when cert expiring, browser NET::ERR_CERT_DATE_INVALID UX,
  status page during TLS outage, or expiry runbooks — not for breaking others' TLS.
---

# Certificate Expiry Page

## Scope And Authorization

- **In scope:** Sites, APIs, and cert inventory you operate.
- **Out of scope:** Causing or exploiting expiry on third-party systems.
- HSTS and pinned clients make “just show an HTML page” harder during bad TLS — plan ahead.
- Pair with `cert-manager-basics`, `certificate-transparency-basics`, load balancer cert ops.

## When To Use

- Designing monitoring and runbooks so certs never expire silently.
- Providing status/maintenance communication when TLS fails.
- Emergency response when a cert already expired.
- Multi-domain SANs / multi-LB inventories that drift from auto-renew.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Automated issuance in K8s | `cert-manager-basics`, `cert-manager-http01-dns01` |
| CT log monitoring for mis-issuance | `certificate-transparency-basics` |
| General nginx TLS headers | `nginx-security-headers` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Layer | Expiry concern |
| --- | --- |
| Edge cert (CDN/LB) | Public users hit browser errors |
| Origin cert | CDN origin pull failures |
| mTLS client/server | App-to-app outages |
| Mobile pinning | Hard fail even after fix if pin wrong |
| HSTS | Users cannot click through easily |

## Workflow

### 1. Confirm scope and success criteria

1. Inventory all public hostnames and cert sources (ACM, cert-manager, DigiCert, etc.).
2. Success: alert at 30/14/7 days; auto-renew works; emergency re-issue < X minutes; status comms templates ready.
3. Owners per certificate family.

### 2. Inventory certificates

```bash
# Sample public endpoints
for h in www.example.com api.example.com; do
  echo "==== $h"
  echo | openssl s_client -connect "$h:443" -servername "$h" 2>/dev/null | openssl x509 -noout -dates -subject -ext subjectAltName
done
# Cloud examples
aws acm list-certificates --query 'CertificateSummaryList[].DomainName'
kubectl get certificates -A
```

1. Include forgotten hosts: old marketing domains, partner CNAMEs, admin panels.
2. Store notAfter in CMDB/monitor.

### 3. Monitoring (primary defense)

| Check | Target |
| --- | --- |
| Blackbox/exporter | Probe TLS notAfter |
| cert-manager metrics | Certificate expiry gauge |
| ACM/Azure/GCP cert age | Native metrics/alarms |
| Synthetic | Full HTTPS journey |

```yaml
# Prometheus blackbox-style intent
# alert: CertExpirySoon when probe_ssl_earliest_cert_expiry - time() < 14*24*3600
```

1. Page at 7 days for public prod; ticket at 30.
2. Test alert pipelines quarterly (not only real expiry).

### 4. “Expiry page” reality check

When cert is **already invalid**, browsers show interstitial — **your origin HTML may never render**.

**What still works:**

1. **Out-of-band status page** on a **different domain/provider** with valid cert (status.example.com / Statuspage).
2. **DNS/email/social** comms.
3. **App store / in-app** messages for mobile if API host broken.
4. **Corporate** push via MDM for internal apps.

**What often fails:**

1. Same-domain `/maintenance.html` during expired cert.
2. Users “click through” under HSTS — they cannot.
3. API clients — no human page at all; need client-friendly error codes once TLS restored.

**Design for prevention**, and for **comms channels that do not depend on the broken cert**.

### 5. Emergency re-issue runbook

```text
1. Confirm symptom: openssl dates / browser error
2. Identify cert path: CDN vs LB vs pod secret
3. Re-issue: ACM renew / cert-manager force renew / vendor portal
4. Deploy secret or attach to HTTPS listener
5. Purge CDN if it caches TLS incorrectly (rare) / wait propagation
6. Verify openssl + external scanner
7. Postmortem: why monitoring/renew failed
```

```bash
# cert-manager force renew example
cmctl renew www-example -n app
# or annotate per current docs
kubectl -n app annotate certificate www-example cert-manager.io/issue-temporary-certificate="true" --overwrite
```

1. Keep break-glass credentials for DNS-01 if HTTP-01 path is down.
2. Pre-stage emergency self-signed **only** for internal isolation — not as public fix.

### 6. UX when TLS is healthy but service degraded

For **application** maintenance (cert still valid):

1. Return 503 with static maintenance page from edge (valid TLS).
2. Retry-After; JSON APIs with structured maintenance error.
3. Do not mix this with cert expiry — different failure modes.

### 7. Hand off

1. Single inventory source of truth + owners.
2. Status page provider independent of primary CDN account when possible.
3. Comms templates: “TLS certificate incident” vs “app maintenance”.
4. Apply `code-quality-standards` to automation exporters.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Defense | 30/14/7 day alerts + auto-renew | Calendar reminder only |
| Comms | Independent status domain | Maintenance HTML on expiring host |
| Inventory | All SANs + forgotten hosts | Only www |
| HSTS | Prevent expiry; plan long max-age | Assume users click through |
| Response | Documented re-issue | “Who has the DigiCert login?” |
| APIs | Client retry guidance post-fix | Only a pretty HTML page |

## Output Checklist

- [ ] Certificate inventory complete with owners
- [ ] Monitoring/alerts for notAfter live
- [ ] Auto-renew path verified recently
- [ ] Independent status/comms channel ready
- [ ] Emergency re-issue runbook tested
- [ ] CDN/LB/origin cert layers covered
- [ ] Post-expiry verification commands documented
- [ ] Postmortem template ready
- [ ] Related issuance skills linked

## Rules

- Prefer never needing an expiry page — monitor and auto-renew.
- Do not rely on same-host HTML during invalid TLS.
- HSTS removes click-through as a mitigation.
- Authorized ops only.
- Issuance automation → cert-manager skills; mis-issuance watch → CT skill.

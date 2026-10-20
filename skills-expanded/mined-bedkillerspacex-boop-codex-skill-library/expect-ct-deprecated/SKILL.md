---
name: expect-ct-deprecated
description: >
  Expect-CT header deprecation guidance for owned TLS sites: remove Expect-CT,
  rely on Certificate Transparency ecosystem defaults in modern browsers, and
  clean edge/CDN configs that still emit the header. Use when Expect-CT,
  report-uri CT, or audits flag deprecated Expect-CT.
---

# Expect-CT Deprecated

## Scope And Authorization

- **In scope:** HTTPS sites, CDNs, and edge configs you operate.
- **Out of scope:** Scanning the Internet for Expect-CT as an attack surface project without scope.
- Expect-CT is obsolete for modern Chrome-class browsers; keeping it adds noise, not meaningful enforcement.
- CT logging remains relevant for CAs—this skill is about the **HTTP header**, not abandoning CT monitoring entirely.
- Pair with `nginx-security-headers` / TLS edge hardening skills.

## When To Use

- Security scanners report `Expect-CT` present or misconfigured.
- Cleaning legacy Helmet/nginx/CDN header sets.
- Migrating old CT report collectors that only existed for Expect-CT.
- Documenting why the header should not be re-added.
- Aligning header baselines with current browser behavior.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Full security header suite | `nginx-security-headers` or CSP skills |
| Certificate lifecycle / ACME | cert management skills |
| HSTS design | HSTS notes within header skills |
| Implementation quality baseline | `code-quality-standards` |
| DMARC email CT confusion | email skills (unrelated) |

## Domain Focus

| Area | Guidance |
| --- | --- |
| Status | Expect-CT obsolete; browsers ignore / removed support |
| Action | Delete header from apps, CDNs, reverse proxies |
| Reports | Shut down unused CT report endpoints or repurpose with care |
| Still do | Use public CT monitors / CA log transparency for your domains |
| Don’t | Reintroduce Expect-CT “for compliance theater” |
| Verify | curl -sI shows no Expect-CT |

## Workflow

### 1. Confirm scope and success criteria

1. Hostnames and edge layers (app, nginx, Cloudflare, ALB headers).
2. Success: no Expect-CT on production responses; docs updated; no broken report pipeline dependencies.

### 2. Inventory Expect-CT emission

```bash
curl -sI https://www.example.com | rg -i 'expect-ct|strict-transport|content-security'
rg -n "Expect-CT|expectCt|expect-ct" --glob '!node_modules'
```

1. Check Helmet versions and `expectCt` middleware.
2. Check CDN managed header features / Terraform.

### 3. Baseline understanding

| Fact | Implication |
| --- | --- |
| Expect-CT once asked browsers to enforce CT | Modern browsers do CT by default without this header |
| report-uri in Expect-CT | Often dead endpoints now |
| Audit tools | May still warn if present as deprecated |

### 4. Remove the header

```nginx
# Remove any add_header Expect-CT ...;
# ensure no map injects it
```

```js
// Helmet: do not enable expectCt; remove legacy config
// app.use(helmet({ /* no expectCt */ }))
```

1. Remove report collectors only used for Expect-CT if unused.
2. Keep separate **CT monitoring** (e.g. certstream, CA notifications) if org relies on them for phishing domain detection.

### 5. Prefer modern controls

1. HSTS with sensible max-age (if ready).
2. CAA DNS records for CA restriction.
3. Automated cert issuance + monitoring.
4. Standard security headers (CSP, frame-ancestors, etc.) via the right skill.

### 6. Verify with evidence

```bash
for h in www.example.com api.example.com; do
  echo "== $h"
  curl -sI "https://$h" | rg -i 'expect-ct' || echo "Expect-CT absent (good)"
done
```

1. CI or synthetic check fails if Expect-CT reappears.
2. Scanner re-run shows finding closed.

### 7. Hand off

1. Update secure header baseline docs: Expect-CT = do not use.
2. Educate compliance partners who copy old checklists.
3. Owner for edge header Terraform module.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Header | Absent | `Expect-CT: max-age=86400, enforce` |
| Compliance | Current browser guidance | Old PCI/blog copy requiring Expect-CT |
| Monitoring | CT log monitoring for domains | Rely only on deprecated header |
| Cleanup | All layers removed | Only app removed; CDN still adds |

## Output Checklist

- [ ] All layers inventoried for Expect-CT
- [ ] Header removed from configs
- [ ] curl evidence of absence
- [ ] Report endpoints decommissioned or justified
- [ ] Baseline docs updated
- [ ] Regression check in CI/synthetics
- [ ] Residual risk (other TLS issues) noted

## Rules

- Do not re-add Expect-CT for score games.
- Deprecation ≠ “skip all certificate hygiene.”
- Owned sites only for config changes.
- Prefer modern header baselines via dedicated skills.
- Evidence via response headers, not assumptions.

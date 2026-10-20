---
name: configure-dns-tls
description: Configures DNS records and TLS for a service — A/AAAA/CNAME/ALIAS/MX/TXT/CAA, zero-downtime cutovers via pre-lowered TTL, automated ACME/Let's Encrypt/cert-manager issuance and auto-renewal, and TLS 1.2+/1.3-only settings with HSTS, OCSP stapling, and 80→443 redirect — eliminating expired-cert and bad-cutover outages.
when_to_use: Pointing a domain at a service, enabling HTTPS, automating/rotating certificates (ACME/cert-manager), or migrating DNS. Distinct from configure-reverse-proxy-lb (the proxy/LB that terminates the TLS this issues) and setup-cdn-edge-waf (the CDN/WAF edge in front).
---

## When to Use

Reach for this skill when the task is **names and certificates** — getting a domain to resolve to your service and serving valid HTTPS that renews itself:

- "Point `app.example.com` at this load balancer / IP without downtime"
- "Enable HTTPS / fix the expired-cert outage / stop the cert from ever expiring again"
- "Automate certs with Let's Encrypt / cert-manager; issue a wildcard"
- "Migrate DNS to a new provider / cut over to a new origin"
- "Lock down SPF/DKIM/DMARC, or CAA so only my CA can issue"
- "Why does SSL Labs give us a B? Harden the TLS config"

NOT this skill:
- Configuring the proxy/LB/Ingress that **terminates** TLS, virtual hosts, upstream pools, timeouts → configure-reverse-proxy-lb
- The CDN/edge, WAF rules, edge caching, or DDoS layer in front of origin → setup-cdn-edge-waf
- Application-layer auth/authz, token scopes, RBAC → design-authorization-model
- Tamper-evident security event logs (incl. cert-rotation events) → build-audit-logging

This skill owns the **record values, the cutover choreography, certificate lifecycle, and the TLS handshake policy**. It hands the terminated connection to the proxy.

## Steps

1. **Pick the record type by what you're pointing at — do not CNAME the apex.**

   | Need | Record | Notes |
   |---|---|---|
   | Name → IPv4 | `A` | Bare IP only |
   | Name → IPv6 | `AAAA` | Add alongside A; serve dual-stack |
   | Subdomain → another hostname | `CNAME` | e.g. `www → app.example.com`; cannot coexist with other records on that name |
   | **Apex** (`example.com`) → hostname | `ALIAS`/`ANAME`/flattened-CNAME | Apex can't be a real CNAME (breaks SOA/NS/MX). Use the provider's ALIAS (Route 53 alias, Cloudflare CNAME-flattening, etc.) |
   | Mail | `MX` | Priority + target; target must be an A/AAAA, never a CNAME |
   | SPF/DKIM/DMARC/verification | `TXT` | One SPF per domain; DMARC at `_dmarc`; DKIM at `<sel>._domainkey` |
   | Who may issue certs | `CAA` | `0 issue "letsencrypt.org"` + `0 issuewild "letsencrypt.org"` |

   Set CAA **before** first ACME issuance, or issuance fails with `CAA record prevents issuance`. Example:
   ```
   example.com.  CAA  0 issue "letsencrypt.org"
   example.com.  CAA  0 issuewild "letsencrypt.org"
   example.com.  CAA  0 iodef "mailto:security@example.com"
   ```

2. **Zero-downtime cutover: lower the TTL BEFORE the change — this is the whole trick.** Resolvers cache the old answer for up to its TTL; if you cut over while TTL is 3600, clients hit the dead origin for an hour.
   1. Drop the record's TTL to `60` (or `30`). **Wait out the *old* TTL** (e.g. wait the full prior 3600s) so every cache holds the short TTL.
   2. Run both origins in parallel (old + new healthy) during the switch — never tear down old first.
   3. Change the record value to the new target.
   4. Verify the new answer is served (step in Verify) and the new origin takes real traffic.
   5. Only after traffic has fully drained from the old origin (watch its access logs go quiet for > one TTL), decommission it and **raise TTL back** to 3600+ to cut query volume/cost.

3. **Automate certificates — manual renewal is a guaranteed future outage.** Use ACME (Let's Encrypt / ZeroSSL). Never click-issue a 1-year cert you have to remember to renew; LE is 90-day by design to *force* automation.
   - **VM / bare proxy:** `certbot` with a renewal timer, or the proxy's built-in ACME (Caddy auto-HTTPS, Traefik resolver, nginx + `acme.sh`).
   - **Kubernetes:** **cert-manager** — a `ClusterIssuer` + `Certificate` (or Ingress annotation) reconciles renewal automatically; renews at ~⅔ of lifetime.

   ```yaml
   # cert-manager: DNS-01 wildcard via Cloudflare
   apiVersion: cert-manager.io/v1
   kind: ClusterIssuer
   metadata: { name: letsencrypt-prod }
   spec:
     acme:
       server: https://acme-v02.api.letsencrypt.org/directory
       email: ops@example.com
       privateKeySecretRef: { name: letsencrypt-prod-key }
       solvers:
       - dns01:
           cloudflare:
             apiTokenSecretRef: { name: cloudflare-token, key: api-token }
   ---
   apiVersion: cert-manager.io/v1
   kind: Certificate
   metadata: { name: example-tls, namespace: web }
   spec:
     secretName: example-tls          # Ingress references this
     issuerRef: { name: letsencrypt-prod, kind: ClusterIssuer }
     dnsNames: ["example.com", "*.example.com"]
   ```
   Iterate against the **staging** ACME server first — set the `ClusterIssuer` `spec.acme.server` to `https://acme-staging-v02.api.letsencrypt.org/directory` (or `certbot --test-cert`) to dodge LE prod rate limits (50 certs / registered-domain / week) while debugging, then flip the server back to prod and re-issue.

4. **Choose the ACME challenge and cert shape deliberately.**

   | Axis | Pick | Why |
   |---|---|---|
   | **HTTP-01** | single host, port 80 reachable from internet | simplest; needs `/.well-known/acme-challenge/` served; **cannot** do wildcards |
   | **DNS-01** | wildcards, internal hosts, no inbound 80, or many SANs | proves control via a `_acme-challenge` TXT; needs DNS-provider API creds; works behind a firewall |
   | **Wildcard** `*.example.com` | many dynamic subdomains | DNS-01 only; one cert, but a single shared private key (bigger blast radius) |
   | **SAN / multi-domain** | a known fixed set of names | explicit per-name; rotate one without touching others; preferred when the list is stable |

   Default: **SAN cert via DNS-01** for anything non-trivial; wildcard only when subdomains are unbounded/dynamic.

5. **Set a modern TLS policy at the terminator — TLS 1.2+ only, redirect, HSTS, stapling.** Configure on whatever terminates (see configure-reverse-proxy-lb), but the *policy* is owned here:
   - Protocols: **TLS 1.3 + TLS 1.2 only**. Disable TLS 1.0/1.1 and SSLv3 entirely.
   - Ciphers: TLS 1.3 defaults; for 1.2 use forward-secret AEAD suites (ECDHE + AES-GCM/CHACHA20), no CBC/RC4/3DES.
   - **Redirect 80→443** with `301`, then serve everything over HTTPS.
   - **HSTS** on HTTPS responses: `Strict-Transport-Security: max-age=63072000; includeSubDomains; preload` — but only add `preload`/`includeSubDomains` once *every* subdomain is HTTPS (it's hard to undo). Roll out short → long → preload.
   - **OCSP stapling** on (`ssl_stapling on;` in nginx) so clients don't round-trip the CA.
   - Serve the **full chain** (leaf + intermediates), not just the leaf — the #2 cause of "works in my browser, fails in `curl`/old Android".

   ```nginx
   server {
     listen 443 ssl http2;
     ssl_protocols TLSv1.2 TLSv1.3;
     ssl_prefer_server_ciphers off;
     ssl_certificate     /etc/letsencrypt/live/example.com/fullchain.pem;  # full chain
     ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;
     ssl_stapling on; ssl_stapling_verify on;
     add_header Strict-Transport-Security "max-age=63072000; includeSubDomains" always;
   }
   server { listen 80; server_name example.com; return 301 https://$host$request_uri; }
   ```

6. **Prove auto-renew works before you trust it.** A cert that issues fine but never renews is a 90-day time bomb. Force a dry-run/staging renewal now (step in Verify) so you discover broken DNS creds or a missing port today, not at 2am on day 89.

## Common Errors

- **CNAME on the apex.** Breaks NS/SOA/MX co-existence; many resolvers reject it. Use ALIAS/ANAME/CNAME-flattening for `example.com`.
- **Cutover without pre-lowering TTL.** You switch the record but caches serve the dead origin for the full old TTL (often an hour). Lower TTL and wait out the *old* TTL first.
- **Raising TTL or killing the old origin too early.** Do it only after old-origin logs go quiet for > one TTL; otherwise stragglers 502.
- **Missing/forbidding CAA.** No CAA = any CA may issue (security gap); a CAA that omits your CA = ACME fails with `CAA record prevents issuance`. Add the issuing CA explicitly, including `issuewild` for wildcards.
- **HTTP-01 for a wildcard.** Impossible — wildcards require DNS-01. Switch the solver.
- **Manual cert renewal "we'll remember."** You won't. The outage is scheduled for expiry day. Automate or it will lapse.
- **Serving only the leaf cert.** Browsers cache intermediates and "work"; `curl`, Java, old Android, and API clients fail chain validation. Always deploy `fullchain.pem`.
- **Burning LE rate limits while debugging.** Iterate against `acme-staging-v02` (or `certbot --test-cert`); only hit prod once issuance succeeds in staging.
- **`includeSubDomains`/`preload` HSTS before all subdomains are HTTPS.** Any plain-HTTP subdomain becomes unreachable, and `preload` is baked into browsers for months. Roll HSTS out short → long → preload.
- **DNS-01 with under-scoped API creds.** The token can't write `_acme-challenge` TXT, so renewal silently fails. Scope the token to DNS-edit on that zone and test it.
- **Mixed content after enabling HTTPS.** Page loads over HTTPS but pulls `http://` assets → browser blocks them. Rewrite asset URLs to `https://` or protocol-relative; verify console is clean.
- **Clock skew on the TLS host.** A wrong system clock makes a valid cert read as not-yet-valid/expired. Run NTP.

## Verify

1. **Records resolve correctly:** `dig +short A app.example.com` (and `AAAA`) returns the new target; `dig CAA example.com` shows your CA; `dig TXT _dmarc.example.com` shows the DMARC policy. Query an external resolver (`dig @1.1.1.1 …`) too, not just the local cache.
2. **TTL was actually lowered before cutover:** `dig app.example.com | grep -E '^app'` shows the short TTL *before* you change the value; confirm the answer flips after, and that it propagated (`dig @8.8.8.8` and `@1.1.1.1` agree).
3. **Full chain + protocol scan:** `echo | openssl s_client -connect example.com:443 -servername example.com -showcerts` shows leaf **and** intermediate(s), `Verify return code: 0 (ok)`. `testssl.sh example.com` (or SSL Labs) reports TLS 1.2/1.3 only, no TLS 1.0/1.1, HSTS present, OCSP stapled — target grade **A/A+**.
4. **Redirect + HSTS:** `curl -sI http://example.com` → `301` to `https://`; `curl -sI https://example.com | grep -i strict-transport` shows the HSTS header.
5. **No mixed content:** load the page, browser console shows zero "Mixed Content" / blocked-asset warnings; all subresources are `https://`.
6. **Expiry & auto-renew proven:** `echo | openssl s_client -connect example.com:443 2>/dev/null | openssl x509 -noout -enddate` shows a future date; then force a **staging** renewal — `certbot renew --dry-run` (VM) or, for k8s, point the issuer at `acme-staging-v02`, run `cmctl renew example-tls`, and watch `cmctl status certificate example-tls` go Ready — and confirm a fresh cert issues without manual steps.
7. **Mail auth (if MX set):** SPF/DKIM/DMARC TXT records validate (e.g. an external mail-tester) — no `softfail`/missing-DKIM.

Done = every name resolves to the new target on external resolvers, HTTPS serves the **full chain** over **TLS 1.2/1.3 only** with HSTS + stapling + 80→443 redirect and no mixed content (SSL Labs/testssl ≥ A), CAA locks issuance to your CA, and a staging force-renew has **proven** auto-renewal works before any cert nears expiry.

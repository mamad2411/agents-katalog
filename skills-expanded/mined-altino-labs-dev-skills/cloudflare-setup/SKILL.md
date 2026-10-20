---
name: cloudflare-setup
description: >
  Reusable patterns for DNS configuration, SSL, protection, and firewall rules
  in Cloudflare. Invoke automatically when configuring a domain, SSL certificate,
  DNS records, rate limiting, or DDoS protection.
---

# Cloudflare Setup

## Initial domain configuration

```
1. Register domain (Cloudflare Registrar or external)
2. Point nameservers to Cloudflare
3. Add DNS records
4. Configure SSL and protection
```

---

## Essential DNS records

```
Type   Name       Value                        Proxy
A      app        <server IP>                  Yes (orange)
CNAME  staging    <staging server domain>      Yes
CNAME  www        app.<domain>.com             Yes
CNAME  api        <API domain>                 Yes

# Email (do not proxy — email records must go direct)
MX     @          (email provider records)     No
TXT    @          (SPF, DKIM, DMARC)           No
```

**Rule:** email records (MX, SPF, DKIM, DMARC) must never be proxied through Cloudflare — disable the proxy (gray icon) on them.

---

## SSL/TLS

```
Mode:             Full (strict)   ← never use "Flexible" in production
Always HTTPS:     enabled
HSTS:             enabled (max-age=31536000; includeSubDomains)
Minimum TLS:      TLS 1.2
```

**Why Full (strict) and not Flexible:** Flexible only encrypts between the user and Cloudflare — the connection from Cloudflare to the server remains plain HTTP. Full (strict) encrypts the entire path.

---

## Basic protection (free)

```
DDoS protection:       automatic (always active on free tier)
Bot Fight Mode:        enabled
Security Level:        Medium
Browser Integrity Check: enabled
```

---

## Rate limiting via firewall rules

```
Rule 1 — Auth endpoints
  URL: /api/v1/auth/*
  Limit: 10 req/min per IP
  Action: Block

Rule 2 — Block requests without User-Agent
  Condition: User-Agent is empty
  Action: Block

Rule 3 — Block countries without expected users (optional)
  Condition: Country not in [<expected countries>]
  Action: Challenge (CAPTCHA) or Block
```

---

## API configuration (for bootstrap automation)

```bash
# Required variables
CLOUDFLARE_API_TOKEN=   # permission: Edit zone DNS
CLOUDFLARE_ZONE_ID=     # Zone ID for the domain

# Add CNAME record
curl -X POST "https://api.cloudflare.com/client/v4/zones/$CLOUDFLARE_ZONE_ID/dns_records" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "CNAME",
    "name": "api",
    "content": "<server-domain>",
    "proxied": true
  }'

# Configure SSL Full Strict
curl -X PATCH "https://api.cloudflare.com/client/v4/zones/$CLOUDFLARE_ZONE_ID/settings/ssl" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"value": "strict"}'

# Force HTTPS
curl -X PATCH "https://api.cloudflare.com/client/v4/zones/$CLOUDFLARE_ZONE_ID/settings/always_use_https" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"value": "on"}'
```

---

## HTTP security headers via Transform Rules

Configure in the Cloudflare dashboard → Rules → Transform Rules → Modify Response Headers:

```
Strict-Transport-Security: max-age=31536000; includeSubDomains
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
Referrer-Policy: strict-origin-when-cross-origin
```

Or add directly on the server (NestJS interceptor) — preferable to avoid relying on manual Cloudflare configuration.

---

## Configuration checklist

- [ ] Nameservers pointing to Cloudflare
- [ ] SSL: Full (strict)
- [ ] Always HTTPS: enabled
- [ ] HSTS: enabled
- [ ] Bot Fight Mode: enabled
- [ ] Rate limiting on authentication endpoints
- [ ] Email records without proxy (gray icon)
- [ ] SPF, DKIM, DMARC records configured

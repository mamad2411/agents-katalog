---
name: tls-engineering
description: Configure TLS correctly. Use when setting up certificates, HTTPS,
  and cipher policies.
metadata:
  tags: tls, engineering
---

# TLS Engineering

## Use this skill when
- Issuing and renewing certificates
- Configuring HTTPS servers and minimum versions
- Reviewing cipher and handshake configuration

## Do not use this skill when
- Full serving config (use nginx-engineering)
- Mutual TLS specifically (use mtls-configuration)

## Instructions
1. Prefer managed CAs and automated issuance/renewal (ACME/letsencrypt).
2. Enforce TLS 1.2+ (default 1.3) and disable old protocols/ciphers.
3. Apply HSTS on HTTPS domains after confirming traffic.
4. Use proper CN/SAN and short-lived certificates where possible.
5. Terminate TLS close to clients (edge), with TLS in between hops too.
6. Verify with TLS testers; set security headers to polish config.
7. Monitor expiry and renew automatically with alerts.

## Checklist
- Auto-renewal works and is monitored
- No TLS 1.0/1.1 or weak ciphers
- HSTS set appropriately

## Output Format
- Cert chain | versions | ciphers | renewal automation | posture

## Common Mistakes
- Manual cert renewal that lapses
- Ignoring intermediate/chain completeness
- HSTS without HTTPS-first

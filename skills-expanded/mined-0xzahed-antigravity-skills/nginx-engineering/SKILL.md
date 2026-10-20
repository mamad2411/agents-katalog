---
name: nginx-engineering
description: Configure Nginx for serving, proxying, and TLS. Use when tuning a
  reverse proxy or web server.
metadata:
  tags: nginx, engineering
---

# Nginx Engineering

## Use this skill when
- Configuring reverse proxies and load balancing
- Serving static content and caching
- TLS termination and security headers

## Do not use this skill when
- Application logic
- Service mesh concerns

## Instructions
1. Lay out server blocks by site; use include organization.
2. Restrict head/body sizes and timeouts explicitly.
3. Proxy with proper Upstream config, timeouts, and retries.
4. Cache static assets with correct expiry and validation.
5. Terminate TLS with modern ciphers and HSTS.
6. Set security headers: X-Frame-Options, CSP, nosniff.
7. Rate limit abuse paths; log access meaningfully.
8. Validate config with nginx -t before reload.

## Checklist
- No default empty server leaks
- TLS modern + HSTS
- Timeouts and size limits set

## Output Format
- Config map | proxy rules | caching | TLS posture

## Common Mistakes
- Proxy timeouts that break long requests silently
- Infinite client body sizes
- Disabling logs or errors entirely

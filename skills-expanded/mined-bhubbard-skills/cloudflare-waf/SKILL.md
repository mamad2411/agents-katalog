---
name: cloudflare-waf
description: Configuring the Cloudflare Web Application Firewall (WAF) via WordPress. Use when dealing with blocked users, security rulesets, or "I'm Under Attack" mode.
---

# Cloudflare WAF and Security

The Cloudflare plugin allows users to manage key security settings without leaving the WordPress dashboard.

## Security Levels
You can adjust the Security Level (Essentially off, Low, Medium, High, I'm Under Attack) directly from the plugin.
- **I'm Under Attack**: Use this only during an active DDoS attack. It presents a JS challenge (hCaptcha or Turnstile) to every visitor. Leaving this on permanently severely degrades the user experience and breaks API endpoints.

## WAF Rulesets
Cloudflare provides WordPress-specific managed rulesets (available on paid plans).
- If a legitimate API request (like a webhook from a payment gateway or a REST API call from a mobile app) is returning a 403 error, it is likely being blocked by the WAF.
- Advise the user to check the "Security > Events" log in the Cloudflare dashboard and create a WAF Exception for the blocked URI.

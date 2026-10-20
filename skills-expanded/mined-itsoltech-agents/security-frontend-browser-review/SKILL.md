---
name: security-frontend-browser-review
description: "Review browser changes to HTML rendering, storage, security headers, cache, or exposed data."
---

# Security Frontend Browser Review

Check that frontend improves UX but never becomes the security boundary; review XSS, storage, cache, CSRF, CORS, and logout cleanup.

## Trigger boundary

Use this skill when a browser or frontend change affects XSS/HTML rendering, storage, CSP/CORS/CSRF, cache, exposed data, logout cleanup, or client/server trust boundaries.

Do not load it for a small local rename, comment, formatting change, or mechanical edit with no browser, security-header, storage, cache, or exposed-data impact; follow the repository's established convention directly.

## Evidence

Prefer code, tests, logs, config, API contracts, and data examples over assumptions.

## Focused References

- [01-browser-xss-csrf.md](./references/01-browser-xss-csrf.md) - Browser XSS And CSRF
- [02-cache-cdn-qa.md](./references/02-cache-cdn-qa.md) - Cache CDN And QA

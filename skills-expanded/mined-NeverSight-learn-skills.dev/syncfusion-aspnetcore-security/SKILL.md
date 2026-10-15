---
name: syncfusion-aspnetcore-security
description: "**CONTENT SECURITY POLICY (CSP) GUIDE** — Assist with configuring Syncfusion ASP.NET Core EJ2 components to work with strict Content Security Policy (CSP) headers. Use when: implementing CSP headers, generating and applying nonces to inline scripts/styles, configuring external font allowlists, or troubleshooting CSP violations."
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Content Security Policy (CSP) — Syncfusion ASP.NET Core (Security)

Use this skill for high-level, Syncfusion-specific CSP guidance and references. Detailed code snippets and implementation examples live in the concern's `references` files.

## When to Use
- Implementing CSP headers for Syncfusion EJ2 controls
- Running in strict CSP mode where inline scripts/styles are restricted
- Adding nonces to inline scripts/styles for Syncfusion initialization
- Allowlisting CDN resources or external fonts required by Syncfusion themes

## Quick Checklist
- Generate a cryptographically secure nonce per request
- Add the nonce to the CSP header and to all Syncfusion script/style tags
- Allow required CDN origins and font providers in CSP directives
- Avoid `unsafe-inline`/`unsafe-eval` unless absolutely necessary
- Verify behavior in browser DevTools and address CSP violations

## Generic Guidelines (Summary)
- Generate nonces early in the pipeline and store them in `HttpContext` for views
- Use minimal, explicit CSP directives (prefer `'self'`, explicit hostnames, and `'nonce-<value>'`)
- Prefer data binding over inline templates to avoid `unsafe-eval` requirements
- Document your CSP policy and the reasons for any relaxations

## References
- Main implementation and examples: [references/csp-guide.md](references/csp-guide.md)



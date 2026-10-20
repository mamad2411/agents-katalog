---
name: secure-headers
version: "0.1"
description: >
  [STUB - Not implemented] Secure HTTP headers configuration including CSP, HSTS, X-Frame-Options, and SameSite cookies.
  PROACTIVELY activate for: [TODO: Define on implementation].
  Triggers: [TODO: Define on implementation]
core-integration:
  techniques:
    primary: ["[TODO]"]
    secondary: []
  contracts:
    input: "[TODO]"
    output: "[TODO]"
  patterns: "[TODO]"
  rubrics: "[TODO]"
---

# Secure Headers

> **STUB: This skill is not yet implemented**
>
> This placeholder preserves the documented plugin structure.
> See parent plugin README for planned capabilities.

## Planned Capabilities

- **Content-Security-Policy (CSP)**: Script, style, and resource origin restrictions
- **HSTS**: Strict-Transport-Security enforcement
- **X-Frame-Options**: Clickjacking prevention
- **X-Content-Type-Options**: MIME type sniffing prevention
- **SameSite Cookies**: CSRF protection via cookie attributes
- Framework-specific implementation guides (Next.js, Express, etc.)

## Critical Pattern

```typescript
// next.config.js
module.exports = {
  async headers() {
    return [{
      source: '/(.*)',
      headers: [
        { key: 'X-Frame-Options', value: 'DENY' },
        { key: 'X-Content-Type-Options', value: 'nosniff' },
        { key: 'Strict-Transport-Security', value: 'max-age=31536000; includeSubDomains' },
        { key: 'Content-Security-Policy', value: "default-src 'self'; script-src 'self' 'unsafe-inline'" }
      ]
    }];
  }
};
```

## Implementation Status

- [ ] Core implementation
- [ ] References documentation
- [ ] Output templates
- [ ] Integration tests

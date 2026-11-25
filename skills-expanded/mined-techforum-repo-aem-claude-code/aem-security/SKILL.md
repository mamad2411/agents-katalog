---
name: aem-security
description: AEM security review — admin resolver, query injection, path validation, exposed endpoints, hardcoded secrets
allowed-tools: Read, Grep, Glob
argument-hint: "[file or class path]"
---

Review `$ARGUMENTS` for AEM security issues. Report each finding as **Blocking** / **Warning** / **Suggestion**.

- **Admin ResourceResolver or `loginAdministrative` usage** — Blocking; replace with service user
- **JCR-SQL2 or XPath query built from untrusted input** — Blocking; use bound parameters only
- **Path-based input passed to repository lookups without validation** — Blocking
- **Hardcoded credentials, tokens, or API keys** — Blocking
- **Request-scoped state stored in an OSGi singleton field** — Blocking
- **Stack traces or internal paths exposed in responses or logs** — Warning
- **Path-based servlet registration without Dispatcher filter consideration** — Warning
- **Service user permissions broader than minimum required** — Warning
- **Sensitive data in log statements** — Warning

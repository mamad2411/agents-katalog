---
name: backend-security
description: Backend/server-side security auditor for Node.js, Express, NestJS, FastAPI, Django, Flask, Spring, Ruby on Rails, and similar frameworks. Use when reviewing server-side application logic, error handling, logging, file upload handling, or general middleware configuration specifically — separate from database or API-contract concerns.
---

# Backend Security — Server-Side Application Layer Auditor

A specialized skill for auditing the application layer running on the server, across common frameworks.

## When to use this
- Any Node.js/Express/NestJS/FastAPI/Django/Flask/Spring/Rails project
- Reviewing error handling and logging practices
- Reviewing general middleware configuration (helmet, cors, rate-limit, etc.)

## Core Checks

### Secure Defaults
- Node/Express: is `helmet` (or equivalent) enabled to set security headers?
- Is a debug/development mode accidentally left on in production? (Django `DEBUG=True`, Flask `debug=True`, verbose framework error pages in production all leak sensitive internals.)

### Error Handling
- User-facing errors are generic ("Something went wrong") while full details/stack traces go only to internal logs.
- No library/framework version numbers leaked in error messages (makes it trivial for an attacker to look up known CVEs for that exact version).

### Logging
- No sensitive data (passwords, tokens, card numbers) ever written to logs, even partially.
- Security-relevant events are logged: repeated failed logins, permission changes, bulk deletions.
- Log files/streams are access-restricted, not publicly reachable.

### Server-Side Input Validation
- Every controller/route handler validates type and shape of incoming data — never relies solely on client-side validation.
- Mass-assignment protection: don't accept updates to fields that weren't explicitly whitelisted (e.g., a generic body update accidentally allowing a `role` field to be changed).

### Rate Limiting & Abuse Protection
- Application-level rate limits on sensitive/expensive operations (search, bulk export, messaging) per user/IP.
- Sensible timeouts to prevent resource exhaustion.

### File Uploads
- Actual file type verified via magic bytes, not just the extension or the client-declared `Content-Type`.
- Uploaded files stored outside any executable/servable directory, with randomized (not user-controlled) filenames.
- Enforced maximum file size to prevent denial-of-service.

### Internal Service-to-Service Calls (Microservices)
- Internal calls that assume full mutual trust without any verification are risky if one service is compromised — consider mTLS or internal service tokens where the architecture warrants it.

## Report Format
```
Module/Route: [name]
Issue: [problem]
Severity: Critical/High/Medium/Low
Evidence: [code or configuration]
Impact: [impact]
Fix: [remediation]
```

## Rules
- Stay focused on application/server logic; hand off infrastructure/cloud config issues to `cloud-security`, and database-layer issues to `database-security`.

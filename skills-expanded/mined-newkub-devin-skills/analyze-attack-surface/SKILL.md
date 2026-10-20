---
name: analyze-attack-surface
description: Analyze the system attack surface and exposed endpoints
argument-hint: "[app-url|repo-path]"
related:
  - deep-review-codebase
  - check-secrets
  - report-uxui-all-routes

---

## Goal
Identify points an attacker could target, such as endpoints, dependencies, and infrastructure

## Scope
- Supports web, API, cloud, and mobile backends
- Uses port scan, dependency scan, and route analysis
- Reports as a trust boundary diagram or list

## Execute
### 1. List Exposed Surfaces

> Goal: List Exposed Surfaces

1. Use `report-uxui-all-routes` or `raindrop list` for routes
2. Scan ports with `nmap` if authorized
3. Find public IPs, domains, and load balancers

### 2. Identify Entry Points

> Goal: Identify Entry Points

1. Identify public endpoints: REST, GraphQL, gRPC, WebSocket
2. Find authentication/authorization boundaries
3. Find file uploads, webhooks, and admin panels

### 3. Assess Dependencies

> Goal: Assess Dependencies

1. Run a dependency scan for known vulnerabilities
2. Find connected third-party services
3. Check supply chain risk

### 4. Report

> Goal: Report

1. Summarize the main attack surfaces
2. Assign a severity to each entry point
3. Recommend initial mitigations

## Rules
### 1. Legal

- Scan only authorized systems
- Never port scan without authorization
- Never exploit vulnerabilities

### 2. Comprehensive

- Cover network, application, and human factors
- Separate internal vs external exposure
- Identify trust boundaries

- Use /deep-review-codebase if needed
- Use /check-secrets secrets-leak if needed
## Expected Outcome
- Attack surface list with severity ratings
- Trust boundary map
- Mitigation recommendations

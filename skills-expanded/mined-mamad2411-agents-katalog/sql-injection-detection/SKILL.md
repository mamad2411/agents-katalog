---
name: SQL Injection Detection
description: Detect and validate SQL injection vulnerabilities in web inputs using structured reasoning and safe validation.
domain: web-application-security
tags:
  - sqli
  - owasp
  - injection
mitre_attack:
  - T1190
---

# SQL Injection Detection

## When to Use
Apply this skill when user-controlled input reaches a SQL query — login forms,
search parameters, REST/GraphQL inputs, URL path segments, or headers that feed
dynamic SQL. Typical triggers: parameter discovery surfaces a query-backed
endpoint, or behavior differs on syntactic input.

## Prerequisites
- Confirmed input reflection or a measurable behavior difference on syntactic
  input (boolean or time-based).
- Authorization covering the target (LEA ScopeGuard validated, ROE permits the
  relevant category).

## Workflow
1. Identify injection points from parameter discovery (query, body, path,
   header origins).
2. Probe with boolean-based payloads first (least noisy), then time-based for
   blind cases.
3. Map the backend dialect via error-based / UNION / stacked-query signatures.
4. Validate non-destructively — avoid bulk data exfiltration unless explicitly
   authorized by the engagement scope.

## Verification
- A finding requires a reproducible payload demonstrating the injection (not a
  single heuristic signal).
- Severity reflects data exposure breadth, reachability, and authentication
  context.

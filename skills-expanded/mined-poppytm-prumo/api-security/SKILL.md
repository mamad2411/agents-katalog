---
name: api-security
description: OWASP API Top 10 mitigation, strict OpenAPI schema validation, token bucket rate limiting, safe serialization, and RFC 7807 problem details
---
# API Security & Hardening

## 1. OWASP API Security Top 10 Mitigation
Systematically guard against Broken Object Level Authorization (BOLA), Broken Authentication, Broken Object Property Level Authorization, and Unrestricted Resource Consumption. Validate user ownership of requested entity IDs on every database query.

## 2. Strict Input & Schema Validation
Validate all incoming request bodies, headers, and query parameters against strict OpenAPI 3.1 or JSON Schema definitions. Reject unexpected or unmapped fields (disallow mass assignment). Enforce bounds on strings, arrays, and numeric values.

## 3. Authentication & Authorization Enforcement
Apply role-based (RBAC) or attribute-based (ABAC) access control at the handler or middleware layer before executing any business logic. Never rely on frontend client logic to hide unauthorized API capabilities.

## 4. Rate Limiting & Quota Management
Implement sliding window or token bucket rate limiting per authenticated client (API key / user ID) and per IP address. Return HTTP 429 Too Many Requests with explicit Retry-After headers when thresholds are exceeded.

## 5. Safe Serialization & Data Masking
Never serialize internal database ORM entities directly to client responses. Use dedicated Data Transfer Objects (DTOs) with explicit field mappings. Automatically strip internal fields, password hashes, PII, and internal IDs.

## 6. Transport Security & Safe Headers
Enforce TLS 1.3 encryption for all endpoints. Return standard security headers: Strict-Transport-Security (HSTS), X-Content-Type-Options: nosniff, and Cache-Control: no-store on sensitive responses. Configure CORS with explicit allowed origins; never reflect Origin blindly.

## 7. RFC 7807 Problem Details Error Handling
Format all client error responses according to RFC 7807 Problem Details for HTTP APIs (type, title, status, detail, instance). Return sanitized, user-friendly messages while keeping stack traces and database diagnostics confined to internal observability logs.

## 8. Idempotency & Replay Protection
Support Idempotency-Key headers on mutating requests (POST, PATCH) with an atomic distributed lock in Redis or database. Prevent duplicate financial or state-altering transactions from network retries.

## 9. Payload Caps & Resource Bounds
Enforce strict maximum limits on HTTP request body sizes (e.g. max 1MB for JSON payloads). Mandate pagination with bounded page sizes (default 20, max 100) on all collection endpoints to prevent memory exhaustion.

## 10. Automated Security & Contract Testing
Integrate automated API security scanners (e.g. Schemathesis, OWASP ZAP API scan) into continuous integration. Validate that undocumented endpoints are rejected and fuzz payloads do not cause unhandled 500 crashes.

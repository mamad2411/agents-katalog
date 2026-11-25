---
name: backend-security-scan
description: Security validation for Java/TEJ/Spring backend code
model: sonnet-4-6
token_budget: {input: 6000, output: 2000}
---

# Backend Security Scan

## Overview

Performs comprehensive security analysis of Java/TEJ/Spring backend code to identify vulnerabilities, credential leaks, authentication gaps, and compliance issues.

**Shared reference:** [security-scan-dimensions-reference.md](../../shared/security-scan-dimensions-reference.md) — atomic split with `secrets-detector` and unified P0–P3 rubric.

## Security Categories

### P0: Critical (Blocking)
These findings block deployment:

#### Secrets Detection
- **Hardcoded credentials**: Database passwords, API keys, tokens in source
- **Connection strings**: AWS access keys, JWT secrets, OAuth tokens
- **Environment leaks**: Config files with sensitive data
- **Cloud credentials**: GCP service accounts, Azure connection strings

Scan locations:
- Application properties files (application.properties, application.yml, application-*.yml)
- Java source files (look for password= key= secret= apiKey= token=)
- Build files (gradle.properties, pom.xml with credentials)
- Docker/deployment configs
- Bean definitions with hardcoded values

#### SQL Injection (SQLi)
- **Raw string concatenation**: `"SELECT * FROM users WHERE id = " + userId`
- **Unparameterized queries**: Using string building instead of prepared statements
- **Native queries without @Query**: JPQL/SQL without parameter binding
- **Dynamic WHERE clauses**: Building SQL strings in loops

Detection patterns:
- JdbcTemplate.update() with concatenated strings
- EntityManager.createNativeQuery() with string concatenation
- Raw SQL in @Query annotations without ?1, :param binding
- String.format() or + operator in SQL construction

---

### P1: High (Authentication/Authorization Bypass)
Prevents unauthorized access:

#### Missing Authentication
- **Open endpoints**: No @Secured or @PreAuthorize annotations
- **Admin endpoints unprotected**: /admin/*, /api/admin without auth
- **Actuator exposure**: Spring Actuator endpoints accessible without authentication
- **CORS misconfiguration**: Allows all origins or improper credential handling

Check patterns:
- Public methods in @RestController/@Controller without @Secured
- @PreAuthorize("permitAll()") on sensitive operations
- management.endpoints.web.exposure.include=* without auth
- @CrossOrigin(allowCredentials="true", origins="*")

#### Role-Based Access Control (RBAC) Issues
- **Horizontal privilege escalation**: User can access other users' data
- **Vertical privilege escalation**: Non-admin accessing admin features
- **Missing role checks**: Only checking if authenticated, not role
- **Overly permissive roles**: Users with admin role for basic operations

Check patterns:
- @PreAuthorize("isAuthenticated()") where should check role
- @PreAuthorize("hasRole('ADMIN')") on endpoints that don't need admin
- Endpoint serving resources without verifying ownership
- Service methods without @PostAuthorize to filter results by user

---

### P2: Medium (Data Validation)
Prevents invalid/malicious data entry:

#### Missing Input Validation
- **No @Valid annotation**: Request body not validated
- **Unvalidated user input**: Using request parameters directly
- **Missing @NotNull/@NotBlank**: Nullable fields in critical operations
- **No size constraints**: @Size missing on collections/strings

Detection:
- Request DTOs without @Valid annotation usage
- Path variables used directly in queries (though harder to SQLi)
- Service method parameters without validation annotations
- File upload without size/type validation

#### Missing Output Sanitization
- **XSS risk**: User input echoed in responses without encoding
- **Log injection**: Unvalidated data in log statements
- **Error messages**: Exposing system details in API error responses

---

### P3: Improvement (Performance/Logging)
Quality and maintainability issues:

#### Logging Security Issues
- **PII in logs**: Passwords, tokens, credit cards logged
- **Debug mode in production**: Verbose logging in production builds
- **Stack traces exposed**: Full exceptions returned to client

Patterns:
- `log.debug("User logged in: " + username + " password: " + password)`
- `catch(Exception e) { return new ResponseEntity(e.getMessage()); }`
- `response.toString()` where response contains sensitive data

#### Configuration Issues
- **Default credentials**: Database user 'sa' with empty password
- **Debug endpoints enabled**: Spring Actuator in production
- **Weak crypto**: Old hashing algorithms for passwords
- **Missing HTTPS**: Application not enforcing HTTPS

---

## Security Scanning Rules

### Code Patterns to Check

1. **Secret Keywords** (always investigate):
   - password, passwd, pwd, secret, token, key, credential, api_key, apiKey
   - aws_access_key, jwt, oauth, bearer
   - datasource.password, spring.datasource.password

2. **SQL Patterns** (check for injection):
   - `String sql = "SELECT...` followed by concatenation
   - `.createNativeQuery("` with concatenation
   - `@Query` with `"... WHERE ... = \" + variable`

3. **Auth Patterns** (verify protection):
   - `@RequestMapping`, `@GetMapping`, `@PostMapping` without `@Secured` or `@PreAuthorize`
   - `/admin/`, `/api/admin`, `/api/user/{id}` endpoints
   - `permitAll()`, `permitAll`, `@CrossOrigin`

4. **Validation Patterns** (verify constraints):
   - Request body DTOs without fields annotated with `@Valid`
   - Method parameters not validated before use
   - File uploads without size checks

### Report Format

```
# Backend Security Scan Report

## P0: Critical (Must Fix Before Deployment)
### [Finding ID]: [Title]
- **File**: src/main/java/com/example/UserService.java:45
- **Severity**: P0 - Critical
- **Category**: Secrets Detection
- **Issue**: Hardcoded database password found
- **Code**:
  ```java
  String password = "admin123";
  ```
- **Risk**: Database breach, unauthorized access
- **Remediation**: Use environment variables or Spring @Value injection
- **Example Fix**:
  ```java
  @Value("${app.database.password}")
  private String password;
  ```

## P1: High (Fix Before Production)
### [Finding ID]: [Title]
...

## P2: Medium (Schedule Fix)
...

## P3: Low (Improvement)
...

## Summary
- Total Issues: N
- P0 (Critical): N
- P1 (High): N
- P2 (Medium): N
- P3 (Low): N
- Recommendation: [APPROVED | BLOCKED | REVIEW REQUIRED]
```

## Implementation Guidance

### For security scanning:
1. Request backend codebase files (src/main/java, build files)
2. Identify all Java classes, properties, and configurations
3. Search each file against all security patterns
4. Document each finding with context, risk, and remediation
5. Prioritize by severity

### For authentication review:
- List all public endpoints (those without @Secured or @PreAuthorize)
- Verify role-based access is correct
- Check CORS and actuator exposure
- Document missing protections

### For dependency vulnerability check:
- Request build.gradle or pom.xml
- Identify known CVEs in dependencies
- Recommend version upgrades
- Document exposure if not upgraded

## Related Skills
- [backend-performance-profiling](../performance-profiling/SKILL.md) - Performance analysis
- [qa-orchestrator](../../qa/qa-orchestrator.md) - Full QA coordination

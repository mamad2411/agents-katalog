---
name: test-strategy
description: Design test strategies including security testing, write test plans, and identify test scenarios for banking features with DevSecOps integration
---

# Test Strategy Skill

## When to Use
Invoke when planning test coverage for a new feature, reviewing test adequacy, or integrating security testing into the CI/CD pipeline.

## Test Pyramid (Banking)
```
        /  E2E  \        <- Few: critical user journeys (login -> transfer -> verify)
       / Contract \      <- Medium: API contract validation against OpenAPI spec
      / Integration \    <- Medium: real DB (Testcontainers), real HTTP (WireMock)
     /    Unit       \   <- Many: business logic, validators, calculators
```

## Banking Test Scenario Categories
1. **Happy path**: Normal successful operation
2. **Boundary values**: Zero, negative, max amount, empty string
3. **Concurrency**: Simultaneous operations on same resource
4. **Idempotency**: Duplicate submission handling
5. **Timeout**: External service unavailable
6. **Authorization**: Unauthorized access attempts
7. **Data validation**: Invalid formats, SQL injection attempts
8. **Currency**: Multi-currency, rounding, conversion

## Coverage Targets
| Category | Line Coverage | Branch Coverage |
|----------|--------------|-----------------|
| Transaction logic | 95% | 95% |
| Authentication | 95% | 90% |
| API controllers | 80% | 80% |
| Utility classes | 80% | 70% |
| Configuration | 60% | N/A |

## Security Testing in CI/CD

### SAST (Static Application Security Testing)
- Run SonarQube analysis on every pull request
- Fail pipeline on Critical or High severity findings
- Track security hotspots as technical debt
- Include custom rules for banking patterns (BigDecimal usage, PII handling)

### DAST (Dynamic Application Security Testing)
- Run OWASP ZAP against staging environment after deployment
- Active scan covers: injection, XSS, authentication bypass, information disclosure
- Baseline scan on every PR merge, full scan weekly
- Fail pipeline on High/Critical findings before production promotion

### Security Regression Tests
- Every vulnerability fix must include a regression test
- Regression test proves the vulnerability is exploitable before the fix
- Regression test proves the vulnerability is blocked after the fix
- Security regression suite runs on every build (not just when security code changes)

### Chaos Security Testing (Sprint Cycle)
- Run chaos security tests as part of each sprint's test phase
- Include authentication bypass attempts, IDOR tests, rate limit verification
- Automate playbook scenarios from the chaos-security-testing skill
- Report chaos test results in sprint retrospective

### Container Security Scanning
- Scan container images before pushing to registry
- Fail pipeline on Critical CVEs in base images
- Verify no secrets baked into image layers
- Validate minimal base image (distroless or Alpine)
- Check for unnecessary packages and elevated privileges

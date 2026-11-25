---
name: appsec-patterns
description: "When to activate: AppSec, application security, secure SDLC, security champions, threat modeling sprint, security requirements, secure code review"
origin: zakr
metadata:
  namespace: zakr/devtools-pack
  version: 1.0.0
  category: security
  language: security
  platforms: [claude-code, codex, gemini-cli, cursor, aider, windsurf]
---
# Application Security Patterns

## Secure SDLC Integration

```
Phase 1 — Requirements:
  ✓ Security user stories in backlog
  ✓ Abuse cases alongside use cases
  ✓ Compliance requirements identified (GDPR, HIPAA, PCI)
  ✓ Data classification for each feature

Phase 2 — Design:
  ✓ Threat model created (STRIDE)
  ✓ Security architecture review
  ✓ Data flow diagrams with trust boundaries

Phase 3 — Development:
  ✓ Secure coding guidelines enforced
  ✓ SAST in IDE (Semgrep, SonarLint)
  ✓ Pre-commit hooks: secrets scan, lint

Phase 4 — Testing:
  ✓ SAST in CI pipeline
  ✓ Dependency audit (pip-audit, npm audit)
  ✓ DAST on staging (OWASP ZAP, Burp)
  ✓ Security regression tests

Phase 5 — Deployment:
  ✓ Container image scanning
  ✓ Infrastructure as Code security scan (tfsec, checkov)
  ✓ Secret rotation before release

Phase 6 — Operations:
  ✓ Runtime security monitoring
  ✓ Vulnerability disclosure process
  ✓ Incident response playbook
```

## Security User Stories

```
Feature: User Authentication

Security Story 1:
  AS a security engineer
  I WANT passwords hashed with argon2id
  SO THAT a database breach doesn't expose credentials

Acceptance Criteria:
  - Password stored as argon2id hash (m=65536, t=3, p=4)
  - Plaintext never logged
  - Hash verified in constant time

Abuse Case:
  An attacker with DB dump cannot crack passwords within 1 year
  on consumer GPU hardware
```

## Security Requirements Template

```yaml
# security-requirements.yaml
authentication:
  mfa_required: true
  session_timeout_minutes: 30
  max_failed_attempts: 5
  lockout_duration_minutes: 15
  password_policy:
    min_length: 12
    require_uppercase: true
    require_number: true
    bcrypt_rounds: 12

authorization:
  model: RBAC
  principle: least_privilege
  idor_protection: server_side_ownership_check

data:
  pii_fields: [email, phone, ssn, dob]
  encryption_at_rest: AES-256-GCM
  retention_days: 365
  deletion: hard_delete_on_request

api:
  rate_limiting: 100req/min/user
  input_validation: strict
  output_encoding: json_escape
  cors_origins: [https://app.example.com]
```

## Security Champions Program

```markdown
## Security Champion Responsibilities

Per-team champion (1 developer per squad):
- Attends monthly AppSec office hours
- Reviews PRs touching auth/crypto/data handling
- Runs threat model for new features
- Triages SAST findings from CI
- Escalates critical findings to security team

Champion Rotation: every 6 months
Training: OWASP Top 10, secure code review, threat modeling
Recognition: conference budget, public acknowledgment
```

## Secure Code Review Checklist

```python
# Authentication
assert password_hashed_with_strong_algo()      # argon2/bcrypt not MD5
assert constant_time_comparison_used()          # hmac.compare_digest
assert session_invalidated_on_logout()

# Authorization
assert ownership_verified_before_access()       # user.id == resource.owner_id
assert privilege_check_server_side()            # not just in UI

# Input Validation
assert input_validated_at_boundary()
assert sql_uses_parameterized_queries()
assert file_paths_sanitized()

# Output
assert html_output_escaped()
assert json_content_type_set()
assert sensitive_data_not_in_logs()

# Cryptography
assert no_custom_crypto()
assert strong_random_used()                     # secrets.token_hex not random.random
assert tls_verified()                           # not verify=False
```

## DAST with OWASP ZAP

```bash
# Baseline scan (passive only)
docker run -t owasp/zap2docker-stable zap-baseline.py \
  -t https://staging.example.com \
  -r zap-report.html

# Full scan (active — use only on owned systems)
docker run -t owasp/zap2docker-stable zap-full-scan.py \
  -t https://staging.example.com \
  -r zap-full-report.html \
  -z "-config scanner.attackStrength=HIGH"

# API scan
docker run -t owasp/zap2docker-stable zap-api-scan.py \
  -t https://staging.example.com/openapi.json \
  -f openapi \
  -r api-report.html
```

## Security Metrics

```python
# Track these in your security dashboard
metrics = {
    "mean_time_to_remediate_critical": "<24h",
    "mean_time_to_remediate_high": "<7d",
    "sast_findings_per_kloc": "<2",
    "dependency_vulnerabilities_open": 0,    # Critical/High
    "secrets_detected_in_code": 0,
    "security_debt_ratio": "<5%",            # security issues / total issues
    "coverage_security_tests": ">80%",
    "pentest_findings_open_critical": 0,
}
```

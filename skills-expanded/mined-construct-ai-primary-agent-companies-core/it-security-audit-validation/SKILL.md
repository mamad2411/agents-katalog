---
title: IT Security Audit & Validation
description: Skill for RLS policy checking, access control validation, security configuration review, and vulnerability assessment in the ConstructAI platform
frequency: Monthly or on-demand for security incidents
success_rate: 95%
tags:
  - it-operations
  - security-audit
  - rls-policies
  - access-control
  - vulnerability-assessment
  - 02050_information-technology
docs:
  - docs_construct_ai/disciplines/02050_information-technology/agent-data/domain-knowledge/02050_DOMAIN-KNOWLEDGE.MD
  - docs_construct_ai/disciplines/02050_information-technology/agent-data/domain-knowledge/02050_GLOSSARY.MD
  - docs_construct_ai/disciplines/02050_information-technology/agent-data/prompts/02050_AI-NATIVE-INFORMATION-TECHNOLOGY-PROMPT.md
  - docs_construct_ai/skills/shared/systematic-debugging/SKILL.md
---

# IT Security Audit & Validation

## Overview

This skill covers security audit and validation for the ConstructAI platform. It encompasses RLS policy verification, access control testing, encryption validation, security configuration review, and vulnerability assessment. Primary agent: 02050-007 Security Auditor. Supporting skills: `shared/systematic-debugging`.

## Triggers

- Monthly security audit scheduled
- New RLS policy deployed
- Access control configuration change
- Security incident detected
- Compliance audit due (quarterly/annual)
- New role or permission added

## Prerequisites

- Access to RLS policy definitions and database
- Knowledge of role hierarchy and permission matrix
- Understanding of data classification levels
- Access to security baseline configurations
- Understanding of compliance requirements

## Steps

### Step 1: RLS Policy Verification
- List all RLS policies in database
- Verify policy syntax and correctness
- Cross-reference policies with role definitions
- Identify policies missing table coverage
- Check for overly permissive policies

### Step 2: Access Control Testing
- Test access for each role against expected permissions
- Verify row-level restrictions function correctly
- Test cross-tenant data isolation
- Verify admin overrides function correctly
- Test edge cases (multiple roles, inherited permissions)

### Step 3: Encryption Validation
- Verify data at rest encryption for sensitive tables
- Verify TLS/TLS for all API connections
- Check encryption key rotation schedules
- Verify no unencrypted sensitive data in logs
- Check credential storage (hashed, not plain text)

### Step 4: Security Configuration Review
- Review security headers (CSP, HSTS, X-Frame-Options)
- Check session management configuration (expiry, rotation)
- Verify CSRF protection active
- Check rate limiting configuration
- Review authentication method security (MFA, password policies)

### Step 5: Vulnerability Assessment
- Review recent security advisories for dependencies
- Check for known SQL injection patterns in queries
- Check for XSS vulnerability patterns in output
- Check for authentication bypass patterns
- Verify input validation on all user-facing endpoints

### Step 6: Access Log Review
- Review access logs for unusual patterns
- Check for unauthorized access attempts
- Verify all access attempts are logged
- Check for privilege escalation attempts
- Correlate with error logs for security anomalies

### Step 7: Compliance Verification
- Verify data retention policies are enforced
- Check audit trail completeness
- Verify consent and privacy compliance
- Check export controls and data sovereignty
- Verify incident response procedures are current

### Step 8: Report & Remediation
- Generate security audit report with findings
- Prioritize findings by severity and likelihood
- Recommend specific remediation for each finding
- Track remediation actions and completion
- Update security baselines based on findings

## Success Criteria

- All RLS policies verified and correctly configured
- Access control tests pass for all roles
- Encryption validated for all sensitive data
- Security configuration meets baseline requirements
- No critical vulnerabilities identified
- Access logs complete and reviewed
- Compliance requirements verified
- Report generated with prioritized recommendations

## Common Pitfalls

1. **Incomplete role testing**: Test all roles, not just common ones
2. **Ignoring inherited permissions**: Complex role hierarchies create subtle issues
3. **Static encryption keys**: Verify key rotation actually happens
4. **False sense of security**: Automated scans miss logic vulnerabilities
5. **Missing log gaps**: Verify logging covers ALL access attempts
6. **Outdated compliance**: Compliance frameworks update regularly — verify currency

## Cross-References

- `shared/systematic-debugging/SKILL.md` — Root cause analysis for security findings
- `it-error-discovery-classification/SKILL.md` — Security-related error classification
- `it-log-analysis-monitoring/SKILL.md` — Continuous security log monitoring
- `it-performance-monitoring-analytics/SKILL.md` — Dashboard for security metrics

## Usage

Apply this skill for scheduled security audits, configuration change validation, incident investigations, and compliance verification. This is a critical skill for maintaining platform security posture.

## Metrics

- **Policy Coverage**: 100% of tables with sensitive data have RLS policies
- **Test Pass Rate**: 95%+ of access control tests pass
- **Encryption Compliance**: 100% of sensitive data encrypted at rest and in transit
- **Vulnerability Resolution**: 100% of critical findings remediated within SLA
- **Log Completeness**: 100% of access attempts logged and reviewed
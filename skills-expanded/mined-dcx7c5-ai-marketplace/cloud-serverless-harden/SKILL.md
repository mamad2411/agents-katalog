---
name: cloud-serverless-harden
description: "Comprehensive security hardening and assessment guide for AWS Lambda and serverless architectures, covering cold starts, event injection, IAM execution roles, function URLs, layers, concurrency controls, and vulnerability scanning."
domain: cybersecurity
---

## Cold Start
Initial function invocation that includes container provisioning, increasing latency and creating a window where cached secrets may not be available.

## Event Injection
Attack where malicious input is embedded in Lambda event data from API Gateway, S3, SQS, or other event sources to exploit the function.

## Execution Role
IAM role assumed by Lambda during execution, defining all cloud API permissions the function can use.

## Function URL
Direct HTTPS endpoint for Lambda functions that can be configured with IAM or no authentication (NONE is insecure).

## Layer
Lambda deployment package containing shared code or dependencies that should be scanned for vulnerabilities independently.

## Reserved Concurrency
Maximum number of concurrent executions for a function, useful for preventing resource exhaustion attacks.

## Provisioned Concurrency
Pre-initialized function instances that reduce cold start latency and ensure secrets are cached.

## Tools & Systems

- **AWS Lambda Power Tuning**: Open-source tool for optimizing Lambda memory and timeout settings to balance security with performance.
- **Snyk**: SCA tool scanning Lambda dependencies for known vulnerabilities with automatic fix suggestions.
- **Semgrep**: SAST tool with serverless-specific rules detecting injection vulnerabilities, hardcoded secrets, and insecure configurations.
- **GuardDuty Lambda Protection**: AWS service monitoring Lambda network activity for connections to malicious endpoints.
- **AWS X-Ray**: Distributed tracing service for detecting suspicious external connections and latency anomalies in Lambda invocations.

## Common Scenarios

### Scenario: SQL Injection via API Gateway to Lambda to RDS

**Context**: A Lambda function receives user input from API Gateway and constructs SQL queries by string concatenation against an RDS PostgreSQL database. An attacker injects SQL payloads through the API.

**Approach**:
1. Audit the Lambda function code for string concatenation in SQL queries.
2. Replace all string-formatted queries with parameterized queries using the database driver.
3. Implement input validation using JSON Schema before any database operation.
4. Add a WAF rule on API Gateway to block common SQL injection patterns.
5. Deploy Semgrep in the CI/CD pipeline with the `python.django.security.injection.sql` rule set.
6. Enable GuardDuty Lambda protection to detect anomalous database connection patterns.

**Pitfalls**: Relying solely on WAF rules without fixing the underlying code vulnerability allows attackers to bypass with encoding tricks. Using ORM methods incorrectly (raw queries) still allows injection.

## Output Format

```
Serverless Security Assessment Report
=======================================
Account: 123456789012
Functions Assessed: 47
Assessment Date: 2025-02-23

CRITICAL FINDINGS:
  [SLS-001] order-processor: SQL injection via string concatenation
    Language: Python 3.12 | Runtime: Lambda
    Vulnerable Code: f"SELECT * FROM orders WHERE id = '{order_id}'"
    Remediation: Use parameterized queries with psycopg2

  [SLS-002] payment-handler: Hardcoded Stripe API key in environment variable
    Key: sk_live_XXXX... (unencrypted)
    Remediation: Migrate to AWS Secrets Manager with KMS encryption

HIGH FINDINGS:
  [SLS-003] 12 functions share the same IAM execution role with s3:*
  [SLS-004] 8 functions have function URLs with AuthType: NONE
  [SLS-005] 23 functions have dependencies with known HIGH CVEs

DEPENDENCY VULNERABILITIES:
  axios@0.21.1:         CVE-2023-45857 (HIGH) - 5 functions affected
  jsonwebtoken@8.5.1:   CVE-2022-23529 (CRITICAL) - 3 functions affected
  lodash@4.17.15:       CVE-2021-23337 (HIGH) - 11 functions affected

SUMMARY:
  Critical: 2 | High: 5 | Medium: 12 | Low: 8
  Functions with Least Privilege: 14/47 (30%)
  Functions with Secrets Manager: 19/47 (40%)
  Functions with Input Validation: 22/47 (47%)
```

---
name: iac-fast-scan
description: Single-pass, token-optimized IaC security scan. Covers all 6 domains in one file. Use instead of individual skills when running "Run fast IaC scan".
---

# iac-fast-scan

You are an AWS IaC security scanner performing a single-pass analysis across all security domains. You do NOT generate remediation — you identify and prioritize risks only.

## CRITICAL RULES

1. **No remediation.** Do not suggest fixes, code changes, migration steps, or "how to fix" guidance.
2. **High and Critical only.** Skip Medium/Low/Info findings.
3. **Confidence score on every finding.** Use 0.0–1.0 scale. ≥0.9 = direct IaC evidence. 0.7–0.89 = strong inference. 0.5–0.69 = moderate inference. <0.5 = speculative (include only if Critical).
4. **Evidence required.** Every finding must cite file:line.
5. **No architecture diagram.** Describe architecture in prose instead.
6. **Single output file.** Write findings to `iac-scan/fast-results.md`.

## FILE SCOPE

Scan only secrets-relevant and IaC files. **Skip:** `*.md`, `docs/`, `node_modules/`, `vendor/`, `.terraform/providers/`, lockfiles, binaries.

Include: `*.tf`, `*.tfvars`, `*.yaml`, `*.yml`, `*.json` (IaC), `.env*`, CI/CD (`.github/workflows/*`, `buildspec.yml`, etc.), `serverless.yml`, `samconfig.toml`.

## ANALYSIS CHECKLIST

Read scoped files once. For each file, check ALL domains simultaneously:

### IAM

- [ ] Wildcard `Action: *` or `Resource: *` on non-bootstrap roles
- [ ] `iam:PassRole` without resource/service condition
- [ ] `sts:AssumeRole` trust to `*` or broad principals
- [ ] Cross-account trust without `sts:ExternalId`
- [ ] Managed policy `AdministratorAccess` or `PowerUserAccess` on workload roles
- [ ] Missing permission boundaries on roles that create other roles
- [ ] Overprivileged Lambda/ECS/EC2 execution roles (actions far exceeding workload purpose)
- [ ] `kms:Decrypt` on `*` without `kms:ViaService` or encryption context conditions
- [ ] ECS Exec enabled broadly without caller-side IAM constraints

### Network

- [ ] Security group ingress `0.0.0.0/0` on non-80/443 ports (especially 22, 3389, 5432, 3306, 27017)
- [ ] `publicly_accessible = true` on RDS/Redshift/ElastiCache
- [ ] Missing `aws_s3_bucket_public_access_block`
- [ ] Internet Gateway + route table + public subnet + workload without WAF
- [ ] VPC peering with full CIDR routes (flat network)
- [ ] Security groups using VPC CIDR instead of source security group references
- [ ] Database subnets with NAT/IGW default routes
- [ ] No VPC endpoints for sensitive services (SSM, KMS, S3, ECR)
- [ ] ALB/NLB without WAF association

### Storage

- [ ] S3 bucket policy with `Principal: *`
- [ ] Missing server-side encryption (no SSE config block)
- [ ] RDS `deletion_protection = false` in production
- [ ] RDS `multi_az = false` in production
- [ ] Backup retention < 7 days in production
- [ ] Missing versioning on data buckets
- [ ] No Object Lock on compliance-sensitive buckets
- [ ] DynamoDB without PITR
- [ ] KMS key policy with broad `kms:Decrypt` to `Principal: *` (even with org condition)

### Secrets

- [ ] AWS access key patterns (`AKIA[A-Z0-9]{16}`) in source files
- [ ] Plaintext passwords/tokens in environment variables, user data, or config
- [ ] Private key blocks (`-----BEGIN.*PRIVATE KEY-----`)
- [ ] Database connection strings with embedded credentials
- [ ] `.env` files or `terraform.tfvars` with secrets committed
- [ ] SSM parameter values hardcoded instead of referenced
- [ ] CloudFormation outputs exposing secret retrieval commands

### Logging & Monitoring

- [ ] No `aws_cloudtrail` resource in scope
- [ ] No `aws_guardduty_detector` resource in scope
- [ ] CloudTrail with `is_multi_region_trail = false`
- [ ] ALB/NLB access logging disabled
- [ ] No VPC Flow Logs
- [ ] No CloudWatch alarms on security-relevant metrics
- [ ] Log groups with no retention policy (infinite retention)
- [ ] Log groups with `RemovalPolicy.DESTROY` in production
- [ ] Missing S3 access logging on sensitive buckets

### Serverless

- [ ] Lambda Function URL with `authorization_type = "NONE"`
- [ ] API Gateway method/route with `authorization = "NONE"` on sensitive endpoints
- [ ] Lambda execution role with dangerous permissions (iam:*, s3:*, dynamodb:*)
- [ ] No `reserved_concurrent_executions` on public-triggered functions
- [ ] SQS/SNS event sources without DLQ
- [ ] Secrets in Lambda environment variables (plaintext)
- [ ] API Gateway without throttling/usage plan
- [ ] Missing WAF on API Gateway

## ENVIRONMENT DETECTION

Classify each resource's environment from these signals (highest to lowest confidence):
1. Explicit tags: `Environment=prod`
2. Directory path: `envs/prod/`, `environments/production/`
3. Resource name contains: `prod`, `production`, `staging`, `dev`
4. Workspace/provider alias
5. Config file name: `cdc-prod.yaml`, `production.tfvars`

Production findings are always higher severity than dev equivalents.

## SEVERITY CALIBRATION

**Critical:** Internet-reachable + exploitable + account-wide blast radius + production. Example: public Lambda with admin IAM and no auth.

**High:** One of: (a) internet-reachable with significant blast radius, (b) exploitable privilege escalation in production, (c) complete detection blindness in production, (d) public data exposure with sensitive classification.

Skip Medium/Low/Info in fast mode.

## OUTPUT FORMAT

Write `iac-scan/fast-results.md`:

```markdown
# Fast IaC Security Scan Results

**Repository:** {path}
**Scan date:** {date}
**Mode:** Fast (single-pass, High/Critical only)

## Architecture Summary

{2-3 paragraphs describing the inferred architecture: VPCs, workloads, data stores, entry points, environments. State confidence level.}

## Findings

### {FINDING-ID}: {title}

**Severity:** Critical|High
**Confidence:** {0.0-1.0}
**Domain:** IAM|Network|Storage|Secrets|Logging|Serverless
**Environment:** {prod|dev|staging|shared|unknown}
**Evidence:**
- `{file}:{line}` — `{code snippet}`

**Risk:** {2-3 sentences explaining what an attacker could do, blast radius, detection probability}

**Related findings:** {IDs of findings that compound with this one}

---

{repeat for each finding}

## Cross-Domain Risks

{Brief description of how findings combine across domains. No full attack chain analysis, just obvious compound risks like "public endpoint + admin IAM + no logging".}

## Positive Controls

{Bullet list of good security practices observed.}

## Limitations

- Fast mode: Medium/Low/Info findings omitted.
- No deep attack chain correlation.
- SKILL.md definitions not loaded; detection depth is reduced vs full scan.
- Run `Run IaC security scan` for complete coverage.
```

Then generate `iac-scan/fast-report.html` — a self-contained HTML report:

- Clean professional design, dark-mode compatible
- No external dependencies (all CSS inline)
- Executive summary at top
- Severity distribution table
- All findings with evidence
- Architecture summary in prose
- Footer: "Fast scan mode. Run full scan for complete coverage."

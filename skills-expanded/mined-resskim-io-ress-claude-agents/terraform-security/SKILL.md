---
name: terraform-security
category: infrastructure
description: "Terraform Security Patterns — Terraform 보안 패턴 및 best practices. Use when working with infrastructure 도메인의 패턴 / 구현 선택."
effort: xhigh
deprecated: false
---

# Terraform Security Patterns

Terraform 보안 패턴 및 best practices.

## Sensitive Variables

```hcl
# Mark as sensitive
variable "db_password" {
  description = "Database password"
  type        = string
  sensitive   = true
}

# Use AWS Secrets Manager
data "aws_secretsmanager_secret_version" "db_password" {
  secret_id = "prod/db/password"
}

resource "aws_db_instance" "main" {
  password = data.aws_secretsmanager_secret_version.db_password.secret_string
}
```

## IAM Minimal Permissions

```hcl
# BAD - Too broad
resource "aws_iam_policy" "bad" {
  policy = jsonencode({
    Statement = [{
      Effect   = "Allow"
      Action   = "*"
      Resource = "*"
    }]
  })
}

# GOOD - Minimal permissions
resource "aws_iam_policy" "good" {
  policy = jsonencode({
    Statement = [{
      Effect   = "Allow"
      Action   = ["s3:GetObject", "s3:PutObject"]
      Resource = "arn:aws:s3:::my-bucket/*"
    }]
  })
}
```

## Encryption

### S3 Bucket

```hcl
resource "aws_s3_bucket_server_side_encryption_configuration" "example" {
  bucket = aws_s3_bucket.example.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm     = "aws:kms"
      kms_master_key_id = aws_kms_key.example.arn
    }
  }
}
```

### RDS

```hcl
resource "aws_db_instance" "example" {
  storage_encrypted = true
  kms_key_id        = aws_kms_key.example.arn
}
```

### EBS

```hcl
resource "aws_ebs_volume" "example" {
  encrypted  = true
  kms_key_id = aws_kms_key.example.arn
}
```

## Security Groups

```hcl
# BAD - Open to world
resource "aws_security_group_rule" "bad" {
  type        = "ingress"
  from_port   = 22
  to_port     = 22
  protocol    = "tcp"
  cidr_blocks = ["0.0.0.0/0"]  # Dangerous!
}

# GOOD - Restricted access
resource "aws_security_group_rule" "good" {
  type        = "ingress"
  from_port   = 22
  to_port     = 22
  protocol    = "tcp"
  cidr_blocks = ["10.0.0.0/8"]  # VPN/Internal only
}
```

## S3 Bucket Security

```hcl
resource "aws_s3_bucket_public_access_block" "example" {
  bucket = aws_s3_bucket.example.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_versioning" "example" {
  bucket = aws_s3_bucket.example.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_logging" "example" {
  bucket = aws_s3_bucket.example.id
  target_bucket = aws_s3_bucket.logs.id
  target_prefix = "s3-access-logs/"
}
```

## tfsec Integration

```bash
# Install
brew install tfsec

# Run scan
tfsec .

# High severity only
tfsec --minimum-severity HIGH .

# CI/CD integration
tfsec --format json --out results.json .
```

## Common tfsec Checks

| Check | Issue | Fix |
|-------|-------|-----|
| AWS002 | S3 bucket logging disabled | Enable access logging |
| AWS004 | S3 bucket public access | Block public access |
| AWS009 | SG allows 0.0.0.0/0 | Restrict CIDR blocks |
| AWS017 | S3 bucket not encrypted | Enable SSE |
| AWS018 | Sensitive variable not marked | Add `sensitive = true` |
| AWS089 | CloudWatch logs not encrypted | Enable KMS encryption |

## Anti-patterns

| Mistake | Correct | Why |
|---------|---------|-----|
| Hardcoded secrets | Secrets Manager / SSM | Security exposure |
| `Action: "*"` | Specific actions | Least privilege |
| `Resource: "*"` | Specific ARNs | Scope limitation |
| `0.0.0.0/0` ingress | Specific CIDRs | Network security |
| No encryption | KMS encryption | Data protection |
| Public S3 buckets | Block public access | Data exposure |

**관련 skill**: `/terraform-modules`

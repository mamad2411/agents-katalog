---
name: Manage Secrets
description: Manage application secrets and configuration using AWS SSM Parameter Store and Secrets Manager, covering rotation policies, access control, environment variable injection into ECS tasks, audit logging, and secret lifecycle management.
---

# Manage Secrets

## Your Expertise

You are a **Senior Cloud Security Engineer** with 15+ years implementing secrets management for production applications on AWS. You've designed secrets architectures for SOC 2, HIPAA, and PCI-compliant environments. You are an expert in:

- AWS Secrets Manager — automatic rotation, cross-account access, Lambda rotation functions
- AWS Systems Manager Parameter Store — hierarchical configuration, SecureString encryption
- Secret rotation strategies — zero-downtime rotation for database credentials, API keys, tokens
- Application integration — SDK-based retrieval, environment variable injection, sidecar patterns
- Encryption — KMS key management, envelope encryption, key policies, key rotation
- Audit and compliance — CloudTrail logging, secret access monitoring, least-privilege access

You manage secrets so that no credential is hardcoded, no key is shared in Slack, and no rotation causes downtime. Every secrets architecture you design is auditable, rotatable, and recoverable.

---

## Project Configuration

> Customize this skill for your project. Fill in what applies, delete what doesn't.

### Secret Storage
<!-- Example: SSM Parameter Store (free tier) for most secrets, Secrets Manager for RDS auto-rotation -->

### Rotation Policy
<!-- Example: RDS credentials auto-rotated every 30 days, third-party API keys manually rotated every 90 days -->

### Access Controls
<!-- Example: ECS execution role has ssm:GetParameter on /myapp/{env}/* only, KMS decrypt on secrets key -->

### Audit Logging
<!-- Example: CloudTrail enabled, EventBridge rule alerts on PutParameter/DeleteParameter/GetSecretValue -->

### Encryption (KMS)
<!-- Example: Customer-managed KMS key per environment: alias/myapp-production-secrets, annual auto-rotation -->

---

## Common Rules

```
┌──────────────────────────────────────────────────────────────┐
│      MANDATORY RULES FOR EVERY SECRETS MANAGEMENT TASK       │
│                                                              │
│  1. NO HARDCODED SECRETS ANYWHERE                            │
│     → Never put credentials in source code, Dockerfiles,     │
│       docker-compose files, or Terraform tfvars              │
│     → Store all secrets in SSM Parameter Store (SecureString) │
│       or Secrets Manager — nowhere else                      │
│     → Add .env, *.pem, and credentials files to .gitignore   │
│       and set up pre-commit hooks to catch leaks             │
│     → If a secret is found in code, rotate it immediately    │
│       — assume it has been compromised                       │
│                                                              │
│  2. ROTATE REGULARLY WITHOUT DOWNTIME                        │
│     → Use Secrets Manager auto-rotation for database          │
│       credentials — never manually rotate DB passwords       │
│     → For third-party API keys, use a dual-key approach:     │
│       add the new key, deploy, verify, then revoke the old   │
│     → Force new ECS task deployments after updating secrets   │
│       so containers pick up the rotated values               │
│     → Test the rotation procedure in staging before applying │
│       it to production                                       │
│                                                              │
│  3. LEAST PRIVILEGE ACCESS TO SECRETS                        │
│     → Scope IAM policies to the exact SSM path:              │
│       /project/environment/* — never allow access to /*      │
│     → Use separate KMS keys per environment so a staging     │
│       role cannot decrypt production secrets                 │
│     → Grant ssm:GetParameter to the execution role only —    │
│       the task role should not read infrastructure secrets   │
│     → Review secret access permissions quarterly and revoke  │
│       anything no longer needed                              │
│                                                              │
│  4. AUDIT EVERY SECRET ACCESS                                │
│     → Enable CloudTrail for ssm:GetParameter, ssm:Put-      │
│       Parameter, secretsmanager:GetSecretValue events        │
│     → Set up EventBridge rules to alert on secret deletion,  │
│       modification, and failed access attempts               │
│     → Query CloudTrail logs monthly to identify unexpected   │
│       access patterns or unused secrets                      │
│     → Rotate any credential immediately after a team member  │
│       with access leaves the organization                    │
│                                                              │
│  5. ENCRYPTION AT REST AND IN TRANSIT                        │
│     → Use SecureString type for every credential in SSM —    │
│       never use plain String type for sensitive values       │
│     → Create customer-managed KMS keys with enable_key_      │
│       rotation = true for annual automatic rotation          │
│     → Restrict KMS key usage to specific roles via the key   │
│       policy — do not rely on IAM policies alone             │
│     → Ensure all secret retrieval happens over TLS — ECS     │
│       execution role calls use HTTPS endpoints by default    │
│                                                              │
│  6. NO AI TOOL REFERENCES — ANYWHERE                         │
│     → No AI mentions in parameter names, KMS key aliases,    │
│       or secrets documentation                               │
│     → All output reads as if written by a cloud security     │
│       engineer                                               │
└──────────────────────────────────────────────────────────────┘
```

---

## 1. SSM Parameter Store vs Secrets Manager

```
┌──────────────────────────────────────────────────────────────────────────┐
│          SSM Parameter Store vs AWS Secrets Manager                       │
│                                                                          │
│  Feature               │ SSM Parameter Store    │ Secrets Manager        │
│  ────────────────────────────────────────────────────────────────       │
│  Cost                  │ Free (standard tier)   │ $0.40/secret/month    │
│  Max size              │ 8 KB (advanced: 8 KB)  │ 64 KB                 │
│  Encryption            │ KMS (SecureString)     │ KMS (always encrypted)│
│  Rotation              │ Manual only            │ Built-in Lambda-based │
│  Versioning            │ Yes (history)          │ Yes (staging labels)  │
│  Cross-account sharing │ No (use RAM or assume) │ Yes (resource policy) │
│  Hierarchy             │ Yes (/app/env/key)     │ No (flat names)       │
│  CloudTrail audit      │ Yes                    │ Yes                   │
│  JSON secret support   │ Yes (as string)        │ Yes (native JSON)     │
│  Throughput            │ 40 TPS (standard)      │ 10,000 TPS            │
│                                                                          │
│  WHEN TO USE WHAT:                                                       │
│                                                                          │
│  SSM Parameter Store (default choice):                                   │
│    ✅ Application config (DATABASE_URL, JWT_SECRET, API keys)           │
│    ✅ Feature flags and toggles                                          │
│    ✅ Non-rotating credentials                                           │
│    ✅ When you need hierarchical paths (/myapp/prod/db/url)             │
│    ✅ When cost matters (free tier)                                      │
│                                                                          │
│  Secrets Manager (only when needed):                                     │
│    ✅ Database credentials with automatic rotation                      │
│    ✅ Third-party API keys that need rotation                           │
│    ✅ Cross-account secret sharing                                       │
│    ✅ Secrets > 8 KB (rare)                                              │
│    ✅ RDS managed master user password                                   │
└──────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Secret Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                     Secret Flow Architecture                             │
│                                                                          │
│  ┌──────────────────────────────────────────────────────────────┐       │
│  │  SSM Parameter Store                                          │       │
│  │  Path: /{project}/{environment}/{key}                         │       │
│  │                                                               │       │
│  │  /myapp/production/DATABASE_URL      (SecureString)          │       │
│  │  /myapp/production/JWT_SECRET        (SecureString)          │       │
│  │  /myapp/production/REDIS_URL         (String)                │       │
│  │  /myapp/production/SENDGRID_API_KEY  (SecureString)          │       │
│  │  /myapp/production/S3_BUCKET_NAME    (String)                │       │
│  │  /myapp/production/GOOGLE_CLIENT_ID  (String)                │       │
│  └──────────────┬───────────────────────────────────────────────┘       │
│                 │                                                        │
│                 │ Referenced at container start                          │
│                 ▼                                                        │
│  ┌──────────────────────────────────────────────────────────────┐       │
│  │  ECS Task Definition                                          │       │
│  │                                                               │       │
│  │  secrets: [                                                   │       │
│  │    { name: "DATABASE_URL",                                    │       │
│  │      valueFrom: "arn:aws:ssm:.../myapp/production/DB_URL" },│       │
│  │    { name: "JWT_SECRET",                                      │       │
│  │      valueFrom: "arn:aws:ssm:.../myapp/production/JWT..." }, │       │
│  │  ]                                                            │       │
│  │                                                               │       │
│  │  ECS Execution Role:                                          │       │
│  │    ssm:GetParameter on /myapp/production/*                   │       │
│  └──────────────┬───────────────────────────────────────────────┘       │
│                 │                                                        │
│                 │ Injected as environment variables                      │
│                 ▼                                                        │
│  ┌──────────────────────────────────────────────────────────────┐       │
│  │  Container Runtime                                            │       │
│  │                                                               │       │
│  │  process.env.DATABASE_URL  = "postgresql://..."              │       │
│  │  process.env.JWT_SECRET    = "abc123..."                     │       │
│  │  process.env.REDIS_URL     = "redis://..."                   │       │
│  │                                                               │       │
│  │  App code reads from process.env — never knows about SSM    │       │
│  └──────────────────────────────────────────────────────────────┘       │
│                                                                          │
│  ┌──────────────────────────────────────────────────────────────┐       │
│  │  Secrets Manager (rotation-capable)                           │       │
│  │                                                               │       │
│  │  myapp/production/rds-master     → Auto-rotated (30 days)   │       │
│  │  myapp/production/stripe         → Manual rotation           │       │
│  └──────────────────────────────────────────────────────────────┘       │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 3. SSM Parameter Store Implementation

### Creating Parameters

```hcl
# Non-sensitive config (String — not encrypted)
resource "aws_ssm_parameter" "redis_url" {
  name        = "/${local.project}/${local.environment}/REDIS_URL"
  type        = "String"
  value       = "redis://${aws_elasticache_replication_group.main.primary_endpoint_address}:6379"
  description = "Redis connection URL"

  tags = {
    Project     = local.project
    Environment = local.environment
    Service     = "backend"
  }
}

resource "aws_ssm_parameter" "s3_bucket" {
  name        = "/${local.project}/${local.environment}/S3_BUCKET_NAME"
  type        = "String"
  value       = aws_s3_bucket.uploads.id
  description = "S3 bucket for file uploads"

  tags = {
    Project     = local.project
    Environment = local.environment
  }
}

# Sensitive secrets (SecureString — KMS encrypted)
resource "aws_ssm_parameter" "database_url" {
  name        = "/${local.project}/${local.environment}/DATABASE_URL"
  type        = "SecureString"
  value       = "postgresql://${aws_db_instance.main.username}:${random_password.db.result}@${aws_db_instance.main.endpoint}/${aws_db_instance.main.db_name}?sslmode=require"
  description = "PostgreSQL connection string"
  key_id      = aws_kms_key.secrets.arn

  tags = {
    Project     = local.project
    Environment = local.environment
    Sensitive   = "true"
  }

  lifecycle {
    ignore_changes = [value]  # Don't overwrite if manually rotated
  }
}

resource "aws_ssm_parameter" "jwt_secret" {
  name        = "/${local.project}/${local.environment}/JWT_SECRET"
  type        = "SecureString"
  value       = random_password.jwt.result
  description = "JWT signing secret"
  key_id      = aws_kms_key.secrets.arn

  tags = {
    Project     = local.project
    Environment = local.environment
    Sensitive   = "true"
  }

  lifecycle {
    ignore_changes = [value]
  }
}

# Generate secure random values
resource "random_password" "db" {
  length           = 32
  special          = true
  override_special = "!#$%^&*()-_=+"
}

resource "random_password" "jwt" {
  length  = 64
  special = false
}
```

### KMS Key for Encryption

```hcl
resource "aws_kms_key" "secrets" {
  description             = "KMS key for ${local.project} ${local.environment} secrets"
  deletion_window_in_days = 30
  enable_key_rotation     = true

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "AllowRootFullAccess"
        Effect = "Allow"
        Principal = {
          AWS = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:root"
        }
        Action   = "kms:*"
        Resource = "*"
      },
      {
        Sid    = "AllowECSExecutionDecrypt"
        Effect = "Allow"
        Principal = {
          AWS = aws_iam_role.ecs_execution.arn
        }
        Action = [
          "kms:Decrypt",
          "kms:DescribeKey",
        ]
        Resource = "*"
      },
    ]
  })

  tags = {
    Name        = "${local.project}-${local.environment}-secrets-key"
    Environment = local.environment
  }
}

resource "aws_kms_alias" "secrets" {
  name          = "alias/${local.project}-${local.environment}-secrets"
  target_key_id = aws_kms_key.secrets.key_id
}
```

---

## 4. Secrets Manager with Rotation

```hcl
# Stripe API keys (manual rotation)
resource "aws_secretsmanager_secret" "stripe" {
  name        = "${local.project}/${local.environment}/stripe"
  description = "Stripe API keys"
  kms_key_id  = aws_kms_key.secrets.arn

  tags = {
    Project     = local.project
    Environment = local.environment
  }
}

resource "aws_secretsmanager_secret_version" "stripe" {
  secret_id = aws_secretsmanager_secret.stripe.id
  secret_string = jsonencode({
    secret_key      = var.stripe_secret_key
    publishable_key = var.stripe_publishable_key
    webhook_secret  = var.stripe_webhook_secret
  })

  lifecycle {
    ignore_changes = [secret_string]  # Don't overwrite manual updates
  }
}

# RDS credentials (auto-rotation every 30 days)
resource "aws_secretsmanager_secret" "rds_credentials" {
  name        = "${local.project}/${local.environment}/rds-credentials"
  description = "RDS master credentials with automatic rotation"
  kms_key_id  = aws_kms_key.secrets.arn

  tags = {
    Project     = local.project
    Environment = local.environment
    Rotation    = "automatic"
  }
}

resource "aws_secretsmanager_secret_rotation" "rds" {
  secret_id           = aws_secretsmanager_secret.rds_credentials.id
  rotation_lambda_arn = aws_lambda_function.rotate_rds.arn

  rotation_rules {
    automatically_after_days = 30
  }
}
```

---

## 5. ECS Task Definition — Secret Injection

```hcl
resource "aws_ecs_task_definition" "backend" {
  family                   = "${local.project}-${local.environment}-backend"
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = 512
  memory                   = 1024
  execution_role_arn       = aws_iam_role.ecs_execution.arn
  task_role_arn            = aws_iam_role.ecs_task.arn

  container_definitions = jsonencode([{
    name      = "backend"
    image     = "${aws_ecr_repository.backend.repository_url}:latest"
    essential = true

    # Non-sensitive config (plain text)
    environment = [
      { name = "NODE_ENV", value = "production" },
      { name = "PORT", value = "3001" },
      { name = "LOG_LEVEL", value = "info" },
    ]

    # Sensitive secrets (injected from SSM/SecretsManager at container start)
    secrets = [
      # SSM Parameter Store references
      {
        name      = "DATABASE_URL"
        valueFrom = "arn:aws:ssm:us-east-1:${data.aws_caller_identity.current.account_id}:parameter/${local.project}/${local.environment}/DATABASE_URL"
      },
      {
        name      = "JWT_SECRET"
        valueFrom = "arn:aws:ssm:us-east-1:${data.aws_caller_identity.current.account_id}:parameter/${local.project}/${local.environment}/JWT_SECRET"
      },
      {
        name      = "REDIS_URL"
        valueFrom = "arn:aws:ssm:us-east-1:${data.aws_caller_identity.current.account_id}:parameter/${local.project}/${local.environment}/REDIS_URL"
      },
      {
        name      = "SENDGRID_API_KEY"
        valueFrom = "arn:aws:ssm:us-east-1:${data.aws_caller_identity.current.account_id}:parameter/${local.project}/${local.environment}/SENDGRID_API_KEY"
      },

      # Secrets Manager references (JSON key extraction with ::)
      {
        name      = "STRIPE_SECRET_KEY"
        valueFrom = "${aws_secretsmanager_secret.stripe.arn}:secret_key::"
      },
      {
        name      = "STRIPE_WEBHOOK_SECRET"
        valueFrom = "${aws_secretsmanager_secret.stripe.arn}:webhook_secret::"
      },
    ]

    # ... rest of container definition
  }])
}
```

### Execution Role Permissions for Secrets

```hcl
resource "aws_iam_role_policy" "ecs_execution_secrets" {
  name = "secrets-access"
  role = aws_iam_role.ecs_execution.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "ReadSSMParameters"
        Effect = "Allow"
        Action = [
          "ssm:GetParameters",
          "ssm:GetParameter",
        ]
        Resource = [
          "arn:aws:ssm:us-east-1:${data.aws_caller_identity.current.account_id}:parameter/${local.project}/${local.environment}/*"
        ]
      },
      {
        Sid    = "ReadSecretsManager"
        Effect = "Allow"
        Action = [
          "secretsmanager:GetSecretValue",
        ]
        Resource = [
          "arn:aws:secretsmanager:us-east-1:${data.aws_caller_identity.current.account_id}:secret:${local.project}/${local.environment}/*"
        ]
      },
      {
        Sid    = "DecryptWithKMS"
        Effect = "Allow"
        Action = [
          "kms:Decrypt",
        ]
        Resource = [
          aws_kms_key.secrets.arn
        ]
      },
    ]
  })
}
```

---

## 6. Secret Naming Convention

```
┌──────────────────────────────────────────────────────────────────────┐
│                   Secret Naming Standards                             │
│                                                                       │
│  SSM Parameter Store:                                                 │
│  Format: /{project}/{environment}/{KEY_NAME}                         │
│                                                                       │
│  Examples:                                                            │
│  /myapp/production/DATABASE_URL                                       │
│  /myapp/production/JWT_SECRET                                         │
│  /myapp/production/REDIS_URL                                          │
│  /myapp/production/GOOGLE_CLIENT_ID                                   │
│  /myapp/production/GOOGLE_CLIENT_SECRET                               │
│  /myapp/staging/DATABASE_URL                                          │
│  /myapp/staging/JWT_SECRET                                            │
│                                                                       │
│  Secrets Manager:                                                     │
│  Format: {project}/{environment}/{service-name}                      │
│                                                                       │
│  Examples:                                                            │
│  myapp/production/stripe        → { secret_key, publishable_key }    │
│  myapp/production/sendgrid      → { api_key }                        │
│  myapp/production/rds-master    → { username, password, host, port } │
│                                                                       │
│  Rules:                                                               │
│  1. Always include project and environment in the path               │
│  2. Use UPPER_SNAKE_CASE for parameter names (matches env vars)      │
│  3. Use lowercase kebab-case for Secrets Manager names               │
│  4. Never include the actual secret value in the name                │
│  5. Group related secrets (e.g., all Stripe keys in one SM secret)  │
│  6. Use "String" type for non-sensitive config, "SecureString" for  │
│     anything credential-related                                       │
└──────────────────────────────────────────────────────────────────────┘
```

---

## 7. Audit Logging

### CloudTrail for Secret Access

```hcl
resource "aws_cloudwatch_log_group" "secret_access" {
  name              = "/aws/cloudtrail/${local.project}-secret-access"
  retention_in_days = 90

  tags = {
    Purpose = "Security audit - secret access logging"
  }
}

# CloudTrail event rule for secret access
resource "aws_cloudwatch_event_rule" "secret_access" {
  name        = "${local.project}-secret-access-alert"
  description = "Alert on unusual secret access patterns"

  event_pattern = jsonencode({
    source      = ["aws.ssm", "aws.secretsmanager"]
    detail-type = ["AWS API Call via CloudTrail"]
    detail = {
      eventName = [
        "GetParameter",
        "GetParameters",
        "GetSecretValue",
        "PutParameter",
        "DeleteParameter",
        "UpdateSecret",
        "DeleteSecret",
      ]
      requestParameters = {
        name = [{ prefix = "/${local.project}/" }]
      }
    }
  })
}

resource "aws_cloudwatch_event_target" "secret_access_log" {
  rule      = aws_cloudwatch_event_rule.secret_access.name
  target_id = "log-secret-access"
  arn       = aws_cloudwatch_log_group.secret_access.arn
}
```

### Useful Audit Queries

```
# Who accessed production database credentials in the last 24 hours?
fields @timestamp, userIdentity.arn, requestParameters.name, sourceIPAddress
| filter eventSource = "ssm.amazonaws.com"
| filter eventName = "GetParameter" OR eventName = "GetParameters"
| filter requestParameters.name like "/myapp/production/DATABASE"
| sort @timestamp desc

# Who modified any secret in the last 7 days?
fields @timestamp, userIdentity.arn, eventName, requestParameters.name
| filter eventSource in ["ssm.amazonaws.com", "secretsmanager.amazonaws.com"]
| filter eventName in ["PutParameter", "UpdateSecret", "DeleteParameter", "DeleteSecret"]
| sort @timestamp desc

# Failed secret access attempts (potential unauthorized access)
fields @timestamp, userIdentity.arn, errorCode, errorMessage, requestParameters.name
| filter errorCode != ""
| filter eventSource in ["ssm.amazonaws.com", "secretsmanager.amazonaws.com"]
| sort @timestamp desc
```

---

## 8. CLI Commands for Secret Management

```bash
# --- SSM Parameter Store ---

# Create a new secret
aws ssm put-parameter \
  --name "/myapp/production/NEW_API_KEY" \
  --type "SecureString" \
  --value "sk_live_abc123..." \
  --key-id "alias/myapp-production-secrets" \
  --description "New third-party API key" \
  --tags "Key=Project,Value=myapp" "Key=Environment,Value=production"

# Read a secret
aws ssm get-parameter \
  --name "/myapp/production/DATABASE_URL" \
  --with-decryption \
  --query "Parameter.Value" --output text

# List all secrets for an environment
aws ssm get-parameters-by-path \
  --path "/myapp/production" \
  --recursive \
  --query "Parameters[*].{Name:Name,Type:Type,Version:Version,Modified:LastModifiedDate}" \
  --output table

# Update a secret (creates new version)
aws ssm put-parameter \
  --name "/myapp/production/JWT_SECRET" \
  --type "SecureString" \
  --value "new-secret-value-here" \
  --overwrite

# View secret history (versions)
aws ssm get-parameter-history \
  --name "/myapp/production/JWT_SECRET" \
  --query "Parameters[*].{Version:Version,Modified:LastModifiedDate,ModifiedBy:LastModifiedUser}" \
  --output table

# --- Secrets Manager ---

# Create a JSON secret
aws secretsmanager create-secret \
  --name "myapp/production/stripe" \
  --secret-string '{"secret_key":"sk_live_...","publishable_key":"pk_live_...","webhook_secret":"whsec_..."}' \
  --kms-key-id "alias/myapp-production-secrets"

# Read a specific JSON key from a secret
aws secretsmanager get-secret-value \
  --secret-id "myapp/production/stripe" \
  --query "SecretString" --output text | jq -r '.secret_key'

# Rotate a secret immediately
aws secretsmanager rotate-secret \
  --secret-id "myapp/production/rds-credentials"

# View rotation status
aws secretsmanager describe-secret \
  --secret-id "myapp/production/rds-credentials" \
  --query "{RotationEnabled:RotationEnabled,LastRotated:LastRotatedDate,NextRotation:NextRotationDate}" \
  --output table
```

---

## 9. Secret Rotation Workflow

```
┌─────────────────────────────────────────────────────────────────────┐
│                  Secret Rotation Decision Tree                       │
│                                                                      │
│  What type of secret?                                                │
│  │                                                                   │
│  ├─ Database credentials                                            │
│  │   └─ Use Secrets Manager with automatic rotation                 │
│  │       ├─ RDS: Use manage_master_user_password (native)           │
│  │       └─ Custom DB: Lambda rotation function                     │
│  │                                                                   │
│  ├─ Third-party API keys (Stripe, SendGrid, etc.)                   │
│  │   └─ Manual rotation                                             │
│  │       ├─ Generate new key in third-party dashboard               │
│  │       ├─ Update SSM/SecretsManager                               │
│  │       ├─ Restart ECS tasks to pick up new value                  │
│  │       └─ Revoke old key after confirming new works               │
│  │                                                                   │
│  ├─ JWT signing secret                                               │
│  │   └─ Manual rotation with dual-key support                       │
│  │       ├─ Add new key to app (accept both old + new)              │
│  │       ├─ Deploy app with dual-key support                        │
│  │       ├─ Wait for old tokens to expire                           │
│  │       └─ Remove old key, deploy again                            │
│  │                                                                   │
│  └─ Encryption keys (KMS)                                           │
│      └─ Automatic rotation (enable_key_rotation = true)             │
│          └─ AWS rotates annually, old versions still decrypt        │
└─────────────────────────────────────────────────────────────────────┘
```

### Manual Rotation Script

```bash
#!/bin/bash
# rotate-api-key.sh — Rotate a third-party API key
set -euo pipefail

PARAM_NAME="/myapp/production/SENDGRID_API_KEY"
NEW_VALUE="$1"
CLUSTER="myapp-production"
SERVICE="myapp-production-backend"

if [ -z "${NEW_VALUE}" ]; then
  echo "Usage: $0 <new-api-key-value>"
  exit 1
fi

echo "Step 1: Updating SSM parameter..."
aws ssm put-parameter \
  --name "${PARAM_NAME}" \
  --type "SecureString" \
  --value "${NEW_VALUE}" \
  --overwrite

echo "Step 2: Restarting ECS tasks to pick up new secret..."
aws ecs update-service \
  --cluster "${CLUSTER}" \
  --service "${SERVICE}" \
  --force-new-deployment

echo "Step 3: Waiting for service stability..."
aws ecs wait services-stable \
  --cluster "${CLUSTER}" \
  --services "${SERVICE}"

echo "Rotation complete. Verify the service is healthy, then revoke the old API key."
```

---

## 10. Cost Implications

| Resource | Cost | Notes |
|----------|------|-------|
| SSM Parameter Store (Standard) | Free | Up to 10,000 parameters |
| SSM Parameter Store (Advanced) | $0.05/parameter/month | Higher throughput, policies |
| Secrets Manager | $0.40/secret/month | Per secret stored |
| Secrets Manager API calls | $0.05/10,000 calls | GetSecretValue |
| KMS key | $1/month per key | Plus $0.03/10,000 API calls |
| KMS automatic rotation | Free | Included in key cost |
| CloudTrail (for auditing) | Free (1 trail) | Additional trails cost extra |

### Cost Optimization

- Use SSM Parameter Store (free) for most secrets; only use Secrets Manager when rotation is required
- Share one KMS key across all secrets in an environment (don't create per-secret keys)
- Use parameter path hierarchy to organize (e.g., /myapp/production/* uses one policy)
- Avoid Secrets Manager for static secrets that never rotate

---

## 11. Security Considerations

- Never store secrets in environment variables in Dockerfiles or docker-compose files
- Never commit secrets to git (use .gitignore, pre-commit hooks)
- Never log secret values (mask in application logging)
- Use SecureString type for all credentials in SSM
- Enable KMS key rotation for encryption keys
- Restrict SSM/SecretsManager access to specific parameter paths (not *)
- Enable CloudTrail for auditing all secret access
- Use separate KMS keys per environment (prod key cannot decrypt staging secrets)
- Rotate credentials after any team member departure
- Never pass secrets as command-line arguments (visible in process list)

---

## 12. Common Mistakes / Anti-Patterns

| Mistake | Why It's Bad | Fix |
|---------|-------------|-----|
| Secrets in .env files committed to git | Exposed in repository history forever | Use SSM/SecretsManager, add .env to .gitignore |
| `Resource: "*"` on SSM access | Role can read ALL parameters in account | Scope to `parameter/{project}/{environment}/*` |
| Using same secret across environments | Staging incident exposes production | Separate paths per environment |
| No KMS encryption on SSM params | Stored as plaintext in AWS | Always use `SecureString` type |
| Hardcoding secrets in Terraform | Visible in state file | Use `random_password` + `ignore_changes` |
| Not restarting ECS after rotation | Containers still use old secret | Force new deployment after updating secrets |
| Using Secrets Manager for everything | Unnecessary cost ($0.40/secret/month) | Use free SSM Parameter Store for non-rotating secrets |
| No audit trail | Cannot detect unauthorized access | Enable CloudTrail + EventBridge alerting |
| Sharing secrets via Slack/email | Transmitted in plaintext, logged | Share via SSM/SM, give access to the parameter |
| No rotation schedule | Credentials remain valid indefinitely | Rotate critical secrets every 90 days minimum |

<!--
┌──────────────────────────────────────────────────────────────┐
│  HEAPTRACE DEVELOPER SKILLS                                  │
│  Created by Heaptrace Technology Private Limited             │
│                                                              │
│  MIT License — Free and Open Source                          │
│                                                              │
│  You are free to use, copy, modify, merge, publish,         │
│  distribute, sublicense, and/or sell copies of this skill.   │
│  No restrictions. No attribution required.                   │
│                                                              │
│  heaptrace.com | github.com/heaptracetechnology              │
└──────────────────────────────────────────────────────────────┘
-->

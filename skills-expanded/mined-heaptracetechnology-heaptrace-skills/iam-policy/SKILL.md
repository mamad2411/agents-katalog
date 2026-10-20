---
name: Write IAM Policies
description: Write least-privilege IAM policies for AWS services, covering roles, policies, trust relationships, cross-account access, service-linked roles, policy evaluation logic, and condition keys for production-grade access control.
---

# Write IAM Policies

## Your Expertise

You are a **Senior Cloud Security Engineer** with 15+ years designing IAM policies and access control systems on AWS. You hold AWS Security Specialty certification and have implemented least-privilege access for organizations with 500+ AWS accounts. You are an expert in:

- IAM policy language — Effect, Action, Resource, Condition, Principal, policy evaluation logic
- Least-privilege design — starting with zero access and adding only what's needed
- Role-based access — service roles, cross-account roles, federation, SSO integration
- Policy boundaries — permission boundaries, SCPs, session policies
- Security anti-patterns — wildcard resources, overly broad actions, unused permissions
- IAM Access Analyzer — identifying unintended access and policy validation

You write IAM policies that are as restrictive as possible and as permissive as necessary. Every policy you create can be explained in plain English and justified with a specific use case.

---

## Project Configuration

> Customize this skill for your project. Fill in what applies, delete what doesn't.

### AWS Account Structure
<!-- Example: Single account 123456789012 for prod+staging, no AWS Organizations yet -->

### Existing Roles
<!-- Example: ecs-execution-role, ecs-task-role, github-actions-deploy, rds-monitoring-role -->

### Service Accounts
<!-- Example: GitHub Actions via OIDC (no access keys), no other service accounts -->

### SSO / Federation
<!-- Example: No SSO — IAM users with MFA for console access, OIDC for CI/CD -->

### Compliance
<!-- Example: SOC 2 — requires CloudTrail enabled, no wildcard resource policies, quarterly access reviews -->

---

## Common Rules

```
┌──────────────────────────────────────────────────────────────┐
│        MANDATORY RULES FOR EVERY IAM POLICY TASK             │
│                                                              │
│  1. LEAST PRIVILEGE IS THE ONLY STARTING POINT               │
│     → Start with zero permissions and add only the specific  │
│       actions the workload needs to function                 │
│     → Enumerate every API action explicitly — never use      │
│       service-level wildcards like "s3:*" or "ecs:*"         │
│     → Use IAM Access Advisor to find and remove unused       │
│       permissions after 30 days                              │
│     → Every statement must have a clear Sid that explains    │
│       its purpose in plain English                           │
│                                                              │
│  2. NEVER USE WILDCARDS IN PRODUCTION                        │
│     → Scope Resource to specific ARNs — never "*" unless     │
│       the API does not support resource-level permissions    │
│     → When "*" is required (e.g., ecr:GetAuthorizationToken) │
│       add a comment explaining why                           │
│     → Use condition keys to further restrict broad actions   │
│       (aws:SourceAccount, aws:RequestedRegion, etc.)         │
│     → Reject any PR that adds Resource "*" without a         │
│       documented exception                                   │
│                                                              │
│  3. ROLES OVER USERS ALWAYS                                  │
│     → Use IAM roles with temporary credentials for all       │
│       service-to-service authentication                      │
│     → Use OIDC federation for CI/CD (GitHub Actions) —       │
│       never store long-lived access keys                     │
│     → Separate execution roles from task roles — the ECS     │
│       agent should never have application-level permissions  │
│     → Apply permission boundaries to all non-admin roles     │
│       to cap the maximum possible permissions                │
│                                                              │
│  4. EVERY POLICY HAS A JUSTIFICATION                         │
│     → Document the specific use case for each policy in      │
│       the description field or Terraform comments            │
│     → Include the requesting service or ticket number        │
│     → If you cannot explain why a permission is needed in    │
│       one sentence, the policy is too broad                  │
│     → Tag every role with Project, Environment, and Service  │
│                                                              │
│  5. AUDIT REGULARLY                                          │
│     → Enable CloudTrail in all regions for IAM event logging │
│     → Run IAM Access Analyzer to detect unintended external  │
│       access to roles and resources                          │
│     → Review IAM Access Advisor quarterly and revoke unused  │
│       permissions                                            │
│     → Set up alerts for high-risk IAM events: CreateUser,    │
│       AttachUserPolicy, PutRolePolicy with wildcards         │
│                                                              │
│  6. NO AI TOOL REFERENCES — ANYWHERE                         │
│     → No AI mentions in policy names, role descriptions,     │
│       or IAM documentation                                   │
│     → All output reads as if written by a cloud security     │
│       engineer                                               │
└──────────────────────────────────────────────────────────────┘
```

---

## 1. IAM Policy Evaluation Logic

```
┌─────────────────────────────────────────────────────────────────────┐
│                  How AWS Evaluates IAM Policies                      │
│                                                                      │
│  Request arrives                                                     │
│       │                                                              │
│       ▼                                                              │
│  ┌──────────────────┐                                               │
│  │ Explicit Deny?   │──── YES ──→ DENIED (always wins)              │
│  └────────┬─────────┘                                               │
│           │ NO                                                       │
│           ▼                                                          │
│  ┌──────────────────┐                                               │
│  │ SCP allows?      │──── NO ──→ DENIED (Organization boundary)     │
│  └────────┬─────────┘                                               │
│           │ YES                                                      │
│           ▼                                                          │
│  ┌──────────────────┐                                               │
│  │ Resource policy   │──── YES ──→ ALLOWED (e.g., S3 bucket policy) │
│  │ grants access?   │                                               │
│  └────────┬─────────┘                                               │
│           │ NO explicit allow                                        │
│           ▼                                                          │
│  ┌──────────────────┐                                               │
│  │ Permission       │──── YES ──→ DENIED (used for max permissions) │
│  │ boundary denies? │                                               │
│  └────────┬─────────┘                                               │
│           │ NO                                                       │
│           ▼                                                          │
│  ┌──────────────────┐                                               │
│  │ Identity policy   │──── YES ──→ ALLOWED                          │
│  │ allows?           │                                               │
│  └────────┬─────────┘                                               │
│           │ NO                                                       │
│           ▼                                                          │
│       DENIED (implicit deny — default)                               │
└─────────────────────────────────────────────────────────────────────┘
```

### Key Principles

- Default deny: Everything is denied unless explicitly allowed
- Explicit deny always wins: A single deny in any policy overrides all allows
- Resource policies can grant cross-account access independently
- Permission boundaries restrict the maximum permissions a role can have
- SCPs (Service Control Policies) restrict what an entire AWS account can do

---

## 2. Role Architecture for a Typical Application

```
┌─────────────────────────────────────────────────────────────────────┐
│                     IAM Role Architecture                            │
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │  ECS Execution Role                                          │    │
│  │  (used by ECS agent — NOT your application code)             │    │
│  │                                                              │    │
│  │  Trusted by: ecs-tasks.amazonaws.com                         │    │
│  │  Permissions:                                                │    │
│  │    ✅ Pull images from ECR                                   │    │
│  │    ✅ Write logs to CloudWatch                               │    │
│  │    ✅ Read secrets from SSM/SecretsManager                   │    │
│  │    ❌ No S3, SQS, SES, or application-level access          │    │
│  └─────────────────────────────────────────────────────────────┘    │
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │  ECS Task Role                                               │    │
│  │  (used by your application code at runtime)                  │    │
│  │                                                              │    │
│  │  Trusted by: ecs-tasks.amazonaws.com                         │    │
│  │  Permissions:                                                │    │
│  │    ✅ Read/write to specific S3 buckets                      │    │
│  │    ✅ Send emails via SES                                    │    │
│  │    ✅ Publish to specific SNS topics                         │    │
│  │    ✅ Send/receive from specific SQS queues                  │    │
│  │    ❌ No ECR, CloudWatch Logs, or infrastructure access     │    │
│  └─────────────────────────────────────────────────────────────┘    │
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │  CI/CD Role (GitHub Actions)                                 │    │
│  │  (used by deployment pipeline)                               │    │
│  │                                                              │    │
│  │  Trusted by: GitHub OIDC provider                            │    │
│  │  Condition: repo:org/repo:ref:refs/heads/main                │    │
│  │  Permissions:                                                │    │
│  │    ✅ Push to ECR                                            │    │
│  │    ✅ Update ECS services                                    │    │
│  │    ✅ Register task definitions                              │    │
│  │    ❌ No database, S3 data, or secret write access          │    │
│  └─────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 3. Policy Structure and Syntax

### Anatomy of an IAM Policy

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowS3BucketAccess",
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject",
        "s3:DeleteObject"
      ],
      "Resource": [
        "arn:aws:s3:::myapp-production-uploads/*"
      ],
      "Condition": {
        "StringEquals": {
          "s3:x-amz-server-side-encryption": "AES256"
        }
      }
    }
  ]
}
```

### Policy Element Reference

```
┌──────────────────────────────────────────────────────────────────┐
│  Element   │ Required │ Purpose                                   │
│  ────────────────────────────────────────────────────────────    │
│  Version   │ Yes      │ Always "2012-10-17" (latest)              │
│  Statement │ Yes      │ Array of permission rules                 │
│  Sid       │ No       │ Human-readable statement ID               │
│  Effect    │ Yes      │ "Allow" or "Deny"                         │
│  Action    │ Yes      │ AWS API actions (e.g., s3:GetObject)      │
│  Resource  │ Yes*     │ ARN(s) the action applies to              │
│  Condition │ No       │ When the statement applies                │
│  Principal │ Trust**  │ Who can assume this role                  │
│                                                                   │
│  * Some actions (like iam:CreateUser) don't support Resource     │
│  ** Principal is used in trust policies, not permission policies  │
└──────────────────────────────────────────────────────────────────┘
```

---

## 4. Common Policy Patterns

### ECS Execution Role

```hcl
resource "aws_iam_role" "ecs_execution" {
  name = "${local.project}-${local.environment}-ecs-execution"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Principal = { Service = "ecs-tasks.amazonaws.com" }
      Action = "sts:AssumeRole"
    }]
  })

  tags = {
    Name        = "${local.project}-${local.environment}-ecs-execution"
    Environment = local.environment
  }
}

resource "aws_iam_role_policy" "ecs_execution" {
  name = "execution-permissions"
  role = aws_iam_role.ecs_execution.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "PullFromECR"
        Effect = "Allow"
        Action = [
          "ecr:GetDownloadUrlForLayer",
          "ecr:BatchGetImage",
          "ecr:BatchCheckLayerAvailability",
        ]
        Resource = [
          "arn:aws:ecr:us-east-1:${data.aws_caller_identity.current.account_id}:repository/${local.project}-*"
        ]
      },
      {
        Sid      = "ECRAuth"
        Effect   = "Allow"
        Action   = ["ecr:GetAuthorizationToken"]
        Resource = "*"  # GetAuthorizationToken doesn't support resource-level permissions
      },
      {
        Sid    = "WriteLogs"
        Effect = "Allow"
        Action = [
          "logs:CreateLogStream",
          "logs:PutLogEvents",
        ]
        Resource = [
          "arn:aws:logs:us-east-1:${data.aws_caller_identity.current.account_id}:log-group:/ecs/${local.project}-${local.environment}-*:*"
        ]
      },
      {
        Sid    = "ReadSecrets"
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
    ]
  })
}
```

### ECS Task Role (Application Runtime)

```hcl
resource "aws_iam_role" "ecs_task" {
  name = "${local.project}-${local.environment}-ecs-task"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Principal = { Service = "ecs-tasks.amazonaws.com" }
      Action = "sts:AssumeRole"
      Condition = {
        StringEquals = {
          "aws:SourceAccount" = data.aws_caller_identity.current.account_id
        }
        ArnLike = {
          "aws:SourceArn" = "arn:aws:ecs:us-east-1:${data.aws_caller_identity.current.account_id}:*"
        }
      }
    }]
  })
}

resource "aws_iam_role_policy" "ecs_task_s3" {
  name = "s3-uploads"
  role = aws_iam_role.ecs_task.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "ReadWriteUploads"
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:DeleteObject",
        ]
        Resource = "arn:aws:s3:::${local.project}-${local.environment}-uploads/*"
      },
      {
        Sid    = "ListBucket"
        Effect = "Allow"
        Action = ["s3:ListBucket"]
        Resource = "arn:aws:s3:::${local.project}-${local.environment}-uploads"
        Condition = {
          StringLike = {
            "s3:prefix" = ["tenants/*"]  # Only list within tenant prefix
          }
        }
      },
      {
        Sid    = "GeneratePresignedUrls"
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:PutObject",
        ]
        Resource = "arn:aws:s3:::${local.project}-${local.environment}-uploads/*"
        Condition = {
          NumericLessThanEquals = {
            "s3:signatureAge" = "3600"  # Presigned URLs valid max 1 hour
          }
        }
      },
    ]
  })
}

resource "aws_iam_role_policy" "ecs_task_ses" {
  name = "ses-send-email"
  role = aws_iam_role.ecs_task.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Sid    = "SendEmail"
      Effect = "Allow"
      Action = [
        "ses:SendEmail",
        "ses:SendRawEmail",
      ]
      Resource = [
        "arn:aws:ses:us-east-1:${data.aws_caller_identity.current.account_id}:identity/lmsht.com",
        "arn:aws:ses:us-east-1:${data.aws_caller_identity.current.account_id}:configuration-set/${local.project}-${local.environment}",
      ]
      Condition = {
        StringEquals = {
          "ses:FromAddress" = [
            "noreply@lmsht.com",
            "support@lmsht.com",
          ]
        }
      }
    }]
  })
}

# ECS Exec support (for debugging)
resource "aws_iam_role_policy" "ecs_task_exec" {
  name = "ecs-exec"
  role = aws_iam_role.ecs_task.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Sid    = "ECSExec"
      Effect = "Allow"
      Action = [
        "ssmmessages:CreateControlChannel",
        "ssmmessages:CreateDataChannel",
        "ssmmessages:OpenControlChannel",
        "ssmmessages:OpenDataChannel",
      ]
      Resource = "*"
    }]
  })
}
```

### GitHub Actions OIDC Role

```hcl
# OIDC provider (create once per account)
resource "aws_iam_openid_connect_provider" "github" {
  url            = "https://token.actions.githubusercontent.com"
  client_id_list = ["sts.amazonaws.com"]

  thumbprint_list = [
    "6938fd4d98bab03faadb97b34396831e3780aea1",
    "1c58a3a8518e8759bf075b76b750d4f2df264fcd",
  ]
}

# CI/CD deployment role
resource "aws_iam_role" "github_actions" {
  name = "${local.project}-github-actions-deploy"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Principal = {
        Federated = aws_iam_openid_connect_provider.github.arn
      }
      Action = "sts:AssumeRoleWithWebIdentity"
      Condition = {
        StringEquals = {
          "token.actions.githubusercontent.com:aud" = "sts.amazonaws.com"
        }
        StringLike = {
          "token.actions.githubusercontent.com:sub" = "repo:myorg/myapp:ref:refs/heads/main"
        }
      }
    }]
  })
}

resource "aws_iam_role_policy" "github_actions_deploy" {
  name = "deploy-permissions"
  role = aws_iam_role.github_actions.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "ECRPush"
        Effect = "Allow"
        Action = [
          "ecr:GetDownloadUrlForLayer",
          "ecr:BatchGetImage",
          "ecr:BatchCheckLayerAvailability",
          "ecr:PutImage",
          "ecr:InitiateLayerUpload",
          "ecr:UploadLayerPart",
          "ecr:CompleteLayerUpload",
          "ecr:GetAuthorizationToken",
        ]
        Resource = "*"  # GetAuthorizationToken needs *
      },
      {
        Sid    = "ECSDeploy"
        Effect = "Allow"
        Action = [
          "ecs:DescribeServices",
          "ecs:UpdateService",
          "ecs:RegisterTaskDefinition",
          "ecs:DescribeTaskDefinition",
          "ecs:ListTasks",
          "ecs:DescribeTasks",
        ]
        Resource = "*"
        Condition = {
          StringEquals = {
            "ecs:cluster" = "arn:aws:ecs:us-east-1:${data.aws_caller_identity.current.account_id}:cluster/${local.project}-*"
          }
        }
      },
      {
        Sid    = "PassRole"
        Effect = "Allow"
        Action = "iam:PassRole"
        Resource = [
          aws_iam_role.ecs_execution.arn,
          aws_iam_role.ecs_task.arn,
        ]
      },
    ]
  })
}
```

---

## 5. Cross-Account Access

```
┌─────────────────────────────────────────────────────────────────┐
│                  Cross-Account Access Pattern                    │
│                                                                  │
│  Account A (Production: 111111111111)                            │
│  ┌───────────────────────────────────┐                          │
│  │  S3 Bucket: prod-data-exports     │                          │
│  │  Bucket Policy:                   │                          │
│  │    Allow s3:GetObject             │                          │
│  │    Principal: arn:aws:iam::       │                          │
│  │      222222222222:role/analytics  │                          │
│  └───────────────────────────────────┘                          │
│                     ▲                                            │
│                     │ AssumeRole                                 │
│                     │                                            │
│  Account B (Analytics: 222222222222)                             │
│  ┌───────────────────────────────────┐                          │
│  │  Role: analytics                  │                          │
│  │  Trust: Account A (111111111111)  │                          │
│  │  Policy: s3:GetObject on          │                          │
│  │    prod-data-exports bucket       │                          │
│  └───────────────────────────────────┘                          │
└─────────────────────────────────────────────────────────────────┘
```

### Cross-Account Role Terraform

```hcl
# In Account B — create role that trusts Account A
resource "aws_iam_role" "cross_account_analytics" {
  name = "cross-account-analytics"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Principal = {
        AWS = "arn:aws:iam::111111111111:root"
      }
      Action = "sts:AssumeRole"
      Condition = {
        StringEquals = {
          "sts:ExternalId" = "analytics-2026-secure-token"  # Prevents confused deputy
        }
      }
    }]
  })
}
```

---

## 6. Condition Keys Reference

```
┌──────────────────────────────────────────────────────────────────────┐
│                   Most Useful IAM Condition Keys                      │
│                                                                       │
│  Key                               │ Use Case                        │
│  ──────────────────────────────────────────────────────────────      │
│  aws:SourceIp                      │ Restrict to office IP range     │
│  aws:SourceVpc                     │ Only from specific VPC          │
│  aws:SourceVpce                    │ Only via VPC endpoint           │
│  aws:RequestedRegion               │ Restrict to us-east-1 only     │
│  aws:PrincipalTag/Department       │ ABAC — tag-based access        │
│  aws:ResourceTag/Environment       │ Only access prod/staging        │
│  s3:x-amz-server-side-encryption  │ Enforce encryption on upload   │
│  ec2:ResourceTag/Environment       │ Only manage prod EC2 instances │
│  ecs:cluster                       │ Only deploy to specific cluster │
│  kms:ViaService                    │ Key only usable via RDS/S3     │
│  aws:MultiFactorAuthPresent       │ Require MFA for sensitive ops  │
│  aws:PrincipalOrgID               │ Only from same AWS Org         │
│  sts:ExternalId                    │ Prevent confused deputy attack │
└──────────────────────────────────────────────────────────────────────┘
```

---

## 7. Permission Boundaries

```hcl
# Permission boundary — maximum permissions any role in this account can have
resource "aws_iam_policy" "permission_boundary" {
  name        = "${local.project}-permission-boundary"
  description = "Maximum permissions for all roles in this project"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "AllowedServices"
        Effect = "Allow"
        Action = [
          "s3:*",
          "sqs:*",
          "sns:*",
          "ses:*",
          "ecs:*",
          "ecr:*",
          "rds:*",
          "elasticache:*",
          "logs:*",
          "cloudwatch:*",
          "ssm:GetParameter*",
          "secretsmanager:GetSecretValue",
          "kms:Decrypt",
          "kms:GenerateDataKey",
        ]
        Resource = "*"
      },
      {
        Sid    = "DenyDangerousActions"
        Effect = "Deny"
        Action = [
          "iam:CreateUser",
          "iam:CreateAccessKey",
          "iam:AttachUserPolicy",
          "organizations:*",
          "account:*",
          "sts:AssumeRole",  # Only allow specific cross-account
        ]
        Resource = "*"
      },
      {
        Sid      = "RestrictToRegion"
        Effect   = "Deny"
        Action   = "*"
        Resource = "*"
        Condition = {
          StringNotEquals = {
            "aws:RequestedRegion" = ["us-east-1", "us-east-2"]
          }
        }
      },
    ]
  })
}

# Apply boundary to roles
resource "aws_iam_role" "example" {
  name                 = "example-role"
  permissions_boundary = aws_iam_policy.permission_boundary.arn
  # ... rest of role config
}
```

---

## 8. Cost Implications

| Resource | Cost | Notes |
|----------|------|-------|
| IAM roles | Free | No charge for roles/policies |
| IAM users | Free | No charge (but avoid users, use roles) |
| STS AssumeRole | Free | No charge for temporary credentials |
| IAM Access Analyzer | ~$2/analyzer/month | Per analyzer in each region |
| Access Advisor | Free | Shows last-used dates for permissions |
| CloudTrail (for auditing) | Free (1 trail) | Additional trails/insights cost extra |

---

## 9. Security Considerations

- Never use IAM access keys for applications — use IAM roles with temporary credentials
- Always use `ExternalId` in cross-account trust policies to prevent confused deputy attacks
- Enable MFA for human users accessing the console
- Use permission boundaries for delegated admin roles
- Review IAM Access Advisor quarterly — remove unused permissions
- Never attach `AdministratorAccess` managed policy to service roles
- Use `aws:SourceAccount` and `aws:SourceArn` conditions on trust policies
- Rotate any remaining access keys every 90 days
- Enable CloudTrail in all regions for IAM audit logging

---

## 10. Common Mistakes / Anti-Patterns

| Mistake | Why It's Bad | Fix |
|---------|-------------|-----|
| `Resource: "*"` on all statements | Grants access to every resource | Scope to specific ARNs |
| `Action: "*"` (full admin) | Over-privileged, blast radius is huge | List specific actions needed |
| Using IAM users with access keys | Keys can leak, no auto-rotation | Use IAM roles with OIDC/STS |
| No conditions on trust policies | Any entity in trusted account can assume | Add `sts:ExternalId`, source conditions |
| Same role for execution and task | Leaks infrastructure permissions to app | Separate execution role from task role |
| Inline policies everywhere | Hard to audit, can't reuse | Use managed policies, attach to roles |
| Missing `iam:PassRole` restriction | Pipeline could pass any role to ECS | Restrict to specific role ARNs |
| No permission boundary | Delegated admins can escalate | Apply boundaries to all non-admin roles |
| Wildcard in Principal | Anyone can assume the role | Specify exact account/service/OIDC |
| Not using OIDC for GitHub Actions | Requires storing AWS access keys | Use GitHub OIDC provider |

---

## 11. IAM Policy Debugging

```bash
# Simulate policy evaluation
aws iam simulate-principal-policy \
  --policy-source-arn arn:aws:iam::123456789012:role/myapp-ecs-task \
  --action-names s3:GetObject s3:PutObject \
  --resource-arns arn:aws:s3:::myapp-production-uploads/tenants/123/file.pdf \
  --output table

# Check what permissions a role actually has
aws iam list-attached-role-policies --role-name myapp-ecs-task
aws iam list-role-policies --role-name myapp-ecs-task

# View effective policy
aws iam get-role-policy --role-name myapp-ecs-task --policy-name s3-uploads

# Check last accessed services (find unused permissions)
aws iam generate-service-last-accessed-details \
  --arn arn:aws:iam::123456789012:role/myapp-ecs-task

# View the generated report
aws iam get-service-last-accessed-details --job-id <job-id> --output table

# Check who can assume a role (trust policy)
aws iam get-role --role-name myapp-ecs-task \
  --query "Role.AssumeRolePolicyDocument" --output json

# Decode authorization failure messages
aws sts decode-authorization-message --encoded-message <encoded-message> | jq '.DecodedMessage | fromjson'
```

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

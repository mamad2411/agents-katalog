---
name: terraform-patterns
description: "Terraform patterns: a complete RDS PostgreSQL module, Terraform CI/CD with GitHub Actions, detecting and fixing state drift, and Terragrunt run-all. Use when authoring modules or running Terraform in CI."
---

# Terraform Patterns

Module structure, remote state, for_each patterns, Terragrunt DRY configs, and CI/CD for infrastructure.

## Complete Module Example: RDS PostgreSQL

```hcl
# modules/rds-postgres/main.tf
locals {
  identifier = "${var.name}-${var.environment}"
}

resource "aws_db_subnet_group" "this" {
  name       = local.identifier
  subnet_ids = var.subnet_ids

  tags = merge(var.tags, {Name = local.identifier})
}

resource "aws_db_parameter_group" "this" {
  family = "postgres15"
  name   = local.identifier

  parameter {
    name  = "log_min_duration_statement"
    value = "1000"   # Log queries >1s
  }
  parameter {
    name  = "log_connections"
    value = "1"
  }
  parameter {
    name  = "shared_preload_libraries"
    value = "pg_stat_statements"
  }
}

resource "random_password" "db" {
  length           = 32
  special          = true
  override_special = "!#$%&*()-_=+[]{}<>:?"
}

resource "aws_secretsmanager_secret" "db_password" {
  name                    = "${local.identifier}/db-password"
  recovery_window_in_days = var.environment == "production" ? 30 : 7
  kms_key_id              = var.kms_key_id
}

resource "aws_secretsmanager_secret_version" "db_password" {
  secret_id = aws_secretsmanager_secret.db_password.id
  secret_string = jsonencode({
    username = "postgres"
    password = random_password.db.result
    host     = aws_db_instance.this.address
    port     = 5432
    dbname   = var.database_name
  })
}

resource "aws_db_instance" "this" {
  identifier = local.identifier

  engine         = "postgres"
  engine_version = "15.4"
  instance_class = var.instance_class

  allocated_storage     = var.allocated_storage
  max_allocated_storage = var.allocated_storage * 4  # Auto-scaling up to 4x
  storage_type          = "gp3"
  storage_encrypted     = true
  kms_key_id            = var.kms_key_id

  db_name  = var.database_name
  username = "postgres"
  password = random_password.db.result

  db_subnet_group_name   = aws_db_subnet_group.this.name
  vpc_security_group_ids = [aws_security_group.db.id]
  parameter_group_name   = aws_db_parameter_group.this.name

  multi_az               = var.environment == "production"
  publicly_accessible    = false
  deletion_protection    = var.environment == "production"
  skip_final_snapshot    = var.environment != "production"
  final_snapshot_identifier = var.environment == "production" ? "${local.identifier}-final" : null

  backup_retention_period = var.environment == "production" ? 7 : 1
  backup_window          = "03:00-04:00"
  maintenance_window     = "Sun:04:00-Sun:05:00"

  performance_insights_enabled          = var.environment == "production"
  performance_insights_retention_period = 7

  enabled_cloudwatch_logs_exports = ["postgresql", "upgrade"]

  tags = merge(var.tags, {Name = local.identifier})

  lifecycle {
    prevent_destroy = true
    ignore_changes = [password]  # Managed by Secrets Manager rotation
  }
}
```

## Terraform CI/CD with GitHub Actions

```yaml
name: Terraform

on:
  push:
    branches: [main]
    paths: ['environments/production/**']
  pull_request:
    branches: [main]
    paths: ['environments/production/**']

env:
  TF_WORKING_DIR: environments/production
  TF_VERSION: "1.7.0"

jobs:
  validate:
    runs-on: ubuntu-latest
    permissions:
      id-token: write
      contents: read
      pull-requests: write

    steps:
      - uses: actions/checkout@v4

      - uses: hashicorp/setup-terraform@v3
        with:
          terraform_version: ${{ env.TF_VERSION }}

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::ACCOUNT:role/TerraformPlanRole
          aws-region: us-east-1

      - name: Terraform Init
        run: terraform init
        working-directory: ${{ env.TF_WORKING_DIR }}

      - name: Terraform Validate
        run: terraform validate
        working-directory: ${{ env.TF_WORKING_DIR }}

      - name: Checkov Security Scan
        uses: bridgecrewio/checkov-action@master
        with:
          directory: ${{ env.TF_WORKING_DIR }}
          framework: terraform
          skip_check: CKV_AWS_21  # Example: skip specific checks

      - name: Terraform Plan
        id: plan
        run: |
          terraform plan -no-color -out=tfplan 2>&1 | tee plan-output.txt
          echo "exitcode=${PIPESTATUS[0]}" >> $GITHUB_OUTPUT
        working-directory: ${{ env.TF_WORKING_DIR }}

      - name: Comment PR with plan
        if: github.event_name == 'pull_request'
        uses: actions/github-script@v7
        with:
          script: |
            const fs = require('fs');
            const plan = fs.readFileSync('${{ env.TF_WORKING_DIR }}/plan-output.txt', 'utf8');
            const output = `#### Terraform Plan 📋
            \`\`\`
            ${plan.substring(0, 60000)}
            \`\`\``;
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: output
            });

  apply:
    needs: validate
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    environment: production   # Requires manual approval in GitHub

    steps:
      - uses: actions/checkout@v4
      - uses: hashicorp/setup-terraform@v3
        with: {terraform_version: "${{ env.TF_VERSION }}"}

      - name: Configure AWS credentials (Apply role has more permissions)
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::ACCOUNT:role/TerraformApplyRole
          aws-region: us-east-1

      - run: terraform init
        working-directory: ${{ env.TF_WORKING_DIR }}

      - run: terraform apply -auto-approve
        working-directory: ${{ env.TF_WORKING_DIR }}
```

## Detecting and Fixing State Drift

```bash
# Check for drift (what changed outside Terraform)
terraform plan -refresh-only
# If this shows changes, resources were modified outside Terraform

# Accept drift (update state to match reality)
terraform apply -refresh-only

# Import a resource created outside Terraform
terraform import aws_s3_bucket.logs my-existing-bucket

# Terraform 1.5+: import block (preferred, tracked in code)
import {
  to = aws_s3_bucket.logs
  id = "my-existing-bucket"
}

# Move a resource in state (refactoring, no destroy/create)
moved {
  from = aws_instance.example
  to   = module.ec2.aws_instance.example
}

# Remove from state (stop managing, don't destroy)
terraform state rm aws_s3_bucket.old_bucket

# View current state
terraform state list
terraform state show aws_db_instance.main
```

## Terragrunt Run-All

```bash
# Deploy all modules in dependency order
terragrunt run-all apply --terragrunt-working-dir environments/production

# Plan all modules
terragrunt run-all plan --terragrunt-working-dir environments/production

# Apply only specific module and its dependencies
terragrunt apply --terragrunt-working-dir environments/production/rds

# Destroy in reverse dependency order
terragrunt run-all destroy --terragrunt-working-dir environments/staging

# Skip confirmation (CI/CD)
terragrunt run-all apply --auto-approve \
  --terragrunt-non-interactive \
  --terragrunt-working-dir environments/production
```

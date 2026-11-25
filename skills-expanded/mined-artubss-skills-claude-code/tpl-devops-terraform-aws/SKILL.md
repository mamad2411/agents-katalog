---
name: tpl-devops-terraform-aws
description: Template do pack (devops/02-terraform-aws.md). Orienta o agente em infra, deploy, CI/CD e operacao alinhado a esse contexto.
metadata:
  version: 1.0.0
  source_template: devops/02-terraform-aws.md
  generated_by: install_pack_templates_as_claude_skills
---

# PROJECT: Terraform + AWS Infrastructure (EC2/ECS/RDS/S3/CloudFront + ALB)

Skill gerado a partir do pack `templates-claude-code`. Arquivo de origem: `devops/02-terraform-aws.md`. Use como baseline e adapte ao projeto antes de mudancas grandes.

## Conteudo do template

## STACK
- **IaC:** Terraform 1.7+ (HCL)
- **Provider:** hashicorp/aws ~> 5.0
- **Modules:** terraform-aws-modules (vpc, ecs, alb, rds, s3, cloudfront)
- **State:** S3 backend + DynamoDB locking
- **Workspaces:** dev / staging / prod
- **CI:** GitHub Actions (terraform plan on PR, apply on merge)

---

## REPOSITORY STRUCTURE
```
infra/
├── main.tf                  # Root module entry
├── variables.tf
├── outputs.tf
├── versions.tf              # Required providers + terraform version
├── backend.tf               # S3 state + DynamoDB lock
├── locals.tf                # Derived values + naming
├── terraform.tfvars         # Non-sensitive defaults (committed)
├── terraform.tfvars.json    # CI-injected sensitive values (gitignored)
└── modules/
    ├── networking/          # VPC, subnets, NAT, SG
    │   ├── main.tf
    │   ├── variables.tf
    │   └── outputs.tf
    ├── ecs-service/         # ECS cluster + service + task def
    ├── rds-postgres/        # RDS instance + parameter group
    ├── cdn/                 # CloudFront + S3 origin
    └── alb/                 # ALB + target groups + listeners
```

---

## ARCHITECTURE RULES
1. **State is sacred** — S3 backend with DynamoDB lock; never run `apply` without remote state.
2. **Workspaces map to AWS accounts** — dev/staging in one account, prod in a separate account.
3. **Never hardcode IDs** — use data sources (`data.aws_vpc`, `data.aws_caller_identity`) to fetch IDs.
4. **`-target` is forbidden in CI** — always apply full plan; use `lifecycle { ignore_changes }` if needed.
5. **Tag everything** — every resource gets `project`, `env`, `managed-by = terraform`, `owner` tags.
6. **Module versions are pinned** — `source = "terraform-aws-modules/vpc/aws" version = "~> 5.5"`.
7. **Sensitive outputs use `sensitive = true`** — never log RDS password, never output in plaintext.
8. **Plan is code review** — `terraform plan` output is posted to the PR as a comment.

---

## VERSIONS + BACKEND

```hcl
# versions.tf
terraform {
  required_version = ">= 1.7.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.40"
    }
  }
}

# backend.tf
terraform {
  backend "s3" {
    bucket         = "myapp-terraform-state-prod"
    key            = "infra/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-state-lock"
    # Workspace key prefix: env:/dev/infra/terraform.tfstate
  }
}
```

---

## STATE BOOTSTRAP (RUN ONCE)

```bash
# Create state bucket (must exist before terraform init)
aws s3api create-bucket \
  --bucket myapp-terraform-state-prod \
  --region us-east-1

aws s3api put-bucket-versioning \
  --bucket myapp-terraform-state-prod \
  --versioning-configuration Status=Enabled

aws s3api put-bucket-encryption \
  --bucket myapp-terraform-state-prod \
  --server-side-encryption-configuration '{"Rules":[{"ApplyServerSideEncryptionByDefault":{"SSEAlgorithm":"AES256"}}]}'

# Create DynamoDB lock table
aws dynamodb create-table \
  --table-name terraform-state-lock \
  --attribute-definitions AttributeName=LockID,AttributeType=S \
  --key-schema AttributeName=LockID,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST \
  --region us-east-1
```

---

## WORKSPACE STRATEGY

```bash
# Create workspaces
terraform workspace new dev
terraform workspace new staging
terraform workspace new prod

# Switch and plan
terraform workspace select staging
terraform plan -var-file=envs/staging.tfvars -out=staging.plan
terraform apply staging.plan
```

---

## NAMING CONVENTIONS + LOCALS

```hcl
# locals.tf
locals {
  env     = terraform.workspace          # dev | staging | prod
  project = var.project_name             # myapp

  # Resource name prefix: myapp-prod
  prefix  = "${local.project}-${local.env}"

  # Standard tags applied to all resources via merge(local.common_tags, { ... })
  common_tags = {
    Project    = local.project
    Env        = local.env
    ManagedBy  = "terraform"
    Owner      = var.team_email
    CostCenter = var.cost_center
  }
}
```

---

## VPC MODULE EXAMPLE

```hcl
# modules/networking/main.tf
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 5.5"

  name = "${var.prefix}-vpc"
  cidr = var.vpc_cidr   # "10.0.0.0/16"

  azs              = slice(data.aws_availability_zones.available.names, 0, 3)
  private_subnets  = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
  public_subnets   = ["10.0.101.0/24", "10.0.102.0/24", "10.0.103.0/24"]
  database_subnets = ["10.0.201.0/24", "10.0.202.0/24", "10.0.203.0/24"]

  enable_nat_gateway     = true
  single_nat_gateway     = local.env != "prod"   # HA NAT only in prod
  enable_dns_hostnames   = true
  enable_dns_support     = true

  # Flow logs to CloudWatch
  enable_flow_log                      = true
  create_flow_log_cloudwatch_log_group = true
  create_flow_log_cloudwatch_iam_role  = true

  tags = var.tags
}
```

---

## ECS SERVICE MODULE EXAMPLE

```hcl
# modules/ecs-service/main.tf
resource "aws_ecs_cluster" "main" {
  name = "${var.prefix}-cluster"

  setting {
    name  = "containerInsights"
    value = "enabled"
  }

  tags = var.tags
}

resource "aws_ecs_task_definition" "app" {
  family                   = "${var.prefix}-app"
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = var.task_cpu     # "256"
  memory                   = var.task_memory  # "512"
  execution_role_arn       = aws_iam_role.ecs_execution.arn
  task_role_arn            = aws_iam_role.ecs_task.arn

  container_definitions = jsonencode([{
    name      = "app"
    image     = var.container_image
    essential = true
    portMappings = [{ containerPort = var.container_port, protocol = "tcp" }]
    environment  = var.environment_vars
    secrets      = var.secret_vars   # [{name="DB_PASSWORD", valueFrom="arn:aws:secretsmanager:..."}]
    logConfiguration = {
      logDriver = "awslogs"
      options = {
        awslogs-group         = "/ecs/${var.prefix}-app"
        awslogs-region        = var.aws_region
        awslogs-stream-prefix = "ecs"
      }
    }
  }])
}

resource "aws_ecs_service" "app" {
  name            = "${var.prefix}-service"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.app.arn
  desired_count   = var.desired_count
  launch_type     = "FARGATE"

  network_configuration {
    subnets          = var.private_subnet_ids
    security_groups  = [aws_security_group.ecs_tasks.id]
    assign_public_ip = false
  }

  load_balancer {
    target_group_arn = var.alb_target_group_arn
    container_name   = "app"
    container_port   = var.container_port
  }

  deployment_circuit_breaker {
    enable   = true
    rollback = true
  }

  lifecycle {
    ignore_changes = [desired_count]   # Controlled by autoscaling
  }
}
```

---

## RDS MODULE EXAMPLE

```hcl
module "rds" {
  source  = "terraform-aws-modules/rds/aws"
  version = "~> 6.5"

  identifier = "${local.prefix}-postgres"

  engine               = "postgres"
  engine_version       = "16.2"
  instance_class       = local.env == "prod" ? "db.t4g.medium" : "db.t4g.micro"
  allocated_storage    = local.env == "prod" ? 100 : 20
  max_allocated_storage = 200   # Autoscaling

  db_name  = var.db_name
  username = var.db_username
  port     = 5432

  # Password managed by AWS Secrets Manager
  manage_master_user_password = true

  vpc_security_group_ids = [module.networking.db_security_group_id]
  db_subnet_group_name   = module.networking.database_subnet_group_name

  multi_az            = local.env == "prod"
  skip_final_snapshot = local.env != "prod"
  deletion_protection = local.env == "prod"

  backup_retention_period = local.env == "prod" ? 30 : 7
  backup_window           = "03:00-04:00"
  maintenance_window      = "Mon:04:00-Mon:05:00"

  tags = local.common_tags
}
```

---

## GITHUB ACTIONS TERRAFORM CI

```yaml
# .github/workflows/terraform.yml
name: Terraform
on:
  pull_request:
    paths: ['infra/**']

jobs:
  plan:
    runs-on: ubuntu-24.04
    defaults:
      run:
        working-directory: infra
    steps:
      - uses: actions/checkout@v4

      - uses: hashicorp/setup-terraform@v3
        with:
          terraform_version: "1.7.5"

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: ${{ secrets.TF_ROLE_ARN }}
          aws-region: us-east-1

      - run: terraform init
      - run: terraform workspace select ${{ github.base_ref == 'main' && 'prod' || 'staging' }}
      - run: terraform validate
      - run: terraform fmt -check -recursive

      - name: Plan
        id: plan
        run: terraform plan -no-color -out=plan.tfplan

      - name: Post plan to PR
        uses: actions/github-script@v7
        with:
          script: |
            const output = `${{ steps.plan.outputs.stdout }}`
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: `\`\`\`\n${output}\n\`\`\``
            })
```

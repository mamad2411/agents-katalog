---
name: terraform-builder
description: "Build infrastructure as code with Terraform. Covers module design, state management, AWS/GCP/Azure resources, and production-grade practices."
category: devops
tags: [terraform, iac, aws, gcp, infrastructure, cloud]
complexity: expert
risk: low
compatibility: [claude-code, antigravity, gemini-cli, cursor, copilot, codex-cli, autohand, kiro]
source: antigravity-official
version: "1.0.0"
date_added: "2026-07-10"
last_updated: "2026-07-10"
---

# Terraform IaC Builder

## Purpose
Provision and manage cloud infrastructure with Terraform using modular, reusable, and safe IaC patterns.

## Terraform Best Practices

### Module Structure
```
infrastructure/
├── modules/
│   ├── vpc/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   ├── rds/
│   └── ecs/
├── environments/
│   ├── prod/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── terraform.tfvars
│   └── staging/
└── shared/
    └── backend.tf
```

### AWS Example: ECS + RDS
```hcl
# modules/ecs-service/main.tf
resource "aws_ecs_service" "this" {
  name            = var.name
  cluster         = var.cluster_id
  task_definition = aws_ecs_task_definition.this.arn
  desired_count   = var.desired_count
  launch_type     = "FARGATE"

  network_configuration {
    subnets          = var.private_subnet_ids
    security_groups  = [aws_security_group.service.id]
    assign_public_ip = false
  }

  load_balancer {
    target_group_arn = var.target_group_arn
    container_name   = var.name
    container_port   = var.container_port
  }

  deployment_circuit_breaker {
    enable   = true
    rollback = true
  }

  lifecycle {
    ignore_changes = [desired_count]  # Managed by autoscaling
  }
}

# Remote state backend
terraform {
  backend "s3" {
    bucket         = "my-terraform-state"
    key            = "prod/infrastructure.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-state-lock"
  }
}
```

### Variables and Outputs
```hcl
variable "environment" {
  type        = string
  description = "Deployment environment (prod, staging, dev)"
  validation {
    condition     = contains(["prod", "staging", "dev"], var.environment)
    error_message = "Environment must be prod, staging, or dev."
  }
}

output "database_endpoint" {
  value       = aws_rds_instance.main.endpoint
  sensitive   = true
  description = "RDS instance endpoint"
}
```

## Outputs
1. Module structure for your infrastructure
2. Environment-specific configurations
3. Remote state configuration
4. CI/CD integration for Terraform
5. State management strategy
6. Cost estimation commands

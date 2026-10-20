---
name: Deploy to ECS
description: Deploy containerized applications to AWS ECS with Fargate or EC2 launch types, covering task definitions, services, ALB integration, auto-scaling policies, rolling updates, blue/green deployments, and production-grade service configuration.
---

# Deploy to ECS

## Your Expertise

You are a **Senior Container & Deployment Engineer** with 15+ years deploying containerized applications on AWS ECS. You hold AWS Solutions Architect Professional and DevOps Engineer Professional certifications. You've deployed and managed 200+ production ECS services across multiple regions. You are an expert in:

- ECS Fargate and EC2 launch types — task definitions, service configuration, capacity providers
- ALB/NLB integration — target groups, health checks, path-based routing, sticky sessions
- Blue/green and rolling deployments — CodeDeploy integration, canary releases, rollback triggers
- ECR image management — vulnerability scanning, lifecycle policies, cross-account access
- Auto-scaling — target tracking, step scaling, scheduled scaling, capacity provider strategies
- Container observability — CloudWatch Container Insights, log drivers, X-Ray tracing

You deploy containers that are production-ready from day one — secure, observable, scalable, and recoverable. Every deployment you configure has health checks, rollback triggers, and zero-downtime guarantees.

---

## Project Configuration

> Customize this skill for your project. Fill in what applies, delete what doesn't.

### AWS Account & Region
<!-- Example: Account ID 123456789012, primary region us-east-1 -->

### ECS Cluster Config
<!-- Example: Cluster "myapp-production" using Fargate, capacity provider FARGATE + FARGATE_SPOT -->

### Services & ECR Repos
<!-- Example: backend (ECR: myapp-backend, port 3001), frontend (ECR: myapp-frontend, port 3000) -->

### Load Balancer
<!-- Example: ALB arn:aws:elasticloadbalancing:..., HTTPS :443 with ACM cert for *.lmsht.com -->

### Deploy Strategy
<!-- Example: Rolling update with circuit breaker + auto-rollback, min 100% healthy, max 200% -->

### Secrets
<!-- Example: SSM /myapp/production/* for DATABASE_URL, JWT_SECRET; SecretsManager for Stripe keys -->

---

## Common Rules

```
┌──────────────────────────────────────────────────────────────┐
│       MANDATORY RULES FOR EVERY ECS DEPLOYMENT TASK          │
│                                                              │
│  1. READ EXISTING INFRASTRUCTURE FIRST                       │
│     → Inspect the current cluster, task definitions, and     │
│       service config before making any changes               │
│     → Check running task count, scaling policies, and ALB    │
│       target group health                                    │
│     → Review recent deployment history and any active alarms │
│     → Never modify a service you haven't fully read first    │
│                                                              │
│  2. ZERO DOWNTIME NO EXCEPTIONS                              │
│     → Always use rolling updates with minimum 100% healthy   │
│     → Enable deployment circuit breaker with auto-rollback   │
│     → Set health check grace period long enough for app      │
│       startup (120s minimum for Node.js apps)                │
│     → Configure deregistration delay on target groups to     │
│       drain in-flight requests before killing tasks          │
│                                                              │
│  3. SECURITY IS THE DEFAULT                                  │
│     → Place all tasks in private subnets with no public IP   │
│     → Use separate execution and task IAM roles — never      │
│       combine them into a single role                        │
│     → Pull secrets from SSM/SecretsManager at startup —      │
│       never bake credentials into images or env files        │
│     → Enable container init process to handle signals and    │
│       prevent zombie processes                               │
│                                                              │
│  4. EVERY RESOURCE MUST BE OBSERVABLE                        │
│     → Send all container logs to CloudWatch with retention   │
│       policies (7d staging, 30d production)                  │
│     → Enable Container Insights for CPU/memory/network       │
│       metrics per task                                       │
│     → Set up alarms for running task count, CPU, memory,     │
│       and 5xx error rate                                     │
│     → Tag every resource for cost allocation and tracing     │
│                                                              │
│  5. COST-AWARE DECISIONS                                     │
│     → Right-size tasks based on actual CloudWatch metrics,   │
│       not guesswork — start small and scale up               │
│     → Use Fargate Spot for non-critical workloads and batch  │
│       jobs to save up to 70%                                 │
│     → Set ECR lifecycle policies to clean untagged images    │
│       and limit tagged image retention                       │
│     → Review auto-scaling scale-in cooldown to avoid         │
│       thrashing that wastes compute                          │
│                                                              │
│  6. NO AI TOOL REFERENCES — ANYWHERE                         │
│     → No AI mentions in task definitions, deploy scripts,    │
│       or infrastructure comments                             │
│     → All output reads as if written by a deployment         │
│       engineer                                               │
└──────────────────────────────────────────────────────────────┘
```

---

## 1. Launch Type Decision Tree

```
What is your workload profile?
│
├─ Predictable, steady traffic + cost-sensitive
│   └─ EC2 Launch Type
│       ├─ Use Reserved Instances or Savings Plans
│       ├─ You manage OS patching, AMI updates, instance scaling
│       └─ Best for: Large monoliths, GPU workloads, persistent storage
│
├─ Variable traffic, want zero server management
│   └─ Fargate Launch Type
│       ├─ Pay per vCPU-second and GB-second
│       ├─ No instances to manage, patch, or scale
│       └─ Best for: Microservices, batch jobs, new projects
│
├─ Burst workloads (CI runners, batch processing)
│   └─ Fargate Spot
│       ├─ Up to 70% cost savings vs regular Fargate
│       ├─ Tasks can be interrupted with 30-second warning
│       └─ Best for: Non-critical batch, data processing, CI builds
│
└─ Mixed workload
    └─ Capacity Providers (combine EC2 + Fargate)
        ├─ Base capacity on EC2 (reserved), burst to Fargate
        └─ Use capacity provider strategy with weights
```

---

## 2. ECS Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                        ECS Cluster Architecture                      │
│                                                                      │
│  Internet                                                            │
│     │                                                                │
│     ▼                                                                │
│  ┌──────────────────────────────────────────────────────────┐       │
│  │  Application Load Balancer (ALB)                          │       │
│  │  ┌─────────────────┐  ┌─────────────────┐               │       │
│  │  │ Listener :443   │  │ Listener :80    │               │       │
│  │  │ (HTTPS)         │  │ (redirect→443)  │               │       │
│  │  └────────┬────────┘  └─────────────────┘               │       │
│  │           │                                               │       │
│  │  ┌────────▼────────────────────────────────┐             │       │
│  │  │ Target Group (backend-tg, port 3001)    │             │       │
│  │  │ Health: /api/health, interval 30s       │             │       │
│  │  └────────┬────────────────────────────────┘             │       │
│  └───────────┼──────────────────────────────────────────────┘       │
│              │                                                       │
│  ┌───────────▼──────────────────────────────────────────────┐       │
│  │  ECS Cluster: production                                  │       │
│  │                                                           │       │
│  │  ┌─── Service: backend (desired: 3) ──────────────────┐  │       │
│  │  │                                                     │  │       │
│  │  │  ┌──────────┐  ┌──────────┐  ┌──────────┐         │  │       │
│  │  │  │ Task 1   │  │ Task 2   │  │ Task 3   │         │  │       │
│  │  │  │ AZ: 1a   │  │ AZ: 1b   │  │ AZ: 1c   │         │  │       │
│  │  │  │ 0.5 vCPU │  │ 0.5 vCPU │  │ 0.5 vCPU │         │  │       │
│  │  │  │ 1GB RAM  │  │ 1GB RAM  │  │ 1GB RAM  │         │  │       │
│  │  │  └──────────┘  └──────────┘  └──────────┘         │  │       │
│  │  │                                                     │  │       │
│  │  │  Auto-scaling: min=2, max=10, target CPU=70%       │  │       │
│  │  └─────────────────────────────────────────────────────┘  │       │
│  │                                                           │       │
│  │  ┌─── Service: frontend (desired: 2) ─────────────────┐  │       │
│  │  │  ┌──────────┐  ┌──────────┐                        │  │       │
│  │  │  │ Task 1   │  │ Task 2   │                        │  │       │
│  │  │  │ AZ: 1a   │  │ AZ: 1b   │                        │  │       │
│  │  │  └──────────┘  └──────────┘                        │  │       │
│  │  └─────────────────────────────────────────────────────┘  │       │
│  └───────────────────────────────────────────────────────────┘       │
│                                                                      │
│  ┌──────────────────────────────┐  ┌───────────────────────────┐    │
│  │ ECR: backend repo           │  │ ECR: frontend repo         │    │
│  │ Images: latest, v1.2.3      │  │ Images: latest, v1.2.3    │    │
│  └──────────────────────────────┘  └───────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 3. ECR Repository Setup

```hcl
resource "aws_ecr_repository" "backend" {
  name                 = "${local.project}-backend"
  image_tag_mutability = "MUTABLE"  # Allow :latest tag overwrite

  image_scanning_configuration {
    scan_on_push = true  # Scan for CVEs on every push
  }

  encryption_configuration {
    encryption_type = "AES256"
  }

  tags = {
    Name        = "${local.project}-backend"
    Environment = local.environment
  }
}

resource "aws_ecr_lifecycle_policy" "backend" {
  repository = aws_ecr_repository.backend.name

  policy = jsonencode({
    rules = [
      {
        rulePriority = 1
        description  = "Keep last 20 tagged images"
        selection = {
          tagStatus     = "tagged"
          tagPrefixList = ["v"]
          countType     = "imageCountMoreThan"
          countNumber   = 20
        }
        action = {
          type = "expire"
        }
      },
      {
        rulePriority = 2
        description  = "Remove untagged images older than 7 days"
        selection = {
          tagStatus   = "untagged"
          countType   = "sinceImagePushed"
          countUnit   = "days"
          countNumber = 7
        }
        action = {
          type = "expire"
        }
      }
    ]
  })
}
```

### Build and Push Commands

```bash
# Authenticate Docker to ECR
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin 123456789012.dkr.ecr.us-east-1.amazonaws.com

# Build with BuildKit for faster builds
DOCKER_BUILDKIT=1 docker build \
  --platform linux/amd64 \
  -t 123456789012.dkr.ecr.us-east-1.amazonaws.com/myapp-backend:latest \
  -t 123456789012.dkr.ecr.us-east-1.amazonaws.com/myapp-backend:v1.2.3 \
  -f src/infrastructure/docker/Dockerfile.backend \
  src/backend/

# Push both tags
docker push 123456789012.dkr.ecr.us-east-1.amazonaws.com/myapp-backend:latest
docker push 123456789012.dkr.ecr.us-east-1.amazonaws.com/myapp-backend:v1.2.3
```

---

## 4. Task Definition

```hcl
resource "aws_ecs_task_definition" "backend" {
  family                   = "${local.project}-${local.environment}-backend"
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = 512    # 0.5 vCPU
  memory                   = 1024   # 1 GB
  execution_role_arn       = aws_iam_role.ecs_execution.arn
  task_role_arn            = aws_iam_role.ecs_task.arn

  runtime_platform {
    operating_system_family = "LINUX"
    cpu_architecture        = "X86_64"
  }

  container_definitions = jsonencode([
    {
      name      = "backend"
      image     = "${aws_ecr_repository.backend.repository_url}:latest"
      essential = true

      portMappings = [
        {
          containerPort = 3001
          protocol      = "tcp"
        }
      ]

      environment = [
        { name = "NODE_ENV", value = "production" },
        { name = "PORT", value = "3001" },
        { name = "REDIS_URL", value = "redis://${aws_elasticache_replication_group.main.primary_endpoint_address}:6379" },
      ]

      secrets = [
        {
          name      = "DATABASE_URL"
          valueFrom = aws_ssm_parameter.database_url.arn
        },
        {
          name      = "JWT_SECRET"
          valueFrom = aws_ssm_parameter.jwt_secret.arn
        },
        {
          name      = "STRIPE_SECRET_KEY"
          valueFrom = "${aws_secretsmanager_secret.stripe.arn}:secret_key::"
        },
      ]

      healthCheck = {
        command     = ["CMD-SHELL", "curl -f http://localhost:3001/api/health || exit 1"]
        interval    = 30
        timeout     = 5
        retries     = 3
        startPeriod = 60
      }

      logConfiguration = {
        logDriver = "awslogs"
        options = {
          "awslogs-group"         = aws_cloudwatch_log_group.backend.name
          "awslogs-region"        = "us-east-1"
          "awslogs-stream-prefix" = "ecs"
        }
      }

      # Prevent container from escalating privileges
      linuxParameters = {
        initProcessEnabled = true  # Use tini as PID 1 for signal handling
      }
    }
  ])

  tags = {
    Name        = "${local.project}-${local.environment}-backend-task"
    Environment = local.environment
  }
}
```

### Task Size Decision Guide

```
┌───────────────────────────────────────────────────────────────┐
│                   Fargate Task Sizing Guide                    │
│                                                               │
│  Workload Type         │ vCPU │ Memory │ Monthly Cost (est.)  │
│  ─────────────────────────────────────────────────────────    │
│  API (light traffic)   │ 0.25 │ 512MB  │ ~$9/task             │
│  API (moderate)        │ 0.5  │ 1GB    │ ~$18/task            │
│  API (heavy/compute)   │ 1    │ 2GB    │ ~$36/task            │
│  Worker (background)   │ 0.5  │ 1GB    │ ~$18/task            │
│  Worker (heavy)        │ 2    │ 4GB    │ ~$73/task            │
│  Frontend (Next.js)    │ 0.5  │ 1GB    │ ~$18/task            │
│  Batch processing      │ 4    │ 8GB    │ ~$145/task           │
│                                                               │
│  Rule of thumb: Start small, scale up based on CloudWatch     │
│  metrics. Watch MemoryUtilization — OOM kills are silent.     │
└───────────────────────────────────────────────────────────────┘
```

---

## 5. ECS Service with ALB

```hcl
resource "aws_ecs_service" "backend" {
  name                               = "${local.project}-${local.environment}-backend"
  cluster                            = aws_ecs_cluster.main.id
  task_definition                    = aws_ecs_task_definition.backend.arn
  desired_count                      = local.environment == "production" ? 3 : 1
  launch_type                        = "FARGATE"
  platform_version                   = "LATEST"
  health_check_grace_period_seconds  = 120
  enable_execute_command             = true  # Allow `aws ecs execute-command` for debugging

  deployment_configuration {
    minimum_healthy_percent = 100  # Never go below desired count during deploy
    maximum_percent         = 200  # Allow 2x tasks during rolling update
  }

  deployment_circuit_breaker {
    enable   = true
    rollback = true  # Auto-rollback if new tasks fail health checks
  }

  network_configuration {
    subnets          = aws_subnet.private[*].id
    security_groups  = [aws_security_group.app.id]
    assign_public_ip = false  # Private subnets — use NAT for outbound
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.backend.arn
    container_name   = "backend"
    container_port   = 3001
  }

  # Spread tasks across AZs for high availability
  ordered_placement_strategy {
    type  = "spread"
    field = "attribute:ecs.availability-zone"
  }

  # Ignore desired_count changes from auto-scaling
  lifecycle {
    ignore_changes = [desired_count, task_definition]
  }

  depends_on = [aws_lb_listener.https]

  tags = {
    Name = "${local.project}-${local.environment}-backend-service"
  }
}
```

### ALB Target Group Configuration

```hcl
resource "aws_lb_target_group" "backend" {
  name        = "${local.project}-${local.environment}-backend-tg"
  port        = 3001
  protocol    = "HTTP"
  target_type = "ip"  # Required for Fargate awsvpc mode
  vpc_id      = aws_vpc.main.id

  health_check {
    path                = "/api/health"
    protocol            = "HTTP"
    port                = "traffic-port"
    healthy_threshold   = 2
    unhealthy_threshold = 5
    timeout             = 10
    interval            = 30
    matcher             = "200"
  }

  deregistration_delay = 30  # Drain connections for 30s before removing task

  stickiness {
    type    = "lb_cookie"
    enabled = false  # Stateless APIs don't need stickiness
  }

  tags = {
    Name = "${local.project}-${local.environment}-backend-tg"
  }
}
```

---

## 6. Auto-Scaling Policies

```hcl
resource "aws_appautoscaling_target" "backend" {
  max_capacity       = 10
  min_capacity       = 2
  resource_id        = "service/${aws_ecs_cluster.main.name}/${aws_ecs_service.backend.name}"
  scalable_dimension = "ecs:service:DesiredCount"
  service_namespace  = "ecs"
}

# Scale based on CPU utilization
resource "aws_appautoscaling_policy" "backend_cpu" {
  name               = "${local.project}-${local.environment}-backend-cpu-scaling"
  policy_type        = "TargetTrackingScaling"
  resource_id        = aws_appautoscaling_target.backend.resource_id
  scalable_dimension = aws_appautoscaling_target.backend.scalable_dimension
  service_namespace  = aws_appautoscaling_target.backend.service_namespace

  target_tracking_scaling_policy_configuration {
    target_value       = 70  # Scale when CPU exceeds 70%
    scale_in_cooldown  = 300 # Wait 5 min before scaling in
    scale_out_cooldown = 60  # Scale out quickly (1 min)

    predefined_metric_specification {
      predefined_metric_type = "ECSServiceAverageCPUUtilization"
    }
  }
}

# Scale based on memory utilization
resource "aws_appautoscaling_policy" "backend_memory" {
  name               = "${local.project}-${local.environment}-backend-memory-scaling"
  policy_type        = "TargetTrackingScaling"
  resource_id        = aws_appautoscaling_target.backend.resource_id
  scalable_dimension = aws_appautoscaling_target.backend.scalable_dimension
  service_namespace  = aws_appautoscaling_target.backend.service_namespace

  target_tracking_scaling_policy_configuration {
    target_value       = 80  # Scale when memory exceeds 80%
    scale_in_cooldown  = 300
    scale_out_cooldown = 60

    predefined_metric_specification {
      predefined_metric_type = "ECSServiceAverageMemoryUtilization"
    }
  }
}

# Scale based on ALB request count per target
resource "aws_appautoscaling_policy" "backend_requests" {
  name               = "${local.project}-${local.environment}-backend-request-scaling"
  policy_type        = "TargetTrackingScaling"
  resource_id        = aws_appautoscaling_target.backend.resource_id
  scalable_dimension = aws_appautoscaling_target.backend.scalable_dimension
  service_namespace  = aws_appautoscaling_target.backend.service_namespace

  target_tracking_scaling_policy_configuration {
    target_value       = 1000  # Scale at 1000 requests per task
    scale_in_cooldown  = 300
    scale_out_cooldown = 60

    predefined_metric_specification {
      predefined_metric_type = "ALBRequestCountPerTarget"
      resource_label         = "${aws_lb.main.arn_suffix}/${aws_lb_target_group.backend.arn_suffix}"
    }
  }
}

# Scheduled scaling for known traffic patterns
resource "aws_appautoscaling_scheduled_action" "backend_morning_scaleup" {
  name               = "morning-scaleup"
  service_namespace  = aws_appautoscaling_target.backend.service_namespace
  resource_id        = aws_appautoscaling_target.backend.resource_id
  scalable_dimension = aws_appautoscaling_target.backend.scalable_dimension
  schedule           = "cron(0 8 ? * MON-FRI *)"  # 8 AM UTC weekdays

  scalable_target_action {
    min_capacity = 4  # Pre-warm for morning traffic
    max_capacity = 10
  }
}
```

---

## 7. Deployment Strategies

### Rolling Update (Default)

```
Time T0:  [Task v1] [Task v1] [Task v1]
                                          ← New task v2 starts
Time T1:  [Task v1] [Task v1] [Task v1] [Task v2]
                                          ← v2 passes health check
Time T2:  [Task v1] [Task v1] [Task v2]  ← v1 drains & stops
Time T3:  [Task v1] [Task v2] [Task v2]
Time T4:  [Task v2] [Task v2] [Task v2]  ← Complete
```

### Blue/Green with CodeDeploy

```
┌─────────────────────────────────────────────────────────┐
│              Blue/Green Deployment Flow                   │
│                                                          │
│  Step 1: Blue is live (100% traffic)                     │
│  ┌────────────┐     ┌────────────┐                      │
│  │ ALB :443   │────▶│ TG-Blue    │ → [Task v1 x3]      │
│  └────────────┘     └────────────┘                      │
│                                                          │
│  Step 2: Green deploys (0% traffic)                      │
│  ┌────────────┐     ┌────────────┐                      │
│  │ ALB :443   │────▶│ TG-Blue    │ → [Task v1 x3]      │
│  └────────────┘     ┌────────────┐                      │
│  (test :8443) ─────▶│ TG-Green   │ → [Task v2 x3]      │
│                     └────────────┘                      │
│                                                          │
│  Step 3: Traffic shift (linear 10% every 5 min)          │
│  ┌────────────┐     ┌────────────┐                      │
│  │ ALB :443   │──┬─▶│ TG-Blue    │ → [Task v1] (90%)   │
│  └────────────┘  └─▶│ TG-Green   │ → [Task v2] (10%)   │
│                     └────────────┘                      │
│                                                          │
│  Step 4: Complete (100% green, blue terminates)          │
│  ┌────────────┐     ┌────────────┐                      │
│  │ ALB :443   │────▶│ TG-Green   │ → [Task v2 x3]      │
│  └────────────┘     └────────────┘                      │
└─────────────────────────────────────────────────────────┘
```

### CodeDeploy Terraform Setup

```hcl
resource "aws_codedeploy_app" "backend" {
  compute_platform = "ECS"
  name             = "${local.project}-${local.environment}-backend"
}

resource "aws_codedeploy_deployment_group" "backend" {
  app_name               = aws_codedeploy_app.backend.name
  deployment_group_name  = "${local.project}-${local.environment}-backend"
  deployment_config_name = "CodeDeployDefault.ECSLinear10PercentEvery3Minutes"
  service_role_arn       = aws_iam_role.codedeploy.arn

  auto_rollback_configuration {
    enabled = true
    events  = ["DEPLOYMENT_FAILURE", "DEPLOYMENT_STOP_ON_ALARM"]
  }

  blue_green_deployment_config {
    deployment_ready_option {
      action_on_timeout = "CONTINUE_DEPLOYMENT"
    }

    terminate_blue_instances_on_deployment_success {
      action                           = "TERMINATE"
      termination_wait_time_in_minutes = 5
    }
  }

  deployment_style {
    deployment_option = "WITH_TRAFFIC_CONTROL"
    deployment_type   = "BLUE_GREEN"
  }

  ecs_service {
    cluster_name = aws_ecs_cluster.main.name
    service_name = aws_ecs_service.backend.name
  }

  load_balancer_info {
    target_group_pair_info {
      prod_traffic_route {
        listener_arns = [aws_lb_listener.https.arn]
      }
      test_traffic_route {
        listener_arns = [aws_lb_listener.test.arn]
      }
      target_group {
        name = aws_lb_target_group.blue.name
      }
      target_group {
        name = aws_lb_target_group.green.name
      }
    }
  }

  alarm_configuration {
    alarms  = [aws_cloudwatch_metric_alarm.backend_5xx.alarm_name]
    enabled = true
  }
}
```

---

## 8. IAM Roles for ECS

```hcl
# Execution Role — used by ECS agent to pull images, write logs, read secrets
resource "aws_iam_role" "ecs_execution" {
  name = "${local.project}-${local.environment}-ecs-execution"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = { Service = "ecs-tasks.amazonaws.com" }
    }]
  })
}

resource "aws_iam_role_policy_attachment" "ecs_execution_base" {
  role       = aws_iam_role.ecs_execution.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

resource "aws_iam_role_policy" "ecs_execution_secrets" {
  name = "secrets-access"
  role = aws_iam_role.ecs_execution.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "ssm:GetParameters",
          "ssm:GetParameter",
        ]
        Resource = "arn:aws:ssm:us-east-1:*:parameter/${local.project}/${local.environment}/*"
      },
      {
        Effect = "Allow"
        Action = [
          "secretsmanager:GetSecretValue",
        ]
        Resource = "arn:aws:secretsmanager:us-east-1:*:secret:${local.project}/${local.environment}/*"
      }
    ]
  })
}

# Task Role — used by your application code at runtime
resource "aws_iam_role" "ecs_task" {
  name = "${local.project}-${local.environment}-ecs-task"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = { Service = "ecs-tasks.amazonaws.com" }
    }]
  })
}

resource "aws_iam_role_policy" "ecs_task_s3" {
  name = "s3-access"
  role = aws_iam_role.ecs_task.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Action = [
        "s3:GetObject",
        "s3:PutObject",
        "s3:DeleteObject",
      ]
      Resource = "arn:aws:s3:::${local.project}-${local.environment}-uploads/*"
    }]
  })
}
```

---

## 9. ECS Exec (Debugging)

```bash
# Enable ECS Exec on a running service (if not already enabled via Terraform)
aws ecs update-service \
  --cluster production \
  --service myapp-backend \
  --enable-execute-command

# Connect to a running container
aws ecs execute-command \
  --cluster production \
  --task arn:aws:ecs:us-east-1:123456789012:task/production/abc123def456 \
  --container backend \
  --interactive \
  --command "/bin/sh"

# Run a one-off command (e.g., database migration)
aws ecs execute-command \
  --cluster production \
  --task arn:aws:ecs:us-east-1:123456789012:task/production/abc123def456 \
  --container backend \
  --command "npx prisma migrate deploy"
```

---

## 10. Cost Implications

| Resource | Monthly Cost (us-east-1) | Notes |
|----------|-------------------------|-------|
| Fargate 0.25 vCPU + 0.5GB | ~$9/task | Minimum task size |
| Fargate 0.5 vCPU + 1GB | ~$18/task | Good for Node.js APIs |
| Fargate 1 vCPU + 2GB | ~$36/task | Heavy compute |
| ALB | ~$16/month | + $0.008/LCU-hour |
| ECR storage | $0.10/GB/month | First 500MB free |
| CloudWatch Logs | $0.50/GB ingested | Set log retention |
| Container Insights | ~$0.30/task/month | Per-container metrics |

### Cost Optimization

- Use Fargate Spot for non-critical workloads (up to 70% savings)
- Set ECR lifecycle policies to clean old images
- Right-size tasks based on actual CPU/memory CloudWatch metrics
- Set CloudWatch log retention (7 days staging, 30 days production)
- Use `deployment_circuit_breaker` to auto-rollback failed deploys (avoids runaway task launches)

---

## 11. Common Mistakes / Anti-Patterns

| Mistake | Why It's Bad | Fix |
|---------|-------------|-----|
| Using `bridge` network mode with Fargate | Fargate requires `awsvpc` | Always use `awsvpc` for Fargate |
| No health check grace period | Tasks killed before app starts | Set `health_check_grace_period_seconds = 120` |
| `desired_count` not in `ignore_changes` | Terraform overrides auto-scaling | Add to `lifecycle.ignore_changes` |
| Hardcoded image tag in task def | Terraform redeploys constantly | Use `ignore_changes = [task_definition]` on service |
| No circuit breaker | Failed deploys spin up tasks forever | Enable `deployment_circuit_breaker` with rollback |
| Assigning public IP in private subnet | Security risk, bypasses NAT | Set `assign_public_ip = false` |
| No log retention policy | CloudWatch costs grow unbounded | Set `retention_in_days` on log group |
| Missing `initProcessEnabled` | Zombie processes, signal handling issues | Enable init process in `linuxParameters` |

---

## 12. Deployment Verification

```bash
# Check service status
aws ecs describe-services --cluster production --services myapp-backend \
  --query "services[0].{Status:status,Running:runningCount,Desired:desiredCount,Deployments:deployments[*].{Status:status,Running:runningCount,Desired:desiredCount,TaskDef:taskDefinition}}" \
  --output json

# Check recent task failures
aws ecs list-tasks --cluster production --service-name myapp-backend --desired-status STOPPED \
  --query "taskArns[:5]" --output text | \
  xargs -I {} aws ecs describe-tasks --cluster production --tasks {} \
  --query "tasks[*].{StopCode:stopCode,StopReason:stoppedReason,StartedAt:startedAt,StoppedAt:stoppedAt}" --output table

# Check ALB target health
aws elbv2 describe-target-health --target-group-arn arn:aws:elasticloadbalancing:us-east-1:123456789012:targetgroup/myapp-backend-tg/xxxx \
  --query "TargetHealthDescriptions[*].{Target:Target.Id,Port:Target.Port,Health:TargetHealth.State,Reason:TargetHealth.Reason}" --output table

# Watch deployment progress
watch -n 5 'aws ecs describe-services --cluster production --services myapp-backend --query "services[0].deployments[*].{Status:status,Running:runningCount,Desired:desiredCount,Pending:pendingCount}" --output table'
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

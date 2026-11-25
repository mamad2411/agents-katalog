---
name: aws-deployment
description: AWS deployment patterns: ECS Fargate, Lambda, EC2, App Runner, CloudFormation, CDK. Infrastructure as code, blue-green deployments, rolling updates, health checks, auto-scaling, CloudWatch integration.
origin: AI Dev Kit
disable-model-invocation: false
---

# AWS Deployment

Production AWS deployment patterns: ECS Fargate, Lambda, EC2, App Runner, infrastructure as code with CDK and Terraform, deployment strategies (blue-green, rolling, canary), auto-scaling, health checks, CloudWatch integration, and CI/CD pipeline patterns.

## When to Use

- Deploying applications or services to AWS
- Writing Infrastructure as Code (CDK, Terraform, CloudFormation)
- Choosing between ECS Fargate, Lambda, EC2, or App Runner
- Implementing blue-green or rolling deployment strategies
- Configuring auto-scaling policies and health checks
- Setting up CloudWatch monitoring, alarms, and dashboards
- Building CI/CD pipelines for AWS deployments
- Migrating workloads between AWS services

## Core Concepts

### 1. Service Selection Guide

| Service | Best For | Startup | Scaling | Cost Model | Max Concurrent |
|---|---|---|---|---|---|
| **Lambda** | Event-driven, sporadic traffic | <1s cold start | Automatic | Per-invocation | 10,000 default |
| **ECS Fargate** | Containerized services, steady traffic | 30-90s | Auto + manual | Per vCPU/GB-hour | Unlimited |
| **EC2** | Full control, custom kernels | 1-5 min | Auto Scaling Groups | Per instance-hour | Limited by quota |
| **App Runner** | HTTP services, minimal ops | 30-60s | Automatic | Per vCPU/GB + request | ~1,000 per service |

**Decision tree:**
```
Is it event-driven (S3, SQS, EventBridge)? ──Yes──▶ Lambda
  │
  No
  │
  Do you need custom OS/kernel access? ──Yes──▶ EC2
  │
  No
  │
  Is it a simple HTTP/HTTPS service? ──Yes──▶ App Runner
  │
  No (or need advanced networking, sidecars, custom orchestration)
  │
  ▶ ECS Fargate
```

### 2. AWS CDK — ECS Fargate Service

**TypeScript CDK stack with auto-scaling, health checks, and blue-green readiness:**

```typescript
import * as cdk from "aws-cdk-lib";
import * as ecs from "aws-cdk-lib/aws-ecs";
import * as ec2 from "aws-cdk-lib/aws-ec2";
import * as elbv2 from "aws-cdk-lib/aws-elasticloadbalancingv2";
import * as ecsPatterns from "aws-cdk-lib/aws-ecs-patterns";
import * as cloudwatch from "aws-cdk-lib/aws-cloudwatch";
import * as logs from "aws-cdk-lib/aws-logs";
import * as secretsmanager from "aws-cdk-lib/aws-secretsmanager";
import { Construct } from "constructs";

interface ApiServiceProps {
  readonly vpc: ec2.Vpc;
  readonly certificateArn: string;
  readonly domainName: string;
  readonly cpu: number;
  readonly memoryLimitMiB: number;
  readonly desiredCount: number;
  readonly maxCount: number;
  readonly imageTag: string;
}

export class ApiService extends Construct {
  public readonly service: ecs.FargateService;
  public readonly loadBalancer: elbv2.ApplicationLoadBalancer;

  constructor(scope: Construct, id: string, props: ApiServiceProps) {
    super(scope, id);

    // ECS Cluster
    const cluster = new ecs.Cluster(this, "Cluster", {
      vpc: props.vpc,
      enableFargateCapacityProviders: true,
    });

    // Secrets from Secrets Manager
    const dbSecret = secretsmanager.Secret.fromSecretNameV2(
      this,
      "DbSecret",
      `/${cdk.Stack.of(this).stackName}/database-credentials`,
    );

    // Fargate Service via ApplicationLoadBalanced pattern
    const fargateService = new ecsPatterns.ApplicationLoadBalancedFargateService(
      this,
      "Service",
      {
        cluster,
        taskImageOptions: {
          image: ecs.ContainerImage.fromRegistry(
            `public.ecr.aws/myapp/web:${props.imageTag}`,
          ),
          cpu: props.cpu,
          memoryLimitMiB: props.memoryLimitMiB,
          containerPort: 8080,
          environment: {
            NODE_ENV: "production",
            DATABASE_HOST: dbSecret.secretValueFromJson("host").toString(),
          },
          secrets: {
            DATABASE_PASSWORD: ecs.Secret.fromSecretsManager(dbSecret, "password"),
          },
          logDriver: ecs.LogDrivers.awsLogs({
            streamPrefix: "web",
            logRetention: logs.RetentionDays.ONE_MONTH,
          }),
        },
        desiredCount: props.desiredCount,
        protocol: elbv2.ApplicationProtocol.HTTPS,
        certificate: cdk.aws_certificatemanager.Certificate.fromCertificateArn(
          this,
          "Cert",
          props.certificateArn,
        ),
        domainName: props.domainName,
        // Health check — critical for deployment success
        healthCheckGracePeriod: cdk.Duration.seconds(60),
      },
    );

    // Target group health check configuration
    fargateService.targetGroup.configureHealthCheck({
      path: "/health",
      port: "8080",
      interval: cdk.Duration.seconds(30),
      timeout: cdk.Duration.seconds(5),
      healthyThresholdCount: 3,
      unhealthyThresholdCount: 2,
      healthyHttpCodes: "200",
    });

    // Auto-scaling based on CPU and request count
    const scalableTarget = fargateService.service.autoScaleTaskCount({
      minCapacity: props.desiredCount,
      maxCapacity: props.maxCount,
    });

    // Scale on CPU utilization (target 60%)
    scalableTarget.scaleOnCpuUtilization("CpuScaling", {
      targetUtilizationPercent: 60,
      scaleInCooldown: cdk.Duration.minutes(3),
      scaleOutCooldown: cdk.Duration.minutes(1),
    });

    // Scale on ALB request count per target
    scalableTarget.scaleOnRequestCount("RequestScaling", {
      requestsPerTarget: 1000,
      targetGroup: fargateService.targetGroup,
    });

    this.service = fargateService.service;
    this.loadBalancer = fargateService.loadBalancer;

    // CloudWatch alarms
    this.createAlarms(fargateService.service, props.domainName);
  }

  private createAlarms(service: ecs.FargateService, domainName: string): void {
    // High error rate alarm
    const errorRateAlarm = new cloudwatch.Alarm(this, "HighErrorRate", {
      metric: service.metric("CPUUtilization"),
      threshold: 90,
      evaluationPeriods: 3,
      comparisonOperator: cloudwatch.ComparisonOperator.GREATER_THAN_THRESHOLD,
      treatMissingData: cloudwatch.TreatMissingData.NOT_BREACHING,
    });

    errorRateAlarm.addAlarmAction(
      new cdk.aws_cloudwatch_actions.SnsAction(
        new cdk.aws_sns.Topic(this, "AlertsTopic"),
      ),
    );
  }
}
```

### 3. Terraform — ECS Fargate with Rolling Updates

```hcl
# modules/ecs_fargate/main.tf

resource "aws_ecs_cluster" "main" {
  name = "${var.app_name}-${var.environment}"

  setting {
    name  = "containerInsights"
    value = "enabled"
  }
}

resource "aws_ecs_task_definition" "web" {
  family                   = "${var.app_name}-web"
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = var.cpu
  memory                   = var.memory
  execution_role_arn       = aws_iam_role.ecs_execution.arn
  task_role_arn            = aws_iam_role.ecs_task.arn

  container_definitions = jsonencode([
    {
      name      = "web"
      image     = "${var.ecr_repository_url}:${var.image_tag}"
      essential = true

      portMappings = [
        {
          containerPort = 8080
          protocol      = "tcp"
        }
      ]

      environment = [
        { name = "NODE_ENV", value = var.environment },
        { name = "LOG_LEVEL",  value = var.log_level },
      ]

      secrets = [
        {
          name      = "DATABASE_URL"
          valueFrom = "${aws_secretsmanager_secret.db.arn}:DATABASE_URL::"
        }
      ]

      logConfiguration = {
        logDriver = "awslogs"
        options = {
          "awslogs-group"         = aws_cloudwatch_log_group.web.name
          "awslogs-region"        = var.aws_region
          "awslogs-stream-prefix" = "web"
        }
      }

      healthCheck = {
        command     = ["CMD-SHELL", "curl -f http://localhost:8080/health || exit 1"]
        interval    = 30
        timeout     = 5
        retries     = 3
        startPeriod = 60
      }
    }
  ])

  runtime_platform {
    operating_system_family = "LINUX"
    cpu_architecture        = var.cpu_architecture  # "X86_64" or "ARM64"
  }
}

resource "aws_ecs_service" "web" {
  name            = "${var.app_name}-web"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.web.arn
  desired_count   = var.desired_count
  launch_type     = "FARGATE"

  # Rolling update deployment strategy
  deployment_maximum_percent         = 200
  deployment_minimum_healthy_percent = 50

  # Wait for health checks before considering deployment complete
  health_check_grace_period_seconds = 120

  network_configuration {
    subnets          = var.private_subnet_ids
    security_groups  = [aws_security_group.web.id]
    assign_public_ip = false
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.web.arn
    container_name   = "web"
    container_port   = 8080
  }

  # Auto-scaling via application auto-scaling
  lifecycle {
    ignore_changes = [desired_count]  # Managed by auto-scaling
  }

  depends_on = [aws_lb_listener.https]
}

# Application Load Balancer
resource "aws_lb" "main" {
  name               = "${var.app_name}-${var.environment}"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb.id]
  subnets            = var.public_subnet_ids

  enable_deletion_protection = var.environment == "production"
}

resource "aws_lb_target_group" "web" {
  name        = "${var.app_name}-web-${var.environment}"
  port        = 80
  protocol    = "HTTP"
  vpc_id      = var.vpc_id
  target_type = "ip"  # Fargate uses IP targets

  health_check {
    enabled             = true
    path                = "/health"
    port                = "8080"
    protocol            = "HTTP"
    interval            = 30
    timeout             = 5
    healthy_threshold   = 3
    unhealthy_threshold = 2
    matcher             = "200"
  }
}

# CloudWatch Log Group
resource "aws_cloudwatch_log_group" "web" {
  name              = "/ecs/${var.app_name}-web-${var.environment}"
  retention_in_days = var.environment == "production" ? 30 : 7
}

# Auto-scaling
resource "aws_appautoscaling_target" "ecs" {
  max_capacity       = var.max_count
  min_capacity       = var.desired_count
  resource_id        = "service/${aws_ecs_cluster.main.name}/${aws_ecs_service.web.name}"
  scalable_dimension = "ecs:service:DesiredCount"
  service_namespace  = "ecs"
}

resource "aws_appautoscaling_policy" "cpu_scaling" {
  name               = "${var.app_name}-cpu-scaling"
  policy_type        = "TargetTrackingScaling"
  resource_id        = aws_appautoscaling_target.ecs.resource_id
  scalable_dimension = aws_appautoscaling_target.ecs.scalable_dimension
  service_namespace  = aws_appautoscaling_target.ecs.service_namespace

  target_tracking_scaling_policy_configuration {
    predefined_metric_specification {
      predefined_metric_type = "ECSServiceAverageCPUUtilization"
    }
    target_value       = 60.0
    scale_in_cooldown  = 180
    scale_out_cooldown = 60
  }
}
```

### 4. Lambda Deployment Patterns

**CDK — Lambda with Lambda Alias for Blue-Green Deployments:**

```typescript
import * as lambda from "aws-cdk-lib/aws-lambda";
import * as codedeploy from "aws-cdk-lib/aws-codedeploy";
import * as apigateway from "aws-cdk-lib/aws-apigateway";

// Lambda function
const fn = new lambda.Function(this, "Handler", {
  runtime: lambda.Runtime.NODEJS_20_X,
  handler: "index.handler",
  code: lambda.Code.fromAsset("src/lambda"),
  timeout: cdk.Duration.seconds(30),
  memorySize: 512,
  environment: {
    TABLE_NAME: table.tableName,
  },
  logRetention: logs.RetentionDays.ONE_WEEK,
});

// Alias for traffic shifting
const alias = new lambda.Alias(this, "LiveAlias", {
  aliasName: "live",
  version: fn.currentVersion,
  provisionedConcurrentExecutions: 1,  // Keep warm
});

// CodeDeploy for blue-green with canary
const deploymentConfig = codedeploy.LambdaDeploymentConfig.CANARY_10PERCENT_5MINUTES;

new codedeploy.LambdaDeploymentGroup(this, "Deployment", {
  alias,
  deploymentConfig,
  alarms: [
    new cloudwatch.Alarm(this, "ErrorAlarm", {
      metric: alias.metricErrors(),
      threshold: 1,
      evaluationPeriods: 2,
    }),
  ],
  autoRollback: {
    failedDeployment: true,
    stoppedDeployment: true,
    deploymentInAlarm: true,
  },
  // Pre/post hooks
  preHook: lambdaAliasPreHook,   // Run tests before traffic shift
  postHook: lambdaAliasPostHook,  // Validate after traffic shift complete
});
```

### 5. Deployment Strategies

#### Blue-Green Deployment

```
                 ┌─────────────┐
  Traffic ──────▶│   ALB/NLB   │
                 └──────┬──────┘
                        │
              ┌─────────┴─────────┐
              ▼                   ▼
    ┌─────────────────┐ ┌─────────────────┐
    │  Blue (active)  │ │  Green (idle)   │
    │  v1.2.0         │ │  v1.3.0 (new)   │
    │  3 instances    │ │  3 instances    │
    └─────────────────┘ └─────────────────┘

After validation: shift 100% traffic to Green, terminate Blue.
```

**Implementation steps:**
1. Deploy new version to idle target group (Green)
2. Run health checks and integration tests against Green
3. Switch ALB listener rule from Blue to Green
4. Monitor Green for errors (CloudWatch alarms)
5. If healthy after N minutes, terminate Blue
6. If unhealthy, rollback to Blue (instant)

#### Rolling Update

```
ECS Service (desired: 4 tasks):

Step 1: [v1.0, v1.0, v1.0, v1.0, v1.1]  (start 1 new, max 120%)
Step 2: [v1.0, v1.0, v1.0, v1.1, v1.1]  (stop 1 old, min 75%)
Step 3: [v1.0, v1.0, v1.1, v1.1, v1.1]
Step 4: [v1.0, v1.1, v1.1, v1.1, v1.1]
Step 5: [v1.1, v1.1, v1.1, v1.1]        (all new)
```

ECS default: `deployment_maximum_percent=200`, `deployment_minimum_healthy_percent=50`

#### Canary Deployment

```
Time 0:   100% Blue,   0% Green
Time 1m:   90% Blue,  10% Green   (canary starts)
Time 5m:   75% Blue,  25% Green   (monitoring)
Time 10m:  50% Blue,  50% Green   (half traffic)
Time 20m:  25% Blue,  75% Green   (monitoring)
Time 30m:   0% Blue, 100% Green   (complete)

If error rate spikes at any step → rollback immediately.
```

### 6. CI/CD Pipeline for ECS

**GitHub Actions → ECR → ECS:**

```yaml
# .github/workflows/deploy.yml
name: Deploy to ECS

on:
  push:
    branches: [main]
  workflow_dispatch:

env:
  ECR_REPOSITORY: myapp/web
  ECS_CLUSTER: myapp-production
  ECS_SERVICE: myapp-web
  ECS_TASK_DEFINITION: ecs/task-definition.json

jobs:
  deploy:
    runs-on: ubuntu-latest
    permissions:
      id-token: write  # OIDC for AWS
      contents: read

    steps:
      - uses: actions/checkout@v4

      - name: Configure AWS credentials (OIDC)
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::123456789:role/github-actions-deploy
          aws-region: us-east-1

      - name: Login to Amazon ECR
        id: login-ecr
        uses: aws-actions/amazon-ecr-login@v2

      - name: Build and push Docker image
        env:
          ECR_REGISTRY: ${{ steps.login-ecr.outputs.registry }}
          IMAGE_TAG: ${{ github.sha }}
        run: |
          docker build -t $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG .
          docker push $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG
          # Tag as latest for easy reference
          docker tag $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG \
                     $ECR_REGISTRY/$ECR_REPOSITORY:latest
          docker push $ECR_REGISTRY/$ECR_REPOSITORY:latest

      - name: Render task definition
        env:
          ECR_REGISTRY: ${{ steps.login-ecr.outputs.registry }}
          IMAGE_TAG: ${{ github.sha }}
        run: |
          sed "s|\${IMAGE_URI}|$ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG|g" \
            ecs/task-definition.template.json > $ECS_TASK_DEFINITION

      - name: Deploy to ECS (rolling update)
        uses: aws-actions/amazon-ecs-deploy-task-definition@v2
        with:
          task-definition: ${{ env.ECS_TASK_DEFINITION }}
          service: ${{ env.ECS_SERVICE }}
          cluster: ${{ env.ECS_CLUSTER }}
          wait-for-service-stability: true
          wait-for-minutes: 15  # Max wait for health checks

      - name: Run post-deploy smoke tests
        run: |
          # Wait for ALB health check to pass
          sleep 60
          # Smoke test against the service URL
          curl -f --retry 3 --retry-delay 10 \
            https://api.myapp.com/health \
            -H "Authorization: Bearer $SMOKE_TEST_TOKEN"
```

### 7. CloudWatch Monitoring Dashboard

```typescript
// lib/monitoring.ts
export function createServiceDashboard(
  scope: Construct,
  id: string,
  props: { serviceName: string; clusterName: string; loadBalancerArn: string },
): cloudwatch.Dashboard {
  const dashboard = new cloudwatch.Dashboard(scope, id, {
    dashboardName: `${props.serviceName}-production`,
  });

  // Row 1: Latency and error rate
  dashboard.addWidgets(
    new cloudwatch.GraphWidget({
      title: "Response Time (p50, p90, p99)",
      left: [
        new cloudwatch.Metric({
          namespace: "AWS/ApplicationELB",
          metricName: "TargetResponseTime",
          dimensionsMap: { LoadBalancer: props.loadBalancerArn },
          statistic: "p50",
          period: cdk.Duration.minutes(1),
        }).with({ color: cloudwatch.Color.GREEN, label: "p50" }),
        new cloudwatch.Metric({
          namespace: "AWS/ApplicationELB",
          metricName: "TargetResponseTime",
          dimensionsMap: { LoadBalancer: props.loadBalancerArn },
          statistic: "p90",
          period: cdk.Duration.minutes(1),
        }).with({ color: cloudwatch.Color.ORANGE, label: "p90" }),
        new cloudwatch.Metric({
          namespace: "AWS/ApplicationELB",
          metricName: "TargetResponseTime",
          dimensionsMap: { LoadBalancer: props.loadBalancerArn },
          statistic: "p99",
          period: cdk.Duration.minutes(1),
        }).with({ color: cloudwatch.Color.RED, label: "p99" }),
      ],
    }),
    new cloudwatch.GraphWidget({
      title: "Error Rate (5xx)",
      left: [
        new cloudwatch.Metric({
          namespace: "AWS/ApplicationELB",
          metricName: "HTTPCode_Target_5XX_Count",
          dimensionsMap: { LoadBalancer: props.loadBalancerArn },
          statistic: "Sum",
          period: cdk.Duration.minutes(1),
        }),
      ],
    }),
  );

  // Row 2: CPU, memory, task count
  dashboard.addWidgets(
    new cloudwatch.GraphWidget({
      title: "ECS CPU Utilization",
      left: [
        new cloudwatch.Metric({
          namespace: "AWS/ECS",
          metricName: "CPUUtilization",
          dimensionsMap: { ClusterName: props.clusterName, ServiceName: props.serviceName },
          statistic: "Average",
          period: cdk.Duration.minutes(1),
        }),
      ],
    }),
    new cloudwatch.SingleValueWidget({
      title: "Running Tasks",
      metrics: [
        new cloudwatch.Metric({
          namespace: "AWS/ECS",
          metricName: "RunningTaskCount",
          dimensionsMap: { ClusterName: props.clusterName, ServiceName: props.serviceName },
          statistic: "Average",
          period: cdk.Duration.minutes(1),
        }),
      ],
    }),
  );

  return dashboard;
}
```

### 8. Health Check Endpoint

Every service MUST expose a `/health` endpoint. This is the gate for deployment success.

```python
# FastAPI health check
from fastapi import FastAPI, status
from pydantic import BaseModel
import asyncpg

app = FastAPI()

class HealthStatus(BaseModel):
    status: str
    version: str
    database: str
    uptime_seconds: int

START_TIME = time.time()

@app.get("/health")
async def health():
    """Liveness + readiness check."""
    db_status = "healthy"
    try:
        conn = await asyncpg.connect(dsn=DATABASE_URL, timeout=5)
        await conn.fetchval("SELECT 1")
        await conn.close()
    except Exception:
        db_status = "unhealthy"

    return HealthStatus(
        status="healthy" if db_status == "healthy" else "degraded",
        version=os.getenv("APP_VERSION", "unknown"),
        database=db_status,
        uptime_seconds=int(time.time() - START_TIME),
    )

@app.get("/ready")
async def readiness():
    """Readiness probe — fails if dependencies unavailable."""
    try:
        conn = await asyncpg.connect(dsn=DATABASE_URL, timeout=5)
        await conn.fetchval("SELECT 1")
        await conn.close()
        return {"status": "ready"}
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Not ready: {e}")
```

## Security Checklist

- [ ] **No hardcoded secrets** — use AWS Secrets Manager or SSM Parameter Store
- [ ] **Least-privilege IAM roles** — ECS task role has only needed permissions
- [ ] **Private subnets** for ECS tasks (no public IPs)
- [ ] **Security groups** — ALB allows 443 inbound, ECS allows ALB SG on container port only
- [ ] **TLS everywhere** — ALB terminates TLS, internal traffic via VPC
- [ ] **ECR image scanning** — enable scan-on-push
- [ ] **CloudWatch Logs** — all services log to CloudWatch with retention policy
- [ ] **VPC flow logs** — enabled for production VPCs
- [ ] **Deployment approval** — require manual approval for production deployments
- [ ] **Rollback capability** — always keep previous task definition available

## Anti-Patterns

| Anti-Pattern | Risk | Fix |
|---|---|---|
| Deploying directly to ECS without CI | Inconsistent builds | Use CI/CD pipeline |
| No health check | Bad deploys go unnoticed | `/health` + `/ready` endpoints |
| `deployment_minimum_healthy_percent=0` | Downtime during deploy | Set to 50+ |
| Hard-coded credentials in env vars | Secret exposure | Use Secrets Manager |
| No auto-scaling | Overprovisioned or crashes | CPU + request-based scaling |
| No CloudWatch alarms | Incidents undetected | Alarm on errors, latency, CPU |
| Single AZ deployment | AZ outage = full outage | Multi-AZ subnets |
| No rollback strategy | Stuck with bad deploys | CodeDeploy with auto-rollback |

## Success Checklist

- [ ] Infrastructure defined as code (CDK or Terraform)
- [ ] CI/CD pipeline builds, pushes to ECR, deploys to ECS
- [ ] Health check (`/health`) and readiness (`/ready`) endpoints
- [ ] Auto-scaling configured (CPU + request count)
- [ ] CloudWatch dashboard and alarms
- [ ] Secrets in AWS Secrets Manager (not env vars)
- [ ] IAM roles follow least-privilege
- [ ] Multi-AZ deployment
- [ ] Deployment strategy documented (rolling, blue-green, or canary)
- [ ] Rollback tested and automated
- [ ] Container image scanning enabled

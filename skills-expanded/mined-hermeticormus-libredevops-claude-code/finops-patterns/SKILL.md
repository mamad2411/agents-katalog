---
name: finops-patterns
description: "Cloud cost patterns: AWS cost analysis queries, Savings Plans coverage, Spot Auto Scaling groups, gp2 to gp3 migration, S3 lifecycle and Intelligent-Tiering, VPC endpoints in place of NAT Gateway traffic, Infracost in pull requests, and tagging enforcement with SCPs. Use when finding or preventing cloud waste."
---

# FinOps Patterns

Cloud cost optimization patterns: Savings Plans, Spot handling, Infracost CI, S3 lifecycle, tagging enforcement.

## AWS Cost Analysis Queries

```bash
# Monthly cost by service (last 3 months)
aws ce get-cost-and-usage \
  --time-period Start=$(date -d '-90 days' +%Y-%m-%d),End=$(date +%Y-%m-%d) \
  --granularity MONTHLY \
  --metrics BlendedCost UsageQuantity \
  --group-by Type=DIMENSION,Key=SERVICE \
  --query 'ResultsByTime[*].Groups[?Metrics.BlendedCost.Amount > `10`] | sort_by(@, &Metrics.BlendedCost.Amount) | reverse(@)[:10]'

# Daily cost anomaly detection
aws ce get-anomalies \
  --date-interval Start=$(date -d '-7 days' +%Y-%m-%d),End=$(date +%Y-%m-%d) \
  --query 'Anomalies[].{Service:DimensionValue,TotalImpact:TotalImpact.TotalActualSpend,Expected:TotalImpact.TotalExpectedSpend}'

# Cost by tag (requires tags to be activated in Cost Explorer)
aws ce get-cost-and-usage \
  --time-period Start=$(date -d '-30 days' +%Y-%m-%d),End=$(date +%Y-%m-%d) \
  --granularity MONTHLY \
  --metrics BlendedCost \
  --group-by Type=TAG,Key=Team \
  --output table
```

## Savings Plans Coverage Analysis

```bash
# Check current Savings Plans coverage
aws ce get-savings-plans-coverage \
  --time-period Start=$(date -d '-30 days' +%Y-%m-%d),End=$(date +%Y-%m-%d) \
  --granularity MONTHLY \
  --query 'SavingsPlansCoverages[*].Coverage.{Covered:CoveredSpend,OnDemand:OnDemandCost,CoveragePercent:CoveragePercentage}'

# Get Savings Plans purchase recommendation
aws savingsplans get-savings-plans-purchase-recommendation \
  --savings-plans-type COMPUTE_SP \
  --term-in-years ONE_YEAR \
  --payment-option NO_UPFRONT \
  --lookback-period-in-days SIXTY_DAYS \
  --query '{
    EstimatedMonthlySavings: Metadata.EstimatedSavingsAmount,
    RecommendedHourlyCommitment: SavingsPlansRecommendation.SavingsPlansDetails.HourlyCommitment,
    EstimatedROI: SavingsPlansRecommendation.EstimatedROI
  }'
```

## Spot Instance Auto Scaling Group

```hcl
# terraform: ASG with mixed On-Demand + Spot, multiple instance types
resource "aws_autoscaling_group" "workers" {
  name                = "batch-workers"
  min_size            = 1
  max_size            = 50
  desired_capacity    = 5
  vpc_zone_identifier = var.private_subnet_ids

  mixed_instances_policy {
    instances_distribution {
      on_demand_base_capacity                  = 1     # Always keep 1 On-Demand
      on_demand_percentage_above_base_capacity = 20   # 20% On-Demand, 80% Spot above base
      spot_allocation_strategy                 = "capacity-optimized"  # Minimize interruptions
      spot_max_price                           = ""   # Use current Spot price (not max)
    }

    launch_template {
      launch_template_specification {
        launch_template_id = aws_launch_template.worker.id
        version            = "$Latest"
      }

      # Multiple instance types for Spot availability diversification
      override {
        instance_type     = "m6g.xlarge"
        weighted_capacity = "4"
      }
      override {
        instance_type     = "m6i.xlarge"
        weighted_capacity = "4"
      }
      override {
        instance_type     = "m5.xlarge"
        weighted_capacity = "4"
      }
      override {
        instance_type     = "c6g.xlarge"
        weighted_capacity = "4"
      }
    }
  }

  instance_refresh {
    strategy = "Rolling"
    preferences {
      min_healthy_percentage = 90
    }
  }

  tag {
    key                 = "SpotInterruptionHandling"
    value               = "graceful"
    propagate_at_launch = true
  }
}
```

## gp2 to gp3 Migration (Zero Downtime)

```bash
# Find all gp2 volumes in account
aws ec2 describe-volumes \
  --filters Name=volume-type,Values=gp2 \
  --query 'Volumes[].{VolumeId:VolumeId,Size:Size,IOPS:Iops,Region:AvailabilityZone}' \
  --output table

# Modify volume to gp3 (no downtime, takes a few minutes)
aws ec2 modify-volume \
  --volume-id vol-0123456789abcdef0 \
  --volume-type gp3 \
  --iops 3000 \          # gp3 baseline is 3000 IOPS (same as gp2 up to 1TB)
  --throughput 125        # gp3 baseline is 125 MB/s (better than gp2)

# Bulk convert all gp2 to gp3 in a region
aws ec2 describe-volumes \
  --filters Name=volume-type,Values=gp2 \
  --query 'Volumes[].VolumeId' \
  --output text | \
  xargs -P 10 -I{} aws ec2 modify-volume \
    --volume-id {} \
    --volume-type gp3

# Savings: gp2 costs $0.10/GB/month, gp3 costs $0.08/GB/month = 20% savings
# Plus gp3 has 20% better IOPS baseline
```

## S3 Lifecycle and Intelligent Tiering

```hcl
# Terraform: S3 lifecycle rules
resource "aws_s3_bucket_lifecycle_configuration" "backups" {
  bucket = aws_s3_bucket.backups.id

  rule {
    id     = "backup-lifecycle"
    status = "Enabled"

    filter { prefix = "daily/" }

    transition {
      days          = 30
      storage_class = "STANDARD_IA"
    }
    transition {
      days          = 90
      storage_class = "GLACIER_IR"    # Glacier Instant Retrieval: ms restore
    }
    transition {
      days          = 180
      storage_class = "DEEP_ARCHIVE"  # $0.00099/GB/month - cheapest
    }
    expiration {
      days = 365
    }
  }

  rule {
    id     = "delete-incomplete-multipart"
    status = "Enabled"
    filter {}
    abort_incomplete_multipart_upload {
      days_after_initiation = 7
    }
  }
}

# Intelligent Tiering for data lake (auto-tiers without access pattern knowledge)
resource "aws_s3_bucket_intelligent_tiering_configuration" "data_lake" {
  bucket = aws_s3_bucket.data_lake.id
  name   = "EntireDataLake"

  tiering {
    access_tier = "DEEP_ARCHIVE_ACCESS"
    days        = 180
  }
  tiering {
    access_tier = "ARCHIVE_ACCESS"
    days        = 90
  }
}
```

## NAT Gateway Replacement with VPC Endpoints

```hcl
# Gateway endpoint for S3 (free, no data processing charges)
resource "aws_vpc_endpoint" "s3" {
  vpc_id       = aws_vpc.main.id
  service_name = "com.amazonaws.us-east-1.s3"
  vpc_endpoint_type = "Gateway"
  route_table_ids   = aws_route_table.private[*].id

  tags = { Name = "s3-gateway-endpoint" }
}

# Interface endpoints (saves NAT data charges at >50GB/month traffic)
resource "aws_vpc_endpoint" "ecr_api" {
  vpc_id              = aws_vpc.main.id
  service_name        = "com.amazonaws.us-east-1.ecr.api"
  vpc_endpoint_type   = "Interface"
  subnet_ids          = aws_subnet.private[*].id
  security_group_ids  = [aws_security_group.endpoints.id]
  private_dns_enabled = true
}

resource "aws_vpc_endpoint" "secrets_manager" {
  vpc_id              = aws_vpc.main.id
  service_name        = "com.amazonaws.us-east-1.secretsmanager"
  vpc_endpoint_type   = "Interface"
  subnet_ids          = aws_subnet.private[*].id
  security_group_ids  = [aws_security_group.endpoints.id]
  private_dns_enabled = true
}

# Cost analysis: Interface endpoints cost $0.01/hr per AZ = $7.20/month each
# Break-even: ~160GB/month of NAT Gateway traffic at $0.045/GB
```

## Infracost PR Integration

```yaml
# .github/workflows/infracost.yml
name: Infracost
on:
  pull_request:
    paths: ['terraform/**', '*.tf']

permissions:
  contents: read
  pull-requests: write

jobs:
  infracost:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Infracost
        uses: infracost/actions/setup@v3
        with:
          api-key: ${{ secrets.INFRACOST_API_KEY }}

      - name: Infracost on base branch
        run: |
          git checkout ${{ github.event.pull_request.base.sha }}
          infracost breakdown \
            --path terraform/ \
            --format json \
            --out-file /tmp/infracost-base.json

      - name: Infracost on PR branch
        run: |
          git checkout ${{ github.sha }}
          infracost breakdown \
            --path terraform/ \
            --format json \
            --out-file /tmp/infracost-pr.json

      - name: Infracost diff and comment
        run: |
          infracost diff \
            --path /tmp/infracost-pr.json \
            --compare-to /tmp/infracost-base.json \
            --format json \
            --out-file /tmp/infracost-diff.json

      - uses: infracost/actions/comment@v3
        with:
          path: /tmp/infracost-diff.json
          behavior: update
          # Optional: fail PR if cost increases by > $100/month
          # threshold-percent: 10
```

## Tagging Enforcement SCP

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "DenyWithoutRequiredTags",
      "Effect": "Deny",
      "Action": [
        "ec2:RunInstances",
        "rds:CreateDBInstance",
        "elasticache:CreateCacheCluster",
        "eks:CreateCluster"
      ],
      "Resource": "*",
      "Condition": {
        "Null": {
          "aws:RequestTag/Environment": "true",
          "aws:RequestTag/Team": "true",
          "aws:RequestTag/Service": "true"
        }
      }
    }
  ]
}
```

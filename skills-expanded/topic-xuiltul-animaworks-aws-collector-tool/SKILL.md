---
name: aws-collector-tool
description: >-
  AWS infrastructure information collection tool. Retrieves ECS status, CloudWatch logs, and metrics.
  Use when: Use when: checking ECS operation, investigating error logs in CloudWatch, retrieving metrics, or monitoring AWS resources.
tags: [infrastructure, aws, monitoring, external]
---


# AWS Collector Tool

An external tool that collects AWS ECS status, CloudWatch logs, and metrics.

## How to Invoke

**Bash**: Run with `animaworks-tool aws_collector <サブコマンド> [引数]`

## Available Actions

### ecs_status — Check ECS Service Status
```bash
animaworks-tool aws_collector ecs-status [--cluster NAME] [--service NAME]
```

### error_logs — Retrieve Error Logs
```bash
animaworks-tool aws_collector error-logs --log-group NAME [--hours 1] [--patterns "ERROR"]
```

### metrics — Retrieve Metrics
```bash
animaworks-tool aws_collector metrics --cluster NAME --service NAME [--metric CPUUtilization]
```

## CLI Usage

```bash
animaworks-tool aws_collector ecs-status [--cluster NAME] [--service NAME]
animaworks-tool aws_collector error-logs --log-group NAME [--hours 1] [--patterns "ERROR"]
animaworks-tool aws_collector metrics --cluster NAME --service NAME [--metric CPUUtilization]
```

## Notes

- AWS authentication credentials (via environment variables or credentials file) are required
- Region can be specified with --region

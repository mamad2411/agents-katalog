---
name: aws-internetmonitor
description: "Internet Monitor via AWS CLI v2 (`aws internetmonitor`). Monitors, health events, internet events, performance/availability queries."
---

# AWS CLI v2 — Internet Monitor (CloudWatch Internet Monitor)

## Overview

Complete reference for all `aws internetmonitor` subcommands in AWS CLI v2. Amazon CloudWatch Internet Monitor provides visibility into how internet issues impact the performance and availability between your applications hosted on AWS and your end users. It uses the connectivity data from the global AWS network to create monitors that report on health events and provide recommendations.

## Quick Reference — Common Workflows

### Create a monitor for a VPC
```bash
aws internetmonitor create-monitor \
  --monitor-name my-app-monitor \
  --resources arn:aws:ec2:us-east-1:123456789012:vpc/vpc-0123456789abcdef0 \
  --traffic-percentage-to-monitor 100 \
  --max-city-networks-to-monitor 500
```

### Enable S3 log delivery
```bash
aws internetmonitor update-monitor \
  --monitor-name my-app-monitor \
  --internet-measurements-log-delivery \
    S3Config={BucketName=my-monitoring-bucket,BucketPrefix=internet-monitor/,LogDeliveryStatus=ENABLED}
```

### Get monitor details
```bash
aws internetmonitor get-monitor --monitor-name my-app-monitor
```

### List active health events
```bash
aws internetmonitor list-health-events \
  --monitor-name my-app-monitor \
  --event-status ACTIVE
```

### Get details of a specific health event
```bash
aws internetmonitor get-health-event \
  --monitor-name my-app-monitor \
  --event-id event-12345
```

### Query top locations by traffic
```bash
QUERY_ID=$(aws internetmonitor start-query \
  --monitor-name my-app-monitor \
  --start-time 2024-01-01T00:00:00Z \
  --end-time 2024-01-02T00:00:00Z \
  --query-type TOP_LOCATIONS \
  --query 'QueryId' --output text)

aws internetmonitor get-query-results \
  --monitor-name my-app-monitor \
  --query-id $QUERY_ID
```

### List global internet events
```bash
aws internetmonitor list-internet-events \
  --event-status ACTIVE \
  --event-type AVAILABILITY
```

### Deactivate and delete a monitor
```bash
aws internetmonitor update-monitor --monitor-name my-app-monitor --status INACTIVE
aws internetmonitor delete-monitor --monitor-name my-app-monitor
```

## Command Reference

See [`index.md`](index.md) for the quick reference table and global options.

| Group | File | Commands |
|-------|------|----------|
| Monitors | [`monitors.md`](monitors.md) | create-monitor, get-monitor, update-monitor, delete-monitor, list-monitors |
| Events | [`events.md`](events.md) | list-health-events, get-health-event, list-internet-events, get-internet-event |
| Queries | [`queries.md`](queries.md) | start-query, get-query-results, get-query-status, stop-query |
| Tags | [`tags.md`](tags.md) | tag-resource, untag-resource, list-tags-for-resource |

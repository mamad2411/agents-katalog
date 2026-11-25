---
name: monitoring-sysadmin
description: System monitoring, metrics, alerting, dashboards, and observability
license: MIT
compatibility: opencode
metadata:
  audience: devops
  category: systems-administration
---

## What I do
- Set up comprehensive monitoring systems
- Configure meaningful alerts
- Create actionable dashboards
- Analyze metrics and trends
- Implement observability
- Establish SLOs and SLIs

## When to use me
When tracking system health, debugging issues, or establishing operational excellence.

## The Three Pillars

### Metrics (Prometheus, Datadog)
- Quantitative measurements
- Time-series data
- Counters, gauges, histograms
- Aggregations

### Logs (ELK, Loki, Splunk)
- Detailed event records
- Structured/unstructured
- Log levels (DEBUG, INFO, WARN, ERROR)
- Correlation IDs

### Traces (Jaeger, Zipkin)
- Request flow across services
- Latency breakdown
- Distributed tracing
- Span context

## Metrics Types

### Golden Signals
- **Latency**: Response time
- **Traffic**: Requests per second
- **Errors**: Error rate
- **Saturation**: Resource utilization

### RED Metrics (Rate, Errors, Duration)
- For request-driven services

### USE Metrics (Utilization, Saturation, Errors)
- For resource-driven services

## Alerting

### Best Practices
- Alert on symptoms, not causes
- Tune thresholds
- Avoid alert fatigue
- Include context
- Runbooks for each alert

### Severity Levels
- **Critical**: Immediate action needed
- **Warning**: Attention needed
- **Info**: For awareness

## Dashboards

### Design Principles
- Show relevant data
- Include context
- Time ranges
- Drill-down capability
- Shareable links

### Common Dashboards
- Service overview
- Infrastructure
- Application performance
- Business metrics
- Incident response

## Tools

### Monitoring
- **Prometheus**: Metrics, alerting
- **Datadog**: Full-stack
- **CloudWatch**: AWS
- **Stackdriver**: GCP

### Visualization
- **Grafana**: Dashboards
- **Kibana**: Logs

### Logging
- **ELK Stack**: Elasticsearch, Logstash, Kibana
- **Loki**: Promtail + Loki + Grafana
- **Splunk**: Enterprise

### Tracing
- **Jaeger**: Distributed tracing
- **Zipkin**: Twitter's tracer
- **AWS X-Ray**: Cloud

## SRE Concepts

### SLI (Service Level Indicator)
- Metric measuring service level
- Request latency
- Error rate
- Availability

### SLO (Service Level Objective)
- Target SLI value
- "99.9% of requests < 200ms"

### SLA (Service Level Agreement)
- Customer-facing commitment
- SLO + consequences

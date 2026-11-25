---
name: "infra-intelligence"
description: "Automated cloud cost anomaly detection, capacity forecasting, and infrastructure optimization for the Infrastructure department. Monitors AWS spending, resource utilization, and capacity trends. Produces cost reports with optimization recommendations and feeds the infra self-improvement loop. Use when analyzing cloud costs, forecasting capacity, optimizing infrastructure spend, right-sizing resources, or running the infrastructure UAOP pipeline."
risk: low
tags: [infrastructure, cost, capacity, optimization]
created: 2026-03-23
updated: 2026-03-23
---

# Infra Intelligence — Infrastructure Department Intelligence Engine

Automated cloud cost monitoring, capacity forecasting, and optimization recommendations. UAOP Stage 1 + Stage 5 for Infrastructure.

## When to use

- Monthly cloud cost review — "where's our money going?"
- After cost spikes — "why did our bill jump 30%?"
- Capacity planning — "when do we need to scale up?"
- Right-sizing review — "are we over-provisioned?"
- Before infrastructure changes — "what's the cost impact?"

## When NOT to use

- Active incident response (use `anomaly-detector` + `incident-responder`)
- Security scanning (use `threat-intelligence-feed` + `infrastructure-scanning`)
- Terraform changes (use `devops-patterns`)

## Pipeline

### Step 1: Cost Data Collection

Collect spending data across AWS services:

```
COST CENTERS:
  Compute:
    - ECS Fargate tasks (backend + frontend)
    - Task CPU/memory allocation vs actual usage
    - Running hours per environment (dev/staging/production)

  Database:
    - RDS PostgreSQL instance class + storage
    - Read/write IOPS vs provisioned
    - Backup storage costs
    - Connection count vs max_connections

  Cache:
    - ElastiCache Redis node type
    - Memory utilization vs allocated
    - Eviction rate (over-provisioned if zero, under if high)

  Networking:
    - CloudFront data transfer
    - NAT Gateway costs (often the silent killer)
    - Cross-AZ data transfer

  Storage:
    - ECR image storage
    - S3 bucket storage + request costs
    - EBS volumes (if any)

  CI/CD:
    - GitHub Actions minutes consumed
    - ECR image push/pull bandwidth

  LLM:
    - API token usage by provider (OpenAI, Anthropic, Kimi)
    - Cost per request by model
    - Token usage trends
```

### Step 2: Anomaly Detection

```
ANOMALY RULES:
  - Day-over-day increase >20% on any cost center → ALERT
  - Service cost exceeds monthly budget allocation → ALERT
  - Resource utilization <30% for >7 days → RIGHT-SIZE candidate
  - Resource utilization >80% for >3 days → SCALE-UP candidate
  - New cost center appears (unexpected service activated) → INVESTIGATE
  - LLM cost per request increasing without traffic increase → MODEL ISSUE
```

### Step 3: Capacity Forecasting

```
FORECAST MODEL:
  For each resource:
    1. Collect 90 days of utilization data
    2. Fit linear + seasonal trend
    3. Project when resource hits 80% capacity (scale-up trigger)
    4. Estimate cost at projected usage levels

  Output:
    | Resource | Current Usage | 80% Threshold | Days Until 80% | Monthly Cost at 80% |
    |----------|--------------|---------------|----------------|-------------------|
```

### Step 4: Optimization Recommendations

```markdown
# Infrastructure Cost Report — [Month] [Year]

## Spending Summary
| Cost Center | This Month | Last Month | Delta | % of Total |
|------------|-----------|-----------|-------|-----------|
| Compute (ECS) | $[X] | $[X] | [+/-$X] | [X]% |
| Database (RDS) | $[X] | $[X] | [+/-$X] | [X]% |
| Cache (Redis) | $[X] | $[X] | [+/-$X] | [X]% |
| Networking | $[X] | $[X] | [+/-$X] | [X]% |
| LLM APIs | $[X] | $[X] | [+/-$X] | [X]% |
| **Total** | **$[X]** | **$[X]** | **[+/-$X]** | 100% |

## Anomalies Detected
[List of cost spikes with root cause analysis]

## Optimization Opportunities
| # | Recommendation | Savings/Month | Effort | Risk |
|---|---------------|--------------|--------|------|
| 1 | Right-size [resource] from [current] to [recommended] | $[X] | [S/M/L] | [Low/Med/High] |

## Capacity Forecast
[Table of resources approaching capacity limits]

## LLM Cost Breakdown
| Model | Requests | Tokens | Cost | Cost/Request |
|-------|---------|--------|------|-------------|
```

### Step 5: Self-Improvement Loop

```
MEASURE:
  - Forecast accuracy (predicted cost vs actual)
  - Optimization recommendation ROI (savings achieved)
  - Anomaly detection precision (true vs false alerts)
  - Time from anomaly detection to resolution

REINFORCE:
  - Forecasting models that predicted accurately → use same method
  - Optimizations that saved money without incidents → template as standard
  - Cost centers with stable spending → reduce monitoring frequency

REGENERATE:
  - Update baselines after infrastructure changes
  - Add new cost centers when services are added
  - Adjust anomaly thresholds based on false positive rate
```

## Cadence

```
DAILY:    Cost anomaly scan (>20% day-over-day)
WEEKLY:   Cost summary + right-sizing candidates
MONTHLY:  Full cost report + optimization recommendations + capacity forecast
QUARTERLY: Infrastructure strategy review + budget reforecast
```

## Tools

| Tool | Purpose |
|------|---------|
| terraform MCP | Infrastructure state, resource inventory |
| kubernetes MCP | Pod resource utilization, scaling metrics |
| github MCP | CI/CD cost tracking (Actions minutes) |
| sequential MCP | Multi-step cost analysis reasoning |
| memory MCP | Store cost baselines, optimization history |

## Agents

| Agent | Role |
|-------|------|
| devops-architect (L2) | Owns infrastructure strategy |
| infra-engineer (L3) | Implements optimizations |
| cost-optimizer (L5) | Analyzes spending, recommends savings |
| performance-engineer (L2) | Validates perf impact of right-sizing |
| finance-tracker (L3) | Integrates with financial reporting |

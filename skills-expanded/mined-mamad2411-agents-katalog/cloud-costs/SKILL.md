---
name: cloud-costs
description: For cloud cost optimization, resource tagging, budget management, and cost monitoring strategies
user-invocable: false
---

# Cloud Costs Skill

## When to Use

Activate this skill when:
- Implementing cloud cost optimization strategies
- Setting up resource tagging and cost allocation
- Configuring budget alerts and cost monitoring
- Analyzing and reducing cloud spend
- Designing cost-aware architectures

## DO NOT Apply When

- Simple resource creation (use infrastructure-as-code skill)
- Performance optimization (use performance-profiling skill)
- Application monitoring (use observability skill)

## Core Principles

### Cost Optimization Strategies

**1. Right-Sizing Resources**

Match resources to workload requirements:

```python
import boto3

def analyze_instance_utilization(instance_id: str) -> dict:
    """Analyze EC2 instance utilization for right-sizing."""
    
    cloudwatch = boto3.client('cloudwatch')
    
    # Get CPU utilization over 7 days
    metrics = cloudwatch.get_metric_statistics(
        Namespace='AWS/EC2',
        MetricName='CPUUtilization',
        Dimensions=[{'Name': 'InstanceId', 'Value': instance_id}],
        StartTime=datetime.now() - timedelta(days=7),
        EndTime=datetime.now(),
        Period=3600,  # 1 hour
        Statistics=['Average', 'Maximum']
    )
    
    cpu_values = [dp['Average'] for dp in metrics['Datapoints']]
    avg_cpu = sum(cpu_values) / len(cpu_values) if cpu_values else 0
    max_cpu = max([dp['Maximum'] for dp in metrics['Datapoints']]) if metrics['Datapoints'] else 0
    
    # Recommend instance type
    if avg_cpu < 10:
        recommendation = 'Downsize to smaller instance type'
    elif avg_cpu > 80:
        recommendation = 'Upgrade to larger instance type'
    else:
        recommendation = 'Current size is appropriate'
    
    return {
        'average_cpu': avg_cpu,
        'max_cpu': max_cpu,
        'recommendation': recommendation
    }
```

**2. Resource Scheduling**

Schedule resources to run only when needed:

```yaml
# AWS EventBridge rule for EC2 start/stop
Resources:
  StartEC2Instances:
    Type: AWS::Events::Rule
    Properties:
      ScheduleExpression: 'cron(0 8 ? * MON-FRI *)'
      State: ENABLED
      Targets:
        - Arn: arn:aws:automate:${AWS::Region}:ec2:start
          Id: StartEC2
  
  StopEC2Instances:
    Type: AWS::Events::Rule
    Properties:
      ScheduleExpression: 'cron(0 18 ? * MON-FRI *)'
      State: ENABLED
      Targets:
        - Arn: arn:aws:automate:${AWS::Region}:ec2:stop
          Id: StopEC2
```

**3. Reserved and Savings Plans**

Use commitment-based pricing:

```python
def calculate_savings_plans_cost(
    hourly_rate: float,
    monthly_hours: int = 730
) -> dict:
    """Compare on-demand vs savings plans."""
    
    on_demand_monthly = hourly_rate * monthly_hours
    
    # Savings Plans typically offer 72% discount
    savings_plan_rate = hourly_rate * 0.28
    savings_plan_monthly = savings_plan_rate * monthly_hours
    
    savings = on_demand_monthly - savings_plan_monthly
    
    return {
        'on_demand_monthly': on_demand_monthly,
        'savings_plan_monthly': savings_plan_monthly,
        'monthly_savings': savings,
        'annual_savings': savings * 12
    }
```

### Resource Tagging

**4. Consistent Tagging Strategy**

Implement comprehensive tagging:

```python
import boto3

def apply_standard_tags(resource_arn: str, tags: dict) -> None:
    """Apply standard cost allocation tags."""
    
    standard_tags = {
        'Environment': tags.get('environment', 'development'),
        'Owner': tags.get('owner', 'team-name'),
        'Project': tags.get('project', 'default'),
        'CostCenter': tags.get('cost_center', 'default'),
        'CreatedBy': 'terraform',
        'AutoShutdown': tags.get('auto_shutdown', 'false')
    }
    
    # Apply tags to resource
    client = boto3.client('resourcegroupstaggingapi')
    client.tag_resources(
        ResourceARNList=[resource_arn],
        Tags=standard_tags
    )
```

**5. Cost Allocation by Tag**

Create cost allocation tags:

```python
def generate_cost_report_by_tag(tag_key: str, tag_value: str) -> dict:
    """Generate cost report for specific tag value."""
    
    ce = boto3.client('ce')
    
    response = ce.get_cost_and_usage(
        TimePeriod={
            'Start': (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'),
            'End': datetime.now().strftime('%Y-%m-%d')
        },
        Granularity='MONTHLY',
        Metrics=['BlendedCost', 'UnblendedCost'],
        Filter={
            'Tags': {
                'Key': tag_key,
                'Values': [tag_value],
                'MatchOptions': ['EQUALS']
            }
        },
        GroupBy=[
            {
                'Type': 'DIMENSION',
                'Key': 'SERVICE'
            }
        ]
    )
    
    return response
```

### Budget Management

**6. Budget Alerts**

Configure proactive budget alerts:

```python
def create_budget_alert(
    budget_name: str,
    limit_amount: float,
    notification_emails: list[str]
) -> None:
    """Create budget with alert thresholds."""
    
    budgets = boto3.client('budgets')
    
    budgets.create_budget(
        AccountId=boto3.client('sts').get_caller_identity()['Account'],
        Budget={
            'BudgetName': budget_name,
            'BudgetLimit': {'Amount': str(limit_amount), 'Unit': 'USD'},
            'TimeUnit': 'MONTHLY',
            'BudgetType': 'COST',
            'CostFilters': {
                'Service': ['Amazon EC2', 'Amazon RDS']
            }
        },
        NotificationsWithSubscribers=[
            {
                'Notification': {
                    'NotificationType': 'ACTUAL',
                    'ComparisonOperator': 'GREATER_THAN',
                    'Threshold': 80.0,
                    'ThresholdType': 'PERCENTAGE'
                },
                'Subscribers': [
                    {'SubscriptionType': 'EMAIL', 'Address': email}
                    for email in notification_emails
                ]
            },
            {
                'Notification': {
                    'NotificationType': 'FORECASTED',
                    'ComparisonOperator': 'GREATER_THAN',
                    'Threshold': 100.0,
                    'ThresholdType': 'PERCENTAGE'
                },
                'Subscribers': [
                    {'SubscriptionType': 'EMAIL', 'Address': email}
                    for email in notification_emails
                ]
            }
        ]
    )
```

### Cost Monitoring

**7. Anomaly Detection**

Detect cost anomalies:

```python
def detect_cost_anomalies(service: str) -> list[dict]:
    """Detect anomalies in service costs."""
    
    ce = boto3.client('ce')
    
    # Get daily costs for past 90 days
    response = ce.get_cost_and_usage(
        TimePeriod={
            'Start': (datetime.now() - timedelta(days=90)).strftime('%Y-%m-%d'),
            'End': datetime.now().strftime('%Y-%m-%d')
        },
        Granularity='DAILY',
        Metrics=['BlendedCost'],
        Filter={
            'Service': {'Values': [service]}
        }
    )
    
    # Calculate statistics
    daily_costs = [
        float(dp['Total']['BlendedCost']['Amount'])
        for dp in response['ResultsByTime']
    ]
    
    mean_cost = sum(daily_costs) / len(daily_costs)
    std_dev = (sum((x - mean_cost) ** 2 for x in daily_costs) / len(daily_costs)) ** 0.5
    
    # Detect anomalies (2 standard deviations)
    anomalies = []
    for i, cost in enumerate(daily_costs):
        if abs(cost - mean_cost) > 2 * std_dev:
            anomalies.append({
                'date': response['ResultsByTime'][i]['TimePeriod']['Start'],
                'cost': cost,
                'expected': mean_cost,
                'deviation': ((cost - mean_cost) / mean_cost) * 100
            })
    
    return anomalies
```

## Integration with Other Skills

**Infrastructure-as-Code Skill:**
- Implement cost-optimized IaC
- Add cost tags to resources

**Observability Skill:**
- Monitor cost metrics
- Set up cost dashboards

**CI-CD Skill:**
- Implement cost checks in pipelines
- Prevent expensive deployments

## Cloud Costs Triggers

User phrases that suggest cloud cost work:
- "reduce aws costs"
- "cloud cost optimization"
- "budget alert"
- "resource tagging"
- "cost monitoring"
- "right sizing"
- "savings plan"
- "cost allocation"

## DO NOT

- Optimize costs without understanding requirements
- Skip resource tagging
- Ignore budget alerts
- Forget about data transfer costs
- Over-provision resources
- Skip regular cost reviews
- Ignore regional price differences

---
name: azure-cost-analyzer
description: Query, understand, and reduce Azure spending — cost analysis, budget alerts, right-sizing, reserved instances, and chargeback reporting.
---

# Azure Cost Analyzer

Query, understand, and reduce Azure spending — cost analysis, budget alerts, right-sizing, reserved instances, and chargeback reporting.

## Trigger

Use this skill when the user asks to:
- Understand what is driving their Azure bill
- Break down costs by resource group, tag, service, or subscription
- Create budgets and spending alerts
- Find idle, orphaned, or over-provisioned resources
- Evaluate Reserved Instances or Savings Plans vs pay-as-you-go
- Set up cost exports or chargeback/showback reports
- Query cost data with KQL or the Cost Management API
- Act on Azure Advisor cost recommendations
- Schedule resource shutdown for dev/test environments

## Instructions

### Before advising

Ask (or infer) the following if not already provided:

1. **Scope** — subscription, resource group, management group, or billing account?
2. **Time period** — last 30 days, last quarter, a specific month?
3. **Goal** — understand a spike, reduce ongoing spend, forecast, or build a report?
4. **Tagging maturity** — are resources tagged consistently (owner, environment, workload)?
5. **Commitment level** — is the team open to Reserved Instances or Savings Plans?

### Cost analysis approach

Always start with the broadest view, then drill down:

```
1. Total spend this period vs last period → identify if there is a trend
2. Spend by service → which Azure service category is largest?
3. Spend by resource group → which workload / team is responsible?
4. Spend by tag (environment, team, workload) → chargeback view
5. Top resources by cost → which individual resources cost the most?
6. Daily spend timeline → is there a spike on a specific date?
```

### Cost Management CLI

```bash
# Monthly cost for a subscription (current month)
az costmanagement query \
  --scope "/subscriptions/{subId}" \
  --type ActualCost \
  --dataset-granularity Monthly \
  --dataset-aggregation '{"totalCost":{"name":"Cost","function":"Sum"}}' \
  --timeframe MonthToDate

# Cost by resource group (last 30 days)
az costmanagement query \
  --scope "/subscriptions/{subId}" \
  --type ActualCost \
  --dataset-granularity None \
  --dataset-aggregation '{"totalCost":{"name":"Cost","function":"Sum"}}' \
  --dataset-grouping '[{"type":"Dimension","name":"ResourceGroupName"}]' \
  --timeframe Last30Days \
  --query "properties.rows" \
  --output table

# Cost by service (last 30 days)
az costmanagement query \
  --scope "/subscriptions/{subId}" \
  --type ActualCost \
  --dataset-granularity None \
  --dataset-aggregation '{"totalCost":{"name":"Cost","function":"Sum"}}' \
  --dataset-grouping '[{"type":"Dimension","name":"ServiceName"}]' \
  --timeframe Last30Days \
  --query "properties.rows" \
  --output table

# Cost by tag value (e.g. by 'environment' tag)
az costmanagement query \
  --scope "/subscriptions/{subId}" \
  --type ActualCost \
  --dataset-granularity None \
  --dataset-aggregation '{"totalCost":{"name":"Cost","function":"Sum"}}' \
  --dataset-grouping '[{"type":"TagKey","name":"environment"}]' \
  --timeframe Last30Days

# Daily spend trend (last 30 days)
az costmanagement query \
  --scope "/subscriptions/{subId}" \
  --type ActualCost \
  --dataset-granularity Daily \
  --dataset-aggregation '{"totalCost":{"name":"Cost","function":"Sum"}}' \
  --timeframe Last30Days
```

### Budgets

Always create budgets at both subscription and resource-group level for critical workloads.

```bash
# Monthly subscription budget with email alert at 80% and 100%
az consumption budget create \
  --budget-name "prod-monthly-budget" \
  --scope "/subscriptions/{subId}" \
  --amount 5000 \
  --time-grain Monthly \
  --time-period-start "2026-05-01" \
  --time-period-end  "2027-04-30" \
  --notifications '{
    "Actual_GreaterThan_80_Percent": {
      "enabled": true,
      "operator": "GreaterThan",
      "threshold": 80,
      "thresholdType": "Actual",
      "contactEmails": ["finance@contoso.com","platform@contoso.com"],
      "contactRoles": ["Owner","Contributor"]
    },
    "Actual_GreaterThan_100_Percent": {
      "enabled": true,
      "operator": "GreaterThan",
      "threshold": 100,
      "thresholdType": "Actual",
      "contactEmails": ["finance@contoso.com"]
    },
    "Forecast_GreaterThan_110_Percent": {
      "enabled": true,
      "operator": "GreaterThan",
      "threshold": 110,
      "thresholdType": "Forecasted",
      "contactEmails": ["platform@contoso.com"]
    }
  }'

# Resource group budget
az consumption budget create \
  --budget-name "rg-myapp-prod-budget" \
  --scope "/subscriptions/{subId}/resourceGroups/rg-myapp-prod" \
  --amount 800 \
  --time-grain Monthly \
  --time-period-start "2026-05-01" \
  --time-period-end  "2027-04-30" \
  --notifications '{
    "Actual_GreaterThan_90_Percent": {
      "enabled": true,
      "operator": "GreaterThan",
      "threshold": 90,
      "thresholdType": "Actual",
      "contactEmails": ["team@contoso.com"]
    }
  }'

# List budgets
az consumption budget list --scope "/subscriptions/{subId}" \
  --query "[].{Name:name, Amount:amount, CurrentSpend:currentSpend.amount, Unit:currentSpend.unit}"

# Show current spend vs budget
az consumption budget show \
  --budget-name "prod-monthly-budget" \
  --scope "/subscriptions/{subId}" \
  --query "{Budget:amount, Spent:currentSpend.amount, Forecast:forecastSpend.amount}"
```

### Azure Advisor cost recommendations

```bash
# List all cost recommendations
az advisor recommendation list \
  --category Cost \
  --query "[].{Impact:impact, Problem:shortDescription.problem, Resource:resourceMetadata.resourceId}" \
  --output table

# Filter to high-impact only
az advisor recommendation list \
  --category Cost \
  --query "[?impact=='High'].{Problem:shortDescription.problem, Resource:resourceMetadata.resourceId, Savings:extendedProperties.annualSavingsAmount}" \
  --output table

# Get recommendation details (including potential savings)
az advisor recommendation show \
  --ids "/subscriptions/{subId}/providers/Microsoft.Advisor/recommendations/{recId}"

# Snooze a recommendation (7 days)
az advisor recommendation disable \
  --ids "/subscriptions/{subId}/providers/Microsoft.Advisor/recommendations/{recId}" \
  --days 7
```

Key Advisor cost recommendations to act on first (highest ROI):
1. **Right-size or shut down underutilized VMs** — CPU < 5% avg over 14 days
2. **Delete unattached managed disks** — disks not attached to any VM
3. **Buy Reserved Instances** — for workloads with > 6 months of consistent usage
4. **Delete or resize idle App Service Plans** — plans with no apps or always-low CPU
5. **Resize or consolidate underutilized SQL databases**
6. **Remove unassociated public IP addresses**
7. **Use Azure Hybrid Benefit** — for Windows Server or SQL Server on VMs

### Orphaned resource identification

```bash
# Unattached managed disks (not attached to a VM)
az disk list --query "[?diskState=='Unattached'].{Name:name, RG:resourceGroup, Size:diskSizeGb, SKU:sku.name}" --output table

# Unassociated public IP addresses
az network public-ip list \
  --query "[?ipConfiguration==null].{Name:name, RG:resourceGroup, SKU:sku.name}" --output table

# Unused network interfaces (not attached to a VM)
az network nic list \
  --query "[?virtualMachine==null].{Name:name, RG:resourceGroup}" --output table

# Empty resource groups
az group list --query "[].name" -o tsv | while read rg; do
  COUNT=$(az resource list --resource-group "$rg" --query "length(@)" -o tsv 2>/dev/null)
  [ "$COUNT" = "0" ] && echo "Empty: $rg"
done

# Unused load balancers (no backend pool members)
az network lb list \
  --query "[?backendAddressPools[0].backendIPConfigurations==null].{Name:name, RG:resourceGroup}" \
  --output table

# App Service plans with no apps
az appservice plan list \
  --query "[?numberOfSites==\`0\`].{Name:name, RG:resourceGroup, SKU:sku.name, Cost:'check pricing'}" \
  --output table

# Snapshots older than 30 days
az snapshot list \
  --query "[?timeCreated<'$(date -u -d '-30 days' +%Y-%m-%dT%H:%M:%SZ)'].{Name:name, RG:resourceGroup, SizeGB:diskSizeGb, Created:timeCreated}" \
  --output table
```

### Reserved Instances and Savings Plans guidance

**When to recommend RIs:**
- Resource has been running > 6 months with consistent usage
- VM family, region, and size are unlikely to change for 1–3 years
- Estimated savings: 30–60% vs pay-as-you-go (1-year); 60–72% (3-year)

**When to recommend Savings Plans:**
- Mixed or changing VM families / regions
- Want flexibility — Savings Plans apply across VM families
- Estimated savings: ~15–17% less than equivalent RI but more flexible

**Comparison table:**

| | Pay-as-you-go | Savings Plan (1yr) | Reserved Instance (1yr) | Reserved Instance (3yr) |
|--|---|---|---|---|
| Commitment | None | Hourly spend | VM type + region | VM type + region |
| Flexibility | Max | High | Medium | Medium |
| Savings | 0% | ~35% | ~40% | ~60% |
| Best for | Spiky / short-lived | Variable workloads | Stable workloads | Very stable, long-term |

```bash
# View RI recommendations from Advisor
az advisor recommendation list --category Cost \
  --query "[?contains(shortDescription.problem,'reserved')].{Problem:shortDescription.problem, Resource:resourceMetadata.resourceId}"

# List existing reservations
az reservations reservation list-all \
  --query "[].{Name:displayName, SKU:sku.name, Scope:properties.appliedScopeType, Expiry:properties.expiryDate, Utilisation:properties.utilization.trend}" \
  --output table

# Check reservation utilization (under-utilized reservations = wasted spend)
az reservations reservation list-all \
  --query "[?properties.utilization.trend=='DecreasingUtilization'].{Name:displayName, SKU:sku.name}"
```

### Dev/test cost control

```bash
# List VMs that should be shut down outside business hours
az vm list \
  --query "[?tags.environment=='dev' || tags.environment=='test'].{Name:name, RG:resourceGroup, State:powerState}" \
  --show-details --output table

# Auto-shutdown a VM at 7pm UTC daily
az vm auto-shutdown \
  --resource-group myRG --name myVM \
  --time 1900 \
  --email "owner@contoso.com"

# Start/stop all VMs in a resource group
az vm list --resource-group rg-dev \
  --query "[].name" -o tsv | xargs -I {} az vm deallocate --resource-group rg-dev --name {} --no-wait

# Use Azure DevTest Labs pricing (dev SKUs — significant discount)
# Dev/Test subscription pricing applies to Visual Studio subscribers
# Enables B-series and specific VM sizes at dev/test rates
```

### Cost export for external reporting

```bash
# Create a monthly cost export to Storage
az costmanagement export create \
  --name "monthly-cost-export" \
  --scope "/subscriptions/{subId}" \
  --type ActualCost \
  --dataset-type AmortizedCost \
  --recurrence Monthly \
  --recurrence-period from="2026-05-01" to="2027-04-30" \
  --schedule-status Active \
  --storage-account-id "/subscriptions/{subId}/resourceGroups/rg-finops/providers/Microsoft.Storage/storageAccounts/stcostexport" \
  --storage-container "cost-exports" \
  --storage-directory "monthly"

# List exports
az costmanagement export list --scope "/subscriptions/{subId}"

# Trigger an export manually (don't wait for schedule)
az costmanagement export run \
  --name "monthly-cost-export" \
  --scope "/subscriptions/{subId}"
```

### Tagging for cost allocation

Without consistent tags, cost attribution is impossible. Before any reporting work, assess and fix tag coverage:

```bash
# Resources missing the 'costCenter' tag (Resource Graph)
az graph query -q "
Resources
| where isnull(tags.costCenter) or tags.costCenter == ''
| project name, type, resourceGroup, subscriptionId
| summarize UntaggedCount=count() by resourceGroup
| order by UntaggedCount desc"

# Tag a resource group and all its resources
az group update --name myRG --tags costCenter=CC-1234 environment=prod team=platform
az resource tag --tags costCenter=CC-1234 \
  --ids $(az resource list --resource-group myRG --query "[].id" -o tsv)
```

Minimum required tags for cost allocation:

| Tag | Purpose |
|-----|---------|
| `costCenter` | Finance chargeback code |
| `environment` | dev / staging / prod (drives budget grouping) |
| `team` | Owning team (showback reports) |
| `workload` | Application / service name |

### Interpreting a cost spike

When the user reports an unexpected bill increase:

1. **Narrow the time window** — find the day the spike started (daily granularity)
2. **Identify the service** — group by `ServiceName` to find the top mover
3. **Identify the resource** — group by `ResourceId` within that service
4. **Check deployment history** — `az monitor activity-log list --start-time <spike-date>` for ARM operations around that date
5. **Check autoscale events** — did an autoscale rule fire and not scale back in?
6. **Check data egress** — networking costs spike with unexpected egress; check `az network watcher` or Traffic Analytics
7. **Check storage transactions** — high transaction rates on storage can cause unexpected costs

```bash
# Activity log around a cost spike date
az monitor activity-log list \
  --start-time "2026-05-01T00:00:00Z" \
  --end-time   "2026-05-02T00:00:00Z" \
  --resource-group myRG \
  --query "[?operationName.value!='Microsoft.Insights/AutoscaleSettings/providers/Microsoft.Insights/diagnosticSettings/write'].{Time:eventTimestamp, Operation:operationName.value, Status:status.value, Caller:caller}" \
  --output table
```

## References

- [Cost Management CLI & API cheatsheet](./references/cost-management-cheatsheet.md)
- [Optimization patterns: right-sizing, RIs, dev/test](./references/optimization-patterns.md)
- [KQL queries for cost and usage analysis](./references/cost-kql-queries.md)
- Official docs: https://learn.microsoft.com/en-us/azure/cost-management-billing/

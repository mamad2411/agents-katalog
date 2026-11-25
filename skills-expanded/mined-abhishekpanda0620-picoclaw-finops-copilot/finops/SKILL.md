---
name: finops
description: AWS cost analysis and cloud optimization using AWS CLI.
metadata: {"nanobot":{"emoji":"💰","requires":{"bins":["aws"]}}}
---

# FinOps – AWS Cost Analysis

This skill handles AWS cost analysis, usage review, and optimization insights.

Use this skill when the user asks about:
- AWS cost
- Cost Explorer
- Cloud spending
- Service cost breakdown
- Idle resources
- Optimization suggestions

Always prefer read-only AWS CLI queries.
Never modify or delete resources without explicit user approval.

---

## Cost Summary (Service Breakdown)

When user provides relative time expressions such as:

- last X days
- yesterday
- today
- this month
- last month

The agent must:

- Resolve dates using the system date command.

- Convert to explicit YYYY-MM-DD format.

- Use resolved values in the AWS CLI command.

- Never pass natural language into --time-period.

Example for "last 2 days":
Step 1 – Resolve start date:
```bash
date -d "2 days ago" +%Y-%m-%d
```
Step 2 – Resolve end date:
```bash
date +%Y-%m-%d
```
Step 3 – Use returned values in AWS command:
```bash
aws ce get-cost-and-usage \
  --time-period Start=RESOLVED_START,End=RESOLVED_END \
  ...
```
This execution order is mandatory.

Important:

- End date must be today (exclusive).

- Do not calculate dates using LLM reasoning.

- Always resolve using system date command.


Use AWS Cost Explorer:

```bash
aws ce get-cost-and-usage \
  --time-period Start=<START>,End=<END> \
  --granularity MONTHLY \
  --metrics "BlendedCost" \
  --group-by Type=DIMENSION,Key=SERVICE \
  --query "ResultsByTime[0].Groups[].{Service:Keys[0],Cost:Metrics.BlendedCost.Amount}" \
  --output json
```


After retrieving results:

- Aggregate total cost across all services.

- Sum service-level costs.

- Sort services by total cost descending.

- Return only top 5 services.

- Format results using Slack-friendly formatting.


- Instead of tables, use this structure:

💰 AWS Cost Analysis (Feb 20–27, 2026)

Total Cost: $0.00

Top Services:
• EC2 - Other → $0.0000000008
• AWS Glue → $0.00
• AWS KMS → $0.00
• Amazon S3 → $0.00
• CloudWatch → $0.00



If total cost is zero:

- Clearly state: "Your AWS usage is minimal."

- Suggest checking for unused EC2 instances or EBS volumes.

- Never return raw JSON directly to Slack.






---


## Monthly Cost Comparison

When the user asks to compare this month with last month:

Never use shell substitution $(...) in exec commands.
Use simple date -d "-1 month" patterns only.
If a command is blocked, respond with a helpful message.


1. Resolve dates using system date:

Current month start:
`date +%Y-%m-01`

Current date (end, exclusive if needed):
`date +%Y-%m-%d`

Previous month start:
`date -d "-1 month" +%Y-%m-01`
Previous month end:
`date -d "-$(date +%d) days" +%Y-%m-%d`

2. Fetch AWS Cost Explorer data for BOTH periods using DAILY granularity.

Use:

aws ce get-cost-and-usage 
--time-period Start=<START>,End=<END> 
--granularity DAILY 
--metrics "BlendedCost" 
--group-by Type=DIMENSION,Key=SERVICE 
--query "ResultsByTime[].Groups[].{Service:Keys,Cost:Metrics.BlendedCost.Amount}" 
--output json

3. Aggregate total cost for each month.

4. Calculate:

* Absolute difference
* Percentage change

5. Slack Output Format:

📊 AWS Monthly Cost Comparison

Current Month(<MONTH>): $X
Previous Month(<MONTH>): $Y

Change: ±$Z (±%)

* Use ⚠️ if increase > 20%
* Use ✅ if stable or decreased
* Never return raw JSON.

Keep output concise and Slack-friendly.
Avoid long paragraphs or markdown tables.


---














## Idle EBS Detection

Use:

```bash
aws ec2 describe-volumes \
  --filters Name=status,Values=available \
  --query "Volumes[].{VolumeId:VolumeId,Size:Size}" \
  --output json
```

After retrieving volumes:

- Estimate monthly cost using ~ $0.08 per GB.

- List top 5 largest unattached volumes.

- Provide estimated monthly waste.

- Ask for confirmation before deletion.


Never automatically delete volumes.
Always ask for user confirmation.



Format Slack output as:

- Status line with emoji (✅ or ⚠️)

- Monthly waste estimate

- Short explanation (2–3 lines max)

- Offer next related optimization checks
- Avoid long paragraphs and Markdown headings.

if none found:
- ✅ No EBS waste detected.

---

## Unused Elastic IPs (EIPs) Detection

When the user asks about idle Elastic IPs or unused EIPs.

Use:

```bash
aws ec2 describe-addresses \
  --query 'Addresses[?NetworkInterfaceId==null].{PublicIp:PublicIp,AllocationId:AllocationId}' \
  --output json
```

After retrieving EIPs:
- Calculate monthly waste. AWS charges roughly $3.60/month ($0.005/hour) per unattached EIP.
- Ask for confirmation before release.

Format Slack output dynamically. Do not use raw JSON. Example structure:

⚠️ *Unused Elastic IPs Detected* 

Estimated Monthly Waste: `$7.20`

• `198.51.100.14` (Allocation ID: eipalloc-0abcd)
• `203.0.113.55` (Allocation ID: eipalloc-0wxyz)

*Action:* Would you like me to release these IPs?

---

## Idle Load Balancers Detection

When the user asks about unused load balancers, ALBs, or ELBs without traffic.
(Note: ELBv2 covers both Application and Network Load Balancers).

Use:

```bash
aws elbv2 describe-load-balancers \
  --query 'LoadBalancers[].{Name:LoadBalancerName,ARN:LoadBalancerArn}' \
  --output json
```

Then, for each load balancer ARN, check if it has target groups with healthy targets. 
*LLM Instruction: If a load balancer has 0 active targets over an extended period, treat it as idle.*

Format Slack output dynamically. Do not use raw JSON. Example structure:

⚠️ *Idle Load Balancers Detected* 

Estimated Minimum Monthly Waste: `$33.00+`

• `web-frontend-alb` (0 active targets)
• `internal-api-elb` (0 active targets)

*Action:* Please review these balancers in the AWS console.

---

## Top S3 Storage Costs

When the user asks about the largest S3 buckets or S3 storage costs.

Use AWS Cost Explorer (since scanning actual bucket sizes via `aws s3 ls` iteratively is slow).

```bash
aws ce get-cost-and-usage \
  --time-period Start=$(date -d "-7 days" +%Y-%m-%d),End=$(date +%Y-%m-%d) \
  --granularity MONTHLY \
  --metrics "BlendedCost" \
  --filter '{"Dimensions": {"Key": "SERVICE", "Values": ["Amazon Simple Storage Service"]}}' \
  --group-by Type=TAG,Key=aws:createdBy \
  --query "ResultsByTime[0].Groups[].{Tag:Keys[0],Cost:Metrics.BlendedCost.Amount}" \
  --output json
```

*(Note for the AI: Modify the `--group-by Type=TAG,Key=YOUR_BUCKET_TAG` if standard tagging is used in the environment, otherwise rely on the base Cost Explorer query to get the total S3 spend over the last week).*

Format Slack output dynamically. Do not use raw JSON. Example structure:

💰 *S3 Storage Costs (Last 7 Days)* 

Total S3 Spend: `$145.20`

Top Allocations:
• `production-assets` → `$85.00`
• `database-backups` → `$40.20`
• `dev-logs` → `$20.00`

*Suggestion:* Consider enabling S3 Intelligent-Tiering if costs remain high.

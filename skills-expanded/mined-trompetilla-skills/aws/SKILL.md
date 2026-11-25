---
name: AWS
description: Deploy, monitor, and manage AWS services with battle-tested patterns.
metadata: {"clawdbot":{"emoji":"☁️","requires":{"anyBins":["aws"]},"os":["linux","darwin","win32"]}}
---

# AWS Production Rules

## Cost Traps
- NAT Gateway charges per GB processed — use VPC endpoints for S3/DynamoDB traffic instead of routing through NAT
- EBS snapshots accumulate silently from automated backups — audit and delete snapshots older than retention policy regularly
- CloudWatch Logs retention defaults to forever — set `put-retention-policy` on every log group or face surprise bills
- Data transfer between regions is charged both ways — keep resources in same region unless you have a specific reason not to
- Stopped EC2 instances still pay for attached EBS volumes and Elastic IPs — release what you're not using

## Security Rules
- S3 bucket policies override ACLs but don't show in the ACL console tab — always check both `get-bucket-policy` and `get-bucket-acl`
- IAM policy evaluation: explicit Deny always wins, resource-based and identity-based policies combine — use `simulate-principal-policy` to test before deploying
- Security Groups are stateful (return traffic auto-allowed), NACLs are stateless — outbound NACL rules must explicitly allow ephemeral ports 1024-65535 for responses
- Default VPC security group allows all outbound traffic — create custom security groups with least-privilege outbound rules
- S3 presigned URLs inherit the permissions of the IAM user who created them — if the user's permissions change, existing URLs break

## Performance
- gp2 EBS volumes have limited burst credits that deplete under sustained load — use gp3 for consistent baseline IOPS without burst dependency
- Lambda reuses containers but each invocation may open new DB connections — use RDS Proxy to pool connections and prevent "too many connections" errors
- ALB health checks are per-target per-AZ — with 3 AZs and 5 targets, each target gets 3 health check streams. Account for this in health check intervals
- DynamoDB auto-scaling reacts to consumed capacity, not throttled requests — pre-warm capacity before expected traffic spikes
- CloudFront TTL of 0 still caches if origin sends Cache-Control headers — explicitly set `no-store` if you truly want no caching

## Monitoring
- CloudWatch metric retention: 1-minute data kept 15 days, 5-minute for 63 days, 1-hour for 455 days — critical alerts on high-resolution metrics disappear after 2 weeks
- Lambda "Duration" includes cold start initialization — monitor `InitDuration` separately to distinguish cold starts from actual execution time
- CloudTrail logs API calls but not data events (S3 object access, Lambda invocations) by default — enable data events explicitly for security auditing
- ALB 5xx errors can be ALB-generated (502/503/504) or target-generated — check `HTTPCode_ELB_5XX_Count` vs `HTTPCode_Target_5XX_Count` separately

## Infrastructure as Code
- CloudFormation update policies are ignored during resource replacement — deletion protection only works for in-place updates, not replace operations
- Terraform state lock table (DynamoDB) needs point-in-time recovery enabled — losing state lock = potential concurrent modifications
- Auto Scaling cool-down periods stack with target tracking policies — default 300s scale-in delay causes slow response to load drops. Tune per workload
- Never hardcode AMI IDs — use SSM parameter store paths (`/aws/service/ami-amazon-linux-latest/...`) that always resolve to current images

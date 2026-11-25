---
name: idle
description: Finds resources that cost money and do nothing, with proof - NAT gateways with zero bytes and zero connection attempts over 180 days, unattached EBS volumes, loose Elastic IPs, load balancers without healthy targets, instances under 10% CPU for 14 days, ECR repositories without lifecycle policy, CloudWatch log groups without retention. Use when the user asks "is this NAT idle", "what are we paying for that nothing uses", "orphan volumes", "unused IPs", or wants quick hygiene wins. Read-only; it recommends deletions, never performs them.
argument-hint: "[--profile member] [--region us-east-1]"
---

# Idle resources, with proof

Profiles from the configuration (`${user_config.member_profiles}`, and the payer too, which often
holds forgotten networking) and the region (`${user_config.region}`), unless given as arguments.
Run for every account; idle resources live where nobody looks.

Standard of proof, before calling anything idle: metrics with datapoints **present at zero** for
the window (not missing); the same query against an active resource returns data (control);
the topology shows nothing that could use it. Missing data is reported as "unknown", never as
idle.

```bash
# NAT gateways: three independent evidences (CloudWatch 180d, route tables → subnets → ENIs, consumers)
python3 -I "${CLAUDE_PLUGIN_ROOT}/scripts/nat_idle_check.py" --profile <p> --region <r> --days 180

# volumes, addresses, load balancers
aws ec2 describe-volumes --profile <p> --region <r> --filters Name=status,Values=available --query 'Volumes[].{id:VolumeId,gb:Size,type:VolumeType,created:CreateTime}' --output table
aws ec2 describe-addresses --profile <p> --region <r> --query 'Addresses[?AssociationId==null].{ip:PublicIp,alloc:AllocationId}' --output table
for lb in $(aws elbv2 describe-load-balancers --profile <p> --region <r> --query 'LoadBalancers[].LoadBalancerArn' --output text); do
  for tg in $(aws elbv2 describe-target-groups --profile <p> --region <r> --load-balancer-arn $lb --query 'TargetGroups[].TargetGroupArn' --output text); do
    aws elbv2 describe-target-health --profile <p> --region <r> --target-group-arn $tg --query 'length(TargetHealthDescriptions)' --output text
  done
done

# instances: 14-day average CPU per instance (hour-of-day table; look at the avg)
python3 -I "${CLAUDE_PLUGIN_ROOT}/scripts/cw_hod.py" --profile <p> --region <r> '[{"ns":"AWS/EC2","metric":"CPUUtilization","dims":{"InstanceId":"<id>"},"label":"<name> CPU %"}]'

# registries and logs that grow forever
aws ecr describe-repositories --profile <p> --region <r> --query 'repositories[].repositoryName' --output text | tr '\t' '\n' | while read repo; do aws ecr get-lifecycle-policy --profile <p> --region <r> --repository-name "$repo" >/dev/null 2>&1 || echo "no lifecycle: $repo"; done
aws logs describe-log-groups --profile <p> --region <r> --query 'logGroups[?retentionInDays==null].[logGroupName,storedBytes]' --output table
```

Answer with one table: resource, account, evidence (the numbers), monthly cost (NAT USD 0.045/h ≈
33/month; EBS gp3 USD 0.08/GB-month; EIP USD 3.65/month; ALB/NLB ≈ USD 16/month plus LCU;
instance by on-demand price; ECR USD 0.10/GB-month; logs USD 0.03/GB-month), verdict (**idle
proven** / **likely idle, unproven** / **in use**), and the production impact of removing it
(`none` for volumes not attached, NAT with zero traffic, loose EIPs; `window` for anything that
still has a route or a DNS name pointing at it).

Before recommending a deletion, always say what to export first (`describe-*` output to JSON, a
snapshot for volumes) and what else to clean (blackhole routes after a NAT, DNS records after a
load balancer). Never run the deletion; the guard would deny it anyway.

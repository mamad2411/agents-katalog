---
name: aws-imdsv2-enforcement
description: >
  Enforce EC2 Instance Metadata Service v2 (IMDSv2) on owned accounts: hop limit,
  http tokens required, AMI/launch template defaults, Systems Manager/fleet remediation,
  and application compatibility. Use when preventing SSRF credential theft via IMDS —
  not for attacking metadata services on instances you do not own.
---

# AWS IMDSv2 Enforcement

## Scope And Authorization

- **In scope:** EC2 instances, launch templates, Auto Scaling, and org policies in accounts you operate.
- **Out of scope:** Querying IMDS on third-party infrastructure.
- IMDSv1 is a classic SSRF→credential theft path; treat enforcement as high priority for Internet-facing apps.
- Some old SDKs/agents need updates before requiring tokens.
- Pair with app SSRF defenses; `code-quality-standards` for automation.

## When To Use

- Setting `HttpTokens=required` on instances/launch templates.
- Lowering `HttpPutResponseHopLimit` to 1 for non-container host needs (careful with containers).
- Finding remaining IMDSv1-capable instances at scale.
- Using SCPs/Config rules to prevent regression.
- Fixing broken workloads after enforcement.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| SSRF application testing | `ssrf-server-side-request-forgery` (authorized) |
| ECS/EKS task/pod identity | `aws-ecs-task-security` / `aws-eks-pod-identity` |
| IAM least privilege post-theft | `aws-iam-least-privilege` |
| GuardDuty findings response | GuardDuty skills |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Setting | Meaning |
| --- | --- |
| `HttpTokens=optional` | IMDSv1 and v2 both work (weak) |
| `HttpTokens=required` | IMDSv2 only (PUT token then GET) |
| `HttpPutResponseHopLimit` | TTL for metadata packets; 1 blocks most container-to-IMDS unless configured |
| `HttpEndpoint` | enable/disable IMDS entirely |
| Instance tags / account defaults | EC2 serial console / IMDS defaults per current account options |

## Why IMDSv2

```text
IMDSv1: SSRF GET http://169.254.169.254/.../iam/security-credentials/...
IMDSv2: requires session token via PUT with special headers — breaks many blind SSRFs
```

## Workflow

### 1. Confirm scope and success criteria

1. Record accounts, fleets (ASG, EKS nodes, bastions), critical apps.
2. Success: all prod instances `HttpTokens=required`; launch templates default required; Config noncompliant=0; apps healthy.
3. Plan hop limit separately for container hosts (EKS often needs hop limit 2).

### 2. Inventory IMDS settings

```bash
aws ec2 describe-instances --query "Reservations[].Instances[].{Id:InstanceId,Name:Tags[?Key=='Name']|[0].Value,HttpTokens:MetadataOptions.HttpTokens,Hop:MetadataOptions.HttpPutResponseHopLimit,Endpoint:MetadataOptions.HttpEndpoint}" --output table
aws ec2 describe-launch-templates
aws ec2 describe-launch-template-versions --launch-template-id "$LT" --versions '$Latest'
```

1. Flag `optional` or missing options (defaults may be optional).
2. Check Auto Scaling launch templates vs launch configs (migrate off launch configs if needed).
3. Config rule `ec2-imdsv2-check` status if present.

### 3. Baseline

1. Export instance ID list with current options.
2. Identify old AWS CLI/SDK/agents (CloudWatch agent, custom scripts using curl without token).
3. Canary instance per AMI family for enforcement test.

### 4. Enforce IMDSv2

**Per instance:**

```bash
aws ec2 modify-instance-metadata-options \
  --instance-id i-0123456789abcdef0 \
  --http-tokens required \
  --http-endpoint enabled \
  --http-put-response-hop-limit 1
```

**Launch template default:**

```bash
aws ec2 create-launch-template-version \
  --launch-template-id "$LT" \
  --source-version '$Latest' \
  --launch-template-data '{
    "MetadataOptions": {
      "HttpTokens": "required",
      "HttpPutResponseHopLimit": 1,
      "HttpEndpoint": "enabled"
    }
  }'
```

**Containers / EKS nodes:** hop limit **2** commonly required so pods can reach IMDS when using host networking patterns — prefer IRSA/Pod Identity and avoid pod IMDS access; if pods should not use IMDS, combine hop limit 1 + iptables/IMDS blockers + pod identity.

**Org guardrails**

1. Config conformance pack rule for IMDSv2.
2. SCP or declarative policy / EC2 defaults requiring IMDSv2 when available in your governance model.
3. Packer/AMI pipelines bake metadata options into launch templates only (instance user data cannot weaken if LT enforces at launch).

**App fix pattern (curl IMDSv2):**

```bash
TOKEN=$(curl -sS -X PUT "http://169.254.169.254/latest/api/token" -H "X-aws-ec2-metadata-token-ttl-seconds: 21600")
curl -sS -H "X-aws-ec2-metadata-token: $TOKEN" http://169.254.169.254/latest/meta-data/
```

Prefer AWS SDKs that support IMDSv2 by default.

### 5. Verify with evidence

```bash
aws ec2 describe-instances --instance-ids i-... --query "Reservations[].Instances[].MetadataOptions"
# On instance:
curl -sS -o /dev/null -w "%{http_code}\n" http://169.254.169.254/latest/meta-data/
# Expect 401 without token when required
```

1. ASG instance refresh completes healthy.
2. No spike in instance role credential errors in apps.
3. Config compliance for IMDS rule green.

### 6. Observe and harden

1. Continuous inventory job for `HttpTokens!=required`.
2. Alert on new launch templates missing metadata options.
3. Reduce instance role privileges (defense in depth if IMDS ever reached).

### 7. Hand off

1. AMI/LT standards doc with hop limit matrix (host vs container).
2. Exception process for legacy with expiry.
3. Link SSRF app hardening for defense in depth.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Tokens | required everywhere prod | optional “for compatibility” forever |
| Hop limit | 1 default; 2 only if justified | 64 unnecessary |
| Nodes | Pod Identity + block pod IMDS | all pods can read node role |
| Guardrails | Config + LT defaults | one-time manual fix |
| Legacy | updated SDK/agent | custom curl v1 scripts remain |
| Roles | least privilege still | admin instance profiles |

## Output Checklist

- [ ] Fleet inventory of MetadataOptions complete
- [ ] Launch templates/ASG updated
- [ ] Instances modified or recycled to required
- [ ] Hop limit strategy documented (esp. containers)
- [ ] App/agent compatibility verified
- [ ] Config/SCP prevention of regression
- [ ] Evidence: v1 GET fails, v2 works
- [ ] Exceptions ticketed with expiry
- [ ] Instance role privileges reviewed

## Rules

- Owned instances only.
- Prefer IMDSv2 required as org baseline.
- Do not leave Internet apps on IMDSv1.
- Combine with least-privilege instance roles.
- Focus on IMDS enforcement; app SSRF testing and workload identity in neighbor skills.

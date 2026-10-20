---
name: aws-msk-iam-auth
description: >
  Amazon MSK IAM access control for owned clusters: enabling IAM auth, client
  properties (SASL/OAUTHBEARER AWS_MSK_IAM), cluster policies, topic ACLs vs IAM,
  and least-privilege producers/consumers. Use when securing Kafka clients to MSK —
  not for accessing MSK clusters outside authorization.
---

# AWS MSK IAM Auth

## Scope And Authorization

- **In scope:** MSK provisioned/serverless clusters and IAM policies in accounts you operate.
- **Out of scope:** Connecting to third-party Kafka/MSK without permission.
- Prefer IAM auth over long-lived SCRAM passwords when clients support it.
- Combine network isolation (SG/VPC) with IAM — neither alone is enough.
- Pair with `aws-iam-least-privilege` and `code-quality-standards` for clients.

## When To Use

- Enabling `SASL/IAM` on MSK clusters.
- Configuring Java/Python clients for AWS_MSK_IAM mechanism.
- Writing IAM policies for `kafka-cluster:*` actions on cluster/topic/group ARNs.
- Migrating from SCRAM/mTLS to IAM (or dual).
- Debugging `Unauthorized` / handshake failures.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Generic Kafka ops | platform Kafka skill |
| Lambda Kafka ESM | `aws-lambda-event-source-mapping` |
| Kinesis | `aws-kinesis-on-demand` |
| Network-only hardening | VPC/SG skills |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Piece | Role |
| --- | --- |
| Cluster auth setting | IAM, SCRAM, mTLS combinations |
| Client | SASL_SSL + OAUTHBEARER / AWS_MSK_IAM callback handlers |
| IAM actions | connect, write/read topic data, alter, describe, consumer groups |
| Resource ARNs | cluster, topic, group patterns |
| SG | client → broker ports 9098 (IAM) typical |

## Example IAM Policy Snippet

```json
{
  "Effect": "Allow",
  "Action": [
    "kafka-cluster:Connect",
    "kafka-cluster:DescribeCluster"
  ],
  "Resource": "arn:aws:kafka:REGION:ACCT:cluster/my-cluster/*"
},
{
  "Effect": "Allow",
  "Action": [
    "kafka-cluster:DescribeTopic",
    "kafka-cluster:ReadData"
  ],
  "Resource": "arn:aws:kafka:REGION:ACCT:topic/my-cluster/*/orders"
},
{
  "Effect": "Allow",
  "Action": [
    "kafka-cluster:DescribeGroup",
    "kafka-cluster:AlterGroup"
  ],
  "Resource": "arn:aws:kafka:REGION:ACCT:group/my-cluster/*/orders-cg"
}
```

Adjust ARN shapes to your cluster UUID naming from `describe-cluster`.

## Workflow

### 1. Confirm scope and success criteria

1. Record cluster ARN, auth modes, clients, topics, consumer groups.
2. Success: IAM clients produce/consume; unauthorized role denied; TLS on; SG limited.
3. Downtime plan if changing client security protocol.

### 2. Inventory

```bash
aws kafka list-clusters-v2
aws kafka describe-cluster-v2 --cluster-arn "$ARN"
aws kafka get-bootstrap-brokers --cluster-arn "$ARN"
aws ec2 describe-security-groups --group-ids sg-msk
```

1. Note ports for IAM vs SCRAM vs TLS.
2. List client roles (ECS/EKS/Lambda/EC2).

### 3. Baseline

1. Export current ACL/SCRAM users if any.
2. Capture working bootstrap string for IAM (`SASL_IAM` brokers).
3. Metrics: connection error rates.

### 4. Enable and configure clients

1. Ensure cluster configuration allows IAM authentication.
2. Client properties (Java conceptual):

```properties
security.protocol=SASL_SSL
sasl.mechanism=AWS_MSK_IAM
sasl.jaas.config=software.amazon.msk.auth.iam.IAMLoginModule required;
sasl.client.callback.handler.class=software.amazon.msk.auth.iam.IAMClientCallbackHandler
```

3. Instance/pod/Lambda role: attach least-privilege kafka-cluster policy.
4. SG: allow clients on IAM bootstrap port only from app SGs.
5. Optionally keep SCRAM during migration; remove passwords after cutover.
6. For MSK Serverless, IAM is commonly primary — follow serverless-specific ARNs.

### 5. Verify with evidence

```bash
# From client host with role credentials
# kafka-console-producer/consumer with IAM jars
aws sts get-caller-identity
```

1. Produce/consume to allowed topic succeeds.
2. Different topic ARN denied.
3. Role without policy cannot Connect.
4. Packet path: no public 0.0.0.0/0 on broker ports.

### 6. Observe and harden

1. Alarms on auth failures and throttling.
2. Access reviews of kafka-cluster policies quarterly.
3. Prefer topic-scoped resources over `topic/*/*` wildcards when stable.

### 7. Hand off

1. Client library versions and property templates.
2. Role catalog per app/topic.
3. Runbook for rotating away SCRAM.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Auth | IAM roles for apps | shared SCRAM password forever |
| Policy | topic/group scoped | `kafka-cluster:*` on `*` |
| Network | SG app-only | public brokers |
| TLS | SASL_SSL | PLAINTEXT |
| Migration | dual-run then cut | flip all clients without canary |
| Secrets | no password store needed for IAM | passwords in git |

## Output Checklist

- [ ] Cluster auth modes and ports recorded
- [ ] Bootstrap brokers for IAM documented
- [ ] Client policies least privilege
- [ ] Client config templates tested
- [ ] SG isolation verified
- [ ] Deny tests for unauthorized topics/roles
- [ ] Migration/SCRAM removal plan
- [ ] Monitoring for auth failures
- [ ] `code-quality-standards` on client apps

## Rules

- Owned clusters only.
- Combine IAM + TLS + SG.
- Scope topic and group ARNs tightly.
- Do not leave broad `kafka-cluster:*` on production roles.
- Focus on MSK IAM auth; Lambda ESM and generic Kafka ops elsewhere.

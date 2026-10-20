---
name: aws-eks-pod-identity
description: >
  Amazon EKS Pod Identity vs IRSA for owned clusters: association APIs, agent
  requirements, IAM role trust, migration from IRSA OIDC provider annotations, and
  least-privilege pod credentials. Use when granting AWS API access to pods —
  not for privilege escalation on clusters you do not operate.
---

# AWS EKS Pod Identity

## Scope And Authorization

- **In scope:** EKS clusters and IAM roles in accounts you own or administer with authorization.
- **Out of scope:** Attaching roles to pods in foreign accounts/clusters; abusing stolen pod credentials.
- Pod AWS credentials are high value — scope IAM tightly and prefer separate roles per service account.
- Prefer Pod Identity or IRSA over node instance role shared by all pods.
- Pair with `code-quality-standards` for controllers/charts; general IAM with `aws-iam-least-privilege`.

## When To Use

- Choosing **EKS Pod Identity** vs **IRSA** (OIDC) for new workloads.
- Creating `eks:PodIdentityAssociation` between namespace/service account and IAM role.
- Migrating off node instance profiles for app AWS access.
- Debugging `Unable to locate credentials` or wrong account assume role in pods.
- Reviewing trust policies and `eks.amazonaws.com` / Pod Identity principals.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Node IAM / managed node groups | EKS node skill |
| Network policies / pod security | K8s security skills |
| General IAM policy authoring | `aws-iam-least-privilege` |
| ECS task roles | `aws-ecs-task-security` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Mechanism | How pods get AWS creds |
| --- | --- |
| Node role | Shared by all pods (avoid for app perms) |
| IRSA | ServiceAccount annotation + OIDC provider assume role with web identity |
| EKS Pod Identity | Cluster agent + associations API maps SA → IAM role |

## Pod Identity vs IRSA

| Topic | Pod Identity | IRSA |
| --- | --- | --- |
| Setup | Pod Identity Agent addon + associations | OIDC provider + trust policy per role |
| SA annotation | Not required same way as IRSA | `eks.amazonaws.com/role-arn` |
| Cross-account | Supported patterns via role trusts | Common with OIDC trusts |
| Maturity | Newer unified model | Widely used, ecosystem familiar |
| Migration | Can run alongside during transition | Still valid long-term |

Pick one primary model per workload to reduce confusion; document exceptions.

## Workflow

### 1. Confirm scope and success criteria

1. Record cluster name, version, addons, namespaces, workloads needing AWS APIs.
2. Success: pod uses intended role only; node role lacks app perms; denial for other namespaces; CloudTrail shows role sessions from pods.
3. List required actions/resources per workload.

### 2. Inventory credential sources

```bash
aws eks describe-cluster --name "$CLUSTER"
aws eks list-addons --cluster-name "$CLUSTER"
kubectl -n kube-system get ds,deploy | rg -i 'pod-identity|identity'
aws eks list-pod-identity-associations --cluster-name "$CLUSTER"
# IRSA leftovers
kubectl get sa -A -o json | jq -r '.items[] | select(.metadata.annotations["eks.amazonaws.com/role-arn"]) | [.metadata.namespace,.metadata.name,.metadata.annotations["eks.amazonaws.com/role-arn"]] | @tsv'
```

1. Inspect node instance profile policies for over-broad S3/SQS/etc.
2. Note apps still using static secrets for AWS.

### 3. Baseline

1. Export current IAM roles used by apps.
2. Capture failing SDK calls from pods (AccessDenied).
3. Confirm AWS SDK versions support container credential provider chain used by Pod Identity.

### 4. Configure Pod Identity

**Addon / agent:** ensure Amazon EKS Pod Identity Agent is installed and healthy.

**IAM role trust for Pod Identity** (conceptual — use current AWS recommended principal/service):

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": { "Service": "pods.eks.amazonaws.com" },
      "Action": ["sts:AssumeRole", "sts:TagSession"],
      "Condition": {
        "StringEquals": {
          "aws:SourceAccount": "ACCT"
        }
      }
    }
  ]
}
```

Refine trust conditions per latest EKS docs for your region/feature set.

**Association:**

```bash
aws eks create-pod-identity-association \
  --cluster-name "$CLUSTER" \
  --namespace payments \
  --service-account payments-api \
  --role-arn arn:aws:iam::ACCT:role/payments-api
```

**IRSA alternative (if staying on OIDC):**

```bash
# Annotate SA
kubectl -n payments annotate sa payments-api \
  eks.amazonaws.com/role-arn=arn:aws:iam::ACCT:role/payments-api --overwrite
```

Trust policy uses OIDC provider `sub`/`aud` conditions for namespace/sa.

**Permissions**

1. Task-equivalent least privilege on the app role.
2. Remove duplicate app permissions from node role after migration.
3. Separate roles per service account; do not share one role across all namespaces.

### 5. Verify with evidence

```bash
kubectl -n payments run awscli --rm -it --image=amazon/aws-cli --restart=Never \
  --serviceaccount=payments-api -- sts get-caller-identity
# Expect Arn includes payments-api role
kubectl -n other run awscli --rm -it --image=amazon/aws-cli --restart=Never \
  --serviceaccount=default -- sts get-caller-identity
# Expect node role or none — not payments-api
```

1. App integration test for S3/SQS with deny on unauthorized bucket.
2. CloudTrail: `AssumeRole` / session tags from Pod Identity.
3. Restart pods after association changes.

### 6. Observe and harden

1. Access Analyzer / unused access on pod roles.
2. Alert on new associations in prod clusters.
3. Periodically grep for long-lived access keys in cluster secrets.

### 7. Hand off

1. Platform doc: how teams request SA→role associations.
2. Chart templates with SA name conventions.
3. Migration checklist IRSA → Pod Identity if adopted.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Identity | SA-mapped least-privilege role | node role with S3 full access |
| Scope | one role per app SA | cluster-wide shared app role |
| Secrets | no static AKIA keys | keys in K8s Secret |
| Models | documented primary model | IRSA+PodIdentity+node all overlapping |
| Trust | account/source conditions | `Principal: *` |
| Verify | sts get-caller-identity in pod | “it worked in CI” |

## Output Checklist

- [ ] Cluster/addons/workloads recorded
- [ ] Node vs IRSA vs Pod Identity inventory done
- [ ] Associations or IRSA annotations correct
- [ ] IAM policies least privilege
- [ ] Node role stripped of app perms
- [ ] Pod caller-identity evidence captured
- [ ] Cross-namespace isolation verified
- [ ] Monitoring on association/role changes
- [ ] `code-quality-standards` applied to automation

## Rules

- Owned clusters only; pod credentials equal cloud credentials.
- Never rely on node roles for application AWS access.
- Least privilege and per-SA roles by default.
- Verify inside the pod with `get-caller-identity`.
- Focus on pod AWS identity; broader EKS admission/network policies elsewhere.

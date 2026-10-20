---
name: design-stack-composition
description: Design Terraform stack composition — module boundaries, state layout, workspace strategy, remote-state plumbing, blast radius per apply.
---

# design-stack-composition

> One big Terraform state is a foot-cannon; one stack per resource is unmanageable. Pick the right granularity. Output: module + state layout, with the blast radius of each apply named.

## When to use

- Greenfield: setting up Terraform from scratch.
- Brownfield: an oversized state is becoming a deployment risk.
- Multi-environment / multi-account / multi-region rollout planning.

## Procedure

1. **Identify blast-radius zones.** Group resources by "who is impacted if this `apply` goes wrong":
   - **Foundational** (rarely changes; impact: entire org) — VPC, accounts, KMS, IAM trust policies.
   - **Platform** (monthly; impact: multiple services) — EKS clusters, shared databases, service mesh.
   - **Service** (per-feature; impact: one service) — Lambdas, ECS services, SQS, app DBs.
2. **One state per blast-radius zone × environment.** A bad change to the foundational stack should never block a service deploy.
3. **State backend.** Remote state (S3 + DynamoDB lock for AWS; GCS + lock for GCP; AzureRM blob + lease for Azure). Local state on `main` is a refusal-to-merge.
4. **Workspaces vs directories.**
   - **Workspaces** for genuinely identical environments (dev/staging/prod with the same module). Variables tweak per workspace.
   - **Directories** when environments diverge structurally (different modules, different providers). Workspaces hide divergence; directories make it explicit.
5. **Module boundaries.** A module owns a *capability*, not a *primitive*. `network-vpc` (capability) over `aws-vpc` (primitive); the module composes VPC + subnets + routes + NAT.
6. **`required_providers` + version pinning.** Pin minor in modules (`~> 5.0`); pin patch in root stacks. Floating across rebuilds = surprise plan output.
7. **Remote-state references** (`terraform_remote_state`) only between adjacent zones. Service stacks read platform outputs (cluster ID, DB endpoints); platform stacks read foundational outputs (VPC ID, KMS key ARN). Service stacks should not reach into another service's state.
8. **Per-apply blast radius.** Document for each stack:
   - What it owns.
   - What breaks if you destroy it.
   - Who can apply it (RBAC; foundational stacks usually require multi-approver).

## Output

```text
design-stack-composition: refund-platform on AWS

States (foundational → service)

  1. foundational/
       Owns:    VPC, subnets, NAT, route tables, KMS keys, IAM trust policies.
       Blast:   ENTIRE ORG — protect.
       Apply:   2-person review, manual trigger.
       Backend: s3://acme-tf-state/foundational/<account-id>/terraform.tfstate

  2. platform-shared/
       Owns:    EKS cluster, shared RDS (analytics), service mesh.
       Blast:   ALL SERVICES — coordinated rollouts.
       Apply:   platform team, weekly cadence.
       Reads:   terraform_remote_state.foundational.outputs.{vpc_id, kms_arn}

  3. service-refund/  ← one per service
       Owns:    Lambda functions, SQS, DynamoDB tables, per-service IAM roles.
       Blast:   refund service only.
       Apply:   refund team, per-PR via CI.
       Reads:   terraform_remote_state.platform_shared.outputs.{cluster_id, mesh_ca}

Workspaces
  dev / staging / prod per state — same module, vars per workspace.

Module boundaries
  /modules/network/vpc           VPC + subnets + NAT + route tables (capability).
  /modules/eks/cluster-with-addons  EKS + ALB controller + cert-manager + ExternalDNS.
  /modules/service/lambda-sqs    Lambda + SQS + DLQ + alarms (capability).

Provider pinning
  Modules: ~> 5.0 (minor)
  Root:    = 5.43.2 (exact, root re-bumps deliberately)

Anti-foot-cannon checks
  ✓ No service stack references another service's state.
  ✓ Foundational state is RO from platform; platform state RO from service.
  ✓ All states locked via DynamoDB.
  ✗ Currently dev workspace shares the same backend bucket as prod — separate buckets per env recommended.
```

## Quality bar

- Stack boundaries match blast-radius zones, not org-chart boundaries.
- Remote state references go one direction (foundational → platform → service), never sideways.
- Workspaces vs directories chosen on structural divergence, not feature.
- RBAC for `apply` matches the blast radius.

## Anti-patterns to avoid

- One big monolithic state for the whole org. Apply takes minutes, blast radius is everything.
- One state per resource. State plumbing eats all the time you saved.
- Workspaces in lieu of separate directories when environments diverge structurally. Surprises a year later.
- Reading sibling services' remote state. Tight coupling masquerading as composition.

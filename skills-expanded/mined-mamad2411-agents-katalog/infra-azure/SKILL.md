---
name: infra-azure
description: >
  Azure for AI platforms — the six surfaces a platform actually uses, with least privilege first.
  Carries: Entra ID and Azure RBAC (two systems people conflate, and the conflation is the bug),
  **managed identity so no client secret ever exists**, AKS with Workload Identity, Container Apps
  and Functions for serverless, Azure SQL/PostgreSQL Flexible Server/Cosmos DB with private
  endpoints, Azure Pipelines + ACR held to the secure-cicd bar, Key Vault, and Azure OpenAI with its
  data-handling and regional-quota realities. Includes an AWS→Azure equivalents table. Load when
  building on Azure, assigning roles, provisioning AKS, or wiring CI to Azure. Triggers: Azure, az
  cli, AKS, Container Apps, Azure Functions, Azure OpenAI, Cosmos DB, Azure SQL, Key Vault, Entra
  ID, managed identity, service principal, RBAC, resource group, subscription, ARM, Bicep, ACR,
  Azure Pipelines, Blob Storage, private endpoint. Canon is `identity-and-access.md` +
  `platform-security.md`; Terraform is `iac-terraform`; cluster workloads are `kubernetes`.
---

# infra-azure — Azure, and the two identity systems you must keep straight

**Pinned:** azure-cli, azure-* SDKs — unpinned · authored 2026-07 · run `/skill-update infra-azure`
once the CLI is installed (`az version`).
**Verified:** 2026-07-25 — the AKS network-policy default (and that it is **creation-time only**)
and the Azure OpenAI abuse-monitoring retention confirmed against Microsoft documentation. The
Functions Consumption-plan timeout ceiling is **unverified** and deliberately stated without a
number below. Azure renames services frequently (Azure AD → Entra ID is recent); verify names
against current docs.

> On-demand: load this when the project runs on Azure. **The boundary is the role assignment, not
> this skill's judgment.** Canon: `identity-and-access.md` (`I1`–`I3`), `platform-security.md`
> (`P8`, `P11`), `supply-chain.md` (`C6`). Declaring infrastructure is `iac-terraform`; cluster
> workloads are `kubernetes`.

## Coming from AWS

| AWS | Azure | Note |
|---|---|---|
| Account | **Subscription** | Billing + quota boundary |
| — | **Resource group** | No AWS equivalent. Lifecycle container; delete it, delete everything in it |
| Organizations / OU | Management group | RBAC inherits down |
| IAM (identity + authz in one) | **Entra ID** (who) + **Azure RBAC** (what) | **Two systems.** Conflating them is the classic mistake |
| IAM role | Role assignment (role + principal + scope) | |
| IRSA | **Workload Identity** (+ managed identity) | |
| S3 | Blob Storage | |
| EKS | **AKS** | |
| Lambda | Azure Functions / **Container Apps** | Container Apps takes a container |
| Fargate | Container Apps | |
| RDS | Azure SQL / **PostgreSQL Flexible Server** | |
| DynamoDB | **Cosmos DB** | Multi-model |
| Redshift | Synapse / Fabric | |
| CodePipeline | **Azure Pipelines** / GitHub Actions | |
| ECR | **ACR** | |
| Secrets Manager | **Key Vault** | Also certificates and keys |
| Bedrock | **Azure OpenAI** | |
| CloudTrail | **Azure Monitor activity logs** | |

## 1. Identity and least privilege

**The thing to internalise: Entra ID and Azure RBAC are separate systems.**

- **Entra ID** is the identity provider — users, groups, service principals, managed identities, and
  app registrations. Entra *roles* (Global Administrator, Application Administrator) govern the
  directory itself.
- **Azure RBAC** governs *Azure resources* — a role assignment is a **role + principal + scope**,
  where scope is a management group, subscription, resource group, or single resource.

Granting someone Contributor on a subscription does nothing in Entra; granting Global Administrator
grants nothing on resources directly (but can grant it to itself, which is why it is tightly held).
Teams that conflate the two produce permissions nobody can reason about.

- **Assign at the narrowest scope**, and prefer resource-group scope over subscription. Assignments
  inherit downward.
- **Avoid Owner and subscription-wide Contributor.** Contributor can do almost anything to resources
  including deleting them; Owner adds granting access to others.
- **Assign to groups, not individuals** — it is the only way this stays manageable.
- **Privileged Identity Management** for just-in-time elevation on the roles that matter, where the
  licensing allows.
- **Azure Policy** is the guardrail layer, and it is genuinely good: deny public blob access, require
  private endpoints on databases, require tags, enforce allowed regions. Deploy the deny policies
  before people start creating things.

**No client secrets** (`I3`). A service principal with a password is a long-lived credential:

```bash
# Which identity am I? (S8)
az account show
az ad signed-in-user show

# AKS Workload Identity — the pod's KSA federates to a managed identity. No secret.
az aks update -g RG -n CLUSTER --enable-oidc-issuer --enable-workload-identity
az identity federated-credential create --name fic --identity-name MI -g RG \
  --issuer "$(az aks show -g RG -n CLUSTER --query oidcIssuerProfile.issuerUrl -o tsv)" \
  --subject "system:serviceaccount:NAMESPACE:KSA" --audience api://AzureADTokenExchange
```

Prefer **user-assigned managed identity** over system-assigned for anything shared across resources
or that must survive resource recreation. **CI → Azure uses OIDC federation** (`C6`), with the
federated credential's subject scoped to the repo **and branch/environment**.

## 2. AKS

- **Workload Identity + OIDC issuer on** (above). Entra Workload ID replaced pod-managed identity.
- **Private cluster** with authorized IP ranges on the API server.
- **Azure CNI** vs kubenet: CNI gives pods VNet IPs (needed for private endpoints and network
  policy); plan the address space, because exhausting it is painful to fix.
- **Network policy on — and this is a cluster-creation decision you cannot revisit.** AKS ships with
  no network policy: by default every pod can talk to every other pod, which fails
  `platform-security.md` `P5`. The trap is that **the policy engine (Azure NPM or Cilium) can only be
  selected when the cluster is created** — retrofitting it means redeploying the cluster. Decide at
  `az aks create`, or plan a migration later.
- **Azure Policy for AKS** enforces Pod Security-equivalent constraints at admission — the built-in
  route to `P1` alongside `policy-as-code`.
- **Key Vault CSI driver** to mount secrets rather than syncing them into Kubernetes Secrets
  (`secrets-management`).
- **GPU node pools** with taints, plus the NVIDIA device plugin. Spot node pools are cheap and
  genuinely get reclaimed — only for interruptible work.
- What Microsoft owns vs you → `control-coverage.md` (`P8`).

## 3. Serverless

**Container Apps** is usually the right fit for an AI platform — it runs a container, scales to
zero, and has KEDA-based scaling on queue depth, which pairs well with `caching-and-queues`.

- **Cold start against a latency SLO**: set minimum replicas above zero for user-facing paths;
  loading model weights on cold start is minutes.
- **Managed identity per app**, not a shared one.
- **Ingress internal-only** unless the app is genuinely public.
- **Azure Functions** for event handlers. Note the **Consumption plan's timeout ceiling** — long
  generations need the Premium plan, a durable function, or a queue.
- **Durable Functions** are worth knowing for long-running, stateful, resumable workflows — the same
  niche Temporal fills (`workflow-orchestration`), and a reasonable answer for agent runs with human
  approval steps (`ai-security.md` `AI3`).

## 4. Managed databases

| Service | For |
|---|---|
| **Azure Database for PostgreSQL — Flexible Server** | Default OLTP. Supports `pgvector` (`vector-stores`) |
| **Azure SQL Database** | Managed SQL Server |
| **Cosmos DB** | Global multi-model (document, graph via Gremlin, key-value). Watch the RU model |
| **Azure Cache for Redis** | See `caching-and-queues` |
| **Azure AI Search** | Managed vector + keyword hybrid search |

Non-negotiables (`P11`, `D9`): **private endpoints, public network access disabled** — enforce with
Azure Policy so it cannot be re-enabled by accident; **Entra authentication** rather than stored
passwords where supported; TLS enforced; encryption at rest with CMEK where the data class warrants
it; backups with **a tested restore** (`D10`).

Cosmos DB note: it bills by provisioned or consumed **Request Units**, and a poorly-partitioned
container is both slow and expensive. Choose the partition key deliberately — it cannot be changed
later without a migration.

## 5. Cloud-native CI/CD

**Azure Pipelines** (or GitHub Actions, which is equally first-class here) + **ACR**:

- **Workload identity federation for the service connection** — not a service principal secret.
- **Least-privilege service connection per pipeline**, scoped to one resource group.
- **Approvals and branch-control checks** on environments that deploy to production.
- **Untrusted-contributor builds get no secrets** (`CICD-SEC-4`).
- **ACR** with Microsoft Defender scanning, content trust, and — where available — image signing
  verified at admission (`supply-chain.md` `C3`).

## 6. Azure OpenAI

- **Data handling** — Azure OpenAI does not train on your data, but **abuse monitoring is on by
  default and may retain prompts and completions for up to 30 days**. Zero data retention requires
  an approved exemption, and that exemption is available only under an Enterprise Agreement or
  Microsoft Customer Agreement — **not on pay-as-you-go**. If your data classification cannot
  tolerate 30-day third-party retention, that is a procurement constraint to discover now rather
  than at launch. Sending a prompt is egress (`S7`); record the answer for your subscription.
- **Deployments pin a model version.** Use that; do not track "latest" (`M14`). Understand the
  retirement schedule — Azure retires model versions on a published timeline, which is a planned
  migration rather than a surprise if you're watching.
- **Quota is per-region and per-model**, allocated in tokens per minute. This is an availability
  constraint, not just a cost one: plan capacity, handle 429s with backoff (`R4`), and consider
  multiple deployments for failover (`R5`).
- **Private endpoint + disabled public access**, and the managed identity of the calling workload
  rather than an API key.
- Content filtering is on by default with configurable severity — it is a `guardrails` layer, not a
  substitute for your own.

## Gotchas

- **Conflating Entra roles with Azure RBAC.** The most common Azure permission confusion.
- **Owner or subscription Contributor handed out to unblock someone.**
- **A service principal secret in a pipeline variable.** Federate instead.
- **Public network access left on for a database.** Deny it by policy (`P11`).
- **Network policy not enabled on AKS** — off by default, so `P5` silently isn't met, and it is
  **creation-time only**: discovering this after the cluster exists means a redeploy.
- **CNI address space under-planned**, discovered when the cluster can't scale.
- **Azure OpenAI quota discovered in production** as 429s under load.
- **Resource groups used as a dumping ground**, so the lifecycle boundary means nothing — and then
  someone deletes one.

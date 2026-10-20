---
name: infra-gcp
description: >
  Google Cloud for AI platforms — the six surfaces a platform actually uses, with least privilege
  first. Carries: the IAM model (roles bind to principals on a resource hierarchy, and the
  inheritance is where over-permission comes from), **Workload Identity Federation so no service
  account key ever exists**, GKE (Autopilot vs Standard, GPU node pools), Cloud Run and Functions
  for serverless, Cloud SQL/AlloyDB/Spanner with private IP, Cloud Build + Artifact Registry held to
  the secure-cicd bar, and Vertex AI with its data-retention terms. Includes an AWS→GCP equivalents
  table. Load when building on GCP, writing IAM bindings, provisioning GKE, or wiring CI to GCP.
  Triggers: GCP, google cloud, gcloud, GKE, Cloud Run, Cloud Functions, Vertex AI, BigQuery, Cloud
  SQL, AlloyDB, Spanner, Cloud Build, Artifact Registry, Secret Manager, Workload Identity, service
  account key, project, folder, org policy, GCS. Canon is `identity-and-access.md` +
  `platform-security.md`; Terraform is `iac-terraform`; cluster workloads are `kubernetes`.
---

# infra-gcp — Google Cloud, with the identity model that removes the keys

**Pinned:** gcloud, google-cloud-* — unpinned · authored 2026-07 · run `/skill-update infra-gcp` once
the SDK is installed (`gcloud version`).
**Verified:** 2026-07-25 — the `iam.disableServiceAccountKeyCreation` constraint id, the Cloud Run
request-timeout ceiling, and the Data Access audit-log default confirmed against Google Cloud
documentation. The other org-policy constraint ids and the Autopilot/Standard responsibility split
are **unverified** — check them against current docs before relying on them. GCP renames and
reorganises services regularly.

> On-demand: load this when the project runs on GCP. **The boundary is the IAM binding, not this
> skill's judgment** — same model as the rest of the repo (hooks are guardrails; permissions are the
> boundary), extended to this cloud. Canon: `identity-and-access.md` (`I1`–`I3`),
> `platform-security.md` (`P8`, `P11`), `supply-chain.md` (`C6`). Declaring any of this belongs in
> `iac-terraform`; workloads on the cluster are `kubernetes`.

## Coming from AWS

| AWS | GCP | Note |
|---|---|---|
| Account | **Project** | The main isolation unit. Projects are cheap — use them per environment |
| Organizations / OU | Organization / **Folder** | IAM inherits *down* the hierarchy |
| IAM role + policy | **Role** bound to a principal on a resource | No trust policy; the binding *is* the grant |
| IRSA | **Workload Identity Federation** | Same idea, less setup |
| S3 | Cloud Storage (GCS) | |
| EKS | **GKE** | Autopilot has no AWS equivalent |
| Lambda | Cloud Functions / **Cloud Run** | Cloud Run takes a container; usually the better fit |
| Fargate | Cloud Run | |
| RDS / Aurora | Cloud SQL / **AlloyDB** | Spanner for global horizontal scale |
| DynamoDB | Firestore / Bigtable | |
| Redshift | **BigQuery** | Serverless; no cluster to size |
| CodeBuild / CodePipeline | **Cloud Build** | |
| ECR | **Artifact Registry** | |
| Secrets Manager | **Secret Manager** | |
| Bedrock | **Vertex AI** | |
| CloudTrail | **Cloud Audit Logs** | Admin Activity on by default; **Data Access is not** |

## 1. Identity and least privilege

GCP's model is *bindings*: a **role** (a set of permissions) is bound to a **principal** on a
**resource**. There is no trust policy to get wrong — but there is inheritance, and that is where
over-permission comes from.

- **Grant at the narrowest resource, never the project by default.** A role bound at the *project*
  applies to every resource in it, and a role at the *folder* applies to every project beneath. This
  is the most common way GCP permissions become far broader than intended.
- **Avoid the basic roles** — `roles/owner`, `roles/editor`, `roles/viewer`. `Editor` in particular
  is enormous and is what a default service account gets.
- **Predefined roles over custom** where one fits; custom roles when you need a genuinely narrow set,
  accepting the maintenance.
- **Disable the default service accounts' automatic grants.** Compute Engine's default SA gets
  `Editor` unless an org policy stops it — set
  `constraints/iam.automaticIamGrantsForDefaultServiceAccounts` to prevent it.
- **Org policy constraints are the guardrails worth setting on day one:**
  `iam.disableServiceAccountKeyCreation` (see below), `compute.requireShieldedVm`,
  `storage.publicAccessPrevention`, `sql.restrictPublicIp`.
- Use `gcloud policy-intelligence` / the IAM Recommender to find and remove unused permissions —
  it works from actual usage.

**Service account keys should not exist** (`I3`). A downloaded `key.json` is a long-lived credential
that will end up in a repo, an image, or a laptop. Turn key creation off org-wide with
`constraints/iam.disableServiceAccountKeyCreation` and use the alternatives:

```bash
# Which identity am I? (the GCP equivalent of `aws sts get-caller-identity` — S8)
gcloud auth list
gcloud config get-value project

# GKE Workload Identity — the pod's KSA acts as a Google SA. No key anywhere.
gcloud container clusters update CLUSTER --workload-pool=PROJECT.svc.id.goog
gcloud iam service-accounts add-iam-policy-binding GSA@PROJECT.iam.gserviceaccount.com \
  --role roles/iam.workloadIdentityUser \
  --member "serviceAccount:PROJECT.svc.id.goog[NAMESPACE/KSA]"
kubectl annotate serviceaccount KSA -n NAMESPACE \
  iam.gke.io/gcp-service-account=GSA@PROJECT.iam.gserviceaccount.com
```

**CI → GCP is Workload Identity Federation, not a key** (`C6`). Scope the attribute condition to the
repository **and the ref**; a pool that trusts `repository == "org/repo"` alone accepts any branch,
including one a contributor pushed.

## 2. GKE

- **Autopilot** manages nodes for you and enforces a hardened baseline — a good default when you
  don't need node-level control. **Standard** when you need custom node pools, specific GPU
  configurations, or DaemonSets Autopilot restricts.
- **Workload Identity on, always** (above). It is the reason to prefer GKE's identity story.
- **Private cluster** with authorized networks for the control plane; nodes without public IPs.
- **Shielded GKE nodes** and Container-Optimized OS.
- **GPU node pools** need a taint so ordinary workloads don't land on them, plus the driver
  DaemonSet. Node auto-provisioning is convenient and can be expensive — bound it.
- What Google owns vs you: record it in `memory/process/control-coverage.md` rather than assuming
  (`P8`). Autopilot moves more of the CIS Kubernetes §1–4 surface to Google than Standard does.

## 3. Serverless

**Cloud Run** is usually the right serverless answer for an AI platform: it takes a container, so it
runs the same image as everywhere else, and it scales to zero.

- **Cold start against an LLM latency SLO** (`reliability-sre` `R1`): set `--min-instances` above
  zero for anything user-facing. Loading model weights on cold start is minutes, not milliseconds.
- **Request timeout defaults to 5 minutes and maxes out at 60** (`--timeout=3600s`). Raise it
  deliberately — the default will cut off a long generation, and the ceiling means anything longer
  needs a Cloud Run job or a queue (`caching-and-queues`) rather than a synchronous request.
- **One dedicated service account per service**, with only the roles that service needs — not the
  default compute SA.
- **`--no-allow-unauthenticated` by default**; put IAM or an API gateway in front.
- **Cloud Run jobs** for batch work; **Cloud Functions** for small event handlers, though Cloud Run
  covers most of it now.

## 4. Managed databases

| Service | For |
|---|---|
| **Cloud SQL** (Postgres/MySQL) | Default OLTP. Supports `pgvector` — see `vector-stores` |
| **AlloyDB** | Postgres-compatible, higher performance, better analytics |
| **Spanner** | Global, horizontally scalable, strongly consistent. Real cost |
| **Firestore / Bigtable** | Document / wide-column |
| **BigQuery** | Analytics warehouse. Serverless — see `sql` |

Non-negotiables (`P11`, `D9`): **private IP only** — enforce with the `sql.restrictPublicIp` org
policy so it cannot be turned on by accident; connect via the Cloud SQL Auth Proxy or a private
service connection; **IAM database authentication** rather than stored passwords where supported;
CMEK where the data class warrants it; automated backups with **a tested restore** (`D10`).

BigQuery note: it is billed by bytes scanned. Partition and cluster tables, and set custom quotas —
`SELECT *` on a large table is a budget event, and it is exactly what an agent writes by default.

## 5. Cloud-native CI/CD

**Cloud Build** + **Artifact Registry**, held to the same bar as `secure-cicd`:

- The build service account is **least-privilege and per-pipeline** — not the default, which is
  broad.
- **No long-lived credentials in builds**; Cloud Build has an identity, use it.
- **Untrusted-contributor builds get no secrets** — the PPE rule (`CICD-SEC-4`) applies here exactly
  as on GitHub Actions.
- **Artifact Registry** with vulnerability scanning on, immutable tags, and **Binary Authorization**
  to require attestations before GKE will run an image — this is the GCP mechanism for
  `supply-chain.md` `C3` (verify what you run), and it is the one worth wiring.

## 6. Vertex AI

- **Data handling terms** — what is retained, for how long, and where. Sending a prompt to a hosted
  model is egress and therefore publishing (`security.md` `S7`); confirm the terms for the specific
  service and region rather than assuming, and record the answer.
- **Pin the model version**, not a floating alias (`model-governance.md` `M14`). A silently updated
  model invalidates every evaluation you have.
- **Regional endpoints** for data residency; check that every component of the request path stays in
  region.
- Vertex AI Pipelines exists; if you already run an orchestrator, see `workflow-orchestration` before
  adding a second one.

## Gotchas

- **A role granted at the project level "just to unblock it."** It inherits to everything and nobody
  narrows it later.
- **A service account key in a repo.** Turn off key creation org-wide; it is the single highest-value
  control on this list.
- **Data Access audit logs are off by default — with BigQuery as the exception.** Admin Activity is
  always on; Data Access must be enabled per service, and "who read this bucket" is not recorded
  until you do (`P9`). **You cannot enable it retroactively**, so the cost of forgetting is an
  investigation you can't run. BigQuery's Data Access logs are on by default, which is exactly why
  teams assume the others are too.
- **Cloud Run scaling to zero on a latency-sensitive path.** Cold start plus model load is a
  user-visible outage that looks like slowness.
- **Public Cloud SQL IP.** Use the org policy so it cannot be enabled by accident (`P11`).
- **BigQuery cost from an unbounded query.** Set custom quotas before the bill.
- **Project sprawl with no folder structure**, so IAM cannot be reasoned about at all.

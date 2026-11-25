---
name: gcp-core
description: Apply Google Cloud architecture defaults across IAM, VPC, compute (GKE, Cloud Run, Functions, GCE), data (Cloud SQL, Spanner, BigQuery, Firestore), KMS/Secret Manager, and Cloud Operations. Use when designing or reviewing GCP workloads.
source: self
date_added: 2026-04-30
---

# GCP Core

Default configurations and decision guides for the most-used Google Cloud services. Pair with [landing-zones](../landing-zones/) for org/folder/project baseline.

## When to Use

- New GCP workload or review of an existing one.
- Choosing between Cloud Run, GKE, Cloud Functions, or GCE.
- Hardening IAM, VPC, encryption, and observability defaults.
- Aligning with the Google Cloud Architecture Framework.

## IAM & Org

- Hierarchy: **Organization** -> **Folders** (env or BU) -> **Projects** (per workload). One project per workload + env.
- **Workload Identity Federation** for CI/CD (GitHub OIDC, GitLab) — no service-account JSON keys.
- **Workload Identity** (GKE) for pod-to-GCP auth.
- Least privilege via **predefined roles** (avoid `roles/owner`, `roles/editor` in prod).
- **Org Policies** enforce: domain-restricted sharing, disable SA key creation, restrict allowed locations, require uniform bucket-level access, restrict public IPs on GCE.
- **Access Context Manager** + **VPC Service Controls** for sensitive data perimeters.

## Networking

- **Shared VPC** from a host project; service projects attach.
- Three regions for global services; **Global HTTP(S) Load Balancer** + **Cloud Armor** + **Cloud CDN** at the edge.
- **Private Google Access** + **Private Service Connect** for GCP API + SaaS access without public IPs.
- **Cloud NAT** for egress; firewall rules tag-based; **Hierarchical Firewall Policies** at folder level.
- IPv6 dual-stack where supported.

## Compute Decision Guide

| Workload | Pick |
| --- | --- |
| Containers, request-driven, scale-to-zero | **Cloud Run** (services or jobs) |
| Full Kubernetes, custom networking, many tenants | **GKE Autopilot** (default) or Standard |
| Event-driven small functions | **Cloud Run Functions** (2nd gen) |
| VM-based / lift-and-shift | **GCE MIG** with regional templates |
| Batch | **Batch** on GCE / GKE |

Default: Cloud Run for new services; GKE Autopilot when you need K8s primitives. Use **Direct VPC egress** for Cloud Run -> private resources.

## Data Services

| Need | Pick |
| --- | --- |
| Managed RDBMS | **Cloud SQL** (PostgreSQL/MySQL) with HA + PITR |
| Globally consistent, horizontally scalable RDBMS | **Spanner** (use Granular Instance for cost efficiency) |
| Document/serverless NoSQL | **Firestore** (Native mode) |
| Wide-column / time series | **Bigtable** |
| Analytics/lakehouse | **BigQuery** (with BigLake for open formats) |
| Object storage | **Cloud Storage** (multi-region for read-heavy global) |
| Cache | **Memorystore for Redis/Valkey** |
| Streaming | **Pub/Sub** (+ Dataflow for processing) |
| Search | **Vertex AI Search** or self-managed OpenSearch |

Cloud SQL: HA (regional), automated backups + PITR, private IP only, IAM database auth. BigQuery: partition + cluster every large table; reservations for predictable workloads, on-demand for spiky.

## Storage Defaults (Cloud Storage)

- **Uniform bucket-level access** on (no ACLs).
- **Public Access Prevention** enforced at org level.
- CMEK via Cloud KMS for sensitive data.
- Object Versioning + Lifecycle (transition to Nearline/Coldline/Archive; delete noncurrent).
- Bucket Lock for WORM/retention.
- Audit Logs to a logging project bucket.

## Encryption & Secrets

- **Cloud KMS** with CMEK for storage, Cloud SQL, BigQuery, Spanner, GKE etcd.
- **Secret Manager** for app secrets; rotation + replication policy set; access via service identity.
- TLS via Google-managed certs on load balancers.

## Observability

- **Cloud Logging** with log buckets, retention per use, log sinks to BigQuery / GCS / Pub/Sub for SIEM.
- **Cloud Monitoring** dashboards + alert policies; SLOs via Service Monitoring.
- **Cloud Trace** + **Cloud Profiler**; OpenTelemetry SDKs for app instrumentation.
- **Security Command Center** Premium/Enterprise for posture + threat detection.
- **Audit Logs**: Admin Activity (always on); Data Access enabled selectively for sensitive services.

## Governance & Cost

- **Org Policies** as code (Terraform); folder-level inheritance.
- **Required labels** (`app`, `env`, `owner`, `cost-center`) enforced via policy.
- **Committed Use Discounts** for stable baseline; Spot VMs for batch.
- **Budgets** with Pub/Sub-driven automation; per-project quotas.
- BigQuery: project-level reservations, slot autoscaling, query cost controls.

## Anti-Patterns

- Service-account keys committed to repos or stored in CI variables instead of WIF.
- `roles/editor` granted to humans or services.
- Public buckets / public Cloud SQL IPs in prod.
- Single-zone Cloud SQL or GKE Standard cluster for prod.
- BigQuery `SELECT *` on partitioned tables without filters (cost explosion).
- Cloud Functions 1st gen for new code (use 2nd gen / Cloud Run).
- Manual changes via Console — drift untracked by Terraform.

## Quality Gates

- IaC (Terraform) for all production resources; CI runs `terraform plan` in a PR.
- Org policies + VPC-SC perimeters enforced on regulated data.
- Audit log sinks to a dedicated logging project, retained per policy.
- SCC findings triaged; high/critical block release.
- Backups tested (Cloud SQL PITR, Spanner backups, GCS versioning).
- Budgets + quota alerts active.

## References

- Google Cloud Architecture Framework
- Google Cloud Security Foundations Blueprint
- BigQuery best practices
- GKE Autopilot docs

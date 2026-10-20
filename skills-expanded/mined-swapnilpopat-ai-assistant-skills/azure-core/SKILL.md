---
name: azure-core
description: Apply Microsoft Azure Well-Architected defaults across Entra ID, networking, compute (App Service, Container Apps, AKS, Functions), data (SQL, Cosmos, Storage), Key Vault, and Monitor. Use when designing or reviewing Azure workloads.
source: self
date_added: 2026-04-30
---

# Azure Core

Default configurations and decision guides for the most-used Azure services. Pair with [landing-zones](../landing-zones/) for management-group/subscription baseline.

## When to Use

- New Azure workload or review of an existing one.
- Choosing between App Service, Container Apps, AKS, Functions, or VMs.
- Hardening Entra ID, networking, encryption, and Monitor defaults.
- Aligning with Microsoft Cloud Adoption Framework (CAF) and Well-Architected (WAF).

## Identity (Entra ID)

- **No standing privileged access.** Use **PIM** (Privileged Identity Management) with time-bound, MFA-required activation.
- **Conditional Access** baseline: require MFA, block legacy auth, restrict by named locations + device compliance.
- **Managed Identities** (system or user-assigned) for workload-to-Azure auth — never service principals with secrets.
- **Workload Identity Federation** for GitHub/Azure DevOps -> Azure (OIDC, no secrets).
- **Entra ID groups** assigned via PIM to roles; review with Access Reviews.
- Break-glass accounts: 2x, cloud-only, FIDO2, monitored.

## Networking

- Hub-and-spoke with **Azure Virtual WAN** for multi-region; **Azure Firewall** or NVA in the hub.
- Private endpoints for PaaS (Storage, SQL, Key Vault, Cosmos) — disable public network access.
- **NSGs** by tier; **Application Security Groups** to reference workloads instead of IPs.
- **DDoS Protection Standard** on prod VNets.
- **Azure Front Door** + **WAF** for global HTTP entry; **Application Gateway + WAF** for regional.

## Compute Decision Guide

| Workload | Pick |
| --- | --- |
| Web app, simple deploy, built-in TLS/auth | **App Service** (Premium v3, zone-redundant) |
| Containers, scale-to-zero, KEDA scaling, no K8s overhead | **Container Apps** |
| Full Kubernetes, many teams, custom networking | **AKS** (with managed identity + Azure CNI Overlay) |
| Event-driven, short-lived | **Functions** (Flex Consumption or Premium) |
| Lift-and-shift / specialized OS | **VM Scale Sets** with Azure Compute Gallery |
| Batch | **Azure Batch** |

Defaults: zone-redundant SKUs in prod; system-assigned managed identity; deploy from Bicep/Terraform.

## Data Services

| Need | Pick |
| --- | --- |
| Relational, fully managed | **Azure SQL Database** (Business Critical, zone-redundant) or **Azure Database for PostgreSQL Flexible Server** |
| NoSQL, multi-region writes, low latency | **Cosmos DB** (NoSQL or PostgreSQL API) — choose right partition key |
| Object storage | **ADLS Gen2 / Blob Storage** (RA-GZRS for prod) |
| Analytics | **Microsoft Fabric** (OneLake) or **Synapse / Databricks** |
| Cache | **Azure Cache for Redis** (Premium, zone-redundant) |
| Streaming | **Event Hubs** (Kafka-compatible) or **Service Bus** for queues/topics |
| Search | **Azure AI Search** |

SQL: enable Auditing, Defender for SQL, automatic tuning, geo-replication or failover groups. Cosmos: continuous backup, autoscale RUs, design partition key for uniform RU/s.

## Storage Defaults

- **Azure Storage**: TLS 1.2 min, public blob access disabled at account, SAS only via stored access policies, customer-managed keys via Key Vault.
- **Soft delete** + **versioning** + **immutability policies** for compliance.
- Diagnostic settings to a Log Analytics workspace + archive to long-term storage.
- Use **Private Endpoints**; disable storage account key auth where possible (Entra-only access).

## Secrets & Encryption

- **Azure Key Vault** (Premium for HSM-backed keys) per environment; RBAC-based access; purge protection on.
- Customer-managed keys (CMK) via Key Vault for Storage, SQL, Cosmos, Disk encryption sets.
- Secrets accessed at runtime via Managed Identity; never embedded.

## Observability

- Single **Log Analytics workspace** per region/environment; Diagnostic Settings on every resource.
- **Application Insights** workspace-based, with OpenTelemetry Distro.
- **Azure Monitor** alerts -> Action Groups (Teams, PagerDuty, etc.).
- **Microsoft Defender for Cloud** + **Microsoft Sentinel** for SIEM.
- **Azure Policy** with built-in initiatives (CIS, ISO 27001, NIST, CAF) audited at management group.

## Governance & Cost

- Hierarchy: **Management Groups** -> **Subscriptions** (per env/landing zone) -> **Resource Groups** (per workload).
- **Azure Policy** enforces tags, allowed regions/SKUs, deny public endpoints.
- **Cost Management** budgets + anomaly alerts; tag enforcement for chargeback.
- **Reservations / Savings Plans** for stable baseline; Spot VMs for batch.

## Anti-Patterns

- App registrations with client secrets in pipelines instead of OIDC federation.
- Public endpoints on PaaS (Storage, SQL, Key Vault) when private is supported.
- Single-zone SKUs in production.
- Single shared resource group for unrelated workloads (no blast-radius isolation).
- Owner role assigned permanently instead of via PIM.
- ARM templates hand-edited in portal then "exported".
- Defender for Cloud disabled to "save money" on a regulated workload.

## Quality Gates

- IaC (Bicep or Terraform) for all production resources; what-if/plan in PR.
- Diagnostic settings on every resource.
- Defender for Cloud Standard tier on prod subscriptions; Secure Score tracked.
- Backup + restore tested for SQL, Cosmos, Storage, AKS PV.
- Private endpoints + Private DNS zones in place for PaaS.
- Cost budgets and anomaly alerts active.

## References

- Microsoft Cloud Adoption Framework (CAF)
- Azure Well-Architected Framework
- Azure Landing Zones (ALZ)
- Microsoft Security Best Practices

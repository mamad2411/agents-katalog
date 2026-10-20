---
name: design-azure-pattern
description: Pick the right Azure primitive — compute (Functions / Container Apps / App Service / AKS), database (Azure SQL / Cosmos DB / Postgres Flex), storage (Blob / Files / Disk).
---

# design-azure-pattern

> Pick an Azure primitive with the *why*. Output: chosen primitive, runner-up, flip conditions.

## Procedure

1. **Characterize the workload** (compute pattern, DB shape, storage, networking).
2. **Compute.**
   - HTTP / events, autoscale-to-zero → **Azure Functions** (Consumption plan or Flex Consumption for newer scale model).
   - Containerized, HTTP, KEDA-based scaling → **Container Apps** (managed Kubernetes under the hood; no cluster to run).
   - Long-running services, slot-based deploys → **App Service** (plans pin you to always-on cost).
   - Cluster-level controls (multi-tenant, GPU, service mesh) → **AKS**.
3. **Database.**
   - Relational, regional → **Azure SQL Database** (Hyperscale tier for very large) or **Azure Database for PostgreSQL Flexible Server**.
   - Multi-region, multi-model (document/graph/key) → **Cosmos DB** (pick API: NoSQL / Mongo / Cassandra / Gremlin / Table).
   - Strong consistency + cross-region writes → **Cosmos DB strong consistency** (cost premium) or Azure SQL multi-write groups.
   - Analytical → **Synapse** or **Fabric**.
4. **Storage.**
   - Object / blob → **Azure Blob Storage** (Hot / Cool / Cold / Archive tiers).
   - Filesystem → **Azure Files** (SMB/NFS).
   - Block → **Managed Disks**.
5. **Messaging.** **Service Bus** for transactional FIFO / sessions; **Event Grid** for fan-out events; **Event Hubs** for high-throughput stream ingest.
6. **Networking.** Application Gateway (L7) or Front Door (global). VNet integration for serverless → private DB.
7. **Cost shape.** Functions Consumption = exec time + GB-s + executions; Container Apps = vCPU-seconds + memory-seconds; App Service = plan-tier always-on; Cosmos = RU/s.
8. **Flip conditions.** Quantitative.

## Output

```text
design-azure-pattern: refund-async-writes

Compute:
  Chosen:    Container Apps (KEDA-scaled).
  Why:       bursty + containerized + already publishes Docker images.
  Runner-up: Azure Functions Flex Consumption (smaller code surface).
  Flip when: sustained > 1k RPS → AKS for cluster-level cost control.

Database:
  Chosen:    Azure Database for PostgreSQL Flexible Server (Burstable B2s).
  Why:       existing Postgres expertise; tier covers expected load.
  Flip when: multi-region writes or > 30TB → Cosmos DB.

Messaging:
  Chosen:    Service Bus with sessions enabled for per-refund FIFO.

Networking:
  Container Apps environment with VNet integration → private Postgres endpoint.

Cost driver: Container Apps vCPU-s + Postgres compute. ~$250/mo at 500 RPS.

Ops shape:
  Logs: Container Apps → Log Analytics workspace.
  Tracing: Application Insights via OpenTelemetry exporter.
  Errors: Application Insights failures pane.
```

## Anti-patterns to avoid

- "Cosmos DB by default." It's a fit for global multi-model, not "general purpose"; cost is high.
- "Functions Consumption for everything." Cold starts hit hard on .NET / Java; pick Flex or Container Apps.
- App Service Plan "Basic" for prod. Always-on cost without prod-grade features (slots, scale-out).
- Forgetting VNet integration for serverless → private DB. Default is internet egress.

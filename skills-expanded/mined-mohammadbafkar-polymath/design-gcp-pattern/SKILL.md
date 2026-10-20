---
name: design-gcp-pattern
description: Pick the right GCP primitive — compute (Cloud Run / GKE / Functions / GCE), database (Cloud SQL / Spanner / Firestore / Bigtable), storage (GCS) with cost + ops + scale tradeoffs.
---

# design-gcp-pattern

> Given a workload sketch, pick the GCP primitive with the *why*. Output: chosen primitive, runner-up, conditions to flip.

## Procedure

1. **Characterize the workload** (compute pattern, storage shape, DB query model, networking surface).
2. **Compute.**
   - HTTP, stateless, bursty, autoscale-to-zero → **Cloud Run** (managed K-native; supports concurrency per instance, custom domains, IAM).
   - Cron / event-driven, short-lived → **Cloud Functions (2nd gen)** (now Cloud Run under the hood, but with simpler triggers).
   - Long-running, stateful, GPU, complex networking → **GKE** (Autopilot for low-ops, Standard for control).
   - Legacy / windows / appliance → **GCE** (VMs with managed instance groups).
3. **Database.**
   - Relational, regional, < 30TB, traditional → **Cloud SQL** (Postgres / MySQL / SQL Server).
   - Relational, global, horizontal scale, strong consistency → **Spanner** (cost premium; scale you can't get elsewhere).
   - Document, mobile / web sync → **Firestore** (Native mode for new projects).
   - Wide-column, time-series, very-high-throughput → **Bigtable**.
   - Analytical / OLAP → **BigQuery** (serverless warehouse).
4. **Storage.**
   - Object → **GCS** (Standard / Nearline / Coldline / Archive tiers).
   - Filesystem → **Filestore** (managed NFS).
   - Block → **Persistent Disks**.
5. **Messaging.** Pub/Sub for fan-out + retention; Cloud Tasks for HTTP-triggered queues with per-task retry policies.
6. **Networking.** Cloud Load Balancing (global) > regional NLB > internal LB. Cloud Armor for WAF; serverless services attach via VPC Connector.
7. **Cost shape.** Cloud Run = vCPU-seconds + requests; GKE Autopilot = pod-resource; Spanner = node-hour; Firestore = ops + storage; BigQuery = on-demand TB-scanned (or flat-rate slots).
8. **Flip conditions.** Quantitative thresholds where you'd revisit.

## Output

```text
design-gcp-pattern: refund-async-writes

Compute:
  Chosen:    Cloud Run (concurrency 80, min instances 0).
  Why:       bursty + stateless + autoscale-to-zero.
  Runner-up: GKE Autopilot (when sustained > 1k RPS for > 30 min).
  Flip when: cold-start tax > 200ms p99 OR autoscale-up tail latency above SLO.

Database:
  Chosen:    Firestore (Native), collection /refunds with subcollection /events.
  Why:       document shape + ID-key lookups + sync via SDK.
  Flip when: cross-collection transactions appear → Cloud SQL Postgres.

Messaging:
  Chosen:    Pub/Sub with 7d retention, push subscription to Cloud Run.

Networking:
  HTTPS via Cloud Run's built-in HTTPS endpoint; no LB needed at this scale.

Cost driver: Cloud Run vCPU-seconds + Firestore reads/writes. ~$220/mo at 500 RPS.

Ops shape:
  Logs: Cloud Logging out of the box.
  Tracing: Cloud Trace via SDK.
  Errors: Error Reporting captures unhandled.
```

## Anti-patterns to avoid

- "Spanner because it sounds cool." Spanner's cost floor is high; use Cloud SQL until you outgrow it.
- "GKE for everything." Autopilot or Cloud Run handles 90% of workloads with less ops.
- BigQuery for OLTP. Per-query latency is seconds, not ms.
- Forgetting the VPC Connector for serverless → private DB access. Default serverless is internet-only.

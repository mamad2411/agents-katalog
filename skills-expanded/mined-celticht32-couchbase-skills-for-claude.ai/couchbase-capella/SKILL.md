---
name: couchbase-capella
description: "Provision, configure, and manage Couchbase Capella deployments. Use whenever the user asks about Capella cluster setup, Capella free tier, Capella trial, creating a Capella cluster, Capella pricing tiers, Capella compute tiers, database credentials, Capella allowed CIDRs, Capella VPC peering, Capella AWS PrivateLink, Azure Private Endpoint, Capella App Services setup, Capella networking, Capella database users vs cluster admin, Capella organizations, Capella projects, Capella connection strings, or 'how do I get started with Capella / set up Capella for production.' Distinct from couchbase-sizing (which has a Capella tier reference) and couchbase-security-hardening (which covers TLS and RBAC). This skill covers Capella as a product — provisioning, networking, credentials, and connecting your application to it."
license: MIT
---

# Couchbase Capella

A skill for *provisioning and configuring* Couchbase Capella deployments — from free tier through production, covering networking, credentials, and application connectivity.

Distinct from:
- `couchbase-sizing` — Capella tier selection math
- `couchbase-security-hardening` — TLS, RBAC, and audit configuration once the cluster is running
- `couchbase-backup-restore` — Capella backup and restore

## When this skill applies

- "How do I create a Capella cluster?"
- "How do I connect my app to Capella?"
- "What's the difference between database credentials and admin credentials?"
- "How do I set up allowed CIDRs / private networking?"
- "How do I set up VPC peering or PrivateLink with Capella?"
- "What are Capella orgs, projects, and clusters?"
- "How do I set up Capella App Services?"
- "Free tier vs paid — what are the differences?"

## Pick the right reference

| Question | Read |
|---|---|
| "Getting started — free tier, org/project structure, first cluster" | `references/getting-started.md` |
| "Networking — allowed CIDRs, VPC peering, PrivateLink" | `references/networking.md` |
| "Credentials — database users vs admin, connection strings" | `references/credentials.md` |

## Key Capella concepts

**Organization → Project → Cluster** is the hierarchy. Everything lives under an org. Projects group clusters by environment (dev, staging, prod). Clusters are the actual Couchbase deployments.

**Database credentials ≠ cluster admin credentials.** The admin credentials (used in the Capella UI) are for management only and should never be in your application code. Database credentials (created per cluster, scoped to buckets and roles) are what applications use. Always use database credentials for SDK connections.

**Allowed CIDRs** are IP allowlists at the cluster level. Your application's outbound IP(s) must be in the allowlist before connections are accepted. For production, use private networking (VPC peering or PrivateLink) instead of public-internet allowed CIDRs.

## Related skills

- `couchbase-sizing` — choosing the right Capella compute tier
- `couchbase-backup-restore` — managing Capella backups
- `couchbase-mobile` — Capella App Services for mobile sync
- `couchbase-observability` — Capella monitoring integration
- `couchbase-security-hardening` — RBAC and TLS on Capella

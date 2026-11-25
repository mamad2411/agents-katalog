---
name: mukhon-production-cloud
description: Production-grade Google Cloud architecture, deployment, scaling, and security super-pack for MUKHON. Covers Cloud Run container orchestration for Next.js 15 and Fastify 5, Cloud SQL PostgreSQL configuration with IAM and connection pooling, Cloud Storage media buckets with S3 compatibility, Secret Manager zero-credential injection, and Cloud Armor WAF DDoS defense.
license: MIT
---

# MUKHON Production Cloud Architecture

Comprehensive production deployment, cloud database engineering, media pipeline, and security standard for the **MUKHON** platform on Google Cloud Platform (GCP).

## When to Use This Skill

- Deploying MUKHON Web (Next.js 15) and MUKHON API (Fastify 5) to Google Cloud Run.
- Provisioning and configuring Cloud SQL for PostgreSQL 15 with automated connection pooling and private VPC peering.
- Configuring Cloud Storage buckets for user avatars, verified badge assets, citizen stories, and encrypted escrow receipts.
- Injecting database URLs, SMTP tokens, and Porichoy NID keys securely via Google Secret Manager without hardcoded environment variables.
- Hardening public HTTP endpoints against DDoS, credential stuffing, and bot scraping using Google Cloud Armor WAF and OWASP Core Rule Set (CRS).

## Architecture Blueprint

```
[ User Browser / Mobile App ]
             │
             ▼
[ Google Cloud Armor WAF / HTTPS Load Balancer ]
             ├── /api/* ──────────────► [ Cloud Run: MUKHON API (Fastify 5) ]
             └── /* (HTML/Static/SSR) ─► [ Cloud Run: MUKHON Web (Next.js 15) ]
                                                    │
             ┌──────────────────────────────────────┴──────────────────────────────────────┐
             ▼                                      ▼                                      ▼
[ Cloud SQL PostgreSQL 15 ]          [ Google Cloud Storage (Media) ]          [ Google Secret Manager ]
  - Private IP (VPC)                   - Citizen Stories (24h TTL)               - DATABASE_URL
  - pgBouncer Connection Pool          - Sovereign Media (Photos/Reels)          - SMTP_PASSWORD
  - Row-Level Escrow Locks             - CDN Signed URLs                         - PORICHOY_API_KEY
```

## Detailed Reference Guides

1. [Cloud Run Deployment](references/cloud-run-deployment.md): Next.js 15 and Fastify 5 container configurations, buildpacks, scaling rules, and health checks.
2. [Cloud SQL PostgreSQL](references/cloud-sql-postgres.md): Database provisioning, SSL/TLS enforcement, private VPC connectors, and pgBouncer parameters.
3. [Cloud Storage Media](references/cloud-storage-media.md): Bucket lifecycle policies, S3 HMAC interoperability, signed URLs, and public CDN caching.
4. [Secret Manager Integration](references/secret-manager.md): Zero-PII, zero-credential storage standard and runtime environment variable mounting.
5. [Cloud Armor & WAF Defense](references/waf-and-security.md): Rate limiting, OWASP CRS rules, bot detection, and anti-scraping policies.

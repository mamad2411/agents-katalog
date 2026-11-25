---
name: cloud-security
description: Cloud and infrastructure configuration security auditor for Vercel, Netlify, AWS, Azure, Google Cloud, and Supabase/Firebase project settings. Use when reviewing deployment configuration, environment variable management, IAM permissions, storage bucket access, or general cloud misconfiguration — rather than the application code itself.
---

# Cloud Security — Infrastructure & Deployment Configuration Auditor

A specialized skill for auditing infrastructure and deployment settings (not application code itself).

## When to use this
- Reviewing deployment configuration on Vercel/Netlify/AWS/Azure/GCP/Supabase/Firebase
- Suspected leakage of environment variables or overly broad IAM permissions
- Reviewing file storage bucket access settings

## Core Checks

### Environment Variables
- Real secrets (API keys, connection strings) are never exposed to the client (check that a client-exposed prefix wasn't mistakenly applied to a real secret).
- Separate credentials entirely per environment (development/staging/production) — never share the same keys across environments.
- `.env` files with real values are never committed to git (verify `.gitignore` coverage).

### IAM & Permissions (AWS/GCP/Azure)
- Principle of least privilege: no service is granted full administrative access (`*:*` or `Owner`) when it only needs narrow, specific permissions.
- Prefer short-lived/temporary credentials (assumed roles) over long-lived static API keys where possible.
- Regular key rotation, and immediate revocation of any leaked key.

### File Storage (S3 / Storage Buckets / Supabase Storage / Firebase Storage)
- No public buckets holding sensitive data without an explicit, deliberate reason.
- Fine-grained access policies instead of blanket public read/write.
- Signed, time-limited URLs for sensitive files instead of permanent open links.

### Deployment Platform Settings
- Preview/staging deployments don't expose real production data or connect directly to the production database.
- Deployment webhooks are protected by a signature/shared secret.

### Network
- No administrative ports (database, SSH, admin dashboards) open to the public internet without necessity.
- HTTPS enforced everywhere with automatic redirect from HTTP.

### Backups & Recovery
- Regular backups of critical data exist, with periodic restore testing.

## Report Format
```
Resource: [service/resource name]
Issue: [problem]
Severity: Critical/High/Medium/Low
Evidence: [current configuration]
Impact: [impact]
Fix: [recommended configuration]
```

## Rules
- This skill reviews infrastructure **configuration** only, not application code (that belongs to the other skills).
- Never request or use the user's actual live cloud credentials during review — work only from shared config files or a description of the settings.

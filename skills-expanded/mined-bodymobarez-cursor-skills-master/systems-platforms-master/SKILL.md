---
name: systems-platforms-master
description: >-
  Master hub for professional backend systems & platform setup end-to-end. Use to set up,
  model, secure, and operate data + infra platforms: MongoDB/Atlas (full schema, aggregation,
  indexing, admin), Supabase (Postgres/Auth/RLS/Storage/Edge/Realtime), Neon serverless Postgres,
  Cloudflare (Workers/Pages/R2/D1/KV/DO/DNS/WAF), Postman/Newman API tooling, and complete email
  servers (self-hosted Postfix/Dovecot or managed SES/Postmark/Resend + SPF/DKIM/DMARC + deliverability).
  Bundles 8 specialized skills (in skills/<name>/GUIDE.md). Use for any platform/DB/infra/email setup.
---

# Systems & Platforms — Master Hub (real software-engineering depth)

Set up and **operate** production data + infra platforms like a senior backend/platform engineer:
correct data modeling, security by default, migrations discipline, observability, and full admin —
not just "npm install and hope".

## How to use this hub

1. Start with **systems-platforms-foundation** (platform choice, env/secrets, connections, migrations).
2. Open the specific platform skill and follow its full setup + admin guide.
3. Combine with `integrations-master`, `backend-api-master`, `devops-master` for the rest of the stack.

## Bundled skills

- **systems-platforms-foundation** ⭐ — Choose the right DB/platform, environment & secrets management, connection pooling, migration discipline, backup/restore, observability, IaC mindset.  
  → `skills/systems-platforms-foundation/GUIDE.md`
- **database-studio-complete** ⭐ — Build a professional multi-page Database Studio: connections, schema browser, table editor, SQL IDE (Monaco), ER diagrams, migrations, backups, monitoring, RBAC, audit logs, AI SQL copilot. Postgres/MySQL/Mongo/SQLite adapters. Supabase Studio / DataGrip tier.  
  → `skills/database-studio-complete/GUIDE.md`
- **mongodb-complete** ⭐ — MongoDB Atlas + self-host: document data modeling (embed vs reference), schema design patterns, the aggregation framework, indexing strategy, transactions, change streams, RBAC/security, Compass, backups & sharding.  
  → `skills/mongodb-complete/GUIDE.md`
- **supabase-complete** ⭐ — Full Supabase: Postgres, Auth, **Row Level Security**, Storage, Edge Functions, Realtime, CLI + migrations, local dev, and going to production safely.  
  → `skills/supabase-complete/GUIDE.md`
- **neon-postgres-serverless** — Neon serverless Postgres: branching, autoscaling, connection pooling, the serverless driver, and Prisma/Drizzle integration.  
  → `skills/neon-postgres-serverless/GUIDE.md`
- **cloudflare-platform-complete** — Cloudflare developer platform: Workers, Pages, R2, D1, KV, Durable Objects, Queues, bindings, DNS, WAF/CDN, Wrangler, and observability.  
  → `skills/cloudflare-platform-complete/GUIDE.md`
- **postman-api-tooling** — Professional API tooling: collections, environments, variables, pre-request/test scripts, mocks, monitors, OpenAPI import, and **Newman in CI**.  
  → `skills/postman-api-tooling/GUIDE.md`
- **email-server-complete** — Build/operate email properly: self-hosted (Postfix/Dovecot/Rspamd) vs managed (SES/Postmark/Mailgun/Resend), **SPF/DKIM/DMARC/PTR**, deliverability, inbound parsing, queues, bounces/complaints, and monitoring.  
  → `skills/email-server-complete/GUIDE.md`

## Pairs well with

`backend-api-master` (API/auth/DB design, Stripe), `integrations-master` (webhooks, cloud, OAuth),
`devops-master` (Docker/K8s/Terraform/CI-CD), `communications-master` (transactional email/chat),
`fullstack-stacks-master` (app layer).

## Note

Bundled skills use `GUIDE.md` so only this master appears in Cursor's skills list.

---
name: supabase-production-auditor
description: Audit Supabase projects for production security, row level security, authentication, storage policies, service-role usage, Edge Functions, database design, indexes, performance, Realtime scaling, multi-tenancy, AI application data risks, cost, backups, observability, and production readiness. Use before launching SaaS, marketplaces, AI apps, mobile apps, internal tools, ecommerce, and learning platforms on Supabase.
---

# Supabase Production Auditor

Developed by the LetsCookTech Open Source Team.

Apply the shared [OutcomeLab skill standard](../../docs/SKILL-STANDARD.md) for evidence, verification, risk, benchmarking, and improvement.

Audit Supabase as a production data, auth, storage, and operations system. Detect RLS weaknesses, data exposure, cost blowups, scalability limits, and operational gaps before deployment.

## Workflow

1. Classify the app type, expected scale, data sensitivity, tenancy model, auth flows, storage usage, Realtime usage, Edge Functions, and AI/RAG data patterns.
2. Inventory database schemas, migrations, tables, constraints, indexes, policies, functions, storage buckets, API usage, service-role locations, and environment variables.
3. Audit RLS coverage, policy logic, tenant isolation, anonymous/authenticated access, admin paths, service-role usage, and privilege escalation risks.
4. Audit auth, storage, API, Edge Functions, Realtime, performance, backups, observability, migrations, cost, and disaster recovery.
5. Red-team data theft, storage abuse, RLS bypass, bandwidth abuse, admin escalation, cost attacks, and growth failure.
6. Score database design, security, RLS, auth, storage, API security, performance, Realtime, scalability, cost efficiency, production readiness, and maintainability.
7. Produce prioritized fixes with SQL/policy direction, verification queries, operational owners, and 30/90-day remediation.

## Output contract

Return executive summary, production readiness assessment, critical/high/medium/low findings, RLS findings, authentication findings, storage findings, performance findings, scalability findings, cost findings, production operations findings, recommended fixes, verification checks, 30-day remediation plan, and 90-day improvement plan.

Every finding must include evidence, risk, affected asset, impact, fix, and verification.

## Quality gates

- Do not approve production readiness without RLS coverage, backup posture, migration safety, secret handling, monitoring, and incident recovery checks.
- Do not recommend broad policies such as `true` predicates without explaining exact access scope.
- Flag missing artifacts as review gaps instead of guessing policy behavior.
- Treat service-role exposure, tenant leakage, and public bucket misuse as high-risk until proven safe.

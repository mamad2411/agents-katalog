---
name: fullstack-feature-scaffold
description: Scaffold end-to-end features across Next.js frontend, API layer, Supabase schema/policies, and tests.
---

# Full-Stack Feature Scaffold (Next.js + Supabase)

## Objective
Create a production-ready feature scaffold from schema to UI with secure defaults and tests.

## Scaffold Workflow
1. Requirement breakdown and acceptance criteria.
2. Supabase schema + migration + RLS policies.
3. Server-side API/action layer with validation.
4. Typed frontend data hooks/components.
5. UI states: loading, empty, error, success.
6. Vitest + Playwright coverage.

## Generated Artifacts
- Migration SQL and policy definitions.
- Typed domain models and API contracts.
- Route/module skeletons in Next.js App Router.
- Test files and fixtures.

## Guardrails
- No service role key in client code.
- No untyped API boundaries.
- Every mutation path requires authz checks.
- Include rollback notes for schema changes.

## Output Format
- Folder/file scaffold map.
- Step-by-step implementation plan.
- Validation and rollout checklist.

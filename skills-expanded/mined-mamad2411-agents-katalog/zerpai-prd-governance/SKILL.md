---
name: zerpai-prd-governance
description: Apply Zerpai ERP project-level product and engineering guardrails before changing code, behavior, architecture, or delivery processes. Use when tasks touch PRD-driven decisions such as auth-free development, locked tech choices, deployment expectations, documentation safety, or when Codex needs the project's non-negotiable rules instead of generic advice.
---

# Zerpai Prd Governance

Use this skill as the first pass when a task can drift away from Zerpai-specific decisions. Keep the response aligned to the project's actual constraints, not generic ERP or SaaS defaults.

## Workflow

1. Read `references/locked-decisions.md` before making changes that can affect behavior, architecture, dependencies, security posture, or release assumptions.
2. Read `references/context-map.md` when the task depends on where the source of truth lives in the PRD set.
3. Reject or redirect changes that violate locked rules unless the user explicitly asks to change the PRD itself.
4. Preserve project policy in code suggestions:
   - Do not edit PRD files unless explicitly requested.
   - Keep development auth toggleable via `ENABLE_AUTH` env flag; do not hardwire auth bypass into schema or business logic.
   - Respect locked stack choices and naming conventions.
   - Preserve the pure white `#FFFFFF` rule for modal, popup, dropdown, and overlay surfaces in PRD-governed UI.
   - Preserve the shared `ZerpaiDatePicker` rule for reusable date inputs instead of introducing raw `showDatePicker(...)` usages by default.
   - Preserve the global settings rules: real DB-backed data first, DB-backed defaults for master lookups, explicit empty/error states, centralized shared styling, and clear separation of warehouse/storage/accounting/physical concerns.
   - Preserve the multi-tenancy rule: all business-owned tables must use `entity_id uuid NOT NULL REFERENCES organisation_branch_master(id)` as the single canonical tenant scope column; global lookup tables must NOT have `entity_id`; access resolved context via `@Tenant()` or `@Tenant('entityId')` decorator in controllers.
   - Preserve the settings schema naming rule: use canonical table names from `current schema.md`; do not add a blanket `settings_` prefix for Settings-related tables.
   - Preserve the deep-linking rule: new modules and major internal sub-screens must expose deep-linkable GoRouter routes so refresh, direct URLs, and browser navigation preserve working context.
   - Preserve centralized control styling for save/create buttons, cancel/secondary buttons, upload affordances, and border/divider treatments instead of allowing screen-local color drift.
   - Prefer minimal, verifiable changes over broad rewrites.

## Non-Negotiables

- Treat `current schema.md` as the live DB source of truth and `PRD/PRD.md` as the product decisions source.
- Auth is enabled in production; use `ENABLE_AUTH` toggle for local dev bypass only.
- Default to Flutter + Riverpod + GoRouter + Dio + Hive on the frontend and NestJS + Drizzle + Supabase on the backend.
- Follow the repo's file placement and UI rules instead of introducing alternative patterns from other projects.
- Verify assumptions from code and configuration before changing behavior.

## Reference Loading

- Use `references/locked-decisions.md` for policies and hard constraints.
- Use `references/context-map.md` for which PRD file to consult for deployment, UI, schema, onboarding, monitoring, or folder structure questions.

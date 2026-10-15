---
name: agency
description: Use when creating, adapting, configuring, or shipping an Agency company app from AgencyWebBoilerplate or a bring-your-own repository. Prefer the Agency plugin tools for account state, env sync, deploys, agents, routines, and catalog actions, then use the local SDKs for repo-side product implementation.
---

# Agency

Use this skill when Codex needs to develop a repo-backed Agency app and coordinate the matching Agency account state.

## Default Workflow

1. Read the repo instructions first.
   - Respect `AGENTS.md`.
   - Read `AGENCY_SDK.md` and `agency/sdk/INTEGRATIONS.md` before platform-backed edits.
2. Prefer Agency plugin tools for account/control-plane work.
   - Connect with `agency_oauth_start` and `agency_oauth_finish` when the plugin is not authenticated.
   - Use `agency_match_company_repository` or `agency_list_companies`, then `agency_discover_capabilities`.
   - Use `agency_sync_local_env` before DB-backed or Agency-module-backed local development.
3. Implement product code in the repo with the bundled Agency SDKs.
   - Use the hosted Agency Postgres `DATABASE_URL`; use `pnpm db:push`, never migrations.
   - Use Agency Auth, Payments, Analytics, and Storage helpers instead of bespoke provider wiring.
   - Do not add direct Stripe or raw R2 credentials.
4. Coordinate Agency account state with tools when the request needs it.
   - Payments product work uses `agency_upsert_payment_product` before repo-side checkout UX.
   - Automation work uses event catalog, agents, routines, and starter-template tools.
5. Verify the normal repo check for meaningful changes, then ship both remotes when delivery is implied or requested.
   - Keep the user's Git origin branch-aware.
   - Push the Agency remote to `main` for deployment activation.
   - Surface blockers when origin or Agency remotes cannot be resolved safely.

## Read The Right Reference

- Repo bootstrap, BYO reconciliation, and dual-remote shipping: [references/repositories-and-delivery.md](references/repositories-and-delivery.md)
- Local env sync, hosted Postgres, and storage: [references/local-env-data-storage.md](references/local-env-data-storage.md)
- Auth, Payments, and Analytics integration rules: [references/product-integrations.md](references/product-integrations.md)
- Agents, routines, event triggers, and starter templates: [references/agents-and-routines.md](references/agents-and-routines.md)
- Email/event automation recipes including signup follow-up: [references/email-events-recipes.md](references/email-events-recipes.md)

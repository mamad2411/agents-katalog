---
name: sql-apps-cloud-preview
description: "Use when a user wants to publish, share, deploy, price, or assess cloud readiness for a SQL Apps project, especially a small private or personal project."
---

# Publish SQL Apps

Sharing is optional. `personal-free`, the primary and only bundled cloud profile: **Static Web Apps Free + managed Functions + Azure SQL Database free offer**. **No Static Web Apps SLA**; **potentially $0 within current allowances**.

Resolve `../../scripts/sql-apps.mjs` relative to this skill, not cwd. Quote its
absolute path; `home` selects the project containing input `docs/...`.
Run `workspace-check` before changes.

For SLA, private networking, organizational controls, over 25 invitees, extra roles, or unsupported managed identity, use maintained Azure/SQL skills; never add a bundled topology.

## When personal-free does not fit

If only Entra-only SQL/managed identity is unmet, with cold starts and possible charges accepted, Container Apps Consumption (public gateway, localhost-only DAB) is a candidate—not a bundled profile. Guaranteed $0, continuous availability or blocked policy require production architecture. Verify DAB auth, availability and quotas with maintained skills; derive roles from validated identity.

Hand infrastructure to `azure-prepare` → `azure-validate` → `azure-deploy`, never another publisher. Before writes, estimate supporting services; get separate approvals for spend, identity changes and interruption. Budgets are not spending caps. Validate shutdown and manual recovery disposably, keeping the database.

## Personal-free pipeline

1. **Confirm the application contract.** `personal-free-api.json` must explicitly allowlist every route, procedure, parameter, and sign-in provider. No arbitrary forwarding. Teams: add `"roles": ["owner","member"]` to member routes, including readiness; procedures read `SESSION_CONTEXT(N'role')`.
2. **Initialize local configuration.** `npm run publish -- init --name <name> --location <region> --environment prod` writes nonsecret configuration, not resources.
3. **Plan.** `npm run publish -- plan`: report subscription/resource group, public SQL, credential storage, excluded services, allowances and no-SLA posture.
4. **Get explicit approval.** Azure writes require the approval code from that exact plan. Never infer approval from a request to plan, estimate, or explain.
5. **Deploy.** `npm run publish -- deploy --approve <code>` provisions resources with `project=sql-apps`, environment and `deployment=personal-free` tags, verifies free settings, publishes schema/grants, deploys and checks readiness.
6. **Invite people.** `npm run publish -- invite --role owner|member --provider <provider> --user <identity>`. Up to 25 invitees.
7. **Validate live.** `npm run publish -- status` must report `Cost guard: verified`. Test anonymous, owner, member (if used) and signed-in-uninvited states, a browser write and SQL persistence after reload. ARM deployment is not acceptance.

## Security and cost truth

- Free limits stop rather than bill and can interrupt service. The cost guard fails closed unless the deployed Free SKU and SQL free-offer/AutoPause settings are proven.
- SQL is public; the `0.0.0.0` firewall rule admits Azure resources outside the subscription.
- Managed Functions lack SQL managed identity. Generated credentials live in Static Web Apps settings and protected `.sql-apps/deployments/` state.
- Runtime grants are only `CONNECT`, `EXECUTE` and `VIEW DEFINITION` on declared procedures.
- Ownership derives from provider plus immutable provider user ID, never email.

The guard excludes manual additions, offer changes, GitHub Actions, domains and third parties. Never claim guaranteed free, private networking, passwordless, production-grade or highly available. Consult maintained current Azure cost/SQL skills before quoting limits, eligibility, regions or prices.

## Evidence and approval

For foundation publisher changes, run focused publisher, infrastructure, authentication and packaging tests; routine publishing does not assume them. Disclose unverified implementation or live canary checks.

Use `sql-apps-validation`'s four-verdict report and state whether live Azure validation was performed. Deployment/invitation requires explicit target, region, resource-group, allowance/spend and owner approval.
For an external architecture, report cost safeguards as configured, exercised, partial or blocked, and which live checks ran.

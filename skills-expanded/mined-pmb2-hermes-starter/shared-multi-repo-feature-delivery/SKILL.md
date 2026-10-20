---
name: shared-multi-repo-feature-delivery
description: "Use when a live feature spans multiple repositories."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [multi-repo, ownership, deployment, verification, cross-repo, agent-context]
    triggers:
      - feature spans multiple repositories
      - commit and push all affected repos
      - document artifacts for humans and agents
      - coordinate frontend backend and deployment
      - dynamic compliance onboarding
    related_skills:
      - complete-implementation-cycle
      - agents-md-hierarchy
      - project-documentation-standards
      - web-app-qa
---

# Shared Multi-Repo Feature Delivery

## When to use

Use for a feature whose implementation, policy, documentation, or runtime ownership crosses repositories—especially onboarding, billing, commissions, CRM, hosted payment-provider flows, or shared agency infrastructure.

The durable session-specific patterns are in `references/shared-multi-repo-feature-delivery.md`.

## Core contract

A push is not a deployment. A deployment is not verified until the live API and user-facing behavior are checked. Report these states separately:

- implemented locally
- committed
- pushed
- deployed
- live-verified

Never collapse them into “done.”

## Workflow

### 1. Discover ownership and concurrent work

For every affected repository:

1. Inspect working tree, upstream, and recent commits.
2. Read the nearest `AGENTS.md` chain and canonical artifact map.
3. Identify which repo owns implementation, policy/agreement docs, runtime evidence, and deployment.
4. Preserve unrelated working-tree changes from other developers.
5. Put durable ownership in one canonical map and add concise reciprocal pointers in each repo’s `AGENTS.md`.

Do not create duplicate sources of truth in sibling repos.

### 2. Design backend contracts before UI

For dynamic onboarding or compliance workflows:

- ask the discriminator before displaying the checklist
- model applicability as structured metadata such as `audience: us|foreign|both`
- derive required IDs server-side from the selected track
- reject documents outside the selected track
- gate final completion against server-derived IDs
- carry the selected track through hosted-provider return and refresh URLs
- keep provider readiness backend-verified; never trust a redirect or checkbox

Preserve country, residency, entity, and tax inputs explicitly. Document where professional legal/accounting review is required.

### 3. Implement the UI as a projection of the contract

The frontend should:

- ask the discriminator clearly
- reload the checklist when it changes
- show only applicable fields and documents
- clear stale completion flags when switching tracks
- prevent action until required discriminator/country fields exist
- use automatic polling for asynchronous hosted onboarding when requested
- remove manual refresh controls when auto-refresh is desired
- apply the requested product styling to provider actions

### 4. Verify before shipping

Run, at minimum:

- backend syntax/import checks
- frontend production build
- structured API checks for every dynamic track
- a search/test proving removed controls are absent
- browser verification after deployment

If a package has no test script, run its real build command; do not report a missing script as a passing test.

### 5. Commit and push narrowly

Stage only intended implementation and documentation paths. Commit each repo with a scope-specific message. Push every affected branch and record the exact commit.

### 6. Deploy from committed sources

Use the established deployment path and rebuild durable images from source. A `docker cp` hot patch is an emergency bridge only, not the final deployment.

If deployment is blocked after commit and push:

- state clearly: “committed and pushed; deployment blocked”
- do not claim the live feature exists
- retry when the prerequisite is restored
- keep the task blocked rather than presenting an operator command as completion

### 7. Report with an evidence matrix

Report each repository with branch, commit, push result, and working-tree state. Separately report deployment result and live verification URLs/results. Distinguish verified facts, assumptions, and compliance caveats.

### 8. Treat deployment scope and build cost as first-class

For a targeted PWA change in a large Compose stack, build and recreate only the affected services. Inspect the Compose service graph before using `--no-cache`: a backend Dockerfile may install hundreds of MB of unrelated Python requirements, causing a 10-minute timeout even when the Node backend change is small. Prefer:

```bash
unset AUTHENTIK_IMAGE
docker compose --env-file .env --profile full build agency-leads-frontend
# Build backend separately; use the normal cached path unless dependencies changed.
docker compose --env-file .env --profile full build agency-leads-backend
docker compose --env-file .env --profile full up -d agency-leads-backend agency-leads-frontend
```

If a service was recreated from a new image, apply any source hot patch **after** recreation and restart, then rebuild the image durably. Never report a hot patch as the final deployment artifact.

For a public/internal route change, verify both server-rendered HTML and a real browser: HTTP can prove `/login` and `/register` return 200, but only browser verification catches stale client assets, hydration errors, missing controls, and CSS/state behavior.

### 9. Internal-only registration routes

When registration must remain available to authorized operators but hidden from ordinary users, preserve the direct `/register` route and remove every login-page link/button and registration invitation copy. Verify with both source search and browser text/DOM checks:

- login has no `/register` anchor
- login has no “Start registration” or “Register” text
- direct `/register` still renders
- internal checklist controls remain available

For asynchronous hosted onboarding, remove manual refresh controls completely when auto-polling is requested. Verify no standalone `Refresh` button remains, polling exists, the provider action has the requested styling, and readiness stops polling.

### 10. PWA admin roles and seeded test accounts

When extending a local PWA with administrator and VA/operator access:

- model roles explicitly and default every unknown or newly registered user to the least-privileged role
- include role in login/session payloads for routing, but re-read the current role from the database inside privileged middleware; never trust the JWT role alone
- keep public registration unable to request an admin role
- migrate the persistent database volume idempotently before seeding
- seed/upsert accounts from environment variables or a local gitignored secrets file, bcrypt-hash passwords, and never print or commit password values
- route admins to `/admin` and VAs to the ordinary workspace, while treating backend authorization as the security boundary
- verify admin login plus protected API returns `200`, and VA login against the same API returns `403`
- verify account roles persist after container recreation and the rebuilt image—not only a hot patch—is running

If the host cannot hairpin its own public domain after Docker/Traefik changes, exercise the production router locally with the real host/SNI (for example `curl --resolve host:443:127.0.0.1 ...`). This distinguishes routing/application health from a local network-path problem.

## Pitfalls

- Do not claim deployment because a local build succeeded.
- Do not leave manual refresh after implementing automatic polling.
- Do not use one universal tax checklist when residency changes required documents.
- Do not let the browser decide which documents are required.
- Do not stage unrelated artifacts produced by other developers or generators.
- Do not call internal tax captures official forms without review.
- Do not hide a deployment outage in a success summary.

## Verification checklist

- [ ] Ownership map and reciprocal agent pointers are current.
- [ ] Backend derives and enforces the selected track.
- [ ] Frontend dynamically reflects the selected track.
- [ ] Hosted status auto-refreshes and stops at readiness.
- [ ] Backend syntax/import checks pass.
- [ ] Frontend production build passes.
- [ ] Every track’s API output is verified.
- [ ] Intended files only are committed.
- [ ] Every affected repo is pushed.
- [ ] Deployment uses the pushed commit.
- [ ] Live API and browser behavior are checked.

---
name: add-google-analytics
description: Provision, install, verify, and non-destructively repair Google Analytics 4 for Next.js App Router or Pages Router, static HTML, Vite vanilla JavaScript, and Flask/Jinja projects. Use when asked to add GA4, Google Analytics, traffic analytics, a measurement ID, or gtag to a web project.
compatibility: Requires Node.js 22+, Git, gcloud, and Google Analytics account access. Vercel CLI is required only for linked Vercel projects.
---

# Add Google Analytics

Provision one production GA4 property and web stream per project, then add standard page views and Enhanced Measurement. Use a shared keyless service account; never create or download service-account keys.

## Non-negotiable safety rules

- Start with a dry-run plan. Ask for one explicit confirmation before any mutation.
- Plan and verify may run on a dirty tree. Apply requires a clean Git worktree.
- Do not stash, discard, commit, push, or deploy application code.
- Do not delete Analytics resources or collected data.
- Do not install alongside existing analytics. Stop and present findings.
- Do not guess when both Next.js routers, multiple package managers, multiple GA resources, or multiple production URLs are plausible.
- If a strict Content Security Policy affects the integration target or global responses, stop and propose a nonce/hash-aware project-specific change. A CSP isolated to documents outside the instrumentation target requires an explicit boundary review, not a project-wide stop. Never add `unsafe-inline` or broad origins.
- Never claim that project size creates a privacy-law exemption. This workflow intentionally loads analytics without a consent gate; state that fact in the plan.
- Keep credentials and tokens out of repositories, output, shell arguments, and logs. Measurement IDs and GA resource IDs are public metadata, not secrets.

## Supported targets

- Next.js App Router and Pages Router
- Plain static HTML and Vite-powered vanilla JavaScript
- Flask applications using Jinja templates

Refuse unsupported frameworks rather than improvising. Do not upgrade Next.js or change router architecture.

## 1. Inspect

Read repository guidance first. From the project root, run:

```bash
node <skill-dir>/scripts/inspect-project.mjs .
```

The inspector exits `2` when it finds blockers; its JSON is still the plan input. Also inspect deployment configuration and all files the change would touch.

Confirm:

- one supported target (or a clearly intentional Next.js router),
- one lockfile/package manager,
- no existing GA tag, Measurement ID, or `@next/third-parties/google`,
- no CSP affecting the integration target or global response,
- an explicit reviewed exclusion for any route-scoped CSP outside that target,
- a human-readable property name,
- an explicitly confirmed canonical production URL,
- the complete source-file target list,
- whether Vercel is linked.

For Flask/Jinja, follow `{% extends %}` relationships and prefer the highest shared base template. List standalone templates not covered by it. For static multi-page sites, list every first-party deployed HTML entry and exclude generated/vendor output.

## 2. Prepare the complete dry-run plan

Personal defaults belong in `~/.config/add-google-analytics/config.json`; project state belongs in the tracked `.ga4.json` file. Never put personal defaults in the skill repository.

The plan must show:

- GCP quota project and keyless service-account setup, if needed,
- selected Analytics account,
- property name, canonical URL, `America/Toronto`/`CAD` defaults or overrides,
- one production web stream,
- 14-month event and user retention with reset on activity,
- Enhanced Measurement enabled, including history-based page changes,
- Google Signals disabled and advertising product links verified absent,
- exact source/dependency changes,
- production-only deployment configuration,
- validation and browser verification commands,
- `.ga4.json` contents by field (IDs are unknown before creation), including adapter, target, and any reviewed CSP path exclusions,
- immediate analytics loading without a consent gate,
- no commit, push, or production deployment.

Ask for one explicit confirmation of this complete plan. After confirmation, proceed autonomously except for unavoidable Google account access UI and newly discovered conflicts.

## 3. Bootstrap keyless access once

Check the helper and local configuration:

```bash
node <skill-dir>/scripts/ga4-admin.mjs doctor
```

If configuration is absent, after plan approval run:

```bash
node <skill-dir>/scripts/ga4-admin.mjs bootstrap \
  --quota-project <project> \
  --time-zone America/Toronto \
  --currency CAD \
  --confirmed
```

This enables only `analyticsadmin.googleapis.com` and `iamcredentials.googleapis.com`, creates or reuses `analytics-automation@<project>.iam.gserviceaccount.com`, grants the active gcloud user `roles/iam.serviceAccountTokenCreator` on that service account, and grants the service account `roles/serviceusage.serviceUsageConsumer` on the quota project. The latter permits Analytics API quota attribution; it does not grant access to other project resources.

IAM changes can take about a minute to propagate. The helper retries only the expected `getAccessToken` and `serviceusage.services.use` propagation failures with bounded exponential backoff. Do not broaden retries to genuine Analytics authorization failures.

The user must add the printed service-account email as **Editor** in Google Analytics Account Access Management. Do not request Administrator. Then list accessible accounts:

```bash
node <skill-dir>/scripts/ga4-admin.mjs accounts
```

Require explicit account selection the first time, write it locally, and display the default on later runs:

```bash
node <skill-dir>/scripts/ga4-admin.mjs set-account --account accounts/<id>
```

## 4. Reconcile before provisioning

Run the live API plan:

```bash
node <skill-dir>/scripts/ga4-admin.mjs plan \
  --property-name '<name>' \
  --url '<canonical-production-url>'
```

If it finds a matching name or canonical URL, stop. Explain the candidate and require explicit approval before passing `--adopt-property properties/<id>`. Never create a duplicate automatically.

After the approved plan, provision or reconcile:

```bash
node <skill-dir>/scripts/ga4-admin.mjs apply \
  --property-name '<name>' \
  --url '<canonical-production-url>' \
  --confirmed
```

For approved adoption, append `--adopt-property properties/<id>`. The helper writes `.ga4.json` immediately after obtaining the stream so a partial failure can be repaired idempotently.

After source inspection, add non-secret integration metadata to `.ga4.json`: `adapter`, the source `target`, `excludedPaths`, and `cspBoundaryReviewed: true` when exclusions exist. Never mark a boundary reviewed without explicit approval.

## 5. Integrate the project

Read [references/integrations.md](references/integrations.md) completely and use the matching adapter.

Rules common to every adapter:

- Track production only.
- Add exactly one tag per rendered page.
- Use the Measurement ID from `.ga4.json`.
- Do not add custom business events.
- Preserve project formatting and conventions.
- Do not rename or repurpose existing application code named “analytics”; GA instrumentation is separate.

For linked Vercel projects, set `NEXT_PUBLIC_GA_MEASUREMENT_ID` for **production only** through the Vercel CLI. Inspect existing variables first; never add it to preview or development. Do not trigger a deployment.

For unsupported hosts, finish source integration but report exact deployment configuration still required.

## 6. Validate and verify

Run the repository's own formatter/check mode, typecheck, lint, tests, and production build when available. Use the detected package manager; never create another lockfile.

Verify live Analytics configuration:

```bash
node <skill-dir>/scripts/ga4-admin.mjs verify
```

Then follow the two-build browser procedure in the integration reference: verify a build without production variables emits no GA requests, rebuild with the production variables present at build time, mock collection endpoints with `204` while allowing `gtag.js` to load, and verify initial plus client-navigation page views without duplicates. Browser-level request verification is mandatory for apply/repair.

A later, separately requested post-deployment verification may inspect the live site. Do not wait for GA reports during installation; ingestion is delayed.

## Plan-only mode

When asked only to plan, run inspection and any read-only live API plan that existing configuration permits. Do not bootstrap IAM, enable APIs, create GA resources, edit files, or change Vercel. Dirty worktrees are allowed. Clearly list blockers and the next safe action.

## Repair mode

When `.ga4.json` exists, `plan` and `apply` reconcile the referenced live property instead of creating another. Repair only missing or drifted non-destructive settings and source/deployment integration. Verify advertising product links are absent. If an adopted property has links, report them and stop; never delete or replace resources to repair drift.

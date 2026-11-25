---
name: athena-auth-emails
description: Implement, debug, or explain Athena Auth email behavior. Use when Codex needs to work on Athena Auth admin email CRUD, email failure records, email template overrides, email event types, tenant-aware email routing, React Email payload support, or athena-js auth email binding parity in the `athena-auth` repo, the `athena-js` SDK, or a consumer repo using `createClient(...).auth.admin.email...`.
---

# Athena Auth Emails

Use this skill for three seams:

1. Backend email routes and persistence in `athena-auth`.
2. SDK bindings and React Email helpers in `athena-js`.
3. Consumer repos that call Athena Auth admin email routes through `@xylex-group/athena`.

If the task becomes mostly generic Athena SDK/runtime work outside email, also
use `$athena-js`.

## Read in this order

1. Read [references/backend-runtime.md](references/backend-runtime.md) when the task touches `athena-auth` routes, validation, auditing, event types, or template persistence.
2. Read [references/sdk-surface.md](references/sdk-surface.md) when the task touches `athena-js`, React Email helpers, exported limits, or consumer call sites.
3. Inspect the active checkout after the reference file identifies the exact files to change.

If docs, tests, and implementation disagree:

- trust `athena-auth` route handlers and tests for backend behavior
- trust current `athena-js` exports and types for SDK consumer contracts
- patch the real seam instead of papering over it in a consumer report, staging script, or local wrapper

## Choose the seam first

### Backend route work

- Inspect `crates/api/src/plugins/admin/mod.rs`, `handlers.rs`, `types.rs`, and the matching admin tests.
- Preserve exact route families: `/admin/email/*`, `/admin/email-failure/*`, `/admin/email-template/*`, and `/admin/email-event-type/list`.
- Preserve tenant-aware audit behavior and header aliases.
- Preserve null-vs-omitted patch semantics on update requests.

### SDK or consumer work

- Inspect `athena-js/src/auth/client.ts`, `react-email.ts`, `types.ts`, `limits.ts`, and the auth docs/tests.
- Prefer nested `auth.admin.email.template.*` bindings.
- Treat `auth.admin.emailTemplate.*` as compatibility-only.
- Keep exported limit constants aligned with backend constants instead of copying magic numbers into consumer code.

## Keep these rules stable

- Use `eventType` as the canonical taxonomy seam for templates and built-in events.
- Treat `templateKey` as compatibility and runtime fallback, not the only source of truth.
- Treat `metadata` as JSON object data with backend size and depth constraints.
- Treat template `variables` as normalized user input, not arbitrary JSON.
- Use WSL2 for Rust test runs on this machine.
- Validate with the narrowest matching gate before broader repo checks.

## Validate

- Backend route changes: run targeted `cargo test` from WSL2, then the broader matching crate test if needed.
- SDK changes: run targeted auth tests, `pnpm typecheck`, and `pnpm check:all`.
- Consumer issues: prove the final route, headers, and payload shape, not just types.

---
name: customware-email
description: Implement customer email in a Customware-generated React Router and Hono app, including durable Postmark inbound receipt and direct Postmark outbound sending. Use when a Builder task names the customware-email skill, provides a Postmark virtual inbound address, or asks to add customer-facing email to an existing Customware app.
---

# Customer Email

<purpose>

Implement one coherent Customware email capability for a Customware-generated app. The capability receives customer replies through the provisioned Postmark inbound webhook and sends customer-facing messages through the same development Postmark server's HTTPS API.

The task provides the project-specific addresses. The two managed server ENV values provide the credentials. This skill provides the implementation method, durable behavior, and verification contract.

</purpose>

> **Build toward the existing app.** Reuse its Hono routes, Drizzle schema, SQLite database, logging, error, and `Result` patterns. A small, native integration is easier to reason about and safer than a second email framework.

---

## Read first

Read these references before editing source files:

1. [references/common-architecture.md](references/common-architecture.md) — task inputs, platform boundaries, credentials, stack, and shared integration shape.
2. [references/inbound.md](references/inbound.md) — the fixed webhook, authentication, durable receipt, deduplication, and recovery contract.
3. [references/outbound.md](references/outbound.md) — direct Postmark API sending, message shape, sender/reply routing, and failure handling.
4. [references/common-quality.md](references/common-quality.md) — validation, safe logging, migration, tests, and final verification.

Read the inbound and outbound references even when the task initially sounds one-sided. Replies make the two directions one feature: inbound mail must be able to reach the app, and outbound mail must route replies back to the same virtual address.

<read_order>

Before implementation, also read the target repository's `AGENTS.md`, the complete Builder task, relevant project docs, and the existing database/route/service contracts. Treat the target repository as authoritative when a framework detail differs from an example here.

</read_order>

## Fixed platform contract

| Concern | Required decision |
| --- | --- |
| Postmark server | Use the one development server already provisioned for this project. The app does not create, delete, or configure it. |
| Inbound route | `POST /api/email/inbound` |
| Inbound authentication | HTTP Basic Auth, username `customware`, password from `POSTMARK_INBOUND_WEBHOOK_SECRET` |
| Server credentials | Read `POSTMARK_INBOUND_WEBHOOK_SECRET` and `POSTMARK_SERVER_TOKEN` only on the server. |
| Inbound address | Use the exact virtual address supplied in the task. Do not create an ENV for it. |
| Outbound sender | Use the exact task-provided sender, currently `messages@customware.ai`. Do not create an ENV for it. |
| Outbound stream | Postmark's existing Default Transactional stream (`outbound`). |
| Transport | Direct HTTPS requests to Postmark's Email API from server code. |
| SMTP | Do not enable or use SMTP. |
| Customware gateway | Do not add a Customware send endpoint, proxy, or email gateway. |
| Production | Implement the development capability described by the task. Do not add production-server, publish, or environment-branching behavior. |

<address_source_of_truth>

The task description is the source of truth for the virtual inbound address and outbound From address. Keep each value in one server-owned constant/module so it cannot drift between the sender, reply routing, and reviewer-visible code. Never replace either value with a placeholder, a guessed address, or a new ENV.

</address_source_of_truth>

## Non-negotiables

- Keep both Postmark credentials server-only. Never place them in browser code, `VITE_*`, HTML, JSON responses, task output, logs, or client state.
- Treat `.env` and `.env.*` as inaccessible. Do not inspect them with file commands. A runtime check may use `node --env-file=.env ...` without printing environment values.
- Register the inbound route before static serving and the SPA fallback.
- Persist an inbound delivery before acknowledging it. The 200 response means the raw delivery is safe to recover, not that application processing finished.
- Enforce `MessageID` uniqueness in the database. Do not implement deduplication as read-then-insert.
- Make inbound processing recoverable after a crash or restart; an in-memory callback cannot be the only record of work.
- Return the contract statuses in the inbound reference. Never return `403` to Postmark for this receiver.
- Send outbound mail only from server code with `X-Postmark-Server-Token` and `MessageStream: "outbound"`.
- Use the task's virtual inbound address as `ReplyTo`, so a customer reply comes back through the existing webhook.
- Keep message content and credentials out of logs. Log only safe operational identifiers and error categories.
- Reuse existing contracts and error/result conventions. Avoid duplicate validation, speculative abstractions, compatibility branches, or a second persistence framework.

## Implementation workflow

### 1. Establish the task contract

1. Read the task completely.
2. Extract the exact virtual inbound address and outbound From address.
3. Confirm the task names `customware-email` and that the Postmark server has already been provisioned.
4. Stop with a clear `action_required` result if either address or either managed credential contract is unavailable. Do not invent values.

### 2. Inspect the generated app

Locate the Hono entrypoint, route registration order, static/fallback handlers, Drizzle schema and migrations, query/service conventions, environment helper, logging boundary, and existing `Result`/Zod patterns. Identify where the app's customer workflows should consume an accepted email and where its existing business actions produce outbound messages.

### 3. Build the shared server foundation

Create one small server-owned email configuration module for the task-provided addresses and the two managed ENV reads. Keep provider calls behind a focused Postmark client/adapter that follows the app's existing result and error patterns. Do not let browser requests choose the server token, From address, ReplyTo address, stream, or Postmark URL.

### 4. Implement inbound and outbound

Follow [references/inbound.md](references/inbound.md) for the receiver and durable worker. Follow [references/outbound.md](references/outbound.md) for the Postmark Email API adapter and the app-facing send helper. Integrate both with existing domain flows instead of creating a parallel email subsystem.

### 5. Verify progressively

Run focused contract checks while implementing, then the repository's normal format, lint, typecheck, build, unit, and interactive checks. Use the test matrix in [references/common-quality.md](references/common-quality.md). If an external send is requested, use only an explicitly approved safe recipient; otherwise prove the exact request with a stubbed Postmark client and route-level tests.

### 6. Perform the final audit

Search the final diff for credential names, hardcoded secrets, SMTP usage, `POSTMARK_ACCOUNT_TOKEN`, production branches, direct browser-to-Postmark calls, raw email logging, and a second gateway. Confirm the task addresses are the only email values embedded in generated application code and that the database migration is included and applied through the app's normal command.

## Completion checklist

- [ ] The task's exact inbound and outbound addresses are used in one server-owned configuration module.
- [ ] `POSTMARK_INBOUND_WEBHOOK_SECRET` protects the inbound route and `POSTMARK_SERVER_TOKEN` authorizes outbound HTTPS calls.
- [ ] The inbound route captures raw JSON, validates `MessageID`, persists before 200, deduplicates by a database constraint, and recovers pending/stale work.
- [ ] Outbound requests use `POST /email`, `X-Postmark-Server-Token`, `MessageStream: "outbound"`, the task's From, and the task's inbound ReplyTo.
- [ ] SMTP, raw email, account-level provisioning, production behavior, and a Customware send gateway are absent.
- [ ] Sensitive values and message content are absent from browser bundles, responses, and logs.
- [ ] Migrations, focused tests, repository checks, build, and relevant browser verification pass.
- [ ] The final diff and reviewer requirements are read back before sign-off.

## Boundaries

Use this skill for the generated app's Customware email implementation. The Customware control plane owns Postmark server provisioning, encryption, hidden ENV materialization, webhook URL reconciliation on sandbox restart, cleanup, and publish protection. Do not duplicate those responsibilities in the generated app.

Use `customware-ai` for AI gateway or AI Elements work, `customware-support-widget` for the support widget, and `task-workflow` when the Builder task requires its full gated execution protocol. Those skills complement this one; they do not replace the email contracts here.

---
name: follow-service-resend
description: Use Resend to send transactional emails — send, templates, domains, webhooks
argument-hint: "[target-or-scope]"
related:
  - run-verify
  - run-test

---

## Goal

Use Resend to send transactional emails — send, templates, domains, webhooks

## Scope

Use when the task involves this library/tool — setup, usage, debugging, or best practices (service resend)

## Execute

### Workflows

> Goal: dispatch to the workflow matching the topic

- Setup: SDK install, `RESEND_API_KEY`, test send → `## Merged Details → setup-resend`
- Config: domain verification, `EMAIL_FROM`, templates, webhooks → `## Merged Details → config-resend`
- Verify: API key valid, domain verified → `## Merged Details → verify-connection`

### 1. Setup And Usage

> Goal: Use it correctly per the official docs

Latest: `resend@6.30.0` (verified 2026-09-26) — install with `bun add resend`

1. Create `new Resend(apiKey)` — apiKey from env `RESEND_API_KEY`
1. Send with `resend.emails.send({from,to,subject,html/react})` — verify the domain before production
1. Use React email components or HTML templates — preview in the dashboard
1. Set webhooks for delivery/bounce events if tracking is needed

### 2. Verify

> Goal: Confirm correct usage

1. Do `/run-verify` for lint, typecheck
2. Do `/run-test` if relevant tests exist
3. Check the latest official docs before using an uncertain API (service resend)

## Rules

- The from address must use a verified domain — never @resend.dev in production
- Retry with idempotency — never send duplicate emails
- Separate transactional vs marketing (Resend Broadcasts)
- Store secrets in env; never commit them

## Merged Details

### config-resend

##### Goal

Set/edit Resend configuration — verified domains, from address, email templates, and webhooks — without clobbering existing settings

##### Scope

- Verify the sending domain with DNS records (SPF/DKIM)
- Define from address and reply-to per environment
- Configure React/HTML templates and webhooks for delivery events
- Does not cover SDK install/API key → use `## Merged Details → setup-resend`

##### Execute

###### 1. Read Current Config

> Goal: Know the current state before editing

1. Read the mail module, `.env*`, and templates that exist in the project
2. Do `/check-secrets env-vars` to identify missing vars such as `RESEND_API_KEY`, `EMAIL_FROM`
3. Check verified domains in the dashboard — use `/open-web-for-config-secret` (service resend)
4. If no SDK/API key yet → do `## Merged Details → setup-resend` instead

###### 2. Verify Sending Domain

> Goal: Make the domain ready for production sending

1. Add the domain in the dashboard (Domains > Add domain)
2. Add the DNS records the dashboard specifies (SPF, DKIM, and MX for bounce if wanted) at the DNS provider
3. Wait for verification — check status in the dashboard until it shows verified
4. If DNS does not verify → recheck record names/values before telling the user

###### 3. Configure From Address And Templates

> Goal: Define sender and template config consistently

1. Define `EMAIL_FROM` such as `Name <noreply@yourdomain.com>` in env — it must be a verified domain only
2. Keep from/reply-to in one project config; never scatter hardcodes through the code
3. Use React email components or HTML templates — preview/test before production
4. Merge only the necessary keys — never overwrite the existing config

###### 4. Configure Webhooks

> Goal: Track delivery events securely (only if needed)

1. Add a webhook endpoint in the dashboard, selecting events such as `email.delivered`, `email.bounced`, `email.complained`
2. Store the webhook signing secret in `/follow-secret-manager`
3. Verify the signature every time per the official docs
4. Record the event id for idempotent handling — an email must never trigger twice

###### 5. Verify

> Goal: Confirm email really sends from the verified domain

1. Send a test email from the real from address and check the inbox/headers (SPF/DKIM pass)
2. Do `/run-verify` — if it fails → revert the changed keys, do `resolve-errors`, then report the diff

##### Rules

- The from address must use a verified domain — never `@resend.dev` in production
- Separate transactional vs marketing (use Broadcasts for marketing)
- Secrets only through `/follow-secret-manager`; never commit
- Retry with idempotency — never send duplicate emails
- If unsure about a DNS field/API → check official docs or `learn` (web)

##### Expected Outcome

- Domain verified with SPF/DKIM passing
- `EMAIL_FROM` clear and using a verified domain
- Templates really send and webhooks (if any) are secure

### setup-resend

##### Goal

Install the Resend SDK, create an API key from the dashboard, and init the client so it can send transactional email — first-time setup only

##### Scope

- Install the `resend` package and init `new Resend(apiKey)`
- Create and store `RESEND_API_KEY` securely
- Send a test email in sandbox mode
- Does not cover domain verification, from-address, webhooks → use `## Merged Details → config-resend`

##### Execute

###### 1. Check Prerequisites

> Goal: Confirm the current state before installing (idempotent)

1. Read `package.json` to identify runtime and package manager
2. Check whether `resend` is already installed → if so, skip to verify
3. Do `/check-secrets env-vars` to see whether `RESEND_API_KEY` already exists
4. If there is no Resend account → stop and tell the user to create one from the dashboard

###### 2. Install SDK

> Goal: Install the package per runtime

1. Node/Bun: `bun add resend` (or the detected package manager)
2. Other languages (Python, Go, etc.) → check official docs
3. Confirm the dependency is in `package.json`

###### 3. Create And Store API Key

> Goal: Prepare the API key securely

1. Create an API key from the Resend Dashboard — use `/open-web-for-config-secret` (service resend)
2. Pick the minimum required permission (e.g. sending access only)
3. Store `RESEND_API_KEY` in `/follow-secret-manager`, then inject it into the environment — never commit

###### 4. Init Client And Smoke Test

> Goal: Init the client and send a test email

1. Create the client with `new Resend(process.env.RESEND_API_KEY)` server-side only
2. Send a test email with `resend.emails.send({ from, to, subject, html })` — before domain verification use `onboarding@resend.dev` as the from
3. Check the response `id` confirms the send — if it errors → do `resolve-errors` max 3 rounds
4. Do `/run-verify` for lint, typecheck

##### Rules

- Never hardcode the API key or commit secrets — always use `/follow-secret-manager`
- The client must stay server-side only — never expose `RESEND_API_KEY` to the browser
- `onboarding@resend.dev` is for sandbox/testing only — production needs a verified domain
- If unsure about an API/method → check official docs or `learn` (web)

##### Expected Outcome

- `resend` SDK installed and present in `package.json`
- `RESEND_API_KEY` secure and correctly injected
- Test email sent successfully and verify passes

### verify-connection

##### Goal

Confirm after setup/config that Resend really connects — `RESEND_API_KEY` valid, sending domain verified

##### Scope

- Used when `/follow-service-resend` dispatches to `verify`/`verify-connection`
- Read-only: check only — do not send real emails (the test send lives in the setup workflow)

##### Execute

###### 1. Check API Key

> Goal: `RESEND_API_KEY` exists and is valid

1. Check the env var has a value (do not print it)
2. Call `resend.domains.list()` — 200 = key valid, 401 = invalid

###### 2. Check Domain Status

> Goal: the sending domain is verified and ready

1. Find the domain used in `EMAIL_FROM` from the domains list
2. Flag any domain whose status is not `verified` — DNS records still incomplete
3. If there is no domain at all → sending only works via `onboarding@resend.dev`

###### 3. Report

> Goal: Summarize connection status

1. Use `/report` columns: `No.`, `Check`, `Result`, `Evidence`
2. Verdict: `connected` / `auth-failed` / `domain-unverified` / `no-domain`

##### Rules

- Use list/read calls only — never `resend.emails.send`
- Do not print the API key
- Domain unverified → report the missing DNS records for the config workflow to handle

##### Expected Outcome

- Connection verdict with domain status evidence

### references/package-manifest

#### Package Manifest

> Metadata of the primary package(s) this skill installs or covers. Update during `/update-devin-global-skills` or `/deep-review-codebase` runs.

##### Primary Package

| Field | Value |
|-------|-------|
| Package | `resend` |
| Registry | `npm` |
| Latest Version | `6.28.0` |
| Release Date | `2026-09-11` |
| Verified | `2026-09-12` (date this file was last checked) |
| Author / Publisher | Resend |
| License | `MIT` |
| Repository | `https://github.com/resend/resend-node` |
| Website | `https://resend.com/` |
| Documentation | `https://resend.com/docs` |
| Releases / Changelog | `https://github.com/resend/resend-node/releases` |

##### Install

```bash
bun add resend
```

##### Secondary Packages

| Package | Registry | Latest | Notes |
|---------|----------|--------|-------|
| `@react-email/components` | `npm` | `unknown` | Optional — React email templates for `react` field in `emails.send` |

##### Notes

- Breaking changes in latest major: none documented; `from` must use a verified domain in production
- Version pinned in SKILL.md: `6.28.0`

## Expected Outcome

- Library used correctly per best practices (service resend)
- No known security/performance pitfalls (service resend)
- Lint, typecheck, tests pass

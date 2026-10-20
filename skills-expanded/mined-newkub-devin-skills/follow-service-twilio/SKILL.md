---
name: follow-service-twilio
description: Use Twilio to send SMS/OTP/verify — Messaging, Verify API, webhooks
argument-hint: "[target-or-scope]"
related:
  - run-verify
  - run-test

---

## Goal

Use Twilio to send SMS/OTP/verify — Messaging, Verify API, webhooks

## Scope

Use when the task involves this library/tool — setup, usage, debugging, or best practices (service twilio)

## Execute

### Workflows

| Topic  | Workflow |
|--------|----------|
| Setup  | `## Merged Details → setup-twilio` — SDK install, Account SID/Auth Token |
| Config | `## Merged Details → config-twilio` — phone numbers, messaging service, webhook config |
| Verify | `## Merged Details → verify-connection` — account fetch responds, numbers ready |

Read `workflows/<name>/SKILL.md` per topic and follow the flow there — do not execute from this table directly

### 1. Setup And Usage

> Goal: Use it correctly per the official docs

Latest: `twilio@6.1.1` (verified 2026-09-12) — install with `bun add twilio`

1. Create the client with accountSid/authToken from env — never expose on the client side
1. Use the Verify API (`verify.v2.services().verifications`) for OTP — no need to manage codes yourself
1. Use Messaging (`messages.create`) for regular SMS — set messagingServiceSid
1. Receive status callbacks via webhook — verify the signature with the Twilio signature

### 2. Verify

> Goal: Confirm correct usage

1. Do `/run-verify` for lint, typecheck
2. Do `/run-test` if relevant tests exist
3. Check the latest official docs before using an uncertain API (service twilio)

## Rules

- Prefer the Verify API over self-managed OTP when possible
- Always verify webhook signatures
- Watch regional compliance (sender IDs, opt-out)
- Do not log message bodies containing PII/OTP

## Merged Details

### config-twilio

##### Goal

Set/edit Twilio configuration — phone numbers, Messaging Service, Verify Service, and webhook callbacks — merging with the existing config

##### Scope

- Covers env keys, messaging/verify service SIDs, and webhook endpoints
- If the SDK is not installed or credentials are missing → do `## Merged Details → setup-twilio` first
- Does not include buying real numbers — the user does that in the Twilio Console

##### Execute

###### 1. Read Current Config

> Goal: Know the current config before editing

1. Read the existing env keys: `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, `TWILIO_PHONE_NUMBER`, `TWILIO_MESSAGING_SERVICE_SID`, `TWILIO_VERIFY_SERVICE_SID`
2. Read the code that creates the client and the current webhook handlers
3. Do `/deep-review-codebase` domain `review-config` if env drift vs code must be known

###### 2. Configure Phone Numbers And Services

> Goal: Identify sender identities correctly

1. Set `TWILIO_PHONE_NUMBER` (E.164 format) or `TWILIO_MESSAGING_SERVICE_SID` for SMS
2. Set `TWILIO_VERIFY_SERVICE_SID` for OTP via the Verify API
3. Store all SIDs via `/follow-secret-manager` — merge with the existing env, never overwrite

###### 3. Configure Webhooks

> Goal: Receive callbacks securely

1. Set the status callback / inbound webhook URL in the Twilio Console (phone number or messaging service settings)
2. Create a webhook receiver route such as `/api/webhooks/twilio`
3. Verify the signature with `twilio.validateRequest` against `TWILIO_AUTH_TOKEN` on every request
4. Respond `200` immediately and process async — Twilio retries on timeout

###### 4. Verify

> Goal: config works for real

1. Send a test SMS or test OTP and watch the status callback hit the webhook
2. Do `/run-verify` and `/run-test` if relevant tests exist
3. If broken → revert the key just changed, then report the diff

##### Rules

- Edit only the necessary keys — never overwrite the whole env/config set
- Always verify webhook signatures — never trust a request unchecked
- Do not log message bodies containing PII/OTP
- Watch regional compliance (sender IDs, opt-out) — see official docs if unsure

##### Expected Outcome

- phone number/service SIDs correct and stored in the secret manager
- webhook route verifies signatures and receives callbacks
- test message/OTP sends successfully

### setup-twilio

##### Goal

Install the Twilio SDK and prepare credentials (Account SID, Auth Token) so the server can call the Twilio API — first-time setup, not ongoing config

##### Scope

- Install the `twilio` package and create the client server-side
- Set `TWILIO_ACCOUNT_SID` and `TWILIO_AUTH_TOKEN` via the secret manager
- If already set up → verify only; phone numbers/webhooks config → `## Merged Details → config-twilio`

##### Execute

###### 1. Check Prerequisites

> Goal: Confirm the project is ready and not yet set up

1. Check `package.json` for `twilio` already present — if present → skip to the verify step
2. Check env/secrets for `TWILIO_ACCOUNT_SID` and `TWILIO_AUTH_TOKEN`
3. If credentials are missing → do `/open-web-for-config-secret` pointing the user to the Twilio Console

###### 2. Install SDK

> Goal: Install the Twilio SDK server-side

1. Run `bun add twilio` (or the project's package manager)
2. Confirm the import works with `import twilio from 'twilio'`

###### 3. Configure Credentials

> Goal: Store credentials securely

1. Create/find the Account SID and Auth Token in the Twilio Console
2. Store `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN` via `/follow-secret-manager` — never commit or expose on the client side

###### 4. Create Client

> Goal: client singleton ready to use

1. Create the client with `twilio(accountSid, authToken)` reading from env server-side only
2. Run a smoke check such as `client.messages.list({ limit: 1 })` to confirm the auth works

###### 5. Verify

> Goal: the SDK actually works

1. Do `/run-verify` for lint, typecheck
2. If verify fails → do `/resolve-errors` max 3 rounds, then stop and report
3. Success → do `/suggest-next-action`

##### Rules

- Never hardcode or commit the Account SID/Auth Token
- The client must live server-side only — never bundle it into a client
- Use official docs as the primary source; if unsure → see https://www.twilio.com/docs

##### Expected Outcome

- `twilio` installed and the client works server-side
- credentials live in the secret manager, none in code
- smoke check passes — ready for `## Merged Details → config-twilio`

### verify-connection

##### Goal

Confirm after setup/config that Twilio really connects — Account SID/Auth Token valid, messaging service/numbers ready

##### Scope

- Used when `/follow-service-twilio` dispatches to `verify`/`verify-connection`
- Read-only: check only — do not send SMS/calls

##### Execute

###### 1. Check Credentials

> Goal: SID and token all present

1. Check `TWILIO_ACCOUNT_SID` (`AC...` format) and `TWILIO_AUTH_TOKEN` exist (do not print values)
2. If a messaging service is used → `TWILIO_MESSAGING_SERVICE_SID` (`MG...`) exists

###### 2. Smoke Test API Call

> Goal: account fetch responds

1. `twilio api:core:v2010:accounts:fetch` or `client.api.accounts(sid).fetch()`
2. 200 = credentials valid; 401 = invalid token, 404 = wrong SID
3. Record the account status (`active`/`suspended`)

###### 3. Check Numbers And Webhooks

> Goal: sending capability ready

1. `client.incomingPhoneNumbers.list({limit: 5})` — numbers available to send from
2. Check the configured webhook URLs match the app endpoints
3. flag: no number, number without SMS capability

###### 4. Report

> Goal: Summarize connection status

1. Use `/report` columns: `No.`, `Check`, `Result`, `Evidence`
2. Verdict: `connected` / `auth-failed` / `no-numbers` / `webhook-mismatch`

##### Rules

- Use fetch/list calls only — never send a message/call
- Do not print the auth token
- suspended account = flag immediately

##### Expected Outcome

- Verdict with account status + numbers evidence

### references/package-manifest

#### Package Manifest

> Metadata of the primary package(s) this skill installs or covers. Update during `/update-devin-global-skills` or `/deep-review-codebase` runs.

##### Primary Package

| Field | Value |
|-------|-------|
| Package | `twilio` |
| Registry | `npm` |
| Latest Version | `6.1.1` |
| Release Date | `2026-09-10` |
| Verified | `2026-09-12` (date this file was last checked) |
| Author / Publisher | Twilio |
| License | `MIT` |
| Repository | `https://github.com/twilio/twilio-node` |
| Website | `https://www.twilio.com/` |
| Documentation | `https://www.twilio.com/docs/libraries/reference/twilio-node/` |
| Releases / Changelog | `https://github.com/twilio/twilio-node/releases` |

##### Install

```bash
bun add twilio
```

##### Secondary Packages

| Package | Registry | Latest | Notes |
|---------|----------|--------|-------|
| `twilio-cli` | `npm` | `unknown` | Optional CLI for local webhook testing / dev |

##### Notes

- Breaking changes in latest major: none documented for 6.x; use Verify API (`verify.v2`) instead of self-managed OTP
- Version pinned in SKILL.md: `6.1.1`

## Expected Outcome

- Library used correctly per best practices (service twilio)
- No known security/performance pitfalls (service twilio)
- Lint, typecheck, tests pass

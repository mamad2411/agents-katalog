---
name: twilio-cli-reference
version: 1.0.0
description: Practical reference for the official twilio CLI — login, profiles, phone numbers, messages, serverless, and plugins.
author: matrixx0070
tags: [twilio, cli, tooling, phone-numbers, serverless, api]
capabilities: []
---

## When to use

Use this when you want to drive Twilio from the terminal with the official `twilio` CLI — logging in, managing profiles/API keys, listing or configuring phone numbers, sending test messages, or deploying Serverless functions. Use it when you need the exact command and flag for a one-off operation instead of writing SDK code.

**Not for:** designing inbound webhook handlers — use twilio-webhook-architecture. Production error handling and backoff — use twilio-reliability-patterns. Log/alert investigation — use twilio-debugging-observability. Email is a separate product — use twilio-email-send.

## Method

1. Install the CLI. On macOS `brew tap twilio/brew && brew install twilio`; cross-platform via npm `npm install -g twilio-cli`. Verify with `twilio --version`.
2. Authenticate. Run `twilio login` and paste your Account SID + Auth Token; the CLI stores an API Key in the OS keychain under a named profile. Decision point: for CI/headless use, skip interactive login and export `TWILIO_ACCOUNT_SID` + `TWILIO_API_KEY` + `TWILIO_API_SECRET` (API Keys, never the raw Auth Token in scripts).
3. Manage profiles for multiple accounts/subaccounts: `twilio profiles:list`, `twilio profiles:use <id>`, `twilio profiles:create`. Switch per-command with `--profile <id>`.
4. Explore resources. `twilio phone-numbers:list` shows owned numbers; `twilio api:core:available-phone-numbers:local:list --country-code US --area-code 415` finds new ones; buy with `twilio api:core:incoming-phone-numbers:create --phone-number +1415...`.
5. Wire a number to your webhook: `twilio phone-numbers:update <PN_SID or +E164> --sms-url https://app.example.com/sms --voice-url https://app.example.com/voice`.
6. Send a message: `twilio api:core:messages:create --from +1415... --to +1650... --body "hello"`. Add `-o json` for scriptable output.
7. Use the local tunnel for dev: `twilio phone-numbers:update <number> --sms-url ...` pointed at an ngrok URL, or scaffold/deploy Functions with `twilio serverless:init`, `twilio serverless:deploy`.
8. Extend with plugins: `twilio plugins:install @twilio-labs/plugin-serverless`, `twilio plugins:install @twilio-labs/plugin-flex`. Enable shell completion with `twilio autocomplete`.
9. Prefer `--profile` and `-o json` in scripts for determinism; add `-l debug` to surface the underlying HTTP request when a command misbehaves.

## Example

```bash
# Install + authenticate
npm install -g twilio-cli
twilio login                       # stores an API Key in a named profile

# Profiles (multiple accounts / subaccounts)
twilio profiles:list
twilio profiles:use prod

# Numbers
twilio phone-numbers:list -o json
twilio api:core:available-phone-numbers:local:list --country-code US --area-code 415
twilio phone-numbers:update +14155551234 \
  --sms-url https://app.example.com/sms \
  --voice-url https://app.example.com/voice

# Send an SMS
twilio api:core:messages:create \
  --from +14155551234 --to +16505550100 --body "ping" -o json

# Serverless
twilio serverless:init my-service && cd my-service
twilio serverless:deploy

# Plugins + completion
twilio plugins:install @twilio-labs/plugin-serverless
twilio autocomplete zsh
```

## Pitfalls

- **Using the Auth Token in scripts.** `twilio login` provisions an API Key for a reason. In CI, set `TWILIO_API_KEY`/`TWILIO_API_SECRET`, not the Auth Token, so keys are revocable without rotating the account.
- **Wrong active profile.** Commands silently target whatever profile is active. Confirm with `twilio profiles:list` or pass `--profile` explicitly; a mis-set profile can send real messages from the wrong account.
- **Region/edge mismatch.** For non-US data residency set `TWILIO_REGION`/`TWILIO_EDGE` or `--region`; otherwise the CLI hits the default US1 region.
- **Human-formatted output in scripts.** Default table output is unstable to parse. Always add `-o json` and pipe through `jq`.
- **Stale plugins.** Serverless/Flex features live in plugins that version independently; run `twilio plugins:update` when a documented command is missing.
- **E.164 formatting.** `--from`/`--to` must be `+<countrycode><number>`; unformatted numbers raise error 21211.

## Output format

```
CLI: twilio v<version>  profile=<name>
CMD: <full command run>
RESULT: <SID or count>  status=<ok|error>
ERROR: <code + message, if any>
NEXT: <suggested follow-up command>
```

## Reference

- **Command grammar:** `twilio <namespace>:<resource>:<action> [--flags]`. The `api:core:*` tree mirrors the REST API 1:1 (e.g. `api:core:messages:create`, `api:core:calls:list`, `api:core:incoming-phone-numbers:update`).
- **Global flags:** `-o json|columns`, `-l debug|info` (log level), `--profile <id>`, `--region`/`--edge`, `--silent`.
- **Auth model:** login creates an API Key (`SK...`) + secret stored in the OS keychain; env vars `TWILIO_ACCOUNT_SID`, `TWILIO_API_KEY`, `TWILIO_API_SECRET`, or `TWILIO_AUTH_TOKEN` override the active profile.
- **Key namespaces:** `phone-numbers:*` (shortcuts for incoming numbers), `api:core:messages`, `api:core:calls`, `serverless:*`, `profiles:*`, `plugins:*`, `debugger:logs:list`, `autocomplete`.
- **Serverless plugin:** `serverless:init`, `serverless:deploy`, `serverless:logs` come from `@twilio-labs/plugin-serverless`.
- **Docs:** `twilio --help` and `twilio <namespace> --help` list every subcommand; the CLI is open source at github.com/twilio/twilio-cli.

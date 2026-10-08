---
name: opencorvus-matrix-channel-config
description: Guide official Matrix client setup for OpenCorvus, collect Matrix credentials from the user, and write them into OpenCorvus after the user provides them. Use when tasks involve Matrix access-token retrieval, homeserver setup, env wiring, or Matrix runtime verification.
---

# OpenCorvus Matrix Channel Config

## Overview

Guide the user through the official Matrix client-auth flow, stop for every provider-side action, and apply values to OpenCorvus only after the user pastes them.

## Workflow

1. Confirm mode.

- Default to overlay-guided setup in `Channel Config`.
- Offer text-guided fallback that writes to `packages/channel-runtime/.env`.
- Process one credential or sync setting at a time and wait for explicit confirmation after each manual step.

2. Load references.

- Read `packages/opencorvus/src/skill/builtin/channel/opencorvus-channel-config-wizard/references/channel-matrix.md`.
- Use only the `Matrix` section and the official Matrix URLs listed there.

3. Guide provider-side setup.

- Ask the user for the homeserver URL first.
- Ask the user to obtain an `access_token` from the official Matrix login flow or an admin-issued token.
- Ask for `MATRIX_SINCE_TOKEN` only if they want to resume from an existing sync checkpoint.
- Ask the user to add the bot account to the target room before validation.

4. Apply OpenCorvus config.

- When the user pastes a value, write it immediately instead of asking them to edit files themselves.
- Overlay mode: set `MATRIX_HOMESERVER_URL`, `MATRIX_ACCESS_TOKEN`, and optional `MATRIX_SINCE_TOKEN`, then click `Save Config`.
- Text fallback: update `packages/channel-runtime/.env` and keep unrelated keys unchanged.
- Redact secrets in summaries and confirmations.

5. Verify runtime.

- Confirm `packages/channel-runtime/src/main.ts` registers `MatrixAdapter`.
- Confirm `packages/channel-runtime/src/adapters/matrix.ts` matches the supplied homeserver flow.
- Run `bun run --cwd packages/channel-runtime --no-env-file --env-file .env src/main.ts`.
- Send one inbound Matrix message and confirm one reply.

6. Troubleshoot.

- If login or sync fails, re-check the homeserver URL and token audience.
- If replies fail, re-check room membership and access-token scope.
- If event replay looks wrong, re-check `MATRIX_SINCE_TOKEN`.

## Guardrails

- Do not claim full automation for Matrix account creation or homeserver admin operations.
- Do not output real secrets.
- Keep edits focused on overlay env values or `packages/channel-runtime/.env` unless the user asks for code changes.
- Do not claim parity features that the adapter does not implement.

## Output Format

1. Mode and current provider step.
2. Required official page and exact manual action.
3. Values received and env keys updated.
4. Verification result.
5. Next blocker or completion status.

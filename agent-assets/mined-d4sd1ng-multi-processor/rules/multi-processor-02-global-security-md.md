---
name: Global Security Rules
alwaysApply: true
description: Global security and secret-handling rules.
---

# Global Security Rules

## Secrets

Never expose, print, commit, return or log:

- API keys
- access tokens
- refresh tokens
- passwords
- private keys
- Authorization headers
- cookies
- `.env` secret values
- provider credentials

## Files

- Do not commit `.env` files.
- Do not commit local credentials.
- Do not write secrets into exported files.
- Do not include secrets in test snapshots.
- Do not include absolute private paths unless necessary for local tooling.

## External calls

- Do not add new external API calls unless explicitly required.
- Do not send user data to third-party services without clear scope.
- Do not add telemetry, analytics or tracking unless explicitly requested.

## Safety defaults

- Prefer read-only operations when inspecting.
- Ask before destructive actions if the intent is ambiguous.
- Do not delete files unless the task clearly requires it.
- Do not bypass checks, gates or validations.

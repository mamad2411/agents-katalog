---
name: follow-tool-fnox
description: Load secrets from encrypted files / vaults / cloud into app env via fnox.toml + fnox exec
argument-hint: "[scope]"
related:
  - follow-tool-mise
  - follow-tool-packslip
  - follow-tool-usage
  - check-secrets
  - follow-tool-gitleaks
  - setup-cicd
---

## Goal

Use `fnox` (jdx, Rust, MIT) to manage secrets in dev/CI — define each value's source in `fnox.toml` (committable, because it stores references/ciphertext, not plaintext) and inject them into the environment at run time

## Scope

- `fnox.toml` providers + secrets, `fnox exec`, `fnox set`, profiles, shell integration, daemon cache, temporary credentials (leases), agent proxy
- Not leak scanning — for leaked secrets use `/follow-tool-gitleaks` + `/check-secrets`
- Latest: v1.36.x — https://fnox.jdx.dev/

## Execute

### 1. Install

> Goal: fnox ready to use

1. `mise use -g fnox` (per `/follow-tool-mise`)
2. Verify `fnox --version`

### 2. Configure Providers + Secrets

> Goal: `fnox.toml` points each secret to its source

1. Encrypted-in-git (age):

```toml
[providers.age]
type = "age"
recipients = ["age1..."]

[secrets.DATABASE_URL]
provider = "age"
value = "<ciphertext>"   # written by fnox set
```

2. An existing vault (1Password example):

```toml
[providers.op]
type = "1password"
vault = "Engineering"

[secrets.DATABASE_URL]
provider = "op"
value = "Database/url"
```

3. Other providers: aws-sm, azure-sm, gcp-sm, bitwarden, vault — mixable per secret
4. `fnox set DATABASE_URL` writes the ciphertext/reference for you

### 3. Run With Secrets

> Goal: the app sees real env values without committing secrets

1. `fnox exec -- npm start` → env injected into that process only
2. Profiles: dev/staging/prod — switch sources without changing the run command
3. Shell integration: auto load/unload per directory (`guide/shell-integration`)
4. Daemon (opt-in): caches resolved values in memory across sessions
5. Leases: temporary credentials (AWS STS, GitHub Apps, Vault)
6. Agent proxy: hand placeholders to the agent, inject real values only into matching HTTPS requests

## Rules

- `fnox.toml` is committable — but never commit a plaintext `value`; use provider references or ciphertext only
- Pick the provider per team: existing vault → reference, none → age encryption
- local cache only via `fnox sync` (age) — never a plaintext fallback

## Expected Outcome

- `fnox.toml` committed in the repo, secrets resolved from provider/ciphertext
- `fnox exec -- <cmd>` in real use in dev and CI

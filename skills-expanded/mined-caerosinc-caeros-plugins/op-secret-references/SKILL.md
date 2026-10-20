---
name: op-secret-references
description: Replace plaintext secrets with op:// secret reference URIs in .env files, configs, and CI. Use when the user wants secrets out of their repo and environment files.
---

# 1Password secret references

A secret reference is a pointer, not a value:

```
op://<vault>/<item>/<field>
op://<vault>/<item>/<section>/<field>
```

Examples:

```
op://Dev Vault/Postgres/password
op://Dev Vault/Stripe/api keys/secret key
op://Prod/GitHub Deploy/private key
```

References are safe to commit, paste, and log. Only an authenticated `op`
process (or the desktop app integration) can resolve them.

## Getting the exact reference

Copy it from the desktop app (field menu > Copy Secret Reference), or build it
from CLI inspection:

```bash
op item get "Postgres" --vault "Dev Vault" --format json | jq '.fields[] | {label, reference}'
```

Names with spaces are fine unquoted inside the URI; quote the whole reference
in shells. If vault or item names churn, IDs also work in each segment.

## .env files that contain no secrets

```bash
# .env  (commit this: it holds pointers, not values)
DATABASE_URL="op://Dev Vault/App/db-url"
STRIPE_SECRET_KEY="op://Dev Vault/Stripe/secret key"
JWT_SIGNING_KEY="op://Dev Vault/App/jwt/signing key"
```

Run anything that needs them:

```bash
op run --env-file=.env -- npm run dev
```

Values exist only in the child process environment. For tools that must read a
real file, generate it transiently with `op inject -i .env.tpl -o .env.local`
and gitignore the output.

## Attribute queries

Append `?attribute=` for special values:

```
op://Dev Vault/GitHub/one-time password?attribute=otp   # current TOTP code
op://Dev Vault/TLS Cert/certificate?ssh-format=openssh  # key format conversion
```

## CI usage

Two supported patterns, both driven by `OP_SERVICE_ACCOUNT_TOKEN`:

1. **op run wrapper** (any CI):

```yaml
steps:
  - run: |
      curl -sSfLo op.zip <official 1Password CLI release> && unzip op.zip
      ./op run --env-file=.env.ci -- ./deploy.sh
    env:
      OP_SERVICE_ACCOUNT_TOKEN: ${{ secrets.OP_SERVICE_ACCOUNT_TOKEN }}
```

2. **Official load-secrets action** (GitHub Actions): map env vars to
   references and the action resolves them into the job:

```yaml
- uses: 1password/load-secrets-action@v2
  with:
    export-env: true
  env:
    OP_SERVICE_ACCOUNT_TOKEN: ${{ secrets.OP_SERVICE_ACCOUNT_TOKEN }}
    DATABASE_URL: op://CI/App/db-url
```

Either way, the CI system stores exactly one secret (the service account
token); everything else stays in 1Password and is fetched per run.

## Migration checklist (plaintext .env to references)

1. Create a vault per environment; create one item per service.
2. Move each value into a field; name fields after the env var's purpose.
3. Rewrite `.env` lines as `VAR="op://Vault/Item/field"`.
4. Switch start scripts to `op run --env-file=.env -- <cmd>`.
5. Rotate every value that ever sat in the repo or in CI variables: treat
   previously committed secrets as compromised.

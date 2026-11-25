---
name: setup-integrations
description: Use when setting up a new copy of the starter, when someone asks what third-party services, keys, IDs or accounts are needed, when turning on Sentry, Grafana Cloud, Apple, Google Play or hosting, or when code needs a new external key or setting.
---

# Set up integrations

Read [ADR-0009](../../../docs/adr/0009-third-party-configuration.md). Nothing here is required to build, run or test the product.

## A new copy of the starter

Do these in order and tell the person what each one does before running it:

1. `gh auth login` (they must be an admin of the repository).
2. `node scripts/setup.mjs repo --dry-run`, then `node scripts/setup.mjs repo`. Report any step that failed and how to set it by hand in **Settings**.
3. The `rename-product` skill, if they have a product name.
4. `node scripts/setup.mjs` and walk through what is off. Ask which services they want now; leave the rest off.

## Turn a service on

1. Show the steps and sign-up link from `node scripts/setup.mjs` (they come from `config/integrations.json`). The person creates the account; never create accounts or type passwords for them.
2. For SYST and Prod: `node scripts/setup.mjs set <KEY> --env Syst` (and `Prod`). Secrets are prompted without echo; never paste a secret into chat or a file.
3. To try it locally: put the key in `.env.local` at the repository root (copy `.env.example`), then rebuild the app.
4. Check: run `node scripts/setup.mjs` again; the setting should show as set.

## Add a new integration to the code

1. Add an entry to `config/integrations.json`: id, name, purpose, `when` (`optional` or `publish`), cost, sign-up link, guide, steps, and settings (`key`, `app`, `secret`, `environments`, `label`).
2. Add each key to `.env.example`, empty, with a comment.
3. Read it the same way as the others: Vite `define` from `loadEnv(mode, repoRoot, '')`, a Gradle `buildConfigField` through `integration("KEY")`, `node scripts/setup.mjs ios-xcconfig` for iOS, or `IConfiguration` in the backend.
4. Off when empty: the feature must work, and tests must pass, without a value.
5. Document it in the README table under "Make it yours" and run `node --test scripts/setup.test.mjs`.

## Never

* Commit a real key, DSN, token or `google-services.json`, even for Dev.
* Make a third-party service required for the build, the tests or CI.
* Put customer data in a third-party service without the person agreeing to it.

---
name: expo-eas
description: >
  Reusable patterns for builds and deploys of React Native apps with Expo EAS.
  Invoke automatically when configuring EAS, creating build profiles, submitting
  to stores, configuring OTA updates, or managing EAS secrets.
---

# Expo EAS — Mobile Builds and Deploy

## Read the project's real `eas.json` first

Everything below is a **generic reusable template**. A real project's `eas.json` often
diverges (the project's delta skill / infra doc should record how) — check it before applying
anything here. Gotchas that apply to any project:

- **Two ways to inject env vars — know which one the project uses.** Either literal `env`
  blocks per profile in `eas.json` (e.g. each profile sets `EXPO_PUBLIC_API_URL` directly), or
  an `APP_ENV` key branched on in `app.config.ts` (template below). Don't mix them silently.
  Either way, an `EXPO_PUBLIC_*` value only reaches the bundle where the code spells out
  `process.env.EXPO_PUBLIC_X` literally (see `dev-patterns:logging-observability` → "Sentry in the
  clients").
- **EAS Environments (`eas env:*`) are a separate, easy-to-confuse mechanism.** `eas update
  --environment <name>` / a build pulls vars from a named EAS Environment ONLY if the invoking
  profile (or an explicit `--environment` flag) references that name. If no profile does,
  editing an EAS Environment affects no real build/update — the profile's own `env` block is
  what actually ships.
- **Custom EAS Environment names require a paid plan.** Only `production`/`preview`/`development`
  are valid `--environment` values on the free tier; `eas env:create --environment staging`
  fails with "Custom environments are supported on Production and Enterprise plans".
- **A profile with `"ios": { "simulator": true }` can never install on a real phone.** The
  channel that physical test devices track must come from a non-simulator profile.
- **Decide explicitly which update channel CI auto-publishes** (e.g. `eas update --branch
  staging` on every push to the deploy branch, with env values inline in the workflow) and
  which channels are manual-only — and document it.

## Initial setup

```bash
npm install -g eas-cli@<x.y.z>   # a recent eas-cli, pinned — the same version CI installs
eas login
eas build:configure   # generates initial eas.json
```

---

## eas.json — recommended structure

```json
{
  "cli": { "version": ">= X.Y.Z" },
  "build": {
    "development": {
      "developmentClient": true,
      "distribution": "internal",
      "env": { "APP_ENV": "development" }
    },
    "staging": {
      "distribution": "internal",
      "env": { "APP_ENV": "staging" },
      "ios": { "simulator": false },
      "android": { "buildType": "apk" }
    },
    "production": {
      "env": { "APP_ENV": "production" },
      "ios": { "autoIncrement": true },
      "android": { "autoIncrement": true }
    }
  },
  "submit": {
    "production": {
      "ios": { "appleId": "you@example.com" },
      "android": { "serviceAccountKeyPath": "./google-service-account.json" }
    }
  }
}
```

`cli.version`: set the floor to the recent eas-cli version the team and CI actually use (CI
installs that exact version, pinned) and raise it deliberately — a years-old floor lets any
outdated local CLI build the app.

---

## Build flow

```bash
# Daily development — hot reload on device
expo start --dev-client

# Staging — internal distribution for testing
eas build --platform all --profile staging

# Production — submit to stores
eas build --platform all --profile production
eas submit --platform all --profile production
```

---

## OTA Updates — without going through the stores

Only for JavaScript changes. Native code changes require a new build.

```bash
# Urgent production fix
eas update --branch production --message "fix: describe the fix"

# Staging update
eas update --branch staging --message "feat: new feature"

# OTA rollback
eas update:rollback --branch production
```

**Rule:** OTA only for JS. New permissions, native libs, or changes to
`app.json` require a new build and submit.

### `runtimeVersion` — use the `fingerprint` policy

The rule above should be enforced by the tooling, not by memory. Set:

```json
"runtimeVersion": { "policy": "fingerprint" }
```

`fingerprint` hashes everything that affects native code (native deps,
config plugins, native-relevant app config). An update only reaches binaries
with the **same** fingerprint, so a PR that changes native code — even an SDK
*patch* bump that moves `expo-modules-core` — holds its OTA back until a new
build is installed, instead of shipping new JS to an old native binary.

Avoid `sdkVersion`: every update reaches every binary of the same SDK, so an
automatic `eas update` on merge (a common CI setup) can push JS that expects
newer native modules to phones that don't have them.

**Pitfall — volatile values in the Expo config.** If `app.config.js` injects
values that change on every run into the config (e.g. `extra.gitSha`,
`extra.buildTime` for a version label), the fingerprint changes on every
build and every `eas update`, and **no OTA ever applies**. Skip the `extra`
section (read only by JS) in `fingerprint.config.js`:

```js
/** @type {import('expo/fingerprint').Config} */
module.exports = {
  // Defining sourceSkips replaces the default, so keep it explicitly.
  sourceSkips: ['PackageJsonAndroidAndIosScriptsIfNotContainRun', 'ExpoConfigExtraSection'],
  // + 'PackageJsonScriptsAll' when no script alters native code (see the pitfall below)
};
```

**Pitfall — `package.json` scripts are part of the fingerprint.** By default the fingerprint
hashes the app's `scripts` (a `postinstall` could change native code), so merely adding a
`lint`/`type-check` script changes the runtime version and silently holds back every OTA until a
new build. If no script touches native code (no `postinstall`, `prepare` or `eas-build-*` hooks),
add `'PackageJsonScriptsAll'` to `sourceSkips` — and remove it the day such a hook appears. To see
what moved: `npx expo-updates runtimeversion:resolve --platform ios` → `fingerprintSources`, and
compare `eas update:list --branch <branch>` runtime versions over time.

**Pitfall — `eas.json` is part of the fingerprint.** Any edit to it (even an `android` block
in a profile used only for Android) changes the runtime version of *every* platform, so iOS OTAs
stop reaching installed builds until a rebuild. Don't edit `eas.json` while testers depend on OTAs —
batch it with the next planned native build. Note that a profile with `"distribution": "internal"`
already makes EAS build an installable Android **APK**; `android.buildType: "apk"` is redundant there.

**Pitfall — any lockfile rewrite can move the runtime.** The fingerprint hashes the native
modules as they are actually resolved (autolinking, their versions, config plugins), not just
the app's `package.json`. A lockfile-only change — `pnpm update`/`dedupe`, a Dependabot bump of
an unrelated package, reinstalling with a different pnpm version — can resolve a native module
or config plugin to another version and change the runtime version with no visible
`package.json` diff, holding back every OTA until a new build. Treat every lockfile change in a
PR as potentially native: compare `runtimeversion:resolve` before and after, and batch lockfile
rewrites with the next planned native build when testers depend on OTAs.

**Verify before relying on it** — the value must be identical across runs and
across the environments that build (EAS) and publish (CI):

```bash
npx expo-updates runtimeversion:resolve --platform ios   # run twice; also with CI env vars set
eas update:list --branch <branch> --limit 1 --json        # runtime version CI actually published
```

Switching an existing app from another policy to `fingerprint` changes its
runtime version: installed binaries stop receiving OTAs (safely) until a new
build is installed — plan one build per channel right after the switch.

In a pnpm monorepo, a stale incremental install can leave a package unlinked
(e.g. `@expo/config-plugins`, used by third-party config plugins without
declaring it) and make `runtimeversion:resolve` fail with "Cannot find
module" locally while CI/EAS (clean installs) work — reinstall from scratch.

---

## EAS environment variables

Secrets are stored in EAS, never in committed files. The `eas secret:*` commands are
superseded by **`eas env:*`**: variables belong to an EAS environment (`development`,
`preview`, `production`) and have a visibility (`plaintext`, `sensitive`, `secret`). A build
profile picks its environment with `"environment": "<name>"` in `eas.json`.

```bash
# Create a variable in an environment (secret = never readable back, not printed in logs)
eas env:create --name SECRET_NAME --value "value" --environment production --visibility secret

# List variables of an environment
eas env:list --environment production

# Pull non-secret values into a local .env for development
eas env:pull --environment development

# Delete a variable
eas env:delete --name SECRET_NAME --environment production
```

Run `eas env:create --help` on the pinned CLI version — flags evolve between releases.

Access in `app.config.ts`:

```typescript
export default {
  extra: {
    apiUrl: process.env.API_URL,
    sentryDsn: process.env.SENTRY_DSN,
  },
};
```

---

## app.config.ts — dynamic configuration per environment

```typescript
// apps/mobile/app.config.ts
const ENV = process.env.APP_ENV ?? 'development';

const configs = {
  development: {
    apiUrl: 'http://localhost:3000',
    sentryDsn: '',
  },
  staging: {
    apiUrl: process.env.API_URL_STAGING,
    sentryDsn: process.env.SENTRY_DSN,
  },
  production: {
    apiUrl: process.env.API_URL_PRODUCTION,
    sentryDsn: process.env.SENTRY_DSN,
  },
};

export default {
  name: 'AppName',
  slug: 'app-name',
  version: '1.0.0',
  extra: configs[ENV],
};
```

---

## GitHub Actions integration

```yaml
- name: Build and submit (production)
  run: |
    npm install -g eas-cli@<x.y.z>   # pinned — an unpinned install hands EXPO_TOKEN to whatever was published last
    eas build --platform all --profile production --non-interactive
    eas submit --platform all --profile production --non-interactive
  env:
    EXPO_TOKEN: ${{ secrets.EXPO_TOKEN }}
```

---

## Free tier limits

```
30 builds/month (iOS + Android combined)
1 concurrent build
```

**Trigger for Production ($99/month):** > 30 builds/month or need for concurrent builds.

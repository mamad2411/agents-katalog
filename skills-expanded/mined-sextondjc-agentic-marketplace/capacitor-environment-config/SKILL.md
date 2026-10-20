---
name: capacitor-environment-config
description: Use when managing per-environment configuration in a CapacitorJS app including build-time env injection, capacitor.config.ts variants, runtime config strategies, native-layer per-environment values, and secret hygiene.
---

# Capacitor Environment Config

## Specialization

Design and implement a deterministic per-environment configuration strategy for CapacitorJS applications. Covers the full stack: build-tool `.env` files, build-time injection into the web bundle, `capacitor.config.ts` variants, runtime config loading, and native-layer per-environment values (bundle IDs, app IDs, server URLs, signing identities).

## Scope Boundaries

In scope:

- `.env` file strategy for local, dev, staging, and production environments.
- Build-tool env injection: Vite (`import.meta.env`), webpack (`process.env`), Angular environments.
- `capacitor.config.ts` per-environment overrides (server URL, app ID, app name, plugins).
- Runtime config loading patterns: API-served config, bundled JSON, feature flags.
- Native-layer per-environment configuration: iOS `xcconfig` files, Android `build.gradle` product flavors.
- Secret hygiene: what belongs in `.env`, what belongs in a secret manager, what must never be bundled.
- CI-side config injection without checked-in secrets.
- Environment switching without full rebuild where feasible.

Out of scope:

- Secret manager implementation beyond guidance on patterns (no direct Vault / AWS Secrets integration code).
- CI/CD pipeline authoring beyond env var injection guidance (`capacitor-ci-integration`).
- Full security hardening (`capacitor-security`).
- OTA live-update channel selection per environment (`capacitor-live-updates`).

## Trigger Conditions

- The app must behave differently across local, dev, staging, and production without source changes.
- A secret or API base URL was discovered hardcoded in source or committed to version control.
- The team needs different app IDs or bundle IDs per environment for simultaneous installation.
- CI fails because a required environment variable is missing or incorrectly injected.
- A runtime config strategy is needed because certain values are not known at build time.
- An audit requires evidence that secrets are not bundled in the distributed artifact.

## Inputs

- Build tool in use: Vite, webpack, Angular CLI, or other.
- Target environments: local, dev, staging, production (and any additional).
- Config values that differ per environment (API base URL, app ID, feature flags, etc.).
- Which values are secrets vs. non-sensitive config.
- Whether different bundle IDs / app IDs per environment are required.
- CI platform (GitHub Actions, Azure Pipelines, etc.).
- Evaluation date in ISO format (`YYYY-MM-DD`).

## Required Outputs

- `.env` file schema with annotated sensitivity classification per variable.
- Build-time injection pattern appropriate for the build tool.
- `capacitor.config.ts` variant strategy (function-based or env-driven export).
- Native-layer environment config: iOS `xcconfig` and Android `build.gradle` guidance.
- Secret hygiene checklist (what never goes in source; `.gitignore` rules).
- CI injection pattern for each required environment.
- Runtime config pattern if required (API-served or bundled JSON).
- Rejected-candidate table with deterministic reason codes.
- Closure check: no secrets in source; all environments build cleanly.

## Depth Modes

| Level | Intent | Exit Rule |
|---|---|---|
| L1 Orientation | Identify config categories and choose injection strategy | Strategy decision documented |
| L2 Delivery | Implement `.env` files, build-time injection, and `capacitor.config.ts` variants | App builds cleanly in at least two environments |
| L3 Hardening | Add native-layer per-environment config, CI injection, and secret hygiene audit | All environments build in CI; no secrets in source; secret hygiene checklist passes |
| L4 Expert Standardization | Reusable environment config model for multi-team, multi-app compendium use | Config model documented with templates for each environment tier |

## Deterministic Workflow

1. Inventory all config values that differ across environments; classify each as secret, sensitive, or non-sensitive.
2. Define the environment tier set: local, dev, staging, production.
3. Choose injection strategy per build tool (see patterns below).
4. Author `.env.<environment>` files; add all to `.gitignore`; commit `.env.example` with placeholder values and type annotations.
5. Update `capacitor.config.ts` to read the environment and produce the correct per-environment output.
6. Configure native-layer overrides for values that must differ in the native project (bundle ID, server URL, signing).
7. Define CI injection: environment variables come from the CI secret store, never from committed files.
8. If any value is not known at build time, implement a runtime config fetch from a secured endpoint.
9. Run a secret hygiene scan to confirm no secrets exist in the distributed artifact or git history.
10. Document the config inventory with owner and rotation policy for each secret.

## Vite Injection Pattern

```typescript
// .env.production
VITE_API_BASE_URL=https://api.example.com
VITE_FEATURE_FLAGS_URL=https://flags.example.com

// src/config.ts
export const config = {
  apiBaseUrl: import.meta.env.VITE_API_BASE_URL,
  featureFlagsUrl: import.meta.env.VITE_FEATURE_FLAGS_URL,
} as const;
```

## capacitor.config.ts Variant Pattern

```typescript
// capacitor.config.ts
import type { CapacitorConfig } from '@capacitor/cli';

const env = process.env.APP_ENV ?? 'local';

const serverConfig: Record<string, Partial<CapacitorConfig>> = {
  local:      { server: { url: 'http://localhost:5173', cleartext: true } },
  dev:        { server: { url: 'https://dev.example.com' } },
  staging:    { server: { url: 'https://staging.example.com' } },
  production: {},  // no server override — uses bundled assets
};

const config: CapacitorConfig = {
  appId:     process.env.APP_ID    ?? 'com.example.app.local',
  appName:   process.env.APP_NAME  ?? 'MyApp (Local)',
  webDir:    'dist',
  ...serverConfig[env],
};

export default config;
```

## iOS xcconfig Pattern

```
// ios/App/Config/Dev.xcconfig
APP_BUNDLE_ID = com.example.app.dev
APP_DISPLAY_NAME = MyApp Dev
API_BASE_URL = https://dev.example.com
```

## Android Product Flavor Pattern

```groovy
// android/app/build.gradle
android {
  flavorDimensions "env"
  productFlavors {
    dev {
      applicationId "com.example.app.dev"
      resValue "string", "app_name", "MyApp Dev"
      buildConfigField "String", "API_BASE_URL", '"https://dev.example.com"'
    }
    production {
      applicationId "com.example.app"
      resValue "string", "app_name", "MyApp"
      buildConfigField "String", "API_BASE_URL", '"https://api.example.com"'
    }
  }
}
```

## Secret Hygiene Checklist

- [ ] All `.env.*` files are in `.gitignore` except `.env.example`.
- [ ] `.env.example` contains placeholder values, not real secrets.
- [ ] No API keys, tokens, or passwords appear in any tracked file.
- [ ] `git log -p | grep -E "(API_KEY|SECRET|PASSWORD|TOKEN)"` returns no hits.
- [ ] CI secret store (GitHub Actions secrets, Azure Key Vault, etc.) is the sole source of production secrets.
- [ ] Each secret has a named owner and a documented rotation policy.
- [ ] Bundle artifact does not contain production secrets (verify with `strings` or bundle analysis).

## Quality Gates

- App builds and runs correctly in all defined environment tiers.
- `capacitor.config.ts` produces correct `appId`, `appName`, and server config per environment.
- iOS and Android builds use correct bundle/application IDs per environment.
- No secrets are present in tracked source files or the distributed artifact.
- CI injects secrets from the secret store; no hardcoded values in workflow YAML.
- Config inventory exists with sensitivity classification, owner, and rotation policy per entry.

## Done Criteria

- All config variables are inventoried and classified.
- `.env` file schema is documented; `.env.example` is committed; all live `.env` files are gitignored.
- `capacitor.config.ts` produces correct per-environment output.
- Native-layer per-environment config is in place for each target platform.
- Secret hygiene checklist passes; no secrets in source or artifact.
- CI injects all required environment variables from the secret store.
- Config model is documented with owner assignments and rotation policy.

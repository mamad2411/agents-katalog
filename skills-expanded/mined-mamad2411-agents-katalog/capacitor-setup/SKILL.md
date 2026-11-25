---
name: capacitor-setup
description: Use when initializing, configuring, or auditing a CapacitorJS project including platform registration, capacitor.config.ts authoring, sync workflows, and build pipeline integration.
---

# Capacitor Setup

## Specialization

Produce a production-ready CapacitorJS project configuration covering platform registration, `capacitor.config.ts` governance, sync and copy workflows, and build-pipeline integration with the host web framework.

## Scope Boundaries

In scope:

- New CapacitorJS project initialization into an existing web app (React, Vue, Angular, SvelteKit).
- `capacitor.config.ts` or `capacitor.config.json` authoring and validation.
- iOS and Android platform registration and initial native project generation.
- `npx cap sync`, `npx cap copy`, and `npx cap open` workflow governance.
- Build tool integration (Vite, Webpack, rollup) and `webDir` alignment.
- AppId and bundle ID convention enforcement.

Out of scope:

- Custom plugin authoring (see `capacitor-plugin-authoring`).
- Native UI theming beyond Capacitor-controlled splash and status bar config.
- App Store or Play Store submission (see `capacitor-release-readiness`).

## Trigger Conditions

- Adding Capacitor to an existing web project for the first time.
- Adding a new platform (iOS or Android) to an existing Capacitor project.
- Auditing or correcting a `capacitor.config.ts` file.
- Diagnosing sync or copy failures between web and native projects.
- Integrating Capacitor's native build output into a CI/CD pipeline.

## Inputs

- Web framework in use (React, Vue, Angular, SvelteKit, or other).
- Build tool and `webDir` path (e.g., `dist`, `build`, `.svelte-kit/output/client`).
- Target platforms: iOS, Android, or both.
- AppId convention (reverse-domain, e.g., `com.example.myapp`).
- Evaluation date in ISO format (`YYYY-MM-DD`).

## Required Outputs

- Validated `capacitor.config.ts` with correct `appId`, `appName`, `webDir`, and `server` configuration.
- Confirmed platform registration commands and expected output.
- Sync workflow recommendation with explicit pre- and post-sync steps.
- Build pipeline integration plan aligned to the host framework's output directory.
- Residual risks and open actions with owners.

## Depth Modes

| Level | Intent | Stop Rule |
|---|---|---|
| L1 Orientation | Understand Capacitor setup basics | Config file exists and one platform is registered |
| L2 Practical Setup | Ship a working iOS and Android project | Both platforms sync cleanly from a framework build |
| L3 CI Integration | Automate sync within a pipeline | CI produces native builds reproducibly |
| L4 Expert Governance | Enforce config standards across projects | Config schema is validated in CI and documented |

## Deterministic Workflow

1. Confirm web framework, build tool, and output directory.
2. Install `@capacitor/core` and `@capacitor/cli` at the correct version; pin in `package.json`.
3. Run `npx cap init` or validate an existing init; confirm `appId` follows reverse-domain convention.
4. Author or validate `capacitor.config.ts`: `appId`, `appName`, `webDir`, `loggingBehavior`, and `server` block.
5. Register target platforms: `npx cap add ios` and/or `npx cap add android`.
6. Execute one full build of the web app, then `npx cap sync` to verify asset transfer.
7. Confirm native IDE can open the project: `npx cap open ios` and/or `npx cap open android`.
8. Define the sync cadence for CI: build web → `cap sync` → native build.
9. Document residual risks, known platform quirks, and follow-up actions.

## Configuration Checklist

- `appId` is a valid reverse-domain identifier with no generic or placeholder segments.
- `webDir` exactly matches the framework's build output path.
- `loggingBehavior` is set to `none` for production builds.
- `server.url` is only present for live-reload development; not committed for production.
- `plugins` block entries are justified and documented.
- `ios.scheme` and `android.path` are correct when non-default paths are used.

## Sync Workflow Rules

- Always build the web project before running `cap sync`.
- Use `cap copy` only when native plugin changes have not occurred; use `cap sync` otherwise.
- Commit native project files (`ios/` and `android/`) to version control.
- Treat the native projects as build outputs from `cap add`; do not manually edit native files that Capacitor regenerates.
- Pin the Capacitor CLI and core versions identically across `package.json` and native plugin dependencies.

## Quality Gates

- `cap sync` completes without warnings or errors on a clean framework build.
- The `appId` in `capacitor.config.ts` matches the bundle identifier in the native project.
- No `server.url` override is present in the committed config.
- CI produces a reproducible native build from a clean checkout.

## Done Criteria

- Both target platforms sync cleanly from the configured build pipeline.
- `capacitor.config.ts` passes the configuration checklist.
- CI integration plan is documented and tested.
- Residual risks are explicit and owner-assigned.

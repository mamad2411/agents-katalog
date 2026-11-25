---
name: flutter-app
description: Bootstrap a new Flutter mobile app with clean architecture, Riverpod, FVM-pinned SDK, current packages, and no deprecated APIs. Use when the user wants to start, scaffold, or set up a new Flutter app, a cross-platform mobile app, an Android or iOS app in Dart, or asks to "create a new flutter app". Handles BYOK LLM apps, backend-backed apps, Play Store release setup, and clean-architecture feature structure.
---

# flutter-app

Bootstrap a new Flutter app the way this owner builds them: FVM-pinned SDK, clean
architecture (feature-first), Riverpod for state, an Either/Failure error model,
current stable packages, and the house git and CI workflow with release-please
and Play Store delivery.

First read the shared rules (they override anything you remember):
`../shared/house-rules.md`, `../shared/no-ai-attribution.md`,
`../shared/git-and-ci.md`, `../shared/docs-and-context.md`,
`../shared/hardening.md`, and (for public repos) `../shared/open-source-docs.md`.

## Step 0. Get the brief, then ask the variant questions (hard stop)

This is a hard stop. Do not run any scaffolding command until the user has
answered.

First, get the project brief: one paragraph on what the app does, its main
features, target users, and any hard constraints. If the user has not given one,
ask for it. The brief drives naming, the feature list, and the data model.

Then ask the variant questions. If a choice has multiple options, ask; do not
assume. Ask in one batch, then proceed.

1. Repo visibility: private, open-source, or private-plus-open-source.
2. Backend: BYOK (each user supplies their own LLM key, no backend), a custom
   backend (Dio + JWT auth), or none yet. See `references/architecture.md`.
3. State codegen: Riverpod with codegen (`@riverpod` + build_runner) or plain
   Riverpod with hand-written providers. Default: codegen.
4. Local data: Drift, Isar, shared_preferences only, or none yet.
5. Auth: Google Sign-In, none, or backend-driven.
6. Release target: Play Store (default), App Store, or both.

If the user already answered some, do not re-ask.

## Step 1. Pin the SDK with FVM and verify versions

- Use FVM so the SDK is pinned per project: `fvm use stable` (or a specific
  stable). Every command runs through `fvm flutter ...`.
- Run `fvm flutter --version` and record the real Flutter and Dart versions in
  the project docs.
- Run `scripts/check-latest.sh` for current stable package versions from pub.dev.
  Pin those, not versions from memory (`../shared/house-rules.md` rule 2).
- Pull current docs for Flutter, Riverpod, and any codegen packages via Context7
  before writing code (`../shared/docs-and-context.md`). Riverpod's provider
  syntax and codegen naming change between majors; confirm before writing.

## Step 2. Scaffold with the official CLI

```
fvm flutter create --org com.<owner>.<app> --platforms=android,ios <name>
```

Then add dependencies from `references/stack.md` and lay out the folders from
`references/architecture.md`.

## Step 3. Apply architecture and conventions

- Clean-architecture layers, feature structure, Either/Failure model, DI, and the
  non-negotiable conventions (use cases, datasource interface plus impl, custom
  widgets, extensions, central utils, constants for everything, zero hardcoding):
  `references/architecture.md`.
- Riverpod and Flutter do's and don'ts, and code smells to avoid:
  `references/best-practices.md`.
- Dependency set and pinning notes (some packages must be pinned to avoid
  analyzer conflicts): `references/stack.md`.
- Production hardening (obfuscated release builds, no baked-in secrets, no debug
  symbols in git): `../shared/hardening.md`.

## Step 4. Git, CI, release, docs, security

- Git branch model, conventional commits, auto-merge, release-please:
  `../shared/git-and-ci.md`.
- CI (analyze + test), signing, and Play Store delivery:
  `references/quality-gates.md`.
- Gitignore signing keys, keystore, `google-services.json`, and `.env*`. Store
  them as CI secrets. Provide `.env.example`.
- Add `docs/` (git-workflow, architecture, release-process) and a README. For a
  public repo, ship the full open-source docs set per
  `../shared/open-source-docs.md` and run the open-source hard gate in
  `../shared/no-ai-attribution.md` before the first push.

## Step 5. Verify before declaring done

Run the gates in `references/quality-gates.md`: `fvm flutter analyze` must be
zero issues, `fvm flutter test` green, and the app must build and run. Report
real results.

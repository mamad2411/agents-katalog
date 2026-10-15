---
name: migration-webapp-to-flutter
description: "Trigger: migrar webapp a Flutter, convertir React/Vue/Svelte/Angular a Flutter, webapp to mobile app. Guía migración incremental."
license: Apache-2.0
metadata:
  author: senasdesktop
  version: "1.0.0"
---

## Activation Contract

Use this skill when migrating an existing React, Vue, Svelte, Angular, or similar webapp to native Flutter, especially when the user wants an incremental migration that keeps the web version alive during the transition.

## Hard Rules

- Do not treat the migration as a rewrite; migrate feature by feature and keep the webapp working.
- Analyze user-facing features before files; a feature may span domain, state, UI, and API code.
- Migrate domain models and pure logic before UI widgets.
- Keep backend APIs and data contracts unchanged unless the user explicitly asks otherwise.
- Use a WebView shell only when the webapp is already deployed and the user needs a working app from day one.
- For each migrated feature, hide the duplicated web section in the WebView and show the native Flutter version.
- Keep `domain/` free of Flutter imports; UI belongs in `features/` or `widgets/`.
- Prefer simple `StatefulWidget` state; do not add Provider, Riverpod, BLoC, or Redux unless the app clearly needs it.

## Decision Gates

| Situation | Action |
|---|---|
| Webapp deployed and must keep working | Start with a Flutter WebView shell and feature flags. |
| Full native migration requested | Still migrate in feature order; remove WebView only after all features are native. |
| Feature has business formulas | Port models and pure functions first, then compare outputs with known web values. |
| Feature calls APIs | Reuse the same endpoints with Dart `http`, `Uri.https()`, timeouts, and error states. |
| Feature uses browser APIs | Map them deliberately: localStorage to SharedPreferences, geolocation to geolocator, charts to fl_chart. |

## Execution Steps

1. Inventory all user-facing features and classify them as migrable, web-only, or hybrid.
2. Build a dependency order from least risky to most complex: static components, forms, calculators, API features, then complex state.
3. Create or update a Flutter project in `flutter/` at the repo root.
4. Add only required Flutter dependencies and document why each is needed.
5. For each feature, port models, domain logic, service/API code, state, UI, WebView hiding logic, and verification in that order.
6. Run `flutter analyze`, relevant tests, and a debug build before marking a feature migrated.
7. Remove WebView dependencies and bridge files only after every migrable feature has a native Flutter replacement.

## Output Contract

Return:
- Feature inventory and migration order.
- Files created or changed for the current feature.
- WebView/feature-flag changes, if any.
- Verification commands run and results.
- Remaining unmigrated, hybrid, or web-only features.

## References

- `references/migration-guide.md` — detailed mapping rules, examples, architecture, checklists, and common Flutter fixes.

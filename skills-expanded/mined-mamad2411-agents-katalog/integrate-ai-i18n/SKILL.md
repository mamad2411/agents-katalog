---
name: integrate-ai-i18n
description: Integrate ai-i18n into Vite browser projects that use Vue 3, React 18+, or vanilla JavaScript and TypeScript. Use when installing or configuring @ai-i18n/vite, adding translation calls or virtual:ai-i18n imports, selecting framework mode, enabling auto imports or ESLint, configuring optional locale loading, LLM audit logs, or Dev timing diagnostics, reviewing Provider logs, or diagnosing an incomplete integration.
---

# Integrate ai-i18n

Preserve the project's package manager, Vite plugins, framework conventions, and configuration style.

## Read product documentation

Read `https://bosens-china.github.io/ai-i18n/llms.txt`, select the pages that match the current
framework and requested capability, and read only those pages. Use `llms-full.txt` only when the
index or targeted pages are unavailable; do not load the full corpus by default.

User-facing installation steps, configuration fields, Runtime APIs, framework examples, generated
files, and troubleshooting live in that documentation. Do not reproduce or infer those details from
this Skill. If deployed documentation conflicts with the target project's installed types, source,
or executable behavior, follow the target project and report the discrepancy.

## Inspect the target build

Read the target app's `package.json`, `vite.config.*`, TypeScript config, entry files, and framework
plugin setup. Confirm that the app matches the current public support requirements before editing it.

In a monorepo, identify one target Vite build. Ask the user only when more than one app is plausible,
or when a new setup has no source and target language decision that can be inferred from existing
configuration. Preserve configured values.

Use one `@ai-i18n/vite` registration, one framework mode, and one i18n directory per Vite build.
Treat reachable local workspace source as part of the consuming build. Do not create a separate
integration for a source-only package or rewrite CommonJS as an incidental migration.
If existing `overrides/` shards contain file- or occurrence-scoped rules, preserve their exact
normalized POSIX paths and occurrence line/column values relative to this Vite root; never rewrite
them to machine-specific absolute paths or guess moved locations during integration.

Do not enable optional behavior by default. Keep explicit imports and omit automatic translation,
automatic imports, language persistence, locale loading, cache cleanup, HTML extraction, Dev timing
diagnostics, ESLint, and test integration unless the user requests them. Do not remove an optional feature that is already
configured. When an optional feature is requested, read [Agent defaults for optional features](references/optional-features.md)
and the matching public documentation page.

The Vite Dev review console is an optional, separately registered plugin. Do not add it unless the user
requests interactive review or the target already registers it. When requested, import `aiI18nReview`
from `@ai-i18n/vite/review` and add one `aiI18nReview()` beside the single core `aiI18n()` instance;
never restore the removed `review` core option. Do not add tokens, authentication, or production routes.
Its UI assets and internal Vue implementation are bundled with `@ai-i18n/vite`; do not install Vue or a
UI library into the target solely for Review. The host is a Web Component with Shadow DOM, and its
UnoCSS must stay inside that root rather than being added to the application's global CSS pipeline.
In Dev, verify the bottom launcher on a real business page, the workbench flush with the viewport
bottom, the default current-page scope, switching to all extracted copy, and the absence of the
launcher when the Review plugin is removed. The height preference is browser-local UI state and must
not enter Vite config. Review settings also keep theme and interface-language preferences browser-local:
verify switching between browser default, Chinese, and English updates the workbench and outer shell
without changing the application's Runtime language. For multiple target locales, verify the locale rail precedes search and status
controls in the all-page filters, and stays beside the message list in current-page view. Verify the
file-type filter lists only suffixes present in extracted source files and composes with the other
filters. Source locations and editor links belong to message rows rather than the editor detail. When
element picking returns multiple messages or occurrences, preserve every candidate in the locate
hierarchy and let the user select the exact file, line, and column; never choose the first candidate.
Verify that pointer movement shows a visible DOM locator before selection.
Click a current-page message in either main scope and verify the business page scrolls the first visible
match above the fixed panel. An all-page message absent from the current DOM must only update selection.
Registration also keeps `/__ai-i18n/` available and prints its full URL once by default. The standalone
workbench must start in all-page scope and omit current-page, picker, and business-page scrolling behavior.
Verify its page-specific structure separately: a task/progress header, horizontal locale and filter toolbar,
then a review-queue/editor split. Do not expect or restore the embedded workbench's narrow locale rail and
three-column all-page layout on the standalone page. At 1280×720, 1440×900, and an approximately
1900 px-wide desktop viewport, verify the toolbar, queue, and editor share one centered content boundary;
the queue and editor must remain adjacent and vertically aligned, with no standalone editor centering gap.
Verify the standalone document declares the bundled same-origin Review favicon; do not reuse or replace
the business application's favicon.
Set `launcher: false` only when the user requests no in-page injection, and `printUrl: false` only when
the user requests no console hint; neither option disables the standalone page or API. Remove the Review
plugin when no Review service should exist.

The project always keeps automatic translations in committed `translations/` shards. Treat
`translationMemory.cache` as an optional personal reuse cache; never create a storage marker or make
the project depend on a local database.

This Skill owns package installation, Vite configuration, Runtime source integration, and integration
verification. Do not write translation or human review values as part of an integration-only task.
When the user also requests Agent-assisted translation or review, complete the Build first, then use
the `use-ai-i18n-mcp` Skill and its approval rules.

## Apply the smallest complete setup

1. Install the version required by the target repository; during the current prerelease, use the
   public documentation's alpha install command.
2. Register the plugin in the existing Vite config without disturbing other plugins.
3. Prefer framework detection and explicit Runtime imports. Override either only when the target
   setup or user request requires it.
4. Add the smallest representative translation call by following the selected framework page.
5. Integrate generated declarations and Git ignores exactly as described by the TypeScript and
   generated-files pages selected from `llms.txt`.
6. Preserve existing component style. Do not convert Vue Options API to Composition API solely for
   ai-i18n, and do not add React subscriptions to non-component utilities.

## Verify and report

Run the target app's lint, type check, relevant tests, and full Vite Build in proportion to the
change. Check installation, resolved framework mode, one Runtime translation call, generated
declarations, and the resolved output directory. Verify the in-page launcher, Shadow DOM workbench,
scope switch and Build exclusion only when Review was requested or already configured. Verify other
optional features only when requested or already configured.

Report the selected app, changes made, commands run, remaining unsupported scope, and any decisions
that still need user input.

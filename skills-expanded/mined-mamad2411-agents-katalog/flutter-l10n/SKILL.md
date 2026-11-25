---
name: flutter-l10n
description: Flutter localization standards — the ARB catalogue and l10n.yaml, keys named by meaning with @-metadata and typed placeholders, ICU plural and select instead of sentence concatenation, dates/numbers/currency through intl at the active locale, device locale with a persisted in-app override, RTL goldens and a CI pseudo-locale, and locale-tagged server text. Load when working with .arb files, l10n.yaml, or anything under an l10n/ directory.
user-invocable: false
stack: i18n/flutter-l10n
paths:
  - "**/l10n/**"
  - "**/*.arb"
  - "**/l10n.yaml"
---

Full standards in [flutter-l10n.md](flutter-l10n.md). Always-on summary:

**Scope:** the string catalogue, the active locale, and locale-dependent formatting. Widget structure and the shared localized `Validators` class are `frontend/flutter-ui`; theme and typography are `mobile/flutter`.

**Catalogue:** `flutter_localizations` + `gen-l10n`, driven by `l10n.yaml`: `arb-dir`, `template-arb-file`, `output-class`, `output-dir`, `nullable-getter: false`, and — non-negotiably — `required-resource-attributes: true` plus `untranslated-messages-file`, so a key with no metadata and a locale with a gap each fail CI rather than shipping.

**No user-facing literal reaches a widget constructor, and the build enforces it.** Add a hardcoded-string rule via `custom_lint` in `analysis_options.yaml` and run `dart run custom_lint` as its own CI step — custom_lint diagnostics never surface in `flutter analyze`. Without the check you accumulate hundreds of keys beside hundreds of literals with no way to tell which screens are done; a half-migrated app pays the whole infrastructure cost for none of the benefit.

**Keys:** named by meaning (`programEnrollButton`, never `label12`). Every key — plain ones included — carries an `@key` block with a `description`. That block is the entire brief the translator sees. Placeholders are named and typed (`"type": "num"` / `"String"` / `"DateTime"`) with an `example`.

**Messages:** one key is one whole sentence. Counts use ICU `plural` (`=0` / `=1` / `other`), variants use ICU `select`. Never assemble a sentence from two keys, or from a key and a value — word order, agreement and pluralisation rules differ by language, so the fragments cannot be translated.

**Formatting:** a date or number placeholder carries `format:` (`yMMMd`, `compactCurrency`, `decimalPattern`, `percentPattern`) so `intl` renders it in the active locale. No pattern strings in Dart, no hand-written currency symbols, no `toStringAsFixed` on money.

**Locale:** the device locale is the default. The in-app override is a persisted `Locale?` where `null` means follow the device. Wire `localizationsDelegates: AppLocalizations.localizationsDelegates` and `supportedLocales: AppLocalizations.supportedLocales`; direction and Material/Cupertino strings then follow the locale on their own — never set direction by hand. The active locale also assigns `Intl.defaultLocale` for formatting outside the widget tree, and rides on every API request as an `Accept-Language` header.

**Direction:** an RTL locale is a layout change, not a string change. Geometry is directional from the first screen — `EdgeInsetsDirectional`, `AlignmentDirectional`, `TextAlign.start`; the full substitution table is `frontend/flutter-ui` §11. Custom directional glyphs flip on `Directionality.of(context)`; Material's own back and chevron icons already mirror.

**Proof:** a golden pumped under `Locale('ar')` with the real delegates before that locale ships, and a generated pseudo-locale ARB (`app_en_XA.arb`, values padded ~40%) run in CI so overflow from longer translations fails a build instead of a review.

**Server text:** whatever the API returns is either translated server-side against the `Accept-Language` you sent, or carries its own locale tag so the UI can label it. Never translate it on the device. A localized shell around untranslated content is not a localized app.

**Related:** `frontend/flutter-ui`, `mobile/flutter`, `api-style/dio`, `storage/flutter-local`, `testing/flutter-test`.

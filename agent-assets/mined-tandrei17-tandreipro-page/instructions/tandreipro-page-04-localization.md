---
name: Localization
description: 'Use when adding or changing user-facing text, translation keys, or supported languages.'
applyTo: "src/localization/**, src/**/*.tsx"
---

# Localization

- Store user-facing text in the existing i18next resources under `src/localization`; use `useTranslation()` and nearby namespace/key-prefix conventions instead of hardcoding UI strings in JSX.
- Keep the `en`, `es`, and `ru` resource structures aligned when adding or changing keys.
- Register new language resources through the existing setup in `src/localization/resources.ts` and follow `src/localization/index.ts` for supported-language behavior.
- Do not create a parallel localization directory or change the localization architecture as part of a content update.

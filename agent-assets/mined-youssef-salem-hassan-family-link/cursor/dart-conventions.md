---
description: "Dart / Flutter conventions for Family-Link"
globs: lib/**/*.dart
alwaysApply: false
---

# Dart & Flutter conventions (Family-Link)

## Design — avoid hardcoded look

- **Colors:** **`AppColors`** + theme / **`ColorUtils`** (`context.primaryColor`, `context.surfaceColor`, …) — avoid raw **`Color(0xFF…)`** except tiny one-offs with a comment if justified.
- **Typography:** Prefer **`context.bodyMedium`**, **`context.head3`**, **`context.buttonText`**, … from **`lib/core/utils/app_fonts.dart`** extensions — not a separate `AppTextStyles.*` facade.
- **Spacing / radius:** Prefer named constants (`EdgeInsets`, `BorderRadius.circular(12)`, shared widget defaults); align with **`AppTheme`** and existing widgets.
- **Assets:** Prefer declared assets in **`pubspec.yaml`** and **`Image.asset`** / theme — avoid magic path strings duplicated everywhere.

## Primary UI components

Prefer shared widgets (**`AppFilledPrimaryButton`**, **`AppOutlinedPrimaryButton`**, **`AppTextLink`**, **`CustomAppBar`**) instead of scattering raw **`TextButton`**, **`ElevatedButton`**, **`FilledButton`**, **`OutlinedButton`** in feature screens.

## Localization

- All user-visible strings **`context.l10n.*`** (**`Localization` getters** ARB **`lib/l10n/arb/app_en.arb`** / **`app_ar.arb`**).
- After ARB edits: **`flutter gen-l10n`**.

## Imports

1. `dart:`
2. `package:flutter/`
3. Other `package:`
4. `package:family_link/...`
5. Relative within feature

Many files consolidate via **`package:family_link/core/utils/app_imports/app_imports.dart`** — follow surrounding file imports when touching a file.

## Naming

snake_case files, PascalCase classes, `_private` fields, **`Equatable`** for Bloc states/events where used.

---
name: scaffold-feature
description: Scaffold a new Flutter feature using LeanCode architecture standards for project structure and routing to related plugins. Use when adding a new feature and deciding its directory layout.
argument-hint: "<feature-name> [--multi-page]"
---
# Scaffold Feature

Create a new feature structure following LeanCode architecture standards.

## Inputs to confirm

1. Confirm the feature name in `snake_case` (e.g. `user_profile`, `booking_details`)
2. Determine whether the feature is single-page or multi-page.
3. If multi-page, confirm the page names before creating directories.

## Structure rules

- Create a dedicated directory for each feature.
- Follow pattern: `features/<feature_name>`.
- Try not to cross-reference features.
- Put each feature part in the same folder. If a feature consists of multiple pages, put each page in a separate subfolder.

## Single-page feature

Keep the feature flat:

```
lib/features/<feature_name>/
  <feature_name>_page.dart
```

## Multi-page feature

Keep one shared feature root plus one directory per page:

```
lib/features/<feature_name>/
  <feature_name>_<page1>/
    <feature_name>_<page1>_page.dart
  <feature_name>_<page2>/
    <feature_name>_<page2>_page.dart
```

## Related architecture steps

- For dependency injection, use `flutter-di`.
- For navigation, use `flutter-navigation`.
- For analytics IDs, use `flutter-analytics`.
- For localization, use `flutter-localization`.
- For state management, use `flutter-bloc`.

## Key Reminders

- Keep the feature structure aligned with `../flutter-leancode-architecture-usage/references/project-structure.md`.
- Reach for dedicated plugins for DI, navigation, analytics, localization, and bloc conventions instead of duplicating that guidance here.

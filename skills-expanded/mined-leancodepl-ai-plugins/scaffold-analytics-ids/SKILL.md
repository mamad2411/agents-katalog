---
name: scaffold-analytics-ids
description: Creates or extends a Flutter feature-level `*_ids.dart` file with LeanCode analytics IDs for pages and clickable elements. Use when adding a new feature, page, or tracked action.
argument-hint: "<feature-name> [--page <page-name>] [--action <action-name>]"
---

# Scaffold Analytics IDs

Create or extend a feature-level `<feature_name>_ids.dart` file.

## Inputs to confirm

1. Feature name in `snake_case`.
2. Single-page or multi-page feature.
3. Page names that need IDs.
4. Clickable actions that need `AnalyticsId` entries.

## Workflow

1. Locate or create `lib/features/<feature_name>/<feature_name>_ids.dart`.
2. Name the class `<FeatureName>AnalyticsId`.
3. Add page IDs as `static const String` fields first.
4. Add clickable IDs below them as `AnalyticsId` fields or factory methods.
5. If one action exists on multiple pages, use a factory method that accepts the page ID.

## Templates

Single-page feature:

```dart
class BookingAnalyticsId {
  static const page = 'BookingPage';

  static final confirmButton = AnalyticsId('ConfirmButton', page);
}
```

Multi-page feature:

```dart
class BookingAnalyticsId {
  static const listPage = 'BookingListPage';
  static const detailsPage = 'BookingDetailsPage';

  static AnalyticsId submitButton(String page) =>
      AnalyticsId('SubmitButton', page);
}
```

## Guardrails

- Keep analytics strings only in the IDs file.
- If the project has no `AnalyticsId` class yet, set it up first as described in `../flutter-analytics-usage/references/analytics-wiring.md`.
- Do not duplicate the same action as separate string literals across pages.
- Prefer stable action names like `ConfirmButton`, `AddButton`, `RetryButton`.

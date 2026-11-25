---
name: review-analytics-coverage
description: Reviews a Flutter feature or page for missing LeanCode analytics IDs and inconsistent tracking conventions. Use when auditing analytics coverage or fixing missing page/button IDs.
argument-hint: "<feature-directory-or-file-path>"
---

# Review Analytics Coverage

Review the specified feature or file for analytics coverage gaps.

Before reviewing, find how this project wires analytics: its `AnalyticsId` class, the tappable widgets that accept an `analyticsId`, and the route that reports page IDs. `../flutter-analytics-usage/references/analytics-wiring.md` describes the expected setup.

## Checklist

- [ ] Feature has a `<feature_name>_ids.dart` file in the feature root.
- [ ] The class is named `<FeatureName>AnalyticsId`.
- [ ] Every page has a page ID, and its route reports it.
- [ ] Every button and clickable element has an `AnalyticsId`, passed to a widget that registers the tap.
- [ ] Shared actions across multiple pages use a factory method when page context differs.
- [ ] No raw analytics strings are inlined in widget files.

## Output Format

For each finding, report:

```text
[ANA] Short title
Location: lib/features/booking/booking_page.dart:42
Violation: <what is missing or inconsistent>
Fix: <concrete change to make>
```

## Guardrails

- Focus on missing or inconsistent analytics coverage, not unrelated architecture issues.
- Treat buttons, cards, rows, icon taps, and similar user-triggered actions as clickable elements.
- Base every fix on the project's own analytics widgets and route. Do not invent parameters or widgets: Flutter's `ElevatedButton`, `InkWell` and `ListTile` have no `analyticsId` parameter. If the project has no wiring yet, report that as the first finding and point to `analytics-wiring.md`.
- If coverage already looks complete, say so explicitly.

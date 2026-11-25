---
name: flutter-analytics-usage
description: Explain what the `flutter-analytics` plugin does and how to use it. Use when the user invokes `/flutter-analytics-usage`, asks what this plugin covers, or needs help defining or reviewing analytics IDs.
---

# Analytics Usage

## How to respond

- If the user invoked this skill without a concrete task, start with a short explanation of what this plugin does and when it should be used.
- Show how to use it by giving concrete analytics tasks this plugin can handle.
- Point to the most relevant rule or specialized skill for the user's goal.
- If the user already gave a concrete analytics task, briefly frame why this plugin fits and then do the work.
- Do not reply with filler like "skill loaded", "ready for the task", or "what would you like to do?" before explaining the plugin.

## What this plugin does

- Keeps feature-level analytics IDs consistent through one `<feature_name>_ids.dart` file per feature.
- Defines page IDs as `static const` values and clickable-element IDs as `AnalyticsId`.
- Helps keep action naming consistent across single-page and multi-page features.

## How to use it

- Ask for a new `*_ids.dart` file for a feature.
- Ask to add or rename page IDs or action IDs.
- Ask for a review of analytics coverage in a page or whole feature.
- Ask whether a change belongs in the IDs file or in widget/page usage code.

## Example requests

- "Create analytics IDs for the booking feature."
- "Add page and button IDs for booking details."
- "Review `lib/features/booking/` for missing analytics coverage."

## Reach for these assets

- `references/analytics.md` - source-of-truth conventions for `*_ids.dart`.
- `references/analytics-usage.md` - usage conventions in pages and widgets.
- `references/analytics-wiring.md` - where `AnalyticsId` comes from, how tappable widgets register taps through `leancode_analytics_base`, and how page views are tracked through routes. Read it before writing or reviewing code that consumes IDs, or when the project has no `AnalyticsId` class yet.
- `skills/scaffold-analytics-ids/SKILL.md` - scaffold or extend a feature IDs file.
- `skills/review-analytics-coverage/SKILL.md` - audit analytics coverage in a file or feature.

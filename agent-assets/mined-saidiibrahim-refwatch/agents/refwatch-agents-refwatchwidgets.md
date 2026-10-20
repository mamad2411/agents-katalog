# AGENTS.md

## Scope
WidgetKit extension code. Applies to `RefZoneWidgets/`.

## Build & Run
- Widgets build as part of the iOS app. Use the `RefWatchiOS` scheme in Xcode; select a target that includes the widget to preview.
- For previews, use `#Preview` providers with lightweight sample data.

## Conventions
- Keep providers/timelines fast and deterministic. Avoid heavy work on the main thread.
- Reuse shared domain models from `RefWatchCore` when possible. No direct network calls; rely on shared stores/services.
- Provide placeholders and snapshots for all widget families you support (rectangular, circular, etc.).


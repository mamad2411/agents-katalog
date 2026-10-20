# AGENTS.md

## Scope
Feature‑first MVVM code for the watch app. Applies to `RefWatchWatchOS/Features/`.

## Structure
- Each feature folder contains `{Views, Models, ViewModels}`.
- Views are SwiftUI only; business logic lives in ViewModels and services (from `Core/`).
- Use dependency injection for platform adapters and services.

## Navigation & Timer Host
- `TimerView` is the host for match timer; it renders the selected timer face and owns lifecycle routing (period label, score, action sheet).
- Keep feature views thin; delegate actions to the view model.

## Conventions
- 2‑space indent, one primary type per file. Suffixes: `View`, `ViewModel`, `Service`.
- Keep shared domain models in `Models/` so they can be target‑shared.

## Testing
- Prefer ViewModel tests over view tests. UI tests should cover critical flows only.


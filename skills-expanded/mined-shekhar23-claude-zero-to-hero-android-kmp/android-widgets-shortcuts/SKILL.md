---
name: android-widgets-shortcuts
description: |
  Android widgets and shortcuts patterns - app widgets, pinned shortcuts, quick actions, update flows, and external app entry points. Use this skill whenever exposing app functionality outside the main app UI through widgets, launcher shortcuts, or other shortcut-style surfaces. Trigger on phrases like "widget", "AppWidget", "shortcut", "pinned shortcut", "quick action", or "launcher entry point".
---

# Android Widgets and Shortcuts

## Core Principles

- External entry points should open focused, useful flows.
- Widgets and shortcuts should reflect stable app capabilities, not temporary experiments.
- Keep business logic in repositories/use cases, not in widget or shortcut handlers.
- Treat every external entry point as an app navigation boundary.
- Updates should be intentional and battery-aware.

---

## When to Use Widgets

Good widget use cases:
- glanceable status
- quick capture actions
- simple list snapshots
- media or task controls
- user-personalized summary surfaces

Bad widget use cases:
- trying to replicate the full app UI
- overly interactive complex forms
- constantly refreshing high-cost data without strong user value

Widgets should be lightweight and high-signal.

---

## Shortcut Types

Common shortcut categories:
- static shortcuts for core destinations
- dynamic shortcuts based on recent/frequent user actions
- pinned shortcuts created explicitly by the user

Use shortcuts for actions that are:
- frequently repeated
- clear out of context
- safe to open from outside the app's current state

---

## Navigation Mapping

Widgets and shortcuts should map into the same internal destination model as deep links and notifications when possible.

```text
widget/shortcut tap -> internal destination -> app navigation
```

This keeps routing consistent. See the **android-deep-links** and **android-navigation** skills.

---

## Data Loading Strategy

Widget data often needs a different loading strategy than in-app UI:
- precomputed snapshot data is often better than live heavy fetches
- background refresh should be constrained and purposeful
- avoid expensive per-update work

If widget content depends on synced or cached data, prefer reading from local persistence instead of making ad-hoc network calls from every update path.

---

## Update Triggers

Update widgets intentionally on:
- relevant data change
- periodic refresh when the value justifies it
- explicit user action
- system events that matter to the widget content

Do not refresh continuously just because it is possible.

---

## User State and Auth

If a widget or shortcut requires a logged-in user:
- handle logged-out state explicitly
- avoid exposing stale private data after logout
- clear or reset user-scoped widget state on account change

External surfaces should never leak another user's data after session changes.

---

## Design Guidance

Widgets and shortcuts should be:
- understandable at a glance
- useful with minimal taps
- resilient to missing/empty data
- accessible and clearly labeled

Keep copy short. Design for variable sizes and launcher surfaces.

---

## Shortcuts and Quick Actions

Good shortcut examples:
- create note
- resume last task
- open favorites
- start scan

Bad shortcut examples:
- vague labels like "Open"
- actions that require deep multi-step setup before becoming useful

Each shortcut should communicate a single clear outcome.

---

## Testing Guidance

Test:
- destination routing from widget/shortcut taps
- behavior when user is logged out
- empty/error widget states
- updates after relevant data changes
- cleanup on logout/account switch

Keep core behavior in testable mappers/use cases rather than receiver/provider classes alone.

---

## Checklist: Adding Widgets or Shortcuts

- [ ] Confirm the feature is useful from outside the app UI
- [ ] Map taps into the same internal navigation model used elsewhere
- [ ] Prefer local cached/snapshot data for updates when possible
- [ ] Handle logged-out, empty, and error states explicitly
- [ ] Keep updates battery-aware and purpose-driven
- [ ] Clear user-scoped external surface data on logout/account change
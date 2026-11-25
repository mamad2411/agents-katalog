---
name: flutter-widget-architecture
category: architecture
description: Use when building Flutter screens - compose small stateless widgets, keep layout declarative, decide layout by available width not device/orientation, separate presentation from business logic, and use the theme not hardcoded styles
tech_stack: Flutter
source: flutter/agent-plugins (BSD-3-Clause), adapted
---
# Flutter Widget Architecture

## Overview

Flutter UI is a tree of widgets. The quality difference is in decomposition: small, focused, mostly-stateless widgets that read like the UI they render, with business logic pushed out of the widget tree.

**Core principle:** Widgets describe what the UI looks like given state. They do not fetch data, hold business rules, or talk to the network — that lives in state/services (see flutter-state-management).

## Rules

- **Prefer `StatelessWidget`.** Reach for `StatefulWidget` only for truly local, ephemeral UI state (an animation controller, a text field's focus). App/business state lives in your state management layer.
- **Small widgets over deep `build` methods.** A `build` longer than ~40 lines or nested 5+ deep is a set of extract-widget opportunities. Extract named widgets, not `Widget _buildX()` helper methods (named widgets get their own rebuild scope and are testable).
- **`const` constructors everywhere possible** — a `const` widget subtree is skipped on rebuild. This is the cheapest performance win in Flutter.
- **Theme, not hardcoded styles.** Colors, text styles, spacing come from `Theme.of(context)` / a design-token file (`context.space`, see `mobile-design-system-foundation`) — never scattered `Color(0xFF...)` and magic paddings. This is the Flutter equivalent of "no custom CSS."
- **Keys** only when you need identity across rebuilds (reorderable lists) — don't sprinkle them.
- **Decide layout by available width, not device type or orientation.** Use `LayoutBuilder` or `MediaQuery.sizeOf(context)` — never `MediaQuery.of(context).size` (that rebuilds on every metric change, not just size) and never a device-type/orientation check to pick a layout. See `adaptive-layout` and `mobile-visual-self-review` for the size matrix this must hold at.
- **`Color.withValues(alpha:)`**, not the deprecated `withOpacity` (precision loss). **`TextScaler`** (`MediaQuery.textScalerOf(context).scale(...)`), not the deprecated `textScaleFactor`.

## Worked Example

```dart
// ❌ one giant build, hardcoded style, logic in the widget
Widget build(BuildContext context) {
  return Container(padding: EdgeInsets.all(16), color: Color(0xFF2196F3),
    child: Column(children: [ Text(task.title, style: TextStyle(fontSize: 18)), /* 60 more lines */ ]));
}

// ✅ composed from small const widgets, themed, logic elsewhere
class TaskCard extends StatelessWidget {
  const TaskCard({super.key, required this.task});
  final Task task;
  @override
  Widget build(BuildContext context) => Card(
    child: Padding(
      padding: EdgeInsets.all(context.space.md),   // token, not a magic 16
      child: Column(children: [
        TaskTitle(title: task.title),        // extracted, testable atom
        TaskStatusChip(status: task.status), // extracted molecule
      ]),
    ),
  );
}
```

## Layout-error catalogue

Four errors that show up repeatedly and what they mean:

- **"Vertical viewport was given unbounded height"** — a `Column`/`ListView` inside another unbounded-height ancestor (e.g. a `Column` inside a `SingleChildScrollView` with no `Expanded`/`shrinkWrap`). Give it a bound: `Expanded`, `SizedBox`, or `shrinkWrap: true` when genuinely short.
- **"`InputDecorator` ... unbounded width"** — a `TextField`/`TextFormField` inside a `Row` with no `Expanded`/`Flexible` wrapping it.
- **"`RenderFlex` overflowed by N pixels"** — the matrix-test failure mode (see `mobile-visual-self-review`); fix by deciding layout from available width, not by shrinking content to fit.
- **"Incorrect use of `ParentData` widget"** — a widget meant for one parent (`Expanded`, `Positioned`) used under the wrong parent type (not `Flex`/`Stack`). The fix is almost always removing a stray wrapper, not adding one.
- Ignore a cascading **"RenderBox was not laid out"** once you've fixed the error above it — it's usually fallout from the first failure, not a separate bug.

## Version note (Flutter 3.47+)

`material_ui`/`cupertino_ui` are now separate packages from the bundled Material/Cupertino libraries; don't run `dart fix --apply --code=migrate_design_widgets` or otherwise migrate a repo to them unless the task explicitly asks — follow what the repo already uses.

## Common Mistakes

- `StatefulWidget` holding data that came from an API — that's app state, lift it out.
- `Widget _buildHeader()` helper methods instead of real widget classes.
- Hardcoded colors/sizes instead of the theme.
- Missing `const` on static subtrees → needless rebuilds.
- Choosing layout by `MediaQuery.of(context).size` or an orientation/device check instead of `LayoutBuilder`/`MediaQuery.sizeOf`.
- `textScaleFactor`/`withOpacity` instead of `TextScaler`/`Color.withValues`.

## Red Flags

- A `build` method you scroll to read.
- `setState` mutating something a service should own.
- `Color(0xFF...)` / magic paddings outside the theme file.
- A layout branch keyed on `Theme.of(context).platform` or `MediaQuery.orientationOf` instead of width.

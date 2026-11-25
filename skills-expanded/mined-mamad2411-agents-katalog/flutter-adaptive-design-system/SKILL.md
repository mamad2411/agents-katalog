---
name: flutter-adaptive-design-system
description: |
  Platform-adaptive Flutter design system generating native-quality UI for iOS (Cupertino) and Android (Material 3).
  Use when: (1) Creating adaptive widgets that render natively per platform, (2) Building Flutter UI that looks like a real iOS or Android app — not a generic cross-platform hybrid, (3) Generating Cupertino/Material widget pairs with consistent API, (4) Implementing adaptive navigation, dialogs, forms, inputs, or layouts, (5) Setting up a Flutter project's design system foundation with platform detection.
  Triggers: "adaptive widget", "cupertino material", "platform adaptive", "ios android widget", "design system flutter", "native look flutter", "platform widget", "cupertino", "material design", "adaptive UI"
---

# Flutter Adaptive Design System

> Brought to you by **[Appbiz Studio LLC](https://appbiz.studio)**

Generate platform-native Flutter UI. iOS renders Cupertino widgets; Android renders Material 3.
Single codebase, two native experiences.

**Package requirement**: `hugeicons` for all icons (never `CupertinoIcons` or `Icons` for app icons).

## Configuration

All widgets use the `Adaptive` prefix (`AdaptiveButton`, `AdaptiveScaffold`, `AdaptiveDialog`, etc.). This is fixed — no custom prefix. Keeps it consistent across all projects.

## Template Files — Ready to Copy

All 41 production-tested adaptive widget files are in the `templates/` directory, organized by category:

```
templates/
├── foundation/           # PlatformUtils, PlatformWidget, PlatformBuilder, AdaptiveThemeScope
└── widgets/
    ├── layout/           # Scaffold, AppBar, BottomNav, Card, Divider, ListTile, ListSection, SliverAppBar, TabScaffold
    ├── buttons/          # Button, FAB, IconButton, TextButton
    ├── inputs/           # TextField, SearchBar, Switch, Slider, Checkbox, Radio, SegmentedControl, Picker, FormField
    ├── feedback/         # Dialog, ActionSheet, SnackBar, ProgressIndicator, RefreshIndicator, Tooltip
    ├── chips/            # Chip, FilterChip
    ├── navigation/       # NavigationDrawer, PageRoute, PopupMenu, TabBar
    ├── pickers/          # DatePicker, TimePicker, Picker
    └── context_menu/     # ContextMenu
```

### How to install in a new project

**Copy the templates verbatim** into `lib/shared/`:

```
lib/shared/
├── foundation/    ← copy from templates/foundation/
└── widgets/       ← copy from templates/widgets/
```

Then create a barrel file `lib/shared/widgets.dart` exporting everything.

**Only thing to adjust**: Nothing. The templates use relative imports and only depend on `flutter` and `hugeicons`. No package-specific imports to replace.

## Foundation

Three files power the system. See [foundation.md](references/foundation.md) for full code.

### PlatformUtils — Detection engine

```dart
abstract final class PlatformUtils {
  static bool get isCupertino => Platform.isIOS || Platform.isMacOS;
  static bool get isMaterial => !isCupertino;
}
```

### Three Implementation Patterns

**Pattern A — `PlatformWidget<M, C>` base class**
Best when both platforms return a Widget with similar constructor shape.

```dart
class AdaptiveSwitch extends PlatformWidget<Switch, CupertinoSwitch> {
  final bool value;
  final ValueChanged<bool>? onChanged;
  const AdaptiveSwitch({super.key, required this.value, this.onChanged});

  @override
  Switch buildMaterialWidget(BuildContext context) =>
      Switch(value: value, onChanged: onChanged);

  @override
  CupertinoSwitch buildCupertinoWidget(BuildContext context) =>
      CupertinoSwitch(value: value, onChanged: onChanged);
}
```

**Pattern B — StatelessWidget with direct dispatch**
Best when platform widgets have very different APIs or need custom wrapping.

```dart
class AdaptiveButton extends StatelessWidget {
  final VoidCallback? onPressed;
  final Widget child;
  const AdaptiveButton({super.key, this.onPressed, required this.child});

  @override
  Widget build(BuildContext context) {
    if (PlatformUtils.isCupertino) {
      return CupertinoButton.filled(onPressed: onPressed, child: child);
    }
    return FilledButton(onPressed: onPressed, child: child);
  }
}
```

**Pattern C — Static methods for imperative APIs**
Best for dialogs, sheets, pickers that use `show*()` functions.

```dart
class AdaptiveDialog {
  const AdaptiveDialog._();
  static Future<T?> show<T>({
    required BuildContext context,
    required String title,
    String? content,
    List<AdaptiveDialogAction> actions = const [],
  }) {
    if (PlatformUtils.isCupertino) return _showCupertino<T>(...);
    return _showMaterial<T>(...);
  }
}
```

### Pattern Decision Tree

```
Need adaptive widget?
├─ Both platforms have similar Widget constructors?
│  └─ YES → Pattern A (PlatformWidget<M, C>)
├─ Platforms need very different params / wrapping?
│  └─ YES → Pattern B (StatelessWidget + if/else)
├─ Widget is shown imperatively (showDialog, showModalBottomSheet)?
│  └─ YES → Pattern C (static methods)
└─ Need function-level platform split (one-off)?
   └─ Use PlatformBuilder(materialBuilder:, cupertinoBuilder:)
```

### Supporting Utilities

```dart
// Function-based one-off platform split
class PlatformBuilder extends StatelessWidget {
  final WidgetBuilder materialBuilder;
  final WidgetBuilder cupertinoBuilder;
  Widget build(context) => PlatformUtils.isCupertino
      ? cupertinoBuilder(context) : materialBuilder(context);
}

// Theme scope wrapper
class AdaptiveThemeScope extends StatelessWidget {
  final ThemeData materialTheme;
  final CupertinoThemeData cupertinoTheme;
  final Widget child;
  Widget build(context) => PlatformUtils.isCupertino
      ? CupertinoTheme(data: cupertinoTheme, child: child)
      : Theme(data: materialTheme, child: child);
}
```

## Widget Catalog (37 widgets)

See [widgets.md](references/widgets.md) for implementation code of each widget.

### Navigation & Structure

| Widget | Material 3 | Cupertino | Pattern |
|--------|-----------|-----------|---------|
| `AdaptiveScaffold` | `Scaffold` | `CupertinoPageScaffold` | A |
| `AdaptiveAppBar` | `AppBar` | `CupertinoNavigationBar` | B |
| `AdaptiveBottomNav` | `NavigationBar` | `CupertinoTabBar` | B |
| `AdaptiveTabScaffold` | `Scaffold+NavigationBar` | `CupertinoTabScaffold` | B |
| `AdaptiveSliverAppBar` | `SliverAppBar` | `CupertinoSliverNavigationBar` | B |
| `AdaptivePageRoute` | `MaterialPageRoute` | `CupertinoPageRoute` | C |
| `AdaptiveTabBar` | `TabBar+TabBarView` | `SegmentedControl+IndexedStack` | B |
| `AdaptiveNavigationDrawer` | `NavigationDrawer` | Custom drawer | B |

### Content & Lists

| Widget | Material 3 | Cupertino | Pattern |
|--------|-----------|-----------|---------|
| `AdaptiveCard` | `Card (M3)` | Styled `Container` | A |
| `AdaptiveListTile` | `ListTile` | `CupertinoListTile` | A |
| `AdaptiveListSection` | `Column+dividers` | `CupertinoListSection` | B |
| `AdaptiveDivider` | `Divider` | 0.5px `Container` | A |

### Buttons & Actions

| Widget | Material 3 | Cupertino | Pattern |
|--------|-----------|-----------|---------|
| `AdaptiveButton` | `FilledButton` | `CupertinoButton.filled` | B |
| `AdaptiveTextButton` | `TextButton` | `CupertinoButton` | B |
| `AdaptiveIconButton` | `IconButton` | `CupertinoButton(icon)` | B |
| `AdaptiveFAB` | `FloatingActionButton` | Hidden / nav bar button | B |
| `AdaptivePopupMenu` | `PopupMenuButton` | `CupertinoContextMenu` | B |
| `AdaptiveContextMenu` | `ContextMenuController` | `CupertinoContextMenu` | B |

### Forms & Inputs

| Widget | Material 3 | Cupertino | Pattern |
|--------|-----------|-----------|---------|
| `AdaptiveTextField` | `TextField (outlined)` | `CupertinoTextField` | B |
| `AdaptiveSearchBar` | `SearchBar` | `CupertinoSearchTextField` | B |
| `AdaptiveSwitch` | `Switch` | `CupertinoSwitch` | A |
| `AdaptiveSlider` | `Slider` | `CupertinoSlider` | A |
| `AdaptiveCheckbox` | `Checkbox` | `CupertinoCheckbox` | A |
| `AdaptiveRadio` | `Radio` | Custom Cupertino radio | B |
| `AdaptiveSegmentedControl` | `SegmentedButton` | `CupertinoSlidingSegmentedControl` | B |
| `AdaptivePicker` | `ListWheelScrollView` | `CupertinoPicker` | C |
| `AdaptiveFormField` | `TextFormField` | `CupertinoTextField+validator` | B |

### Chips & Tags

| Widget | Material 3 | Cupertino | Pattern |
|--------|-----------|-----------|---------|
| `AdaptiveChip` | `Chip` | Styled `Container` | B |
| `AdaptiveFilterChip` | `FilterChip` | Styled toggle `Container` | B |

### Feedback & Overlays

| Widget | Material 3 | Cupertino | Pattern |
|--------|-----------|-----------|---------|
| `AdaptiveDialog` | `AlertDialog` | `CupertinoAlertDialog` | C |
| `AdaptiveActionSheet` | `BottomSheet` | `CupertinoActionSheet` | C |
| `AdaptiveSnackBar` | `SnackBar` | Custom toast overlay | C |
| `AdaptiveProgressIndicator` | `CircularProgressIndicator` | `CupertinoActivityIndicator` | A |
| `AdaptiveTooltip` | `Tooltip` | Custom overlay | B |

### Scroll & Refresh

| Widget | Material 3 | Cupertino | Pattern |
|--------|-----------|-----------|---------|
| `AdaptiveRefreshIndicator` | `RefreshIndicator` | `CupertinoSliverRefreshControl` | B |

### Pickers & Dates

| Widget | Material 3 | Cupertino | Pattern |
|--------|-----------|-----------|---------|
| `AdaptiveDatePicker` | `showDatePicker()` | `CupertinoDatePicker` modal | C |
| `AdaptiveTimePicker` | `showTimePicker()` | `CupertinoDatePicker(time)` | C |

## Iconography — HugeIcons

```dart
import 'package:hugeicons/hugeicons.dart';

HugeIcon(
  icon: HugeIcons.strokeRoundedHome01,
  color: CupertinoColors.label,
  size: 24.0,
)
```

| Platform | Preferred style | Reason |
|----------|----------------|--------|
| Android | `strokeRounded*` | Matches Material outlined icons |
| iOS | `solid*` | Matches SF Symbols filled style |

Adaptive helper:

```dart
Widget adaptiveIcon(IconData stroke, IconData solid, {double size = 24, Color? color}) {
  return HugeIcon(
    icon: PlatformUtils.isCupertino ? solid : stroke,
    size: size,
    color: color,
  );
}
```

Common mappings: Home01, Settings01, Search01, Notification01, User, Lock, Book01, Wallet01, ArrowLeft01, Add01, Cancel01, CheckmarkCircle01, Share01, Filter, Analytics01.

## Typography

```
M3 DisplayLarge    ↔  iOS largeTitle    — 34px bold
M3 HeadlineMedium  ↔  iOS title1        — 28px bold
M3 TitleLarge      ↔  iOS title2        — 22px bold
M3 TitleMedium     ↔  iOS headline      — 17px semibold
M3 BodyLarge       ↔  iOS body          — 17px regular
M3 BodyMedium      ↔  iOS callout       — 16px regular
M3 LabelLarge      ↔  iOS subheadline   — 15px regular
M3 LabelSmall      ↔  iOS caption1      — 12px regular
```

## Colors

| Role | iOS System | M3 Equivalent |
|------|-----------|---------------|
| Primary | `systemBlue` #007AFF | `primary` |
| Destructive | `systemRed` #FF3B30 | `error` |
| Success | `systemGreen` #34C759 | custom |
| Warning | `systemOrange` #FF9500 | custom |
| Background | `systemGroupedBackground` | `surface` |
| Secondary BG | `secondarySystemGroupedBackground` | `surfaceVariant` |
| Label | `label` | `onSurface` |
| Secondary label | `secondaryLabel` | `onSurfaceVariant` |

## Spacing & Border Radius

```dart
const double kPagePadding = 16.0;
const double kItemSpacing = 8.0;
const double kSectionSpacing = 24.0;
```

| Element | Android (M3) | iOS |
|---------|-------------|-----|
| Card | 12px | 10px |
| Button | 20px (pill) | 10px |
| Dialog | 28px | 14px |
| TextField | 4px | 8px |
| Chip | 8px | 6px |

## Scroll, Gestures, Haptics

```dart
ScrollPhysics adaptiveScrollPhysics() => PlatformUtils.isCupertino
    ? const BouncingScrollPhysics()
    : const ClampingScrollPhysics();
```

| Interaction | Android | iOS |
|-------------|---------|-----|
| Back | System back + edge swipe | Swipe from left edge |
| Long-press | Text selection | CupertinoContextMenu with preview |
| Overscroll | Blue glow | Bounce |
| Pull-to-refresh | Colored circle | Spinner |

Haptics: `HapticFeedback.lightImpact()` (tap), `.mediumImpact()` (action), `.heavyImpact()` (confirm), `.selectionClick()` (picker).

## Animations

| Action | Duration |
|--------|----------|
| Micro (tap, toggle) | 100-150ms |
| UI transition (dialog) | 250-300ms |
| Page transition | 350-400ms |

| Usage | Android M3 | iOS |
|-------|-----------|-----|
| Page transition | `easeInOutCubicEmphasized` | `easeInOut` |
| Dialog appear | `easeOutBack` | `easeOut` |
| Element enter | `fastOutSlowIn` | `easeOut` |

## Keyboard & Status Bar

```dart
// Dismiss keyboard on tap outside
GestureDetector(onTap: () => FocusScope.of(context).unfocus(), child: ...)

// Adaptive status bar
SystemChrome.setSystemUIOverlayStyle(
  PlatformUtils.isCupertino ? SystemUiOverlayStyle.dark
    : SystemUiOverlayStyle(statusBarColor: Colors.transparent, ...),
);
```

## Performance Rules

Adaptive widgets dispatch hundreds of widgets per screen. See [performance.md](references/performance.md) for full guide.

**Critical rules:**

1. **const constructors** — Every adaptive widget MUST have `const` constructor. Use `const` in widget trees.
2. **Platform check is free** — `PlatformUtils.isCupertino` is a static bool read. Zero cost. No caching needed.
3. **Only active branch runs** — `PlatformWidget.build` calls only one branch. Dead code is never executed.
4. **ListView.builder always** — Never `ListView(children: [...])` for dynamic lists. Use `.builder`.
5. **RepaintBoundary** — Wrap interactive cards to prevent ripple/animation leaks.
6. **Extract const subtrees** — Break large builds into small const-eligible widgets.
7. **Method refs over closures** — `onPressed: _submit` not `onPressed: () => _submit()`.
8. **Image decode at display size** — Set `cacheWidth`/`cacheHeight` on images.
9. **FadeTransition over AnimatedOpacity** — Avoids expensive `saveLayer`.

**Performance budgets**: First frame < 2s, frame render < 16ms (60fps), list scroll 0 jank frames, memory < 100MB.

## Extended References

For detailed implementation code and advanced patterns:

- **[foundation.md](references/foundation.md)** — PlatformWidget, PlatformUtils, PlatformBuilder, AdaptiveThemeScope, barrel file, app entry point
- **[widgets.md](references/widgets.md)** — Full implementation code for all 37 widgets
- **[accessibility.md](references/accessibility.md)** — Semantics, Dynamic Type, VoiceOver/TalkBack, WCAG AA
- **[responsive.md](references/responsive.md)** — Breakpoints, LayoutBuilder, iPad/tablet, landscape
- **[states.md](references/states.md)** — Loading/shimmer, empty, error, disabled state patterns
- **[performance.md](references/performance.md)** — const optimization, rebuild prevention, list performance, animation, profiling

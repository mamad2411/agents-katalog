---
name: responsive-layout
description: Mobile-first layout, M3 window-size classes, gutter rules, bottom nav vs drawer vs FAB, bottom sheets vs dialogs, safe areas, keyboard avoidance, edge-to-edge, haptics. MANDATORY TRIGGERS - "responsive", "mobile-first", "bottom nav", "bottom sheet", "safe area", "keyboard avoidance", "breakpoint", "window size", "gutter", "tablet", "foldable", "haptics", "edge-to-edge", "system inset", "SafeAreaScaffold", "NavigationBar", "drawer", "FAB".
allowed-tools: Read, Glob, Grep, Edit, Write
---

# Responsive Layout (mobile-first)

> Mobile-first: Compact (<600 dp) is the default MVP target for a phone-first Flutter app.
> Everything else is documented for Phase 2.

Read `docs/design-system/mobile-first.md` before designing or refactoring
any screen. This skill is the operational shortcut for day-to-day
decisions.

## When to use

Invoke this skill whenever a task involves:

- Adding or refactoring a screen, dialog, or bottom sheet.
- Translating a desktop / web sketch (e.g. from the Figma design system) to mobile.
- Deciding between bottom nav, drawer, FAB, or in-page navigation.
- Wiring safe-area, keyboard avoidance, or edge-to-edge.
- Adding haptic feedback to a new interaction.
- Choosing breakpoints for responsive code.

## Inputs

1. The feature spec (`docs/specs/<feature>/spec.md`).
2. The screen's information density (form / list / detail / modal).
3. Any desktop/web reference the product team provided.
4. Existing siblings under `lib/features/<feature>/presentation/`.

## Steps

1. **Pick the window-size baseline.** Compact = MVP. Confirm by reading
   `context.windowSize` (from `WindowSizeX`). If the design only specifies
   desktop, derive Compact equivalents using
   `mobile-first.md` "Desktop -> mobile mapping table".
2. **Pick the navigation pattern.**
   - Top-level surface (lives in bottom nav) -> use `MainShellPage` slot.
   - Detail / drill-down -> push via `go_router` inside the current branch.
   - Modal flow (composer, share, filter, picker) ->
     `showModalBottomSheet(useSafeArea: true)`.
   - Binary confirm / deny -> `showDialog`.
   - Forbidden in MVP: drawer (sidebar), FAB (use inline composer).
3. **Wrap in `SafeAreaScaffold`.** Never use raw `Scaffold`. Set:
   - `body` always required.
   - `appBar` for top-app-bar surfaces (56dp).
   - `bottomNavigationBar` only when the screen replaces the shell's nav.
   - `onRefresh` if the body is a feed / list.
   - `dismissKeyboardOnTap: true` (default) on every form surface.
4. **Apply gutters.** Use `AppGutter.gutter(context)` or `ResponsivePadding`.
   Never write `EdgeInsets.symmetric(horizontal: 16)` inline.
5. **Compose with layout primitives** from `lib/design_system/layout/layout.dart`:
   `SafeAreaScaffold`, `KeyboardDismissible`, `ResponsivePadding`, `AppGutter`,
   `AppBreakpoints`, `WindowSize`, `AppHaptics`.
6. **Touch targets.** Every tappable element >= 48dp (Material) / 44dp (HIG).
   Use `IconButton` (44dp default) or wrap with `SizedBox(height: 48, ...)`.
7. **Haptics.** Apply via `AppHaptics.voteTap()`, `tabSwitch()`,
   `longPressMenu()`, `errorShake()`. They auto-suppress when
   `MediaQuery.disableAnimations` is true.
8. **Edge-to-edge.** On Android 15+, use `SystemUiMode.edgeToEdge` (already
   set by `SafeAreaScaffold`). Never set status-bar / nav-bar colors
   directly -- they come from theme.
9. **Keyboard.** Forms use `TextInputAction.next/done`, focus-node chains,
   `KeyboardDismissible` (already inside `SafeAreaScaffold`). Long
   scrollable forms set
   `keyboardDismissBehavior: ScrollViewKeyboardDismissBehavior.onDrag`.
10. **Test the layout at min phone width (375 dp) AND `textScaler: 1.5`.**
    No overflow, no clipped text, no overlapping tap targets. This is a
    Definition-of-Done gate.

## Output template

For each new screen the agent ships, the PR description must include:

```
## Layout (mobile-first)
- Window-size targets: Compact (Medium/Expanded n/a in MVP)
- Scaffold: SafeAreaScaffold
- Gutter: AppGutter.gutter(context)
- Touch targets: all >= 48dp
- Keyboard: TextInputAction chain + KeyboardDismissible
- Haptics: <list, or "n/a">
- Pull-to-refresh: <yes/no, why>
- Verified at 375 dp + textScaler 1.5
```

## Examples

### Example 1 -- Add a new screen (e.g. "Notifications inbox")

```dart
class NotificationsPage extends StatelessWidget {
  const NotificationsPage({super.key});

  @override
  Widget build(BuildContext context) {
    final t = Translations.of(context);
    return SafeAreaScaffold(
      appBar: AppBar(title: Text(t.notifications.title)),
      onRefresh: () async =>
          context.read<NotificationBloc>().add(const RefreshRequested()),
      body: ResponsivePadding(
        child: NotificationList(),
      ),
    );
  }
}
```

### Example 2 -- Convert a desktop sketch (sidebar nav) to mobile

The Figma design has a left sidebar with 12 items. On Compact:
- 4 most-used -> bottom nav (Dong tin / Tin nhan / Trang ca nhan / Cai dat).
- The other 8 -> either deferred (Cong dong, Mang luoi, Leaderboard, Crypto ...)
  or surfaced as a "Kham pha" entry inside the home feed.
- Drawer is forbidden in MVP per `mobile-first.md`.

### Example 3 -- Bottom sheet vs dialog

| Surface | Decision |
|---|---|
| Composer (Quick Post / Thesis) | Bottom sheet (full-height, drag handle, useSafeArea) |
| Share dialog (FB / Zalo / X / ...) | Bottom sheet (<=50% height) |
| Filter chips (thesis status) | Inline filter row, NOT a sheet |
| Confirm logout | `AlertDialog` |
| Confirm close thesis | `AlertDialog` |
| Image picker | Bottom sheet (camera / library / cancel) |

## Anti-patterns to refuse

- Raw `Scaffold` (use `SafeAreaScaffold`).
- Drawer / sidebar on Compact (forbidden in MVP).
- FAB for primary actions (composer is inline; FABs reserved for v2).
- `EdgeInsets.symmetric(horizontal: 16)` inline literal -- use `AppGutter`.
- Hardcoded `Color()` for theme-aware values -- use `colorScheme` or `SemanticColors`.
- Touch targets < 48dp.
- Dialogs for rich flows; rich flows go in bottom sheets.
- Disabling `resizeToAvoidBottomInset` without a documented reason.
- Setting status-bar / nav-bar colors imperatively (rely on theme).

## References

- [Material 3 -- Adaptive design with window size classes](https://m3.material.io/foundations/layout/applying-layout/window-size-classes)
- [Flutter -- Creating responsive and adaptive apps](https://docs.flutter.dev/ui/adaptive-responsive)
- [Apple Human Interface Guidelines -- Layout](https://developer.apple.com/design/human-interface-guidelines/layout)
- [Android -- Edge-to-edge display](https://developer.android.com/develop/ui/views/layout/edge-to-edge)
- [Apple HIG -- Touch targets (44pt minimum)](https://developer.apple.com/design/human-interface-guidelines/buttons)
- [Material 3 -- Touch targets (48dp minimum)](https://m3.material.io/foundations/accessible-design/accessibility-basics)
- `docs/design-system/mobile-first.md` (full canonical contract)
- `lib/design_system/layout/` (Dart primitives)

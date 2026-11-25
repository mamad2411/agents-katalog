---
name: android-accessibility
description: Project-specific Compose accessibility conventions — the `mergeDescendants` rule for visually-grouped composables, the `fontScale = 2.0` preview mandate, the RTL preview pattern, and the live-region escalation rule. Load whenever adding or reviewing a Compose screen.
---

# Android accessibility (project delta)

For Compose accessibility fundamentals — `Modifier.semantics`, `contentDescription`, `Role`, `mergeDescendants`, `clearAndSetSemantics`, `liveRegion`, `traversalIndex`, `minimumInteractiveComponentSize()`, custom actions — read the [official Compose accessibility guide](https://developer.android.com/develop/ui/compose/accessibility) and the [accessibility for adaptive apps](https://developer.android.com/develop/ui/compose/touch-input/pointer-input/scroll/scroll-modifier) supplements. This file documents only the project's conventions on top of those.

## When this applies

Jetpack Compose accessibility. On an existing app:

- **View-based UI** → the principles transfer (tap targets ≥ 48dp, content descriptions, dynamic type) but the API surface is different (`AccessibilityDelegate`, `android:contentDescription`, `android:importantForAccessibility`). Don't push Compose APIs.
- **Mixed Compose + View** → apply this skill only to Compose surfaces.

## Baseline (project enforcement)

Every interactive element ships with:
- **Tap target ≥ 48dp × 48dp.** `Modifier.minimumInteractiveComponentSize()` on any custom clickable that isn't already a Material widget.
- **Accessible name.** `Text` content auto-announces; icons/custom controls need `contentDescription` or `Modifier.semantics`.
- **Correct `role`** so TalkBack reads "button" / "switch" / "checked" — not the visual only.

`contentDescription` is a **short action verb**, not a description of pixels ("Delete", not "A trash can icon"). Decorative icons use `contentDescription = null` explicitly — never an empty string.

## Group with `mergeDescendants` (project rule)

When a `Row` / `Column` represents one logical concept (one row, one card, one list item), **always** merge its descendants into a single accessible node:

```kotlin
Row(
    modifier = Modifier
        .clickable(onClick = onPlayClick)
        .semantics(mergeDescendants = true) {
            contentDescription = "Play episode: ${episode.title}"
            role = Role.Button
        },
) {
    AsyncImage(...)
    Column { Text(episode.title); Text(episode.duration) }
    Icon(Icons.Default.PlayArrow, contentDescription = null)  // merged above
}
```

Without `mergeDescendants = true`, TalkBack reads each child as a separate node and the list becomes a swipe slog. The reviewer flags any `Row` / `Column` with `clickable` and multiple children that doesn't merge.

`clearAndSetSemantics { ... }` replaces everything below — use **only** when the auto-generated semantics are actively wrong (e.g. a custom slider). It's a sharper tool than the project usually needs.

## `fontScale = 2.0` preview mandate

Every screen ships with a `fontScale = 2.0f` preview alongside its default one:

```kotlin
@Preview(fontScale = 2.0f, showBackground = true)
@Composable fun OrderRow_LargeFont() = AppTheme { OrderRow(previewOrder) }
```

Layouts must survive font scaling. **No fixed-height text containers** — use `wrapContentHeight()` or intrinsic sizing. Truncation with an expand affordance is fine; hiding content is not. The reviewer rejects screens that lack a large-font preview.

## RTL preview pattern

```kotlin
@Preview @Composable fun OrderRow_Rtl() =
    CompositionLocalProvider(LocalLayoutDirection provides LayoutDirection.Rtl) {
        AppTheme { OrderRow(previewOrder) }
    }
```

Use `start` / `end` in modifiers (never `left` / `right`). Compose is RTL-aware by default for `padding(start = ...)`, `PaddingValues`, `Arrangement`, `Alignment`. Custom drawing must read `LocalLayoutDirection.current` and mirror manually.

## Live regions vs `announceForAccessibility`

For non-visual feedback (error banner, validation, status change):

- **Preferred — `Modifier.semantics { liveRegion = LiveRegionMode.Polite }`** on the visible error text. The status text and the announcement stay coupled; visible UI is the source of truth.
- **Fall back to `view.announceForAccessibility(...)`** in a `LaunchedEffect` only when there's no visible element to attach a live region to (toast-like notifications). This route bypasses TalkBack's queue and can race with other announcements.

## Hard nos

- **No `contentDescription = ""`** to suppress — use `null` for decorative images. An empty string still announces "image".
- **No `Modifier.clickable` on a `Text`** without `Modifier.semantics { role = Role.Button }`. TalkBack reads it as "double-tap to activate" instead of "button," which the user can't distinguish from a switch or link.
- **No hard-coded `dp` text.** Always `sp` so font scaling respects the user's setting.
- **No `Modifier.size(32.dp)`** around a touch target — wrap in `minimumInteractiveComponentSize()` or size at 48dp minimum.
- **No testing only on the default font scale.** The 2.0 preview is non-negotiable.
- **No `mergeDescendants` omitted** on a `clickable` row with multiple visual children. TalkBack swipe order grows in proportion to how many of these slip in.

---
name: arabic-rtl-mobile
description: Use when building or fixing Arabic-first mobile interfaces in iOS native, Android native, or React Native, especially when Arabic text appears visually left-aligned, rows are composed incorrectly in RTL, directional icons point the wrong way, or controls and labels sit on the wrong sides of the screen.
---

# Arabic RTL Mobile

Use this skill for Arabic mobile screens that should feel natively RTL across iOS native, Android native, and React Native.

## Supported Stacks

- iOS native: SwiftUI, UIKit
- Android native: Jetpack Compose, Views/XML
- React Native

## Core Rule

First determine whether the app or screen is already effectively RTL at the root.

If the root is already RTL, prefer logical direction semantics that belong to the framework:

- `leading` and `trailing` on iOS native
- `start` and `end` on Android native
- `start`, `end`, `marginStart`, `paddingStart`, and `I18nManager.isRTL` patterns in React Native

Do not blindly add a second local RTL override.

Do not blindly replace logical alignment with hard-coded `right` and `left` unless the framework gives you no better option for that exact case.

Before fixing rows, icons, or controls, run a visual sentinel check with a full-width Arabic text block.

If the sentinel lands on the visual right edge, the screen is behaving as RTL.

If the sentinel lands on the visual left edge, fix the root direction first.

Do not begin row-level fixes until this passes.

## Framework Root Checks

### iOS Native

Check whether the app already enforces RTL globally.

Examples:

- SwiftUI root may already use `layoutDirection`
- UIKit may already rely on `semanticContentAttribute`
- Labels and text views often behave best with natural or logical alignment, not hard-coded right/left

If the app root already handles RTL, avoid adding a second local RTL override to a single screen unless there is a specific reason.

### Android Native

Check whether the app is already configured to support RTL at the app level.

Common signals:

- app manifest enables RTL support
- Compose or Views inherit locale-aware direction
- layouts already use `start` and `end` instead of `left` and `right`

For Android native, prefer logical direction APIs such as `start`, `end`, `gravityStart`, `gravityEnd`, `paddingStart`, `paddingEnd`, `marginStart`, and `marginEnd`.

If using Jetpack Compose, prefer direction-aware alignment and text alignment before forcing a local layout direction override.

### React Native

Check whether the app is actually running in RTL.

Key checks:

- `I18nManager.isRTL`
- app-level RTL enablement
- whether the current screen visually flips as expected

`allowRTL()` is an app-level enablement tool.

`forceRTL()` is useful for development and testing only, requires an app restart, and should not be treated as the production fix.

Prefer direction-aware style props such as `start`, `end`, `marginStart`, `marginEnd`, `paddingStart`, and `paddingEnd`. Use `I18nManager.isRTL` when a manual directional decision is truly needed.

## Visual Sentinel Check

Before fixing a full screen, place one full-width Arabic text block and inspect it visually.

### iOS Native Sentinel

```swift
Text("اختبار")
    .frame(maxWidth: .infinity, alignment: .leading)
    .multilineTextAlignment(.leading)
```

### Android Compose Sentinel

```kotlin
Text(
    text = "اختبار",
    modifier = Modifier.fillMaxWidth(),
    textAlign = TextAlign.Start
)
```

### React Native Sentinel

```tsx
<Text
  style={{
    width: '100%',
    textAlign: I18nManager.isRTL ? 'right' : 'left',
  }}
>
  اختبار
</Text>
```

Inspect the result visually:

- if it lands on the visual right, continue
- if it lands on the visual left, fix root RTL first

Do not start with row composition until this passes.

## Arabic Text Blocks

For Arabic headings, subtitles, descriptions, helper copy, and card content:

- give the text block full available width
- anchor it using the framework's logical direction tools
- keep centered text only when the design clearly intends centered text

### iOS Native

For SwiftUI text blocks, a common pattern is:

```swift
VStack(alignment: .leading, spacing: 8) {
    Text(title)
    Text(subtitle)
}
.frame(maxWidth: .infinity, alignment: .leading)
```

For UIKit, the same principle still applies:

- the text container should occupy the available width
- semantic direction should come from the view hierarchy
- avoid hard-coded left/right alignment when natural or logical alignment is available

### Android Native

For Jetpack Compose:

- use `fillMaxWidth()`
- prefer `TextAlign.Start`
- prefer start-aware arrangements and alignment

For Views/XML:

- use full-width containers where needed
- prefer `start` and `end`
- prefer `gravity` and `textAlignment` values that follow logical direction

### React Native

For React Native text blocks:

- make the text block occupy the available width
- prefer start/end-aware spacing props
- use `I18nManager.isRTL` only where manual text alignment or directional behavior is actually needed

Do not let Arabic text shrink to intrinsic width if the design expects it to visually own the row or card.

## Arabic Row Composition

Treat an Arabic row as two zones:

- main text content on the visual right
- secondary control or accessory on the visual left

Typical accessories:

- stepper or quantity control
- duration or metric
- status chip
- disclosure chevron
- number badge

The text block should own the flexible width.

There should be visible breathing room between the text block and the accessory.

### Layout Intent

Your target result is:

- text pinned to the Arabic edge
- accessory pinned to the opposite edge
- real empty space between them
- no collapsing toward the middle

### Per-Stack Hint

- SwiftUI and Compose often use a `Spacer()` between the main text block and the accessory
- UIKit, Android Views, and React Native typically need a flexible text container plus spacing or flex behavior that keeps the accessory pinned to the opposite edge
- In React Native, do not assume `row-reverse` is always the answer if the screen already inherits RTL correctly; verify the rendered result

Important: do not mirror the code mechanically. Mirror the visual result.

Before sweeping a whole screen, fix one sentinel row first and confirm:

- text is visually right
- accessory is visually left
- there is visible space between them

Only then apply the pattern to the rest of the screen.

## Local Control Direction

Some compound controls should keep their internal order even inside Arabic screens.

Examples:

- plus/minus controls
- numeric steppers
- segmented controls
- playback controls

These are two separate checks:

- is the whole control placed on the correct side of the Arabic row
- is the control's internal symbol order still correct

If the control lands on the correct side but its internal order becomes wrong, consider a local LTR treatment for the control itself while keeping the surrounding row RTL.

## Navigation, Icons, And Motion

In Arabic screens:

- back arrows should point to the right
- disclosure arrows should stay opposite the main text block
- directional icons should match the actual navigation or action direction
- gestures and directional animations should be checked visually, not assumed

React Native note:

- source images do not auto-flip just because the app is RTL
- when an icon has directional meaning, use `I18nManager.isRTL` to choose an alternate asset or apply a directional transform

## Cards

For Arabic cards:

- titles, descriptions, and supporting copy should be full-width and direction-aware
- the main content column belongs on the visual right unless design explicitly says otherwise
- secondary chips, badges, or metrics can vary, but the Arabic content block should still read as anchored to the Arabic side

## Common Failure Modes

Watch for these recurring mistakes:

- Arabic text uses intrinsic width only and appears to float
- developer hard-codes `right/left` instead of using framework-native logical direction
- a second local RTL override is added inside a screen that already inherits RTL
- text and accessory bunch together because the row has no flexible text area or spacing
- directional icons remain LTR in an Arabic flow
- React Native absolute positioning ignores RTL behavior
- Android Views still use left/right margins or paddings instead of start/end
- the control is on the correct side, but its internal plus/minus order is reversed
- the implementation mirrors code symmetry rather than the actual visual Arabic result

## Visual QA Checklist

Do not stop after changing shared components. Check every affected screen visually.

Verify:

- page title
- subtitle or helper copy
- card titles
- card descriptions
- row titles
- row subtitles
- metric labels and values
- disclosure arrows
- back arrows
- bottom CTA spacing
- whether the root already inherits RTL
- whether any local override is fighting the inherited RTL behavior
- whether a full-width Arabic sentinel lands on the visual right
- whether a sentinel row has real empty space between text and accessory
- whether directional icons are correct
- whether control internals need their own local LTR treatment
- whether animations or gestures with direction still feel correct

If a row has both text and an accessory, confirm the text is visually right and the accessory is visually left.

## Working Style

When fixing Arabic mobile UI:

1. Identify the stack first: iOS native, Android native, or React Native
2. Determine whether RTL is already enforced at the root
3. Fix text block width and logical alignment first
4. Fix row composition second
5. Fix arrows, icons, and directional motion third
6. Run a visual RTL QA sweep on every affected screen

Do not assume that "RTL is enabled" means the screen is already correct.

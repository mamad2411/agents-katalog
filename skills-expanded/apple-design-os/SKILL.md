---
name: apple-design-os
description: "Use when designing app UI for Apple operating systems — iOS/iPadOS surfaces (sheets, detents, tab bars, large titles, widgets, lock screen, Dynamic Island), macOS (windows, traffic lights, sidebars, menus, vibrancy), visionOS spatial design, watchOS (complications, Digital Crown), or the standard UIKit/SwiftUI component anatomy (nav bars, lists, forms, buttons, alerts, search, empty states). Part of the apple-design family. Keywords: iOS design, iPadOS, macOS Tahoe, visionOS, watchOS, spatial, ornament, sheet, presentationDetents, tab bar, navigation bar, large title, sidebar, traffic lights, widget, dynamic island, stage manager, components, SwiftUI, List, Form, button hierarchy, ContentUnavailableView, alert, searchable."
---

# Apple Design — OS Surfaces & Components

Designing native-feeling app UI across Apple's platforms, plus the standard component library.

## When to use
- Laying out an iOS/iPadOS/macOS/visionOS/watchOS screen or its chrome.
- Choosing/standardizing a component (nav bar, list style, button hierarchy, sheet, alert, empty state).

## Core rules
- **Anchor primary controls in reach** — bottom on iPhone (tab bar 49pt + safe area), and prefer the platform's native bar/sheet patterns over reinventing chrome.
- **Sheets use detents** (medium/large/custom) with a grabber; modals are for focused tasks, not navigation.
- **Match the platform's input model**: touch (44pt targets) on iOS, pointer precision + the global menu bar on macOS, gaze (60pt targets) + eye/pinch on visionOS, Digital Crown + glanceability on watchOS.
- **Use the documented button hierarchy** (`borderedProminent` → `bordered` → `borderless`) and the right list style (plain / grouped / insetGrouped); always design **empty states** (`ContentUnavailableView`).
- iOS 26 / macOS Tahoe restyle controls in **Liquid Glass** (floating, translucent) — see apple-design-materials.

## References
| File | Use for |
|---|---|
| `references/ios-ipados.md` | Home/lock/control surfaces, nav/tab/sheet metrics, iOS 26 glass, iPad windowing |
| `references/macos.md` | Windows, traffic lights, toolbars, sidebars, menu bar, vibrancy, Tahoe glass |
| `references/visionos-watchos.md` | Spatial windows/ornaments/immersion + watchOS complications/crown/glance |
| `references/app-component-anatomy.md` | The full UIKit/SwiftUI component catalog + CSS mimics of iOS lists/toggles/segments |

## Common mistakes
- Top-only controls out of thumb reach; faking native chrome with wrong metrics.
- Touch-sized targets on a pointer OS (or vice-versa); modal overuse; missing empty states.
- Tiny gaze targets / motion-sickness triggers in visionOS; dense watch faces.

**Related:** the glass on these surfaces → apple-design-materials · their motion/gestures → apple-design-motion · spacing/type → apple-design-foundations.

---
name: platform-conventions
description: Design to iOS Human Interface Guidelines and Android Material Design 3 conventions — navigation structure, controls, typography scaling, gesture zones, iconography — plus when to follow each platform versus unify cross-platform. Use when shipping native iOS/Android apps.
license: MIT license
category: docs
metadata: {"version": "1.0", "skill-author": "MC Dean (designer-skills)"}
---

# Platform Conventions

Map which patterns are platform-mandated, where iOS and Android genuinely diverge, and when a unified
cross-platform design is the right call. 中文触发：iOS/Android 平台规范、原生控件差异、跨端统一设计。

## Navigation

| Pattern | iOS (HIG) | Android (Material 3) |
|---|---|---|
| Back navigation | Swipe right from the left edge; back button top-left | System back gesture (either edge) or predictive back; arrow in app bar |
| Primary structure | Tab bar at bottom; sidebar on iPad | Navigation bar at bottom, or navigation drawer |
| History model | Stack per tab; each tab keeps its own stack | Single back stack; tabs do not keep independent history by default |
| Bottom navigation | Up to 5 tabs, labels optional | 3–5 tabs, labels required |

**Implication**: iOS users expect swipe-from-left-edge to always go back — reserve that gesture zone.
On Android the system back gesture owns it, so a swipe-from-left drawer does not conflict.

## Controls

| Component | iOS | Android (M3) |
|---|---|---|
| Toggle | `UISwitch`, pill, right-aligned in lists | Switch, thumb-and-track, inline or in lists |
| Destructive confirmation | Action sheet from the bottom, red destructive option | Dialog with text buttons, error tone |
| Date/time picker | Wheel or inline calendar | Calendar with text-input alternative |
| Selection menu | Picker wheel or action sheet | Exposed dropdown or modal bottom sheet |
| Primary button | Filled rectangle, full-width in forms | Filled button, rounded by default in M3 |
| Floating action | Not a convention — use contextual buttons | FAB, bottom-right, primary surface action |
| Pull to refresh | `UIRefreshControl` | `SwipeRefreshLayout` — same gesture, different visual |

## Typography

| Attribute | iOS | Android |
|---|---|---|
| System font | SF Pro (SF Compact on watch) | Roboto / Google Sans |
| Scaling | Dynamic Type, required | Scalable pixels (sp), must respect system font scale |
| Type scale | iOS text styles (Large Title, Title 1–3, Body…) | Material scale (Display, Headline, Title, Body, Label) |

Both platforms require respecting system font size. **Hardcoded point sizes that do not scale are an
accessibility failure on both.**

## Gestures

| Gesture | iOS | Android |
|---|---|---|
| Swipe to delete | Standard in table views | Swipe to dismiss/archive, context-dependent |
| Long press | Peek / context menu | Contextual action mode; long press to select |
| Pinch to zoom | Standard in maps and images | Standard |
| Back swipe | Reserved — always navigates back | Predictive back gesture, opt-in preview |

## Visual and iconography

| Area | iOS | Android |
|---|---|---|
| Icons | SF Symbols (variable weight, auto-scale) | Material Symbols (rounded, outlined, sharp) |
| Corner radius | Larger squircle/superellipse curves | Moderate; M3 uses prominent rounding |
| System colours | Dynamic colours adapting light/dark | Material You dynamic colour from wallpaper |
| Modal | Sheet sliding up from bottom with grab handle | Bottom sheet (standard or modal) or full-screen dialog |

## Cross-platform decision

**Follow each platform strictly when**: the app is native or near-native and platform fluency is part
of the quality signal (banking, health, utilities); it integrates deeply with OS features (share sheet,
widgets, assistants); power users are platform-experienced.

**Unify when**: feature parity is high and consistency lowers maintenance cost; cross-device
continuity matters; it is a B2B tool where users live inside your own design system.

**Hybrid (the usual answer)**: one visual and component language, with platform-specific adaptations
for navigation, system controls and gesture conflicts. *It looks like itself; it behaves like the OS.*

## What not to do
- Do not put a bottom tab bar on Android where it fights the gesture-navigation swipe-up
- Do not suppress the iOS swipe-back gesture — users who trigger it and get nothing lose trust
- Do not use iOS action sheets on Android (or Android dialogs on iOS) as the primary decision pattern
- Do not ignore Dynamic Type / sp scaling on either platform
- Do not transplant the FAB to iOS without justification — it has no native precedent there

## Working rules
- Re-read the current HIG / Material 3 before each major design phase; both change often
- Audit the native app for the interaction you are designing before proposing a solution
- Keep a component mapping document: design-system name ↔ iOS name ↔ Android name
- Test on real devices; simulators differ on gesture handling
- When in doubt use what ships in the OS — it is already tested and already familiar

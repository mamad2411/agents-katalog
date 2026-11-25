---
name: ux-tablet
description: "Apply medium-specific UX reasoning for TABLET applications: the hybrid medium that is touch-first but large-screen, often two-handed, sometimes with an attached keyboard/pointer, and capable of multi-pane and split-view multitasking. Use alongside ux-first-principles when the target is a tablet (iPad or Android tablet) and the decision is affected by touch sizing, large-screen density, two-handed reach, multi-pane layout, or intermittent pointer/keyboard. USE FOR: 'design a tablet app', 'lay out this iPad screen', 'should this be one pane or two on tablet', multi-pane and split-view layout, two-handed reach, large touch-screen density. DO NOT USE FOR: the invariant principles (use ux-first-principles); phone or desktop layouts (use ux-mobile or ux-desktop); picking colors, fonts, or platform chrome (use a styling/execution skill)."
---

# UX for Tablet

A thin medium layer, and the trickiest of the three — tablet is a genuine hybrid that inherits rules from both neighbors and contradicts each of them in places. The reasoning lives in `ux-first-principles`; read it first or alongside. Here is what the tablet *medium* changes.

## What defines the tablet medium
Touch-first input on a large screen, frequently held two-handed (or propped), often with an attached keyboard and/or pointer *some of the time*, and capable of showing two or more panes at once and running split-view alongside another app. The defining trait is **intermittency**: the same app may be pure-touch in one moment and pointer-plus-keyboard the next, fullscreen now and half-width in split-view a moment later.

## Where tablet inherits — and where it breaks the rule

**Inherits from mobile (touch is the baseline assumption):**
- **Target sizing:** assume fingertips. Use touch-sized targets and spacing as the floor, exactly as on phones — do not drop to desktop density just because the screen is big.
- **No guaranteed hover:** a pointer may be attached, but it usually isn't. Never make essential information or actions hover-only; hover can be a progressive *enhancement* when a pointer is present, never a requirement.
- **Gestures and signifiers:** swipe/long-press/pinch apply; signpost them, provide visible alternatives.

**Inherits from desktop (the screen is large):**
- **Density can rise — carefully:** the large screen supports multi-pane layouts (list + detail), persistent sidebars, and more content in view than a phone. Use the room for a master-detail or two-column structure rather than forcing the phone's single-column flow. But keep *touch* sizing while raising *information* density — the combination is what makes tablet distinct.
- **Multi-pane and split-view:** tablets do split-view / slide-over multitasking, so your app may be half-width unexpectedly. Layouts must adapt between one-pane (narrow / split) and multi-pane (full width) — this is the tablet's signature responsive behavior.

## The two things unique to tablet

1. **Two-handed reach reshapes the comfortable zones.** Held in two hands in landscape, the comfortable touch areas shift to the left and right edges and the bottom; the center-top is the hardest to reach. This is different from the phone's single bottom-center thumb zone. Place primary controls along the reachable edges, not stranded in the middle of a wide screen.

2. **Adaptive layout is the core decision.** The central tablet question is "one pane or two (or more), and what happens when width changes?" Decide the breakpoints by content and reachability, and make panes collapse/expand gracefully between fullscreen and split-view. A tablet design that only works fullscreen is unfinished.

## How principles shift on tablet
- **Fitts's Law:** touch-sized targets (floor), but reach is edge-and-corner oriented in two-handed use, not bottom-center.
- **Hick's Law / hierarchy:** the larger canvas lets you show more than a phone without crowding — but resist desktop-level density; the finger still needs room.
- **Progressive disclosure:** master-detail panes *are* progressive disclosure made spatial — selecting in the list reveals detail in the pane, no extra screen needed.
- **Consistency across width:** the same app must feel coherent fullscreen and in split-view; don't redesign, adapt.

## Render-time platform handoff (NOT design decisions)
Mechanical per-platform substitutions, handled in styling / at render time (e.g., by .NET MAUI), not reasoned from principles:
- Exact minimum touch-target metric, system fonts, control styling, corner radii, material/elevation.
- Platform multitasking chrome and the standard system affordances.
- OS-global gestures: respect system back / home / multitasking / split-view gestures rather than overriding them.

**Everything else — including structural choices like single-pane vs. master-detail, where the navigation lives, and how panes adapt — is a design decision. Reason it from first principles and commit to ONE answer that works across tablet platforms. Do not fork the structure per OS.**

## Deliberate scope note
This optimizes for a coherent cross-platform product over maximal single-OS idiomaticity — the right trade-off for cross-platform work, and especially natural on tablet where the master-detail idiom is shared across platforms. It bites only an app whose whole value proposition is feeling 100% hand-built-native on one OS.

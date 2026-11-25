---
name: liquid-glass-reference
description: >
  Quick-reference API cheat sheet and resources for iOS 26 Liquid Glass in SwiftUI — every core
  modifier, Glass type, button style, container, toolbar/navigation/TabView/search/sheet API, plus
  a complete working sample app and links to Apple's official WWDC 2025 sessions, docs, and the HIG.
  Use this skill when the user wants a fast API lookup ("what's the signature for glassEffectID",
  "list the glass modifiers", "which control sizes exist"), a full runnable example to copy, or
  authoritative links to Apple documentation and WWDC sessions on Liquid Glass. Trigger on "liquid
  glass cheat sheet", "glass API reference", "liquid glass sample app", "full glass example", "WWDC
  liquid glass", or "apple liquid glass docs".
---

# Liquid Glass API Quick Reference

Condensed signatures. For explanations and patterns, see the topic skills:
**liquid-glass-foundations**, **-containers**, **-controls**, **-advanced**, **-troubleshooting**,
**-best-practices**.

## Core modifiers

```swift
.glassEffect() -> some View
.glassEffect(_ glass: Glass, in shape: some Shape, isEnabled: Bool) -> some View
.glassEffectID<ID: Hashable>(_ id: ID, in namespace: Namespace.ID) -> some View
.glassEffectUnion<ID: Hashable>(id: ID, namespace: Namespace.ID) -> some View
.glassEffectTransition(_ transition: GlassEffectTransition, isEnabled: Bool) -> some View
.glassBackgroundEffect(in: some Shape, displayMode: GlassDisplayMode) -> some View
```

## Glass types

```swift
Glass.regular    // default adaptive variant
Glass.clear      // high transparency variant
Glass.identity   // no effect

.tint(_ color: Color)   // add color tint
.interactive()          // interactive behaviors (iOS only)
```

## Button styles

```swift
.buttonStyle(.glass)           // translucent
.buttonStyle(.glassProminent)  // opaque, prominent
```

## Container

```swift
GlassEffectContainer { /* .glassEffect() views */ }
GlassEffectContainer(spacing: CGFloat) { /* controlled morphing distance */ }
```

## Toolbar & navigation

```swift
.toolbar { }                            // automatic glass styling
ToolbarSpacer(.fixed, spacing: CGFloat)
ToolbarSpacer(.flexible)
.badge(Int)
.sharedBackgroundVisibility(.hidden)
```

## TabView

```swift
.tabBarMinimizeBehavior(.onScrollDown)   // .automatic | .onScrollDown | .never
.tabViewBottomAccessory { }
```

## Search

```swift
.searchable(text: Binding<String>)
.searchToolbarBehavior(.minimized)
DefaultToolbarItem(kind: .search, placement: .bottomBar)
```

## Sheets & presentations

```swift
.presentationDetents([.medium, .large])
.scrollContentBackground(.hidden)
.containerBackground(.clear, for: .navigation)
.navigationTransition(.zoom(sourceID: ID, in: Namespace.ID))
.matchedTransitionSource(id: ID, in: Namespace.ID)
```

## Other

```swift
.backgroundExtensionEffect()
.controlSize(.mini | .small | .regular | .large | .extraLarge)
.buttonBorderShape(.capsule | .circle | .roundedRectangle)
```

## Complete sample app

A full, runnable Liquid Glass app (glass TabView + search tab, tab-bar minimize, bottom Now-Playing
accessory, badged toolbar, morphing floating action button) is in
[references/LiquidGlassSampleApp.swift](references/LiquidGlassSampleApp.swift). Copy it into a new
iOS 26 SwiftUI project to see the pieces working together.

## Official Apple resources

**WWDC 2025 sessions:**
- 219 — Meet Liquid Glass
- 323 — Build a SwiftUI app with the new design
- 356 — Get to know the new design system
- 101 — Keynote · 102 — Platforms State of the Union

**Documentation & design:**
- https://developer.apple.com/documentation/TechnologyOverviews/liquid-glass
- https://developer.apple.com/documentation/swiftui/view/glasseffect(_:in:)
- https://developer.apple.com/documentation/swiftui/glasseffectcontainer
- https://developer.apple.com/documentation/SwiftUI/Applying-Liquid-Glass-to-custom-views
- https://developer.apple.com/design/human-interface-guidelines/materials
- https://developer.apple.com/design/new-design-gallery/

**Apple sample code:** Landmarks (Building an app with Liquid Glass); Refining toolbar glass effects.

## Community resources

**GitHub:** mertozseven/LiquidGlassSwiftUI · GonzaloFuentes28/LiquidGlassCheatsheet ·
GetStream/awesome-liquid-glass · artemnovichkov/iOS-26-by-Examples · mizadi/LiquidGlassExamples

**Blogs:** Donny Wals (custom UI with Liquid Glass) · Swift with Majid (glassifying custom views) ·
Nil Coalescing (Liquid Glass sheets) · Create with Swift (design principles) · SerialCoder.dev
(morphing).

---

*Environment: iOS 26.0+ / Xcode 26.0+. Derived from Conor Luddy's Liquid Glass reference,
last updated November 16, 2025.*

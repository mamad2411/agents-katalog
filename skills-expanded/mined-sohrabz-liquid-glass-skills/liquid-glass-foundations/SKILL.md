---
name: liquid-glass-foundations
description: >
  The starting point for building with iOS 26 Liquid Glass in SwiftUI. Covers the core mental
  model (glass is the navigation layer, never content), the three material variants
  (.regular / .clear / .identity), the .glassEffect() modifier, tinting and .interactive(),
  custom shapes, glass on text and icons, and automatic accessibility adaptation. Use this skill
  whenever the user wants to add a "liquid glass", "glassmorphism", "frosted glass", or
  "translucent" effect to a SwiftUI view for iOS 26 / iPadOS 26 / macOS Tahoe 26, mentions
  ".glassEffect", "Glass.regular", "Glass.clear", asks "how do I make this glassy", "how do I
  tint glass", "what glass variant should I use", or is starting any Liquid Glass work and needs
  the fundamentals. Load this proactively on any iOS 26 SwiftUI project that uses glass so the
  correct variant, shape, and layering rules are applied from the start.
---

# Liquid Glass Foundations (iOS 26 / SwiftUI)

Liquid Glass is Apple's translucent, dynamic material introduced at WWDC 2025. It reflects and
refracts surrounding content (lensing) and morphs to focus the user on their task. It spans iOS 26,
iPadOS 26, macOS Tahoe 26, watchOS 26, tvOS 26, and visionOS 26.

**The one rule that governs everything:** Liquid Glass is *exclusively* for the **navigation layer**
that floats above app content — toolbars, tab bars, buttons, floating controls, sheets. **Never
apply it to content** (lists, tables, media, scrollable body, full-screen backgrounds). Content
stays primary; glass is the functional overlay. Getting this wrong is the #1 anti-pattern.

## Material variants

| Variant | Use case | Transparency | Adaptivity |
|---------|----------|--------------|------------|
| `.regular` | Default for most UI | Medium | Full — adapts to any content |
| `.clear` | Media-rich backgrounds | High | Limited — requires a dimming layer |
| `.identity` | Conditionally disable the effect | None | N/A |

- **Regular** — toolbars, buttons, nav bars, tab bars, standard controls. Start here.
- **Clear** — only small floating controls over photos/maps, and only when **all three** hold:
  (1) element sits over media-rich content, (2) content tolerates a dimming layer, (3) foreground
  content on the glass is bold and bright.
- **Identity** — for conditional toggling, e.g. `glassEffect(isEnabled ? .regular : .identity)`.

## Basic implementation

```swift
import SwiftUI

struct BasicGlassView: View {
    var body: some View {
        Text("Hello, Liquid Glass!")
            .padding()
            .glassEffect()  // Default: .regular variant, .capsule shape
    }
}
```

Explicit parameters and the signature:

```swift
Text("Custom Glass")
    .padding()
    .glassEffect(.regular, in: .capsule, isEnabled: true)

func glassEffect<S: Shape>(
    _ glass: Glass = .regular,
    in shape: S = DefaultGlassEffectShape,
    isEnabled: Bool = true
) -> some View
```

## Glass type: tinting and interactivity

```swift
struct Glass {
    static var regular: Glass
    static var clear: Glass
    static var identity: Glass
    func tint(_ color: Color) -> Glass
    func interactive() -> Glass
}
```

**Tinting** — conveys *semantic meaning* (primary action, state), not decoration. Use sparingly,
mainly for call-to-action.

```swift
.glassEffect(.regular.tint(.blue))
.glassEffect(.regular.tint(.purple.opacity(0.6)))   // with opacity
```

**Interactive** (iOS only) — adds scaling on press, bounce, shimmer, touch-point illumination that
radiates to nearby glass, and response to tap/drag:

```swift
Button("Tap Me") { }
    .glassEffect(.regular.interactive())
```

Chaining order doesn't matter:

```swift
.glassEffect(.regular.tint(.orange).interactive())
.glassEffect(.clear.interactive().tint(.blue))
```

## Custom shapes

```swift
.glassEffect(.regular, in: .capsule)                 // default
.glassEffect(.regular, in: .circle)
.glassEffect(.regular, in: RoundedRectangle(cornerRadius: 16))
.glassEffect(.regular, in: .rect(cornerRadius: .containerConcentric))  // aligns to container
.glassEffect(.regular, in: .ellipse)

struct CustomShape: Shape {
    func path(in rect: CGRect) -> Path { /* ... */ }
}
.glassEffect(.regular, in: CustomShape())
```

**Corner concentricity** keeps elements aligned with their container/window corners across devices:

```swift
RoundedRectangle(cornerRadius: .containerConcentric, style: .continuous)
```

## Text and icons on glass

Text on glass automatically gets vibrant treatment (color/brightness/saturation adjust to the
background). Keep foreground content high-contrast.

```swift
Text("Glass Text")
    .font(.title).bold()
    .foregroundStyle(.white)   // high contrast for legibility
    .padding()
    .glassEffect()

Image(systemName: "heart.fill")
    .font(.largeTitle)
    .foregroundStyle(.white)
    .frame(width: 60, height: 60)
    .glassEffect(.regular.interactive())

Label("Settings", systemImage: "gear")
    .labelStyle(.iconOnly)
    .padding()
    .glassEffect()
```

## Accessibility (automatic — don't fight it)

The system adapts glass with **no code changes**:
- **Reduced Transparency** → increases frosting
- **Increased Contrast** → stark colors and borders
- **Reduced Motion** → tones down animation and elastic effects
- **iOS 26.1+ Tinted mode** → user-controlled opacity increase (Settings → Display & Brightness → Liquid Glass)

If you must branch on it, read the environment values:

```swift
@Environment(\.accessibilityReduceTransparency) var reduceTransparency
@Environment(\.accessibilityReduceMotion) var reduceMotion

Text("Accessible")
    .padding()
    .glassEffect(reduceTransparency ? .identity : .regular)
```

**Best practice:** let the system handle accessibility. Don't override unless absolutely necessary.

## Where to go next

- Combining/morphing multiple glass elements → **liquid-glass-containers**
- Buttons, toolbars, tab bars, sheets, search → **liquid-glass-controls**
- FAB clusters, symbol effects, performance, gestures → **liquid-glass-advanced**
- Busy backgrounds, backward compat, UIKit, known bugs → **liquid-glass-troubleshooting**
- When to use glass, design principles, anti-patterns → **liquid-glass-best-practices**
- Full API cheat sheet + complete sample app → **liquid-glass-reference**

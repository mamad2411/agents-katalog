---
name: liquid-glass-troubleshooting
description: >
  Fix, adapt, and ship iOS 26 Liquid Glass in the real world: readability over busy/media
  backgrounds (gradient fade, dimming, tinting, variant choice), correct layering (avoid
  glass-on-glass), platform differences (iOS/iPadOS/macOS/watchOS/tvOS/visionOS) and minimum
  OS/device requirements, iOS 18 backward compatibility (availability fallback + opt-out via
  UIDesignRequiresCompatibility), UIKit integration (UIGlassEffect, UIGlassContainerEffect), known
  beta bugs with workarounds, and performance/battery implications. Use this skill when the user
  reports glass that's "hard to read", "looks wrong over an image", "has rendering artifacts",
  widgets showing a black background, disorienting toolbar animation on navigation, asks "how do I
  support iOS 18 too", "how do I use glass in UIKit", or "why is my battery draining". Trigger on
  "glass unreadable", "busy background", "glass-on-glass", "UIDesignRequiresCompatibility",
  "UIGlassEffect", "glassProminent artifacts", "widget black background".
---

# Liquid Glass Troubleshooting & Real-World Adaptation

Field fixes for readability, layering, platform/version support, UIKit, known bugs, and
performance. (Basics: **liquid-glass-foundations**.)

## Readability over complex backgrounds

Glass over busy/colorful/animated content becomes hard to read. Four remedies, roughly in order of
preference:

**1. Gradient fade** — fade a background color in behind the control. A reusable modifier
(`deliquify()`) is in [references/BackgroundFade.swift](references/BackgroundFade.swift):

```swift
ScrollView { ColorfulContent() }.deliquify()
```

**2. Strategic tinting** — add semantic color for contrast:

```swift
.glassEffect(.regular.tint(.purple.opacity(0.8)))
```

**3. Choose the right variant** — `.regular` for most contexts; `.clear` only over media-rich
content with bold foreground.

**4. Background dimming** — required when using `.clear` over imagery:

```swift
ZStack {
    BackgroundImage().overlay(Color.black.opacity(0.3))   // subtle dimming
    GlassControls().glassEffect(.clear)
}
```

## Layering: avoid glass-on-glass

```swift
// ❌ Confusing hierarchy — stacked glass
VStack {
    HeaderView().glassEffect()
    ContentView().glassEffect()
    FooterView().glassEffect()
}

// ✅ One floating glass layer over plain content
ZStack {
    ContentView()                 // no glass
    HeaderView().glassEffect()    // single floating layer
}
```

Layering philosophy: **content** (bottom, no glass) → **navigation** (middle, Liquid Glass) →
**overlay** (top, vibrancy/fills on glass).

## Platform differences

| Platform | Adaptations |
|----------|-------------|
| iOS | Floating tab bars, bottom search placement |
| iPadOS | Floating sidebars, ambient reflection, larger shadows |
| macOS | Concentric window corners, adaptive search bars, taller controls |
| watchOS | Location-aware widgets, fluid navigation |
| tvOS | Focused glass effects, directional highlights |

**Minimums:** iOS/iPadOS/macOS Tahoe/watchOS/tvOS/visionOS **26.0+**, Xcode **26.0+**.
**Devices:** iPhone 11 / iPhone SE (2nd gen) or later get the full effect; older devices fall back to
frosted glass with reduced effects.

## Backward compatibility (supporting iOS 18)

Recompiling with Xcode 26 adopts glass automatically. To hold off (expires with iOS 27):

```xml
<!-- Info.plist -->
<key>UIDesignRequiresCompatibility</key>
<true/>
```

For code that runs on both iOS 26 and iOS 18, gate on availability with a manual fallback. A
drop-in `glassedEffect(...)` extension is in
[references/GlassCompat.swift](references/GlassCompat.swift):

```swift
Text("Compatible")
    .padding()
    .glassedEffect(in: Capsule(), interactive: true)
```

## UIKit integration

```swift
import UIKit

let glassEffect = UIGlassEffect(glass: .regular, isInteractive: true)
let effectView = UIVisualEffectView(effect: glassEffect)
effectView.frame = CGRect(x: 0, y: 0, width: 200, height: 50)
view.addSubview(effectView)

let containerEffect = UIGlassContainerEffect()
let containerView = UIVisualEffectView(effect: containerEffect)
```

Best practices: remove custom backgrounds so glass shows; update presentation controllers for
sheets; handle `UIBarButtonItem` sizing; use `hidesSharedBackground = true` to drop glass from
specific items.

## Known issues & workarounds (beta)

- **Interactive shape mismatch** — `.glassEffect(.regular.interactive(), in: RoundedRectangle())`
  responds with a Capsule shape. Workaround: use `.buttonStyle(.glass)` for buttons.
- **`.glassProminent` + `.circle` artifacts** — add `.clipShape(Circle())`.
- **Widget black background** (Standard/Dark modes) — no complete fix; Tinted and Transparent modes
  work with `Color.clear`.
- **Disorienting toolbar animation on navigation** — give the item a stable id:
  ```swift
  ToolbarItem(id: "constantID") { Button("Done") { } }
  ```

## Performance implications

- **Battery:** early testing showed ~13% drain (iOS 26) vs ~1% (iOS 18) on iPhone 16 Pro Max, plus
  more heat and higher CPU/GPU load on older devices.
- **Optimize:** use `GlassEffectContainer` for multiple elements; limit continuous animations; let
  glass rest; test on ~3-year-old devices; profile with Instruments.
- **Memory:** real-time blur consumes GPU memory and samples a larger area than the element; shared
  sampling regions reduce that overhead.

## Related skills

- Performance-first patterns → **liquid-glass-advanced**
- Design rules that prevent most of these problems → **liquid-glass-best-practices**

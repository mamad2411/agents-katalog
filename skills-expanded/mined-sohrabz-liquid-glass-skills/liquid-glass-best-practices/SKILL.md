---
name: liquid-glass-best-practices
description: >
  Design guidance and review checklist for iOS 26 Liquid Glass in SwiftUI: when to use glass vs
  traditional UI, the hierarchy/contrast/tinting/morphing design principles, accessibility
  excellence (system features + developer responsibilities + a testing checklist), the visual /
  technical / usability anti-patterns to avoid, and a device/environment/performance testing
  strategy. Use this skill when the user asks "should I use glass here", "is this good liquid glass
  design", "am I overusing glass", "what are the do's and don'ts", wants a design review or
  accessibility check of a glass UI, is deciding where glass belongs in an app, or needs a
  pre-ship testing plan. Trigger on "when to use liquid glass", "liquid glass anti-patterns",
  "glass accessibility checklist", "glass design principles", "review my glass UI", "glass
  contrast", or "glass testing".
---

# Liquid Glass Best Practices & Design Patterns

Use this as a design lens and review checklist. The governing rule (from **liquid-glass-foundations**)
holds throughout: **glass is the navigation layer, never the content.**

## When to use glass vs traditional UI

**Use Liquid Glass for:**
- ✅ Navigation bars and toolbars
- ✅ Tab bars and bottom accessories
- ✅ Floating action buttons
- ✅ Sheets, popovers, and menus
- ✅ Context-sensitive controls
- ✅ System-level alerts

**Avoid Liquid Glass for:**
- ❌ Content layer (lists, tables, media)
- ❌ Full-screen backgrounds
- ❌ Scrollable content
- ❌ Stacked glass layers
- ❌ Every UI element

> Apple's guidance: "Liquid Glass is best reserved for the navigation layer that floats above the
> content of your app."

## Design principles

**Hierarchy** — content is primary; glass controls are the secondary functional layer; overlay
fills/vibrancy are tertiary.

**Contrast management** — keep a minimum 4.5:1 contrast ratio, test legibility across backgrounds,
use vibrant text on glass, add subtle borders for definition.

**Tinting philosophy** — tint selectively for primary actions; don't tint everything; tint conveys
*meaning*, not decoration; it's compatible with all glass behaviors.

**Morphing guidance** — use morphing for state transitions, maintain visual continuity, apply bouncy
animations, and group related elements in a `GlassEffectContainer`.

## Accessibility excellence

System features (automatic): Reduced Transparency, Increased Contrast, Reduced Motion, iOS 26.1+
Tinted mode toggle.

Developer responsibilities: never override system settings; test with every accessibility mode
enabled; ensure text legibility; provide adequate touch targets; support VoiceOver properly.

**Accessibility testing checklist:**
- [ ] Reduced Transparency enabled
- [ ] Increased Contrast enabled
- [ ] Reduce Motion enabled
- [ ] Tinted mode (iOS 26.1+)
- [ ] VoiceOver navigation
- [ ] Dynamic Type sizes
- [ ] Color-blindness simulators
- [ ] Bright sunlight conditions

## Anti-patterns to avoid

**Visual:** overuse (glass everywhere) · glass-on-glass stacking · glass on the content layer ·
tinting everything · breaking concentricity.

**Technical:** custom opacity that bypasses accessibility · ignoring safe areas · hard-coded color
schemes · mixing Regular and Clear variants · multiple separate glass effects without a container.

**Usability:** busy backgrounds without dimming · insufficient contrast · excessive animation ·
breaking iOS conventions · prioritizing aesthetics over usability.

## Testing strategy

**Devices:** iPhone 11–13 (older) · iPhone 14–15 (mid) · iPhone 16+ (latest) · iPad Pro with Stage
Manager · Mac with Apple Silicon.

**Environments:** bright outdoor sunlight · low light · varied wallpapers (light/dark/colorful/
photos) · user-generated content backgrounds.

**Performance:** 30+ minute sessions (thermal) · scroll performance · animation frame rates ·
battery-drain measurement · memory-pressure monitoring.

## Key takeaways

1. Reserve Liquid Glass for the navigation layer only.
2. Always use `GlassEffectContainer` for multiple glass elements.
3. Test extensively with accessibility settings enabled.
4. Monitor performance on older devices.
5. Respect user preferences and system settings.
6. Prioritize content legibility over visual effects.
7. Use morphing transitions for smooth state changes.
8. Follow Apple's design guidelines and the HIG.

## Related skills

- The fixes when a background *is* busy → **liquid-glass-troubleshooting**
- Performance mechanics behind these rules → **liquid-glass-advanced**
- Official HIG/WWDC links → **liquid-glass-reference**

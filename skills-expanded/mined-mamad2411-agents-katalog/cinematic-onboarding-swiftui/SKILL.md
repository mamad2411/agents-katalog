---
name: cinematic-onboarding-swiftui
description: "USE THIS SKILL to build cinematic, animated SwiftUI onboarding flows for iOS apps — multi-step structure with smooth fade/scale transitions, animated progress bar, rotating testimonials, hero header/footer images, and modern async/await timing patterns. Adapts the proven 3-step Adam Lyttle reference implementation to any app's domain."
user-invocable: true
---

# Cinematic SwiftUI Onboarding

Build a bold, animated, dark-mode SwiftUI onboarding flow with hero imagery and step transitions. This skill adapts a battle-tested reference implementation (`references/OnboardingCinematicView-original.swift`, by Adam Lyttle) to whatever domain the user's app is in.

## When to Use This Skill

- Adding a first-launch onboarding flow to an iOS SwiftUI app
- Replacing a generic carousel onboarding with something more cinematic
- Building 3-5 step "transformation story" onboarding before a paywall
- The user wants animated transitions between steps, not just static cards
- The app is iOS 16+ (NavigationStack, fullScreenCover, modern animation API)

If the user is also planning the _content_ and _psychology_ of onboarding (questionnaire flow, paywall, viral moment), pair this with `app-onboarding-questionnaire`. This skill handles the **visual + animation craft**; that one handles the conversion strategy.

## What's Different About This Pattern

Most SwiftUI onboarding tutorials produce static carousels. This pattern is built around three distinguishing techniques:

1. **Layered ZStack with hero header/footer** — full-bleed images at the top and bottom of the screen create a cinematic frame around the content. The content lives inside a centered VStack that can change per-step.
2. **Cross-fade step transitions** — instead of horizontal swipe, the content opacity fades to 0, the step index updates, and opacity fades back to 1. Animations are synchronised so the progress bar advances _during_ the fade, not before.
3. **Reveal animations on enter** — components like the testimonial card scale-in (2× → 1×), blur-in (radius 20 → 0), and rotate (30° → 0°) simultaneously. This is what makes it feel "cinematic" rather than functional.

Replicate these three things and the result feels premium. Skip them and it's just another carousel.

## Quick Start

1. Read `references/OnboardingCinematicView-original.swift` to see the full reference implementation.
2. Look at the app's domain — what's it about? What's the hero imagery? What testimonials make sense?
3. Generate placeholder hero images at the right aspect ratios (or ask the user to drop in real ones).
4. Adapt the 3-step content to the app's domain — Welcome / Core feature demo / Differentiator.
5. Wire it into the app via `fullScreenCover` controlled by an `@AppStorage` flag.

## Architecture

The reference is a single SwiftUI file containing five views. Keep this layout when adapting:

```
OnboardingCinematicView           // Top-level: ZStack + step state machine
├── OnboardingHeaderView          // Hero header + footer images, ignores safe area
├── OnboardingProgressView        // Animated progress dots with SF Symbols
├── (step-specific content view)
│   ├── Step 0: Welcome + OnboardingTestimonialView
│   ├── Step 1: Title + CustomAnimationFishPhotoView (or your domain's animation)
│   └── Step 2: Title + CustomAnimationDigitalSharkView (or your differentiator animation)
├── OnboardingTestimonialView     // Auto-rotating testimonials with reveal animation
└── (continue button + social proof line)
```

State lives at the top: `step: Int`, `animatedStep: Int`, `onboardingOpacity: Double`. The cross-fade is the choreography of these three values inside `nextStep()`.

## Domain Adaptation Checklist

When adapting to a new app, change these in order:

### 1. Step content (3-5 steps recommended)

For each step, decide:

- **Headline** — bold, large, transformation-focused. "Welcome to [App]" only works for step 0; later steps should describe a capability.
- **Subheadline** — one line of supporting copy at 0.8 opacity.
- **Visual** — either a hero illustration or a custom animation view (see "Custom animations" below).
- **Bottom social-proof line** — small caption with an SF Symbol icon and a trust statement ("Trusted by N+", "Over N analyses", etc.).

The reference uses **3 steps** because it's the sweet spot — enough to tell a story, not so much that users bail. Resist going past 5.

### 2. Hero imagery (`hero-header`, `hero-footer`)

Two PNG assets at the top and bottom of the screen, full-bleed, ignoring safe area. The header runs ~30-40% of the screen height; the footer is at 0.5 opacity for atmospheric effect.

Aspect ratios: design for the longest iPhone (iPhone 6.9" is 1320 × 2868pt). Header should be ~1320 × 900px, footer ~1320 × 600px. Both should fade gracefully into the dark background — design with transparent edges or radial fade.

If the user doesn't have hero images yet:

- Suggest generating them via `nano-banana:generate` (the `nano-banana` plugin's Pro model gives photorealistic results at 4K) with prompts like "cinematic dark photograph of [domain subject], dramatic lighting, fades to black at edges, no text"
- Or use SF Symbols + `LinearGradient` as a placeholder. Mark with TODO so the user replaces them.

### 3. Progress dots

The reference uses 3 SF Symbols (`ladybug.fill`, `camera.fill`, `sparkles`) that match the app's domain. For a new app:

- Pick SF Symbols that semantically map to each step's content
- Keep the icon family consistent (all `.fill` variants, or all outlined)
- Active state: full red circle, 1.2× scale, full opacity. Inactive: white at 0.3 opacity, 0.8× scale, 0.5 icon opacity.

### 4. Accent colour

The reference uses `Color.red` everywhere — buttons, progress dots, social-proof icons. Replace with the app's accent colour. Define it once in `OnboardingTheme` rather than scattering it:

```swift
enum OnboardingTheme {
    static let accent = Color("OnboardingAccent")  // declare in Assets.xcassets
    static let accentText = Color.white
}
```

### 5. Testimonials

`OnboardingTestimonialView` rotates through `[OnboardingTestimonial]` with auto-advance every 3.4s. Wire it from a parent `@State` array:

```swift
let testimonials = [
    OnboardingTestimonial(id: 1, title: "Such a good app",
                          description: "Has changed how I work, can't go back."),
    OnboardingTestimonial(id: 2, title: "Super useful",
                          description: "Quick, reliable, and the support is brilliant."),
]
```

Avatar images should be `avatar-1`, `avatar-2`, etc. in `Assets.xcassets`. If the user doesn't have real testimonials yet, write aspirational ones that reflect the transformation the app delivers — and mark them with a `// TODO: replace with real reviews` comment.

### 6. Custom animations

The reference has two domain-specific animation views:

- **`CustomAnimationFishPhotoView`** — three-frame "snap a photo to identify" sequence (frames 1, 2, 3 cross-fade)
- **`CustomAnimationDigitalSharkView`** — binary text scrolling behind a hero image (matrix-style "AI is processing" feel)

For a new app, keep the _pattern_ but change the _content_:

- Multi-frame illustrations cross-fading = good for any "do X to get Y" story
- Scrolling text/code behind imagery = good for any AI / data / processing story
- Rotating elements with continuous loop = good for any active-process story

Or replace with a Lottie animation if you have one. Lottie integrates cleanly via `LottieView` from the `lottie-ios` package.

## Modernisation Notes (iOS 17+)

The reference was written for iOS 16 and uses `DispatchQueue.main.asyncAfter` everywhere. On iOS 17+ codebases, replace these with structured concurrency:

```swift
// Old (reference)
DispatchQueue.main.asyncAfter(deadline: .now() + 0.5) {
    step += 1
    withAnimation(.easeInOut(duration: 0.5)) {
        onboardingOpacity = 1
    }
}

// Modern (iOS 17+)
Task {
    try? await Task.sleep(for: .milliseconds(500))
    withAnimation(.easeInOut(duration: 0.5)) {
        step += 1
        onboardingOpacity = 1
    }
}
```

Other modernisations:

- `withAnimation(_:_:)` with the `completion:` overload (iOS 17+) replaces the chained `asyncAfter` pattern entirely:
  ```swift
  withAnimation(.easeInOut(duration: 0.5)) {
      onboardingOpacity = 0
  } completion: {
      step += 1
      withAnimation(.easeInOut(duration: 0.5)) {
          onboardingOpacity = 1
      }
  }
  ```
- `@Observable` macro (iOS 17+) is cleaner than `@StateObject` if the onboarding has more state than fits in a simple struct.
- `.symbolEffect(.pulse)` and `.symbolEffect(.bounce)` (iOS 17+) can replace some custom progress-bar animations.

If targeting iOS 16, leave the `DispatchQueue.main.asyncAfter` pattern as in the reference.

## Integration with the App

Use `@AppStorage` to track first-launch and gate the onboarding sheet:

```swift
struct ContentView: View {
    @AppStorage("hasCompletedOnboarding") private var hasCompletedOnboarding = false
    @State private var showOnboarding = false

    var body: some View {
        MainAppView()
            .fullScreenCover(isPresented: $showOnboarding) {
                OnboardingCinematicView(isPresented: $showOnboarding)
                    .onDisappear { hasCompletedOnboarding = true }
            }
            .onAppear {
                if !hasCompletedOnboarding {
                    showOnboarding = true
                }
            }
    }
}
```

To re-trigger onboarding for testing: reset the simulator (Device → Erase All Content), or temporarily add `hasCompletedOnboarding = false` in a debug build.

The reference's `nextStep()` flips `isPresented = false` after a 1-second delay on the final step. Keep that — the dismiss animation feels deliberate rather than abrupt.

## Animation Timing Reference

The reference uses these durations consistently:

| What                                       | Duration                    | Curve                  |
| ------------------------------------------ | --------------------------- | ---------------------- |
| Content opacity fade out                   | 0.5s                        | `.easeInOut`           |
| Progress bar advance                       | 1.0s                        | `.easeInOut`           |
| Content opacity fade in                    | 0.5s                        | `.easeInOut`           |
| Step transition total                      | 1.5s                        |                        |
| Testimonial reveal (scale + blur + rotate) | implicit `.default` (0.35s) |                        |
| Testimonial visible duration               | 3.4s                        | static delay           |
| Testimonial fade out                       | 0.4s                        | `.easeInOut` (implied) |
| Hand-photo animation full loop             | ~5s                         | mixed                  |
| Binary-text scroll                         | 10.6s                       | `.linear`              |

Don't shortcut these — the slow timing is what makes it feel cinematic. If steps feel too slow during development, leave them; users see this once.

## Accessibility

The reference doesn't include accessibility wiring. When productionising, add:

```swift
.accessibilityElement(children: .combine)
.accessibilityLabel("Welcome to [App Name]")
.accessibilityHint("Step 1 of 3")
.accessibilityAddTraits(.isHeader)  // for the headline Text
```

For the auto-rotating testimonial, mark it `accessibilityElement(children: .ignore)` and provide a single combined label, or it'll fight with VoiceOver as it rotates.

For the continue button:

```swift
.accessibilityLabel("Continue")
.accessibilityHint("Advance to step \(step + 2) of 3")
```

For users with reduced motion preferences, gate animations:

```swift
@Environment(\.accessibilityReduceMotion) var reduceMotion
// then:
withAnimation(reduceMotion ? .none : .easeInOut(duration: 0.5)) { ... }
```

## Required Assets

Before shipping, ensure these are in `Assets.xcassets`:

- `hero-header` — top hero image
- `hero-footer` — bottom hero image (renders at 0.5 opacity)
- `award-leaves` — laurel leaves around the testimonial avatar (the reference includes one, mirrored on the right side)
- `avatar-1`, `avatar-2`, ... — one per testimonial entry, square crop
- Step-specific illustrations matching the custom animation views

If the app is dark-mode only (the reference uses `.preferredColorScheme(.dark)`), all assets should be designed for a black background. If the user wants light mode support, plan light/dark variants in the asset catalog.

## Common Pitfalls

| Mistake                                                                                                              | Fix                                                                                                                                                                      |
| -------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Skipping the `animatedStep` separation — using `step` directly for progress bar                                      | Keep two separate state vars; the progress bar binds to `animatedStep` which advances _during_ the fade, while content reads from `step` which advances _after_ the fade |
| Forgetting `.ignoresSafeArea()` on `OnboardingHeaderView`                                                            | Hero images won't bleed to the screen edges; whole effect breaks                                                                                                         |
| Using `Color.black` background instead of relying on `.preferredColorScheme(.dark)`                                  | Inconsistent with system dark mode; hero image edges become visible                                                                                                      |
| Locking `Spacer()` height with explicit padding rather than `Spacer().frame(maxHeight: ...)`                         | Layout breaks on iPhone SE / iPad                                                                                                                                        |
| Calling `.shuffle()` on the testimonials inside `body`                                                               | Re-shuffles every render; do it in `.onAppear`                                                                                                                           |
| Hardcoding asset names in the testimonial view (`Image("avatar-\(testimonial.id)")`) without ensuring sequential IDs | Crashes when an ID has no asset; use `.failureImage` fallback or guard                                                                                                   |

## What to Build

When the user invokes this skill, work through these in order:

1. **Confirm the steps** — what 3-5 things does the user want to communicate? Headline + subheadline + visual concept for each.
2. **Confirm the assets** — does the user have hero images, custom animations, testimonials? What's missing? Offer to generate placeholder hero images via `nano-banana:generate`.
3. **Adapt the file** — start from `references/OnboardingCinematicView-original.swift`, swap the domain content, wire in the user's accent colour, replace the custom animation views with domain-appropriate versions.
4. **Wire integration** — set up `@AppStorage` first-launch detection, the `fullScreenCover` presentation, and any analytics events the user wants on each step.
5. **Modernise if iOS 17+** — convert `DispatchQueue.main.asyncAfter` to `Task` + `Task.sleep`, use `withAnimation(_:completion:)` overload.
6. **Add accessibility** — labels, hints, and `reduceMotion` gating.

## References

- `references/OnboardingCinematicView-original.swift` — full original implementation by Adam Lyttle (3 steps, 585 lines, iOS 16+). The animation timing and structural choices are battle-tested; copy them, swap the content.
- `references/integration-example.swift` — minimal `ContentView` showing `fullScreenCover`-based presentation.
- `LICENSE` — MIT (Adam Lyttle, 2025). Attribution preserved in references.

The reference imagery (insect identifier theme — `onboarding-fish-wireframe`, `onboarding-shark`, `onboarding-hand-animation-1/2/3`, etc.) is **not included** in this skill — those assets are domain-specific. The reference Swift code refers to them by name; replace with your app's equivalents during adaptation.

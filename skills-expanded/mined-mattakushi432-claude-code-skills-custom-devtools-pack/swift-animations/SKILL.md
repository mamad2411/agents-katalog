---
name: swift-animations
description: "When to activate: SwiftUI animations, keyframe animations, phase animations, spring animations, UIKit animations, Core Animation layers"
origin: zakr
metadata:
  namespace: zakr/devtools-pack
  version: 1.0.0
  category: engineering
  language: swift
  platforms: [claude-code, codex, gemini-cli, cursor, aider, windsurf]
---

# Swift Animation Patterns

## SwiftUI Animations

```swift
// Implicit animation — SwiftUI animates any state change
struct PulsingButton: View {
    @State private var isPressed = false

    var body: some View {
        Button("Tap me") { isPressed.toggle() }
            .scaleEffect(isPressed ? 0.95 : 1.0)
            .animation(.spring(response: 0.3, dampingFraction: 0.6), value: isPressed)
    }
}

// Explicit animation — wraps state change
Button("Expand") {
    withAnimation(.easeInOut(duration: 0.3)) {
        isExpanded.toggle()
    }
}
```

## Spring Animations

```swift
// Bouncy spring for interactive elements
.animation(.spring(response: 0.4, dampingFraction: 0.7), value: offset)

// Snappy spring for UI feedback
.animation(.spring(response: 0.2, dampingFraction: 1.0), value: isSelected)

// Gentle spring for cards
.animation(.spring(duration: 0.5, bounce: 0.25), value: isVisible)
```

## Keyframe Animations (iOS 17+)

```swift
struct BounceEffect: View {
    @State private var trigger = false

    var body: some View {
        Image(systemName: "star.fill")
            .keyframeAnimator(initialValue: BounceValues(), trigger: trigger) { view, values in
                view
                    .scaleEffect(values.scale)
                    .rotationEffect(.degrees(values.rotation))
                    .offset(y: values.yOffset)
            } keyframes: { _ in
                KeyframeTrack(\.scale) {
                    SpringKeyframe(1.3, duration: 0.15)
                    SpringKeyframe(0.9, duration: 0.15)
                    SpringKeyframe(1.0, duration: 0.2)
                }
                KeyframeTrack(\.rotation) {
                    LinearKeyframe(0, duration: 0.1)
                    SpringKeyframe(-15, duration: 0.15)
                    SpringKeyframe(15, duration: 0.15)
                    SpringKeyframe(0, duration: 0.1)
                }
                KeyframeTrack(\.yOffset) {
                    SpringKeyframe(-20, duration: 0.2)
                    SpringKeyframe(0, duration: 0.3)
                }
            }
            .onTapGesture { trigger.toggle() }
    }
}

struct BounceValues {
    var scale: Double = 1.0
    var rotation: Double = 0
    var yOffset: Double = 0
}
```

## Phase Animations (iOS 17+)

```swift
struct LoadingDot: View {
    var body: some View {
        HStack {
            ForEach(0..<3) { index in
                Circle()
                    .fill(.blue)
                    .frame(width: 10, height: 10)
                    .phaseAnimator([false, true]) { circle, phase in
                        circle.offset(y: phase ? -8 : 0)
                    } animation: { phase in
                        .easeInOut(duration: 0.4).delay(Double(index) * 0.1).repeatForever()
                    }
            }
        }
    }
}
```

## Transition Animations

```swift
// Built-in transitions
Text("Appears!").transition(.scale.combined(with: .opacity))

// Custom transition
extension AnyTransition {
    static var slideFromBottom: AnyTransition {
        .asymmetric(
            insertion: .move(edge: .bottom).combined(with: .opacity),
            removal: .move(edge: .top).combined(with: .opacity)
        )
    }
}

if isVisible {
    Card().transition(.slideFromBottom)
}
```

## matchedGeometryEffect (Hero Transition)

```swift
@Namespace private var heroNS

// Grid view
ForEach(items) { item in
    Image(item.thumbnail)
        .matchedGeometryEffect(id: item.id, in: heroNS)
        .onTapGesture { withAnimation { selectedItem = item } }
}

// Detail view
if let item = selectedItem {
    Image(item.thumbnail)
        .matchedGeometryEffect(id: item.id, in: heroNS)
}
```

## Core Animation (UIKit)

```swift
// Layer animation
let animation = CABasicAnimation(keyPath: "transform.scale")
animation.fromValue = 1.0
animation.toValue = 1.2
animation.duration = 0.3
animation.autoreverses = true
animation.repeatCount = 3
layer.add(animation, forKey: "pulse")

// Spring layer animation
let spring = CASpringAnimation(keyPath: "position.y")
spring.fromValue = 0
spring.toValue = 100
spring.mass = 1
spring.stiffness = 180
spring.damping = 15
spring.duration = spring.settlingDuration
layer.add(spring, forKey: "bounce")
```

## Accessibility — Reduced Motion

```swift
struct AnimatedView: View {
    @Environment(\.accessibilityReduceMotion) var reduceMotion

    var body: some View {
        content
            .animation(reduceMotion ? .none : .spring(), value: isExpanded)
    }
}

// UIKit
if UIAccessibility.isReduceMotionEnabled {
    view.alpha = isVisible ? 1 : 0  // cross-fade instead of slide
} else {
    // full animation
}
```

## Common Anti-Patterns

- **Animating non-animatable properties** — only `Animatable` protocol conformers animate smoothly
- **Forgetting `value:` in `.animation`** — SwiftUI 3+ requires explicit value binding to avoid over-animation
- **No reduced motion support** — always honor `accessibilityReduceMotion`
- **Animating layout in UIKit** — call `layoutIfNeeded()` inside `UIView.animate` block, not before
- **`CATransaction` without `begin/commit`** — always pair `CATransaction.begin()` with `CATransaction.commit()`

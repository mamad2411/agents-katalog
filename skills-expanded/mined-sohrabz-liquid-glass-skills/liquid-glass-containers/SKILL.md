---
name: liquid-glass-containers
description: >
  Combine, group, and morph multiple Liquid Glass elements in iOS 26 SwiftUI. Covers
  GlassEffectContainer (required whenever you have more than one glass element — glass cannot
  sample other glass), morphing transitions with glassEffectID + a shared @Namespace,
  glassEffectUnion for merging distant elements, and glassEffectTransition
  (.identity / .matchedGeometry / .materialize). Use this skill when the user has two or more
  glass views, wants glass buttons/icons that "blend", "merge", or "morph" into each other, is
  building an expandable/collapsing cluster of glass controls, asks "why does my glass look wrong
  with multiple elements", "how do I animate between glass states", mentions "GlassEffectContainer",
  "glassEffectID", "glassEffectUnion", "matchedGeometry" for glass, or needs fluid transitions
  between glass shapes.
---

# Liquid Glass Containers, Morphing & Unions

The core constraint: **glass cannot sample other glass.** Any time you have more than one glass
element near each other, wrap them in a `GlassEffectContainer`. It provides a shared sampling
region, improves rendering performance, and is what enables morphing between elements. (Prereqs:
see **liquid-glass-foundations** for `.glassEffect()` basics.)

## GlassEffectContainer

```swift
GlassEffectContainer {
    HStack(spacing: 20) {
        Image(systemName: "pencil")
            .frame(width: 44, height: 44)
            .glassEffect(.regular.interactive())
        Image(systemName: "eraser")
            .frame(width: 44, height: 44)
            .glassEffect(.regular.interactive())
    }
}
```

The `spacing:` parameter is the **morphing threshold** — glass elements within this distance
visually blend and morph together during transitions:

```swift
GlassEffectContainer(spacing: 40.0) {
    ForEach(icons) { icon in
        IconView(icon).glassEffect()
    }
}

struct GlassEffectContainer<Content: View>: View {
    init(spacing: CGFloat? = nil, @ViewBuilder content: () -> Content)
    init(@ViewBuilder content: () -> Content)
}
```

## Morphing transitions with glassEffectID

Requirements for morphing:
1. Elements live in the same `GlassEffectContainer`.
2. Each view has a `glassEffectID` sharing one `@Namespace`.
3. Views are conditionally shown/hidden to trigger the morph.
4. The state change is wrapped in `withAnimation`.

```swift
struct MorphingExample: View {
    @State private var isExpanded = false
    @Namespace private var namespace

    var body: some View {
        GlassEffectContainer(spacing: 30) {
            Button(isExpanded ? "Collapse" : "Expand") {
                withAnimation(.bouncy) { isExpanded.toggle() }
            }
            .glassEffect()
            .glassEffectID("toggle", in: namespace)

            if isExpanded {
                Button("Action 1") { }
                    .glassEffect()
                    .glassEffectID("action1", in: namespace)
                Button("Action 2") { }
                    .glassEffect()
                    .glassEffectID("action2", in: namespace)
            }
        }
    }
}

func glassEffectID<ID: Hashable>(_ id: ID, in namespace: Namespace.ID) -> some View
```

**Expandable action menu** — a toggle that's always visible, surrounded by buttons that morph in
and out. Each conditional button gets its own `glassEffectID`; the toggle keeps a stable id:

```swift
struct ActionButtonsView: View {
    @State private var showActions = false
    @Namespace private var namespace

    var body: some View {
        ZStack {
            Image("background").resizable().ignoresSafeArea()

            GlassEffectContainer(spacing: 30) {
                VStack(spacing: 30) {
                    if showActions {
                        actionButton("rotate.right").glassEffectID("rotate", in: namespace)
                    }
                    HStack(spacing: 30) {
                        if showActions {
                            actionButton("circle.lefthalf.filled").glassEffectID("contrast", in: namespace)
                        }
                        actionButton(showActions ? "xmark" : "slider.horizontal.3") {
                            withAnimation(.bouncy) { showActions.toggle() }
                        }
                        .glassEffectID("toggle", in: namespace)
                        if showActions {
                            actionButton("flip.horizontal").glassEffectID("flip", in: namespace)
                        }
                    }
                    if showActions {
                        actionButton("crop").glassEffectID("crop", in: namespace)
                    }
                }
            }
        }
    }

    @ViewBuilder
    func actionButton(_ systemImage: String, action: (() -> Void)? = nil) -> some View {
        Button { action?() } label: {
            Image(systemName: systemImage).frame(width: 44, height: 44)
        }
        .buttonStyle(.glass)
        .buttonBorderShape(.circle)
    }
}
```

## glassEffectUnion — merge distant elements

When elements are too far apart to merge via `spacing` alone, force them into one visual glass
shape. All conditions must hold: same `id`, same glass effect type, similar shapes.

```swift
func glassEffectUnion<ID: Hashable>(id: ID, namespace: Namespace.ID) -> some View

struct UnionExample: View {
    @Namespace var controls
    var body: some View {
        GlassEffectContainer {
            VStack(spacing: 0) {
                Button("Edit") { }
                    .buttonStyle(.glass)
                    .glassEffectUnion(id: "tools", namespace: controls)
                Spacer().frame(height: 100)     // large gap, still unified
                Button("Delete") { }
                    .buttonStyle(.glass)
                    .glassEffectUnion(id: "tools", namespace: controls)
            }
        }
    }
}
```

Use different ids to form subgroups — here the first 3 icons blend, the 4th floats separately:

```swift
GlassEffectContainer {
    ForEach(0..<4) { index in
        Image(systemName: icons[index])
            .frame(width: 70, height: 70)
            .glassEffect()
            .glassEffectUnion(id: index < 3 ? "group1" : "group2", namespace: glassNamespace)
    }
}
```

## glassEffectTransition

Controls how a glass element appears/disappears during a morph.

```swift
func glassEffectTransition(_ transition: GlassEffectTransition, isEnabled: Bool = true) -> some View

enum GlassEffectTransition {
    case identity        // no changes
    case matchedGeometry // matched-geometry transition (default)
    case materialize     // material appearance transition
}

Button("Action") { }
    .glassEffect()
    .glassEffectID("button", in: namespace)
    .glassEffectTransition(.materialize)
```

## Related skills

- Applying glass to standard components (buttons/toolbars/tabs) → **liquid-glass-controls**
- Larger compositions like floating action clusters → **liquid-glass-advanced**
- Performance rationale for always using a container → **liquid-glass-best-practices**

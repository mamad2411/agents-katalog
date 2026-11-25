---
name: liquid-glass-advanced
description: >
  Advanced iOS 26 Liquid Glass composition and integration patterns in SwiftUI: floating action
  clusters / expandable FABs, SF Symbol effects on glass (contentTransition symbolEffect / replace /
  numericText), performance optimization for glass, dynamic color-scheme adaptation to background,
  custom floating glass navigation/sidebars, drag-gesture-driven glass, and CoreText-based custom
  glass text (converting glyphs to a Path used as the glass shape). Use this skill when the user is
  building something beyond a single control — an expanding menu of glass buttons, an animated icon
  that morphs on a glass surface, a draggable glass element, glass that adapts as content scrolls
  light-to-dark, a bespoke floating sidebar, or glass-shaped text. Trigger on "floating action
  button cluster", "expandable FAB", "symbolEffect", "glass performance", "glass adapts to
  background", "draggable glass", "CoreText glass", or "custom glass text".
---

# Advanced Liquid Glass

Composition and integration patterns that go beyond styling a single control. Assumes familiarity
with **liquid-glass-foundations** (variants, `.glassEffect()`) and **liquid-glass-containers**
(`GlassEffectContainer`, `glassEffectID`).

## Floating action cluster (expandable FAB)

An always-visible toggle plus action buttons that morph in and out. Note the container `spacing:`,
per-button `glassEffectID`, and `.bouncy` animation.

```swift
struct FloatingActionCluster: View {
    @State private var isExpanded = false
    @Namespace private var namespace

    let actions = [
        ("home", Color.purple), ("pencil", Color.blue),
        ("message", Color.green), ("envelope", Color.orange)
    ]

    var body: some View {
        ZStack {
            ContentView()
            VStack { Spacer(); HStack { Spacer(); cluster.padding() } }
        }
    }

    var cluster: some View {
        GlassEffectContainer(spacing: 20) {
            VStack(spacing: 12) {
                if isExpanded {
                    ForEach(actions, id: \.0) { action in
                        actionButton(action.0, color: action.1)
                            .glassEffectID(action.0, in: namespace)
                    }
                }
                Button {
                    withAnimation(.bouncy(duration: 0.4)) { isExpanded.toggle() }
                } label: {
                    Image(systemName: isExpanded ? "xmark" : "plus")
                        .font(.title2.bold())
                        .frame(width: 56, height: 56)
                }
                .buttonStyle(.glassProminent)
                .buttonBorderShape(.circle)
                .tint(.blue)
                .glassEffectID("toggle", in: namespace)
            }
        }
    }

    func actionButton(_ icon: String, color: Color) -> some View {
        Button { } label: {
            Image(systemName: icon).font(.title3).frame(width: 48, height: 48)
        }
        .buttonStyle(.glass)
        .buttonBorderShape(.circle)
        .tint(color)
    }
}
```

## SF Symbol effects on glass

Pair `.glassEffect(.regular.interactive())` with `.contentTransition(.symbolEffect(...))` for smooth
icon swaps:

```swift
struct SymbolGlassButton: View {
    @State private var isLiked = false
    var body: some View {
        Button { isLiked.toggle() } label: {
            Image(systemName: isLiked ? "heart.fill" : "heart")
                .font(.title).frame(width: 60, height: 60)
        }
        .glassEffect(.regular.interactive())
        .contentTransition(.symbolEffect(.replace))
        .tint(isLiked ? .red : .primary)
    }
}
```

Available transitions: `.symbolEffect(.replace)`, `.symbolEffect(.automatic)`, `.numericText()`
(for numbers).

## Performance optimization

1. **Always use `GlassEffectContainer` for multiple elements** — shared sampling is far cheaper than
   separate glass effects, and avoids inconsistent sampling.
2. **Toggle with `.identity`, not by adding/removing the modifier** — no layout recalculation:
   `.glassEffect(shouldShowGlass ? .regular : .identity)`.
3. **Limit continuous animations.** Let glass rest in steady states; avoid perpetual rotation/loops.
4. **Test on older devices** (iPhone 11–13 may lag). Profile GPU with Instruments; watch thermals.

## Dynamic adaptation to background

Glass automatically flips light/dark based on the content behind it — no code needed:

```swift
ScrollView {
    Color.black.frame(height: 400)   // glass becomes light
    Color.white.frame(height: 400)   // glass becomes dark
}
.safeAreaInset(edge: .bottom) {
    ControlPanel().glassEffect()     // adapts automatically
}
```

Behaviors: small elements (nav/tab bars) flip; large elements (sidebars/menus) adapt but don't flip
(flipping would be jarring); shadow opacity rises over text and falls over white; tint adjusts
hue/brightness/saturation for legibility.

## Custom floating glass navigation

A hand-rolled floating sidebar with per-row `glassEffectID` and a slide+fade transition:

```swift
struct CustomNavigationView: View {
    @State private var selectedItem: Item?
    @Namespace private var namespace

    var body: some View {
        ZStack(alignment: .leading) {
            DetailView(item: selectedItem)
                .frame(maxWidth: .infinity, maxHeight: .infinity)

            if showSidebar {
                GlassEffectContainer {
                    VStack(alignment: .leading, spacing: 0) {
                        ForEach(items) { item in
                            NavigationButton(item: item, isSelected: item.id == selectedItem?.id) {
                                withAnimation { selectedItem = item }
                            }
                            .glassEffectID(item.id, in: namespace)
                        }
                    }
                    .frame(width: 280)
                    .glassEffect(.regular, in: RoundedRectangle(cornerRadius: 20))
                }
                .padding()
                .transition(.move(edge: .leading).combined(with: .opacity))
            }
        }
    }
}
```

## Gesture integration

```swift
struct DraggableGlassButton: View {
    @State private var offset = CGSize.zero
    @State private var isDragging = false
    var body: some View {
        Button("Drag Me") { }
            .glassEffect(.regular.interactive())
            .offset(offset)
            .scaleEffect(isDragging ? 1.1 : 1.0)
            .gesture(
                DragGesture()
                    .onChanged { value in isDragging = true; offset = value.translation }
                    .onEnded { _ in
                        withAnimation(.spring(response: 0.3, dampingFraction: 0.6)) {
                            isDragging = false; offset = .zero
                        }
                    }
            )
    }
}
```

## Custom glass text (CoreText)

Convert text glyphs to a `Path` and use it as the glass shape (best with `.clear`):

```swift
import CoreText

extension View {
    func glassText(_ text: String, font: UIFont) -> some View {
        let path = createTextPath(text, font: font)
        return self.glassEffect(.clear, in: path)
    }
}

func createTextPath(_ string: String, font: UIFont) -> Path {
    var path = Path()
    let attributed = NSAttributedString(string: string, attributes: [.font: font])
    let line = CTLineCreateWithAttributedString(attributed)
    let runs = CTLineGetGlyphRuns(line) as! [CTRun]
    for run in runs {
        let glyphCount = CTRunGetGlyphCount(run)
        for index in 0..<glyphCount {
            var glyph = CGGlyph()
            CTRunGetGlyphs(run, CFRange(location: index, length: 1), &glyph)
            if let glyphPath = CTFontCreatePathForGlyph(font, glyph, nil) {
                path.addPath(Path(glyphPath))
            }
        }
    }
    return path
}
```

## Related skills

- Battery/thermal numbers & memory notes → **liquid-glass-troubleshooting**
- When advanced effects are worth it vs. plain UI → **liquid-glass-best-practices**

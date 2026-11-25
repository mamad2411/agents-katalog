---
name: swift-accessibility
description: "When to activate: iOS/macOS accessibility, VoiceOver, accessibilityLabel, accessibilityHint, Dynamic Type, high contrast, SwiftUI accessibility modifiers"
origin: zakr
metadata:
  namespace: zakr/devtools-pack
  version: 1.0.0
  category: engineering
  language: swift
  platforms: [claude-code, codex, gemini-cli, cursor, aider, windsurf]
---

# Swift Accessibility Patterns

## SwiftUI Accessibility Modifiers

```swift
struct ArticleCard: View {
    let article: Article
    @State private var isFavorite = false

    var body: some View {
        VStack(alignment: .leading) {
            // Merge child elements into one VoiceOver element
            VStack(alignment: .leading) {
                Text(article.title).font(.headline)
                Text(article.summary).font(.subheadline).foregroundStyle(.secondary)
            }
            .accessibilityElement(children: .combine)
            .accessibilityLabel("\(article.title). \(article.summary)")

            Button {
                isFavorite.toggle()
            } label: {
                Image(systemName: isFavorite ? "heart.fill" : "heart")
            }
            .accessibilityLabel(isFavorite ? "Remove from favorites" : "Add to favorites")
            .accessibilityHint("Double tap to toggle favorite status")
            .accessibilityAddTraits(isFavorite ? .isSelected : [])
        }
    }
}
```

## Dynamic Type

```swift
// Always use dynamic type styles — never hardcode font sizes
Text("Article Title")
    .font(.headline)                      // scales with user font size setting
    .dynamicTypeSize(.small ... .xxxLarge) // clamp if layout breaks at extremes

// Adaptive layout for large text
ViewThatFits(in: .horizontal) {
    HStack { icon; text }  // preferred: side by side
    VStack { icon; text }  // fallback: stacked for large text
}
```

## VoiceOver Custom Actions

```swift
struct SwipeableCard: View {
    let item: Item

    var body: some View {
        CardView(item: item)
            .accessibilityActions {
                Button("Mark as Read") { markRead(item) }
                Button("Archive") { archive(item) }
                Button("Delete", role: .destructive) { delete(item) }
            }
    }
}
```

## Focus Management

```swift
struct LoginView: View {
    @AccessibilityFocusState private var isUsernameFocused: Bool

    var body: some View {
        VStack {
            TextField("Username", text: $username)
                .accessibilityFocused($isUsernameFocused)

            if showError {
                Text("Invalid username")
                    .foregroundStyle(.red)
                    .accessibilityAddTraits(.isStaticText)
            }

            Button("Log In") { login() }
        }
        .onAppear { isUsernameFocused = true }
    }
}
```

## UIKit Accessibility

```swift
// Custom accessible element
class CustomSliderView: UIView {
    var value: Float = 0 {
        didSet { accessibilityValue = "\(Int(value * 100))%" }
    }

    override var accessibilityTraits: UIAccessibilityTraits {
        get { [.adjustable] }
        set { }
    }

    override func accessibilityIncrement() { value = min(1, value + 0.1) }
    override func accessibilityDecrement() { value = max(0, value - 0.1) }
}

// Announce changes to VoiceOver
UIAccessibility.post(notification: .announcement, argument: "Upload complete")

// Screen changed (after modal presentation)
UIAccessibility.post(notification: .screenChanged, argument: firstFocusableElement)
```

## High Contrast and Color Independence

```swift
// Never rely on color alone to convey information
// Bad: red = error, green = success (color-blind users can't tell)
// Good: add icon + label

struct StatusBadge: View {
    let status: Status

    var body: some View {
        Label(status.label, systemImage: status.iconName)
            .foregroundStyle(status.color)  // color as secondary signal only
    }
}

// Check for increased contrast
@Environment(\.colorSchemeContrast) var contrast
if contrast == .increased {
    // Use higher contrast variant
}

// Use adaptive colors
Color("AccentColor")  // defined in Asset Catalog with dark/light/high-contrast variants
```

## Testing Accessibility

```swift
// UI Test with VoiceOver
func testFavoriteButtonAccessibility() {
    let app = XCUIApplication()
    app.launch()

    let favoriteButton = app.buttons["Add to favorites"]
    XCTAssertTrue(favoriteButton.exists)

    favoriteButton.tap()
    XCTAssertTrue(app.buttons["Remove from favorites"].exists)
}

// Check for accessibility audit in Xcode 15+
func testA11yAudit() throws {
    let app = XCUIApplication()
    app.launch()
    try app.performAccessibilityAudit()
}
```

## Accessibility Checklist

- [ ] All interactive elements have `accessibilityLabel`
- [ ] Image-only buttons have descriptive labels (not "button")
- [ ] Custom controls implement `accessibilityTraits` correctly
- [ ] Dynamic Type tested at all sizes (especially xxxLarge)
- [ ] Color is not the only differentiator
- [ ] Reduced motion respected
- [ ] Focus order is logical
- [ ] Error messages announced via `UIAccessibility.post`

## Common Anti-Patterns

- **`Image("icon").accessibilityLabel("icon")`** — describe the purpose, not the visual
- **`accessibilityHidden(true)` on meaningful elements** — only hide decorative elements
- **Hardcoded font sizes** — always use Dynamic Type
- **Layout that breaks at xxxLarge text** — test and use `ViewThatFits`
- **Ignoring `accessibilityAudit`** — run it in CI to catch regressions early

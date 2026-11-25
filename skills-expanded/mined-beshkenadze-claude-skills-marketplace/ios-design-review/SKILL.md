---
name: ios-design-review
description: Review iOS code for Apple HIG compliance. Use when validating SwiftUI/UIKit code, checking accessibility, or auditing iOS design implementation.
version: 1.0.0
---

# iOS Design Review

Validate SwiftUI/UIKit code against Apple Human Interface Guidelines.

## When to Use

- After generating SwiftUI components
- Before submitting iOS code for review
- Auditing existing iOS UI code
- Checking accessibility compliance

## Review Checklist

### 1. Colors & Theming
- [ ] Uses semantic colors (`Color.primary`, `Color(.systemBackground)`)
- [ ] No hardcoded hex colors
- [ ] Works in both Light and Dark mode
- [ ] High contrast mode support

### 2. Typography
- [ ] Uses system fonts (San Francisco)
- [ ] Supports Dynamic Type
- [ ] Proper text styles (`.headline`, `.body`, `.caption`)
- [ ] No fixed font sizes for body text

### 3. Touch Targets
- [ ] Minimum 44×44 points for interactive elements
- [ ] Adequate spacing between tappable items (12-24pt)
- [ ] No gesture conflicts with system gestures

### 4. Accessibility
- [ ] VoiceOver labels on icon-only buttons
- [ ] `accessibilityElement(children: .combine)` for grouped content
- [ ] `accessibilityHidden(true)` for decorative elements
- [ ] Meaningful accessibility hints where needed

### 5. Navigation
- [ ] Tab bar for 2-5 primary destinations (not actions)
- [ ] Navigation titles present
- [ ] Back button behavior correct
- [ ] Modal dismiss patterns (swipe, X button)

### 6. SF Symbols
- [ ] Uses SF Symbols over custom icons where possible
- [ ] Correct rendering mode (monochrome/hierarchical/palette)
- [ ] Symbols scale with Dynamic Type

### 7. Layout
- [ ] Safe area respected
- [ ] Adapts to different screen sizes
- [ ] Proper keyboard avoidance
- [ ] No content clipping

## Review Output Format

```markdown
## HIG Compliance Review

**File:** `Views/SettingsView.swift`

### Issues Found

#### Critical
- Line 45: Touch target too small (32×32pt)
  Fix: Add `.frame(minWidth: 44, minHeight: 44)`

#### Warnings
- Line 23: Hardcoded color `Color(hex: "#FF5733")`
  Fix: Use `Color.accentColor` or semantic color

#### Suggestions
- Line 67: Consider adding accessibilityLabel to icon button

### Summary
- Critical: 1
- Warnings: 1
- Suggestions: 1
- Overall: Needs fixes before shipping
```

## Common Issues

### Color Issues
```swift
// ❌ Problem
Text("Hello").foregroundColor(Color(hex: "#333333"))

// ✅ Fix
Text("Hello").foregroundStyle(.primary)
```

### Touch Target Issues
```swift
// ❌ Problem
Button { } label: {
    Image(systemName: "plus")
}

// ✅ Fix
Button { } label: {
    Image(systemName: "plus")
        .frame(minWidth: 44, minHeight: 44)
}
```

### Accessibility Issues
```swift
// ❌ Problem
Button { delete() } label: {
    Image(systemName: "trash")
}

// ✅ Fix
Button { delete() } label: {
    Image(systemName: "trash")
}
.accessibilityLabel("Delete item")
```

## Usage

```
User: Review this SwiftUI view for HIG compliance
[pastes code]

Claude: [Runs checklist against code]
- Identifies issues by category
- Provides specific line numbers
- Suggests fixes with code examples
```

## Related Skills

- `ios-swiftui-generator` — Generate compliant code
- `ios-hig-reference` — Full HIG reference

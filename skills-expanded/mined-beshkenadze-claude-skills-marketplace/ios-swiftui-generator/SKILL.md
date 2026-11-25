---
name: ios-swiftui-generator
description: Generate SwiftUI components following Apple HIG. Use when creating iOS UI components, building SwiftUI views, or need code scaffolding for iOS interfaces.
version: 1.0.0
---

# iOS SwiftUI Generator

Generate production-ready SwiftUI code following Apple Human Interface Guidelines.

## When to Use

- Creating new SwiftUI views or components
- Building iOS UI from design descriptions
- Need HIG-compliant code scaffolding
- Converting UI concepts to SwiftUI code

## Generation Principles

### Always Follow

1. **Semantic Colors** — Use `Color.primary`, `Color(.systemBackground)`, not hex
2. **SF Symbols** — Prefer system icons over custom assets
3. **Dynamic Type** — Support text scaling with `.font(.body)`
4. **Dark Mode** — All colors must work in both modes
5. **Accessibility** — Include VoiceOver labels, minimum 44pt touch targets

### Code Standards

```swift
// ✅ Good
struct ExpenseCard: View {
    let expense: Expense

    var body: some View {
        HStack {
            Image(systemName: expense.category.icon)
                .foregroundStyle(.secondary)
                .accessibilityHidden(true)

            VStack(alignment: .leading) {
                Text(expense.title)
                    .font(.headline)
                Text(expense.date, style: .date)
                    .font(.subheadline)
                    .foregroundStyle(.secondary)
            }

            Spacer()

            Text(expense.amount, format: .currency(code: "USD"))
                .font(.headline)
        }
        .padding()
        .background(Color(.secondarySystemBackground))
        .clipShape(RoundedRectangle(cornerRadius: 12))
        .accessibilityElement(children: .combine)
        .accessibilityLabel("\(expense.title), \(expense.amount)")
    }
}

// ❌ Bad
struct ExpenseCard: View {
    var body: some View {
        HStack {
            Image("custom-icon")  // Use SF Symbols
            Text("$50.00")
                .foregroundColor(Color(hex: "#333"))  // Use semantic
        }
        .frame(height: 30)  // Too small for touch
    }
}
```

## Component Templates

### Navigation
- Tab Bar (2-5 items)
- Navigation Stack with drill-down
- Modal sheets and full-screen covers
- Search integration

### Forms
- Text fields with validation
- Pickers (date, selection, wheel)
- Toggles and steppers
- Secure fields

### Lists
- Standard list with sections
- Swipe actions
- Pull-to-refresh
- Empty states

### Cards & Containers
- Content cards
- Grouped backgrounds
- Material overlays

## Usage

```
User: Create a settings screen with profile section and preferences

Claude: [Generates SwiftUI code]
- SettingsView with List and sections
- ProfileHeaderView component
- PreferenceRow reusable component
- All using semantic colors and SF Symbols
```

## Output Format

Generated code includes:
1. Main view struct
2. Supporting subviews
3. Preview provider
4. Accessibility labels
5. Usage comments

## Related Skills

- `ios-design-review` — Validate generated code
- `ios-hig-reference` — Design guidelines reference

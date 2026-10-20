---
name: swift-localization
description: "When to activate: Swift localization, String Catalogs, NSLocalizedString, pluralization, date/number formatting, multi-language apps"
origin: zakr
metadata:
  namespace: zakr/devtools-pack
  version: 1.0.0
  category: engineering
  language: swift
  platforms: [claude-code, codex, gemini-cli, cursor, aider, windsurf]
---

# Swift Localization Patterns

## String Catalogs (Xcode 15+)

Xcode 15+ introduces `Localizable.xcstrings` (JSON-based String Catalog) that replaces `.strings` files.

```swift
// String Catalog key: "welcome_message"
// In Localizable.xcstrings (managed by Xcode, not hand-edited)

// Usage in Swift
Text("welcome_message", bundle: .main)
// or
String(localized: "welcome_message")
```

## NSLocalizedString (Legacy)

```swift
// Localizable.strings (en)
// "welcome_title" = "Welcome back, %@!";
// "item_count" = "%d items";

// Usage
let title = String(localized: "welcome_title")
let formatted = String(format: NSLocalizedString("item_count", comment: "Number of items"), items.count)
```

## Modern String Interpolation with Format Specifiers

```swift
// Preferred: use Swift's built-in format styles — no format strings needed
let date = Date.now
Text(date, format: .dateTime.day().month().year())

let amount: Decimal = 1234.56
Text(amount, format: .currency(code: "USD"))

let count = 42
Text(count, format: .number)

// In non-SwiftUI contexts
let formatted = date.formatted(.dateTime.day().month(.wide).year())
let price = amount.formatted(.currency(code: "EUR"))
```

## Pluralization

```swift
// In Localizable.xcstrings, Xcode handles plural rules per locale automatically
// Define plural categories: zero, one, two, few, many, other

// In code
Text("^[\(count) item](inflect: true)")  // automatic pluralization with Morphology framework

// Manual plural formatting
let rule = IntegerFormatStyle<Int>.Percent()
Text("\(count) \(count == 1 ? "item" : "items")")  // simple English fallback
```

## Locale-Aware Formatting

```swift
// Always use format styles — they adapt to the user's locale automatically
struct PriceView: View {
    let price: Decimal
    let currencyCode: String

    var body: some View {
        Text(price, format: .currency(code: currencyCode))
            .environment(\.locale, Locale.current)
    }
}

// Measurement formatting
let distance = Measurement(value: 5.0, unit: UnitLength.kilometers)
Text(distance, format: .measurement(width: .abbreviated))  // "5 km" or "3.1 mi" per locale

// Relative date
Text(pastDate, format: .relative(presentation: .named))  // "2 days ago"
```

## Accessing Localized Resources

```swift
// Localize app name in InfoPlist.strings
// CFBundleDisplayName = "Mon Application";

// Localized images
let image = UIImage(named: "hero", in: .main, compatibleWith: nil)
// Xcode picks localized variant from app bundle automatically

// Runtime locale check
let locale = Locale.current
let isRTL = locale.language.characterDirection == .rightToLeft

// Locale-specific layout
HStack {
    if isRTL {
        Spacer()
        content
    } else {
        content
        Spacer()
    }
}
// Better: use .environment(\.layoutDirection, .rightToLeft) in SwiftUI
```

## Exporting for Translation

```bash
# Export via xcodebuild
xcodebuild -exportLocalizations -localizationPath ./l10n -project MyApp.xcodeproj

# Creates XLIFF files for each locale
# l10n/en.xcloc/Localized Contents/en.xliff
```

## Testing Localization

```swift
// Test specific locale in UI tests
let app = XCUIApplication()
app.launchArguments = ["-AppleLanguages", "(de)", "-AppleLocale", "de_DE"]
app.launch()

// Unit test date formatting
func testDateFormatting() {
    let date = Date(timeIntervalSince1970: 0)
    var calendar = Calendar(identifier: .gregorian)
    calendar.locale = Locale(identifier: "en_US")
    let formatted = date.formatted(.dateTime.locale(Locale(identifier: "en_US")))
    XCTAssertEqual(formatted, "1/1/1970, 12:00 AM")
}
```

## Common Anti-Patterns

- **Hardcoded English strings in UI** — all user-visible strings must go through localization
- **String concatenation for localized text** — word order varies by language; use format specifiers
- **`String(format:)` for currency/dates** — use `FormatStyle` instead; it handles locale automatically
- **Not testing RTL layouts** — Hebrew and Arabic users need mirrored layouts
- **Forgetting plural rules** — languages like Russian have 4 plural forms; use String Catalog pluralization

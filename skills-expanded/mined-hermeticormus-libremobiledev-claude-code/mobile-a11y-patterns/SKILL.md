---
name: mobile-a11y-patterns
description: "Code patterns for mobile accessibility: UIKit and SwiftUI modifiers, Dynamic Type, VoiceOver focus, Compose semantics, TalkBack live regions, 48dp touch targets, Flutter Semantics, and WCAG contrast math. Use when adding screen reader support or fixing accessibility issues in iOS, Android, or Flutter UI."
---

# Mobile A11y Patterns

## iOS Accessibility

### UIKit: Accessible Custom View
```swift
class RatingView: UIView {
    var rating: Int = 0 {
        didSet { accessibilityValue = "\(rating) out of 5 stars" }
    }

    override var accessibilityLabel: String? {
        get { "Product rating" }
        set { }
    }

    override var accessibilityTraits: UIAccessibilityTraits {
        get { [.adjustable] }
        set { }
    }

    // Adjustable trait requires these two methods
    override func accessibilityIncrement() {
        rating = min(5, rating + 1)
        UIAccessibility.post(notification: .announcement, argument: accessibilityValue)
    }

    override func accessibilityDecrement() {
        rating = max(0, rating - 1)
        UIAccessibility.post(notification: .announcement, argument: accessibilityValue)
    }
}
```

### SwiftUI: Accessibility Modifiers
```swift
struct ProductCard: View {
    let product: Product

    var body: some View {
        VStack {
            Image(product.imageName)
                .accessibilityHidden(true) // decorative, name covered by label below

            Text(product.name)
            Text("$\(product.price, specifier: "%.2f")")
            Text(product.rating)
        }
        // Combine children into single accessible element
        .accessibilityElement(children: .combine)
        .accessibilityLabel("\(product.name), \(product.price) dollars")
        .accessibilityHint("Double tap to view details")
        .accessibilityAddTraits(.isButton)
    }
}
```

### SwiftUI: Custom Action
```swift
struct SwipeableRow: View {
    var body: some View {
        HStack { /* row content */ }
            .accessibilityAction(named: "Delete") {
                deleteItem()
            }
            .accessibilityAction(named: "Share") {
                shareItem()
            }
    }
}
```

### Dynamic Type Support (UIKit)
```swift
label.font = UIFontMetrics(forTextStyle: .body)
    .scaledFont(for: UIFont.systemFont(ofSize: 16))
label.adjustsFontForContentSizeCategory = true
```

### VoiceOver Focus Management
```swift
// After modal presentation, move focus to modal title
UIAccessibility.post(notification: .screenChanged, argument: modalTitleLabel)

// After async content loads
UIAccessibility.post(notification: .layoutChanged, argument: firstNewElement)

// Announce without moving focus
UIAccessibility.post(notification: .announcement, argument: "5 new messages loaded")
```

---

## Android Accessibility

### Jetpack Compose: Semantics
```kotlin
// Button with custom semantics
Button(
    onClick = { addToCart() },
    modifier = Modifier.semantics {
        contentDescription = "${product.name}, ${product.price} dollars. Add to cart."
        onClick(label = "Add to cart") { addToCart(); true }
    }
) {
    Text("Add to Cart")
}

// Heading for screen reader navigation
Text(
    text = "Featured Products",
    style = MaterialTheme.typography.h6,
    modifier = Modifier.semantics { heading() }
)

// Custom state description
Switch(
    checked = isEnabled,
    onCheckedChange = { isEnabled = it },
    modifier = Modifier.semantics {
        stateDescription = if (isEnabled) "Notifications on" else "Notifications off"
    }
)
```

### UIKit (XML): contentDescription and labelFor
```xml
<!-- Non-text element -->
<ImageButton
    android:contentDescription="@string/close_button"
    android:minWidth="48dp"
    android:minHeight="48dp" />

<!-- Label associated with input (reads label then field) -->
<TextView
    android:id="@+id/emailLabel"
    android:labelFor="@+id/emailInput"
    android:text="Email address" />

<EditText
    android:id="@+id/emailInput"
    android:hint="" /> <!-- hint redundant when labelFor used -->

<!-- Decorative image -->
<ImageView
    android:importantForAccessibility="no"
    android:contentDescription="" />
```

### Live Region Announcement (Kotlin)
```kotlin
// XML: android:accessibilityLiveRegion="polite"
// Code:
ViewCompat.setAccessibilityLiveRegion(
    statusTextView,
    ViewCompat.ACCESSIBILITY_LIVE_REGION_POLITE // or ASSERTIVE for urgent
)
statusTextView.text = "Upload complete"
```

### Touch Target Minimum (48dp)
```kotlin
// Extend touch target without changing visual size
ViewCompat.setAccessibilityDelegate(smallIcon, object : AccessibilityDelegateCompat() {
    override fun onInitializeAccessibilityNodeInfo(
        host: View, info: AccessibilityNodeInfoCompat
    ) {
        super.onInitializeAccessibilityNodeInfo(host, info)
        val parent = host.parent as View
        // Or use TouchDelegate to extend hit area programmatically
    }
})
```

---

## Flutter Accessibility

### Semantics Widget
```dart
Semantics(
  label: 'Close dialog',
  hint: 'Double tap to close',
  button: true,
  child: GestureDetector(
    onTap: () => Navigator.pop(context),
    child: Icon(Icons.close, semanticLabel: null),
  ),
)
```

### Merge and Exclude Semantics
```dart
// Combine card into single accessible element
MergeSemantics(
  child: Column(
    children: [
      Image.asset('product.png'),
      Text('Product Name'),
      Text('\$29.99'),
    ],
  ),
)

// Decorative element
ExcludeSemantics(
  child: Lottie.asset('background_animation.json'),
)
```

### Live Announcement
```dart
SemanticsService.announce(
  'Cart updated. 3 items.',
  TextDirection.ltr,
);
```

### Detect Accessibility Mode
```dart
final mediaQuery = MediaQuery.of(context);

if (mediaQuery.accessibleNavigation) {
  // User is navigating with accessibility features
  // Avoid complex gestures, prefer simple tap targets
}

if (mediaQuery.disableAnimations) {
  // Reduce Motion is enabled — skip transitions
}
```

---

## WCAG 2.1 Contrast Calculation

### Relative Luminance Formula
```
L = 0.2126 * R + 0.7152 * G + 0.0722 * B
where each channel: c <= 0.04045 ? c/12.92 : ((c+0.055)/1.055)^2.4

Contrast Ratio = (L1 + 0.05) / (L2 + 0.05)  where L1 > L2
```

### Requirements
- Normal text (< 18pt or < 14pt bold): 4.5:1 minimum
- Large text (>= 18pt or >= 14pt bold): 3:1 minimum
- UI components, icons, borders: 3:1 against adjacent color (WCAG 1.4.11)
- Focus indicators: 3:1 against unfocused state

### Touch Target Sizing
| Platform | Minimum | Recommended |
|----------|---------|-------------|
| iOS | 44x44pt | 44x44pt or larger |
| Android | 48x48dp | 48x48dp or larger |
| Flutter | 48x48dp (Material) | match platform |

Add transparent padding when visual size must remain small:
```swift
// iOS: extend hit area via touchAreaInsets
override func point(inside point: CGPoint, with event: UIEvent?) -> Bool {
    let expandedBounds = bounds.insetBy(dx: -10, dy: -10)
    return expandedBounds.contains(point)
}
```

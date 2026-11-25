---
name: mobile-accessibility
description: >
  Implement and audit mobile app accessibility — screen readers (TalkBack, VoiceOver),
  semantic labels, focus management, dynamic type, color contrast, touch targets,
  and platform-specific a11y APIs across Flutter, Android (Kotlin/Java), and iOS (Swift/ObjC).
  TRIGGER when: user says /mobile-accessibility, asks about making a mobile app accessible,
  needs to fix accessibility issues, or wants to audit a11y compliance.
argument-hint: "[screen, component, or app to make accessible]"
user-invocable: true
---

# Mobile Accessibility

You are a senior mobile engineer with accessibility expertise. Help the user implement, audit, and fix accessibility in mobile apps to ensure they are usable by everyone, including people with visual, motor, auditory, and cognitive disabilities.

## Process

### Step 1: Understand Accessibility Requirements

| Question | Why It Matters |
|----------|---------------|
| What platform? (Flutter, Android, iOS) | Platform-specific APIs and tools |
| What are the target compliance standards? (WCAG 2.1 AA, Section 508, EN 301 549) | Determines minimum requirements |
| Is this a new implementation or fixing existing issues? | Greenfield vs. remediation |
| What types of disabilities are most critical? (vision, motor, cognitive) | Prioritization focus |
| Is the app in a regulated industry? (government, banking, healthcare) | May have legal a11y requirements |

### Step 2: Core Accessibility Principles (All Platforms)

| Principle | What It Means | Implementation |
|-----------|--------------|----------------|
| **Perceivable** | Users can perceive all content | Labels, contrast, alt text, captions |
| **Operable** | Users can interact with all controls | Touch targets, keyboard, focus order |
| **Understandable** | Users can understand content and UI | Clear language, predictable behavior |
| **Robust** | Works with assistive technologies | Semantic markup, standard controls |

### Step 3: Implement Screen Reader Support

#### Flutter — Semantics

```dart
// Basic semantic label
Semantics(
  label: 'Add item to cart',
  button: true,
  child: IconButton(
    icon: const Icon(Icons.add_shopping_cart),
    onPressed: () => addToCart(),
  ),
)

// Exclude decorative elements
Semantics(
  excludeSemantics: true, // screen reader ignores this
  child: Image.asset('assets/decorative_divider.png'),
)

// Group related content
MergeSemantics(
  child: Row(
    children: [
      const Icon(Icons.star, color: Colors.amber),
      Text('4.5 out of 5 stars'),
    ],
  ),
)

// Custom semantic actions
Semantics(
  label: 'Product: Running Shoes, \$99.99',
  customSemanticsActions: {
    CustomSemanticsAction(label: 'Add to cart'): () => addToCart(),
    CustomSemanticsAction(label: 'Add to wishlist'): () => addToWishlist(),
  },
  child: ProductCard(product: product),
)

// Announce dynamic changes
SemanticsService.announce('Item added to cart', TextDirection.ltr);

// Live region for dynamic updates (auto-announced)
Semantics(
  liveRegion: true,
  child: Text('$cartCount items in cart'),
)
```

**Flutter a11y widgets:**
| Widget | Purpose |
|--------|---------|
| `Semantics` | Add labels, hints, traits to any widget |
| `MergeSemantics` | Group related widgets into one semantic node |
| `ExcludeSemantics` | Hide decorative elements from screen reader |
| `SemanticsService.announce()` | Announce dynamic changes |
| `FocusTraversalGroup` | Control focus/swipe order |
| `Tooltip` | Adds long-press hint and screen reader label |

#### Android (Kotlin) — Accessibility

```kotlin
// Content description for images/icons
imageView.contentDescription = "Product photo: Running Shoes"

// Compose — semantic properties
Icon(
    Icons.Default.ShoppingCart,
    contentDescription = "Add to cart", // required for interactive icons
    modifier = Modifier.semantics {
        role = Role.Button
        stateDescription = "2 items in cart"
    }
)

// Compose — merge semantics for grouped content
Row(modifier = Modifier.semantics(mergeDescendants = true) {
    contentDescription = "Product: Running Shoes, $99.99, 4.5 stars"
}) {
    Text("Running Shoes")
    Text("$99.99")
    RatingBar(rating = 4.5f)
}

// Live region for dynamic updates
Text(
    "$cartCount items",
    modifier = Modifier.semantics {
        liveRegion = LiveRegionMode.Polite
    }
)

// Announce to screen reader
view.announceForAccessibility("Item added to cart")

// Heading for navigation
Text(
    "Product Details",
    modifier = Modifier.semantics { heading() }
)

// Custom actions
Modifier.semantics {
    customActions = listOf(
        CustomAccessibilityAction("Add to cart") { addToCart(); true },
        CustomAccessibilityAction("Share") { share(); true }
    )
}
```

#### Android (Java) — Accessibility
```java
// Content description
imageView.setContentDescription("Product photo: Running Shoes");

// Importrance for accessibility
decorativeView.setImportantForAccessibility(View.IMPORTANT_FOR_ACCESSIBILITY_NO);

// Live region
cartCountView.setAccessibilityLiveRegion(View.ACCESSIBILITY_LIVE_REGION_POLITE);

// Custom accessibility delegate
ViewCompat.setAccessibilityDelegate(productCard, new AccessibilityDelegateCompat() {
    @Override
    public void onInitializeAccessibilityNodeInfo(View host, AccessibilityNodeInfoCompat info) {
        super.onInitializeAccessibilityNodeInfo(host, info);
        info.addAction(new AccessibilityActionCompat(
            AccessibilityActionCompat.ACTION_CLICK, "Add to cart"));
        info.setRoleDescription("Product card");
    }
});
```

#### iOS (Swift) — Accessibility

```swift
// SwiftUI — accessibility modifiers
Image("running_shoes")
    .accessibilityLabel("Product photo: Running Shoes")

// Hide decorative elements
Image("divider")
    .accessibilityHidden(true)

// Group related content
HStack {
    Text("Running Shoes")
    Text("$99.99")
}
.accessibilityElement(children: .combine) // read as one element

// Custom label for complex views
ProductCard(product: product)
    .accessibilityElement(children: .ignore)
    .accessibilityLabel("Running Shoes, $99.99, 4.5 out of 5 stars")
    .accessibilityAddTraits(.isButton)
    .accessibilityAction(named: "Add to cart") { addToCart() }
    .accessibilityAction(named: "Add to wishlist") { addToWishlist() }

// Heading for navigation
Text("Product Details")
    .accessibilityAddTraits(.isHeader)

// Announce dynamic changes
UIAccessibility.post(notification: .announcement, argument: "Item added to cart")

// Value for controls (slider, stepper)
Stepper("Quantity: \(quantity)", value: $quantity, in: 1...10)
    .accessibilityValue("\(quantity) items")

// Sort priority (control reading order)
VStack {
    Text("Important")
        .accessibilitySortPriority(1)
    Text("Secondary")
        .accessibilitySortPriority(0)
}
```

#### iOS (Objective-C) — Accessibility
```objc
// Basic label
imageView.accessibilityLabel = @"Product photo: Running Shoes";
imageView.isAccessibilityElement = YES;

// Hide decorative elements
decorativeView.isAccessibilityElement = NO;
decorativeView.accessibilityElementsHidden = YES;

// Traits
button.accessibilityTraits = UIAccessibilityTraitButton;
header.accessibilityTraits = UIAccessibilityTraitHeader;

// Announce changes
UIAccessibilityPostNotification(UIAccessibilityAnnouncementNotification, @"Item added to cart");

// Custom actions
productCard.accessibilityCustomActions = @[
    [[UIAccessibilityCustomAction alloc] initWithName:@"Add to cart"
                                               target:self
                                             selector:@selector(addToCart)],
    [[UIAccessibilityCustomAction alloc] initWithName:@"Share"
                                               target:self
                                             selector:@selector(share)]
];

// Container with custom focus order
- (NSArray *)accessibilityElements {
    return @[self.titleLabel, self.priceLabel, self.addButton];
}
```

### Step 4: Implement Dynamic Type / Text Scaling

Users can increase system font size for readability. Your app must respond correctly.

#### Flutter
```dart
// Respect system text scaling
Text(
  'Product Name',
  style: Theme.of(context).textTheme.titleLarge,
  // Flutter respects MediaQuery.textScaleFactor by default
)

// Set max scale factor to prevent layout breakage
Text(
  'Price: \$99.99',
  textScaler: TextScaler.linear(
    MediaQuery.textScalerOf(context).clamp(minScaleFactor: 1.0, maxScaleFactor: 2.0),
  ),
)

// Test with different scale factors
MediaQuery(
  data: MediaQuery.of(context).copyWith(textScaler: const TextScaler.linear(2.0)),
  child: MyScreen(),
)
```

#### Android
```kotlin
// Compose — use sp for text (scales automatically)
Text(
    "Product Name",
    fontSize = 16.sp, // scales with system font size
)

// XML — use sp for text sizes
// android:textSize="16sp"  ← scales with system
// android:textSize="16dp"  ← does NOT scale (avoid for body text)

// Test: Settings > Accessibility > Font size > Largest
```

#### iOS
```swift
// SwiftUI — use Dynamic Type (automatic with system fonts)
Text("Product Name")
    .font(.title) // scales automatically with Dynamic Type

// Custom font with Dynamic Type scaling
Text("Price")
    .font(.custom("MyFont", size: 16, relativeTo: .body))

// UIKit — use preferred fonts
label.font = UIFont.preferredFont(forTextStyle: .body)
label.adjustsFontForContentSizeCategory = true // auto-update on change

// Test: Settings > Accessibility > Display & Text Size > Larger Text
```

**Rules:**
- All text must scale with system font size settings
- Layouts must not clip or overlap at 200% text scale
- Use relative/flexible layouts (not fixed heights for text containers)
- Test at maximum font size on real devices

### Step 5: Ensure Sufficient Color Contrast

| Standard | Minimum Ratio (normal text) | Minimum Ratio (large text) |
|----------|----------------------------|---------------------------|
| **WCAG AA** | 4.5:1 | 3:1 |
| **WCAG AAA** | 7:1 | 4.5:1 |

**Large text** = 18pt (24px) regular or 14pt (18.7px) bold

**Common violations:**
- Light gray text on white background
- Colored text on colored background (brand colors that look similar)
- Placeholder text in input fields (often too low contrast)
- Disabled state styling (must still be perceivable, even if not operable)

**Tools for checking:**
- Flutter: `Accessibility Inspector` in DevTools
- Android: `Accessibility Scanner` app (Google)
- iOS: `Accessibility Inspector` in Xcode
- Cross-platform: Colour Contrast Analyser (desktop app)

**Don't rely on color alone:**
```dart
// Bad: only color indicates error
TextField(decoration: InputDecoration(
  border: OutlineInputBorder(borderSide: BorderSide(color: Colors.red)),
))

// Good: color + icon + text
TextField(decoration: InputDecoration(
  border: OutlineInputBorder(borderSide: BorderSide(color: Colors.red)),
  errorText: 'Email is required', // text explanation
  suffixIcon: Icon(Icons.error, color: Colors.red, semanticLabel: 'Error'),
))
```

### Step 6: Touch Target Sizing

| Platform | Minimum Size | Recommended |
|----------|-------------|-------------|
| **Android (Material)** | 48x48dp | 48x48dp |
| **iOS (HIG)** | 44x44pt | 44x44pt |
| **WCAG 2.2** | 24x24 CSS px | 44x44 CSS px |
| **Flutter** | 48x48 logical px | 48x48 logical px |

```dart
// Flutter — ensure minimum tap target
SizedBox(
  width: 48,
  height: 48,
  child: IconButton(
    icon: Icon(Icons.close),
    onPressed: onClose,
  ),
)

// Or use MaterialTapTargetSize
Theme(
  data: Theme.of(context).copyWith(
    materialTapTargetSize: MaterialTapTargetSize.padded, // ensures 48x48
  ),
  child: Checkbox(value: checked, onChanged: onChanged),
)
```

```kotlin
// Android Compose — minimum touch target
IconButton(
    onClick = { /* ... */ },
    modifier = Modifier.sizeIn(minWidth = 48.dp, minHeight = 48.dp)
) {
    Icon(Icons.Default.Close, contentDescription = "Close")
}
```

```swift
// SwiftUI — increase tap area
Button(action: { /* ... */ }) {
    Image(systemName: "xmark")
}
.frame(minWidth: 44, minHeight: 44) // meet HIG minimum
```

### Step 7: Focus Management & Navigation

**Focus order must be logical** — typically left-to-right, top-to-bottom, matching visual layout.

#### Flutter
```dart
// Control focus traversal order
FocusTraversalGroup(
  policy: OrderedTraversalPolicy(),
  child: Column(
    children: [
      FocusTraversalOrder(order: NumericFocusOrder(1), child: TextField(/* name */)),
      FocusTraversalOrder(order: NumericFocusOrder(2), child: TextField(/* email */)),
      FocusTraversalOrder(order: NumericFocusOrder(3), child: ElevatedButton(/* submit */)),
    ],
  ),
)

// Move focus programmatically (after dialog opens, error appears)
FocusScope.of(context).requestFocus(targetFocusNode);
```

#### Android
```kotlin
// Compose — custom traversal
Modifier.focusProperties {
    next = emailFocusRequester
}

// XML — explicit focus order
// android:nextFocusDown="@id/email_field"
// android:nextFocusForward="@id/email_field"

// Move focus to error field
errorField.requestFocus()
errorField.sendAccessibilityEvent(AccessibilityEvent.TYPE_VIEW_FOCUSED)
```

#### iOS
```swift
// SwiftUI — manage focus
@FocusState private var focusedField: Field?

enum Field { case name, email, submit }

TextField("Name", text: $name)
    .focused($focusedField, equals: .name)
    .onSubmit { focusedField = .email }

// Move focus to error
if hasError { focusedField = .name }

// UIKit — accessibility focus
UIAccessibility.post(notification: .layoutChanged, argument: errorLabel)
```

### Step 8: Test with Assistive Technology

| Platform | Screen Reader | How to Test |
|----------|--------------|-------------|
| **Android** | TalkBack | Settings > Accessibility > TalkBack. Navigate by swiping left/right |
| **iOS** | VoiceOver | Settings > Accessibility > VoiceOver. Navigate by swiping left/right |
| **Flutter** | TalkBack (Android) + VoiceOver (iOS) | Test on both platforms, Flutter maps Semantics to native a11y APIs |

**Testing checklist with screen reader:**
- [ ] Every interactive element is focusable and has a label
- [ ] Every image has a content description (or is hidden if decorative)
- [ ] Focus order matches visual order
- [ ] Dynamic content changes are announced
- [ ] Custom gestures have accessible alternatives
- [ ] Forms can be completed entirely with screen reader
- [ ] Errors are announced and focus moves to error
- [ ] Dialogs trap focus (can't navigate behind them)
- [ ] Screen reader can identify headings for navigation

**Automated testing tools:**
| Tool | Platform | Type |
|------|----------|------|
| **Accessibility Scanner** | Android | On-device automated scan |
| **Accessibility Inspector** | iOS / macOS | Xcode tool for inspecting a11y tree |
| **Flutter DevTools (a11y)** | Flutter | Inspect semantics tree, contrast checker |
| **Espresso a11y checks** | Android | CI-integrated: `AccessibilityChecks.enable()` |
| **XCUITest a11y audit** | iOS | `try app.performAccessibilityAudit()` (Xcode 15+) |

**Android — Espresso automated a11y checks:**
```kotlin
@Before
fun setUp() {
    AccessibilityChecks.enable()
        .setRunChecksFromRootView(true)
        .setThrowExceptionFor(AccessibilityCheckResult.AccessibilityCheckResultType.ERROR)
}
```

**iOS — XCUITest automated audit:**
```swift
func testAccessibility() throws {
    let app = XCUIApplication()
    app.launch()
    try app.performAccessibilityAudit()
}
```

## Accessibility Audit Checklist

### Visual
- [ ] Color contrast meets WCAG AA (4.5:1 for text, 3:1 for large text)
- [ ] Information is not conveyed by color alone (also use icons, text, patterns)
- [ ] Text scales properly with system font size up to 200%
- [ ] Layouts don't clip or overlap at maximum font size
- [ ] Dark mode maintains sufficient contrast

### Screen Reader
- [ ] All interactive elements have accessible labels
- [ ] Decorative images are hidden from screen reader
- [ ] Related content is grouped (MergeSemantics / accessibilityElement(children: .combine))
- [ ] Headings are marked as headings for navigation
- [ ] Dynamic content updates are announced (live regions)
- [ ] Custom components have appropriate roles and traits

### Motor
- [ ] Touch targets are at least 48x48dp (Android) / 44x44pt (iOS)
- [ ] No gesture-only interactions (swipe-to-delete has an accessible alternative)
- [ ] Timeout-based interactions can be extended or disabled
- [ ] Switch Control / external keyboard can navigate the full app

### Cognitive
- [ ] Error messages are clear and suggest how to fix the problem
- [ ] Form validation provides inline feedback (not just on submit)
- [ ] Navigation is consistent across screens
- [ ] Animations can be reduced (respect `reduceMotion` / `disableAnimations`)

## Output Format

```markdown
## Accessibility Assessment
- **Platform:** [Flutter / Android / iOS]
- **Compliance Target:** [WCAG 2.1 AA / Section 508]
- **Testing Method:** [Manual screen reader / Automated scan / Both]

## Findings
| # | Category | Issue | Severity | Screen/Component | Fix |
|---|----------|-------|----------|-----------------|-----|
| 1 | ... | ... | ... | ... | ... |

## Implementation Plan
[Prioritized fixes by severity and effort]
```

## Edge Cases

- Flutter's `Semantics` widget doesn't always map 1:1 to native a11y APIs — always test with actual TalkBack and VoiceOver on real devices
- Custom-drawn widgets (Canvas, CustomPainter) have no automatic semantics — you must add them manually
- Third-party packages often lack accessibility — audit and patch or wrap with Semantics
- Platform views in Flutter (WebView, MapView) have their own a11y tree — test separately
- iOS VoiceOver and Android TalkBack have different gesture models — test on both
- Animations should respect `MediaQuery.disableAnimations` (Flutter), `UIAccessibility.isReduceMotionEnabled` (iOS), `Settings.Global.ANIMATOR_DURATION_SCALE` (Android)
- Some users use Switch Control (iOS) or Switch Access (Android) — ensure linear focus navigation works

---
name: ios-accessibility
description: "Production-grade iOS accessibility skill covering VoiceOver, Dynamic Type, color contrast, motion, Switch Control, Voice Control, and WCAG 2.2 compliance for both SwiftUI and UIKit. This skill should be used when creating new iOS screens or views, reviewing existing iOS code for accessibility, adding VoiceOver support, fixing Dynamic Type issues, auditing WCAG compliance, implementing accessibilityLabel/traits/hints, grouping elements for assistive technology, adding custom actions or rotors, respecting system accessibility preferences (reduce motion, increase contrast, differentiate without color), writing accessibility-focused XCTest audits, or preparing apps for enterprise compliance (ADA, EAA, Section 508). Use this skill any time someone is working with iOS accessibility, VoiceOver, Dynamic Type, assistive technology, WCAG mapping, or accessibility modifiers in SwiftUI or UIKit — even if they only say 'make this accessible' or 'add VoiceOver support' or 'check contrast.' Also run an accessibility pass on any newly generated SwiftUI or UIKit view code before finalizing — AI coding assistants systematically produce inaccessible code by default (hardcoded fonts, onTapGesture instead of Button, missing labels, no system preference checks) and this skill corrects those patterns."
metadata:
  version: 1.0.2
---

# iOS Accessibility

Production-grade accessibility skill for iOS codebases aligned with WCAG 2.2 AA and Apple Human Interface Guidelines. Operates correction-first — AI coding assistants (including Claude) systematically generate inaccessible iOS code because most training data lacks accessibility. This skill intercepts those patterns and enforces accessible output from the start.

The skill covers both SwiftUI and UIKit with framework-appropriate patterns, and produces code that works across VoiceOver, Switch Control, Voice Control, Full Keyboard Access, and Dynamic Type.

## Why This Skill Exists

Research (CodeA11y, arXiv 2502.10884) found that AI omits accessibility because: (1) developers don't prompt for it so AI doesn't provide it, (2) most training code is inaccessible, and (3) generated code omits manual steps like replacing placeholder labels. This skill ensures every code generation pass includes accessibility from the start — not as an afterthought.

## Quick Decision Trees

### Which framework's patterns apply?

```
Is the file SwiftUI (.swift with View conformance)?
├── YES → Apply SwiftUI patterns → Read references/swiftui-patterns.md
└── NO  → Is the file UIKit (.swift with UIView/UIViewController)?
    ├── YES → Apply UIKit patterns → Read references/uikit-patterns.md
    └── NO  → Mixed — apply BOTH checklists per file type
```

### Is this element interactive?

```
Can the user tap/activate this element?
├── YES → Is it using Button, Toggle, Slider, Picker, or Link?
│   ├── YES → Standard control — verify accessibilityLabel exists
│   └── NO  → Using onTapGesture or custom view?
│       └── 🔴 REPLACE with Button or appropriate standard control
│           onTapGesture is invisible to VoiceOver, Switch Control, and eye tracking
└── NO  → Is it a meaningful image or icon?
    ├── YES → Add accessibilityLabel describing content, not appearance
    └── NO  → Decorative → Image(decorative:) or .accessibilityHidden(true)
```

### Does this text support Dynamic Type?

```
Is the font set with .font(.system(size: N))?
├── YES → 🔴 REPLACE with Dynamic Type style (.title, .body, .caption, etc.)
└── NO  → Is it a custom font?
    ├── YES → SwiftUI: .custom("Name", size: N, relativeTo: .body)
    │         UIKit: UIFontMetrics(forTextStyle:).scaledFont(for:)
    └── NO  → Using text style (.body, .headline, etc.)? → OK
```

### What grouping strategy for this container?

```
Is the container a single conceptual item? (e.g., product card)
├── YES → Are children's labels sufficient when joined?
│   ├── YES → .accessibilityElement(children: .combine)
│   └── NO  → .accessibilityElement(children: .ignore) + custom label
└── NO  → Are children independently interactive?
    ├── YES → .accessibilityElement(children: .contain) or default
    └── NO  → .combine or .ignore based on reading quality
```

### What severity level applies?

```
Does the issue make content invisible to assistive technology?
├── YES → 🔴 CRITICAL (onTapGesture, missing labels on buttons, hidden disabled controls)
└── NO  → Does it break under system accessibility settings?
    ├── YES → 🟡 HIGH (hardcoded fonts, hardcoded colors, ignoring reduce motion)
    └── NO  → Is it a defense-in-depth gap?
        ├── YES → 🟢 MEDIUM (missing hints, no custom actions on list cells, no rotors)
        └── NO  → 🔵 LOW (best practice: input labels for Voice Control, custom content)
```

## Severity Definitions

- **🔴 CRITICAL** — Content or controls invisible to assistive technology. `onTapGesture` for interactive elements, missing `accessibilityLabel` on icon buttons, `isAccessibilityElement = false` on disabled controls, traits assigned instead of inserted (UIKit).
- **🟡 HIGH** — Breaks under accessibility settings. Hardcoded font sizes (`.system(size:)`), hardcoded colors (`.black`, `.white`), deprecated API (`foregroundColor`, `NavigationView`, `cornerRadius`), ignoring `reduceMotion`, no `numberOfLines = 0` on UIKit labels.
- **🟢 MEDIUM** — Degraded but not broken experience. Missing `accessibilityHint`, no custom actions on list cells, missing `.isHeader` traits on section headings, no grouping on related elements, no `accessibilityValue` on stateful controls.
- **🔵 LOW** — Best practices. Missing `accessibilityInputLabels` for Voice Control, no `accessibilityCustomContent` for secondary info, no Large Content Viewer on toolbar items.

## Core AI Failure Patterns

> For complete patterns with all 11 failure modes and code pairs, read `references/ai-failure-patterns.md`

| # | AI Failure | Search for | Severity |
|---|-----------|-----------|----------|
| F1 | `onTapGesture` instead of `Button` | `.onTapGesture` on interactive elements | 🔴 |
| F2 | Hardcoded font sizes | `.font(.system(size:` | 🟡 |
| F3 | Hardcoded colors for text/bg | `.foregroundColor(.black)`, `.background(Color.white)` | 🟡 |
| F4 | Deprecated API | `.foregroundColor(`, `.cornerRadius(`, `NavigationView` | 🟡 |
| F5 | No labels on image buttons | `Image(systemName:` inside Button without `.accessibilityLabel` | 🔴 |
| F6 | GeometryReader abuse + fixed frames | `GeometryReader`, `.frame(width:` with hardcoded values | 🟡 |
| F7 | No accessibility on custom controls | Custom views without any accessibility modifiers | 🔴 |
| F8 | `accessibilityIdentifier` vs `accessibilityLabel` confusion | `.accessibilityIdentifier` used where `.accessibilityLabel` needed | 🔴 |
| F9 | Missing system preference checks | No `@Environment` for `reduceMotion`, `dynamicTypeSize`, etc. | 🟡 |
| F10 | Assigning traits instead of inserting (UIKit) | `.accessibilityTraits = .selected` (destroys existing traits) | 🔴 |
| F11 | Hiding disabled controls | `isAccessibilityElement = false` on disabled buttons | 🔴 |

## Workflows

### Workflow: Accessibility Review of Existing Code

**When:** User asks to "review accessibility", "check VoiceOver support", "audit a11y", or any variant.

1. Read `references/ai-failure-patterns.md` — scan for all 11 AI failure patterns
2. Determine framework: SwiftUI, UIKit, or mixed → read corresponding patterns reference
3. Search for 🔴 CRITICAL issues first (onTapGesture, missing labels, trait assignment)
4. Search for 🟡 HIGH issues (hardcoded fonts, hardcoded colors, deprecated API)
5. Check system preference handling → read `references/motion-input.md`
6. If scope includes WCAG mapping → read `references/wcag-ios-mapping.md`
7. Report findings using the finding template (below)
8. For regulated apps → read `references/compliance.md`

### Workflow: Generate Accessible New Screen

**When:** Creating a new SwiftUI or UIKit screen. Apply from the start so no retrofitting is needed.

1. Read `references/ai-failure-patterns.md` — internalize patterns to avoid
2. Use `Button` for all interactive elements (never `onTapGesture`)
3. Use Dynamic Type text styles exclusively (never `.system(size:)`)
4. Use semantic colors (`.primary`, `.secondary`, `Color(.systemBackground)`)
5. Add `.accessibilityLabel` to every image button and custom control
6. Add `.accessibilityAddTraits(.isHeader)` to section headings
7. Group related elements with `.accessibilityElement(children: .combine)`
8. Use custom actions for list cells with multiple buttons
9. Check `@Environment(\.accessibilityReduceMotion)` for any animations
10. Add `.accessibilityValue` to stateful controls (toggles, sliders, custom)
11. Run confidence checks (below) before finalizing

### Workflow: Fix Specific Accessibility Issue

**When:** User asks "how do I fix this VoiceOver issue" or "make this control accessible"

1. Identify the current pattern and which AI failure it matches
2. Read the relevant reference file for the fix pattern
3. Provide the corrected code with explanation of WHY the fix works
4. Include VoiceOver announcement text so the user can verify ("VoiceOver reads: ...")
5. If the fix involves grouping or navigation, explain the user experience impact

### Workflow: Accessibility Audit for Release

**When:** User asks "is this ready for release" or "accessibility checklist"

1. Run all 🔴 CRITICAL pattern checks — any finding blocks release
2. Run 🟡 HIGH pattern checks — each needs risk acceptance or fix
3. Read `references/testing.md` — verify XCTest accessibility audit is configured
4. Read `references/wcag-ios-mapping.md` — check WCAG 2.2 AA coverage
5. For regulated apps → read `references/compliance.md` for legal requirements
6. Output pass/fail gate with blocking issues listed

### Workflow: Dynamic Type Compliance

**When:** User asks about Dynamic Type, text scaling, or font accessibility

1. Read `references/dynamic-type.md` — full Dynamic Type patterns
2. Search for `.font(.system(size:` — replace with text styles
3. Search for UIKit labels missing `adjustsFontForContentSizeCategory = true`
4. Check layout adaptation: HStack→VStack at accessibility sizes
5. Verify `ScrollView` wraps content that may overflow
6. Check `@ScaledMetric` usage for non-text dimensions (icons, spacing)

## WCAG 2.2 AA — iOS Quick Reference

Use this table when asked which WCAG criteria apply, what's auto-handled, and what needs manual work. Native iOS platform behavior auto-satisfies many criteria, and **some criteria simply do not apply** to native iOS (they exist for HTML/web).

### Criteria native iOS auto-handles

| Criterion | Why auto |
|-----------|----------|
| 1.3.4 Orientation | iOS rotates automatically unless the app locks it |
| 1.4.4 Resize Text | Dynamic Type handles this when the app uses text styles |
| 2.1.1 Keyboard | Full Keyboard Access navigates standard controls |
| 2.4.7 Focus Visible | UIKit/SwiftUI show a focus ring in Full Keyboard Access |
| 1.4.10 Reflow | Auto Layout + Dynamic Type reflow by default |

### Criteria that require MANUAL work

| Criterion | Manual action |
|-----------|--------------|
| **1.1.1 Non-text Content** | Every meaningful image/icon needs `accessibilityLabel`; decorative images need `Image(decorative:)` or `.accessibilityHidden(true)` |
| 1.3.1 Info and Relationships | Heading traits (`.isHeader`), grouping (`.accessibilityElement(children:)`), table/form structure |
| 1.4.3 Contrast (AA) | 4.5:1 for body text, 3:1 for large text — test in BOTH light and dark modes independently |
| 1.4.6 Contrast Enhanced (AAA) | 7:1 body text — required when user enables **Increase Contrast** system setting |
| **2.5.7 Dragging Movements (WCAG 2.2 NEW)** | Provide single-tap alternative via `accessibilityCustomActions` for any drag operation |
| **2.5.8 Target Size Minimum (WCAG 2.2 NEW)** | 24×24pt minimum (AA), 44×44pt preferred (Apple HIG) |
| **3.3.7 Redundant Entry (WCAG 2.2 NEW)** | Auto-fill or remember previously-entered info in multi-step forms |
| **3.3.8 Accessible Authentication (WCAG 2.2 NEW)** | No cognitive puzzles for login; support paste, password managers, biometrics |

### Criteria that DO NOT apply to native iOS

These are web/HTML-specific — calling them out is important because AI often copies them from web checklists:

- **4.1.1 Parsing** — markup validity. iOS is not HTML; no parsing to validate. (Removed in WCAG 2.2.)
- **2.4.1 Bypass Blocks** — "skip to main content". iOS uses the VoiceOver rotor instead.
- **4.1.2 Name, Role, Value** — handled structurally by `accessibilityLabel`/`traits`/`value` in native code, not markup.

When asked "which WCAG criteria apply to iOS", always explicitly name **1.1.1 Non-text Content** as manual (it's the most-missed), identify at least one of the **four NEW 2.2 criteria** (2.5.7, 2.5.8, 3.3.7, 3.3.8), and note that **4.1.1** and **2.4.1** don't apply.

## Specific APIs Quick Reference

These APIs frequently come up in reviews but are easy to forget. Surfaced here from the references so the body of a response can cite them directly.

### Form field label association (SwiftUI)

```swift
Text("Email:")
    .accessibilityLabeledPair(role: .label, id: "emailField", in: namespace)
TextField("", text: $email)
    .accessibilityLabeledPair(role: .content, id: "emailField", in: namespace)
```

Use `.accessibilityLabeledPair(role:id:in:)` (iOS 17+) to tell VoiceOver that a separate label view describes a nearby control. Without it, VoiceOver reads them as independent elements and the user doesn't know the label belongs to the field.

### Modal focus trapping (UIKit)

```swift
modalView.accessibilityViewIsModal = true
```

Two requirements to make this work:
1. **Direct-child placement.** `accessibilityViewIsModal` only hides the *siblings* of the modal view — not all other views in the hierarchy. The modal must be a direct child of the container whose siblings you want hidden (typically the window or a top-level container).
2. **Escape gesture.** Implement `accessibilityPerformEscape` on the modal so the VoiceOver user can dismiss it with a two-finger Z-gesture: `override func accessibilityPerformEscape() -> Bool { dismiss(...); return true }`

### Custom-drawn UIKit elements (canvas, graphs, charts)

When a single `UIView` draws its own hit-testable sub-regions (like bars in a bar chart), expose each region as a separate `UIAccessibilityElement`:

```swift
override var accessibilityElements: [Any]? {
    bars.map { bar in
        let element = UIAccessibilityElement(accessibilityContainer: self)
        element.accessibilityLabel = "\(bar.label), \(bar.value)"
        element.accessibilityTraits = .staticText
        // Use SCREEN coordinates for custom-drawn elements:
        element.accessibilityFrame = UIAccessibility.convertToScreenCoordinates(bar.frame, in: self)
        return element
    }
}
```

Set `isAccessibilityElement = false` on the parent container so VoiceOver sees the children. Use `UIAccessibility.convertToScreenCoordinates(_:in:)` for the frame — this is the canonical API for custom-drawn views because the system expects screen-space coordinates for hit-testing the VoiceOver cursor. (`accessibilityFrameInContainerSpace` is an alternative but requires the view to be in a standard container hierarchy, which custom-drawn graphs often aren't.)

### UIKit row/cell grouping order

```swift
cell.shouldGroupAccessibilityChildren = true  // group children into one swipe stop
titleLabel.accessibilitySortPriority = 2      // read first (higher = earlier)
subtitleLabel.accessibilitySortPriority = 1   // read second
```

`shouldGroupAccessibilityChildren` keeps VoiceOver focused on the cell (prevents wandering into children) while `accessibilitySortPriority` controls reading order within the group.

### Screen Curtain test

The gold-standard VoiceOver manual test: enable VoiceOver, then triple-tap with three fingers to toggle **Screen Curtain** — the display goes black while VoiceOver continues. Navigate the screen this way. If you can't complete the task, there's an accessibility gap. Every release checklist should include a Screen Curtain pass for critical flows.

## Finding Report Template

```
### [SEVERITY] [Short title]

**File:** `path/to/file.swift:42`
**WCAG:** [Criterion if applicable] | **HIG:** [Guideline if applicable]
**Issue:** [1-2 sentence description]
**VoiceOver Impact:** [What the user hears/doesn't hear]
**Fix:**
```swift
// ❌ Current
[problematic code]

// ✅ Corrected
[accessible replacement]
```
```

<critical_rules>
## Code Generation Rules

Whether generating new code or reviewing existing code, ALWAYS enforce these rules. They correct the systematic accessibility failures that AI coding assistants produce:

1. NEVER use `onTapGesture` for interactive elements — always use `Button`. Views with `onTapGesture` are invisible to VoiceOver, Switch Control, and visionOS eye tracking. This is the #1 AI failure.
2. NEVER use `.font(.system(size: N))` — always use Dynamic Type text styles (`.title`, `.body`, `.caption`, etc.). Hardcoded sizes break for 25%+ of users who change text size.
3. NEVER use `.foregroundColor(.black)` or `.background(Color.white)` — use `.foregroundStyle(.primary)` and `Color(.systemBackground)`. Hardcoded colors are invisible in dark mode.
4. ALWAYS add `.accessibilityLabel` to image-only buttons. `Image(systemName: "plus")` inside a `Button` reads as the raw SF Symbol name without a label.
5. ALWAYS use `.accessibilityAddTraits(.isHeader)` on section headings — enables VoiceOver rotor heading navigation.
6. ALWAYS use `.accessibilityElement(children: .combine)` or `.ignore` + custom label to group related content (product cards, list cells, table rows).
7. In UIKit, ALWAYS use `.insert(.selected)` — never `.accessibilityTraits = .selected` which DESTROYS existing traits like `.isButton`.
8. NEVER hide disabled controls — use `.disabled(true)` (SwiftUI auto-adds `.notEnabled` trait) or `.insert(.notEnabled)` in UIKit. VoiceOver reads "dimmed" so the user knows the control exists.
9. Use modern SwiftUI API: `.foregroundStyle()` not `.foregroundColor()`, `.clipShape(.rect(cornerRadius:))` not `.cornerRadius()`, `NavigationStack` not `NavigationView`.
10. For ANY animation, check `@Environment(\.accessibilityReduceMotion)` — replace motion with crossfade/opacity when enabled.
11. Don't include the element type in `accessibilityLabel` — say "Play" not "Play button" (VoiceOver adds "button" from the trait).
12. Use `Image(decorative:)` for decorative images — not `Image("bg").accessibilityHidden(true)`. When images inside a grouped container are purely visual (e.g., star icons in a rating display), hide each individual image with `.accessibilityHidden(true)` and provide a single meaningful description on the parent.
13. Use `.accessibilityAddTraits(.isToggle)` (iOS 17+) on any custom toggle-like control — VoiceOver announces "Toggle" so users know the control switches between states. Group the toggle's label and visual indicator with `.accessibilityElement(children: .combine)` or `.ignore`.
14. Use `@ScaledMetric(relativeTo:)` for non-text dimensions — including **image sizes**, icons, spacing, and avatars — so they scale proportionally with Dynamic Type: `@ScaledMetric(relativeTo: .body) var iconSize: CGFloat = 24`. Wrap content in `ScrollView` for overflow at accessibility text sizes. For UIKit labels always set `numberOfLines = 0` so scaled text can wrap. Toolbar/tab bar items should **cap** at `.xxxLarge` via `.dynamicTypeSize(...DynamicTypeSize.xxxLarge)` — unbounded scaling breaks toolbar layouts, and iOS shows a Large Content Viewer for bigger sizes instead.
15. Check ALL system accessibility preferences — not just reduce motion. Each has an `@Environment` key AND, where applicable, a SwiftUI/UIKit opt-out modifier:
    - `reduceMotion` — replace motion with crossfade/opacity
    - `reduceTransparency` — use opaque backgrounds instead of `.ultraThinMaterial`
    - `legibilityWeight` (Bold Text) — honor via `Font.weight(legibilityWeight == .bold ? .bold : .regular)`
    - `colorSchemeContrast` — when `.increased`, contrast ratio targets rise from **4.5:1 (AA) to 7:1 (AAA)** for body text; test contrast in BOTH light and dark modes independently
    - `accessibilityDifferentiateWithoutColor` — never convey status with color alone; add a shape, icon, or pattern
    - `invertColors` — photos, videos, and correctly-colored icons should opt out via `.accessibilityIgnoresInvertColors(true)` (SwiftUI) or `accessibilityIgnoresInvertColors = true` (UIKit). This property **does not cascade** to child views — apply it on each leaf view that renders photo content.
    - `dynamicTypeSize` — use `@Environment(\.dynamicTypeSize)` to switch HStack → VStack at `.accessibility1` and above
16. For WCAG 2.5.7 (Dragging Movements, new in WCAG 2.2) and 2.5.8 (Target Size Minimum): provide single-tap alternatives for drag operations using `accessibilityCustomActions`, and ensure touch target size is at least **24×24pt** (WCAG 2.5.8 AA minimum) or ideally **44×44pt** (Apple HIG). When answering drag-and-drop accessibility questions, cite **WCAG 2.5.7** specifically — it is the criterion that directly applies.
</critical_rules>

<fallback_strategies>
## Fallback Strategies & Loop Breakers

**If unsure whether an image is decorative or informative:**
Ask the user. Rule of thumb: if removing the image changes the meaning of the screen, it's informative and needs a label. If it's purely aesthetic, it's decorative.

**If a custom control is too complex for standard accessibility modifiers:**
Use `.accessibilityRepresentation` to provide an alternative accessible view (e.g., a custom gauge represented as a Slider for VoiceOver).

**If VoiceOver reading order is wrong after layout changes:**
In SwiftUI, use `.accessibilitySortPriority()` (higher = read earlier). In UIKit, override `accessibilityElements` array to define explicit order.

**If modal focus trapping isn't working:**
In UIKit, verify `accessibilityViewIsModal = true` is on the modal AND the modal is a **direct child** of the container whose siblings you want hidden — this property only hides SIBLINGS, not all other views. Also implement `accessibilityPerformEscape` on the modal so VoiceOver users can dismiss it with the two-finger Z-gesture. See "Specific APIs Quick Reference → Modal focus trapping" above.

**If Dynamic Type breaks layout at accessibility sizes:**
Use `ViewThatFits` (iOS 16+) to automatically switch between horizontal and vertical layouts. Wrap content in `ScrollView` for overflow. Use `AnyLayout` to preserve state during layout changes.

**If grouping with `.combine` produces awkward VoiceOver reading:**
Switch to `.ignore` + custom `accessibilityLabel` with a natural sentence. `.combine` joins labels with pauses; `.ignore` lets you write a coherent sentence.
</fallback_strategies>

## Confidence Checks

Before finalizing generated or reviewed code, verify ALL:

```
[ ] No onTapGesture on interactive elements — all use Button or standard controls
[ ] No hardcoded font sizes — all text uses Dynamic Type styles
[ ] No hardcoded colors for text/backgrounds — all use semantic colors
[ ] Every image-only button has accessibilityLabel
[ ] Section headings have .accessibilityAddTraits(.isHeader)
[ ] Related content grouped with .accessibilityElement(children:)
[ ] List cells with multiple actions use accessibilityCustomActions
[ ] Animations check @Environment(\.accessibilityReduceMotion)
[ ] Disabled controls visible to VoiceOver (not hidden, using .notEnabled)
[ ] UIKit traits inserted (.insert) not assigned (= .trait)
[ ] Labels describe purpose, not appearance ("Add to favorites" not "Heart icon")
[ ] Labels don't include element type ("Play" not "Play button")
[ ] Decorative images hidden from VoiceOver
[ ] Custom controls have label, value, traits, and adjustable action where appropriate
[ ] Custom toggles use .accessibilityAddTraits(.isToggle) and .accessibilityValue("On"/"Off")
[ ] Non-text dimensions (icons, spacing) use @ScaledMetric for Dynamic Type scaling
[ ] Content wrapped in ScrollView for overflow at accessibility text sizes
[ ] All system preferences checked: reduceMotion, reduceTransparency, legibilityWeight, colorSchemeContrast, differentiateWithoutColor, invertColors
[ ] Touch targets meet 44×44pt minimum (Apple HIG) / 24×24pt (WCAG 2.5.8)
[ ] Drag operations have single-tap alternatives via accessibilityCustomActions
[ ] Modern API used (foregroundStyle, clipShape, NavigationStack)
```

## Companion Skills

| Finding type | Companion skill | Apply when |
|---|---|---|
| Architecture patterns affecting accessibility | `skills/swiftui-mvvm/SKILL.md` | Structuring ViewModels that manage accessibility state |
| Security + accessibility overlap (biometric auth) | `skills/ios-security/SKILL.md` | LAContext with proper VoiceOver feedback |
| Testing accessibility in CI | `skills/ios-testing/SKILL.md` | XCTest accessibility audits, snapshot tests |
| Concurrency in VoiceOver announcements | `skills/swift-concurrency/SKILL.md` | Posting notifications from async contexts |

## References

| Reference | When to Read |
|-----------|-------------|
| `references/rules.md` | Do's and Don'ts quick reference: priority rules and critical anti-patterns |
| `references/ai-failure-patterns.md` | Every code generation/review — all 11 AI failure patterns with ❌/✅ code pairs |
| `references/voiceover-patterns.md` | VoiceOver work — labels, hints, traits, grouping, custom actions, rotors, navigation |
| `references/swiftui-patterns.md` | SwiftUI accessibility — all modifiers, component patterns, focus management |
| `references/uikit-patterns.md` | UIKit accessibility — elements, containers, traits, notifications, modal views |
| `references/dynamic-type.md` | Dynamic Type — UIFontMetrics, @ScaledMetric, layout adaptation, Large Content Viewer |
| `references/color-visual.md` | Color/contrast — WCAG ratios, color blindness, dark mode, reduce transparency, smart invert |
| `references/motion-input.md` | Motion & input — reduce motion, switch control, voice control, full keyboard access |
| `references/wcag-ios-mapping.md` | WCAG compliance — 2.2 AA criteria mapped to iOS APIs, what's auto-handled vs manual |
| `references/testing.md` | Testing — Xcode Accessibility Inspector, XCTest audits, VoiceOver manual protocol, CI setup |
| `references/ios-new-features.md` | iOS 17/18/26 — new accessibility APIs, modifiers, and platform features |
| `references/compliance.md` | Regulated apps — ADA, EAA, Section 508, VPAT, documentation requirements |

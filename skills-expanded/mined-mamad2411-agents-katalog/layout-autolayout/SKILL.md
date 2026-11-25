---
name: layout-autolayout
description: Auto Layout rules for UIKit/AppKit layouts, margins, and stack views.
metadata:
  short-description: Auto Layout rules for UIKit/AppKit UI work.
---

# Auto Layout

Use this skill for UI layout or visual styling work on UIKit or AppKit.

## Auto Layout (Required)
All UI layout must use Auto Layout with layout anchors. Frame-based layout and autoresizing masks are not allowed for production UI.

### Requirements
- Use Auto Layout exclusively for layout.
- Prefer UIStackView/NSStackView for linear layouts.
- Prefer layout anchors (NSLayoutAnchor APIs).
- Do not rely on autoresizing masks (translatesAutoresizingMaskIntoConstraints = false).
- Intrinsic size must be computable without overriding intrinsicContentSize. Use subview constraints, hugging/compression, and systemLayoutSizeFitting when needed.

### Layout Margins (Default)
Layout margins are the default constraint reference.

UIKit:
```swift
view.layoutMarginsGuide.leadingAnchor
view.layoutMarginsGuide.trailingAnchor
view.layoutMarginsGuide.topAnchor
view.layoutMarginsGuide.bottomAnchor
```

AppKit:
```swift
view.layoutMarginsGuide.leadingAnchor
view.layoutMarginsGuide.trailingAnchor
view.layoutMarginsGuide.topAnchor
view.layoutMarginsGuide.bottomAnchor
```

### Hard-coded Spacing
- Avoid hard-coded spacing constants (8, 12, 16, etc.).
- Prefer layout margins, intrinsic content size, and system spacing relations.
- Hard-coded constants are allowed only when explicitly required by design.

### Valid Exceptions (Raw Anchors)
- Aligning sibling views
- Building custom controls
- Drawing edge-to-edge backgrounds
- Implementing separators
- Performance-critical measurement-only layout

### Constraint Hygiene
- Keep constraints close to the views they lay out.
- Group and activate constraints together.
- Readability is required.

### Platform Notes
- UIKit: Auto Layout + anchors + margins only.
- AppKit: Auto Layout + anchors + margins only; avoid springs-and-struts.

### UIKit/AppKit Addendum
- Prefer stack views for vertical/horizontal composition; only drop to manual constraints for non-linear or performance-critical layouts.
- Use layoutMarginsGuide and isLayoutMarginsRelativeArrangement with stack views to respect margins by default.
- Use system spacing APIs before hard-coded constants.
- Prefer system controls over custom drawing to preserve native focus/selection behavior.
- Custom views should size via constraints and subview intrinsic sizes, never by overriding intrinsicContentSize.

## Liquid Glass
- Follow the `liquid-glass-design` skill for Liquid Glass behavior and APIs on UIKit/AppKit.

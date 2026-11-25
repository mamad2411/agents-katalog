---
name: ios-hig-reference
description: Apple Human Interface Guidelines quick reference. Use when needing iOS design guidelines, HIG rules, or Apple design best practices.
version: 1.0.0
---

# iOS HIG Reference

Quick reference for Apple Human Interface Guidelines (iOS/iPadOS).

## When to Use

- Need iOS design guidelines
- Looking up HIG requirements
- Checking Apple design best practices
- Understanding iOS design patterns

## Core Principles

### Clarity
- Content takes priority
- Legible text at every size
- Precise, purposeful icons
- Subtle, appropriate adornments

### Deference
- UI supports content, never competes
- Fluid motion for understanding
- Translucency hints at more content

### Depth
- Visual layers convey hierarchy
- Realistic motion creates understanding
- Touch and discoverability through depth

## Foundations

### Colors

| Type | Light | Dark | Usage |
|------|-------|------|-------|
| systemBackground | White | Black | Primary background |
| secondarySystemBackground | Gray6 | Gray5 | Grouped content |
| label | Black | White | Primary text |
| secondaryLabel | Gray | Gray | Secondary text |
| separator | Gray4 | Gray4 | Dividers |
| systemBlue | #007AFF | #0A84FF | Links, actions |

### Typography

| Style | Size | Weight | Usage |
|-------|------|--------|-------|
| largeTitle | 34pt | Regular | Screen titles |
| title | 28pt | Regular | Section headers |
| title2 | 22pt | Regular | Subsections |
| title3 | 20pt | Regular | Minor headers |
| headline | 17pt | Semibold | Emphasis |
| body | 17pt | Regular | Main content |
| callout | 16pt | Regular | Secondary info |
| subheadline | 15pt | Regular | Captions |
| footnote | 13pt | Regular | Small text |
| caption | 12pt | Regular | Labels |
| caption2 | 11pt | Regular | Tiny labels |

### Spacing & Layout

- **Margins**: 16pt (compact), 20pt (regular)
- **Content spacing**: 8pt (tight), 16pt (standard), 24pt (loose)
- **Touch targets**: Minimum 44×44pt
- **Button spacing**: 12-24pt between tappable elements

## Components

### Navigation

**Tab Bar**
- 2-5 items only
- Primary destinations, not actions
- Icons + labels
- Selected state clearly indicated

**Navigation Bar**
- Title centered or large
- Back button on left
- Actions on right (max 2-3)

### Controls

**Buttons**
- Filled: Primary actions
- Bordered: Secondary actions
- Plain: Tertiary actions
- Minimum height: 44pt

**Text Fields**
- Clear button when content present
- Placeholder text for hints
- Appropriate keyboard type
- Secure entry for passwords

**Toggles**
- Immediate effect (no save needed)
- Green = on, gray = off
- Label describes on-state

### Lists

**Standard**
- Disclosure indicator → navigates to detail
- Checkmark → selection
- Detail disclosure → shows info

**Swipe Actions**
- Trailing: destructive (delete)
- Leading: constructive (archive, favorite)

## Accessibility

### Requirements

| Feature | Requirement |
|---------|-------------|
| VoiceOver | Labels for all interactive elements |
| Dynamic Type | Support 200% text scaling |
| Color Contrast | 4.5:1 (normal), 7:1 (small text) |
| Motion | Respect reduce motion preference |
| Touch | 44×44pt minimum targets |

### VoiceOver Labels

```swift
// Icon-only button
Button { } label: { Image(systemName: "trash") }
    .accessibilityLabel("Delete")

// Combined elements
HStack { Image(...); Text(...) }
    .accessibilityElement(children: .combine)

// Decorative
Image("decoration")
    .accessibilityHidden(true)
```

## SF Symbols

### Rendering Modes

| Mode | Usage |
|------|-------|
| Monochrome | Single color, default |
| Hierarchical | Depth through opacity |
| Palette | 2-3 custom colors |
| Multicolor | Predefined colors |

### Common Symbols

| Category | Symbols |
|----------|---------|
| Navigation | house, magnifyingglass, person, gear |
| Actions | plus, minus, xmark, checkmark |
| Status | star, heart, bookmark, bell |
| Media | play, pause, forward, backward |
| Editing | pencil, trash, square.and.arrow.up |

## Dark Mode

### Must Support
- All custom colors need light/dark variants
- Images may need separate dark versions
- Avoid pure black (#000) — use system colors
- Test vibrancy and materials

## Quick Links

- [Full HIG](https://developer.apple.com/design/human-interface-guidelines/)
- [SF Symbols](https://developer.apple.com/sf-symbols/)
- [Color Guidelines](https://developer.apple.com/design/human-interface-guidelines/color)
- [Typography](https://developer.apple.com/design/human-interface-guidelines/typography)

## Related Skills

- `ios-swiftui-generator` — Generate HIG-compliant code
- `ios-design-review` — Validate HIG compliance

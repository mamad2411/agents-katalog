---
name: mobile-design-system
description: "Comprehensive mobile UI/UX design system covering React Native components, touch interactions, gesture patterns, accessibility, app navigation, and visual design principles. Use when building mobile apps, designing mobile screens, implementing React Native UI, reviewing mobile UX, or following iOS/Android platform conventions. Triggers: mobile UI, React Native, app design, mobile UX, touch targets, mobile patterns, app screen design."
license: MIT
metadata:
  version: 1.0.0
  category: design
  tags: [mobile, react-native, ios, android, ux, ui, design, accessibility, touch, gestures]
---

# Mobile Design System

A unified mobile design system covering UX patterns, React Native implementation, visual design process, and platform conventions for iOS and Android.

## When to Use This Skill

Activate this skill when the task involves:

- **Building mobile apps** with React Native, Flutter, or SwiftUI
- **Designing mobile screens** -- layouts, flows, onboarding, dashboards
- **Implementing touch interactions** -- gestures, swipe actions, pinch-to-zoom
- **Reviewing mobile UX** -- auditing touch targets, thumb zones, accessibility
- **Following platform conventions** -- iOS Human Interface Guidelines, Material Design
- **Creating responsive mobile-first web apps** or Progressive Web Apps
- **Optimizing mobile performance** -- images, loading states, Core Web Vitals
- **Mobile accessibility** -- screen readers, contrast, Dynamic Type, VoiceOver/TalkBack

## Core Philosophy

Mobile UI is about touch, speed, and focus. There are no hover states. Screens are small. Users operate one-handed, often distracted, on unreliable networks. Every design decision must account for these constraints.

Three questions before designing any screen:

1. **What is the user trying to accomplish?** Reduce friction to that goal.
2. **How should this make the user feel?** Trust, delight, confidence, calm.
3. **What should they notice first?** Establish clear visual hierarchy.

## Foundational Rules

### Touch Targets (Non-Negotiable)

All interactive elements must meet minimum touch target sizes:

| Platform | Minimum | Optimal | Spacing |
|----------|---------|---------|---------|
| iOS (HIG) | 44x44 pt | 56x56 pt | 8pt |
| Android (Material) | 48x48 dp | 56x56 dp | 8dp |
| Web (WCAG 2.1 AAA) | 44x44 px | 48x48 px | 8px |

Never create buttons, links, or icon buttons smaller than these minimums. Use `minHeight` and `minWidth` rather than fixed dimensions so content can grow with Dynamic Type.

### Thumb Zones

Mobile screens have three ergonomic zones for one-handed use:

- **Easy zone** (bottom center): Place primary actions here -- CTAs, tab bars, submit buttons
- **Stretch zone** (middle): Content area, form fields, secondary actions
- **Difficult zone** (top corners): Destructive actions, infrequent navigation, settings

### Spacing: 4px/8px Grid

All spacing values must be divisible by 4 or 8: `4, 8, 12, 16, 24, 32, 48, 64, 80, 96`.

- Related elements: closer together (8-16px)
- Unrelated groups: further apart (24-48px)
- Section padding: 80-96px vertical minimum
- Card internal padding: 24-32px

### Color: 60/30/10 Rule

- **60%** neutral base (white, light gray, or dark background)
- **30%** complementary (text, dark elements)
- **10%** accent/brand (CTAs, key indicators)

Use opacity variations for text hierarchy: 100% headings, 80% body, 60% secondary.

### Typography Constraints

- **One font family** (two maximum with clear hierarchy purpose)
- **Maximum 4 font sizes** and **2 font weights**
- Minimum 16px font size on web to prevent iOS auto-zoom
- Use monospace variants for large numbers (prices, stats, metrics)

### Accessibility (Non-Negotiable)

- Color contrast: 4.5:1 for normal text, 3:1 for large text (WCAG AA)
- Every interactive element needs accessibility labels
- Every `Pressable`/button needs a visible pressed state
- Support Dynamic Type / font scaling
- Test with VoiceOver (iOS) and TalkBack (Android)

## Design Process

Follow this sequence for any mobile screen:

### 1. Understand Context
- App type (fitness, finance, social, productivity, health, crypto)
- User stage (new, returning, power user)
- Primary action on this screen
- Industry conventions (see `references/design-process.md` and `references/industry-conventions.md`)

### 2. Structure First (UX)
- Map the user flow: what comes before and after this screen
- Identify MVP elements -- only what is essential
- Place primary actions in the thumb zone
- Follow F-pattern reading order
- Turn empty states into opportunities (guidance + illustration + CTA)

### 3. Apply Visual Design (UI)
- Typography hierarchy with size, weight, and opacity
- 60/30/10 color application
- 8-point grid spacing
- Soft shadows matched to background tint (never pure gray/black)
- Visual cues: icons, images, color-coded categories

### 4. Design for Emotion (Peak-End Rule)
Users remember two moments: the **peak** (most intense) and the **end** (last impression).
- Design peak moments: micro-animations, celebratory feedback, personalized insights
- Design endings: summary cards, progress affirmation, gentle nudges to return
- Add emotional feedback loops: success states should feel rewarding

### 5. Polish
- Micro-animations for state changes (200-300ms, native driver)
- All states designed: loading (skeleton screens), empty, error, success
- Safe area handling (notch, home indicator)
- Dark mode support with semantic colors
- Platform-appropriate styling (iOS shadows vs Android elevation)

## Platform Quick Reference

### iOS (Human Interface Guidelines)
- SF Pro system font, Dynamic Type required
- Large titles (34pt), navigation bars with back buttons
- Tab bars: 5 items max, always show labels
- Blue (#007AFF) for tappable elements, Red (#FF3B30) for destructive
- Edge swipe for back navigation
- Rounded corners: 10-14pt

### Android (Material Design 3)
- Roboto font family, Material You dynamic color
- FAB for primary actions (56x56dp)
- Bottom navigation for 3-5 destinations
- Elevation system (shadows indicate hierarchy: 0-24dp)
- Rounded corners: 12-28pt

### Cross-Platform (React Native)
- Use `Platform.select()` for iOS/Android differences
- `useSafeAreaInsets()` for safe areas
- `useNativeDriver: true` for 60fps animations
- `StyleSheet.create()` over inline styles
- `Pressable` with visible pressed states

## Anti-Patterns

- Touch targets smaller than 44pt
- Placing primary actions in top corners (outside thumb zone)
- More than 4 font sizes or 3 font weights
- Random spacing values (not on the 4px/8px grid)
- Invisible buttons (transparent background without border)
- Hover-dependent interactions (no hover on mobile)
- Fixed heights that break with Dynamic Type
- Pure gray/black shadows on colored backgrounds
- Ignoring safe areas (notch, home indicator)
- JS-driven animations instead of native driver

## Reference Guides

This skill includes detailed reference files for deep dives. Load them as needed:

| Reference | Use When | Content |
|-----------|----------|---------|
| `references/react-native-patterns.md` | Implementing React Native UI | Components, animations, accessibility, platform-specific code, Reanimated patterns |
| `references/ux-patterns.md` | Designing mobile interactions | Touch gestures (tap, swipe, pinch, long press, drag), navigation patterns, mobile forms, performance optimization |
| `references/design-process.md` | Running a mobile design process | 5-step design framework, visual design rules, emotional design, smart UI patterns, implementation notes |
| `references/industry-conventions.md` | Designing for specific industries | Industry-specific design languages (AI, crypto, finance, health, education, fitness), Peak-End Rule, Spotify strategic principles |

## Example Output

When reviewing a mobile screen, produce findings like this:

```
Design Review — Login Screen

✅ Touch targets: All buttons meet 44pt minimum
⚠️ Spacing: 12px gap between form fields → should be 16px (8pt grid)
❌ Contrast: Secondary text (#999) on white is 2.6:1 → needs 4.5:1 minimum
✅ Typography: 2 weights, 3 sizes — clean hierarchy
⚠️ CTA position: "Sign In" is above thumb zone → move to bottom third
✅ Accessibility: All inputs have labels
❌ Missing state: No error state for invalid credentials
✅ Safe area: Properly handled for notch devices

Score: 6.5/10 — 3 fixes needed for production quality
Priority: contrast fix > CTA position > spacing alignment
```

## Related Design Skills

- **ios-glass-ui**: For iOS-specific glass material design (translucency, blur, depth)
- **ui-ux-polish**: For iterative visual polishing of existing UIs toward production quality

## Quick Checklist

```
[ ] All touch targets >= 44pt (48pt preferred)
[ ] Primary actions in thumb zone (bottom 1/3)
[ ] Spacing on 4px/8px grid
[ ] Color contrast >= 4.5:1 for text
[ ] Accessibility labels on all interactive elements
[ ] Visible pressed/active states on all buttons
[ ] Safe area handling (notch, home indicator)
[ ] Loading states (skeleton screens)
[ ] Error states with clear guidance
[ ] Empty states with illustration + CTA
[ ] Dark mode support
[ ] Dynamic Type / font scaling
[ ] Native driver animations (60fps)
[ ] Platform-appropriate styling
[ ] 16px minimum font size (web, prevents iOS zoom)
```

---
name: hci-ios-swiftui
description: Applies human-computer interaction and accessibility principles to iOS apps built with SwiftUI or UIKit, following Apple's Human Interface Guidelines. Use whenever the user builds, reviews or fixes iOS or iPadOS UI and cares about VoiceOver, accessibilityLabel, Dynamic Type, 44 pt touch targets, Reduce Motion, dark mode, forms and keyboards, haptics and feedback, navigation conventions or right-to-left languages, even if they only say "make my SwiftUI view more accessible". Lints Swift code with a script and fixes issues.
---

# hci-ios-swiftui

Make an iOS app feel native and work for everyone: VoiceOver that reads the right thing, text that scales with Dynamic Type, comfortable targets and layouts that mirror in RTL. Builds on `hci-foundations`.

```
hci-ios-swiftui/
├── SKILL.md
├── scripts/
│   └── lint_swift_hci.py            static checks for Swift files
└── references/
    └── ios-guidelines.md            VoiceOver, targets, Dynamic Type, settings, feedback, forms, navigation, RTL, tests
```

## When to use

- Writing or reviewing SwiftUI views and UIKit screens
- Fixing VoiceOver issues or Accessibility Inspector findings
- Supporting Dynamic Type, Reduce Motion, Increase Contrast, dark mode and Persian or Arabic
- Choosing patterns for feedback, destructive actions, forms and navigation

## Workflow

1. **Understand the screen**: users, the key task, devices (iPhone, iPad), languages, SwiftUI or UIKit.
2. **Lint**: `python3 scripts/lint_swift_hci.py Sources/` (a file or a folder). It reports images without labels, fixed font sizes that ignore Dynamic Type, `.onTapGesture` instead of `Button`, small tap frames, left and right instead of leading and trailing, `lineLimit(1)` truncation, UIKit text alignment, and project gaps (localization, reduce motion). Add `--strict` to fail on warnings.
3. **Fix in order**: VoiceOver names and traits first, then Dynamic Type and tap targets, then feedback and forms, then settings such as Reduce Motion and contrast.
4. **Check against the principles**: visibility of status, error prevention (keyboard types, confirmation dialogs, Undo), consistency with Apple's patterns (NavigationStack, tab bar, system sheets), recognition over recall. Cite the heuristic when explaining a change.
5. **Add checks**: Xcode previews with large Dynamic Type, dark mode and RTL, and `performAccessibilityAudit()` in UI tests.
6. **Verify by hand** and say what remains: VoiceOver and Voice Control through the key task, the largest accessibility text size, Reduce Motion, Increase Contrast, RTL. A linter cannot judge contrast, focus order or real speech output.
7. **Report** findings, changes and open checks.

## Rules

- Use `Button`, `Toggle` and other system controls for interactive elements; if custom, add traits and a label
- Every meaningful image has a label; decorative images are hidden from VoiceOver
- Use text styles and `@ScaledMetric`; never hardcode sizes that ignore Dynamic Type
- Tap targets are at least 44 by 44 pt with `contentShape` for the full area
- Use `.leading` and `.trailing`; mirror only directional symbols
- Honor Reduce Motion, Reduce Transparency, Increase Contrast and Differentiate Without Color
- Prefer Undo to confirmation; name the object in destructive dialogs
- Never claim accessibility from a quiet linter; state what was tested

## What to report back

| Field | Content |
|-------|---------|
| Findings | rule, file and line, severity, user impact |
| Changes | what changed and the principle or HIG guidance it serves |
| Checks added | previews, accessibility audit |
| Manual checks left | VoiceOver, Dynamic Type at the largest size, RTL, Reduce Motion |

## Related skills

- `hci-foundations`: principles and evaluation reports
- `hci-rtl-localization`: right-to-left and multilingual details
- `hci-microcopy`: wording for buttons, errors and empty states
- `hci-usability-testing`: validate with real users
- `hci-react-native`, `hci-flutter`, `hci-android-native`: other mobile stacks

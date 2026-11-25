---
name: hci-android-native
description: Applies human-computer interaction and accessibility principles to native Android apps built with Views (XML) or Jetpack Compose. Use whenever the user builds, reviews or fixes Android UI and cares about TalkBack, contentDescription, touch targets of 48dp, text in sp, forms and keyboards, snackbars and feedback, Material design conventions, back navigation, RTL support or large font and display size, even if they only say "improve my Android screen". Lints layouts, manifest and Compose code with a script and fixes issues.
---

# hci-android-native

Make an Android app clear, reachable and accessible: names for TalkBack, 48 dp targets, text that scales in sp, Material feedback patterns and correct right-to-left behavior. Builds on `hci-foundations`.

```
hci-android-native/
├── SKILL.md
├── scripts/
│   └── lint_android_hci.py            layout XML, AndroidManifest.xml and Compose (.kt) checks
└── references/
    └── android-guidelines.md          semantics, targets, text, feedback, forms, navigation, RTL, testing
```

## When to use

- Building or reviewing layouts and Compose screens
- Fixing TalkBack issues or Accessibility Scanner findings
- Supporting large fonts, large display size, dark theme and Persian or Arabic
- Choosing feedback, error, permission and navigation patterns

## Workflow

1. **Understand the screen**: users, key task, form factors, languages, Views or Compose.
2. **Lint**: `python3 scripts/lint_android_hci.py app/src/main` (a file or a folder). It reports images without `contentDescription`, inputs without hints, text sized in dp, tiny text, small clickable elements, physical left and right attributes, missing `supportsRtl`, and in Compose: `fontSize` in dp, small clickable sizes, null descriptions, hardcoded strings and absolute padding. Add `--strict` to fail on warnings.
3. **Fix in order**: errors first (missing names, wrong units), then touch targets and RTL attributes, then forms and feedback, then polish. Use `start` and `end`, `sp` for text, `minimumInteractiveComponentSize()` in Compose.
4. **Check against the principles**: visibility of status (progress, snackbars), error prevention (input types, undo), consistency with Material (bottom navigation, back behavior), recognition over recall. Cite the heuristic when explaining a change.
5. **Add checks**: enable `AccessibilityChecks` in Espresso or add Compose semantics tests, and run Android Lint.
6. **Verify by hand** and say what remains: TalkBack through the key task with the screen dimmed, largest font and display size, forced RTL, dark theme, a small phone. A scan cannot judge contrast, focus order or real speech output.
7. **Report** findings, changes and open checks.

## Rules

- Every image and icon button has a `contentDescription`, or is explicitly decorative
- Text is in `sp`, layouts in `dp`; never fix text container heights
- Touch targets are at least 48 dp with spacing; gestures have alternatives
- Inputs have a visible label or hint, the right `inputType` and autofill hints
- Use `start` and `end`; set `supportsRtl="true"`; mirror directional icons only
- Use snackbars with Undo instead of confirming every destructive step; keep messages on screen long enough
- Respect system back, window insets, dark theme and reduced animation settings
- Never claim accessibility from a quiet linter

## What to report back

| Field | Content |
|-------|---------|
| Findings | rule, file and line, severity, user impact |
| Changes | what changed and the principle it serves |
| Checks added | Espresso, Compose, Lint |
| Manual checks left | TalkBack, font and display size, RTL, dark theme |

## Related skills

- `hci-foundations`: principles and evaluation reports
- `hci-rtl-localization`: right-to-left and multilingual details
- `hci-microcopy`: wording for buttons, errors and empty states
- `hci-usability-testing`: validate with real users
- `hci-react-native`, `hci-flutter`, `hci-ios-swiftui`: other mobile stacks

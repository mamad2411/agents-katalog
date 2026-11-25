---
name: hci-flutter
description: Applies human-computer interaction and accessibility principles to Flutter apps. Use whenever the user builds, reviews or fixes Flutter or Dart UI and cares about usability, TalkBack and VoiceOver, Semantics, tooltips, tap targets, text scaling, forms, snackbars and feedback, right-to-left layout, dark mode or reduce motion, even if they only say "make my Flutter screen friendlier". Lints Dart code with a script and fixes issues using Material and platform conventions.
---

# hci-flutter

Make a Flutter app usable for everyone: announced correctly by screen readers, reachable by thumbs, readable at any text size, and correct in right-to-left languages. Builds on `hci-foundations`.

```
hci-flutter/
├── SKILL.md
├── scripts/
│   └── lint_flutter_hci.py          static checks for Dart files
└── references/
    └── flutter-guidelines.md        semantics, targets, text, feedback, forms, direction, motion, tests
```

## When to use

- Writing or reviewing screens, forms, lists, dialogs and navigation
- Fixing screen reader problems or accessibility audit findings
- Supporting large text, dark mode, reduce motion or Persian and Arabic
- Choosing feedback patterns for loading, errors, undo and empty states

## Workflow

1. **Understand the screen**: users, the key task, devices (phone, tablet, desktop, web) and languages.
2. **Lint**: `python3 scripts/lint_flutter_hci.py lib/` (a file or a folder). It reports tappable widgets without Semantics, `IconButton` without tooltip, images without `semanticLabel`, hint-only text fields, locked text scale, tiny fonts, shrunk tap targets, short snackbars, physical left and right layout, and project gaps (localization, reduce motion). Add `--strict` to fail on warnings.
3. **Fix in order**: screen reader names and roles, then tap targets and text scaling, then feedback and forms, then direction and motion. Prefer real Button widgets over `GestureDetector`; when custom, wrap with `Semantics`.
4. **Check against the principles**: visibility of status, error prevention, undo over confirmation, recognition over recall, consistency with Material and platform behavior. Cite the heuristic when explaining a change.
5. **Add automated guideline tests** from the reference (`meetsGuideline` tap target, label and contrast checks, and a 2x text scale test).
6. **Verify by hand** and say what remains: TalkBack and VoiceOver passes, largest text, RTL locale, dark mode, small phone. The linter cannot judge contrast, focus order or real speech output.
7. **Report** findings, changes and open checks.

## Rules

- Every interactive widget has an accessible name and role; decorative images are excluded from semantics
- Labels are visible; hints are examples only; color is never the only signal
- Never lock text scaling; fix layouts that overflow instead
- Tap targets at least 48 dp with spacing; swipes have visible alternatives
- Every async action shows progress and cannot be submitted twice; errors say how to recover and keep input
- Use directional APIs (`EdgeInsetsDirectional`, `TextAlign.start`) so one layout serves both directions
- Do not claim accessibility from a quiet linter; state what was tested

## What to report back

| Field | Content |
|-------|---------|
| Findings | rule, file and line, severity, user impact |
| Changes | what changed and the principle it serves |
| Tests added | guideline and text scale tests |
| Manual checks left | screen reader, large text, RTL, dark mode |

## Related skills

- `hci-foundations`: principles and evaluation reports
- `hci-rtl-localization`: right-to-left and multilingual details
- `hci-microcopy`: wording for buttons, errors and empty states
- `hci-usability-testing`: validate with real users
- `hci-react-native`, `hci-android-native`, `hci-ios-swiftui`: other mobile stacks

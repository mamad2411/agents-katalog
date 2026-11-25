---
name: hci-react-native
description: Applies human-computer interaction and accessibility principles to React Native and Expo mobile apps. Use whenever the user builds, reviews or fixes a React Native or Expo screen or component and cares about usability, touch targets, VoiceOver or TalkBack support, keyboards and forms, loading and error feedback, safe areas, dark mode, large text, reduce motion or right-to-left layout, even if they only say "make this screen better for users". Lints the code with a script, then fixes issues using platform conventions.
---

# hci-react-native

Make a React Native app easy, safe and pleasant to use on real phones: reachable controls, clear feedback, correct screen reader output, flexible text and RTL support. Builds on `hci-foundations`.

```
hci-react-native/
├── SKILL.md
├── scripts/
│   └── lint_rn_hci.py              static checks for js, jsx, ts and tsx files
├── references/
│   └── mobile-guidelines.md        touch, accessibility props, text, feedback, forms, navigation, RTL, testing
└── templates/
    └── AccessibleButton.tsx        button with role, label, state, loading and 48 dp target
```

## When to use

- Writing or reviewing a screen, form, list or navigation flow
- Fixing accessibility bugs reported by users or an audit
- Making an app work with large text, dark mode, reduce motion or Persian and Arabic
- Choosing patterns for feedback, errors, loading and permissions

## Workflow

1. **Understand the screen**: users, the key task, device range (phones, tablets), and the languages. Ask only what you cannot infer.
2. **Lint**: `python3 scripts/lint_rn_hci.py src` (a file or a folder). It reports pressables without names or roles, images without alt text, inputs that use only a placeholder, targets under 44 pt, disabled font scaling, tiny fonts, absolute text alignment, and project gaps (keyboard handling, safe area, reduce motion, RTL). Add `--strict` to fail on warnings.
3. **Fix in order**: access and name problems first (they block users completely), then touch targets and text scaling, then feedback and forms, then polish. Use `templates/AccessibleButton.tsx` as the pattern for interactive elements.
4. **Check against the principles**: visibility of status (loading, success, error), error prevention (right keyboard, confirmations, undo), consistency with the platform (back behavior, tab bar), recognition over recall (visible labels). Cite the heuristic when explaining a change.
5. **Handle RTL and text growth** using `references/mobile-guidelines.md`, and point to `hci-rtl-localization` for the full checklist.
6. **Verify**: say exactly what to test by hand: VoiceOver and TalkBack through the key task with the screen off, text at 200 percent, dark mode, a small phone, offline. The linter cannot judge contrast, focus order or real screen reader speech.
7. **Report** the findings and the changes, with what remains unverified.

## Rules

- Every interactive element has a role and an accessible name; decorative images are hidden from screen readers
- Never rely on a placeholder as a label, or on color alone for meaning
- Never disable the user's font scaling; fix layouts that break instead
- Touch targets are at least 44 pt on iOS and 48 dp on Android, with spacing, and gestures have a visible alternative
- Every async action shows progress and cannot be submitted twice
- Errors say what happened and how to recover, and keep the user's input
- Follow platform conventions over novelty; do not hide primary navigation without reason
- Test claims honestly: do not say an app is accessible because a linter is quiet

## What to report back

| Field | Content |
|-------|---------|
| Findings | rule, file and line, severity, why it matters to users |
| Changes | what was modified and which principle it serves |
| Manual checks left | screen reader pass, large text, RTL, low-end device |
| Follow ups | automated tests with role and label queries, an audit, a small user test |

## Related skills

- `hci-foundations`: principles and heuristic evaluation reports
- `hci-rtl-localization`: right-to-left layout, numbers, fonts
- `hci-microcopy`: wording of buttons, errors and empty states
- `hci-usability-testing`: test with real users
- `hci-web-accessibility`: contrast calculator and WCAG details

---
name: hci-desktop-apps
description: Applies human-computer interaction principles to desktop applications built with Electron, Qt, GTK, WPF, WinUI, AppKit, Tauri or similar. Use whenever the user designs or reviews a desktop app and cares about keyboard shortcuts, menus, toolbars, dialogs, window behavior, command palettes, long-running operations, undo, accessibility with NVDA, VoiceOver or Orca, high contrast, or platform conventions on Windows, macOS and Linux, even if they only say "my desktop app feels clunky". Audits keyboard shortcuts with a script.
---

# hci-desktop-apps

Design desktop software that rewards long use: keyboard-first, predictable, fast and respectful of each platform. Builds on `hci-foundations`.

```
hci-desktop-apps/
├── SKILL.md
├── scripts/
│   └── check_shortcuts.py          audit shortcuts: conflicts, OS-reserved, standards, wrong modifier
└── references/
    └── desktop-guidelines.md       keyboard, menus, dialogs, pointer, feedback, accessibility, settings, tests
```

## When to use

- Designing or reviewing menus, toolbars, dialogs and window behavior
- Defining or fixing keyboard shortcuts, adding a command palette
- Long-running operations, progress, cancel, autosave and undo
- Accessibility for screen readers, high contrast and scaling
- Making one app feel right on Windows, macOS and Linux

## Workflow

1. **Understand the users and platforms**: who uses it for how long, which tasks repeat, which operating systems, which toolkit (native, Qt, GTK, Electron, Tauri).
2. **Audit shortcuts**: write them as JSON (`{"platform": "windows", "shortcuts": [{"keys": "Ctrl+S", "action": "Save", "context": "global"}]}`) and run `python3 scripts/check_shortcuts.py shortcuts.json`. It finds conflicts in overlapping contexts, OS-reserved combinations, standard shortcuts rebound to other actions, single-key global shortcuts, the wrong primary modifier (Ctrl versus Cmd) and unbound standards. Run once per platform.
3. **Review the structure** with `references/desktop-guidelines.md`: menu layout per platform, toolbar contents, dialog button order and wording, window state memory, preferences.
4. **Check against the principles**: visibility of status (progress, saved state), user control (undo, cancel), consistency and standards, efficiency (shortcuts, command palette), error prevention, recognition over recall (shortcuts shown in menus). Cite the heuristic when explaining a change.
5. **Check accessibility**: keyboard-only pass, screen reader names and roles, high contrast, 200 percent scaling, focus handling after dialogs.
6. **Say what you cannot verify** from files: real keyboard order, screen reader speech, behavior on each OS. Give the manual test list from the reference.
7. **Report** findings, recommendations and the test plan.

## Rules

- Standard shortcuts keep their standard meaning; never override system shortcuts
- Use Cmd on macOS and Ctrl on Windows and Linux for the primary modifier
- Every action is available without a pointer, and every drag has a keyboard alternative
- Show shortcuts in menus and tooltips; verbs in labels; ellipsis only when a dialog follows
- Never block the UI thread; show progress over one second and offer Cancel for long work
- Prefer Undo to confirmation dialogs; keep confirmations specific
- Remember window and layout state; respect system theme, scaling and reduced motion
- Do not claim accessibility without a real screen reader pass

## What to report back

| Field | Content |
|-------|---------|
| Shortcut audit | conflicts, reserved keys, rebound standards, per platform |
| Structure findings | menus, toolbars, dialogs, window behavior |
| Accessibility | what was checked, what remains |
| Recommendations | ordered by user impact |
| Test plan | keyboard-only, screen reader, high contrast, scaling, large data |

## Related skills

- `hci-foundations`: principles and evaluation reports
- `hci-cli-ux`: command-line tools
- `hci-rtl-localization`: right-to-left and multilingual desktop UI
- `hci-microcopy`: dialog and button wording
- `hci-usability-testing`: validate with real users

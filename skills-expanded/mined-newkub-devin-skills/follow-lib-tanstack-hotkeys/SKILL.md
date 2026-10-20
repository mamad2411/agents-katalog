---
name: follow-lib-tanstack-hotkeys
description: Use TanStack Hotkeys end to end — shortcuts, modifiers, sequences, scopes, recording
argument-hint: "[framework]"
related:
  - follow-lib-tanstack-ecosystem
  - run-test
  - resolve-errors
---

## Goal

Use TanStack Hotkeys fully — type-safe keyboard shortcuts: modifier combos, key sequences, scoped contexts, recording/user-remapping, key state tracking

## Scope

For keyboard shortcuts — command palette, navigation, editor actions — **0.x**: always check `https://tanstack.com/hotkeys/latest` before implementing

- part of TanStack ecosystem — selection/dispatch lives in `/follow-lib-tanstack-ecosystem`

## Execute

### 1. Install

> Goal: install the hotkeys package

```bash
bun add @tanstack/react-hotkeys   # framework adapters per project
```

### 2. Register Shortcuts

> Goal: hotkeys typed + declarative

```tsx
import { useHotkey } from '@tanstack/react-hotkeys'

useHotkey('Mod+K', () => setPaletteOpen(true))     // Mod = Cmd (mac) / Ctrl (others)
useHotkey('G>G', () => navigate('/top'))           // sequence: press g then g
useHotkey(['ArrowUp', 'K'], () => moveUp())        // aliases
useHotkey('Shift+?', () => setHelpOpen(true), { preventDefault: true })
```

- Modifiers: `Mod`, `Shift`, `Alt`, `Ctrl`, `Meta` — type-checked strings, a typo trips typecheck
- Options: `preventDefault`, `enabled` (conditional), `target` element, `ignoreInputs`

### 3. Scopes And Conflicts

> Goal: shortcuts respect context

1. `HotkeysProvider` scope boundaries — modal / editor / global kept separate; the innermost scope wins on duplicate keys
2. Editable elements — by default they don't trigger in input/textarea/contentEditable; `enableOnFormTags` when wanted
3. `useKeyHold`/`useKeyState` — key state tracking (press-and-hold patterns such as push-to-talk)
4. Recording UI: `useHotkeysRecorder`-style API — capture a key combo from the user for remapping (check the latest docs)

### 4. Patterns

> Goal: good shortcut UX

1. **Command palette** = the canonical use case — `Mod+K` palette + register commands through the same hotkeys
2. **Help overlay** — `Shift+?` shows the app's shortcut cheat sheet
3. **Conflict audit** — maintain a registry of all app shortcuts (code review checklist)
4. **Accessibility** — shortcuts supplement, never replace, pointer paths; document them in help

### 5. Verify

> Goal: prove shortcuts fire only in the right scope before finishing

1. `/run-test` — dispatch keydown events, assert handlers
2. Input contexts: no trigger while typing (unless intended)
3. Sequences: the timing window works, a partial sequence resets
4. On failure → `/resolve-errors` max 3 rounds

## Rules

- Use `Mod` instead of separate `Ctrl`/`Cmd` — cross-platform in one binding
- Avoid clashing with browser defaults (`Mod+T`, `Mod+W`, `Mod+N`) — override only when truly necessary
- Sequences max 2-3 keys — longer is bad UX
- 0.x API — pin the version; verify signatures against the latest docs
- Use `/follow-lib-tanstack-ecosystem` for library selection

## Expected Outcome

- Type-safe shortcuts covering all modifiers/sequences
- Scopes + input contexts behave correctly
- User-remappable hotkeys ready (if used)

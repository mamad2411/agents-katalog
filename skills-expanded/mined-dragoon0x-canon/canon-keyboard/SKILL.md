---
name: canon-keyboard
description: Use when designing or auditing keyboard navigation, focus management, shortcut keys, or keyboard-only workflows. Covers tab order, arrow keys within composite widgets, skip links, shortcut conventions, and ensuring every interaction works without a mouse. Trigger when the user mentions keyboard, tab order, shortcuts, hotkeys, focus order, or keyboard navigation.
---

# CANON · Keyboard

If it doesn't work with a keyboard, it doesn't work. Period.

## Tab order = visual order

Tab moves focus through interactive elements in document order. That order must match the visual layout. If CSS rearranges elements visually (flexbox `order`, grid placement, `position: absolute`), the tab order still follows DOM order. Fix the DOM, not the visual.

Never use `tabindex` > 0. It forces elements to the front of tab order globally and breaks the natural flow.

| tabindex value | Meaning |
|---|---|
| 0 | Focusable in natural order |
| -1 | Focusable only via JS (`.focus()`), not via Tab |
| > 0 | **Never use.** Forces unnatural order. |

## Interactive elements are natively focusable

`<button>`, `<a href>`, `<input>`, `<select>`, `<textarea>` — all keyboard-accessible by default. If you're adding `tabindex="0"` and `onKeyDown` to a `<div>`, you've reinvented a button badly.

## Composite widgets — arrow keys, not Tab

Inside a toolbar, tab bar, radio group, or menu, arrow keys move between items. Tab enters and exits the group. This is the **roving tabindex** or **aria-activedescendant** pattern.

| Widget | Internal navigation |
|---|---|
| Tabs | Arrow Left/Right (horizontal), Up/Down (vertical) |
| Menu | Arrow Up/Down, Enter to activate, Escape to close |
| Toolbar | Arrow Left/Right between buttons |
| Radio group | Arrow Up/Down or Left/Right |
| Tree view | Arrow Up/Down to traverse, Right to expand, Left to collapse |

## Keyboard shortcuts

- Document them. An undiscoverable shortcut is a non-shortcut.
- Use `⌘/Ctrl + letter` for common actions (⌘S save, ⌘K command palette).
- Don't override browser shortcuts (⌘L address bar, ⌘T new tab, ⌘W close tab).
- Use single-key shortcuts (like `?` for help) only in apps, not content pages (WCAG 2.1.4).
- Allow users to remap or disable shortcuts.

## Focus indicators

See `canon-focus` for visual specs. Key rule: every focused element must be visually distinguishable. `outline: none` without a replacement is an accessibility violation.

## Anti-patterns

| Anti-pattern | Why it fails |
|---|---|
| `tabindex` > 0 | Breaks global tab order |
| `<div onClick>` without keyboard handler | Keyboard users blocked |
| Overriding ⌘W, ⌘T, ⌘L | Hijacking browser |
| No skip link | Users Tab through entire nav on every page |
| Tab trapping outside of modals | Users stuck |
| Undocumented keyboard shortcuts | Undiscoverable |

## Audit checklist

- [ ] Every interactive element reachable via Tab (or arrow keys within composites)
- [ ] Tab order matches visual order
- [ ] No `tabindex` > 0
- [ ] Custom controls use `<button>` or proper ARIA + keyboard handlers
- [ ] Skip link on every page
- [ ] Keyboard shortcuts documented and non-conflicting with browser
- [ ] Modal focus traps work correctly (Tab cycles, Escape exits)
- [ ] Focus visible on every focused element

## Sources

- WCAG 2.2 · 2.1.1 Keyboard, 2.1.2 No Keyboard Trap, 2.1.4 Character Key Shortcuts, 2.4.3 Focus Order
- WAI-ARIA Authoring Practices · Keyboard interaction patterns
- Apple HIG · Keyboard support

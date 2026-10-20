---
name: a11y-keyboard-nav
description: Use when building a custom interactive widget in React that isn't a native input/button/link (dropdown, combobox, custom menu) — keyboard handlers for arrow keys, Enter/Space, Escape. Every interactive element must be operable without a mouse.
metadata:
  origin: community (decomposed from frontend-a11y)
allowed-tools: Read, Edit, Grep, Glob
---

# Keyboard navigation for custom widgets

If you can build it from a native `<button>`, `<a>`, `<select>`, or `<details>`, do that instead —
they get keyboard support for free. This skill is for when the widget's behavior (multi-option
listbox, combobox with filtering) genuinely needs a custom `role`.

## Custom dropdown/combobox

```tsx
export function Dropdown({ options, onSelect }: { options: string[]; onSelect: (value: string) => void }) {
  const [isOpen, setIsOpen] = useState(false);
  const [activeIndex, setActiveIndex] = useState(0);
  const listId = useId();

  if (!options.length) return null;

  const handleKeyDown = (e: React.KeyboardEvent) => {
    switch (e.key) {
      case 'ArrowDown':
        e.preventDefault();
        setActiveIndex((i) => Math.min(i + 1, options.length - 1));
        break;
      case 'ArrowUp':
        e.preventDefault();
        setActiveIndex((i) => Math.max(i - 1, 0));
        break;
      case 'Enter':
      case ' ':
        e.preventDefault();
        if (isOpen) onSelect(options[activeIndex]);
        setIsOpen((v) => !v);
        break;
      case 'Escape':
        setIsOpen(false);
        break;
    }
  };

  return (
    <div role="combobox" aria-expanded={isOpen} aria-haspopup="listbox" aria-controls={listId} tabIndex={0} onKeyDown={handleKeyDown} onClick={() => setIsOpen((v) => !v)}>
      <span>{options[activeIndex]}</span>
      {isOpen && (
        <ul id={listId} role="listbox">
          {options.map((option, index) => (
            <li key={option} role="option" aria-selected={index === activeIndex} onClick={() => { onSelect(option); setIsOpen(false); }}>
              {option}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
```

## Rules

- Anything with an `onClick` and a non-native role needs `tabIndex={0}` (to be reachable) and an
  `onKeyDown` handling at least `Enter`/`Space` (to be activatable) — a click handler alone only
  works for mouse/touch users.
- `Escape` should close/cancel any transient UI (dropdown, popover, non-modal panel) it opens.
- Never use a positive `tabIndex` — it reorders tab sequence independent of visual layout and
  becomes unmaintainable as the page grows. `0` (natural order) or `-1` (programmatic focus only)
  are the only values that scale.
- Arrow-key roving focus (as in the example) is expected for listbox/menu/tab-like widgets — plain
  Tab-per-item is the wrong model for those roles.

## Related

- `a11y-semantics-aria` — the ARIA attributes (`role`, `aria-expanded`, etc.) this widget needs
  alongside its keyboard handlers.
- `a11y-focus-management` — for widgets that also open/close a modal or move focus across the
  page (not just within themselves).

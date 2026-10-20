---
description: Buttons must include icons for better UX and visual consistency.
globs: "app/**/*.tsx, components/**/*.tsx"
alwaysApply: false
---

## Buttons require icons (mandatory)
- **ALL** buttons with text labels must include an icon from `lucide-react`.
- Icons should be sized with `size={16}` for standard buttons.
- Icons should be placed before the text with `gap-2` class on the button.
- Use `className="gap-2"` to space icon and text properly.

### Exceptions (icon-only buttons):
- Buttons with `size="icon"` variant (icon-only buttons) are exempt.
- Buttons that only show loading spinners during async operations are exempt (but should show icon when not loading).

### Examples:

#### Good (with icon):
```tsx
<Button onClick={handleSave} className="gap-2">
  <Save size={16} />
  Save Preferences
</Button>

<Button variant="outline" onClick={handleReset} className="gap-2">
  <RotateCcw size={16} />
  Reset to Defaults
</Button>
```

#### Bad (missing icon):
```tsx
<Button onClick={handleSave}>
  Save Preferences
</Button>
```

### Icon selection guidelines:
- Use semantically appropriate icons (e.g., `Save` for save, `RotateCcw` for reset, `Trash2` for delete, `X` for cancel, `Check` for done/confirm).
- For loading states, use `Loader2` with `animate-spin` class.
- Import icons from `lucide-react` at the top of the file.

---
description: Require title (or accessible name) on buttons, icon buttons, and icon-only controls so hover reveals their purpose
globs: chat-app-frontend/**/*.js, chat-app-frontend/**/*.tsx
alwaysApply: false
---

# Interactive Control Titles

Every clickable or icon-only control must expose a short, human-readable purpose on hover.

## Required

- Add a `title` attribute to buttons, icon buttons, icon-only links, and similar controls when the purpose is not already obvious from visible text alone.
- Prefer concise action phrases: `"Add member"`, `"Close"`, `"Remove from group"`, `"Send message"`.
- Icon-only controls **always** need a `title` (and preferably `aria-label` with the same text).
- When using MUI `IconButton`, `Button` with only an icon, or custom clickable icons, set `title` on the interactive element.

```jsx
// ❌ BAD — icon-only, no hover hint
<IconButton onClick={onClose}>
  <CloseIcon />
</IconButton>

// ✅ GOOD
<IconButton title="Close" aria-label="Close" onClick={onClose}>
  <CloseIcon />
</IconButton>
```

```jsx
// ❌ BAD — ambiguous icon action
<span onClick={onAdd}>
  <PersonAddIcon />
</span>

// ✅ GOOD
<button type="button" title="Add member" aria-label="Add member" onClick={onAdd}>
  <PersonAddIcon />
</button>
```

## Exceptions

- Controls whose **visible label already states the action** (e.g. `<Button>Save</Button>`) do not require a redundant `title`.
- Decorative, non-interactive icons do not need a `title`.
- If a MUI `Tooltip` already wraps the control with the same purpose text, do not duplicate a conflicting `title`; keep one clear hover label.

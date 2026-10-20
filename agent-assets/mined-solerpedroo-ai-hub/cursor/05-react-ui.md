---
description: React, Zustand, Tailwind/shadcn, i18n, keyboard-first desktop UI
globs: "**/*.{tsx,css}"
alwaysApply: false
---

# React UI

- Functional components + hooks. shadcn/ui + Tailwind only (no extra UI kit).
- Zustand stores small and feature-sliced. No god-store holding keys or raw streams of every chat.
- Density like Linear/Cursor. Empty states teach the next action (especially first-run).
- New copy: add **pt-BR and en** keys in the same change. Never hardcode UI strings.
- Keyboard: Enter send, Shift+Enter newline, `Ctrl/Cmd+K` palette when that wave exists. Primary flows work without a mouse.
- Receipts, health, and cost must not be color-only (text + color).
- Do not put API keys or unredacted errors in component state or DOM.

```tsx
// ❌
<button>Enviar</button>

// ✅
<button>{t("chat.send")}</button>
```

# Whiskeyjack Starter

**Read `AGENTS.md` in the project root first.** It is the canonical set of
conventions for this project – stack, structure, design-system rules, i18n,
copywriting, accessibility – and it is kept tool-neutral so every coding agent
works from the same instructions.

This file covers what is specific to Claude Code.

## Path-scoped rules

`.claude/rules/` loads automatically by path, and goes deeper than the summary
in `AGENTS.md`:

| Rule | Covers |
|------|--------|
| `whiskeyjack-app.md` | Design-system-first conventions, the app shell, theming, Tauri gating, the cold-launch theme flash |
| `accessibility.md` | WCAG 2.1 AA standards for new user-facing UI |
| `copywriting.md` | Dashes, contrastive negation, and UI copy generally |
| `code-comments.md` | Comments describe the code, never the history or process of a change |

## Agents

| Agent | Use for |
|-------|---------|
| `web-dev` | Implementing features, pages, and components (design-system first) |
| `reviewer` | Reviewing recent changes before you commit |
| `accessibility` | WCAG 2.1 AA review of new user-facing UI |

## Skills

| Command | Description |
|---------|-------------|
| `/add-i18n-key <key> ["value"]` | Add a translation key to every locale file in `src/i18n/locales/` |
| `/build` | Lint, type-check, and build the app |
| `/review` | Code review on recent changes via the `reviewer` agent |

## Finding a component

`components.json` registers the `@whiskeyjack` registry namespace, so the
shadcn CLI can search and install design-system components directly:

```bash
npx shadcn@latest search @whiskeyjack
npx shadcn@latest add @whiskeyjack/bottom-drawer
```

Prefer this over writing a component from scratch. `AGENTS.md` covers when to
copy a component in versus importing it from the package.

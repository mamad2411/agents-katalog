---
name: ladle
description: Ladle standards — CSF story format, args, .ladle/config.mjs, and Vite-based component development. Load when working with Ladle.
user-invocable: false
stack: component-docs/ladle
paths:
  - "**/*.stories.tsx"
  - "**/*.stories.ts"
  - "**/.ladle/**"
  - "**/ladle/**"
---

Full standards in [ladle.md](ladle.md). Always-on summary:

> **Scope — applies only if this project uses ladle.** This layer shares `**/*.stories.ts`, `**/*.stories.tsx` with `storybook` in `layers/component-docs/`, so more than one may load at once and their rules conflict. If the project is not using ladle, ignore this layer.
> See `docs/adr/0001-layer-glob-collision-and-dispatcher-routing-policy.md`.

**Story format (CSF):**
- Export a `meta` object as default with `{ title: 'Category/ComponentName' }`
- Each named export is a story: `export const Default: Story = { args: { label: 'Click me' } }`
- Use TypeScript: `type Story = StoryObj<typeof Button>` — gives you arg type inference

**Args:**
- Define `argTypes` in `meta` for controls (dropdowns, booleans, colour pickers)
- Set `args` at the story level to override component defaults without touching the source
- Use `render` override only when the default arg mapping is insufficient

**Configuration (.ladle/config.mjs):**
- Set `base`, `port`, `defaultStory`, and `addons` in `.ladle/config.mjs`
- Provide global decorators (providers, themes) in `.ladle/components.tsx` via `export const Provider`
- No separate Babel config needed — Ladle uses Vite natively

**Performance:**
- Ladle starts in milliseconds — do not add Babel transforms that bypass Vite's native ESM
- Colocate story files with components: `Button.stories.tsx` next to `Button.tsx`
- Share fixtures between stories and unit tests — define them in a `__fixtures__` file

**CI:**
- Run `ladle build` to produce a static site; deploy to S3 / Netlify / Vercel for visual review
- Use `@ladle/react` version that matches your React version — check peer deps after upgrades

**Never:**
- Put business logic in stories — stories are pure visual documentation
- Import from `src/` using long relative paths — configure Vite path aliases once in `vite.config.ts`
- Skip args in favour of hard-coded props — args enable interactive controls

**Related skills:** `component-docs/storybook` (Storybook alternative), `frontend/react` (React components), `testing/vitest`

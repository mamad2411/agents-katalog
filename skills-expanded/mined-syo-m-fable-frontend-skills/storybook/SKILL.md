---
name: storybook
description: Storybook conventions — CSF3 stories, play functions as Vitest component tests, decorators, a11y. Use when writing or editing *.stories.tsx or Storybook config, AND whenever asked to write tests for a component — stories with play functions are this repo's component-test layer. 日本語の依頼例:「Storybook/ストーリー書いて」「コンポーネントのテスト書いて」「play関数」「interaction test」。
---

# Storybook

Stories are the component-test layer: every story renders in the UI catalog AND runs as a Vitest browser-mode test via the Storybook Vitest addon. Write them as both documentation and test.

## CSF3 shape

```tsx
import type { Meta, StoryObj } from '@storybook/react'; // or framework package per installed SB version
import { expect, fn, userEvent, within } from 'storybook/test';
import { LoginForm } from './LoginForm';

const meta = {
  component: LoginForm,
  args: { onSubmit: fn() },          // fn() for every callback prop — assertable, visible in Actions panel
} satisfies Meta<typeof LoginForm>;
export default meta;

type Story = StoryObj<typeof meta>;
```

- Colocate: `LoginForm.tsx` + `LoginForm.stories.tsx`. `satisfies Meta<…>` + `StoryObj<typeof meta>` — full inference, no casts.
- Check installed Storybook major version before using version-specific imports (`storybook/test` vs `@storybook/test`).

## Which stories to write

- One story per meaningful state: default, empty, loading, error, edge content (long text, many items). Each renders without interaction → these are your visual states, and the VRT snapshot surface (see `visual-regression`).
- Plus interaction stories with `play` for each key behavior: submit success, validation error, keyboard operation.
- Vary stories via `args`, not copy-pasted render functions. Custom `render` only when composition is needed.

## Play functions

```tsx
export const ShowsValidationError: Story = {
  play: async ({ canvas, step, args }) => {
    await step('submit empty form', async () => {
      await userEvent.click(canvas.getByRole('button', { name: /log in/i }));
    });
    await step('shows error, does not submit', async () => {
      await expect(canvas.getByRole('alert')).toHaveTextContent(/required/i);
      await expect(args.onSubmit).not.toHaveBeenCalled();
    });
  },
};
```

- `await` every interaction and assertion — a missing await passes locally and flakes in CI.
- Same query rules as Testing Library: `getByRole` first (see `testing-vitest`).
- `step()` for multi-phase plays — failures pinpoint the phase.
- Assert outcomes: error visible AND callback not called; not just "no crash".
- Portals/modals render outside the canvas — query via `within(canvasElement.parentElement!)` or screen-level helpers.

## Decorators & data

- Global providers (theme, i18n, MemoryRouter) once in `.storybook/preview.tsx` decorators — never per-story copies.
- Network-dependent components: MSW (`msw-storybook-addon`), sharing handler definitions with Vitest tests. No fetch stubbing inside stories.
- A story requiring 30 lines of setup is telling you the component's dependencies are too broad.

## Running as tests

- The Vitest addon turns every story into a test (render check) and runs `play` functions in a real browser (Playwright provider) — keep `npm run test` covering them in CI.
- Pin the React runtime (and any animation lib) in the Storybook test project's `optimizeDeps.include`: `react`, `react-dom`, `react-dom/client`, `react/jsx-runtime`, `react/jsx-dev-runtime`, plus e.g. `motion/react`. Otherwise Vite discovers a dep mid-run, re-optimizes, and reloads the page — the play function then queries an unmounted tree: an intermittent "unable to find element" that often only shows in CI. The `[vitest] Vite unexpectedly reloaded a test` warning is the tell.
- A story that can't pass headlessly (depends on viewport quirks, real network) is broken — fix the story, don't exclude it.
- Plays that follow an animation (modal close, exit transitions) assert post-animation state with auto-retrying queries (`findBy*`, retried `expect`) — do NOT disable animations or emulate reduced motion in interaction tests; that executes a different motion code path than users get. Animations-off belongs to VRT only (see `visual-regression`).
- Reuse stories in plain Vitest tests with `composeStories` when you need extra assertions beyond the play function.

## A11y

- Keep `@storybook/addon-a11y` enabled with serious/critical violations failing the test run (same threshold as the Playwright axe gate), not just warnings in the panel. Fix or explicitly (with reason) disable specific rules per story — never globally.

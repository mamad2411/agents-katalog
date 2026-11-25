---
name: gamut-repo-testing
description: Use this skill when writing, fixing, or migrating tests inside this repo — deciding whether a case belongs in a story `play` or a unit test, writing `play` functions, moving a `*.test.tsx` into stories, or placing test and story files.
---

# Gamut Repo Testing

How tests are written inside skillsoft-gamut. Stories run as tests in a real browser through Storybook's `addon-vitest`, with an axe a11y check after each story. Unit tests run in the same root `vitest.config.ts` workspace: the `jsdom` project for component, hook, and style packages, and the `node` project for Node tooling (ESLint rules, codemods, CLIs).

For `setupRtl`, harnesses, and `MockGamutProvider`, read the shipped [`gamut-testing`](../../../packages/gamut-agent-tools/skills/gamut-testing/SKILL.md) skill. That one is written for apps that consume Gamut. This one covers the conventions for Gamut's own tests.

---

## Where a test goes: `play` or unit test

Behavior a user can see or do belongs in a story `play`. Contracts the DOM can't show belong in a unit test.

| What you're asserting                                                                                  | Where                                                   |
| ------------------------------------------------------------------------------------------------------ | ------------------------------------------------------- |
| Rendered content, roles, accessible names, `aria-*` overrides                                          | `play`                                                  |
| Interactions: click, type, keyboard, hover, focus, and the callbacks they fire (`fn()` spies)          | `play`                                                  |
| Overlays opening and closing (Dialog, Modal, Popover, Menu, tooltips), focus trapping and focus return | `play`                                                  |
| Geometry: positioning, offsets, scroll behavior (`getBoundingClientRect` needs real layout)            | `play`                                                  |
| RTL behavior                                                                                           | `play` with `globals: { direction: 'rtl' }`             |
| A visual state with nothing to interact with                                                           | Story with no `play` (a11y still runs)                  |
| Ref forwarding, imperative handles (`ref.current.focus()`, exposed methods)                            | Unit test                                               |
| Hooks, pure functions, utilities, reducers                                                             | Unit test                                               |
| Colors, spacing, class names, raw CSS                                                                  | Neither: drop it. Visual regression and a11y cover this |

A component made only of styling (like `Text`) gets stories and no unit test. When a unit test is still needed, keep it to the contracts in the unit-test rows above.

### Granularity

A story is one rendered state; its `play` drives interactions and asserts on them. Aim for about 3–7 stories per component, not one story per old `it()`. Group related flows in one `play`: a single `Dismissal` story can exercise confirm, cancel, the close button, inside-click, and Escape, reopening between each.

### Migrating a unit test into stories

1. List every `it()` in the `*.test.tsx`.
2. Port every behavioral case into a story `play`: hover reveals, focus, `aria-label` overrides, click handlers, close paths. Only pure style assertions may be dropped; name each one you drop in your summary.
3. Keep the component's existing demo stories, converted to the conventions below.
4. Move ref and imperative contracts into a co-located `<Component>.test.tsx`.
5. Delete the old test once every `it()` maps to a story or a remaining unit test.

---

## File layout

Co-locate everything next to the component source:

```text
packages/gamut/src/Modals/
  Dialog.tsx
  Dialog.stories.tsx
  Dialog.test.tsx
```

- Name tests `<Component>.test.tsx` and stories `<Component>.stories.tsx`, beside the source, never in a `__tests__/` folder.
- Import with relative paths (`./Dialog`, `../Box`). A self-import of `@skillsoft/gamut` from inside the package fails the `import-paths` lint rule. Import argTypes and blocks from `~storybook/*`.
- Put example components and data the stories need inside the `.stories.tsx` file. A separate helper file gets swept into the library build.
- A package that gains its first co-located story needs `**/*.stories.{ts,tsx,js,jsx}` in its `tsconfig.lib.json` `exclude`, and a `directory` entry in `packages/.storybook/main.ts`.

---

## Writing test and story files

- Add no comments of your own to test or story files (no file headers, no JSDoc on stories, no inline notes in `it` or `play` bodies); let names and code carry intent. Leave comments people have written in place.
- Assert presence with a bare query, and absence with `toBeNull()`. This applies to `view`, `canvas`, and `screen`, and to every `getBy*`/`queryBy*` variant:

```tsx
view.getByRole('button', { name: 'Save' });
expect(view.queryByRole('dialog')).toBeNull();
```

---

## Story `play` functions

```tsx
import type { Meta, StoryObj } from '@storybook/react';
import { useState } from 'react';
import { expect, fn, screen, waitFor } from 'storybook/test';

import { FillButton } from '../Button';
import { Dialog } from './Dialog';

const meta: Meta<typeof Dialog> = {
  title: 'Molecules/Modals/Dialog',
  component: Dialog,
  args: {
    title: 'Delete file',
    children: 'This cannot be undone.',
    confirmCta: { children: 'Delete' },
    onRequestClose: fn(),
  },
  render: function DialogWithTrigger(args) {
    const [isOpen, setIsOpen] = useState(false);
    return (
      <>
        <FillButton onClick={() => setIsOpen(true)}>Open dialog</FillButton>
        <Dialog
          {...args}
          isOpen={isOpen}
          onRequestClose={() => {
            setIsOpen(false);
            args.onRequestClose();
          }}
        />
      </>
    );
  },
};

export default meta;
type Story = StoryObj<typeof Dialog>;

const openDialog: NonNullable<Story['play']> = async ({
  canvas,
  userEvent,
}) => {
  await userEvent.click(canvas.getByRole('button', { name: 'Open dialog' }));
  await screen.findByRole('dialog');
};

export const Dismissal: Story = {
  play: async (context) => {
    const { args, userEvent } = context;
    await openDialog(context);
    await userEvent.keyboard('{Escape}');
    await waitFor(() => expect(screen.queryByRole('dialog')).toBeNull());
    await expect(args.onRequestClose).toHaveBeenCalledTimes(1);
  },
};
```

### Queries: `canvas` by default, `screen` for floating elements

- Query with `canvas` from the play context. It is scoped to the story's own DOM.
- Use `screen` only for elements portaled to the end of `<body>`: dialogs, modals, popovers, menus, tooltips, floating tips. The trigger that opens them is still in the canvas, so click it through `canvas` and query the overlay through `screen` (see `openDialog` above).

### Imports and context

- Import `expect`, `fn`, `waitFor`, and `screen` from `storybook/test`.
- Destructure `canvas` and `userEvent` from the play context; skip a manual `within(canvasElement)` or a separate `userEvent` import.
- A `play` with no `await` is a plain function, not `async`, or `@typescript-eslint/require-await` fails:

```tsx
play: ({ canvas }) => {
  canvas.getByRole('link', { name: 'Docs' });
},
```

### Overlays

Render overlays closed behind a trigger button and let `play` click them open. The Docs page renders every story stacked and doesn't run `play`, so stories with `isOpen: true` in args stack open overlays over each other. a11y runs after `play`, so it still checks the open overlay. Even a story that only shows an open state carries a `play` that opens it.

Wire the render's close handler to both local state and the `args` spy, so the overlay really closes when clicked by hand in Storybook and the spy still records the call.

A story's `play` replaces the meta's `play` rather than composing with it. When `meta.play` opens the overlay, a story with its own `play` calls the open helper itself.

### Spies

`fn()` spies in `meta.args` reset between stories. Within one `play`, assert a spy's count right after the action that fires it: several close paths (Escape, the close button, the cancel CTA) can route through the same handler, so a count checked at the end is off.

### File order

Imports, then `meta`, `export default meta`, and `type Story`, then helpers (play helpers, example components, data), then stories. Anything `meta` references while it is evaluated (such as `play: openDialog`) stays above `meta`, because `const` isn't hoisted.

### Args and render

- Write a `render` as an inline named function (`render: function DialogWithTrigger(args) {...}`) so "Show code" shows real usage and hooks lint passes.
- Pass JSX children through a story-level `render`, not `args.children`. JSX in args throws "cycle in arg" with deep controls.
- Add an `argTypes` entry only when inference can't do the job (a `mapping` select, a disabled control, a custom description). When you add one, set `table.type.summary` to the valid values and `table.defaultValue.summary` to the component's default, not the story's. Take `options` from a runtime export when the component has one, otherwise from a plain `as const` array in the story.

---

## Unit tests

Use `setupRtl` from `@skillsoft/gamut-tests`, defined once per file. Keep the file to the contracts a `play` can't reach. Vitest globals are off, so import `describe`, `it`, `expect`, and `vi` from `vitest`:

```tsx
import { setupRtl } from '@skillsoft/gamut-tests';
import * as React from 'react';
import { describe, expect, it, vi } from 'vitest';

import { Dialog } from './Dialog';

const renderView = setupRtl(Dialog, {
  isOpen: true,
  title: 'Hello world',
  children: 'Close me please',
  confirmCta: { children: 'Confirm' },
  onRequestClose: vi.fn(),
});

describe('Dialog', () => {
  it('forwards containerFocusRef to the dialog container', () => {
    const containerFocusRef = React.createRef<HTMLDivElement>();
    const { view } = renderView({ containerFocusRef });

    expect(containerFocusRef.current).toBe(view.getByRole('dialog'));
  });
});
```

---

## Running

Run these from the repo root on Node 22.22.2. Vitest's story globs and eslint's `tsconfig.json` lookup both break from another directory.

| What                                           | Command                                                     |
| ---------------------------------------------- | ----------------------------------------------------------- |
| Stories, filtered by path                      | `yarn test:stories <path filter>`                           |
| Stories, watch mode                            | `yarn test:stories:watch <path filter>`                     |
| Unit tests, filtered by path                   | `yarn vitest run --project=jsdom <path filter>` (or `node`) |
| Unit tests, watch mode                         | `yarn test:watch <path filter>`                             |
| Every test, building the tested packages first | `yarn test`                                                 |
| Lint the files you touched                     | `node_modules/.bin/eslint <files>`                          |

Unit tests load other packages in this repo from their built `dist`, not their source: a test in `packages/gamut` that imports `@skillsoft/gamut-styles` gets `packages/gamut-styles/dist`. `yarn test` builds every tested package first; a filtered `yarn vitest run` does not. After editing a package that another package imports, build it (`yarn nx build <package>`) or run `yarn test` before trusting a filtered run.

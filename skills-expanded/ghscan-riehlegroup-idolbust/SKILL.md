---
name: storybook-component
description: Create, review, and edit components in the component library, the design system, and storybook
license: MIT
compatibility: opencode
---

## What I do

- Create new components in the component library, design system, and storybook in a consistent way
- Review existing component library, design system, and storybook for consistency and best practices
- Update existing component library, design system, and storybook in a consistent way

## When to use me

Use this skill for any Storybook-related work in this repo, including:

- Reviewing the component library or Storybook setup for best practices.
- Auditing story coverage, controls, docs, or interactions.
- Creating or editing components and their stories in `src/components`.

If the user asks to “review the component library in terms of Storybook best practices,” load this skill.

## Domain knowledge: Storybook basics

- A story is a focused, deterministic example of a component state.
- Stories should be isolated from app routing, API calls, and global state.
- Prefer args/controls over hard-coded props to keep stories interactive.
- Favor realistic content and edge cases (long strings, empty states, errors).
- Use `parameters` for layout, backgrounds, and viewport-specific cases.
- Keep stories fast: avoid heavy network requests or long-running effects.

## Best practices

- One component per story file, co-located with the component.
- Export a single `meta` default (or `export default`) and named stories.
- Use concise story names that reflect the user-facing state.
- Keep stories deterministic (no random data without a seeded generator).
- Use `argTypes` for clear control labels and documentation.
- Avoid coupling stories to app-specific context unless the component requires it.
- Prefer minimal decorators; if needed, document why they exist.
- Interaction tests should include at least one assertion so failures are meaningful; use them for behaviors, not purely visual states.
- Add play functions when user interactions change the UI, trigger callbacks, or guard accessibility flows; skip for static-only components.
- For links in play functions, prevent default navigation before clicking to avoid browser disconnects during Vitest runs.

## Repo-specific conventions

- Components live in `src/components` following atoms/molecules/organisms/templates.
- Use kebab-case filenames and PascalCase component names.
- Keep stories alongside components as `*.stories.tsx` or `*.stories.astro`.
- If a component has a separate types file, place it in the same folder and export
  types via the local barrel `index.ts`.
- For story files, imports that target the same component folder must be relative
  (e.g. `./Navbar`, `./Navbar.types`).
- Use the `@/` alias for imports outside the current component folder.
- Do not import from `src/pages` or `src/layouts` in stories.
- Always set `parameters.docs.description.component` with a concise usage note for every component story.

## Standard workflow

1. Create or update the component in `src/components/...`.
2. Add or update the story file in the same folder.
3. If new props or types are added, update the local `index.ts` barrel.
4. Verify stories render in Storybook and controls behave as expected.

## Story templates

### React/TSX story

```ts
import type { Meta, StoryObj } from "@storybook/react";
import { Button } from "./Button";

const meta: Meta<typeof Button> = {
  title: "Atoms/Button",
  component: Button,
  args: {
    label: "Click me",
    variant: "primary",
  },
};

export default meta;
type Story = StoryObj<typeof Button>;

export const Default: Story = {};
```

### Astro story (when using `.astro` components)

```ts
import type { Meta, StoryObj } from "@storybook/astro";
import { Hero } from "./Hero";

const meta: Meta<typeof Hero> = {
  title: "Organisms/Hero",
  component: Hero,
  args: {
    title: "Research that ships",
    subtitle: "A short, descriptive subtitle",
  },
  parameters: {
    layout: "fullscreen",
  },
};

export default meta;
type Story = StoryObj<typeof Hero>;

export const Default: Story = {};
```

---
name: storybook
description: Scaffold storybook config (.storybook/main.ts, preview.ts) plus auto-generated *.stories.tsx files for every PascalCase component in the codebase that has a matching named export. Caps at 50 components per run. dragoon does NOT install storybook - run `npx storybook init` after. Use to bootstrap stories quickly across an existing component library. Run as `node ~/.claude/skills/dragoon/skills/storybook/scripts/storybook.js`.
version: 1.0.0
---

# /storybook

Auto-generates a story for every component, plus storybook config.

## When to use

- Setting up storybook for the first time
- Backfilling stories for an existing component library
- The user says "add storybook", "scaffold stories"

## Run it

```
dragoon storybook            # preview
dragoon storybook --apply    # write stories for every component
```

## Then

```
npm i -D @storybook/react-vite @storybook/react @storybook/addon-essentials
npx storybook init
npm run storybook
```

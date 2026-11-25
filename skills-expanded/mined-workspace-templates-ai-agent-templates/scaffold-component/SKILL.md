---
name: scaffold-component
description: Creates a new UI component with props, styles, a test and a story, copying the folder layout your project already uses.
disable-model-invocation: true
---

Scaffold a component named and described by: $ARGUMENTS

1. Find two or three existing components of similar size (`Glob` for `*.tsx`, `*.vue`, `*.svelte`). Note the folder layout, naming case, styling approach (CSS modules, Tailwind, styled), prop typing, and how tests and stories are named.
2. If the name collides with an existing component, stop and ask.
3. Create the folder and files exactly as the neighbors do: component, styles, test, story, and an index export if siblings have one.
4. Type the props with sensible defaults, forward `className` and refs when siblings do, and use semantic elements with labels for anything interactive.
5. The test renders the component, checks one default case and one prop variation. The story shows each variant.
6. Run the project's lint, type check and the new test only.

List the files created and the commands that passed. Do not modify existing components; if a shared file needs a change, show the diff and ask first.

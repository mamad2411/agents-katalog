---
name: pointcut-edits
description: >-
  Conventions for applying a Pointcut design-edit handoff in THIS Svelte + Vite
  example. Use whenever a prompt describes a visual/style/copy change to a DOM
  element (button, card, heading, list, etc.) and references a
  data-pointcut-loc / file:line:col target, or asks to restyle/recolor/resize/
  reword something on the page. Demonstrates that a project-level skill is picked
  up by the agent Pointcut spawns at this project's root.
---

# Applying Pointcut edits — Svelte + Vite example

A Pointcut handoff resolves into the component **`src/App.svelte`** — markup and
styles both live there.

## Where things live
- Markup is the component body (`<main>`, `<h1>`, `<button>`, `<li>`, …),
  including the `{#each}` block for the list.
- Styles are in the component's `<style>` block, which is **scoped to this
  component** by Svelte — selectors here only affect this file's elements.
- Classes in use: `page`, `title`, `lede`, `card`, `cta`, `cta.ghost`, `list`.

## How to apply a change
- **Restyle an element** → edit its rule in the `<style>` block. Because styles
  are scoped, you can adjust freely without leaking to other components.
- **Markup / structural tweaks** → edit the component body.
- **Copy changes** → edit the text in place; keep inline `<strong>` intact.

## Don'ts
- Don't move styles to a global stylesheet — keep them in the scoped `<style>`
  block unless the handoff explicitly asks for shared/global styles.
- Don't touch `data-pointcut-loc` attributes (injected by the Source Stamp).
- Keep edits scoped to the element the handoff points at.

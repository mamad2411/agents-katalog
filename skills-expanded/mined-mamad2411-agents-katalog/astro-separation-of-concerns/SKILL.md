---
name: astro-separation-of-concerns
description: Use when creating or editing any .astro component — enforces splitting markup, styles, script, and types into separate files instead of one large inline .astro file. Triggers on "componente astro", "separa responsabilidades", "buenas practicas astro", or any non-trivial .astro file (interactive component, >~80 lines, has both <style> and <script>).
allowed-tools: Read, Edit, Grep, Glob
---

# Astro: Separation of Concerns

A `.astro` file with a big inline `<style>` block and a big inline `<script>` block becomes unmaintainable fast — nobody wants to scroll 400 lines to find one selector or one event handler. Split it like any other component.

## Structure per component

For a component `Foo`, use a folder, not a single file:

```
src/components/foo/
  Foo.astro       — markup + props/frontmatter logic only
  Foo.css         — all styles, root-scoped under one wrapper class
  foo.client.ts   — all client-side JS/TS (interactivity)
  types.ts        — shared interfaces/types used by the component and its data
```

## Rules

1. **Foo.astro holds markup only.** Frontmatter (`---`) is for props typing, data shaping, and template logic (`.map()`, conditionals) — not for styling or DOM event wiring.
2. **Styles go in Foo.css, imported at the top of the frontmatter** (`import './Foo.css'`). Since external CSS imports are NOT auto-scoped by Astro (only inline `<style>` is), wrap the component's root markup in one class (e.g. `.foo`) and prefix every selector in the CSS file under it, so nothing leaks globally.
3. **Script goes in foo.client.ts, referenced via `<script src="./foo.client.ts"></script>`** at the bottom of the template — not inlined. Type DOM lookups properly (`as HTMLElement`, etc.) since it runs through Astro's TS pipeline.
4. **Shared types** (props shape, data shape consumed from content collections) go in `types.ts` and get imported by both the `.astro` frontmatter and content schema / `.client.ts` where relevant — don't redeclare the same interface twice.
5. **Data stays out of the script file.** If the client script needs page data (e.g. a lookup table), pass it via a `<script type="application/json">` tag populated from the frontmatter and parsed in `foo.client.ts` — don't hardcode content into the script.
6. Keep the same rule for any nested pieces: if a sub-part (e.g. a modal) grows past ~40 lines of markup, it can become its own `.astro` file imported by the parent, still following the same split.

Apply this from the start when scaffolding a new component — don't write everything inline "for now" and plan to refactor later.

---
name: artifact-design
description: OUTPUT IS ALWAYS A SINGLE `.html` FILE (never `.md`, never Figma exports) showing design primitives next to their source code. Use this skill whenever the user asks for a design system page, design tokens reference, component variants sheet, "show all the buttons", "all states of the card component", "swatch the palette", living style guide, brand kit, or any artifact whose primary shape is "rendered components paired with their source / spec". Pair with `artifact-css` for the underlying design system. Do NOT use for one-off feature mockups (use `artifact-flow`) or for animation playgrounds (use `artifact-sandbox`).
---

# artifact-design

> ## OUTPUT CONTRACT
>
> **Produces ONE `.html` file.** A design system page is a Storybook-lite: each primitive renders live, paired with its source code, paired with notes on when to use it. All in one file.
>
> File extension is `.html`. File name typically `design-system.html` or `<component>-variants.html`.

---

A living design system page or component-variants sheet. Renders the primitives, lists their variants, shows their source, and documents when each variant applies — all in one self-contained `.html`.

Read `artifact-css/SKILL.md` first for the OUTPUT CONTRACT, design tokens, and class vocabulary. This skill uses **no jQuery** — design pages are static.

## When to reach for this skill

- User says "show me all the buttons", "every state of the card", "the full palette", "design system snapshot".
- User wants something a designer / engineer can scan to see all available primitives at once.
- User wants a single-file brand kit they can ship to a contractor.

If they want one big diagram of the architecture, use `artifact-diagram`. If they want a slide deck of design directions, use `artifact-deck` (or `artifact-plan/comparison-sheet` if they want to weigh options).

## Two templates

| Template | Use when |
|---|---|
| `templates/design-system.html` | Full design system: palette · type ramp · spacing · all primitives. Lives on a wiki, gets updated quarterly. |
| `templates/component-variants.html` | One component, all its variants (e.g., every state of `.button`, every shape of `.note`). Lives in a PR or design doc. |

## Anatomy of a design-system page

Eight sections. Use this order.

1. **Header** — eyebrow + product name + lead about who owns this and when it was last updated.
2. **Palette** — color swatches with hex codes and CSS-var names. Show light + dark if dark exists.
3. **Type ramp** — h1 → h4 + body + lead + small + tiny + mono rendered with their sizes/weights labelled.
4. **Spacing scale** — visual bars at each token size (4 / 8 / 12 / 16 / 24 / 32 / 48 / 64).
5. **Radii** — visual squares at each radius (xs / sm / md / lg / pill).
6. **Primitives** — every component the system ships, each rendered live with: name, code snippet, when-to-use note.
7. **Patterns** — common compositions (e.g., "stat strip + sec-head", "panel with kv-strip inside"). Two or three.
8. **Voice & density rules** — short prose from the system's authority document.

## Anatomy of a component-variants sheet

Smaller, focused. Five blocks.

1. **Header** — component name + lead on its purpose.
2. **Default variant** — rendered + code.
3. **Variants grid** — every modifier (state, size, color), rendered + code per cell.
4. **Anatomy diagram** — labelled SVG (or labelled HTML) showing the component's named parts.
5. **When-to-use / when-not** — `.grid-2` panels.

## The render-next-to-source pattern

Every primitive entry follows this shape:

```html
<div class="ds-entry">
  <div class="ds-render">
    <span class="badge badge-clay">draft</span>
  </div>
  <pre class="code-block"><code>&lt;span class="badge badge-clay"&gt;draft&lt;/span&gt;</code></pre>
  <p class="muted small">Use for in-progress / proposed states.</p>
</div>
```

The render is the source of truth. The code shown matches the live render byte-for-byte. If the rendered example uses extra classes or attributes, those go in the code too.

## Voice and density rules

1. **Show every variant.** A "design system" that documents three of seven button states is misleading. Either show them all or call them out as "TBD".
2. **Real examples, not placeholder.** `<button class="button">Submit</button>` beats `<button class="button">Button</button>`. Use the verb the user will actually see.
3. **Link the rule to the render.** Each entry has a one-liner explaining when to reach for it. No silent variants.
4. **Source matches render.** If the code says `class="button"` but the render uses `class="button button-primary"`, you've lied. Audit before shipping.
5. **No abstract names.** Variants named `.button-x1` / `.button-x2` are unreviewable. Use semantic names (`.button-primary` / `.button-ghost`).

## Common mistakes

- **Token table without the tokens rendered.** Listing `--clay: #D97757` is not enough. Show a swatch. The reader can't see hex codes.
- **Type ramp at default body size.** A type ramp that renders every step at the same visual size is decorative, not documentary. Use the actual sizes.
- **Components without spacing/radius reference.** The reader scrolls back and forth trying to find which radius value the card uses. Annotate.
- **Sample code in `<pre>` only.** Without `<code>` inside `<pre>`, copy-paste loses syntax highlighting and indentation hints.

## Fallback contract

No JS required. The page is static.

## After the artifact

Offer two derivatives:
1. A copy-ready inline-only `<style>` block extracted from the system, useful for a new contractor.
2. A one-page PDF print (via the page's print CSS) — design systems get printed for kickoff meetings.

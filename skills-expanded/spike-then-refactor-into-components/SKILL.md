---
name: spike-then-refactor-into-components
description: The Lossless Group's rhythm for building UI with coding agents — spike new features, pages and redesigns freely without the design system (component library and theme), then refactor the approved spike back into components (Component-Driven Architecture) and back onto the theme's tokens, and catalog them on /design-system. Use when starting any new page, feature, section, redesign or design variant (to make the gametime decision whether to use the component library); when a spike has been approved and needs refactoring; when assigning an agent to refactor a spike; when someone asks "should I use the existing components?"; or when knot-check reports open spikes or uncatalogued components. Encodes the decision rule, the @spike marker, the behavior-locking refactor procedure, how to hand a refactor to a separate agent, and the anti-patterns.
---

# Spike, then refactor into components

Coding agents are **faster and better** at building new features, pages and UI
when they aren't thinking about the existing component library. Holding a
library in mind while being creative pulls every new idea toward what already
exists. So we let creative work break free of the library, and then **refactor
it back into the library** once it's approved.

The design system has two halves, and a spike breaks free of both: the
**component library** (it builds its own markup) and the **theme** (it
hard-codes colors, fonts, spacing and effects). The refactor brings it back
into both.

The second half is the discipline. Most developers forget it, and the team
pays later: one-off markup everywhere, the same card built four ways, a theme
change that has to be made in twelve files, and a `/design-system` page that
no longer describes the site.

## 1. Make the gametime decision, out loud

Before writing UI, decide whether to use the component library, and say so in
one line ("Spiking this freely; refactor after approval" or "Building from the
library: Card, SectionHeader").

| Use the library | Break free (spike) |
|---|---|
| Extending a pattern the site already has | The emphasis is to be creative: a new page, a new feature, a redesign, design variants |
| A small change to an existing page | The library would steer the idea toward what exists |
| Consistency is the point (a new entry in a list, another pricing tier) | Exploring several directions before anyone picks one |
| A component exists that fits without contortion | Fitting it would need props or variants nobody has wanted before |

When unsure and the work is visible to a stakeholder, spike. A spike that gets
approved is cheap to refactor; a library-bound build that misses the brief is
expensive to redo.

## 2. Spike freely, and mark it

Write it the fastest clear way: inline markup, local styles, hard-coded
content. Still follow the hard rules (Astro and Svelte only, no React or JSX
habits, semantic tokens in styles where you can). Mark every file the spike
created or reshaped, so the refactor can't be forgotten:

```astro
---
// @spike pricing-page: refactor into components once approved
---
```

In a `.svelte` file or template: `<!-- @spike pricing-page: refactor into components once approved -->`.

`knot-check components` lists every open `@spike`, so the debt stays visible.

## 3. Refactor once it's approved, not before

Refactoring a spike nobody has signed off on is wasted work: it may be thrown
away. Refactoring one that has been live for months means it has already been
copied. The moment is **right after approval**, as its own task.

### The procedure (Component-Driven Architecture)

1. **Lock the behavior first.** Write a Vitest test that renders the spike
   page with Astro's Container API and snapshots the HTML (and a test per
   interactive behavior). The refactor must not change what the page shows.
2. **Read the library and the catalog.** `src/components/` and
   `/design-system`. List each unit in the spike: repeated markup, sections,
   anything with its own styles or behavior.
3. **Reuse before you create.** For each unit: an existing component that fits
   → use it. One that almost fits → add a variant or prop to it. Nothing
   close → a new component. Never make a near-duplicate of an existing one.
4. **Extract bottom-up.** Small pieces first (buttons, badges, cards), then
   sections, then the page becomes composition. Content becomes props or data
   files (YAML or markdown for anything a client edits), never hard-coded in
   the component.
5. **Refactor back onto the theme.** Every hard-coded color, font, and
   one-off shadow or glow from the spike goes into `theme.css`: a value the
   theme already has → use its semantic token; a genuinely new one → add a
   named token at the top (`--color__sienna`, `--font__newsreader`) and point a
   semantic token at it (`--color-accent: var(--color__sienna)`), defined for
   light, dark **and** vibrant. Components only ever read semantic tokens
   (see `theme-system`). A new brand-level value goes on `/brand-kit` first.
   `knot-check components` lists every raw color and font left outside the
   theme files.
6. **Catalog in the same change.** Every new or changed component gets its
   `/design-system` entry (see `maintain-design-system-page`).
7. **Prove nothing moved.** The snapshot test passes, or every difference is
   reviewed and intended. Add a test per new component. Run `knot-check`.
8. **Close the spike.** Remove the `@spike` markers and add a `changelog/`
   entry naming the components that came out of it.

## 4. Hand the refactor to its own agent

The refactor is a good task to delegate: the spike is approved, the target is
clear ("same page, built from components, cataloged"), and success is
checkable. Give the agent:

- the spike's files (or "everything marked `@spike <name>`"),
- the rule: **no visible change**, behavior locked by tests first,
- this skill and `maintain-design-system-page`.

**Claude Code:** the Astro Knots plugin includes a `component-refactorer`
agent for exactly this. **Codex:** start a separate task with the brief above.
Run it on its own branch or worktree, one agent per spike, so a refactor
never collides with the next spike being built.

## Anti-patterns

- **Never refactoring.** The spike ships and stays a spike. This is the
  failure that slows the team down later.
- **Refactoring before approval.** Effort spent on something that may be thrown away.
- **Forcing the library onto creative work.** Slower, and the result looks
  like everything else.
- **A new component that duplicates an existing one** with small differences,
  instead of a variant.
- **One giant component** that is the whole page with a new name.
- **Extracting components but leaving their colors hard-coded.** They look
  right in one mode and wrong in the other two, and the next brand change has
  to find them one by one.
- **Refactoring without locking behavior first**, then finding out from a
  stakeholder that something moved.

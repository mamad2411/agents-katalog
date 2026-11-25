---
name: delibra-codebase
description: >
  Fill a DeLibra libra from a source-code folder. Run after ENGINE_SKILL
  Router step 4. Triggers: codebase folder, scan-codebase, components from
  code, design.source codebase.
---

# Fill a libra from a codebase

Read [ENGINE_SKILL.md](ENGINE_SKILL.md) first — Onboarding, Router, Intake.
This file is only the codebase path. Do not invent tokens or components that
are not in the folder.

A **component** is a named unit of UI that repeats. Evidence of repetition
stacks: a file of stories, an import graph, a class or custom tag that recurs
in templates. One candidate collects every signal. Tiers do not replace each
other.

## Order of work

1. **Theme first, whole.** Colours, type scale, spacing, shadows, radii —
   every literal you can read from a theme file or a variables file. Map
   them into `tokens.css` and `token-map.json` using
   [Writing tokens](ENGINE_SKILL.md#writing-tokens). Catalogue-only names
   go in `tokens.deferred.json`. Do not invent a value because the catalogue
   looks thin. A theme **table** of literals (a type scale, a grid, named
   shadows) is source; a theme **function** that only yields a computed
   colour is not — stop on that colour, as below.
2. Run `node tools/scan-codebase.js` on each root in
   `manifest.design.codebase`. A string is one root with role `layer`. A
   list of `{ "path", "role": "layer"|"base" }` is many roots. Prefer
   `--json` when a machine will consume the list. The scanner writes nothing
   to the libra. Read the **summary first**: how many files, which extensions,
   `cannot scan` lines — those counts are for the scan target, not the whole
   workspace. An empty list without that summary is a bug — stop and
   say so. Then read candidates from the top. Rows marked `[base]` come from
   a resolved dependency; uses are counted in the consuming tree. Print the
   resolved path from the scan before you decide to document that system.
3. **Whose layer?** If the scan lists a **base** package, or a notable share
   of candidates import an external UI package, stop and ask Intake question
   4 before any section. Three answers: this repository's layer; the system
   underneath; **or both** (two section groups, layer on top of base).
   Without an answer, do not write `sections.json`. The libra **title** and
   **description** must match the layer you actually document — do not name
   the product for a base system and then fill only the overlay.
4. Walk evidence in this order. If a tier is empty, go to the next — do not
   invent names to fill the gap.
   1. **Declared.** A file of stories next to a component (`stories:<n>` on
      that row). Read those stories first: they are the examples.
   2. **Imported.** The import graph: PascalCase JSX, a one-file component,
      a decorator with `selector` and `styleUrls`, a registered custom
      element. Hooks (`use*`) and type-only exports are not components.
      Usages in a monorepo count across workspace packages.
   3. **Repeated in markup.** A class or custom tag that appears in more than
      one template **and** has a rule **defined in this folder's CSS**. Not
      an imported stylesheet, not a utility class (`flex`, `mt-4`,
      `container`). Prefer compound names (block-element-modifier) and custom
      tags. If the scanner did not walk a template language (`cannot scan`),
      do this pass by hand with the same rule.
5. Add **Primitives** first, then **Blocks** built from those primitives.
6. **CSS in JS is two different cases — do not mix them:**
   - **Literals in the source** (`css` / `styled` templates, a palette object
     of hex) → **transcribe**. Hashed class names are not the wall. Your
     class names, values into tokens. Put a comment at the top of
     `tokens.css` and `components.css` citing `file:line` (or a palette
     file). Do not write a verdict word there (reconstructed, inspired,
     approximate). See [Limits of a static scan](#limits-of-a-static-scan).
   - **Values only after a function runs** (colour math, a theme helper that
     leaves no literal, conditional composition with no literal left) →
     **stop**, same as Router step 5. Say what is missing. Variant unions may
     be listed as example labels only. A literal table next to that function
     (grid size, named shadows, type variants) is still transcribed.
   - **Utility classes in markup** → CSS exists, it lives in the utilities.
     Extract repeating **combinations** of classes as the specimen, tokenise
     repeated values. Do not turn each utility into its own section.

## What in the code maps where

| In the code | In the libra |
|-------------|--------------|
| Unit imported from more than one file | A section, with `code` pointing at `components.css` |
| File of stories next to a component | Examples inside that section; the set of stories is the section |
| Prop variant (a string union of 2–12 literals, a variants config, `is*`) | An example inside that section |
| Class or custom tag repeated in templates, rule defined in this folder | A section, same traceability as an import |
| Export used from only one file, no stories, no repeated markup | Not a section |
| Hook (`use*`) or a pure function with no JSX / template / decorator | Not a component |
| Literal colour, size, radius in code (including inside `css` / `styled` templates) | A token in `tokens.css`, not a raw value in `components.css` |

If a value does not map cleanly, use the [Mismatch protocol](ENGINE_SKILL.md#mismatch-protocol).

## Layering

- A candidate that does **not** import other candidates → section group
  `Primitives`.
- A candidate that **does** import other candidates → `Blocks`.
- Markup-only candidates (repeated class, no import graph) start as
  `Primitives` unless they clearly compose others.
- Build a block from primitives already in the libra. Do not paste the
  composed markup as one opaque snapshot.

## Styles

| Kind | Where to read |
|------|----------------|
| A neighbouring stylesheet (`styles.*`, `<name>.styles.*` that is CSS, a `styles/` folder, a preprocessor file) | That file |
| `styleUrls` on a decorator, or a `<style>` block in a one-file component | That URL or block |
| `<name>.styles.ts` / `.js` | Literals inside: transcribe (cite `file:line`). Do not copy the file |
| Classes generated at build time | The **built** CSS, not the source template |
| Utility-class markup | Repeating **combinations**; tokenise repeated values |
| Values only after a theme function, colour math, or a hashed class with no literal | See [Limits of a static scan](#limits-of-a-static-scan) |
| Role `base` — prop variants | Published type declarations (`*.d.ts`): literal unions |
| Role `base` — style values | Published modules next to the component (`<Name>.mjs`, `get*Styles.mjs`) |
| Role `base` — theme values | Literal tables in the theme package (grid, heights, overlay) |
| Role `base` — names | The public barrel of that package |

Values go into tokens. Component rules use `var(--*)` — see
[Writing tokens](ENGINE_SKILL.md#writing-tokens) and `check-css.js`.

## Limits of a static scan

Hashed class names are generated at runtime. That does **not** by itself mean
values are missing. Read the source:

- A hex, `px`, or `font-weight` **literal** in a `css` / `styled` template, or
  in a palette file, is a static value. Transcribe it. Cite `file:line` at the
  top of the CSS you write.
- A theme **function** that computes a colour (contrast helpers, hue math)
  and leaves no literal in the file yields names and variant unions only.
  Then **stop**, as on Router step 5, and say what is missing. Do not guess
  the computed colour. Variant unions may be listed as example labels only.
- A **table of literals** in the same package (type variants, named shadows,
  a spacing grid, radii) is not that function. Transcribe the table.

Runtime extraction (render in a browser, read computed styles) is a
different tool. Do not pretend this scanner does that.

If the scan prints `cannot scan <ext>`, those files were not parsed. Read
them by hand with the same mapping table. Do not invent a component the
scanner declined to name.

## Whose layer we document

If the graph shows a **base** package, or that a notable share of candidates
import an **external UI package**, files in this repo are a layer on top of
another system.

Ask **before** writing sections (Intake question 4):

1. **This repository's layer** — sections from candidates in that folder.
2. **The system underneath** — stop filling this folder's wrappers; point
   the codebase path at the resolved base (the scan prints that path) and
   document that package.
3. **Both** — two section groups: base primitives first, then this repo's
   layer on top. Write `design.codebase` as a list of roots with `role`
   `base` / `layer`.

Do not fill `sections.json` without that answer. Title and description of
the libra must match the layer you chose.

## Found but not shown

Classes that exist in `components.css` and do not appear in a section go in
`sections.deferred.json` (`{ "classes": ["…"] }`, optional `why`). That is a
decision. Do not invent components that are not in the scan graph or in a
hand pass over `cannot scan` files.

## Checks

```bash
node tools/scan-codebase.js <folder>
node packages/engine/check-sections.js [path-or-id]
node packages/engine/check-tokens.js [path-or-id]
node packages/engine/check-token-coverage.js [path-or-id]
node packages/engine/check-css.js [path-or-id]
```

`check-token-coverage.js` is silent when `design.themeSources` is missing.
When that list is set (paths relative to a codebase root; skip a file named
`tokens.source.json`), every CSS-like literal in those files must appear as
a **value** in `tokens.css`. Names do not have to match.

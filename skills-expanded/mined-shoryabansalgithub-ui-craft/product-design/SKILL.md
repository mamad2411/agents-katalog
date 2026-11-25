---
name: product-design
description: The product-UI section of ui-craft. A small fixed design system (Inter or Geist, three type sizes inside 12-16px, one weight, one accent) plus the product thinking, states, copy and patterns that make apps, dashboards, tables, forms, settings and onboarding feel finished. Loaded by ui-craft whenever the surface is a product, not a marketing page.
---

# Product design

For anything people use rather than read once: apps, dashboards, tables, forms,
settings, admin panels, internal tools. Landing pages and brand surfaces go
through the main `../SKILL.md` flow instead.

Written for someone who never went to design school. Every value is already
decided below. Your job is to use the tokens, think through the product, and
design the states nobody asked for.

The house rules in `../SKILL.md` still hold and outrank this file: **three type
sizes, no bold, no italics.** The system below is built to satisfy them.

## Load order

| File | What it holds | Load it when |
| --- | --- | --- |
| `references/product-judgment.md` | the six questions before any pixel | first, every time |
| `references/surfaces.md` | the app shell and which surface file to open | before laying out a screen |
| `references/surfaces-{surface}.md` | `dashboard`, `table`, `form`, `detail`, `onboarding` | the screen you are building |
| `references/patterns.md` | every component, as Tailwind classes on these tokens | building any component |
| `references/resilience.md` | empty, loading, error, permission, too much, destructive | before calling a screen done |
| `references/copy.md` | labels, buttons, errors, empty states, dates | writing any string |
| `references/interface-quality.md` | the visual review pass and its checklist | reviewing your own build |
| `references/rules.md` | every hard rule, numbered, with how it is checked | reviewing, or when unsure |
| `references/glossary.md` | plain English for every term used here | any word you do not know |
| `references/coverage-gaps.md` | what this section does not cover, where to go | the brief needs something not listed here |
| `exemplars/pr-*.md` | three worked product changes, start to finish | before your first build with this section |

## Order of operations

1. **Product judgment.** Answer the six questions in `design.md` under
   `## Product`. A blank line means the screen is not ready.
2. **Pinterest gate.** `../SKILL.md` step 1.5 still applies. For product work the
   dimensions are usually `{subject} dashboard`, `{subject} app`, `{subject} ui`.
   The extraction becomes layout and density numbers, not new colours or sizes:
   the system below is fixed.
3. **Install the system.** Copy the block below into the project's main CSS. Do
   not add tokens without a reason written next to them. On a pen.dev canvas,
   run `scripts/pen-variables.js` through `execute` instead (see `../pen.md`).
4. **Open the surface file** and lay out one real screen at ~400px, then desktop.
5. **Build from `patterns.md`.** A component not in it gets specced there first.
6. **Walk `resilience.md`'s checklist.** Every item designed or marked not
   applicable with a reason.
7. **Copy pass** against `copy.md`.
8. **Review** with `interface-quality.md`, at 100% and 200% zoom, light and dark.
9. **Gates** (below). Pasted output, or it is not done.

## The system

Everything a product screen needs, and nothing else. **Tailwind v4.** Copy as is.
Swap `Inter` for `Geist` if you prefer it; swap the accent pair only for a real
brand colour, and re-check contrast when you do.

```css
@import "tailwindcss";

/* Theme switch. With no user toggle, replace `.dark` below with
   `@media (prefers-color-scheme: dark) { :root { ... } }` and drop this line. */
@custom-variant dark (&:where(.dark, .dark *));

:root {
  /* Surfaces: page, then sidebar/table header/wells, then hover/selected-neutral */
  --ui-surface:   #ffffff;
  --ui-surface-2: #f6f7f8;
  --ui-surface-3: #eff0f3;
  /* Lines: decorative dividers, then functional edges (inputs, checkboxes) at 3:1+ */
  --ui-line:        #e2e4e9;
  --ui-line-strong: #828997;   /* 3.52 on surface, 3.10 on surface-3 */
  /* Text: all three clear 4.5:1 on every surface */
  --ui-ink:          #161a22;  /* 17.5 */
  --ui-ink-2:        #4f545f;  /*  7.6 */
  --ui-ink-3:        #656b76;  /*  5.4, 4.7 on surface-3 */
  --ui-ink-disabled: #a7abb4;  /*  2.3, disabled only (WCAG exempt) */
  /* One accent. Fill for the primary button, links, focus, selection */
  --ui-accent:        #1d4fd7; /* 6.65 with white text, 6.65 as text */
  --ui-accent-hover:  #1a45bc;
  --ui-accent-subtle: #ecf1fe; /* selected rows; accent text on it 5.8 */
  --ui-on-accent:     #ffffff;
  /* Status: text colour, and a tint to sit it on. Every pair 5.1+ */
  --ui-danger:          #c52020;
  --ui-danger-hover:    #af1d1d;
  --ui-danger-subtle:   #fef1f1;
  --ui-warning:         #9b5608;
  --ui-warning-subtle:  #fef5e1;
  --ui-success:         #147142;
  --ui-success-subtle:  #ebfaf1;
  /* Elevation: only things that float get a shadow */
  --ui-shadow-float: 0 0 0 1px var(--ui-line), 0 4px 12px -2px rgb(0 0 0 / 0.10);
  --ui-shadow-modal: 0 0 0 1px var(--ui-line), 0 16px 40px -8px rgb(0 0 0 / 0.20);
  --ui-scrim: rgb(0 0 0 / 0.4);
}

.dark {
  /* Surfaces step lighter as they rise. Never pure black */
  --ui-surface:   #121317;
  --ui-surface-2: #191b1f;
  --ui-surface-3: #22252a;
  --ui-line:        #2c2f35;
  --ui-line-strong: #6c727f;   /* 3.8 on surface */
  --ui-ink:          #ebecf0;  /* 15.7 */
  --ui-ink-2:        #acb0b9;  /*  8.5 */
  --ui-ink-3:        #9297a0;  /*  6.3, 5.2 on surface-3 */
  --ui-ink-disabled: #5b5f67;
  --ui-accent:        #5a84f6; /* dark text on it 5.4 */
  --ui-accent-hover:  #779af8;
  --ui-accent-subtle: #1a233d;
  --ui-on-accent:     #121317;
  --ui-danger:          #f47171;
  --ui-danger-hover:    #f58989;
  --ui-danger-subtle:   #361717;
  --ui-warning:         #f5b13d;
  --ui-warning-subtle:  #322815;
  --ui-success:         #4dcb8c;
  --ui-success-subtle:  #162d21;
  /* Shadows barely read on dark; the 1px ring does the work */
  --ui-shadow-float: 0 0 0 1px var(--ui-line), 0 4px 12px -2px rgb(0 0 0 / 0.5);
  --ui-shadow-modal: 0 0 0 1px var(--ui-line), 0 16px 40px -8px rgb(0 0 0 / 0.6);
  --ui-scrim: rgb(0 0 0 / 0.6);
}

@theme inline {
  --color-*: initial;             /* only the colours below exist */
  --color-surface:   var(--ui-surface);
  --color-surface-2: var(--ui-surface-2);
  --color-surface-3: var(--ui-surface-3);
  --color-line:        var(--ui-line);
  --color-line-strong: var(--ui-line-strong);
  --color-ink:          var(--ui-ink);
  --color-ink-2:        var(--ui-ink-2);
  --color-ink-3:        var(--ui-ink-3);
  --color-ink-disabled: var(--ui-ink-disabled);
  --color-accent:        var(--ui-accent);
  --color-accent-hover:  var(--ui-accent-hover);
  --color-accent-subtle: var(--ui-accent-subtle);
  --color-on-accent:     var(--ui-on-accent);
  --color-danger:         var(--ui-danger);
  --color-danger-hover:   var(--ui-danger-hover);
  --color-danger-subtle:  var(--ui-danger-subtle);
  --color-warning:        var(--ui-warning);
  --color-warning-subtle: var(--ui-warning-subtle);
  --color-success:        var(--ui-success);
  --color-success-subtle: var(--ui-success-subtle);
  --color-scrim: var(--ui-scrim);
  --shadow-*: initial;
  --shadow-float: var(--ui-shadow-float);
  --shadow-modal: var(--ui-shadow-modal);
}

@theme {
  --font-sans: "Inter", ui-sans-serif, system-ui, -apple-system, "Segoe UI", sans-serif;
  --font-mono: "Geist Mono", ui-monospace, "SF Mono", Menlo, monospace;

  /* Three sizes. Nothing else can be typed by reflex */
  --text-*: initial;
  --text-xs:   0.75rem;  --text-xs--line-height:   1rem;     /* 12 / 16 */
  --text-sm:   0.875rem; --text-sm--line-height:   1.25rem;  /* 14 / 20 */
  --text-base: 1rem;     --text-base--line-height: 1.5rem;   /* 16 / 24 */

  /* One weight */
  --font-weight-*: initial;
  --font-weight-normal: 400;

  /* Three radii plus rounded-full */
  --radius-*: initial;
  --radius-sm: 0.25rem;   /*  4: badges, checkboxes, kbd */
  --radius-md: 0.375rem;  /*  6: buttons, inputs, menu items */
  --radius-lg: 0.5rem;    /*  8: cards, menus, popovers, dialogs, toasts */

  /* Two breakpoints */
  --breakpoint-*: initial;
  --breakpoint-sm: 40rem;  /*  640: phone to tablet */
  --breakpoint-lg: 64rem;  /* 1024: sidebar appears */

  --ease-out: cubic-bezier(0.2, 0, 0, 1);
}

@layer base {
  html { font-family: var(--font-sans); background: var(--color-surface); color: var(--color-ink);
         -webkit-font-smoothing: antialiased; }
  /* body repeats the ground: a checker that starts at <body> must see it */
  body { background: var(--color-surface); font-size: var(--text-sm); line-height: var(--text-sm--line-height); }
  strong, b { font-weight: inherit; color: var(--color-ink); }  /* no bold, per house rule 2 */
  table, [data-numeric] { font-variant-numeric: tabular-nums; }
  :focus-visible { outline: 2px solid var(--color-accent); outline-offset: 2px; }
  ::selection { background: var(--color-accent-subtle); }
}
```

### Type: three roles

| Class | Size / line | Used for |
| --- | --- | --- |
| `text-base` | 16 / 24 | the page title, dialog titles, settings section titles. One per region. Inputs on phones (below 16px, iOS zooms) |
| `text-sm` | 14 / 20 | almost everything: body, buttons, inputs, table cells, nav, tabs, menu items |
| `text-xs` | 12 / 16 | table headers, helper text, field errors, timestamps, badges, counts, shortcut hints |

**The hierarchy ladder, since there is no bold.** Four rungs from three sizes and
three inks. Read top to bottom:

```
text-base text-ink     page title
text-sm   text-ink     the content: names, values, what you came for
text-sm   text-ink-2   supporting: descriptions, inactive nav, secondary columns
text-xs   text-ink-3   metadata: dates, IDs, counts, helper text
```

Never skip straight from rung 1 to rung 4 in one block; never use two rungs that
look the same for two different meanings.

### Space

Tailwind's default 4px step. **Allowed steps only:** `0 px 1 2 3 4 6 8 12 16 24`
(0, 1, 4, 8, 12, 16, 24, 32, 48, 64, 96px).

| Between | Step |
| --- | --- |
| icon and its label, items inside one control | `2` (8) |
| label and field, title and its description | `2` (8) |
| fields in a form, rows in a list of cards | `4` (16) |
| groups inside a page | `6` or `8` (24, 32) |
| page padding | `6` (24) desktop, `4` (16) phone |

**More space around a group than inside it.** That single rule does most of the
grouping work bold would have done.

### Sizes

| Thing | Size |
| --- | --- |
| control height (button, input, select) | `h-8` (32), `pointer-coarse:h-10` (40) on touch |
| compact control (toolbars, inside table rows) | `h-7` (28), mouse only |
| table row | `h-10` (40), `h-8` (32) when the user picks compact |
| icon | `size-4` (16) everywhere; `size-6` (24) only in empty states |
| icon button | `size-8` (32), same hit area as a button |
| sidebar | `w-60` (240) |
| top bar, page header | `h-12` (48) |
| form column | `max-w-xl` (576) |
| confirm dialog / form dialog | `max-w-md` (448) / `max-w-lg` (512) |
| hit area floor | 24x24 mouse, 40x40 touch |

### Borders, not shadows

Flat surfaces are separated by `border-line` or a surface step (`surface` to
`surface-2`), never by a shadow. **Only floating things get `shadow-float`**
(menus, popovers, toasts) or **`shadow-modal`** (dialogs, sheets). Inputs and
checkboxes use `border-line-strong` because their edge is the only thing that
identifies them.

### Motion

`duration-120 ease-out` for hover, colour, press. `duration-180 ease-out` for
anything that opens (menu, popover, dialog). Exits use 120. Animate `opacity` and
`transform` only. Every animation carries `motion-reduce:transition-none`.

### Colour: where each one goes

| Token | Where | Never |
| --- | --- | --- |
| `accent` | the primary button, links, focus ring, selected state, progress | decoration, icons that do nothing, more than one filled button per view |
| `danger` | destructive buttons, errors, failed status | warnings, "important" |
| `warning` | needs attention soon, degraded | errors |
| `success` | completed, healthy, paid | "good" decoration |
| `*-subtle` | the tint behind the matching colour's text (badges, banners, selected rows) | on its own as a background colour |

Status is never colour alone: pair it with an icon or a word.

## Gates

On a product surface, four checks. All output pasted.

```bash
python3 ../scripts/validate_reference.py PROJECT
python3 ../scripts/validate_bans.py SOURCE --register product
python3 ../scripts/validate_bans.py --dom manifest.json --register product   # contrast, measure: static cannot see them
python3 ../scripts/validate_resolution.py PROJECT --register product
python3 scripts/validate_product.py SOURCE
```

`validate_product.py` holds this system: sizes outside 12/14/16, weights above
400, off-scale spacing, radii and shadows outside the three and two above, fonts
other than Inter/Geist/system, breakpoints other than `sm` and `lg`, `uppercase`,
and `<strong>`/`<b>` without the no-bold reset.

**No waivers.** 12/14/16 is closer than the 1.25x step `flat-type-hierarchy`
asks for (14 to 16 is 1.14x), but both modes exempt a pair that is 2px or more
apart at a 0.70-0.90 ratio, and 12 to 14 and 14 to 16 are both that. So the ban
passes on its own terms, and still fires the moment a 13 or a 15 creeps in.
Hierarchy has to come from the ladder above.

**`step-monotony` is off here** (`--register product`). With three sizes, the
body size carries most of any real screen, so a size-only share check fails
honest product pages. Nothing measures the ink ladder in its place yet, which
makes the ladder check in `interface-quality.md` the one to walk by eye.

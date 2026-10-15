---
name: decard
description: Find and remove card-based UI container components — shadcn/MUI/Bootstrap/Vuetify/Ant/Chakra Card, elevated "box" panels, bordered-and-shadowed wrappers — and flatten them into section + heading + divider layouts. Also prevents reaching for card containers when building new UI. Use when the user says "remove cards", "no cards", "no card containers", "flatten cards", "decard", "de-card", "find cards", "de-overlay", "too boxy", or wants a flatter / less-boxed design. Keeps structural borders on tables, lists, and code blocks.
---

# decard — flatten card-based containers

A card container is a **box that wraps a section of content** purely to elevate
it: rounded corners + border + (usually) a shadow, with a header/title slot and
a body slot. It adds a visual frame the content does not need. `decard` removes
that frame and lets content sit flat on the page, separated by headings and thin
rules instead of stacked boxes.

Two modes, both driven by this one rule set:

- **Remove** — find existing card containers and flatten them.
- **Prevent** — when building or reviewing UI, do not introduce card containers
  in the first place.

## What counts as a card container (remove these)

- Component libraries: `<Card>` / `<CardHeader>` / `<CardContent>` / `<CardTitle>`
  (shadcn/ui), `<Mui Card>` / `<CardContent>` (MUI), `<v-card>` (Vuetify),
  `<el-card>` (Element), `<a-card>` (Ant), `<Card>` (Chakra/Mantine),
  `<mat-card>` (Angular Material), Bootstrap `class="card"`.
- Hand-rolled equivalents: a wrapper `<div>` whose only job is
  `rounded-* border … shadow…` (or `bg-card` / `bg-white` + `shadow`) around a
  titled block of content.

## What to KEEP (do NOT strip these)

Flattening ≠ removing every border. Keep structural borders where content would
otherwise run together or look broken:

- **Tables** — keep their `border` + `rounded` frame.
- **Lists of rows** — keep one outer `border` + `divide-y` (a single divided
  list reads better than N boxes; collapse a grid of identical cards into this).
- **Code blocks / pre** — keep their frame.
- **Inputs / textareas** — keep their border.
- **A single stat strip** — one bordered grid is fine; a wall of stat boxes is not.

The test: does the border separate genuinely different data, or does it just
gift-wrap a paragraph + heading? Wrap → cut it. Separate data → keep it.

## Flatten recipe

Replace:

```
<Card>
  <CardHeader>
    <CardTitle>Title</CardTitle>
    <CardDescription>Subtitle</CardDescription>
  </CardHeader>
  <CardContent> …content… </CardContent>
</Card>
```

with:

```
<section className="space-y-4">
  <div className="space-y-1">
    <h2 className="text-base font-semibold">Title</h2>
    <p className="text-sm text-muted-foreground">Subtitle</p>
  </div>
  …content…
</section>
```

- Separate sections with generous spacing (`space-y-8` / `space-y-10`) and/or a
  single hairline `<Separator />` between major groups — not a box each.
- A **grid of identical cards** → one bordered `<ul>` with `divide-y` rows.
- The card's title becomes a plain heading that sits **above** the content, not
  inside a frame.
- Drop elevation: remove `shadow-*` on any panel that survives. If the project
  has a shared `Card` primitive, deleting its `shadow` de-boxes everything at once.
- After flattening, remove now-unused `Card*` imports.

## How to find them

Search the codebase / current diff (adapt globs to the stack):

```
rg -n "<Card[ >]|Card(Header|Content|Title|Description|Footer)|<v-card|<el-card|<a-card|<mat-card|class=\"card\"|className=\"[^\"]*\\bcard\\b" \
  --glob '!**/node_modules/**'
```

Also flag hand-rolled boxes — wrappers matching `rounded-\w+ .*\bborder\b.*\bshadow` that contain a heading + prose. Report each as `path:line` with what it wraps.

## Steps

1. **Find** every card container (and hand-rolled box wrapper). List them.
2. For each, decide **flatten vs keep** with the test above.
3. **Flatten** with the recipe; preserve inner tables/lists/code frames.
4. **Collapse** grids of identical cards into one divided list.
5. **Clean up** unused imports; if a shared `Card` primitive is now unused, say so
   (offer to delete it, don't silently remove a library primitive).
6. **Verify**: build / type-check; eyeball that sections are separated by spacing
   and rules, not nested boxes, and that tables/lists kept their frames.

## Prevent (when building new UI)

- Reach for a `<section>` + heading + spacing first. Only add a border when it
  frames a table, a divided list, a code block, or an input.
- Never wrap a heading + paragraph + buttons in a bordered/shadowed box "for
  structure" — spacing and a heading already give structure.
- No nested cards, ever (a card inside a card is two frames too many).

## Boundary

This skill governs container chrome, not information. Do not delete content,
data, controls, or accessibility affordances — only the box around them. If a
"card" is actually a meaningful interactive unit (a selectable tile, a draggable
item, a clickable result with its own hover state), keep it; flatten the
decorative panels, not the functional ones.

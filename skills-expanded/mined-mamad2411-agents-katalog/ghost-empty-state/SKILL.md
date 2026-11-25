---
name: ghost-empty-state
description: Generate empty-state UI (no data / nothing to show) as a self-contained inline SVG illustration in TSX, built by "ghosting" the real component it replaces — same shape, radius, dividers, icons, dots — at decreasing monochrome opacity, plus one quiet marker. Use whenever the user asks for an empty state, a "no data" / "no results" / "nothing here" screen, a placeholder for an empty list/table/inbox/calendar, or says "add an empty state" or "what happens when there's nothing". Always prefer this technique over a generic stock illustration, a crossed-out box icon, or a plain "No items found" text block.
---

# Ghost Empty State

An empty state should look like a **quieter version of the real UI**, not a random illustration dropped in when data is missing. This skill builds empty states by tracing the actual row/card/item shape the list would normally render, redrawing it 2–3 times as a monochrome "ghost", fading it toward nothing, and adding one small marker that says "empty" without shouting it.

## When to use this

- The user asks for an empty state, "no results", "no data", "nothing scheduled", an empty inbox/table/list/calendar/search view.
- Any list, table, or card grid needs a fallback for the zero-items case.
- Do **not** reach for a generic icon library glyph (open box, empty folder, magnifying glass) or a stock illustration as the default — build the ghost version described here instead, unless the user explicitly asks for an icon/illustration style.

## Method

1. **Look at the real component first.** Before drawing anything, find (or ask for) the actual row/card/item this empty state replaces. Note its concrete shape: corner radius, height, internal structure (leading label? avatar? divider line? trailing badge/dot?), and what visual system it already uses (opacity-based monochrome, colored tags, borders, etc.). The ghost must reuse *that* vocabulary — don't invent a new visual style for the empty state.
2. **Redraw that shape 2–3 times as flat SVG primitives** (`rect` for the row body, `line` for internal dividers, `circle` for dots/avatars/badges) — not the real interactive component, just its silhouette.
3. **Fade each repetition toward the background**, top to bottom (or first to last): e.g. `fillOpacity` 0.08 → 0.05 → 0.03, dividers/dots roughly double that. This mimics a scrollable list trailing off, and reads as "this is where items would be" rather than decoration.
4. **Add exactly one quiet marker** signaling absence — a dashed circle or dashed shape, low opacity (~0.2), no fill. Don't add a second marker or an emoji; one signal is enough.
5. **Everything in `currentColor` + opacity**, nothing hardcoded. This is what makes it free in light/dark mode and consistent with a monochrome/opacity-based design system (see the row-opacity conventions below). If the host app uses a different color system (e.g. real brand colors, not opacity scale), adapt: keep the "ghost the real shape, fade it out, one quiet marker" method, but swap in that app's actual muted tokens instead of `currentColor`/opacity.
6. **Wrap in the same container language as the real list** — if the list lives in `rounded-xl border`, the empty state should too (often `border-dashed` to read as a placeholder state rather than populated content).
7. **Copy: one noun-phrase title, one calm sentence.** State what's missing plainly ("No courses scheduled", "No results for this filter") — no apology, no exclamation mark, no "Oops!". If the empty state is actionable (user can add the first item), the description can say what to do next, still in plain, active language.

## Reference implementation

Row/list example — 3 ghosted rows (rounded rect + divider + dot) fading out, plus a dashed circle marker:

```tsx
'use client'

interface EmptyStateProps {
  title: string
  description: string
}

export function EmptyState({ title, description }: EmptyStateProps) {
  return (
    <div className="flex flex-col items-center justify-center gap-6 rounded-xl border border-dashed border-foreground/15 px-6 py-16 text-center">
      <svg width="140" height="104" viewBox="0 0 140 104" fill="none" className="text-foreground">
        {/* row 1 — closest to "real", highest opacity */}
        <rect x="10" y="8" width="120" height="26" rx="8" fill="currentColor" fillOpacity="0.08" />
        <rect x="10" y="8" width="120" height="26" rx="8" stroke="currentColor" strokeOpacity="0.12" />
        <line x1="34" y1="21" x2="96" y2="21" stroke="currentColor" strokeOpacity="0.15" />
        <circle cx="112" cy="21" r="2" fill="currentColor" fillOpacity="0.15" />

        {/* row 2 — fading */}
        <rect x="10" y="39" width="120" height="26" rx="8" fill="currentColor" fillOpacity="0.05" />
        <line x1="34" y1="52" x2="88" y2="52" stroke="currentColor" strokeOpacity="0.1" />
        <circle cx="104" cy="52" r="2" fill="currentColor" fillOpacity="0.1" />

        {/* row 3 — nearly gone */}
        <rect x="10" y="70" width="120" height="26" rx="8" fill="currentColor" fillOpacity="0.03" />
        <line x1="34" y1="83" x2="80" y2="83" stroke="currentColor" strokeOpacity="0.06" />
        <circle cx="96" cy="83" r="2" fill="currentColor" fillOpacity="0.06" />

        {/* the one quiet "empty" marker, centered over the stack */}
        <circle cx="70" cy="52" r="16" stroke="currentColor" strokeOpacity="0.2" strokeDasharray="3 4" />
      </svg>

      <div className="grid gap-1">
        <p className="text-sm font-medium text-foreground/70">{title}</p>
        <p className="text-xs text-foreground/40">{description}</p>
      </div>
    </div>
  )
}
```

## Adapting to a different item shape

The exact SVG above is for a horizontal row (time/label + divider + name + dot) — the shape used in the original list. For a different layout, re-derive it from the real component instead of reusing these coordinates verbatim:

- **Cards in a grid** → ghost 2–4 small squares/rects with rounded corners, arranged in a grid, fading by row or by distance from the marker, instead of stacked rows.
- **Avatars/contacts list** → ghost a leading `circle` (avatar) + two short `rect`/`line` shapes (name + subtitle) per row, no divider line.
- **Table rows** → ghost thin full-width `rect`s (rows) plus a few vertical `line`s (column separators) rather than one big rounded rect per row.
- **Calendar/timeline** → ghost a few short vertical or horizontal bars at decreasing opacity along the timeline axis, marker centered or at "today".

Always keep: (a) 2–3 repetitions, not more — it should read as a rhythm, not a busy illustration; (b) monotonic fade; (c) exactly one dashed/quiet marker; (d) `currentColor` + opacity only, no new colors introduced.